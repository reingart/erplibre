# -*- coding: utf-8 -*-
# intente algo como

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

session = config.session
request = config.request

# modules = __import__('applications.%s.modules' % config.WEB2PY_APP_NAME, globals(), locals(), ['operations', 'crm'], -1)
# crm = modules.crm
# operations = modules.operations

from modules import crm, operations

# Import web2py app modules
# import applications.erplibre.modules.operations as operations
# import applications.erplibre.modules.crm as crm

from gui2py.form import EVT_FORM_SUBMIT

T = config.env["T"]

####################################################################
##   Auxiliar functions
####################################################################

def update_operation(operation_id, vars):
    db.operation[operation_id].update_record(**vars)
    db.commit()
    print T("The operation %(operation)s was updated") % dict(operation=operation_id)


# list of orderable concepts
# returns a dict with value, name pairs for
# IS_IN_SET validator
def orderable_concepts(limit_by = None):
    the_dict = dict()
    rows = db(db.concept.internal == False).select()
    for n, row in enumerate(rows):
        if (n < limit_by) or (limit_by is None):
            the_dict[row.concept_id] = row.description
        else:
            break
    return the_dict


def movements_taxes(operation_id):
    """ Performs tax operations for the given operation """

    # TODO: clean zero amount tax items,
    # Separate the movements values
    # processing in a function

    # WARNING: db.table[0] returns None

    operation = db.operation[operation_id]
    document = db.document[operation.document_id]
    # number of tax items
    items = 0
    taxes = dict()
    data = list()
    for movement in db(db.movement.operation_id == operation_id \
    ).select():
        # Compute the tax values if required
        concept = db(db.concept.concept_id == movement.concept_id \
        ).select().first()

        # Calculate movement amount without taxes
        try:
            amount = float(movement.value) * float(movement.quantity)
        except (TypeError, ValueError, AttributeError):
            amount = None

        if (concept is not None) and (concept.taxed):
            if not concept.tax_id is None:
                tax = db.concept[concept.tax_id]
                config.verbose(("Movement concept", concept.description, "Tax concept:", tax.description))
            else:
                tax = None
                print "Error: concept is taxed but no tax concept found"
                
            # None taxes can occur if a
            # concept is taxed but has no
            # tax concept as reference
            if (tax is not None) and (amount is not None):
                tax_amount = (float(amount) * float(tax.amount)) \
                - float(amount)
                print tax.description, ":", tax_amount
                try:
                    taxes[tax.concept_id] += tax_amount
                except KeyError:
                    taxes[tax.concept_id] = tax_amount

                if not document.discriminate:
                    # add to item amount if not discriminated
                    movement.update_record(amount = float( \
                    amount) + tax_amount)

    for tax_concept_id in taxes:
        tax = db.concept[tax_concept_id]
        # Get and increase or create tax item
        if document.discriminate:
            tax_record = db(( \
            db.movement.concept_id == tax_concept_id) & ( \
            db.movement.operation_id == operation_id \
            )).select().first()

            if tax_record is None:
                tax_record_id = db.movement.insert( \
                operation_id = operation_id, \
                value = taxes[tax_concept_id], \
                amount = taxes[tax_concept_id], \
                concept_id = tax_concept_id, quantity = 1)
                tax_record = db.movement[tax_record_id]
            else:
                tax_record.update_record(amount = taxes[tax_concept_id], \
                value = taxes[tax_concept_id])
    items = len(taxes)
    return items


def movements_checks(operation_id):
    """ Movements check processing """
    # TODO: erease checks movement if amount is 0
    # TODO: return warnings/errors
    # TODO: assign one-to-one relation to checks and movements
    
    concept_id = None
    checks = db(db.bank_check.operation_id == operation_id).select()
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    if operation.type == "S":
        
        concept_id = db(db.concept.code == db( \
        db.option.name == "sales_check_input_concept" \
        ).select().first().value).select().first().concept_id
        
    elif operation.type == "P":

        concept_id = db(db.concept.code == db( \
        db.option.name == "purchases_check_input_concept" \
        ).select().first().value).select().first().concept_id
        
    else:
        # Do not input checks if it is a stock operation
        return 0

    # get or create the movement
    if concept_id is not None:
        q = db.movement.operation_id == operation_id
        q &= db.movement.concept_id == concept_id
        s = db(q)

        if len(checks) > 0:
            checks_movement = s.select().first()
            if (checks_movement is None):
                checks_movement_id = db.movement.insert( \
                operation_id = operation_id, \
                concept_id = concept_id)

                # Get the new checks movement db record
                checks_movement = \
                db.movement[checks_movement_id]

            # Calculate the total amount and update the
            # checks movement
            checks_movement.update_record( \
            amount = sum([check.amount for check in checks]))

    else:
        # no concept configured for checks
        return 0


    return len(checks)


def movements_difference(operation_id):
    # None for unresolved amounts
    difference = None
    invert_value = 1
    operation = db.operation[operation_id]

    document = operation.document_id

    try:
        if document.invert: invert_value = -1
    except AttributeError:
        # no document specified
        return None

    # draft movements algorithm:
    # difference = exit concepts - entry c.
    q_entry = db.movement.concept_id == db.concept.concept_id
    q_entry &= db.concept.entry == True
    q_entry &= db.movement.operation_id == session.operation_id

    q_exit = db.movement.concept_id == db.concept.concept_id
    q_exit &= db.concept.exit == True
    q_exit &= db.movement.operation_id == session.operation_id

    print T("Calculate movements difference....")

    rows_entry = db(q_entry).select()
    print T("Entries: %(amounts)s") % dict(amounts=str([row.movement.amount for row in rows_entry]))

    rows_exit = db(q_exit).select()
    print T("Exits: %(amounts)s") % dict(amounts=str([row.movement.amount for row in rows_exit]))

    # Value inversion gives unexpected difference amounts in documents
    # TODO: complete difference evaluation including Entry/Exit parameters

    difference = float(sum([row.movement.amount for row in \
    rows_exit if row.movement.amount is not None], 0) \
    - sum([row.movement.amount for row \
    in rows_entry if row.movement.amount is not None], 0))
    # * invert_value

    print T("Difference: %(difference)s") % dict(difference=difference)

    return difference


def movements_update(operation_id):
    """ Operation maintenance (amounts, checks, taxes, difference) """
    # Get options
    update_taxes = session.get("update_taxes", False)

    update = False

    if update_taxes == True:
        taxes = movements_taxes(operation_id)

    checks = movements_checks(operation_id)
    session.difference = movements_difference(operation_id)
    db.operation[operation_id].update_record( \
    amount = movements_amount(operation_id))
    update = True

    db.commit()
    
    return update


def movements_amount(operation_id):
    """ Calculate the total amount of the operation"""

    amount = None

    if db.operation[operation_id].document_id == None:
        # no document specified (operation header is incomplete)
        print T("Operation header incomplete. Please select a document type")
        return None

    if db.operation[operation_id].document_id.receipts != True:
        
        q_items = db.movement.concept_id == db.concept.concept_id
        q_items &= db.concept.internal != True
        q_items &= db.concept.discounts != True
        q_items &= db.concept.surcharges != True
        q_items &= db.concept.current_account != True
        q_items &= db.concept.banks != True
        
        q_items &= db.movement.operation_id == operation_id

        q_discounts = db.movement.concept_id == db.concept.concept_id
        q_discounts &= db.concept.discounts == True
        q_discounts &= db.movement.operation_id == operation_id

        q_surcharges = db.movement.concept_id == db.concept.concept_id
        q_surcharges &= db.concept.surcharges == True
        q_surcharges &= db.movement.operation_id == operation_id

        rows_items = db(q_items).select()
        rows_surcharges = db(q_surcharges).select()
        rows_discounts = db(q_discounts).select()

        items = float(abs(sum([item.movement.amount for item \
        in rows_items if item.movement.amount is not None])))


        surcharges = float(abs(sum([item.movement.amount \
        for item in rows_surcharges if item.movement.amount is not None])))

        discounts = float(abs(sum([item.movement.amount \
        for item in rows_discounts if item.movement.amount is not None])))

        amount = float(items + surcharges -discounts)

    else:
        q_payments = db.movement.operation_id == operation_id
        q_payments &= db.movement.concept_id == db.concept.concept_id
        q_payments &= db.concept.payment_method == True
        rows_payments = db(q_payments).select()

        amount = float(abs(sum([payment.movement.amount \
        for payment in rows_payments if payment.movement.amount is not None])))

    return amount


def movements_stock(operation_id):
    """ Process stock values.

    TODO: detect stock errors, rollback
    transactions and return False """
    
    update_stock_list = session.get("update_stock_list", set())
    result = False
    movements = db(db.movement.operation_id == operation_id).select()
    document = db.operation[operation_id].document_id
    warehouse_id = session.get("warehouse_id", None)
    items = 0
    for movement in movements:
        concept = db(db.concept.concept_id == movement.concept_id \
        ).select().first()
        if (concept is not None) and (warehouse_id is \
        not None) and (concept.stock == True) and (movement.movement_id in update_stock_list):
            stock = db(( \
            db.stock.warehouse_id == warehouse_id) \
            & (db.stock.concept_id == concept.concept_id) \
            ).select().first()
            if stock is not None:
                value = stock.value
                if (document is not None) and ( \
                document.invert == True):
                    value += movement.quantity
                else:
                    value -= movement.quantity

                # update stock value
                print T("Updating stock id: %(id)s as %(value)s") % dict(id = stock.stock_id, value = value)
                stock.update_record(value = value)

                items += 1
    result = True
    return result



def is_editable(operation_id):
    """ Check if operation can be modified"""
    operation = db.operation[operation_id]
    if operation.voided or operation.canceled or operation.processed:
        return False
    return True

####################################################################
#   Controller actions
####################################################################


def index(evt, args=[], vars={}):
    """ Staff on-line panel. Show info/stats/links to actions"""

    now = datetime.datetime.now()
    delta = datetime.timedelta(7)
    time_limit = now - delta

    q = db.operation.operation_id > 0
    preset = db(q)
    the_set = preset(db.operation.posted >= time_limit)

    """
    TODO: filter by order document type

    # list all document types with orders == True
    order_documents = db(db.document.orders == True).select()
    order_documents_list = [document.document_id for document in order_documents]
    # make a subset of operations with order documents
    customer_orders_subset = customer_orders_set & db()
    """
    # get operation rows
    operations = the_set.select()

    return dict(operations = operations, message=T("Administrative panel"))

# base web interface for movements
# administration

def ria_movements_process(evt, args=[], vars={}):
    # TODO: incomplete
    # do not expose if operation was already processed
    # process/validate the operation
    if operations.process(db, session, session.operation_id):
        db.commit()
        print T("Operation processed")
        
    else:
        print T("Could not process the operation")
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="ria_movements"))
    
    
def ria_movements_reset(evt, args=[], vars={}):
    session.operation_id = None
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="ria_movements"))

def ria_movements(evt, args=[], vars={}):
    # reset the current operation (sent client-side)
    reset_operation_form = A(T("Reset operation"), _href=URL(a=config.APP_NAME, c="operations", f="ria_movements_reset"))
    # get the current operation if stored in session
    operation_id = session.get("operation_id", None)

    # Get the operation id requested
    # (assuming that an operation was specified)
    if len(args) > 0:
        session.operation_id = operation_id = int(args[1])
    
    # Otherwise, if the user started a new operation, or none was
    # specified, create one
    elif ("new" in request.vars) or (operation_id is None):
        session.operation_id = operation_id = db.operation.insert(\
        user_id = config.auth.user_id)

    # standard operation update sqlform
    # TODO: operation change shouldn't be allowed if processed
    
    session.form = SQLFORM(db.operation, operation_id, _id="operation_form")
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.operation[session.operation_id].update_record(**session.form.vars)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_movements"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, ria_movements)

    # Process operation for accounting/other when accepted
    process_operation_form = A(T("Process operation"), _href=URL(a=config.APP_NAME, c="operations", f="ria_movements_process"))

    

    movements_rows = db( \
        db.movement.operation_id == session.operation_id).select()
    movements_list = SQLTABLE(movements_rows, \
                              columns=["movement.movement_id", \
                                       "movement.description", \
                                       "movement.concept_id", \
                                       "movement.quantity", \
                                       "movement.posted"], \
                              headers={"movement.movement_id": "Edit", \
                                       "movement.description": "Description", \
                                       "movement.concept_id": "Product", \
                                       "movement.quantity": "Qty", \
                                       "movement.posted": "Posted"}, \
                              linkto=URL(a=config.APP_NAME, c="operations", \
                                         f="movements_modify_element"))
    
    add_item = A(T("Add item"), _href=URL(a=config.APP_NAME, c="operations", f="movements_element"))

    return dict(message=T("Operation number %(id)s") % dict(id = operation_id), \
    form = session.form, \
    reset_operation_form = reset_operation_form, \
    process_operation_form = process_operation_form, movements_list \
    = movements_list, add_item = add_item)

def movements_element(evt, args=[], vars={}):
    """ Insert sub-form for concept selection at movements form"""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Operation not found.")
    
    session.form = SQLFORM(db.movement, fields=["code","description",
"concept_id", "price_id", "quantity", "amount", "discriminated_id", \
"table_number", "detail", "value", "posted", "discount", "surcharge", \
"replica"])
    session.form.vars.operation_id = session.operation_id

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.movement.insert(**session.form.vars)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_movements"))
        elif form.errors:
            print T("The form has errors")
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_element)
    # query for operation movements
    return dict(form=session.form)

def movements_modify_element(evt, args=[], vars={}):
    """ Movements element edition sub-form."""
    if len(args) > 1:
        session.movements_element_id = args[1]

    session.form = SQLFORM(db.movement, session.movements_element_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.movement[session.movements_element_id].update_record(**session.form.vars)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_movements"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_modify_element)
    return dict(form=session.form)

# create intallment/quotas for current operation
def operation_installment(evt, args=[], vars={}):
    total = 0
    
    # get session operation
    operation = db.operation[session.operation_id]

    # calculate operation total payment
    movements = db(db.movement.operation_id == operation.operation_id).select()
    for mov in movements:
        try:
            total += float(mov.value) * float(mov.quantity)
        except (ValueError, TypeError):
            # TODO: add error warning/handling
            pass

    # installment creation form
    session.form = SQLFORM.factory(Field('quotas', 'integer'), \
    Field('fee_id', 'integer', requires=IS_IN_DB(db, db.fee)))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # create installment and fixed quotas
            # TODO: custom quota fields
            session.installment_id = db.installment.insert(\
            customer_id = operation.customer_id, subcustomer_id = operation.subcustomer_id, \
            supplier_id = operation.supplier_id, fee_id = session.form.vars.fee_id)

            # quota amount = total / quotas
            quota_amount = total / float(session.form.vars.quotas)
            quotas_list = list()

            print T("Quota amount"), quota_amount
            
            for x in range(int(session.form.vars.quotas)):
                quotas_list.append(db.quota.insert(installment_id = session.installment_id, \
                fee_id = session.form.vars.fee_id, number = x+1, amount = quota_amount))

            print T("Quotas list"), quotas_list

            db.installment[session.installment_id].update_record(quotas = len(quotas_list), \
            monthly_amount = quota_amount, starting_quota_id = quotas_list[0], \
            ending_quota_id = quotas_list[len(quotas_list) -1])

            db.commit()
            print T("Installment created")
            
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="operation_installment"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, operation_installment)

    installment = db.installment[session.installment_id]

    return dict(total = total, form = session.form, installment = installment)


def ria_new_customer_order_reset(evt, args=[], vars={}):
    session.operation_id = None
    return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_new_customer_order"))


def ria_new_customer_order(evt, args=[], vars={}):

    customer = None
    
    if session.get("operation_id", None) is not None:
        the_operation = db.operation[session.operation_id]
        the_document = db.document[the_operation.document_id]
        try:
            if the_document.orders != True:
                # reset document (it is not an order)
                session.operation_id = None
            else:
                customer = db.customer[the_operation.customer_id]
                
        except (AttributeError, KeyError):
            # reset document (misconfigured operation)
            session.operation_id = None

    """ Customer's ordering on-line form.
    Note: get db objects with db(query).select()
    i.e. contact.customer returns the db record id """

    # TODO: modify for local gui client configuration

    contact_user = db(db.contact_user.user_id == config.auth.user_id).select().first()
    
    reset = A(T("Reset this order"), _href=URL(a=config.APP_NAME, c="operations", f="ria_new_customer_order_reset"))

    if len(args) > 0:
        session.operation_id = int(args[1])

    # catch incomplete registrations (no contact user relations)
    if contact_user is None:
        return dict(form=None, reset = None, \
        contact = None, customer = None, order = None, \
        contact_user=None)
    try:
        contact = db(db.contact.contact_id == contact_user.contact_id \
        ).select().first()
    except KeyError:
        contact = None

    # Look for allowed orders in options db
    customer_allowed_orders = db(db.option.name == \
    "customer_allowed_orders").select().first()
    
    if customer_allowed_orders and  isinstance( \
    customer_allowed_orders.value, basestring):
        allowed_orders_list = [str(o).strip() for o in \
        customer_allowed_orders.value.split("|") if len(o) > 0]
    else:
        allowed_orders_list = []

    # Get the default order
    try:
        default_order = db(db.document.code == db(db.option.name == \
        "customer_default_order").select().first().value).select().first().document_id
    except (AttributeError, KeyError), e:
        default_order = None

    if isinstance(default_order, basestring):
        try:
            default_order = int(default_order)
        except ValueError:
            default_order = None

    # TODO: auto-select supplier by document type (Purchases/Sales)

    # create a new order with pre-populated user data
    if not "operation_id" in session.keys():
        customer_order = db.operation.insert( \
        customer_id = customer, document_id = default_order)
        session.operation_id = customer_order
        db.commit()
        
    else:
        customer_order = session.operation_id
        if session.operation_id is None:
            customer_order = db.operation.insert( \
            document_id = default_order)
            session.operation_id = customer_order
            db.commit()

    session.form = SQLFORM(db.operation, customer_order, \
    fields=["description", "customer_id", "subcustomer_id", "supplier_id", "document_id"], _id="new_customer_order_form")

    # Available order documents
    order_documents = db(db.document.orders == True).select()
    checks = 0
    loop_count = 0
    check_list = list()
    order_options = dict()

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.operation[customer_order].update_record( \
            description = session.form.vars.description, \
            customer_id = session.form.vars.customer_id, \
            subcustomer_id = session.form.vars.subcustomer_id, \
            supplier_id = session.form.vars.supplier_id, \
            document_id = session.form.vars.document_id)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_new_customer_order"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, ria_new_customer_order)


    for order_document in order_documents:
        loop_count += 1
        # check option if previously selected
        if db.operation[customer_order].document_id \
        == order_document.document_id:
            checked = True
        elif order_document.document_id == default_order:
            checked = True
        else:
            checked = False
        if order_document.code in allowed_orders_list:
            order_options[order_document.document_id] = dict()
            order_options[order_document.document_id]["label"] = order_document.description
            order_options[order_document.document_id]["name"] = "order_type"
            order_options[order_document.document_id]["value"] = order_document.document_id
            if checked:
                order_options[order_document.document_id]["checked"] = True
                checked = False
            else:
                order_options[order_document.document_id]["checked"] = False

    order_list = db(db.movement.operation_id == session.operation_id  \
    ).select()

    return dict(form=session.form, reset=reset, contact = contact, \
    customer = customer, order = db.operation[customer_order], \
    contact_user = contact_user, order_options = order_options, order_list = order_list)

# order movement creation
def new_customer_order_element(evt, args=[], vars={}):
    """ Insert sub-form for product selection at Customer ordering form"""
    
    if not "operation_id" in session.keys():
        raise HTTP(500, "Customer order not found.")

    session.form = SQLFORM.factory(Field('concept_id', 'reference concept', \
    requires=IS_IN_SET(orderable_concepts())), \
    Field('description'), Field('quantity', 'double'), \
    _id="new_customer_order_element_form")

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.movement.insert(operation_id = session.operation_id, \
            concept_id = session.form.vars.concept_id, \
            description = session.form.vars.description, \
            quantity = session.form.vars.quantity)

            db.commit()

            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_new_customer_order"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, new_customer_order_element)

    return dict(form=session.form)


# order movement modification
def new_customer_order_modify_element(evt, args=[], vars={}):
    """ Customer order element edition sub-form."""
    if not "operation_id" in session.keys():
        raise HTTP(500, T("Customer order not found."))

    if len(args) > 1:
        session.customer_order_element_id = args[1]
        
    customer_order_element = db.movement[session.customer_order_element_id]

    session.form = SQLFORM(db.movement, customer_order_element.movement_id, \
    deletable = True, fields = ["description", "concept_id", "quantity"], \
    _id="new_customer_order_modify_element_form")

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.delete_this_record is not None:
                # erase the db record if marked for deletion
                print T("Erasing movement %(id)s") % dict(id=customer_order_element.movement_id)
                db.movement[customer_order_element.movement_id].delete_record()
            else:
                customer_order_element.update_record(**session.form.vars)

            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_new_customer_order"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, new_customer_order_modify_element)

    return dict(form=session.form)


def order_allocation(evt, args=[], vars={}):
    # Note: this is a draft for
    # Inventory/Order allocation
    # management and is not intended
    # as a complete and refined solution
    # for the matter. TODO: order allocation
    # algorithms implementation

    # the current algorithm
    # has not been tested
    # and may lead to stock inconsistencies

    # get movements from order operations
    # wich have unallocated items (unprocessed)

    q = db.movement.operation_id == db.operation.operation_id
    q &= db.operation.processed != True
    q &= db.operation.document_id == db.document.document_id
    q &= db.document.orders == True
    preset = db(q)
    order_movements = preset.select()

    # separate movements by customer and concept
    session.movements_stack = dict()
    session.pending_stack = dict()
    session.operations_stack = set()
    session.allocations_completed = session.get("allocations_completed", set())

    for om in order_movements:
        try:
            qty = float(om.movement.quantity)
        except (ValueError, KeyError):
            qty = 0
        try:
            concept = int(om.movement.concept_id)
            customer = int(om.operation.customer_id)
            operation = int(om.operation.operation_id)
            session.operations_stack.add(operation)
        except (KeyError, ValueError, AttributeError, TypeError):
            concept = customer = operation = None

        if customer in session.movements_stack:
            if concept in session.movements_stack[customer]:
                session.movements_stack[customer][\
                concept]["qty"] += qty
            else:
                session.movements_stack[customer][\
                concept] = dict(first = operation, \
                qty = qty, allocated = 0, pending = True, \
                stock = 0, allocate = 0.0)
        else:
            session.movements_stack[customer] = dict()
            session.movements_stack[customer][concept] = dict(\
            first = operation, qty = qty, \
            allocated = 0, pending = True, stock = 0, allocate = 0.0)

    # compare order quantity and allocated qty
    # per order item (order allocation after order date)
    for customer in session.movements_stack:
        for concept in session.movements_stack[customer]:
            # get the item stock
            # TODO: manage user selected warehouses

            try:
                stock = db(\
                db.stock.concept_id == concept).select().first().value
                oldest = db.operation[session.movements_stack[\
                customer][concept]["first"]\
                ].posted
            except AttributeError:
                stock = oldest = None

            if stock is not None:
                # update the stock value for the current customer/concept
                session.movements_stack[customer][concept]["stock"] = stock

                q = (db.movement.concept_id == concept)
                q &= db.movement.operation_id == db.operation.operation_id
                q &= db.operation.document_id == db.document.document_id
                q &= db.document.books == True

                if oldest is not None:
                    q &= (db.movement.posted >= oldest)

                allocated_set = db(q)

                # set allocated amount
                try:
                    session.movements_stack[customer][concept][\
                    "allocated"] = sum(\
                    [m.movement.quantity for m in allocated_set.select() \
                    if m.movement.quantity is not None], 0.00)
                except KeyError:
                    session.movements_stack[customer][concept][\
                    "allocated"] = 0.00
                # if allocated is equal to ordered for any order movement
                # set item as completed
                if session.movements_stack[customer][concept]["qty"] <= \
                session.movements_stack[customer][concept]["allocated"]:
                    session.movements_stack[customer][concept]["pending"] = False

    # present a form-row to allocate from inventory
    # based on available stock value.
    form_rows = []
    for customer, v in session.movements_stack.iteritems():
        for concept, w in v.iteritems():
            try:
                # getting the customer with dictionary syntax
                # throws a KeyError exception
                customer_desc = db(db.customer.customer_id == customer \
                ).select().first().description
            except (AttributeError, KeyError):
                customer_desc = customer
            try:
                concept_code = db.concept[str(concept)].code
                concept_desc = db.concept[str(concept)].description
            except (AttributeError, KeyError):
                concept_code = concept_desc = concept

            form_rows.append(TR(TD(customer_desc), TD(concept_code), \
            TD(concept_desc), TD(w["qty"]), TD(w["allocated"]), \
            TD(w["stock"]), \
            INPUT(_name="order_allocation_%s_%s" % (customer, concept))))

    session.form = FORM(TABLE(THEAD(TR(TH(T("Customer")),TH(T("Product code")), \
    TH(T("Concept")), TH(T("Ordered")), TH(T("Allocated")), TH(T("Stock")), \
    TH(T("Allocate")))), TBODY(*form_rows), TFOOT(TR(TD(), TD(), TD(), \
    TD(), TD(), TD(), TD(INPUT(_value="Allocate orders", _type="submit"))))))

    # form processing:
    # classify allocated items by customer
    # for each customer allocation item group

    session.operations_stack = set()

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            for var in session.form.vars:
                if "order_allocation" in var:
                    try:
                        concept = int(var.split("_")[3])
                        customer = int(var.split("_")[2])
                        session.movements_stack[customer][concept]["allocate"] = float( \
                        session.form.vars[var])
                    except (ValueError, TypeError, KeyError):
                        customer = None
                        concept = None

            # create and populate the order allocation document
            order_allocations = 0
            for customer, v in session.movements_stack.iteritems():
                operation = None
                for concept, w in v.iteritems():
                    if w["allocate"] > 0:
                        if operation is None:
                            # new operation
                            # TODO: order allocation document defined by user input/configuration
                            operation = db.operation.insert(customer_id = customer, \
                            document_id = db(db.document.books == True).select().first().document_id)
                            order_allocations += 1

                        db.movement.insert(operation_id = operation, \
                        quantity = w["allocate"], concept_id = concept)
                        # reduce stock value
                        stock_item = db(db.stock.concept_id == concept).select().first()
                        stock_value = stock_item.value -w["allocate"]
                        stock_item.update_record(value = stock_value)
                        session.operations_stack.add(operation)
            db.commit()
            
            session.allocations_completed = session.operations_stack
            
            print T("Order allocations completed: %(oa)s") % dict(oa=order_allocations)
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="order_allocation"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, order_allocation)

    # return a list with allocations by item
    return dict(form = session.form, allocations_completed = session.allocations_completed)

def list_order_allocations(evt, args=[], vars={}):
    q = db.operation.processed == False
    q &= db.operation.document_id == db.document.document_id
    q &= db.document.books == True
    columns = ["operation.operation_id", "operation.code", \
    "operation.description", "operation.posted"]
    headers={"operation.operation_id": T("Edit"), "operation.code":T("Code"), \
    "operation.description": T("Description"), "operation.posted": T("Posted")}
    order_allocations = SQLTABLE(db(q).select(), columns = columns, \
    headers = headers, \
    linkto=URL(a=config.APP_NAME, c="operations", f="update_order_allocation"))
    
    return dict(order_allocations = order_allocations)

def update_order_allocation(evt, args=[], vars={}):
    if len(args) > 1:
        session.operation_id = session.order_allocation_id = args[1]

    session.form = SQLFORM(db.operation, session.order_allocation_id, \
    fields=["code", "description", "supplier_id", "customer_id", \
    "subcustomer_id", "detail", "document_id", "branch", "voided"], \
    )
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.operation[session.order_allocation_id].update_record(**session.form.vars)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="list_order_allocations"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_order_allocation)

    movements = SQLTABLE(db(\
    db.movement.operation_id == session.order_allocation_id).select(), \
    columns=["movement.movement_id", "movement.code","movement.concept_id", \
    "movement.quantity"], headers={"movement.movement_id": \
    T("ID"), "movement.code": T("Code"), \
    "movement.concept_id": T("Concept"), "movement.quantity": T("Quantity")}, \
    linkto=URL(a=config.APP_NAME, c="operations", f="movements_modify_element"))
    
    return dict(form = session.form, movements = movements)

def reset_packing_slip(evt, args=[], vars={}):
    session.packing_slip_id = None
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="packing_slip"))

def packing_slip(evt, args=[], vars={}):
    """Create a packing slip from order allocation
    operation.
    """

    # packing slip fields
    form_fields = ["code", "description", "customer_id", \
    "subcustomer_id", "supplier_id", "document_id", "branch", "voided"]

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # web2py stores the created record id as "id"
            # instead of using the table field definition
            if session.packing_slip_id is not None:
                db.operation[session.packing_slip_id].update_record(**session.form.vars)
                
            else:
                # session.packing_slip_id = db.operation.insert(**session.form.vars)
                raise HTTP(200, "No packing slip found to update")

            db.commit()
            print T("Form accepted")

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, \
            c="operations", f="packing_slip"))

    else:
        session.document_id = db(db.document.packing_slips == True).select(\
        ).first().document_id

        if len(args) > 1:
            # packing slip from order allocation document
            session.packing_slips_id = None
            session.order_allocation_id = args[1]
            order_allocation = db.operation[session.order_allocation_id]
            
            # copy the allocation data to the new packing slip
            # TODO: user/configuration document selection
            # and custom packing slip source and items

            session.packing_slip_id = db.operation.insert(\
            customer_id = order_allocation.customer_id, \
            document_id = session.document_id)

            # TODO: fill packing slip with allocation movements
            for m in db(db.movement.operation_id == session.order_allocation_id).select():
                db.movement.insert(operation_id = session.packing_slip_id, \
                quantity = m.quantity, \
                value = m.value, concept_id = m.concept_id)
                
            order_allocation.update_record(processed = True)
            db.commit()
            
            # create the form
            session.form = SQLFORM(db.operation, session.packing_slip_id, fields=form_fields)

            print T("New packing slip: %(psid)s") % dict(psid=session.packing_slip_id)

        else:
            if session.get("packing_slip_id", None) is not None:
                session.form = SQLFORM(db.operation, session.packing_slip_id, fields=form_fields)
            else:
                # new packing slip
                session.operation_id = session.packing_slip_id = db.operation.insert( \
                document_id = session.document_id)
                session.form = SQLFORM(db.operation, session.operation_id, fields=form_fields)
                db.commit()

            session.form.vars.document_id = session.document_id

        config.html_frame.window.Bind(EVT_FORM_SUBMIT, packing_slip)

    if session.packing_slip_id is not None:
        movements = SQLTABLE(db(\
        db.movement.operation_id == session.packing_slip_id).select(), \
        columns=["movement.movement_id", "movement.code","movement.concept_id", \
        "movement.quantity"], headers={"movement.movement_id": T("ID"), \
        "movement.code": T("Code"), \
        "movement.concept_id": T("Concept"), "movement.quantity": T("Quantity")})

    else:
        movements = None

    return dict(form = session.form, movements = movements, \
    packing_slip_id = session.packing_slip_id)



def ria_product_billing_start(evt, args=[], vars={}):
    """ Presents a packing slips list for billing
    and collects billing details. Creates an invoice
    and redirects the action to the movements update form.
    """
    
    customer_id = session.get("customer_id", None)
    subcustomer_id = session.get("subcustomer_id", None)

    # form to filter packing slips  by customer
    session.form = SQLFORM.factory(Field('customer_id', \
    'reference customer', requires = IS_IN_DB(db, db.customer, "%(legal_name)s")), \
    Field('subcustomer_id', 'reference subcustomer', \
    requires = IS_IN_DB(db, db.subcustomer, "%(legal_name)s")), \
    Field("price_list_id", \
    requires = IS_EMPTY_OR(IS_IN_DB(db(db.price_list), \
    "price_list.price_list_id", "%(description)s"))) )

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.customer_id = session.form.vars.customer_id
            session.subcustomer_id = session.form.vars.subcustomer_id
            session.price_list_id = session.form.vars.price_list_id
            
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="ria_product_billing"))
            
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, ria_product_billing_start)

    return dict(form = session.form)

def ria_product_billing(evt, args=[], vars={}):

    packing_slips = list()
    packing_slips_rows = list()
    checked_list = list()
    document_id = None
    document_type = "S"

    try:
        payment_terms_id = db(db.payment_terms.code == \
        db(db.option.name == "sales_payment_default_payment_terms_code").select().first().value \
        ).select().first().payment_terms_id
    except (AttributeError, KeyError), e:
        print "Failed reading the default payment terms option"
        payment_terms_id = None
        pass

    # get the default supplier option
    try:
        supplier_id = db(db.supplier.code == db( \
        db.option.name=="default_supplier_code" \
        ).select().first().value).select().first().supplier_id
    except (AttributeError, KeyError), e:
        print "Failed reading the default supplier option"
        supplier_id = None

    customer_id = session.get("customer_id", None)
    subcustomer_id = session.get("subcustomer_id", None)

    if (customer_id is None) and (subcustomer_id is None):
        raise Exception("No customer or subcustomer specified")

    q = (db.operation.customer_id == session.customer_id \
    ) | (db.operation.subcustomer_id == session.subcustomer_id)
    q &= db.operation.processed != True
    q &= db.operation.document_id == db.document.document_id
    q &= db.document.packing_slips == True

    packing_slips = db(q).select()
    
    # create packing slips table for selection
    # and the actual billing form
    # TODO: present new eyecandy third party widgets for multiselect box
    for row in packing_slips:
        packing_slips_rows.append(TR(TD(row.operation.operation_id), \
        TD(row.operation.posted), \
        TD(row.operation.code), TD(row.operation.description), \
        INPUT(_type="checkbox", \
        _name="operation_%s" % row.operation.operation_id)))

    documents = db(db.document.invoices == True).select()
    
    document_options = [OPTION(document.description, \
    _value=document.document_id) for document in documents]

    session.form = FORM(TABLE(THEAD(TR(TH(T("Operation")),TH(T("Posted")), \
    TH("Code"), TH("Description"), TH("Bill"))), \
    TBODY(*packing_slips_rows), \
    TFOOT(TR(TD(), TD(), TD(), TD(LABEL(T("Choose a document type"), \
    _for="document_id"), SELECT(*document_options, _name="document_id")), \
    TD(INPUT(_value="Bill checked", _type="submit"))))))

    # operations marked for billing
    bill_items = []

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            for k, v in session.form.vars.iteritems():
                if k.startswith("operation_"):
                    if v == "on":
                        bill_items.append(int(k.split("_")[1]))

            if len(bill_items) > 0:
                # create an invoice  with the collected data
                invoice_id = db.operation.insert( \
                document_id = session.form.vars.document_id, \
                customer_id = customer_id, \
                subcustomer_id =  subcustomer_id, \
                supplier_id = supplier_id, \
                payment_terms_id = payment_terms_id, \
                type = document_type)
                
                # fill the invoice
                for packing_slip_id in bill_items:
                    packing_slip_items = db( \
                    db.movement.operation_id == packing_slip_id).select()
                    for movement in packing_slip_items:
                        value = movement.value
                        amount = movement.amount
                        if session.get("price_list_id", None) is not None:
                            
                            # Calculate price
                            price = db((db.price.price_list_id == session.price_list_id \
                            ) & (db.price.concept_id == movement.concept_id)).select().first()

                            if price is not None:
                                value = price.value
                                amount = price.value * movement.quantity
                            else:
                                print "No valid price record found"
                                value = amount = 0
                            
                        db.movement.insert(operation_id = invoice_id, \
                        concept_id = movement.concept_id, \
                        amount = amount, value = value, \
                        quantity = movement.quantity)
                        
                    # check the packing slip as processed
                    db.operation[packing_slip_id].update_record( \
                    processed = True)

                # TODO: insert ivoices payment / current account movements
                # set invoice as current operation
                session.operation_id = invoice_id
                # redirect to movements edition
                db.commit()
                print T("New invoice created")
                return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

            else:
                print T("No items checked")

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, ria_product_billing)

    return dict(form = session.form)


####################################################################
############ Sequential operation processing (no RIA) ##############
####################################################################


def on_movements_start_submit(evt):
    if session.form.accepts(evt.args, formname=None, \
    keepvalues=False, dbio=False):
        # new operation
        session.operation_id = db.operation.insert( \
        type=session.form.vars.type, \
        description = session.form.vars.description)

        print T("New operation") + " " + str(session.operation_id)
        db.commit()
        
        # call action if redirect
        print T("Redirecting from event")
        config.html_frame.window.OnLinkClicked(URL( \
        a=config.APP_NAME, c="operations", f="movements_header"))

def movements_start(evt, args=[], vars={}):
    """ Initial operation form """

    # erease stock update values
    session.update_stock_list = set()

    session.form = SQLFORM.factory(Field("type", \
    requires=IS_IN_SET({"T": "Stock", "S": \
    "Sales", "P": "Purchases"}), \
    comment=T("Select an operation type")), Field("description"))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, \
    on_movements_start_submit)

    return dict(form = session.form)


def on_movements_header_submit(evt):
    if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):

        # update operation values
        update_operation(session.operation_id, session.form.vars)

        operation = db.operation[session.operation_id]

        db.commit()

        if operation.type in ("S", "P"):
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations" ,f="movements_price_list"))
        else:
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations" ,f="movements_detail"))


def movements_header(evt, args=[], vars={}):
    """ Collect or modify operation basic data"""

    operation_id = session.operation_id
    operation = db.operation[operation_id]

    # default form data
    default_supplier_option = db(db.option.name == "default_supplier_code").select().first()
    default_customer_option = db(db.option.name == "default_customer_code").select().first()
    customer_option = supplier_option = None

    if operation.type == "S":
        fields = ["code", "description", "supplier_id", \
        "customer_id", \
        "detail", "payment_terms_id", "term", "document_id", \
        "branch", "due_date", "voided", "fund_id", \
        "cost_center_id", "observations", "subcustomer_id", \
        "salesperson_id", "jurisdiction_id"]
        supplier_option = default_supplier_option

        # Document form options
        s = db(db.document.entry == True)

    elif operation.type == "T":
        fields = None

        # Document form options
        s = db(db.document.stock == True)
        
    elif operation.type == "P":
        fields = ["code", "description", "supplier_id", \
        "customer_id", \
        "detail", "payment_terms_id", "term", "document_id", \
        "branch", "due_date", "voided", "fund_id", \
        "cost_center_id", "observations", "jurisdiction_id"]
        customer_option = default_customer_option
        
        # Document form options
        s = db(db.document.exit == True)

    else:
        s = db(db.document)
        fields = None

    # Document filter by Sales, Purchases or Stock
    db.operation.document_id.requires = IS_IN_DB(s, "document.document_id", "%(description)s")

    print T("Header form")
    session.form = SQLFORM(db.operation, operation_id, \
    fields = fields)

    # auto-complete header form
    if supplier_option is not None:
        try:
            session.form.vars.supplier_id = db(db.supplier.code == supplier_option.value).select().first().supplier_id
        except (ValueError, TypeError, AttributeError):
            session.form.vars.supplier_id = None
    elif customer_option is not None:
        try:
            session.form.vars.customer_id = db(db.customer.code == customer_option.value).select().first().customer_id
        except (ValueError, TypeError, AttributeError):
            session.form.vars.customer_id = None

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, on_movements_header_submit)
    return dict(form = session.form, operation = operation)

def on_movements_price_list_submit(evt):
    if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
        session.price_list_id = session.form.vars.price_list
        config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

def movements_price_list(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("price_list", \
    requires = IS_IN_DB(db(db.price_list), \
    "price_list.price_list_id", "%(description)s")))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, on_movements_price_list_submit)
    return dict(form = session.form)


def movements_modify_header(evt, args=[], vars={}):
    """ Modify document initial data"""

    fields = ["code", "description", "customer_id", "supplier_id", \
    "detail", "payment_terms_id", "term", "amount", "balance", \
    "posted", "issue", "document_id", "branch", "number", \
    "due_date", "type", "canceled", "processed", "voided", \
    "fund_id", "cost_center_id", "module", "observations", \
    "cancellation", "avoidance", "hour", "replicated", \
    "subcustomer_id", "salesperson_id", "printed", \
    "jurisdiction_id", "replica"]

    readonly = config.session.get("_submitted_form_show", False)
    
    # erease stock update values
    operation_id = session.operation_id
    session.form = SQLFORM(db.operation, operation_id, \
    fields = fields, readonly = readonly
    )
    
    if readonly:
        session._submitted_form_show = False

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            operation = db.operation[operation_id]
            operation.update_record(**session.form.vars)
            db.commit()
            message = T("Operation modified")

            session._submitted_form_message = message
            session._submitted_form_show = True
            
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_modify_header"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_modify_header)

    return dict(form = session.form, message = config.session._submitted_form_message)


def movements_detail(evt, args=[], vars={}):
    """ List of operation items
    
    A user interface to manage movements
    """

    if len(args) > 1:
        if args[0] == "operation":
            operation_id = session.operation_id = int(args[1])
            
    operation_id = session.operation_id

    # Operation options
    update_stock = session.get("update_stock", None)
    warehouse_id = session.get("warehouse_id", None)
    # Tax items are updated by default
    
    update_taxes = session.get("update_taxes", None)
    if update_taxes is None:
        update_taxes = session.update_taxes = True
    
    # selected price list or None
    price_list_id = session.get("price_list_id", None)
    if price_list_id is not None:
        price_list = db.price_list[price_list_id]
    else: price_list = None

    # update operation values
    if is_editable(operation_id):
        update = movements_update(operation_id)
    else:
        update = False
        print T("Operation %(operation)s is not editable") % dict(operation = str(operation_id))

    # Get the operation dal objects
    operation = db.operation[operation_id]
    customer = db(db.customer.customer_id == operation.customer_id \
    ).select().first()
    subcustomer = db( \
    db.subcustomer.subcustomer_id == operation.subcustomer_id \
    ).select().first()
    supplier = db(db.supplier.supplier_id == operation.supplier_id \
    ).select().first()

    movements = dict()

    if warehouse_id is not None:
        warehouse = db.warehouse[warehouse_id].description
    else:
        warehouse = T("None selected")
        
    if update_stock is None:
        update_stock = session.update_stock = False
    
    # Items (Products/Services/Discounts ...)
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.internal != True
    q &= db.concept.tax != True
    q &= db.concept.banks != True
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    columns = ["movement.movement_id", "movement.code", \
    "movement.description", "movement.concept_id", \
    "movement.quantity", "movement.value", "movement.amount"]
    headers = {"movement.movement_id": T("Edit"), \
    "movement.code": T("Code"), \
    "movement.description": T("Description"), \
    "movement.concept_id": T("Concept"), \
    "movement.quantity": T("Quantity"), \
    "movement.value": T("Value"), \
    "movement.amount": T("Amount")}
    
    rows = s.select()
    movements["items"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL( \
    a=config.APP_NAME, c="operations", f="movements_modify_item"))
   
    # Payments
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.banks != True
    q &= ((db.concept.payment_method == True) | ( \
    db.concept.current_account == True))
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    
    rows = s.select()
    movements["payments"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL( \
    a=config.APP_NAME, c="operations", f="movements_modify_item"))

    # Checks
    q = db.bank_check.operation_id == operation_id
    s = db(q)

    rows = s.select()
    movements["checks"] = SQLTABLE(rows, columns = [
        "bank_check.bank_check_id", "bank_check.bank_id", \
        "bank_check.due_date", \
        "bank_check.number", "bank_check.amount"
        ],
        headers = {
        "bank_check.bank_check_id": T("Edit"), \
        "bank_check.bank_id": T("Bank"), \
        "bank_check.due_date": T("Due date"), \
        "bank_check.number": T("Number"), \
        "bank_check.amount": T("Amount")
        }, linkto=URL(a=config.APP_NAME, c="operations", \
        f="movements_modify_check"))
    
    # Taxes
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.tax == True
    q &= db.movement.operation_id == operation_id
    s = db(q)
    
    rows = s.select()
    movements["taxes"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL( \
    a=config.APP_NAME, c="operations", f="movements_modify_item"))

    return dict(operation = operation, \
    movements = movements, price_list = price_list, \
    update_stock = update_stock, warehouse = warehouse, \
    customer = customer, subcustomer = subcustomer, \
    supplier = supplier, update_taxes = update_taxes)


def on_movements_add_item_submit(evt):
    if session.form.accepts(evt.args, formname=None, \
    keepvalues=False, dbio=False):
        # Get the concept record

        # update stock option
        update_stock_list = session.get("update_stock_list", set())
        
        price_list_id = session.get("price_list_id", None)
        operation_id = session.get("operation_id", None)
        concept_id = session.form.vars.item
        quantity = float(session.form.vars.quantity)
        
        try:
            value = float(session.form.vars.value)
        except (ValueError, TypeError):
            # no value specified
            value = None
        amount = None

        # Calculate price
        if (price_list_id is not None) and (value is None):
            price = db((db.price.price_list_id == price_list_id \
            ) & (db.price.concept_id == concept_id) \
            ).select().first()
            value = price.value

        # calculated amount for the movement
        try:
            amount = value * quantity
        except (ValueError, TypeError):
            # No price list or item value
            amount = None

        # Create the new operation item
        if is_editable(operation_id):
            movement_id = db.movement.insert(operation_id = operation_id, \
            amount = amount, value = value, concept_id = concept_id, \
            quantity = quantity)
            print T("Operation: %(o)s. Amount: %(a)s. Value: %(v)s. Concept: %(c)s, Quantity: %(q)s, Movement: %(m)s") \
            % dict(o=operation_id, a=amount, v=value, c=concept_id, q=quantity, m=movement_id)
            
        else:
            movement_id = None
            T("Operation %(id)s is not editable") % dict(id=operation_id)

        # add movement to temporary stock update list
        if session.form.vars.update_stock:
            if movement_id is not None:
                update_stock_list.add(int(movement_id))
            session.update_stock_list = update_stock_list

        db.commit()

        config.html_frame.window.OnLinkClicked(URL( \
        a=config.APP_NAME, c="operations", f="movements_detail"))


def movements_add_item(evt, args=[], vars={}):
    """ Adds an item movement to the operation.

    Note: on-form item value edition needs AJAX and js events
    for db price queries
    """

    try:
        concept_id = args[1]
    except (ValueError, IndexError, TypeError):
        concept_id = None

    # update stock option
    update_stock_list = session.get("update_stock_list", set())
    
    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    price_list_id = session.get("price_list_id", None)

    session.form = SQLFORM.factory(Field("item", \
    requires=IS_IN_DB(db(db.concept.internal != True), \
    "concept.concept_id", "%(description)s"), default = concept_id), \
    Field("value", "double", comment = T("Blank for price list values")), \
    Field("quantity", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6)), Field("update_stock", "boolean", default = True))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, on_movements_add_item_submit)

    return dict(form = session.form)


def movements_modify_item(evt, args=[], vars={}):
    """ Modify an operation's item (or movement). """

    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    try:
        movement = db.movement[args[1]]
        session.movement_id = args[1]
    except IndexError:
        movement = db.movement[session.movement_id]

    session.form = SQLFORM.factory(Field("item", \
    requires=IS_IN_DB(db(db.concept.internal != True), \
    "concept.concept_id", "%(description)s"), default = movement.concept_id), \
    Field("value", "double", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6), default = movement.value), \
    Field("quantity", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6), default = movement.quantity), \
    Field("delete", "boolean", default = False, comment = T("The item will be removed without confirmation")))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.delete:
                # erase the db record if marked for deletion
                if is_editable(operation_id):
                    print T("Erasing record %(id)s") % dict(id=movement.movement_id)
                    movement.delete_record()
                else:
                    print T("Operation %(id)s is not editable") % dict(id=operation_id)
            else:
                # Get the concept record
                concept_id = session.form.vars.item
                quantity = float(session.form.vars.quantity)
                value = amount = None

                value = float(session.form.vars.value)
                amount = value * quantity

                # Modify the operation item
                if is_editable(operation_id):
                    movement.update_record(\
                    amount = amount, value = value, concept_id = concept_id, \
                    quantity = quantity)
                    print T("Operation: %(o)s. Amount: %(a)s. Value: %(v)s. Concept: %(c)s, Quantity: %(q)s") % dict(o=operation_id, a=amount, v=value, c=concept_id, q=quantity)
                else:
                    print T("Operation %(id)s is not editable") % dict(id=operation_id)

            db.commit()

            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_modify_item)        
    return dict(form = session.form)

# modify check


def movements_modify_check(evt, args=[], vars={}):
    """ Modify an operation's item (or movement). """
    
    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]
    
    try:
        bank_check = db.bank_check[args[1]]
        session.bank_check_id = args[1]
    except IndexError:
        bank_check = db.bank_check[session.bank_check_id]

    db.bank_check.concept_id.requires=IS_EMPTY_OR(IS_IN_DB(db, db.concept, "%(description)s"))

    fields = ["checkbook_id", "code", "description", "customer_id", "supplier_id", "number", "bank_id", "amount", "due_date", "detail", "concept_id"]
    session.form = SQLFORM(db.bank_check, bank_check.bank_check_id, fields = fields, deletable = True)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.delete_this_record is not None:
                # erase the db record if marked for deletion
                if is_editable(operation_id):
                    print T("Erasing check %(id)s") % dict(id=bank_check.bank_check_id)
                    bank_check.delete_record()
                else:
                    print T("Operation %(id)s is not editable") % dict(id=operation_id)
            else:
                # Modify the operation item
                if is_editable(operation_id):
                    bank_check.update_record(**session.form.vars)
                else:
                    print T("Operation %(id)s is not editable") % dict(id=operation_id)
            db.commit()
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_modify_check)
    return dict(form = session.form)
# modify check


def movements_add_check(evt, args=[], vars={}):
    operation_id = session.operation_id
    
    """ Adds a check for any operation type """
    # TODO: select different fields for each operation type
    # add own for company checks

    db.bank_check.concept_id.requires=IS_EMPTY_OR(IS_IN_DB(db, db.concept, "%(description)s"))

    fields = [
    "number", "bank_id", "customer_id", "supplier_id", "amount", \
    "due_date", "checkbook_id", "concept_id"
    ]
    
    session.form = SQLFORM(db.bank_check, fields=fields)
    session.form.vars.operation_id = operation_id
    
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            bank_check_id = db.bank_check.insert(**session.form.vars)
            print T("Check added"), bank_check_id

            db.commit()
            
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_add_check)
    return dict(form = session.form)


def movements_current_account_concept(evt, args=[], vars={}):
    """ Manage current account payment/quotas """
    operation_id = session.operation_id
    # calculate the amount for payment
    session.difference = movements_difference(operation_id)
    # create quotas based on user input
    # (for quotas number > 0)
    # define number of quotas and due dates
    session.quota_frequence = datetime.timedelta(int(db( \
    db.option.name == "quota_frequence").select().first().value))
    session.today = datetime.date.today()

    if session.difference <= 0:
        # return 0 amount message and cancel
        print T("0 difference")
        return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="movements_detail"))

    # Current account concepts dal set
    q = db.concept.current_account == True
    s = db(q)

    session.form = SQLFORM.factory(Field("concept", "reference concept", \
    requires = IS_IN_DB(s, "concept.concept_id", "%(description)s")))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.current_account_concept_id = int(session.form.vars.concept)

            db.commit()

            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_current_account_quotas"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_current_account_concept)

    return dict(form = session.form)


def movements_current_account_quotas(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("number_of_quotas", \
    "integer", requires = IS_INT_IN_RANGE(0, 1e3)))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.current_account_quotas = int(session.form.vars.number_of_quotas)

            db.commit()

            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", \
            f="movements_current_account_data"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_current_account_quotas)
    
    return dict(form = session.form)



def movements_current_account_data(evt, args=[], vars={}):
    # Get operation id and check if it is not
    # editable

    operation_id = session.operation_id
    if not is_editable(operation_id):
        print T("Operation %(id)s is not editable") % dict(id=operation_id)
        return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="movements_detail"))
        
    # Begin current account data processing
    try:
        amount_fields = [Field("quota_%s_amount" % (x+1), \
        "double", requires=IS_FLOAT_IN_RANGE(0, 1e6), \
        default=(session.difference / \
        float(session.current_account_quotas))) \
        for x in range(session.current_account_quotas)]
        due_date_fields = [Field("quota_%s_due_date" % (x+1), \
        "date", default=session.today+(session.quota_frequence*x)) \
        for x in range(session.current_account_quotas)]
        form_fields = []
    except ZeroDivisionError:
        # Zero quotas. Create the
        # current account movement
        # for the difference
        db.movement.insert( \
        concept_id = session.current_account_concept_id, \
        amount = session.difference, value = session.difference, \
        quantity = 1, operation_id = operation_id)
        return dict(_redirect=URL(f="movements_detail"))

    for x in range(session.current_account_quotas):
        form_fields.append(amount_fields[x])
        form_fields.append(due_date_fields[x])

    # Present form for user input with
    # quota fields
    session.form = SQLFORM.factory(*form_fields)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # create or modify the payment movements and quotas
            due_dates = dict()
            amounts = dict()
            # Search for current account items
            for var in session.form.vars:
                if var.endswith("amount"):
                    amounts[var.split("_")[1]] = float(session.form.vars[var])
                elif var.endswith("due_date"):
                    due_dates[var.split("_")[1]] = session.form.vars[var]
            for quota, amount in amounts.iteritems():
                # insert quota
                # insert movement
                db.movement.insert( \
                concept_id = session.current_account_concept_id, \
                amount = amount, value = amount, \
                quantity = 1, operation_id = operation_id)
                # insert payments/plans

            db.commit()

            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, \
            c="operations", f="movements_detail"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_current_account_data)

    return dict(form = session.form)


def movements_add_discount_surcharge(evt, args=[], vars={}):
    """ Select discount to apply """

    # Get the session stored operation id
    operation_id = session.operation_id
    
    # user input: concept, % or value, value, description
    q = (db.concept.surcharges == True) | (db.concept.discounts == True)
    session.form = SQLFORM.factory(Field('concept', requires = IS_IN_DB(db(q), \
    "concept.concept_id", "%(description)s")), Field('percentage', \
    'boolean'), Field('value', 'double'), Field('description'))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.percentage:
                # TODO: refined discount/surcharge
                # processing. Move total amount
                # adding to function "total(operation_id)"
                q = db.movement.concept_id == db.concept.concept_id
                q &= db.movement.operation_id == operation_id
                q &= db.concept.internal != True
                q &= db.concept.tax != True
                rows = db(q).select()
                value = float(session.form.vars.value) * \
                float(sum([abs(item.movement.amount) \
                for item in rows])) / 100
            else: value = float(session.form.vars.value)

            if is_editable(operation_id):
                db.movement.insert(operation_id = operation_id, \
                description = session.form.vars.description, quantity = 1, \
                amount = value, value = value, \
                concept_id = session.form.vars.concept)
            else:
                print T("Operation %(id)s is not editable") % dict(id=operation_id)

            db.commit()

            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, \
            c="operations", f="movements_detail"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_add_discount_surcharge)


    return dict(form = session.form)


def movements_list(evt, args = [], vars = {}):

    # filter rows
    session.form = SQLFORM.factory(Field("customer_id", requires=IS_EMPTY_OR(IS_IN_DB(db, db.customer, "%(description)s")), label=T("customer")),
                                   Field("subcustomer_id", requires=IS_EMPTY_OR(IS_IN_DB(db, db.subcustomer, "%(description)s")), label=T("subcustomer")),
                                   Field("since", type="date", label=T("since")),
                                   Field("to", type="date", label=T("to")),
                                   Field("results", type="integer", label=T("results"), default=20))
    limitby = (0,20)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            url = URL(a=config.APP_NAME, c="operations", f="movements_list", vars=session.form.vars)
            return config.html_frame.window.OnLinkClicked(url)
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_list)

    if vars:
        query = db.operation.id > 0
        if not vars["customer_id"] in (None, "", "None"):
            query &= (db.operation.customer_id == vars["customer_id"])
        if not vars["subcustomer_id"] in (None, "", "None"):
            query &= (db.operation.subcustomer_id == vars["subcustomer_id"])
        if not vars["since"] in (None, "", "None"):
            query &= (db.operation.posted >= vars["since"])
        if not vars["to"] in (None, "", "None"):
            query &= (db.operation.posted <= vars["to"])
        if not vars["results"] in (None, "", "None"):
            limitby = (0, int(vars["results"]))
    else:
        query = db.operation

    rows = db(query).select(orderby=~db.operation.operation_id, limitby=limitby)
    
    return dict(rows = rows, form = session.form)

def movements_select(evt, args = [], vars = {}):
    """ Set operation id and open a detail view """
    session.operation_id = args[1]
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="movements_detail"))

def movements_process(evt, args=[], vars={}):
    message = None

    operation_id = session.operation_id

    if not is_editable(operation_id):
        return dict(message = T("Could not process the operation: it is not editable"))
    
    operation = db.operation[operation_id]
    document = operation.document_id
    movements = db(db.movement.operation_id == operation_id).select()

    # offset / payment terms movement
    # Long notation for record id == 0 db issue
    payment_terms = db( \
    db.payment_terms.payment_terms_id == operation.payment_terms_id \
    ).select().first()

    # Purchases offset custom concept
    try:
        purchases_payment_terms_concept_id = db(db.concept.code == db((db.option.name == "purchases_payment_terms_concept_code") & (db.option.args == str(payment_terms.code))).select().first().value).select().first().concept_id
    except AttributeError, e:
        print str(e)
        purchases_payment_terms_concept_id = None
        
    print T("For purchases: %(d)s payment is recorded as concept id %(c)s") % dict(d=payment_terms.description, c=purchases_payment_terms_concept_id)
    
    stock_updated = False

    # receipt documents movement and offset change
    if document.receipts == True:
        receipt_default_offset_concept_id = db(db.concept.code == db(db.option.name == \
        "receipt_default_offset_concept_code").select().first().value).select().first().concept_id
        
        if operation.type == "S":
            receipt_offset_concept_id = db(db.concept.code == db(db.option.name == \
            "sales_receipt_offset_concept_code").select().first().value).select().first().concept_id
            
        elif operation.type == "P":
            receipt_offset_concept_id = db(db.concept.code == db(db.option.name == \
            "purchases_receipt_offset_concept_code").select().first().value).select().first().concept_id

        receipt_offset_concept = db.concept[receipt_offset_concept_id]

        # Search current account movements
        has_current_account_movements = False

        for movement in movements:
            try:
                movement_concept = db(db.concept.concept_id == \
                movement.concept_id).select().first()

                if (movement_concept.current_account != True) and \
                (movement_concept.payment_method != True):
                    # change the movement concept for booking/current accounts
                    # add movement concept to the item description

                    # invert values if needed
                    if (receipt_offset_concept.entry == movement_concept.entry) or (receipt_offset_concept.exit == movement_concept.exit):
                        amount = movement.amount
                    else:
                        amount = (-1)*movement.amount

                    movement.update_record(concept_id = \
                    receipt_offset_concept_id, \
                    description = movement_concept.description, amount = amount)

                    # set operation with current account movements
                    # for offset concept selection
                    if receipt_offset_concept.current_account == True:
                        has_current_account_movements = True

                elif movement_concept.current_account == True:
                    has_current_account_movements = True
            except RuntimeError, e:
                print str(e)

        print T("The operation has current account movements: %(hccm)s") % dict(hccm=has_current_account_movements)

        if has_current_account_movements:
            # set the default payment concept as offset
            offset_concept_id = receipt_default_offset_concept_id
        else:
            offset_concept_id = receipt_offset_concept_id
            
        print T("Setting offset concept to %(description)s") % dict(description=db.concept[receipt_offset_concept_id].description)
        
    else:
        if operation.type == "P" and (purchases_payment_terms_concept_id is not None) and document.invoices:
            offset_concept_id = purchases_payment_terms_concept_id
        else:
            offset_concept_id = payment_terms.concept_id

        config.verbose("Purchases offset concept: %s" % db.concept[offset_concept_id].description)

    # end of receipt documents movement and offset change


    # Calculate difference for payments
    session.difference = movements_difference(operation_id)
    print T("Movements process. Operation: %(id)s") % dict(id=operation_id)
    print T("session.difference :%(difference)s") % dict(difference=session.difference)

    if abs(session.difference) > 0.01:
        # Wich offset / payment concept to record
        # option based offset concept

        offset_concept = db.concept[offset_concept_id]

        # TODO: validate current account limit if offset concept is
        # current account. Move validation to auxiliar function

        if (offset_concept.current_account == \
        True) and (operation.type == "S") and (not document.receipts == True):
            if operation.subcustomer_id is not None:
                current_account_value = \
                crm.subcustomer_current_account_value( \
                db, operation.subcustomer_id)
                print T("Current account value: %(cav)s") % dict(cav=current_account_value)
                try:
                    # Get the current account limit
                    # allowed
                    debt_limit = float( \
                    operation.subcustomer_id.current_account_limit)
                except (TypeError, ValueError, AttributeError):
                    # No limit found
                    debt_limit = 0.00
                    
                print T("Debt limit: %(dl)s") % dict(dl=debt_limit)

                if (current_account_value + session.difference) > debt_limit:
                    return dict(message= \
                    T("Operation processing failed: debt limit reached"))

            elif operation.customer_id is not None:
                current_account_value = \
                crm.customer_current_account_value(db, \
                operation.customer_id)
                print T("Current account value: %(cav)s") % dict(cav=current_account_value)
                try:
                    # Get the current account limit
                    # allowed
                    debt_limit = float( \
                    operation.customer_id.current_account_limit)
                except (TypeError, ValueError, AttributeError):
                    # No limit found
                    debt_limit = 0.00
                    
                print T("Debt limit: %(dl)s") % dict(dl=debt_limit)
                
                if (current_account_value + session.difference) > debt_limit:
                    return dict(message= \
                    T("Operation processing failed: debt limit reached"))

        # Offset / Payment movement
        # TODO: change difference sign checking debit/credit
        # for now it only calculates correctly if offset concept has exit = True
        
        movement_id = db.movement.insert(operation_id = \
        operation_id, concept_id = offset_concept.concept_id, \
        quantity = 1, amount = session.difference, value = \
        session.difference)

        print T("Movement (offset): %(ds)s: %(amount)s") % dict(ds=db.movement[movement_id].concept_id.description, amount=db.movement[movement_id].amount)

        # update the operation
        updated = movements_update(operation_id)

    # TODO: operation difference revision (for accounting)

    result = None
    stock_updated = None

    # process operation
    if document.countable and operation.type in ("S", "P"):
        result = operations.process(db, session, session.operation_id)
        # print "Bypassing the operation processing"
        # result = True

    # change stock values if requested
    if (session.get("update_stock", False) == True) and (result != False):
        stock_updated = movements_stock(operation_id)

    if (result == False) or (stock_updated == False):
        message = T("The operation processing failed. Booking ok: %(result)s. Stock ok: %(su)s") % dict(result=result, su=stock_updated)
    else:
        message = T("Operation successfully processed")
        db.commit()

    # TODO: rollback on errors
    
    return dict(message=message)


def movements_option_update_stock(evt, args=[], vars={}):
    """ Switch session update stock value """
    if session.update_stock == True:
        session.update_stock = False
    elif session.update_stock == False:
        session.update_stock = True
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="movements_detail"))

def movements_option_update_taxes(evt, args=[], vars={}):
    """ Switch session update taxes value """
    if session.update_taxes == True:
        session.update_taxes = False
    elif session.update_taxes == False:
        session.update_taxes = True

    print T("Change update taxes value to %(ut)s") % dict(ut=session.update_taxes)
    return dict(_redirect=URL(a=config.APP_NAME, c="operations", f="movements_detail"))

def movements_select_warehouse(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("warehouse", \
    requires = IS_IN_DB(db(db.warehouse), \
    "warehouse.warehouse_id", "%(description)s")))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.warehouse_id = session.form.vars.warehouse
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_select_warehouse)
    return dict(form = session.form)


def on_movements_add_payment_method_submit(evt):
    # on form validation process values
    if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
        # form name shortcuts and values filter
        detail = session.form.vars.detail
        reference = session.form.vars.payment_reference_number

        try:
            quotas = int(session.form.vars.quotas)
        except (ValueError, TypeError):
            quotas = 0

        try:
            amount = float(session.form.vars.amount)
        except (ValueError, TypeError):
            amount = 0.0

        try:
            surcharge = float(session.form.vars.surcharge)
        except:
            surcharge = 0.0

        # calculate the total amount with surcharge
        # when specified
        amount = amount*surcharge/100.0 + amount

        # Detailed quota amounts (uniform quota values)
        if quotas >1:
            quota_amount = amount/float(quotas)
            detail += T(" Quotas: %s x%.2f") % (quotas, quota_amount)

        # Payment services transaction number in detail
        if len(reference) > 0:
            detail += T(" Transaction number: %(r)s") % dict(r=reference)

        # insert the movement record if amount is not 0
        if amount != 0.0:
            db.movement.insert(operation_id = session.operation_id, \
            concept_id = session.form.vars.method, detail = detail, \
            amount = amount, description = detail, \
            value = amount, quantity = 1)

            db.commit()

        return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))


def movements_add_payment_method(evt, args=[], vars={}):
    # custom payment form
    operation = db.operation[session.operation_id]
    session.form = SQLFORM.factory(Field("method", "reference concept", \
    requires = IS_IN_DB(db(db.concept.payment_method == True), \
    "concept.concept_id", "%(description)s")), Field("amount", \
    "decimal(10,2)"), Field("quotas", "integer"), \
    Field("surcharge", "double"), Field("detail"), \
    Field("payment_reference_number", \
    comment = T("i.e. third party payment transaction number")))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, on_movements_add_payment_method_submit)
    return dict(form = session.form)


def movements_add_tax(evt, args=[], vars={}):
    operation = db.operation[session.operation_id]
    s = db(db.concept.tax == True)
    session.form = SQLFORM.factory(Field("concept", requires = IS_IN_DB(s, "concept.concept_id", "%(description)s")), Field("value", "double", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6)))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            movement_id = db.movement.insert(operation_id = operation.operation_id, \
            concept_id = session.form.vars.concept, value = session.form.vars.value, \
            quantity = 1, amount = session.form.vars.value)
            print T("Added movement"), movement_id

            db.commit()
            
        config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="movements_detail"))

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_add_tax)
    return dict(form = session.form)


# self-submitted form (stores post form query in config.py)
def movements_articles(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("category", \
    "reference category", requires = IS_IN_DB(db, db.category, \
    "%(description)s")), Field("subcategory", \
    "reference subcategory", requires = IS_IN_DB(db, db.subcategory, \
    "%(description)s")), Field("supplier", "reference supplier", \
    requires = IS_IN_DB(db, db.supplier, "%(legal_name)s")))
    table = None

    # form submitted
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, \
        keepvalues=False, dbio=False):
            # list items for selection
            q = db.concept.category_id == session.form.vars.category
            q &= db.concept.subcategory_id == session.form.vars.subcategory
            q &= db.concept.supplier_id == session.form.vars.supplier
            rows = db(q).select()

            print "Records: ", db(q).count()

            columns = ["concept.concept_id", "concept.code", \
            "concept.description", "concept.family_id", \
            "concept.color_id"]
            headers = {"concept.concept_id": T("Select"), \
            "concept.code": T("Code"), \
            "concept.description": T("Description"), \
            "concept.family_id": T("Family"), \
            "concept.color_id": T("Color")}

            config.after_submission["table"] = SQLTABLE(rows, \
            columns = columns, headers = headers, linkto = URL( \
            a=config.APP_NAME, c="operations", f="movements_add_item"))
            config.html_frame.window.OnLinkClicked(URL( \
            a=config.APP_NAME, c="operations", f="movements_articles"))

    if "table" in config.after_submission:
        table = config.after_submission["table"]
        config.after_submission["table"] = None

    config.html_frame.window.Bind(EVT_FORM_SUBMIT, movements_articles)

    return dict(form = session.form, table = table)


def articles(evt, args=[], vars={}):
    # TODO: allow unspecified fields
    session.form = SQLFORM.factory(Field("category", "reference category", requires = IS_IN_DB(db, db.category, "%(description)s")), Field("subcategory", "reference subcategory", requires = IS_IN_DB(db, db.subcategory, "%(description)s")), Field("supplier", "reference supplier", requires = IS_IN_DB(db, db.supplier, "%(legal_name)s")))

    q = None
    
    # form submitted
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # list items for selection
            q = db.concept.category_id == session.form.vars.category
            q &= db.concept.subcategory_id == session.form.vars.subcategory
            q &= db.concept.supplier_id == session.form.vars.supplier

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, articles)

    if q is not None:
        config.session.articles_query = q
        config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="articles_list"))

    return dict(form = session.form)

def articles_list(evt, args=[], vars={}):
    rows = db(config.session.articles_query).select()
    table = None
    if len(rows) > 0:
        table = SQLTABLE(rows, linkto=URL(a=config.APP_NAME, c="appadmin", f="update"))
    return dict(table = table, back=A(T("New query"), _href=URL(a=config.APP_NAME, c="operations", f="articles")))
