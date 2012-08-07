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
import datetime

def accounting_period(db, year = None):
    # get or create an accounting period
    if year is None:
        # get the system clock year by default
        year = datetime.date.today().year

    pedestal = datetime.date(year, 1, 1)
    threshold = datetime.date(year+1, 1, 1)
    accounting_period_id = None
    the_period = db(db.accounting_period.starting >= pedestal\
    ).select().first()
    if the_period is None:
        accounting_period_id = db.accounting_period.insert(\
        starting = pedestal, ending = threshold, \
        description = str(year))
        db.commit()
    else:
        accounting_period_id = the_period.accounting_period_id
    return accounting_period_id


def journal_entry(db, period_id = None, date = None):
    # get or create a journal_entry
    if period_id is None:
        # create an accounting period
        period_id = accounting_period(db, datetime.date.today().year)
        
    if date is None:
        date = datetime.date.today()

    pedestal = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
    delta = datetime.timedelta(1)
    threshold = pedestal + delta

    # fetch the last journal entry or create it
    journal_entry = db((db.journal_entry.accounting_period_id == period_id) & \
    (db.journal_entry.posted >= pedestal) & (db.journal_entry.posted \
    < threshold)).select().first()
    
    if journal_entry is None:
        journal_entry_id = db.journal_entry.insert(accounting_period_id = period_id, \
        description = str(datetime.date.today()))
        db.commit()
        
    else:
        journal_entry_id = journal_entry.journal_entry_id
        
    return journal_entry_id
