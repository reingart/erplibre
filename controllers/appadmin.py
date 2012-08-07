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

from gluon import *
import gluon

import gluon.validators

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db
T = config.env["T"]
session = config.session

def index(evt, args=[], vars={}):

    static_tables_list = []
    table_groups = dict()
    for k, v in db.static_table_tags.iteritems():
        if not v in table_groups:
            table_groups[v] = list()
        table_groups[v].append(k)
        static_tables_list.append(k)

    # Add tables not listed in the static list
    # in common group
    for table in db.tables:
        if not str(table) in static_tables_list:
            table_name = str(table)
            if "common" in table_groups.keys():
                if not table_name.startswith("_"):
                    table_groups["common"].append(table_name)

    return dict(table_groups = table_groups)


def select(evt, args=[], vars={}):
    # get table
    # get limits or default limits
    table_name = args[0]

    """

    # This section does not work
    # properly with PostgreSQL
    # (default orderby parameters misconfigure
    # the list of items shown)

    # TODO: imitate web2py appadmin select action
    
    table = None
    links = None
    q = None
    upper_limit = None
    lower_limit = None
    db_table = db[table_name]

    try:
        id_field = db_table["%s_id" % table_name]
        id_field_name = "%s_id" % table_name
    except KeyError:
        id_field = db_table["id"]
        id_field_name = "id"
        
    first_row_id = vars.get("first_row_id", None)
    last_row_id = vars.get("last_row_id", None)
    
    if "upper_limit" in vars and "lower_limit" in vars:
        upper_limit = vars["upper_limit"]
        lower_limit = vars["lower_limit"]
        q = (id_field <= int(upper_limit)) & (id_field >= int(\
        lower_limit))

    else:
        if config.session.get("items_per_page", None) is None:
            try:
                # search default options in db
                config.session.items_per_page = db(\
                db.option.name=="items_per_page"\
                ).select().first().value
            except:
                config.session.items_per_page = 10

        # create links list
        rows = db(db_table).select()

        config.session.select_pages = []
        
        if len(rows) > 0:
            first_row_id = rows.first()[id_field_name]
            last_row_id = rows.last()[id_field_name]

            # counter = first_row_id
            subcounter = 0

            tmp_pages = []
            
            for row in rows:
                if row[id_field_name] != last_row_id:
                    tmp_pages.append(row[id_field_name])
                    # counter +=1
                    subcounter += 1
                    if subcounter >= config.session.items_per_page:
                        config.session.select_pages.append(tmp_pages)
                        tmp_pages = list()
                        subcounter = 0
                        
                elif row[id_field_name] == last_row_id:
                    tmp_pages.append(row[id_field_name])
                    # counter +=1
                    # subcounter += 1
                    config.session.select_pages.append(tmp_pages)
                else:
                    break

            if len(config.session.select_pages) > 0:
                lower_limit = config.session.select_pages[0][0]
                upper_limit = config.session.select_pages[0][len(\
                config.session.select_pages[0]) -1]
                
                # first query

                
                q = id_field >= config.session.select_pages[0][0]
                q &= id_field <= config.session.select_pages[0][len(\
                config.session.select_pages[0]) -1]

    if len(config.session.select_pages) > 0:
        page_links = []
        for sp in config.session.select_pages:
            if len(sp) > 0:
                url = URL(a=config.APP_NAME, \
                    c="appadmin", f="select", \
                    args=[table_name], \
                    vars={"lower_limit": sp[0], \
                    "upper_limit": sp[len(sp) -1] })
                text = "%s-%s" % (sp[0], \
                    sp[len(sp) -1])

                if sp[0] == lower_limit:
                    a = A(text, _href=url)
                else:
                    a = EM(A(text, _href=url))

                page_links.append(a)

        links = [SPAN(link) for link in page_links]
    """

    links = []

    db_table = db[table_name]
    q = db_table

    if table_name + "_id" in db_table.fields:
        orderby = table_name + "_id"
    else:
        orderby = "id"

    # create table
    if q is not None:
        rows = db(q).select(orderby=orderby)

    return dict(links = links, table_name = table_name, rows = rows)


def update(evt, args=[], vars={}):

    if len(args) > 0:
        # get table
        config.session.db_table = db[args[0]]
        # get record id
        config.session.record_id = args[1]

    # create form
    session.form = SQLFORM(config.session.db_table, config.session.db_table[config.session.record_id], deletable = True)
    
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # on validation, update the db record
            if config.session.form.vars.delete_this_record is not None:
                config.session.db_table[config.session.record_id].delete_record()
                db.commit()
                print T("Record deleted")
                config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="select", args=[str(config.session.db_table)]))
            else:
                config.session.db_table[config.session.record_id].update_record(**session.form.vars)
                db.commit()
                print T("Record updated")
                config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="read", args=[str(config.session.db_table), config.session.record_id]))
        elif session.form.errors:
            print T("The form has errors")
            print "####################"
            for e in session.form.errors:
                print e


                
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, update)

    return dict(form=session.form)


def read(evt, args=[], vars={}):
    session.form = SQLFORM(db[args[0]], args[1], readonly=True)
    return dict(form = session.form, table_name = args[0])


def create(evt, args=[], vars={}):
    if len(args) > 0:
        # get table
        config.session.db_table = db[args[0]]

    # create form
    config.session.form = SQLFORM(config.session.db_table)

    if evt is not None:
        if config.session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            # on validation, insert the db record
            config.session.record_id = config.session.db_table.insert(**config.session.form.vars)
            db.commit()
            print T("Form accepted")
            config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="read", args=[str(config.session.db_table), config.session.record_id]))
        elif config.session.form.errors:
            print T("The form has errors")
            print "####################"
            for e in config.session.form.errors:
                print e

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, create)


    return dict(form = config.session.form, table=config.session.db_table)
