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
imapdb = config.imapdb
session = config.session
auth = config.auth
request = config.request
response = config.response

T = config.env["T"]

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  


def index(evt, args = [], vars = {}):
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    
    Project's index page
    """
    # Feedback for action redirections
    
    message = config.session.get("message", None)
    if config.session.message is None:
        message = "Desktop App"
    else:
        config.session.message = None

    return dict(message=message)


def change_layout_colors(evt, args=[], vars={}):
    if session.get("layout_colors", None) is None:
        session.layout_colors = ["#" + color for color in config.COLORS]

    if session.layout_colors_background is not None:
        background = session.layout_colors_background
    else:
        background = ""
    if session.layout_colors_background is not None:
        foreground = session.layout_colors_foreground
    else:
        foreground = ""
    if session.layout_colors_background is not None:
        links = session.layout_colors_links
    else:
        links = ""

    session.form = SQLFORM.factory(Field("background", default=background), Field("foreground", default=foreground), Field("links", default=links), Field("random", "boolean"))
    
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            if session.form.vars.random == True:
                import random
                session.layout_colors_background = "#" + str(random.choice(config.COLORS))
                session.layout_colors_foreground = "#" + str(random.choice(config.COLORS))
                session.layout_colors_links = "#" + str(random.choice(config.COLORS))
            else:
                session.layout_colors_background = session.form.vars.background
                session.layout_colors_foreground = session.form.vars.foreground
                session.layout_colors_links = session.form.vars.links

            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="change_layout_colors"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, change_layout_colors)

    for tag in session.form.elements("input [type=text]"):
        tag.attributes["_class"] = "color"
    return dict(form = session.form)

def set_default_layout_colors(evt, args=[], vars={}):

    if config.auth.user is not None:
        user_email = config.auth.user.email
        fg_option = db(db.option.name == "user_%s_layout_fgcolor" % user_email).select().first()
        bg_option = db(db.option.name == "user_%s_layout_bgcolor" % user_email).select().first()
        lnk_option = db(db.option.name == "user_%s_layout_lnkcolor" % user_email).select().first()

        if fg_option is None:
            fg_option_id = db.option.insert(name="user_%s_layout_fgcolor" % user_email, value=config.session.layout_colors_foreground)
        else:
            fg_option.update_record(value=config.session.layout_colors_foreground)

        if bg_option is None:
            db.option.insert(name="user_%s_layout_bgcolor" % user_email, value=config.session.layout_colors_background)
        else:
            bg_option.update_record(value=config.session.layout_colors_background)
            
        if lnk_option is None:
            db.option.insert(name="user_%s_layout_lnkcolor" % user_email, value=config.session.layout_colors_links)
        else:
            lnk_option.update_record(value=config.session.layout_colors_links)

        db.commit()

    return dict(_redirect=config._urls[config._this_url])


def user(evt, args=[], vars={"_next": None}):
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """

    vars["_next"] = vars.get("_next", None)
    if vars["_next"] is not None:
        config._auth_next = vars["_next"]

    if len(args) > 0:
        if args[0] == "not_authorized":
            return dict(message = T("Access denied"), form = None)

    # Default redirection:
    default_url = URL(a=config.APP_NAME, c="default", f="index")

    current = config.current

    if evt is None:
        request.args = args
        request.vars = vars

        if args[0] == "login":
            session.form = SQLFORM.factory(
                Field("email", requires=IS_EMAIL()),
                Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
                )

        elif args[0] == "logout":
            # erease the user object
            config.auth.user = None

            # erease customization
            config.session.layout_colors_background \
            = config.session.layout_colors_foreground \
            = config.session.layout_colors_links = None

            # config.auth = None
            return dict(_redirect=default_url)

        elif args[0] == "register":
            session.form = SQLFORM.factory(Field("first_name", requires=IS_NOT_EMPTY()),
            Field("last_name", requires=IS_NOT_EMPTY()),
            Field("email", requires=IS_EMAIL()),
            Field("password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
            Field("retype_password", "password", requires = gluon.validators.CRYPT(key=config.HMAC_KEY)),
            )
            
        else: pass

        config.html_frame.window.Bind(EVT_FORM_SUBMIT, user)

    else:
        if request.args[0] == "login":
            if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
                the_user = db(db.auth_user.email == session.form.vars.email).select().first()
                if the_user is not None:
                    user_data = config.auth.login_bare(session.form.vars.email, session.form.vars.password)
                    if user_data != False:
                        print T("Login accepted")
                        
                        if config._auth_next is not None:
                            # reset auth redirection
                            # and redirect
                            next_url = config._auth_next
                            config._auth_next = None
                            config._auth_source = None
                            config.html_frame.window.OnLinkClicked(next_url)

                    else: print T("Authentication failed")
                else: print T("The user entered does not exist")
            else: print T("The form did not validate")

        elif request.args[0] == "register":
            if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
                # password encryption web2py builtin method
                # validate identical passwords
                if session.form.vars.password == session.form.vars.retype_password:
                    new_user_id = db.auth_user.insert(first_name = session.form.vars.first_name, \
                    last_name = session.form.vars.last_name, email = session.form.vars.email, \
                    password = session.form.vars.password)
                else:
                    print T("The passwords do not match")
                    
                db.commit()
                
                new_user = db.auth_user[new_user_id]
                the_user = config.auth.login_bare(new_user.email, new_user.password)
                config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="default", f="index"))

            elif session.form.errors:
                print T("Form errors"), session.form.errors
            else:
                print T("The form did not validate")

        else:
            # return error message
            print T("Not implemented")

    return dict(form = session.form, message = None)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

def emails(evt, args = [], vars = {}):
    if imapdb is not None:
        messages = imapdb(imapdb.INBOX).select(imapdb.INBOX.id, imapdb.INBOX.created, imapdb.INBOX.sender, imapdb.INBOX.subject, limitby=(0,5))
        messages = SQLTABLE(messages, linkto=URL(a=config.APP_NAME, c="default", f="message"))
    else:
        messages = None
    return dict(messages = messages)

def message(evt, args = [], vars = {}):
    if imapdb is not None:
        message = imapdb(imapdb.INBOX.id == args[1]).select().first()
    else:
        message = None
    return dict(message = message)

def new_function(evt, args = [], vars = {}):
    return dict(three_size_header = H3("A 3 size header"))

def mylinkto(r):
    print "r", type(r), r