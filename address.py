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

import config

# for rbac access control
# All the conditions for any object
# should be tested from the root to
# the object level

config.address = {
    "__rbac": { "requires": ["basic",] }, # special key for access control
    "appadmin": {
        "__rbac": { "requires": [] },
        "index": {"action": "controllers.appadmin.index",},
        "select": {"action": "controllers.appadmin.select"},
        "read": {"action": "controllers.appadmin.read"},
        "update": {"action": "controllers.appadmin.update"},
        "create": {"action": "controllers.appadmin.create"},
        },
    "setup":{
        "__rbac": { "requires": [], "override": True },
        "index": {"action": "controllers.setup.index"},
        "options": {
            "action": "controllers.setup.options",
            "__rbac": { "requires": ["basic",]},
            },
        "option": {"action": "controllers.setup.option"},
        "set_language": {
            "action": "controllers.setup.set_language",
            "__rbac": { "requires": ["basic",]},
            },
        "configure": {"action": "controllers.setup.configure"}
        },
    "migration":{
        "import_csv_dir": {
            "action": "controllers.migration.import_csv_dir",
            "__rbac": { "requires": ["basic",]},
            },
        "csv_to_db": {
            "action": "controllers.migration.csv_to_db",
            "__rbac": { "requires": ["basic",]},
            },
        "db_to_csv": {
            "action": "controllers.migration.db_to_csv",
            "__rbac": { "requires": ["basic",]},
            },
        },
    "file":{
        "quit": {
            "action": "controllers.file.quit",
            "__rbac": { "requires": [], "override": True },
            },
        },
    "output":{
        "operation": {"action": "controllers.output.operation"},
        },
    "default":{
        "__rbac": { "requires": [], "override": True },
        "index": {"action": "controllers.default.index"},
        "new_function": {"action": "controllers.default.new_function"},
        "user": {"action": "controllers.default.user", "__rbac":{"override": True}},
        "change_layout_colors": {"action": "controllers.default.change_layout_colors", "__rbac": { "requires": [] }},
        "set_default_layout_colors": {"action": "controllers.default.set_default_layout_colors"},
        "emails": {"action": "controllers.default.emails"},
        "message": {"action": "controllers.default.message"}
        },
    "scm":{
        "ria_stock": {"action": "controllers.scm.ria_stock"},
        "change_stock": {"action": "controllers.scm.change_stock"},
        "stock_movement": {"action": "controllers.scm.stock_movement"},
        "stock_item_update": {"action": "controllers.scm.stock_item_update"},
        },
    "accounting":{
        "journal_entries": {"action": "controllers.accounting.journal_entries"},
        "journal_entry": {"action": "controllers.accounting.journal_entry"},
        "entry": {"action": "controllers.accounting.entry"},
        },
    "operations":{
        "articles": {"action": "controllers.operations.articles"},
        "articles_list": {"action": "controllers.operations.articles_list"},
        "ria_product_billing_start": {"action": "controllers.operations.ria_product_billing_start"},
        "ria_product_billing": {"action": "controllers.operations.ria_product_billing"},
        "reset_packing_slip": {"action": "controllers.operations.reset_packing_slip"},
        "reset_packing_slip": {"action": "controllers.operations.reset_packing_slip"},
        "packing_slip": {"action": "controllers.operations.packing_slip"},
        "update_order_allocation": {"action": "controllers.operations.update_order_allocation"},
        "list_order_allocations": {"action": "controllers.operations.list_order_allocations"},
        "order_allocation": {"action": "controllers.operations.order_allocation"},
        "operation_installment": {"action": "controllers.operations.operation_installment"},
        "index": {"action": "controllers.operations.index"},
        "ria_movements": {"action": "controllers.operations.ria_movements"},
        "ria_movements_reset": {"action": "controllers.operations.ria_movements_reset"},
        "ria_movements_process": {"action": "controllers.operations.ria_movements_process"},
        "movements_element": {"action": "controllers.operations.movements_element"},
        "movements_modify_element": {"action": "controllers.operations.movements_modify_element"},
        "movements_modify_check": {"action": "controllers.operations.movements_modify_check"},
        "ria_new_customer_order_reset": {"action": "controllers.operations.ria_new_customer_order_reset"},
        "ria_new_customer_order": {"action": "controllers.operations.ria_new_customer_order"},
        "new_customer_order_element": {"action": "controllers.operations.new_customer_order_element"},
        "new_customer_order_modify_element": {"action": "controllers.operations.new_customer_order_modify_element"},
        "movements_list": {"action": "controllers.operations.movements_list"},
        "movements_select": {"action": "controllers.operations.movements_select"},
        "movements_detail": {"action": "controllers.operations.movements_detail"},
        "movements_start": {"action": "controllers.operations.movements_start"},
        "movements_header": {"action": "controllers.operations.movements_header"},
        "movements_price_list": {"action": "controllers.operations.movements_price_list"},
        "movements_add_item": {"action": "controllers.operations.movements_add_item"},
        "movements_add_payment_method": {"action": "controllers.operations.movements_add_payment_method"},
        "movements_articles": {"action": "controllers.operations.movements_articles"},
        "movements_add_check": {"action": "controllers.operations.movements_add_check"},
        "movements_add_tax": {"action": "controllers.operations.movements_add_tax"},
        "movements_current_account_concept": {"action": "controllers.operations.movements_current_account_concept"},
        "movements_current_account_quotas": {"action": "controllers.operations.movements_current_account_quotas"},
        "movements_current_account_data": {"action": "controllers.operations.movements_current_account_data"},
        "movements_add_discount_surcharge": {"action": "controllers.operations.movements_add_discount_surcharge"},
        "movements_process": {"action": "controllers.operations.movements_process"},
        "movements_option_update_stock": {"action": "controllers.operations.movements_option_update_stock"},
        "movements_option_update_taxes": {"action": "controllers.operations.movements_option_update_taxes"},
        "movements_select_warehouse": {"action": "controllers.operations.movements_select_warehouse"},
        "movements_modify_item": {"action": "controllers.operations.movements_modify_item"},
        "movements_modify_header": {"action": "controllers.operations.movements_modify_header"},
        },
    "registration":
        {
        "post_register_specify_firm": {"action": "controllers.registration.post_register_specify_firm"},
            },
    "crm":
        {
            "customer_current_account_status": {"action": "controllers.crm.customer_current_account_status"},
            "customer_panel": {"action": "controllers.crm.customer_panel"},
            "current_account_report": {"action": "controllers.crm.current_account_report"},
            },
    "financials":
        {
            "current_accounts_type": {"action": "controllers.financials.current_accounts_type"},
            "current_accounts_data": {"action": "controllers.financials.current_accounts_data"},
            "current_accounts_detail": {"action": "controllers.financials.current_accounts_detail"},
            "current_accounts_payment": {"action": "controllers.financials.current_accounts_payment"},
            },
    "fees":
        {
            "list_installments": {"action": "controllers.fees.list_installments"},
            "update_installment": {"action": "controllers.fees.update_installment"},
            "update_quota": {"action": "controllers.fees.update_quota"},
            "update_fee": {"action": "controllers.fees.update_fee"},
            "list_fees": {"action": "controllers.fees.list_fees"},
            "create_fee": {"action": "controllers.fees.create_fee"},
            },
}

