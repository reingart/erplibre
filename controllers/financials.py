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

import gluon
from gluon import *
import datetime
import config

db = config.db
T = config.env["T"]

session = config.session
request = config.request

# import applications.erplibre.modules.operations as operations
# import applications.erplibre.modules.crm as crm

from modules import crm, operations

import datetime

from gui2py.form import EVT_FORM_SUBMIT


def operations_values(operations):
    # TODO: optimize db queries
    # invert values based on document types
    
    # filter movements by current_account concept and operation id set
    # get the movements rows object
    # populate the array with movement values
    
    values = dict()
    for operation in operations:
        entry = 0.0
        exit = 0.0
        difference = 0.0

        # Change amount sign when operation has invert property
        # TODO: Move invert test to debit/credit properties

        if operation.document_id.invert == True:
            invert_value = -1
        else:
            invert_value = 1
            
        movements = db(db.movement.operation_id == operation.operation_id).select()
        for movement in movements:
            try:
                if movement.concept_id.current_account == True:
                    if movement.amount > 0:
                        entry += float(movement.amount)*invert_value
                    elif movement.amount < 0:
                        exit += float(movement.amount)*(-1)*invert_value
            except (RuntimeError, AttributeError), e:
                print str(e)

            difference = entry -exit
        values[operation.operation_id] = [entry, exit, difference]

    return values


def index(): return dict(message="hello from financials.py")

def current_accounts_type(evt, args=[], vars={}):
    """ Let the user choose the type
    of current account administration """
    
    session.form = SQLFORM.factory(Field("current_accounts_type", \
    requires = IS_IN_SET({"C":"Customer", "S":"Supplier"}), \
    default = "C"))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.current_accounts_type = session.form.vars.current_accounts_type
            
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="financials", f="current_accounts_data"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, current_accounts_type)

    return dict(form = session.form)

    
def current_accounts_data(evt, args=[], vars={}):
    """ Initial parameters for the
    current accounts list """
    
    if session.current_accounts_type == "C":
        n = "customer"
        s = db(db.customer)
        i = "customer.customer_id"
        f = "%(legal_name)s"
    elif session.current_accounts_type == "S":
        n = "supplier"
        s = db(db.supplier)
        i = "supplier.supplier_id"
        f = "%(legal_name)s"
        
    today = datetime.date.today()
    start = datetime.date(1970, 1, 1)
    
    session.form = SQLFORM.factory(Field(n, requires = IS_IN_DB(s, i, f)), \
    Field("starts", "date", default = start), Field("ends", \
    "date", default = today), Field("due", "date", \
    default = today), Field("complete", "boolean"))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            for k in session.form.vars:
                if not k.startswith("_"):
                    if k == "complete":
                        if session.form.vars[k] == "on":
                            session["current_accounts_" + k] = True
                        else:
                            session["current_accounts_" + k] = False
                    else:
                        session["current_accounts_" + k] = session.form.vars[k]
                        
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="financials", f="current_accounts_detail"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, current_accounts_data)
            
    return dict(form = session.form)


def current_accounts_detail(evt, args=[], vars={}):
    """ List of current accounts operations"""
    if session.current_accounts_type == "C":
        supplier_id = db(db.supplier.code == db(db.option.name == "default_supplier_code").select().first().value).select().first().supplier_id
        session.current_accounts_supplier = supplier_id
        customer_id = session.current_accounts_customer
        payment_label = T("Collect")

    elif session.current_accounts_type == "S":
        supplier_id = session.current_accounts_supplier
        customer_id = db(db.customer.code == db(db.option.name == "default_customer_code").select().first().value).select().first().customer_id
        session.current_accounts_customer = customer_id
        payment_label = T("Pay")

    # convert date string iso values
    # (modified, the form sends datetime objects)
    
    starts_list = session.current_accounts_starts.isoformat().split("-")
    ends_list = session.current_accounts_ends.isoformat().split("-")
    due_list = session.current_accounts_due.isoformat().split("-")

    # convert ISO to datetime object for DAL compatibility
    
    starts = datetime.datetime(int(starts_list[0]), int(starts_list[1]), int(starts_list[2]), 0, 0, 0)
    ends = datetime.datetime(int(ends_list[0]), int(ends_list[1]), int(ends_list[2]), 0, 0, 0) + datetime.timedelta(1)
    due = datetime.date(int(due_list[0]), int(due_list[1]), int(due_list[2]))

    # TODO: repair query (returns no records or incomplete)
    # As the time value query is datetime based,
    # exact day matching does not work
    
    q = (db.operation.customer_id == customer_id) & (db.operation.supplier_id == supplier_id) & (db.operation.posted >= starts) & (db.operation.posted <= ends)
    q &= ((db.operation.due_date <= due) | (db.operation.due_date == None))

    # list items with text box (multiple selection)
    # form = SQLFORM.factory(Field("operations", "list:reference operation", requires = IS_IN_DB(operations, "operation.operation_id", "%(document_id)s        %(number)s:        %(amount)s", multiple = True)))

    s = db(q)
    operations = s.select()

    # Values is the array with operations and amounts from the operations query
    # values = dict( int operation_id = [float debit, float credit, float debit -credit], ... )
    
    values = operations_values(operations)

    trows = []
    for operation in operations:
        trows.append(TR(TD(operation.document_id.description), TD(operation.operation_id), TD(operation.posted), TD(operation.due_date), TD(values[operation.operation_id][0]), TD(values[operation.operation_id][1]), TD(values[operation.operation_id][2]), TD(INPUT(_type="checkbox", _name="operation_%s" % operation.operation_id))))
    
    tbody = TBODY(*trows)
    table = TABLE(THEAD(TR(TH(T("Document")), TH(T("Number")), TH(T("Date")), TH(T("Due date")), TH(T("Debit")), TH(T("Credit")), TH(T("Difference")), TH(T("Select")))), tbody)
    
    session.form = FORM(SELECT(OPTION(T("Apply"), _value="apply"), OPTION(payment_label, _value="payment"), _name="selection_action"), table, INPUT(_type="submit"))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # TODO: apply/pay/collect actions

            # Get the selected operations or
            # Set the whole list as target
            # (selected form fields have "on" string as value)
            operation_ids = [int(k.split("_")[1]) for k in session.form.vars if (k.startswith("operation_") and session.form.vars[k] == "on")]

            print T("Operation ids"), operation_ids

            # if there are selected items
            # clean the values array of unselected operations
            new_values = dict()

            if len(operation_ids) > 0:
                for k in values:
                    if k in operation_ids:
                        # add item from values
                        new_values[k] = values[k]
                        
                # add values array to session

                session.current_accounts_values = new_values
            else:
                session.current_accounts_values = values

            if session.form.vars.selection_action == "payment":

                return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="financials", f="current_accounts_payment"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, current_accounts_detail)

    return dict(form = session.form)


def current_accounts_payment(evt, args=[], vars={}):
    if session.current_accounts_type == "S":
        point_of_sale_id = db(db.point_of_sale.code == db(db.option.name == "purchases_payment_point_of_sale_code").select().first().value).select().first().point_of_sale_id
        operation_type = "P"
        invert_value = -1

    elif session.current_accounts_type == "C":
        point_of_sale_id = db(db.point_of_sale.code == db(db.option.name == "sales_payment_point_of_sale_code").select().first().value).select().first().point_of_sale_id
        operation_type = "S"
        invert_value = 1

    # get the default payment terms for current accounts
    payment_terms_id = db(db.payment_terms.code == db(db.option.name == "current_account_payment").select().first().value).select().first().payment_terms_id

    # document widget settings
    s = db(db.document.point_of_sale_id == point_of_sale_id)
    i = "document.document_id"
    f = "%(description)s"

    # calculate difference from values array
    values = session.current_accounts_values
    
    difference = sum([values[v][2] for v in values], 0.0) * invert_value
    print T("Calculated difference") + ": %s" % difference

    # pre-operation form
    session.form = SQLFORM.factory(Field("document", "reference document", requires = IS_IN_DB(s, i, f)), Field("amount", "double", default = difference), Field("concept", "reference concept", requires = IS_IN_DB(db(db.concept.current_account == True), "concept.concept_id", "%(description)s")), Field("payment_terms", "reference payment_terms", requires = IS_IN_DB(db(db.payment_terms.payment_terms_id != None), "payment_terms.payment_terms_id", "%(description)s")))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # create the operation with stored user options
            # insert the current accounts movement
            # and redirect to the operation detail form

            # todo: auto operation values (fund, subcustomer, other)

            # receipt payment terms
            if len(session.form.vars.payment_terms) > 0:
                payment_terms_id = session.form.vars.payment_terms

            # get the concept db record
            concept = db.concept[session.form.vars.concept]

            # current account movement amount
            amount = float(session.form.vars.amount)

            # new receipt/current accounts operation
            operation_id = db.operation.insert(customer_id = session.current_accounts_customer, supplier_id = session.current_accounts_supplier, document_id = session.form.vars.document, type = operation_type, payment_terms_id = payment_terms_id)

            session.operation_id = operation_id

            # current accounts movement
            db.movement.insert(operation_id = operation_id, amount = amount, value = amount, quantity = 1, concept_id = concept.concept_id)
            
            session.operation_id = operation_id
            
            db.commit()

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, current_accounts_payment)

    return dict(form = session.form)
