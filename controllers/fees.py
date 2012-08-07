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


# modules = __import__('applications.%s.modules' % config.WEB2PY_APP_NAME, globals(), locals(), ['operations', 'crm'], -1)
# crm = modules.crm
# operations = modules.operations

from modules import crm, operations

# import applications.erplibre.modules.operations as operations
# import applications.erplibre.modules.crm as crm

from gui2py.form import EVT_FORM_SUBMIT

def index(): return dict(message="hello from fees.py")

def list_fees(evt, args=[], vars={}):
    return dict(fees = SQLTABLE(db(db.fee).select(), \
    columns = ["fee.fee_id", "fee.code", "fee.description", \
    "fee.due_date", "fee.document_id", "fee.starting", "fee.ending"], \
    headers = {"fee.fee_id": T("Edit"), "fee.code": T("Code"), \
    "fee.description": T("Description"), "fee.due_date": T("Due date"), \
    "fee.document_id": T("Document"), "fee.starting": T("Starting"), \
    "fee.ending": T("Ending")}, \
    linkto=URL(a=config.APP_NAME, c="fees", f="update_fee")))
    
def update_fee(evt, args=[], vars={}):

    if len(args) > 1:
        session.fee_id = args[1]
    session.form = SQLFORM(db.fee, session.fee_id)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.fee[session.fee_id].update_record(**session.form.vars)
            db.commit()
            print T("Fee updated")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="fees", f="list_fees"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_fee)

    return dict(form = session.form)
    
def create_fee(evt, args=[], vars={}):
    session.form = SQLFORM(db.fee)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.fee.insert(**session.form.vars)
            db.commit()
            print T("Fee updated")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="fees", f="list_fees"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, create_fee)
    return dict(form = session.form)

def list_installments(evt, args=[], vars={}):
    operation = db.operation[session.operation_id]
    
    query = (db.installment.customer_id == operation.customer_id)
    query |= (db.installment.subcustomer_id == operation.subcustomer_id)
    query |= (db.installment.supplier_id == operation.supplier_id)

    preset = db(query)
    
    return dict(installments = SQLTABLE(preset.select(), \
    columns = ["installment.installment_id","installment.customer_id",\
    "installment.subcustomer_id","installment.supplier_id", \
    "installment.fee_id", "installment.quotas"], \
    headers = {"installment.installment_id": T("Edit"), \
    "installment.customer_id": T("Customer"),\
    "installment.subcustomer_id": T("Subcustomer"), \
    "installment.supplier_id": T("Supplier"), \
    "installment.fee_id": T("Fee"), "installment.quotas": T("Quotas")}, \
    linkto=URL(a=config.APP_NAME, c="fees", f="update_installment")))


def update_installment(evt, args=[], vars={}):
    if len(args) > 1:
        session.installment_id = int(args[1])
    session.form = SQLFORM(db.installment, session.installment_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.installment[session.installment_id].update_record(**session.form.vars)
            db.commit()
            print T("Installment updated")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="fees", f="update_installment"))
            
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_installment)

    quotas = SQLTABLE(db(\
    db.quota.installment_id == session.installment_id).select(), \
    columns = ["quota.quota_id","quota.number",\
    "quota.due_date", \
    "quota.fee_id", "quota.amount"], \
    headers = {"quota.quota_id": T("Edit"),"quota.number": T("Number"),\
    "quota.due_date": T("Due date"), \
    "quota.fee_id": T("Fee"), "quota.amount": T("Quota")}, \
    linkto=URL(a=config.APP_NAME, c="fees", f="update_quota.html"))

    return dict(form = session.form, quotas = quotas)


def list_quotas():
    return dict(quotas = SQLTABLE(db(\
    db.quota.installment_id == session.installment_id).select(), \
    columns = ["quota.quota_id","quota.number",\
    "quota.due_date", \
    "quota.fee_id", "quota.amount"], \
    headers = {"quota.quota_id": T("Edit"),"quota.number": T("Number"),\
    "quota.due_date": T("Due date"), \
    "quota.fee_id": T("Fee"), "quota.amount": T("Quota")}, \
    linkto=URL(a=config.APP_NAME, c="fees", f="update_quota.html")))
    
def update_quota(evt, args=[], vars={}):
    if len(args) > 1:
        session.quota_id = args[1]
    session.form = SQLFORM(db.quota, session.quota_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.quota[session.quota_id].update_record(**session.form.vars)
            db.commit()
            print T("Quota updated")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="fees", f="update_installment"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update_quota)
    return dict(form = session.form)
