#! /usr/env python
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


def current_account_value(db, operations):
    """ Calculates the current account value
    for the customer specified

    arguments:
    db: DAL object
    operations: rows object with all
    customer/subcustomer operations
    """

    value = 0.0
    for operation in operations:
        invert_value = 1
        if operation.document_id.invert == True:
            invert_value = -1
        movements = db(db.movement.operation_id == \
        operation.operation_id).select()
        
        for movement in movements:
            try:
                # Filter current_account movements
                if movement.concept_id.current_account != True:
                    if movement.concept_id.entry == True:
                        value += \
                        invert_value*float(movement.amount)
                    elif movement.concept_id.exit == True:
                        value += \
                        invert_value*float(movement.amount)*(-1)
                        
            except (ValueError, TypeError, AttributeError, RuntimeError), e:
                print \
                "Current account value: error calculating movement id %s: %s" \
                % (movement.movement_id, str(e))

    return value

def customer_current_account_value(db, customer_id):
    operations = db(db.operation.customer_id == customer_id).select()
    value = current_account_value(db, operations)
    return value

def subcustomer_current_account_value(db, subcustomer_id):
    operations = db(db.operation.subcustomer_id == subcustomer_id).select()
    value = current_account_value(db, operations)    
    return value

