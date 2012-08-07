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

""" Setup for development db """
import os

from gluon import *
import gluon

import gluon.validators

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db
session = config.session

T = config.env["T"]

def configure(evt, args=[], vars={}):
    configure_options = []
    session.form = None
    if evt is None:
        for name in dir(config):
            if isinstance(getattr(config, name), basestring) and name.isupper():
                configure_options.append(Field(name, type="string", default=getattr(config, name)))
        session.form = SQLFORM.factory(*configure_options)
    return dict(form=session.form)

def index(evt, args=[], vars={}):
    
    # get or create admin users group
    try:
        session.admin_group_id = db(db.auth_group.role == "admin").select().first().id
    except (AttributeError, KeyError, ValueError):
        session.admin_group_id = None
    
    if session.get("admin_group_id", None) is None:
        session.admin_group_id = db.auth_group.insert(role="admin")
        db.commit()
        print T("Admin user group created")

    # create an admin user creation form
    session.form = SQLFORM.factory(Field("first_name", requires=IS_NOT_EMPTY()), Field("last_name", requires=IS_NOT_EMPTY()), Field("email", requires=IS_EMAIL()), Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)), Field("retype_password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)))

    # look for administrative user
    try:
        session.admin_user_id = db(db.auth_membership.group_id == session.admin_group_id).select().first().id
    except (AttributeError, KeyError, ValueError):
        session.admin_user_id = None

    # if no admin user prompt (form) user and password for creation
    if session.admin_user_id is None:
        first_run_form = session.form
    else:
        first_run_form = None

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.password == session.form.vars.retype_password:
                session.admin_user_id = db.auth_user.insert(first_name = session.form.vars.first_name, \
                last_name = session.form.vars.last_name, email = session.form.vars.email, \
                password = session.form.vars.password)

                # assign admin membership
                db.auth_membership.insert(user_id = session.admin_user_id, group_id = session.admin_group_id)

                db.commit()
                
                print T("User %s created") % session.admin_user_id
                print T("You should configure a firm tax id to use ordering forms")
                
                return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="setup", f="index"))
            else:
                print T("The passwords do not match")
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, index)

    actions = [
        A("Options", _href=URL(a=config.APP_NAME, c="setup", f="options")), \
        A("Load example db from CSV", _href=URL(a=config.APP_NAME, c="migration", f="import_csv_dir")), \
        A("Load db records from a CSV file", _href=URL(a=config.APP_NAME, c="migration", f="csv_to_db")), \
        A("Export db records to a CSV file", _href=URL(a=config.APP_NAME, c="migration", f="db_to_csv")), \
        A("Set App language", _href=URL(a=config.APP_NAME, c="setup", f="set_language")),
        ]

    # Redirection message
    if config.session.get("message", None) is not None:
        vars["message"] = config.session.message
        config.session.message = None
        
    return dict(actions = actions, first_run_form = first_run_form, vars = vars, language = config.LANGUAGE)


def setup(evt, args=[], vars={}):
    return dict()


def options(evt, args=[], vars={}):
    the_options = SQLTABLE(db(db.option).select(), linkto=URL(a=config.APP_NAME, c="setup", f="option"))
    return dict(options = the_options)


def option(evt, args=[], vars={}):
    if len(args) > 0:
        session.the_option_id = args[1]
    else:
        if evt is None:
            session.the_option_id = None
        
    if session.get("the_option_id", None) is not None:
        session.form = SQLFORM(db.option, session.the_option_id)
    else:
        session.form = SQLFORM(db.option)

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.get("the_option_id", None) is None:
                session.the_option_id = db.option.insert(**session.form.vars)
            else:
                session.the_option_id = db.option[session.the_option_id].update_record(**session.form.vars)
            db.commit()
            print T("Form accepted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="setup", f="options"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, option)

    return dict(form = session.form)


def set_language(evt, args=[], vars={}):
    languages = []
    for language in os.listdir(os.path.join(config.GUI2PY_APP_FOLDER, "languages")):
        if not (language.startswith("_") or language.startswith(".")):
            languages.append(language[:-3])

    session.form = SQLFORM.factory(Field("language", label=T("language"), requires=IS_IN_SET(languages)))

    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.language is not None:
                if len(session.form.vars.language) > 0:
                    print T("Changing config.ini language value to %s") % session.form.vars.language
                    config.LANGUAGE = session.form.vars.language
                    data = dict([(d, getattr(config, d)) for d in dir(config) \
                    if isinstance(getattr(config, d), basestring)])
                    config.write_values(data)
                    print T("Please restart the desktop application")

    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, set_language)
    
    return dict(form = session.form, languages = languages)


def initialize():
    # not used
    message = ""
    
    # general dictionary for db initial setup
    # Incomplete
    
    # db data input design:
    # records: {
    #    "table_x": [ { "field_a": value, "field_b": value, ... }, ... { } ]
    # }
    
    records = dict()
    
    # for each tablename in records
    #     for each dictionary object obj in records["tablename"]:
    #         insert unpacked obj in tablename
    
    message=T("Done")
    return dict(message=message, records = len(records))


