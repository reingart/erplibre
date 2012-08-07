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

from gui2py.form import EVT_FORM_SUBMIT

def index(): return dict(message="hello from registration.py")

def post_register_specify_firm(evt, args=[], vars={}):
    session.form = FORM(INPUT(_name="firm_tax_id"), INPUT(_type="submit"))
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            contact = db(db.contact.tax_identification == session.form.vars.firm_tax_id).select().first()
            if contact and config.auth.user_id:
                if db((db.contact_user.contact_id == contact.contact_id) & (db.contact_user.user_id == config.auth.user_id)).count() <= 0:
                    db.contact_user.insert(user_id=config.auth.user_id, \
                    contact_id=contact, description=db.auth_user[config.auth.user_id].email)
                    db.commit()
                    print T("Firm specification successful")
                    return dict(_redirect=URL(a=config.APP_NAME, c="default", f="index"))
                else:
                    print T("Contact exists or the user has a contact already")
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, post_register_specify_firm)
        
    return dict(form=session.form)
