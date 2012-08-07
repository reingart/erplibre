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
T = config.env["T"]
session = config.session
request = config.request


# modules = __import__('applications.%s.modules' % config.WEB2PY_APP_NAME, globals(), locals(), ['operations', 'crm'], -1)
# crm = modules.crm
# operations = modules.operations
from modules import crm, operations

# import applications.erplibre.modules.operations as operations
# import applications.erplibre.modules.crm as crm

import datetime

from gui2py.form import EVT_FORM_SUBMIT


def index(): return dict(message="hello from crm.py")


def customer_panel(evt, args=[], vars={}):
    """ Customer on-line panel. Show info/stats/links to actions"""
    contact_user = db(db.contact_user.user_id == config.auth.user_id).select().first()
    if contact_user is None:
        return dict(customer_orders = None, message=T("No tax id selected"), customer = None)
    try:
        contact = db(db.contact.contact_id == contact_user.contact_id).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.customer_id == contact.customer_id).select().first()
    except KeyError:
        customer = None
    
    now = datetime.datetime.now()
    delta = datetime.timedelta(7)
    time_limit = now - delta

    q = db.operation.document_id == db.document.document_id
    q &= db.document.orders == True
    preset = db(q)

    # show orders for user contact configured customer (used in customer web interface)
    # customer_orders_set = preset((db.operation.customer_id == customer) & (db.operation.posted >= time_limit))
    
    # show orders for any customer
    customer_orders_set = preset((db.operation.posted >= time_limit))
    """
    TODO: filter by order document type

    # list all document types with orders == True
    order_documents = db(db.document.orders == True).select()
    order_documents_list = [document.document_id for document in order_documents]    
    # make a subset of operations with order documents
    customer_orders_subset = customer_orders_set & db()
    """
    # get operation rows
    customer_orders = customer_orders_set.select()

    return dict(customer_orders = customer_orders, message=T("Customer panel"), customer = customer)


def current_account_report(evt, args=[], vars={}):
    """ Performs a query of operations and
    returns the current account data
    """
    # 
    session.total_debt = session.get("total_debt", 0.00)

    operations = None
    
    # customer / subcustomer selection form
    session.form = SQLFORM.factory(Field('customer', 'reference customer', \
    requires=IS_IN_DB(db, db.customer, "%(legal_name)s")), Field('subcustomer', \
    'reference subcustomer', requires=IS_EMPTY_OR(IS_IN_DB(db, db.subcustomer, "%(legal_name)s"))))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            q = ((db.operation.customer_id == session.form.vars.customer) | \
                (db.operation.subcustomer_id == session.form.vars.subcustomer))
            q &= (db.operation.document_id == db.document.document_id)
            q &= ((db.document.receipts == True) | (db.document.invoices == True))

            session.operation_q = q
            the_set = db(q)

            session.customer_id = session.form.vars.customer
            session.subcustomer_id = session.form.vars.subcustomer

            # a naive current account total debt
            # TODO: complete and customizable current
            # account processing

            for row in the_set.select():
                try:
                    if row.operation.amount is not None:
                        if row.document.receipts == True:
                            session.total_debt -= row.operation.amount
                        elif row.document.invoices == True:
                            session.total_debt += row.operation.amount
                except (ValueError, TypeError), e:
                    print T("Could not calculate operation") + " %s: %s" % str(row.operation.operation_id, e)

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="crm", f="current_account_report"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, current_account_report)


    if session.operation_q is not None:
        columns = ["operation.operation_id", "operation.posted", \
        "operation.amount", "operation.customer_id", \
        "operation.subcustomer_id", "document.description"]
        headers = { "operation.operation_id": T("Edit"), \
        "operation.posted": T("Posted"), "operation.amount": T("Amount"), \
        "operation.customer_id": T("Customer"), \
        "operation.subcustomer_id": T("Subcustomer"), \
        "document.description": T("Document") }

        operations = SQLTABLE(db(session.operation_q).select(), columns=columns, \
        headers=headers, linkto=URL(a=config.APP_NAME, c="operations", f="ria_movements"))
        
    return dict(query_form = session.form, operations = operations, \
    total_debt = session.total_debt, customer = db.customer[session.customer_id], \
    subcustomer = db.subcustomer[session.subcustomer_id])


def new_customer():
    form = crud.create(db.customer)
    return dict(form = form)

def new_subcustomer():
    form = crud.create(db.subcustomer)
    return dict(form = form)

def customer_current_account_status(evt, args=[], vars={}):
    if args[0] == "customer":
        customer = db.customer[args[1]]
        value = crm.customer_current_account_value(db, \
        customer.customer_id)
    elif args[0] == "subcustomer":
        customer = db.subcustomer[args[1]]
        value = crm.subcustomer_current_account_value(db, \
        customer.subcustomer_id)
        
    return dict(value = value, customer = customer)
    