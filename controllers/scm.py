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

T = config.env["T"]
db = config.db
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


def index():
    return dict()

def ria_stock(evt, args=[], vars={}):
    stock_list = None
    session.form = SQLFORM.factory(
    Field('warehouse', 'reference warehouse', \
    requires=IS_EMPTY_OR(IS_IN_DB(db, db.warehouse, \
    '%(description)s'))), \
    Field('product', 'reference concept', \
    requires = IS_EMPTY_OR(IS_IN_DB(db(\
    db.concept.stock == True), \
    'concept.concept_id', '%(description)s')))
    )

    session.q = session.get("q", None)

    # Query for the stock list
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            session.q = None
            warehouse_query = db.stock.warehouse_id == \
            session.form.vars.warehouse
            product_query = db.stock.concept_id == \
            session.form.vars.product
            
            # filter by product if requested
            if session.form.vars.product is not None:
                if len(session.form.vars.product) > 0:
                    session.q = product_query

            if session.form.vars.warehouse is not None:
                if len(session.form.vars.warehouse) > 0:
                    if session.q is None:
                        session.q = warehouse_query
                    else:
                        session.q &= warehouse_query

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="scm", f="ria_stock"))

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, ria_stock)
        
    if session.q is None: session.q = db.stock

    # stock list records
    s = db(session.q)
    rows = s.select()

    # TODO: presentation code should go into the view
    columns = ['stock.stock_id', 'stock.code', \
    'stock.concept_id', \
    'stock.posted', 'stock.value']
    headers = {'stock.stock_id': T('Edit'), 'stock.code': T('Code'), \
    'stock.concept_id': T('Product'), 'stock.posted': T('Posted'), \
    'stock.value': T('Value')}

    # TODO: unify action/function naming conventions
    stock_list = SQLTABLE(rows, columns = columns, \
    headers = headers, \
    linkto=URL(a=config.APP_NAME, c="scm", f="stock_item_update"))

    change_stock_form = A(T("Change stock"), _href=URL(a=config.APP_NAME, c="scm", f="change_stock"))
    stock_movement_form = A(T("Stock movement"), _href=URL(a=config.APP_NAME, c="scm", f="stock_movement"))


    return dict(stock_list = stock_list, \
    stock_query_form = session.form, \
    stock_movement_form = stock_movement_form, \
    change_stock_form = change_stock_form)

def stock_item_update(evt, args=[], vars={}):
    if len(args) > 1:
        session.stock_id = args[1]

    session.form = SQLFORM(db.stock, session.stock_id)
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            db.stock[session.stock_id].update_record(**session.form.vars)
            db.commit()
            print T("Record updated")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="scm", f="ria_stock"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, stock_item_update)
        
    return dict(form = session.form)

def stock_movement(evt, args=[], vars={}):
    # Move stock
    session.form = SQLFORM.factory(\
    Field('product', 'reference concept', \
    requires = IS_IN_DB(db(db.concept.stock == True), \
    'concept.concept_id', '%(description)s')), \
    Field('warehouse', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, '%(description)s')), \
    Field('destination', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, \
    '%(description)s')), Field('quantity', \
    'double', \
    requires=IS_FLOAT_IN_RANGE(-1e6, 1e6)), \
    )
    
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            stock_item_source = db((\
            db.stock.concept_id == session.form.vars.product) & (\
            db.stock.warehouse_id == session.form.vars.warehouse)).select(\
            ).first()
            if session.form.vars.warehouse == session.form.vars.destination:
                print T("Please choose different warehouses")
                
            elif stock_item_source is not None:
                tmp_stock_value = stock_item_source.value - float(\
                session.form.vars.quantity)
                if tmp_stock_value < 0:
                    # negative stock
                    print T("Insufficient source stock quantity")
                else:
                    # get or create a stock
                    stock_item_destination = db((\
                    db.stock.warehouse_id == session.form.vars.destination\
                    ) & (\
                    db.stock.concept_id == session.form.vars.product)\
                    ).select().first()
                    if stock_item_destination is None:
                        stock_item_destination_id = db.stock.insert(\
                        warehouse_id = session.form.vars.destination, \
                        concept_id = session.form.vars.product, value = 0.0)
                    else:
                        stock_item_destination_id = \
                        stock_item_destination.stock_id

                    stock_item_source.update_record(\
                    value = stock_item_source.value - \
                    float(session.form.vars.quantity))
                    old_value = float(\
                    db.stock[stock_item_destination_id].value)
                    db.stock[stock_item_destination_id].update_record(\
                    value = old_value + float(session.form.vars.quantity))
                    
                    db.commit()
                    print T("Stock updated")
                    return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="scm", f="ria_stock"))

            else:
                # the item does not exist
                print T("The item specified was not found in the warehouse")

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, stock_movement)

    return dict(form = session.form)


def change_stock(evt, args=[], vars={}):
    # Change stock value
    session.form = SQLFORM.factory(
    Field('product', 'reference concept', \
    requires = IS_IN_DB(db(db.concept.stock == True), \
    "concept.concept_id", "%(description)s")), \
    Field('warehouse', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, '%(description)s')), \
    Field('quantity', 'double', \
    requires=IS_FLOAT_IN_RANGE(-1e6, +1e6)), \
    )

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            stock_item = db((\
            db.stock.concept_id == session.form.vars.product) & \
            (db.stock.warehouse_id == session.form.vars.warehouse\
            )).select().first()
            if stock_item is None:
                stock_item_id = db.stock.insert(\
                warehouse_id = session.form.vars.warehouse, \
                concept_id = session.form.vars.product, value = 0.0)
            else:
                stock_item_id = stock_item.stock_id

            tmp_value = db.stock[stock_item_id].value + \
            float(session.form.vars.quantity)

            if tmp_value < 0:
                print T("Insufficient stock value.")
            else:
                db.stock[stock_item_id].update_record(\
                value = tmp_value)
                db.commit()
                print T("Stock value changed")
                return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="scm", f="ria_stock"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, change_stock)
    return dict(form = session.form)


