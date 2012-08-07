# -*- coding: utf-8 -*-

#    This is a Python open source project for migration of modules
#    and functions from GestionPyme and other ERP products from Sistemas
#    Ágiles.
#
#   Copyright (C) 2012 Sistemas Ágiles.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Alan Etkin <spametki@gmail.com>"
__copyright__ = "Copyright (C) 2012 Sistemas Ágiles"
__license__ = "AGPLv3"

# THIS FILE IS DUPLICATED
# (gui2py and web2py apps)
# REMEMBER TO COPY CHANGES
# TO BOTH FILES TO KEEP THE
# DATABASE AND FUNCTIONS
# DEFINITIONS

from gluon import *
import datetime

# table/field functions

# This intends to prevent PostgreSQL table creation errors

# 'auth_user', 'auth_group', 'auth_membership', 'auth_permission', 'auth_event', 'auth_cas', 

# Static table_name: group dictionary for readable table lists
STATIC_TABLE_TAGS = {'accounting_period':'accounting', 'category': 'common', \
'subcategory': 'common', 'jurisdiction': 'common', 'country':'common', \
'state': 'common', 'city': 'common', 'address': 'common', 'tax': 'common', \
'custom_serial_code': 'common', 'debugging': 'common', 'option': 'common', \
'customer_group': 'crm', 'situation': 'crm', 'cost_center': 'financials', \
'bank': 'financials', 'plant': 'hr', 'department': 'hr', 'labor_union': 'hr', \
'payroll': 'hr', 'healthcare': 'hr', 'pension': 'hr', 'role': 'hr', \
'formula': 'hr', 'agreement': 'hr', 'price_list': 'operations', \
'point_of_sale': 'operations', 'collection': 'scm', 'color': 'scm', \
'size': 'scm', 'warehouse': 'scm', 'rate': 'scm', 'account': 'accounting', \
'journal_entry': 'accounting', 'staff_category': 'hr', 'staff': 'hr', \
'entry': 'accounting', 'salesperson': 'crm', 'file': 'hr', 'relative': 'hr', \
'supplier': 'scm', 'family': 'scm', 'concept': 'operations',  \
'fund': 'financials', 'payment_terms': 'financials', \
'payment_method': 'financials', 'checkbook': 'financials', 'payroll_new': 'hr', \
'salary': 'hr', 'document': 'operations', 'product_structure': 'scm', \
'stock': 'scm', 'customer': 'crm', 'subcustomer': 'crm', 'fee': 'fees', \
'contact': 'crm', 'installment': 'fees', 'quota': 'fees', \
'operation': 'operations', 'price': 'operations', 'memo': 'crm', \
'contact_user': 'crm', 'bank_check': 'financials', 'cash_balance': 'financials', \
'payroll_column': 'hr', 'movement': 'operations', 'reconciliation': 'financials', \
'credit_card_coupon': 'financials'}


def define_tables(db, auth, env, web2py = False, migrate = True, fake_migrate = False, T = lambda t: t):

    # custom serial code creation. Include plain text between \t tab chars: "A\tThis is not randomized\tBN"
    # A: alphabetical, B: alphanumeric, N: integers between zero and nine, \t [text] \t: normal text bounds
    # To include "A", "B", "N" use the \tA\t syntax. Auxiliar characters are allowed outside \t \t separators
    # As expected, no \t characters are allowed inside escaped text
    # TODO: Simplify/standarize serial code pseudo-syntax for user html form input

    # Env is globals() for web2py environment and custom shell env instance for desktop app
    # bind translator instance name
    T = env["T"]

    CUSTOM_SERIAL_CODE_STRUCTURE = "AAAA-NNNN-BBBBBB"
    def new_custom_serial_code(structure=CUSTOM_SERIAL_CODE_STRUCTURE):
        import random
        def generate_custom_serial_code(s):
            tmpstring = ""
            skip = False
            for element in s:
                if not skip:
                    if element == "A":
                        element = random.choice([char for char in \
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random char
                    elif element == "N":
                        element = random.randint(0,9) # get random integer
                    elif element == "B":
                        element = random.choice([char for char in \
                        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random alphanumeric
                    elif element == "\t":
                        skip = True
                        continue
                else:
                    if element == "\t":
                        skip = False
                        continue
                tmpstring += str(element)
            return tmpstring

        while True:
            the_code = generate_custom_serial_code(structure)
            if len(db(db.custom_serial_code.code == the_code).select()) <= 0:
                # store serial code in db
                db.custom_serial_code.insert(code = the_code)
                return the_code

        return None


    # login/register forms
    
    def custom_post_login(arg):
        contacts_per_user = len(db(db.contact_user.user_id == auth.user_id).select())
        if contacts_per_user < 1:
            redirect(URL(a="erplibre", c="registration", f="post_register_specify_firm"))

    def custom_post_register(arg):
        redirect(URL(a="erplibre", c="registration", f="post_register_specify_firm"))

    def today():
        return datetime.date.today()

    def now():
        return datetime.datetime.now()

    def price_format(price):
        try:
            r = "%s - %s" % (price.concept_id.description, price.price_list_id.description)
        except (ValueError, KeyError, AttributeError, IndexError, RuntimeError):
            r = "Format error. price index " + str(price.price_id)
        return r

    def operation_format(r):
        try:
            of = "%s %s" % (db.document[r.document_id].description, r.operation_id)
        except (AttributeError, KeyError, ValueError, TypeError):
            of = "Format error: operation %s" % r.operation_id
        return of

    if not web2py:
        # Auth tables
        db.define_table("auth_user", \
        Field("first_name", label = T("first name")), \
        Field("last_name", label = T("last name")), \
        Field("email", label = T("email")), \
        Field("password", label = T("password")), \
        Field("registration_key", label = T("registration key")), \
        Field("reset_password_key", label = T("reset password key")), \
        migrate=migrate, fake_migrate=fake_migrate, sequence_name = "auth_user_id_Seq")

    else:
        # auth settings
        auth.settings.register_onaccept = custom_post_register
        auth.settings.login_onaccept = custom_post_login


    auth.define_tables(migrate = migrate, fake_migrate = fake_migrate) # creates all needed tables

    # Create tables before reference definitions based in STATIC_TABLE_NAMES
    # Raises a psycopg2 error with PostgreSQL
    # (not used)
    if False:
        for table_name in STATIC_TABLE_NAMES:
            sequence_name = table_name + "_id_Seq"
            db.define_table(
            '%s' % table_name,
            Field('%s_%s' % (table_name, "id"), "id"),
            sequence_name = '%s' % sequence_name,
            format='%(description)s',
            migrate=migrate, fake_migrate=fake_migrate,
            )

    # db_00_accounting

    # Accounting period, fiscal year (FY) "Ejercicios"
    db.define_table('accounting_period',
        Field('accounting_period_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, label = T("description")),
        Field('starting', type='date', label = T("starting")),
        Field('ending', type='date', label=T("ending")), # translation test
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "accounting_period_accounting_period_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate,
        )

    # db_00_common

    # tables used both in sales, purchases, etc.

    # product main category
    db.define_table('category',
        Field('category_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=20, label = T("description")),
        Field('products', type='boolean', default=False, label = T("products")),
        Field('units', type='boolean', default=False, label = T("units")), # ¿unidades?
        Field('times', type='boolean', default=False, label = T("times")), # ¿tiempos?
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "category_category_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # product sub category
    db.define_table('subcategory',
        Field('subcategory_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, label = T("description")),
        Field('category_id', 'reference category', label = T("category")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "subcategory_subcategory_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('jurisdiction',
        Field('jurisdiction_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "jurisdiction_jurisdiction_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # country?
    db.define_table('country',
        Field('country_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "country_country_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # states/province/district
    db.define_table('state',
        Field('state_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('country_id', 'reference country', label = T("country")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "state_state_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # city?
    db.define_table('city',
        Field('city_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('city', type='string', length=50, label = T("city")),
        Field('state_id', 'reference state', label = T("state")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "city_city_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # Address?
    db.define_table('address',
        Field('address_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('street', type='string', label = T("street")),
        Field('number', type='string', length=50, label = T("number")),
        Field('other', type='string', length=200, label = T("other")), # whatever else comes here
        Field('zip_code', type='string', length=9, label = T("zip code")), # Argentina's CPA
        Field('city_id', 'reference city', label = T("city")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "address_address_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # tax category
    db.define_table('tax',
        Field('tax_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('tax', 'boolean', label = T("tax")), # Argentina's CUIT (yes/no)
        Field('percentage', type='double', label = T("percentage")),
        Field('aliquot', type='double', label = T("aliquot")),
        Field('category', label = T("category")), # vat type
        Field('abbr', type='string', length=3, label = T("abbr")),
        Field('discriminate', type='boolean', default=False, label = T("discriminate")),
        Field('document_sales_id', 'integer', label = T("document sales")),  # reference
        Field('document_purchases_id', 'integer', label = T("document purchases")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "tax_tax_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)


    # custom serial code table for validation purposes
    db.define_table('custom_serial_code',
        Field('custom_serial_code_id', 'id', label = T("id")),
        Field('code', unique=True, label = T("code")),
        Field('replica', 'boolean', default=True, label = T("replica")),
        sequence_name = "custom_serial_code_custom_serial_code_id_Seq",
        format='%(code)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # debugging entries
    db.define_table('debugging',
        Field('debugging_id', 'id', label = T("id")),
        Field('msg', 'text', label = T("msg")),
        sequence_name = "debugging_debugging_id_Seq",
        format='%(msg)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # erplibre options
    db.define_table('option',
        Field('option_id', 'id', label = T("id")),
        Field('name', unique=True, requires=IS_NOT_EMPTY(), label = T("name")), # "option_1"
        Field('args', label = T("args")), # a value to perform name-args searches (i.e. id or id1 | ... idn)
        Field('description', label = T("description")),
        Field('type', requires=IS_NOT_EMPTY(), default = 'string', label = T("type")), # a valid dal field type
        Field('represent', label = T("represent")),
        Field('requires', label = T("requires")),
        Field('value', 'text', label = T("value")),
        format='%(name)s',
        sequence_name = "option_option_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_00_crm

    # groups
    db.define_table('customer_group',
        Field('customer_group_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "customer_group_customer_group_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # status (active, unactive, prospect, etc.)
    db.define_table('situation',
        Field('situation_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "situation_situation_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_00_financials

    # cost center
    db.define_table('cost_center',
        Field('cost_center_id', 'id', label=T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('addition', type='datetime', label = T("addition")),
        Field('deletion', type='datetime', label = T("deletion")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "cost_center_cost_center_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # banks "Bancos"
    db.define_table('bank',
        Field('bank_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=250, label = T("description")),
        Field('bank_check', label = T("bank check")),  # reference
        Field('concept_id', 'integer', label = T("concept")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "bank_bank_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_00_hr

    db.define_table('plant',
        Field('plant_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "plant_plant_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('department',
        Field('department_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "department_department_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('labor_union',
        Field('labor_union_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('percentage', type='integer', default=0, comment=T('Personal percentage for the union'), label = T("percentage")),
        Field('patronal', type='integer', default=0, comment=T('Employer percentage for the union'), label = T("patronal")),
        Field('voluntary', type='integer', default=0, comment=T('Voluntary contribution'), label = T("voluntary")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "labor_union_labor_union_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('payroll',
        Field('payroll_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', comment=T('Type and period'), label = T("description")),
        Field('type', type='string', length=1, label = T("type")),  # reference?
        Field('half_bonus', type='boolean', default=False, label = T("half bonus")),
        Field('vacations', type='boolean', default=False, label = T("vacations")),
        Field('starting', type='datetime', label = T("starting")),
        Field('ending', type='datetime', label = T("ending")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "payroll_payroll_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('healthcare',
        Field('healthcare_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('percentage', type='integer', default=0, comment=T('Contribution percentage'), label = T("percentage")),
        Field('patronal', type='integer', default=0, comment=T('Patronal contribution'), label = T("patronal")),
        Field('voluntary', type='integer', default=0, comment=T('Voluntary contribution'), label = T("voluntary")),
        Field('adherent', type='integer', default=0, comment=T('Aporte por Adherente'), label = T("adherent")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "healthcare_healthcare_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('pension',
        Field('pension_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('percentage', type='double', comment=T('Personal contribution'), label = T("percentage")),
        Field('contribution', type='integer', default=0, comment=T('Employer contribution'), label = T("contribution")),
        Field('social_services', type='integer', default=0, label = T("social services")), # Argentina: law number 19032
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "pension_pension_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('role',
        Field('role_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "role_role_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('formula',
        Field('formula_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('name', type='string', length=50, label = T("name")),
        Field('quantity', type='text', label = T("quantity")),
        Field('amount', type='double', label = T("amount")),
        Field('datum', type='double', label = T("datum")),
        Field('format', type='string', length=1, label = T("format")),  # reference?
        Field('text', type='text', label = T("text")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "formula_formula_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('agreement',
        Field('agreement_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('text', type='text', label = T("text")),
        Field('amount', type='double', label = T("amount")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "agreement_agreement_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_00_operations

    # pricelists
    db.define_table('price_list',
        Field('price_list_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('entry', type='boolean', default=False, label = T("entry")),
        Field('exit', type='boolean', default=False, label = T("exit")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "price_list_price_list_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # points of sale
    db.define_table('point_of_sale',
        Field('point_of_sale_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('branch', label = T("branch")),
        Field('number', type='integer', default=0, label = T("number")),
        Field('authorization_code', type='string', length=50, label = T("authorization code")), # Argentina's CAI (invoice printing official number)
        Field('due_date', type='datetime', label = T("due date")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "point_of_sale_point_of_sale_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)


    # db_00_scm

    # collections "Colecciones"
    db.define_table('collection',
        Field('collection_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('starting', type='date', label = T("starting")),
        Field('ending', type='date', label = T("ending")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "collection_collection_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # colours (products 1st variant)
    db.define_table('color',
        Field('color_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "color_color_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # sizes (products 2nd variant ) ie. clothes...
    db.define_table('size',
        Field('size_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('type', label = T("type")),
        Field('order_number', 'integer', label = T("order number")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "size_size_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # warehouses
    db.define_table('warehouse',
        Field('warehouse_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('address', type='string', length=50, label = T("address")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "warehouse_warehouse_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # rates / fare / tariff
    db.define_table('rate',
        Field('rate_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('type', type='string', length=1, label = T("type")),  # reference?
        Field('capacity', type='double', label = T("capacity")),
        Field('measure', type='string', length=1, label = T("measure")),
        Field('stock', type='integer', default=0, label = T("stock")),
        Field('index_value', type='double', default=0, label = T("index value")),
        Field('price', type='double', default=0, label = T("price")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "rate_rate_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_01_accounting

    # Account (higher level of Chart of Accounts) "Cuentas"
    db.define_table('account',
        Field('account_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, label = T("description")),
        Field('receives', type='boolean', default=False, label = T("receives")),
        Field('customer_group_id', 'reference customer_group', label = T("customer group")), # reference
        Field('bank_id', 'reference bank', label = T("bank")), # reference
        Field('tax', type='boolean', default=False, label = T("tax")),
        Field('gross_receipts', type='boolean', default=False, label = T("gross receipts")), # ¿iibb?
        Field('collections', type='boolean', default=False, label = T("collections")), # ¿percepciones?
        Field('retentions', type='boolean', default=False, label = T("retentions")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "account_account_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # Journal entry "Asientos"
    db.define_table('journal_entry',
        Field('journal_entry_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, comment=T('Description'), label = T("description")),
        Field('number', type='integer', default=0, label = T("number")),
        Field('posted', type='datetime', default=now, label = T("posted")),
        Field('source', label = T("source")),
        Field('valuation', type='datetime', label = T("valuation")),
        Field('type', type='string', length=1, label = T("type")), # reference?
        Field('draft', type='boolean', default=False, label = T("draft")),
        Field('accounting_period_id', 'reference accounting_period', label = T("accounting period")), # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "journal_entry_journal_entry_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_01_hr

    db.define_table('staff_category',
        Field('staff_category_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('salary', type='double', label = T("salary")),
        Field('hourly', type='double', label = T("hourly")),
        Field('type', type='string', length=1, label = T("type")),  # reference?
        Field('journalized', type='boolean', default=False, label = T("journalized")),
        Field('addition', type='datetime', label = T("addition")),
        Field('deletion', type='datetime', label = T("deletion")),
        Field('agreement_id', 'reference agreement', label = T("agreement")),  # reference
        Field('plant_id', 'reference plant', label = T("plant")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "staff_category_staff_category_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('staff',
        Field('staff_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('staff_category_id', 'reference staff_category', label = T("staff category")), # reference
        Field('name', type='string', length=40, label = T("name")),
        Field('addres', type='string', length=40, label = T("address")),
        Field('city_id', 'reference city', label = T("city")), # reference
        Field('zip_code', type='string', length=4, label = T("zip code")),
        Field('state_id', 'reference state', label = T("state")),  # reference
        Field('telephone', type='string', length=12, label = T("telephone")),
        Field('birth', type='datetime', label = T("birth")),
        Field('id_number', type='string', length=15, label = T("id number")), # (Argentina's DNI)
        Field('nationality_id', 'reference country', label = T("nationality id")), # reference country
        Field('tax_identification', type='string', length=13, label = T("tax identification")), # ¿cuil? (note: taxid != CUIT)
        Field('sex', type='string', length=1, label = T("sex")),
        Field('marital_status', type='string', length=1, label = T("marital status")),
        Field('addition', type='datetime', label = T("addition")),
        Field('deletion', type='datetime', label = T("deletion")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "staff_staff_id_Seq",
        format='%(name)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_02_accounting

    # entry item (posting) "Partidas"
    db.define_table('entry', # revisar: ¿"Partida"?
        Field('entry_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', type='string', length=50, label = T("description")),
        Field('journal_entry_id', 'reference journal_entry', label = T("journal entry")), # reference
        Field('account_id', 'reference account', label = T("account")), # reference
        Field('type', type='string', length=1, label = T("type")), # reference?
        Field('amount', type='double', label = T("amount")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "entry_entry_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_02_crm

    # salesperson
    db.define_table('salesperson',
        Field('salesperson_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('staff_id', 'reference staff', label = T("staff")), # reference
        Field('commission', type='double', label = T("commission")),
        Field('telephone', type='string', length=50, label = T("telephone")),
        Field('address', type='string', length=50, label = T("address")),
        Field('state_id', 'reference state', label = T("state")),  # reference
        Field('city_id', 'reference city', label = T("city")),  # reference
        Field('notes', type='text', label = T("notes")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "salesperson_salesperson_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_02_hr

    db.define_table('file',
        Field('file_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('staff_id', 'reference staff', label = T("staff")),  # reference
        Field('extra_hours', type='double', label = T("extra hours")),
        Field('presenteesm', type='double', comment=T('Presenteesm amount'), label = T("presenteesm")), # ¿presentismo?
        Field('government_increase', type='double', comment=T('salary extra by statal dispositions (divided by months)'), label = T("government increase")),
        Field('sick_days', type='integer', default=0, comment=T('Number of sick days'), label = T("sick days")),
        Field('presenteesm_discount', type='double', label = T("presenteesm discount")),
        Field('failure', type='double', comment=T('Failure discount'), label = T("failure")),
        Field('contribution_discount', type='double', label = T("contribution discount")),
        Field('seniority', type='double', label = T("seniority")),
        Field('per_diem', type='double', comment=T('Per diem amount'), label = T("per diem")),
        Field('profit_percentage', type='double', label = T("profit percentage")),
        Field('schooling', type='integer', default=0, comment=T('Schooling help: number of children'), label = T("schooling")),
        Field('allowance', type='integer', default=0, comment=T('Number of children for annual allowance'), label = T("allowance")),
        Field('paid_vacation', type='double', label = T("paid vacation")),
        Field('half_bonus', type='double', comment=T('Half bonus amount'), label = T("half bonus")),
        Field('prenatal', type='integer', default=0, label = T("id")),
        Field('staff_category_id', 'reference staff_category', label = T("staff category")),  # reference
        Field('healthcare_id', 'reference healthcare', label = T("healthcare")),  # reference
        Field('labor_union_id', 'reference labor_union', label = T("labor union")),  # reference
        Field('pension_id', 'reference pension', default=0, comment=T('(pension id)'), label = T("pension")),  # reference
        Field('cost_center_id', 'reference cost_center', label = T("cost center")),  # reference
        Field('entry', type='datetime', label = T("entry")),
        Field('exit', type='datetime', label = T("exit")),
        Field('salary', type='double', comment=T('Base salary (monthly)'), label = T("salary")),
        Field('seniority_years', type='integer', label = T("seniority years")),
        Field('spouse', type='boolean', default=False, label = T("spouse")),
        Field('seniority_months', type='integer', label = T("id")),
        Field('large_family', type='boolean', default=False, label = T("large family")),
        Field('department_id', 'reference department', label = T("department")),  # reference
        Field('role_id', 'reference role', label = T("role")),  # reference
        Field('plant_id', 'reference plant', label = T("plant")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "file_file_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('relative',
        Field('relative_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('name', type='string', length=100, label = T("name")),
        Field('staff_id', 'reference staff', label = T("staff")),  # reference
        Field('kinship', type='string', length=1, label = T("kinship")),
        Field('tax_identification', type='string', length=13, label = T("tax identification")),
        Field('allowance', type='boolean', default=False, label = T("allowance")),
        Field('disabled', type='boolean', default=False, label = T("disabled")),
        Field('schooling', type='boolean', default=False, label = T("schooling")),
        Field('nationality_id', 'reference country', label = T("nationality")),  # reference country
        Field('birth', type='datetime', comment=T('Birth date'), label = T("birth")),
        Field('marital_status', type='string', length=1, comment=T('marital status'), label = T("marital status")),
        Field('address', type='string', length=25, label = T("address")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "relative_relative_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_03_scm

    # suppliers/providers:
    db.define_table('supplier',
        Field('supplier_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('legal_name', type='string', length=50, label = T("legal name")),
        Field('tax_id', 'reference tax', default=0, label = T("tax")), # Argentina's IVA # reference
        Field('tax_identification', type='string', length=20, label = T("tax identification")), # Argentina's CUIT
        Field('address', type='string', length=30, label = T("address")),
        Field('zip_code', type='string', length=50, label = T("zip code")),
        Field('city_id', 'reference city', label = T("city")), # reference
        Field('state_id', 'reference state', label = T("state")),  # reference
        Field('telephone', type='string', length=20, label = T("telephone")),
        Field('fax', type='string', length=50, label = T("fax")),
        Field('situation_id', 'reference situation', label = T("situation")),  # reference
        Field('id_number', type='string', length=20, label = T("id number")), # ¿Argentina's DNI?
        Field('observations', type='text', label = T("observations")),
        Field('identity_card', type='string', length=20, label = T("identity card")),
        Field('birth', type='datetime', label = T("birth")),
        Field('nationality_id', 'reference country', label = T("nationality")),  # reference country
        Field('jurisdiction_id', 'reference jurisdiction', label = T("jurisdiction")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "supplier_supplier_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_04_scm

    # product families/lines grouping
    db.define_table('family',
        Field('family_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('collection_id', 'reference collection', label = T("collection")), # reference
        Field('amount', type='decimal(10,2)', default=0, label = T("amount")),
        Field('entry', type='boolean', default=False, label = T("entry")),
        Field('exit', type='boolean', default=False, label = T("exit")),
        Field('category_id', 'reference category', label = T("category")),  # reference
        Field('subcategory_id', 'reference subcategory', label = T("subcategory")),  # reference
        Field('supplier_id', 'reference supplier', label = T("supplier")),  # reference
        Field('suspended', type='boolean', default=False, label = T("suspended")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "family_family_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_05_operations

    db.define_table('concept',
        Field('concept_id', 'id', label = T("id")),
        Field('code', unique = True, default=new_custom_serial_code, label = T("code")),
        Field('description', label = T("description")),
        Field('category_id', 'reference category', label = T("category")), # reference
        Field('subcategory_id', 'reference subcategory', label = T("subcategory")), # reference
        Field('family_id', 'reference family', label = T("family")), # reference
        Field('color_id', 'reference color', label = T("color")),# reference
        Field('size_id', 'reference size', label = T("size")), # reference
        Field('quantity', type='integer', default=0, label = T("quantity")),
        Field('amount', type='double', default=0, label = T("amount")),
        Field('addition', type='date', label = T("addition")),
        Field('deletion', type='date', label = T("deletion")),
        Field('tax_id', 'reference concept', label = T("tax")), # self table reference
        Field('supplier_id', 'reference supplier', label = T("supplier")), # reference
        Field('customer_id', 'integer', label = T("customer")), # reference
        Field('account_id', 'reference account', label = T("account")),# reference
        Field('measure', type='string', length=1, label = T("measure")),
        Field('desired', type='double', default=0, label = T("desired")), # ¿deseado?
        Field('presentation', type='string', length=100, label = T("presentation")),
        Field('entry', type='boolean', default=False, label = T("entry")),
        Field('exit', type='boolean', default=False, label = T("exit")),
        Field('taxed', type='boolean', default=False, label = T("taxed")), #  ¿gravado?
        Field('stock', type='boolean', default=False, label = T("stock")),
        Field('unitary', type='boolean', default=False, label = T("unitary")),
        Field('internal', type='boolean', default=False, label = T("internal")),
        Field('payment_method', type='boolean', default=False, label = T("payment method")),
        Field('tax', type='boolean', default=False, label = T("tax")),
        Field('current_account', type='boolean', default=False, label = T("current account")),
        Field('cash_box', type='boolean', default=False, label = T("cash box")),
        Field('extra', type='boolean', default=False, label = T("extra")),
        Field('cash', type='boolean', default=False, label = T("cash")),
        Field('banks', type='boolean', default=False, label = T("banks")),
        Field('receipt', type='string', length=50, label = T("receipt")),
        Field('statement', type='string', length=50, label = T("statement")), # ¿resumen?
        Field('abbr', type='string', length=50, label = T("abbr")),
        Field('stock_quantity', type='double', label = T("stock quantity")),
        Field('collection_id', 'reference collection', label = T("collection")), # reference
        Field('floor', type='double', label = T("floor")), # ¿mínimo?
        Field('suspended', type='boolean', default=False, label = T("suspended")),
        Field('discounts', type='boolean', default=False, label = T("discounts")),
        Field('surcharges', type='boolean', default=False, label = T("surcharges")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        Field('orderable', 'boolean', default=False, label = T("orderable")), # can be ordered/bought, do not use, filter concepts by internal property
        format='%(description)s',
        sequence_name = "concept_concept_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    db.concept.tax_id.requires = IS_EMPTY_OR(IS_IN_DB(db(db.concept.tax == True), "concept.concept_id", "%(description)s"))

    # db_06_financials

    # funds types (available, imprest/fixed/office fund): "Fondos"
    db.define_table('fund',
        Field('fund_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('type', type='integer', default=0, label = T("type")), # reference?
        Field('upper_limit', type='decimal(10,2)', default=0, label = T("upper limit")),
        Field('balance', type='decimal(10,2)', default=0, label = T("balance")),
        Field('closed', type='boolean', default=False, label = T("closed")),
        Field('current_account', type='boolean', default=False, label = T("current account")),
        Field('bank_checks', type='boolean', default=False, label = T("bank checks")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('account_id', 'reference account', label = T("account")), # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "fund_fund_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # payment terms "CondicionesPago"
    db.define_table('payment_terms',
        Field('payment_terms_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('canceled', type='boolean', default=False, label = T("canceled")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('current_account', type='boolean', default=False, label = T("current account")),
        Field('days_1', 'integer', label = T("days") + " 1"),
        Field('days_2', 'integer', label = T("days") + " 2"),
        Field('days_3', 'integer', label = T("days") + " 3"),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "payment_terms_payment_terms_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # payment methods
    db.define_table('payment_method',
        Field('payment_method_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('coupons', 'integer' , label = T("coupons")),

        Field('coefficient_01', type='double', label = T("coefficient") + " 01"),
        Field('coefficient_02', type='double', label = T("coefficient") + " 02"),
        Field('coefficient_03', type='double', label = T("coefficient") + " 03"),
        Field('coefficient_04', type='double', label = T("coefficient") + " 04"),
        Field('coefficient_05', type='double', label = T("coefficient") + " 05"),
        Field('coefficient_06', type='double', label = T("coefficient") + " 06"),
        Field('coefficient_07', type='double', label = T("coefficient") + " 07"),
        Field('coefficient_08', type='double', label = T("coefficient") + " 08"),
        Field('coefficient_09', type='double', label = T("coefficient") + " 09"),
        Field('coefficient_10', type='double', label = T("coefficient") + " 10"),
        Field('coefficient_11', type='double', label = T("coefficient") + " 11"),
        Field('coefficient_12', type='double', label = T("coefficient") + " 12"),
        Field('coefficient_13', type='double', label = T("coefficient") + " 13"),
        Field('coefficient_14', type='double', label = T("coefficient") + " 14"),
        Field('coefficient_15', type='double', label = T("coefficient") + " 15"),
        Field('coefficient_16', type='double', label = T("coefficient") + " 16"),
        Field('coefficient_17', type='double', label = T("coefficient") + " 17"),
        Field('coefficient_18', type='double', label = T("coefficient") + " 18"),
        Field('coefficient_19', type='double', label = T("coefficient") + " 19"),
        Field('coefficient_20', type='double', label = T("coefficient") + " 20"),
        Field('coefficient_21', type='double', label = T("coefficient") + " 21"),
        Field('coefficient_22', type='double', label = T("coefficient") + " 22"),
        Field('coefficient_23', type='double', label = T("coefficient") + " 23"),
        Field('coefficient_24', type='double', label = T("coefficient") + " 24"),

        Field('quota_01', type='integer', label = T("quota") + " 01"),  # reference?
        Field('quota_02', type='integer', label = T("quota") + " 02"),  # reference?
        Field('quota_03', type='integer', label = T("quota") + " 03"),  # reference?
        Field('quota_04', type='integer', label = T("quota") + " 04"),  # reference?
        Field('quota_05', type='integer', label = T("quota") + " 05"),  # reference?
        Field('quota_06', type='integer', label = T("quota") + " 06"),  # reference?
        Field('quota_07', type='integer', label = T("quota") + " 07"),  # reference?
        Field('quota_08', type='integer', label = T("quota") + " 08"),  # reference?
        Field('quota_09', type='integer', label = T("quota") + " 09"),  # reference?
        Field('quota_10', type='integer', label = T("quota") + " 10"),  # reference?
        Field('quota_11', type='integer', label = T("quota") + " 11"),  # reference?
        Field('quota_12', type='integer', label = T("quota") + " 12"),  # reference?
        Field('quota_13', type='integer', label = T("quota") + " 13"),  # reference?
        Field('quota_14', type='integer', label = T("quota") + " 14"),  # reference?
        Field('quota_15', type='integer', label = T("quota") + " 15"),  # reference?
        Field('quota_16', type='integer', label = T("quota") + " 16"),  # reference?
        Field('quota_17', type='integer', label = T("quota") + " 17"),  # reference?
        Field('quota_18', type='integer', label = T("quota") + " 18"),  # reference?
        Field('quota_19', type='integer', label = T("quota") + " 19"),  # reference?
        Field('quota_20', type='integer', label = T("quota") + " 20"),  # reference?
        Field('quota_21', type='integer', label = T("quota") + " 21"),  # reference?
        Field('quota_22', type='integer', label = T("quota") + " 22"),  # reference?
        Field('quota_23', type='integer', label = T("quota") + " 23"),  # reference?
        Field('quota_24', type='integer', label = T("quota") + " 24"),  # reference?

        Field('days_01', type='integer', label = T("days") + " 01"),
        Field('days_02', type='integer', label = T("days") + " 02"),
        Field('days_03', type='integer', label = T("days") + " 03"),
        Field('days_04', type='integer', label = T("days") + " 04"),
        Field('days_05', type='integer', label = T("days") + " 05"),
        Field('days_06', type='integer', label = T("days") + " 06"),
        Field('days_07', type='integer', label = T("days") + " 07"),
        Field('days_08', type='integer', label = T("days") + " 08"),
        Field('days_09', type='integer', label = T("days") + " 09"),
        Field('days_10', type='integer', label = T("days") + " 10"),
        Field('days_11', type='integer', label = T("days") + " 11"),
        Field('days_12', type='integer', label = T("days") + " 12"),
        Field('days_13', type='integer', label = T("days") + " 13"),
        Field('days_14', type='integer', label = T("days") + " 14"),
        Field('days_15', type='integer', label = T("days") + " 15"),
        Field('days_16', type='integer', label = T("days") + " 16"),
        Field('days_17', type='integer', label = T("days") + " 17"),
        Field('days_18', type='integer', label = T("days") + " 18"),
        Field('days_19', type='integer', label = T("days") + " 19"),
        Field('days_20', type='integer', label = T("days") + " 20"),
        Field('days_21', type='integer', label = T("days") + " 21"),
        Field('days_22', type='integer', label = T("days") + " 22"),
        Field('days_23', type='integer', label = T("days") + " 23"),
        Field('days_24', type='integer', label = T("days") + " 24"),

        Field('expenditure_01', type='decimal(10,2)', label = T("expenditure") + " 01"), # ¿gasto?
        Field('expenditure_02', type='decimal(10,2)', label = T("expenditure") + " 02"), # ¿gasto?
        Field('expenditure_03', type='decimal(10,2)', label = T("expenditure") + " 03"), # ¿gasto?
        Field('expenditure_04', type='decimal(10,2)', label = T("expenditure") + " 04"), # ¿gasto?
        Field('expenditure_05', type='decimal(10,2)', label = T("expenditure") + " 05"), # ¿gasto?
        Field('expenditure_06', type='decimal(10,2)', label = T("expenditure") + " 06"), # ¿gasto?
        Field('expenditure_07', type='decimal(10,2)', label = T("expenditure") + " 07"), # ¿gasto?
        Field('expenditure_08', type='decimal(10,2)', label = T("expenditure") + " 08"), # ¿gasto?
        Field('expenditure_09', type='decimal(10,2)', label = T("expenditure") + " 09"), # ¿gasto?
        Field('expenditure_10', type='decimal(10,2)', label = T("expenditure") + " 10"), # ¿gasto?
        Field('expenditure_11', type='decimal(10,2)', label = T("expenditure") + " 11"), # ¿gasto?
        Field('expenditure_12', type='decimal(10,2)', label = T("expenditure") + " 12"), # ¿gasto?
        Field('expenditure_13', type='decimal(10,2)', label = T("expenditure") + " 13"), # ¿gasto?
        Field('expenditure_14', type='decimal(10,2)', label = T("expenditure") + " 14"), # ¿gasto?
        Field('expenditure_15', type='decimal(10,2)', label = T("expenditure") + " 15"), # ¿gasto?
        Field('expenditure_16', type='decimal(10,2)', label = T("expenditure") + " 16"), # ¿gasto?
        Field('expenditure_17', type='decimal(10,2)', label = T("expenditure") + " 17"), # ¿gasto?
        Field('expenditure_18', type='decimal(10,2)', label = T("expenditure") + " 18"), # ¿gasto?
        Field('expenditure_19', type='decimal(10,2)', label = T("expenditure") + " 19"), # ¿gasto?
        Field('expenditure_20', type='decimal(10,2)', label = T("expenditure") + " 20"), # ¿gasto?
        Field('expenditure_21', type='decimal(10,2)', label = T("expenditure") + " 21"), # ¿gasto?
        Field('expenditure_22', type='decimal(10,2)', label = T("expenditure") + " 22"), # ¿gasto?
        Field('expenditure_23', type='decimal(10,2)', label = T("expenditure") + " 23"), # ¿gasto?
        Field('expenditure_24', type='decimal(10,2)', label = T("expenditure") + " 24"), # ¿gasto?

        Field('replica', type='boolean', default=False),
        format='%(description)s',
        sequence_name = "payment_method_payment_method_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # checkbook
    db.define_table('checkbook',
        Field('checkbook_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('account_id', 'reference account', label = T("account")),  # reference
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('starting', type='datetime', label = T("starting")),
        Field('ending', type='datetime', label = T("ending")),
        Field('next', type='integer', default=0, label = T("next")),  # reference?
        Field('replica', type='boolean', default=False, label = T("replica")),
        sequence_name = "checkbook_checkbook_id_Seq",
        format='%(description)s',
        migrate=migrate, fake_migrate=fake_migrate)

    # db_06_hr

    # new "Noticia"
    db.define_table('payroll_new',
        Field('payroll_new_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('file_id', 'reference file', label = T("file")),  # reference
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('datum', type='double', default=0, label = T("datum")),
        Field('payroll_id', 'reference payroll', label = T("payroll")),  # reference
        Field('addition', type='date', label = T("addition")),
        Field('deletion', type='date', label = T("deletion")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "payroll_new_payroll_new_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('salary',
        Field('salary_id', 'id', label = T("")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('payroll_id', 'reference payroll', label = T("payroll")),
        Field('cost_center_id', 'reference cost_center', label = T("cost center")),  # reference
        Field('staff_category_id', 'reference staff_category', label = T("staff category")),  # reference
        Field('file_id', 'reference file', label = T("file")), # reference
        Field('concept_id', 'reference concept', label = T("concept")), # reference
        Field('liquidation', label = T("liquidation")),  # reference?
        Field('type', type='string', length=1, label = T("type")),  # reference?
        Field('half_bonus', type='boolean', default=False, label = T("half bonus")),
        Field('quantity', type='double', label = T("quantity")),
        Field('amount', type='double', label = T("amount")),
        Field('starting', type='datetime', label = T("starting")),
        Field('ending', type='datetime', label = T("ending")),
        Field('fixed', type='boolean', default=False, label = T("fixed")),
        Field('liquidated', type='boolean', default=False, label = T("liquidated")),
        Field('format', type='string', length=1, label = T("format")),
        Field('text', type='string', length=255, label = T("text")),
        Field('agreement_id', 'reference agreement', label = T("agreement")),  # reference
        Field('department_id', 'reference department', label = T("department")), # reference
        Field('role_id', 'reference role', label = T("role")),
        Field('plant_id', 'reference plant', label = T("plant")), # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "salary_salary_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_06_operations

    db.define_table('document',
        Field('document_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('point_of_sale_id','reference point_of_sale', label = T("point of sale")), # reference
        Field('abbr', type='string', length=3, label = T("abbr")),
        Field('type', type='string', length=1, label = T("type")), # reference?
        Field('tax', type='boolean', default=False, label = T("tax")), # ¿gravar?
        Field('discriminate', type='boolean', default=False, label = T("discriminate")),
        Field('branch', label = T("branch")), # ¿sucursal?
        Field('number', type='integer', default=0, label = T("number")),
        Field('entry', type='boolean', default=False, label = T("entry")),
        Field('exit', type='boolean', default=False, label = T("exit")),
        Field('fiscal', type='boolean', default=False, label = T("fiscal")),
        Field('stock', type='boolean', default=False, label = T("stock")),
        Field('current_account', type='boolean', default=False, label = T("current account")),
        Field('cash', type='boolean', default=False, label = T("cash")), # ¿al contado?
        Field('debit', type='boolean', default=False, label = T("debit")),
        Field('credit', type='boolean', default=False, label = T("credit")),
        Field('invoices', type='boolean', default=False, label = T("invoices")),
        Field('receipts', type='boolean', default=False, label = T("receipts")),
        Field('packing_slips', type='boolean', default=False, label = T("packing slips")), # ¿Remitos?
        Field('orders', type='boolean', default=False, label = T("orders")), # ¿Pedidos?
        Field('budget', type='boolean', default=False, label = T("budget")), # ¿Presupuesto?
        Field('countable', type='boolean', default=False, label = T("countable")),
        Field('printer', type='string', length=50, label = T("printer")), # reference?
        Field('lines', type='integer', default=0, label = T("lines")),
        Field('fund_id', 'reference fund', label = T("fund")), # reference
        Field('replicate', type='boolean', default=False, label = T("replicate")),
        Field('notes', type='text', label = T("notes")),
        Field('observations', type='text', label = T("observations")),
        Field('descriptions', type='text', label = T("descriptions")),
        Field('cash_box', type='boolean', default=False, label = T("cash box")), # ¿caja?
        Field('books', type='boolean', default=False, label = T("books")), # ¿reservas?
        Field('form', 'string', label = T("form")), # reference?
        Field('down_payment', type='boolean', default=False, label = T("down payment")),
        Field('copies', type='integer', label = T("copies")),
        Field('confirm_printing', type='boolean', default=False, label = T("confirm printing")),
        Field('internal', type='boolean', default=False, label = T("internal")),
        Field('invert', type='boolean', default=False, label = T("invert")),
        Field('continuous', type='boolean', default=False, label = T("continuous")),
        Field('multiple_pages', type='boolean', default=False, label = T("multiple pages")),
        Field('preprinted', type='boolean', default=False, label = T("preprinted")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "document_document_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_06_scm

    # product structure (bill of materials)
    db.define_table('product_structure',
        Field('product_structure_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")),
        Field('quantity', type='double', default=0, label = T("quantity")),
        Field('scrap', type='double', default=0, label = T("scrap")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "product_structure_product_structure_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)



    # products inventory (in/out)
    db.define_table('stock',
        Field('stock_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('posted', type='date', comment=T('Date of entry'), label = T("posted")),
        Field('reserved', type='boolean', default=False, label = T("reserved")),
        Field('warehouse_id', 'reference warehouse', label = T("warehouse")),  # reference
        Field('accumulated', type='boolean', default=False, label = T("accumulated")),
        Field('value', type='double', default=0, label = T("value")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "stock_stock_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_07_crm

    # customers/clients: "Deudores"
    db.define_table('customer',
        Field('customer_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('contact', label = T("contact")),
        Field('legal_name', type='string', length=50, comment=T('Customer firm name'), label = T("legal name")),
        Field('address', type='string', length=100, comment=T('Postal address'), label = T("address")),
        Field('zip_code', type='string', length=9, label = T("zip code")),
        Field('city_id', 'reference city', label = T("city")),
        Field('state_id', 'reference state', label = T("state")),
        Field('country_id', 'reference country', label = T("country")),
        Field('fax', type='string', length=20, comment=T('Fax'), label = T("fax")),
        Field('telephone', type='string', length=60, comment=T('Telephone numbers'), label = T("telephone")),
        Field('salesperson_id', 'reference salesperson', label = T("salesperson")), # reference
        Field('price_list_id', 'reference price_list', label = T("price list")), # reference
        Field('tax_identification', type='string', length=20, comment=T('Tax _id'), label = T("tax identificar")), # similar to Argentina's cuit
        Field('tax_id', 'reference tax', label = T("tax")),  # reference
        Field('payment_terms_id', 'reference payment_terms', label = T("payment terms")),  # reference
        Field('invoice', type='string', length=1, comment=T('Invoice header type'), label = T("invoice")),
        Field('current_account', type='string', length=1, comment=T('Type of current account'), label = T("current account")),  # reference?
        Field('situation_id', 'reference situation', comment=T('Finantial situation'), label = T("situation")),  # reference
        Field('customer_group_id', 'reference customer_group', comment=T('Contact Group'), label = T("customer group")),  # reference
        Field('observations', type='text', label = T("observations")),
        Field('place_of_delivery', type='text', label = T("place of delivery")),
        Field('supplier', 'string', label = T("supplier")), # no reference (customer entry)
        Field('addition', type='datetime', comment=T('Customer starting date'), label = T("addition")),
        Field('deletion', type='datetime', comment=T('Customer deletion date'), label = T("deletion")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        Field('current_account_limit', type='double', label = T("current account limit")),
        Field('check_limit', type='double', label = T("check limit")),
        Field('jurisdiction_id', 'reference jurisdiction', label = T("jurisdiction")),  # reference
        Field('debt_limit', type='decimal(10,2)', label = T("debt limit")),
        Field('id_number', label = T("id number")), # Argentina's DNI
        Field('transport', label = T("transport")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(legal_name)s',
        sequence_name = "customer_customer_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # sub-customers ("sub-accounts") "CLIENTES"
    db.define_table('subcustomer',
        Field('subcustomer_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('customer_id', 'reference customer', label = T("customer")),  # reference
        Field('legal_name', type='string', length=50, label = T("legal name")),
        Field('address', type='string', length=100, label = T("address")),
        Field('zip_code', type='string', length=4, label = T("zip code")),
        Field('city_id', 'reference city', label = T("city")),
        Field('state_id', 'reference state', label = T("state")),  # reference
        Field('country_id', 'reference country', label = T("country")), # reference
        Field('fax', type='string', length=20, label = T("fax")),
        Field('telephone', type='string', length=60, label = T("telephone")),
        Field('tax_id', 'reference tax', label = T("tax")),  # reference
        Field('tax_identification', label = T("tax identification")),  # reference
        Field('invoice', type='string', length=1, label = T("invoice")),
        Field('current_account', type='string', length=1, label = T("current account")),  # reference?
        Field('price_list_id', 'reference price_list', label = T("price list")),  # reference
        Field('situation_id', 'reference situation', label = T("situation")),  # reference
        Field('customer_group_id', 'reference customer_group', label = T("customer group")),  # reference
        Field('observations', type='text', label = T("observations")),
        Field('place_of_delivery', type='text', label = T("place of delivery")),
        Field('supplier', 'string', label = T("supplier")),  # no reference (subcustomer entry)
        Field('addition', type='datetime', label = T("addition")),
        Field('deletion', type='datetime', label = T("deletion")),
        Field('current_account_limit', type='double', label = T("current account limit")),
        Field('check_limit', type='double', label = T("check limit")),
        Field('jurisdiction_id', 'reference jurisdiction', label = T("jurisdiction")), # reference
        Field('sex', type="string", length=1, label = T("sex")),
        Field('birth', type='date', label = T("birth")),
        Field('balance', type='double', label = T("balance")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(legal_name)s',
        sequence_name = "subcustomer_subcustomer_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_07_fees

    # Fees, installments, quotes

    db.define_table('fee',
        Field('fee_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('due_date', type='date', label = T("due date")),
        Field('number', type='integer', default=0, label = T("number")),
        Field('month', type='integer', default=0, label = T("month")),
        Field('year', type='integer', default=0, label = T("year")),
        Field('additions', type='boolean', default=False, label = T("additions")),
        Field('document_id', 'reference document', label = T("document")), # reference
        Field('extras', type='boolean', default=False, label = T("extras")),
        Field('ticket', type='boolean', default=False, label = T("ticket")),
        Field('separate', type='boolean', default=False, label = T("separate")),
        Field('starting', type='date', label = T("starting")),
        Field('ending', type='date', label = T("ending")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "fee_fee_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_08_crm

    # contacts
    db.define_table('contact',
        Field('contact_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('customer_id', 'reference customer', label = T("customer")),  # reference
        Field('supplier_id', 'reference supplier', label = T("supplier")),  # reference
        Field('tax_identification', label = T("id")),  # Argentina's CUIT
        Field('department', type='string', length=50, label = T("department")),  # reference?
        Field('telephone', type='string', length=100, label = T("telephone")),
        Field('fax', type='string', length=100, label = T("fax")),
        Field('email', type='string', length=100, label = T("email")),
        Field('schedule', type='string', length=100, label = T("schedule")),
        Field('address', type='string', length=50, label = T("address")),
        Field('zip_code', type='string', length=50, comment=T('Zip code'), label = T("zip code")),
        Field('city_id', 'reference city', label = T("city")),  # reference
        Field('state_id', 'reference state', label = T("state")),  # reference
        Field('observations', type='text', label = T("observations")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "contact_contact_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_08_fees

    db.define_table('installment',
        Field('installment_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('customer_id', 'reference customer', label = T("customer")), # reference
        Field('supplier_id', 'reference supplier', comment=T('Wich supplier to pay to'), label = T("supplier")), # reference
        Field('subcustomer_id', 'reference subcustomer', label = T("subcustomer")), # reference
        Field('fee_id', 'reference fee', label = T("fee")), # reference
        Field('net', type='double', comment=T('Net amount'), label = T("net")),
        Field('discount', type='double', label = T("discount")),
        Field('paid', type='double', label = T("paid")),
        Field('quotas', type='integer', default=0, comment=T('number of quotas'), label = T("quotas")),
        Field('interests', type='double', default=0, comment=T('Transferred interests'), label = T("interests")),
        Field('late_payment', type='double', default=0, comment=T('Late payment fees'), label = T("late payment")),
        Field('monthly_amount', type='double', label = T("monthly amount")),
        Field('paid_quotas', type='integer', default=0, label = T("paid quotas")),
        Field('starting_quota_id', 'integer', comment=T('quota_id'), label = T("starting quota")), # reference
        Field('ending_quota_id', 'integer', default=0, comment=T('quota_id'), label = T("ending quota")), # reference
        Field('starting', type='datetime', label = T("starting")),
        Field('first_due', type='datetime', comment=T('x days of month'), label = T("first due")),
        Field('second_due', type='datetime', comment=T('y days of month'), label = T("second due")),
        Field('observations', type='string', length=50, label = T("observations")),
        Field('canceled', type='boolean', default=False, label = T("canceled")),
        Field('collected', type='double', label = T("collected")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "installment_installment_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    db.define_table('quota',
        Field('quota_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('installment_id', 'reference installment', label = T("installment")),
        Field('number', 'integer', label = T("number")), # TODO: computed field: index number in quotas ordered set +1 (order by id)
        Field('fee_id', 'reference fee', label = T("fee")), # reference
        Field('amount', type='double', label = T("amount")),
        Field('surcharge', type='double', label = T("surcharge")),
        Field('discount', type='double', label = T("discount")),
        Field('paid', type='double', label = T("paid")),
        Field('due_date', type='datetime', label = T("due date")),
        Field('entry', type='integer', default=0, label = T("entry")), # reference?
        Field('exit', type='integer', default=0, label = T("exit")), # reference?
        Field('canceled', type='boolean', default=False, label = T("canceled")),
        Field('collected', type='double', label = T("collected")),
        Field('extra', type='boolean', default=False, label = T("extra")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "quota_quota_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_08_operations

    # Source Document (transactions records)
    db.define_table('operation',
        Field('operation_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('customer_id', 'reference customer', label = T("customer")), # reference
        Field('supplier_id', 'reference supplier', label = T("supplier")), # reference
        Field('detail', type='string', length=60, comment=T('Observations'), label = T("detail")),
        Field('payment_terms_id', 'reference payment_terms', comment=T('Terms of payment'), label = T("payment terms")), # reference
        Field('term', type='string', length=50, label = T("term")),
        Field('amount', type='double', label = T("amount")),
        Field('balance', type='double', label = T("balance")),
        Field('posted', type='datetime', default = now, label = T("posted")),
        Field('issue', type='datetime', label = T("issue")),
        Field('document_id', 'reference document', comment=T('Points to order / invoice / packingslips'), label = T("document")), # reference
        Field('branch', label = T("branch")),
        Field('number', type='integer', default=0, label = T("number")),
        Field('due_date', type='datetime', label = T("due date")),
        Field('type', type='string', length=1, requires=IS_IN_SET({'T': 'Stock','S': 'Sales','P': 'Purchases'}), label = T("type")), # reference? types: T: Stock, S: Sales, P: Purchases
        Field('canceled', type='boolean', default=False, comment=T('False if deferred payment (df), True if paid with cash, ch (check) or current account'), label = T("canceled")),
        Field('processed', type='boolean', default=False, label = T("processed")),
        Field('voided', type='boolean', default=False, label = T("voided")), # ¿anulado?
        Field('fund_id', 'reference fund', label = T("fund")), # reference
        Field('cost_center_id', 'reference cost_center', label = T("cost center")), # reference
        Field('module', type='integer', default=0, comment=T('Referenced table'), label = T("module")), # reference?
        Field('observations', type='string', length=50, label = T("observations")),
        Field('cancellation', type='boolean', default=False, label = T("cancellation")),
        Field('avoidance', type='boolean', default=False, label = T("avoidance")), # ¿anulación?
        Field('file_id', 'reference file', label = T("file")), # ¿legajo? # reference
        Field('payroll_id', 'reference payroll', label = T("payroll")), # reference
        Field('user_id', 'reference auth_user', label = T("user")), # reference
        Field('hour', type='datetime', label = T("hour")),
        Field('replicated', type='datetime', label = T("replicated")),
        Field('subcustomer_id', 'reference subcustomer', label = T("subcustomer")), # reference
        Field('salesperson_id', 'reference salesperson', label = T("salesperson")), # reference
        Field('printed', type='boolean', default=False, label = T("printed")),
        Field('jurisdiction_id', 'reference jurisdiction', label = T("jurisdiction")), # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format=operation_format,
        sequence_name = "operation_operation_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)


    # price "engine":
    db.define_table('price',
        Field('price_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")), # reference
        Field('category_id', 'reference category', label = T("category")), # reference
        Field('salesperson_id', 'reference salesperson', label = T("salesperson")), # reference
        Field('customer_id', 'reference customer', label = T("customer")), # reference
        Field('supplier_id', 'reference supplier', label = T("supplier")), # reference
        Field('customer_group_id', 'reference customer_group', label = T("customer group")), # reference
        Field('situation_id', 'reference situation', label = T("situation")), # reference
        Field('fund_id', 'reference fund', label = T("fund")), # reference
        Field('rate_id', 'reference rate', comment=T('Container type'), label = T("rate")), # ¿tarifaid? # reference
        Field('payment_method_id', 'reference payment_method', comment=T('Method of payment'), label = T("payment method")), # reference
        Field('document_id', 'reference document', comment=T('Document type'), label = T("document")), # reference
        Field('price_list_id', 'reference price_list', label = T("price list")), # reference
        Field('taxed', type='boolean', default=False, label = T("taxed")),
        Field('tax_id', 'reference tax', label = T("tax")), # reference
        Field('type', type='string', length=1, label = T("type")), # reference?
        Field('value', type='double', default=0, comment=T('Insert a value to calculate'), label = T("value")),
        Field('calculate', type='string', length=1, label = T("calculate")),
        Field('operation', label = T("operation")), # reference?
        Field('source', type='string', length=1, comment=T('Field on wich operations will be performed'), label = T("source")),
        Field('condition', type='string', length=2, label = T("condition")),
        Field('quantity_1', type='double', label = T("quantity 1")),
        Field('quantity_2', type='double', label = T("quantity 2")),
        Field('discriminate', type='boolean', default=False, label = T("discriminate")),
        Field('priority', type='integer', label = T("priority")),
        Field('formula', type='text', label = T("formula")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format=price_format,
        sequence_name = "price_price_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)


    # db_09_crm

    # memos messages
    db.define_table('memo',
        Field('memo_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('posted', type='date', label = T("posted")),
        Field('contact_id', 'reference contact', label = T("contact")),  # reference
        Field('subject', type='string', length=50, label = T("subject")),
        Field('observations', type='text', label = T("observations")),
        Field('user_id', 'reference auth_user', label = T("user")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "memo_price_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)


    # many to many referenced user-contact table
    db.define_table('contact_user',
        Field('contact_user_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('user_id', 'reference auth_user', label = T("user")),
        Field('contact_id', 'reference contact', label = T("contact")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "contact_user_contact_user_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_09_financials

    # check
    db.define_table('bank_check',
        Field('bank_check_id', 'id', label = T("id")),
        Field('checkbook_id', 'reference checkbook', \
        requires=IS_EMPTY_OR(IS_IN_DB(db(db.checkbook), \
        "checkbook.checkbook_id", "%(description)s")), label = T("checkbook")), # reference
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('customer_id', 'reference customer', label = T("customer")), # reference
        Field('supplier_id', 'reference supplier', label = T("supplier")), # reference
        Field('number', type='string', length=50, label = T("number")),
        Field('bank_id', 'reference bank', label = T("bank")),  # reference
        Field('amount', type='double', label = T("amount")),
        Field('addition', type='datetime', label = T("addition")),
        Field('due_date', type='datetime', label = T("due date")),
        Field('deletion', type='datetime', label = T("deletion")),
        Field('paid', type='datetime', label = T("paid")),
        Field('exchanged', type='boolean', default=False, label = T("exchanged")),
        Field('bouncer', type='boolean', default=False, label = T("bouncer")),
        Field('operation_id', 'reference operation', label = T("operation")),  # reference
        Field('id_1', type='integer', label = T("id 1")),
        Field('exit', type='integer', label = T("exit")),
        Field('rejection', type='integer', label = T("rejection")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('detail', type='string', length=50, label = T("detail")),
        Field('bd', type='integer', label = T("bd")),
        Field('own', type='boolean', default=False, label = T("own")),
        Field('balance', type='double', label = T("balance")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "bank_check_bank_check_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # cash balance "Cierres"
    db.define_table('cash_balance',
        Field('cash_balance_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('posted', type='date', label = T("posted")),
        Field('balance', type='decimal(10,2)', default=0, label = T("balance")),
        Field('canceled', type='boolean', default=False, label = T("canceled")), # ¿anulado?
        Field('balanced', type='boolean', default=False, label = T("balanced")),
        Field('prints', type='integer', default=0, label = T("prints")),
        Field('operation_1_id', 'reference operation', label = T("operation 1")),  # reference
        Field('operation_2_id', 'reference operation', label = T("operation 2")),  # reference
        Field('pages', type='integer', default=0, label = T("pages")),
        Field('cash', type='integer', default=0, label = T("cash")),
        Field('fund_id', 'reference fund', label = T("fund")),  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "cash_balance_cash_balance_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_09_hr

    # column
    db.define_table('payroll_column',
        Field('payroll_column_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('abbr', type='string', length=50, label = T("abbr")),
        Field('order_number', type='integer', default=0, label = T("order number")), # order
        Field('receipt', type='boolean', default=False, label = T("receipt")),
        Field('remunerative', type='boolean', default=False, label = T("remunerative")),
        Field('operation_id', 'reference operation', label = T("operation")), # ¿operación?  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "payroll_column_payroll_column_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_09_operations

    # ie.: "traditional" line items
    db.define_table('movement',
        Field('movement_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('operation_id', 'reference operation', label = T("operation")), # reference
        Field('concept_id', 'reference concept', label = T("concept")), # reference
        Field('price_id', 'reference price', label = T("price")), # ¿tarifaid? # reference
        Field('quantity', type='double', default=0, label = T("quantity")),
        Field('amount', type='decimal(10,2)', default=0, label = T("amount")),
        Field('discriminated_id', 'reference tax', label = T("discriminated")), # changed (was integer i.e. 21)
        Field('table_number', type='integer', default=0, label = T("table number")), # reference?
        Field('detail', type='string', length=255, label = T("detail")),
        Field('value', type='decimal(10,2)', default=0, label = T("value")),
        Field('posted', type='date', default=today, label = T("posted")),
        Field('discount', type='decimal(10,2)', label = T("discount")),
        Field('surcharge', type='decimal(10,2)', label = T("surcharge")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        Field('bank_check_id', 'integer', label = T("bank check")), # reference
        format='%(description)s',
        sequence_name = "movement_movement_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # db_10_financials

    # bank reconciliation "Conciliación"
    db.define_table('reconciliation',
        Field('reconciliation_id', 'id', label = T("id")),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('posted', type='date', label = T("posted")),
        Field('amount', type='decimal(10,2)', label = T("amount")),
        Field('movement_id', 'reference movement', label = T("movement")), # ¿movimiento?  # reference
        Field('addition', type='date', label = T("addition")),
        Field('deletion', type='date', label = T("deletion")),
        Field('detail', type='text', label = T("detail")),
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "reconciliation_reconciliation_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)

    # credit card coupons
    db.define_table('credit_card_coupon',
        Field('credit_card_coupon_id', 'id'),
        Field('code', unique = True, label = T("code")),
        Field('description', label = T("description")),
        Field('concept_id', 'reference concept', label = T("concept")),  # reference
        Field('number', type='string', length=20, label = T("number")),
        Field('lot', type='string', length=20, label = T("lot")),
        Field('fees', type='integer', label = T("fees")),
        Field('amount', type='double', label = T("amount")),
        Field('addition', type='date', label = T("addition")),
        Field('deletion', type='date', label = T("deletion")),
        Field('due_date', type='date', label = T("due_date")),
        Field('presentation', type='date', label = T("presentation")),
        Field('payment', type='date', label = T("payment")),
        Field('movement_id', 'reference movement', label = T("movement")), # ¿movimiento?  # reference
        Field('replica', type='boolean', default=False, label = T("replica")),
        format='%(description)s',
        sequence_name = "credit_card_coupon_credit_card_coupon_id_Seq",
        migrate=migrate, fake_migrate=fake_migrate)


    # add static table tags
    db.static_table_tags = STATIC_TABLE_TAGS

    if not web2py:
        db.commit()

    # end of define_tables function
    