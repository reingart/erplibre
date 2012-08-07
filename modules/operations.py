#!/usr/bin/env python
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

# THIS FILE IS DUPLICATED
# (gui2py and web2py apps)
# REMEMBER TO COPY CHANGES
# TO BOTH FILES TO KEEP THE
# DATABASE AND FUNCTIONS
# DEFINITIONS

from gluon import *
import datetime

import accounting

# operation processing

# process operation (for accounting)
def process(db, session, operation_id):
    # TODO: validate operation
    # with movements inspection and
    # user / customer parameters

    # invert entry values (1 or -1)
    invert = 1


    # receipt options
    """
    receipt_purchases_offset_concept_id = db(option.name == "purchases_receipt_offset_concept_id").select().first().value
    receipt_sales_offset_concept_id = db(option.name == "sales_receipt_offset_concept_id").select().first().value
    """

    # error list for web client feedback
    session.process_errors = []

    # process operation and movements
    # return True if successful

    # get the operation record
    operation = db.operation[operation_id]

    # the document must be countable
    document = operation.document_id
    if not document.countable:
        return False

    # Get the document inversion property
    if document.invert == True: invert = -1

    # check if already processed
    if operation.processed:
        return False

    # get the last journal entry
    # or create one
    # TODO: precise j.e. selection/creation
    journal_entry = db.journal_entry[accounting.journal_entry(db)]
    # check if journal entry is valid
    # TODO: Do standard entry validation
    # according to local regulations
    # and return error code/messages
    today = datetime.date.today()
    if (journal_entry is None) or (not ((\
    journal_entry.posted.year == today.year) and \
    (journal_entry.posted.month == today.month) and \
    (journal_entry.posted.day == today.day))):
        # journal_entry_id = db.journal_entry.insert(\
        # accounting_period_id = db(\
        # db.accounting_period).select().last(), \
        # description="%s entry" % str(today))
        # journal_entry = db.journal_entry[journal_entry_id]
        journal_entry_id = accounting.journal_entry(db, year = datetime.date.today().year)

    else:
        journal_entry_id = journal_entry.journal_entry_id

    # movements loop (process entries)
    entries = 0

    for mov in db(db.movement.operation_id == operation_id\
    ).select():
        # check if entry or exit and change the records amount with correct sign
        concept = db(db.concept.concept_id == mov.concept_id).select().first()

        """
        # Change the concept_id if the movement is a receipt
        # and concept is not payment/current account
        # TODO: move receipt based changes to the operations controller

        if document.receipts and not (concept.current_account or concept.payment_method):
            if operation.type == "S":
                concept_id = receipt_sales_offset_concept_id
            elif operation.type == "P":
                concept_id = receipt_purchases_offset_concept_id
            else:
                # TODO: this case is an error
                # operation.type must be S or P
                concept_id = None

            # change movement concept
            concept = db.concept[int(concept_id)]
        """

        amount = None
        if concept.entry == True:
            amount = mov.amount*invert
        elif concept.exit == True:
            amount = -(mov.amount)*invert
        # insert entry record
        entry_id = db.entry.insert(journal_entry_id = journal_entry_id, \
        account_id = concept.account_id, amount = amount)
        entries += 1

    # if all records were successfuly added
    # TODO: (and operation validates)
    if entries > 0:
        # check operation as processed
        # and exit
        operation.update_record(processed = True)
        return True

    # end of process
    # no process made
    return False

