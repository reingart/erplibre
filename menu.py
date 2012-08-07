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

def configure_layout_menu(MENU, URL, T=lambda t: t):
    # HTMLWindow Default Layout menu
    config.menu = MENU([
        (T('Index'), False, URL(config.APP_NAME,'default','index'), []),
        (T('Setup'), False, URL(config.APP_NAME,'setup','index'), []),
        ])

def configure_main_menu(URL):
    config.MAIN_MENU = {
                "__rbac": { "requires": [] }, # "basic"
                "file": {
                    "position": 0, "label": "&File",
                    "visible": True, "enabled": True,
                    "action": None,
                    "submenu":{
                        "crud": {
                            "position": 0, "label": "File &CRUD\tCtrl+D",
                            "visible": True, "enabled": True,
                            "action": URL(a=config.APP_NAME, c="appadmin", f="index"),
                            "submenu":{}
                            }, # crud
                        "forms": {
                            "position": 1, "label": "Forms",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "design": {
                                    "position": 0, "label": "Design",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # design

                                "label": {
                                    "position": 1, "label": "Label",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # label
                                "various": {
                                    "position": 2, "label": "Various",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                } # various
                                }, # forms submenu
                            "separator": True
                            }, # forms
                        "update": {
                            "position": 2, "label": "Update",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "price_list": {
                                    "position": 0, "label": "Price list",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "by_article": {
                                            "position": -1, "label": "By article",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="appadmin", f="select", args=["price", ]),
                                            "submenu":{}
                                        } # by_article
                                    } # price_list submenu
                                }, # price_list
                                "articles": {
                                    "position": 1, "label": "Articles",
                                    "visible": True, "enabled": True,
                                    "action": None,
                                    "submenu":{
                                        "browse": {
                                            "position": -1, "label": "Browse",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="operations", f="articles"),
                                            "submenu":{}
                                        }, # browse
                                        "import": {
                                            "position": 0, "label": "Import",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # import
                                        "prices": {
                                            "position": 1, "label": "Prices",
                                            "visible": True, "enabled": True,
                                            "action": URL(a=config.APP_NAME, c="appadmin", f="select", args=["price",]),
                                            "submenu":{}
                                        }, # prices
                                    } # articles submenu
                                }, # articles
                                "sales": {
                                    "position": 2, "label": "Sales",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "auto_apply": {
                                            "position": 0, "label": "Auto apply",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # auto_apply

                                        "verify": {
                                            "position": 1, "label": "Verify",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # verify

                                        "process_jurisdictions": {
                                            "position": 2, "label": "Process jurisdictions",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # process jurisdictions

                                        "discount_by_customer": {
                                            "position": 3, "label": "Discount by customer",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # discount by customer
                                    } # sales submenu
                                }, # sales
                                "purchases": {
                                    "position": 3, "label": "Purchases",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "process_jurisdictions": {
                                            "position": -1, "label": "Process jurisdictions",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # process jurisdictions
                                    } # purchases submenu
                                }, # purchases
                                "closing": {
                                    "position": 4, "label": "Closing",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{} # closing submenu
                                }, # closing
                            }, # update submenu
                        }, # update
                        "transfers": {
                            "position": 3, "label": "Transfers",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "branches": {
                                    "position": 0, "label": "Branches",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{}
                                }, # branches

                                "replica": {
                                    "position": 1, "label": "Replica",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "generate": {
                                            "position": 0, "label": "Generate",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # generate
                                        "send": {
                                            "position": 1, "label": "Send",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # send
                                        "receive": {
                                            "position": 2, "label": "Receive",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # receive
                                        "process": {
                                            "position": 3, "label": "Process",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{}
                                        }, # process
                                    } # replica submenu
                                }, # replica
                                }, # transfers submenu
                            "separator": True
                            }, # transfers
                        "print": {
                            "position": 4, "label": "Print...",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{}
                            }, # print
                        "page_setup": {
                            "position": 5, "label": "Page setup",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            "separator": True
                            }, # page_setup
                        "options": {
                            "position": 6, "label": "Options",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "formats": {
                                    "position": 0, "label": "&Options\tCtrl+O",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c="setup", f="index"),
                                    "submenu":{},
                                    }, # formats
                                "reset": {
                                    "position": 1, "label": "Reset",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # reset
                                "branch": {
                                    "position": 2, "label": "Branch",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # branch
                                "map": {
                                    "position": 3, "label": "Map",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # map
                                "reset_password": {
                                    "position": 4, "label": "Password reset",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # reset_password
                                }, # options submenu
                            }, # options
                        "parameters": {
                            "position": 7, "label": "Parameters",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "fiscal_controller": {
                                    "position": -1, "label": "fiscal controller",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        "model": {
                                            "position": -1, "label": "Model",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{},
                                            }, # model
                                        "per_item_printing": {
                                            "position": -1, "label": "Per item printing",
                                            "visible": True, "enabled": False,
                                            "action": None,
                                            "submenu":{},
                                            }, # per_item_printing
                                        }, # fiscal_controller submenu
                                    },  # fiscal_controller
                                "credit_card": {
                                    "position": -1, "label": "Credit card",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # credit_card
                                "facilitate_collection": {
                                    "position": -1, "label": "Facilitate collection",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # facilitate_collection
                                "default_salesperson": {
                                    "position": -1, "label": "Default salesperson",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # default_salesperson
                                "vat_subjournal": {
                                    "position": -1, "label": "VAT sub-journal",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # vat_subjournal
                                "predefine_documents": {
                                    "position": -1, "label": "Predefine documents",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # predefine_documents
                                "deactivate_access_levels": {
                                    "position": -1, "label": "Deactivate access levels",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # deactivate_access_levels
                                "advanced": {
                                    "position": -1, "label": "Advanced",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # advanced
                                }, # parameters submenu
                            "separator": True
                            }, # parameters

                        "db_update": {
                            "position": 8, "label": "Database",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{
                                "change_location": {
                                    "position": -1, "label": "Change location",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # change_location
                                "backup": {
                                    "position": -1, "label": "Backup",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # backup
                                "repair": {
                                    "position": -1, "label": "repair",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # repair
                                "compress": {
                                    "position": -1, "label": "compress",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    }, # compress
                                }, # db_update submenu
                            "separator": True
                            }, # db_update
                        "change_user": {
                            "position": 9, "label": "&Change user\tCtrl+U",
                            "visible": True, "enabled": True,
                            "action": URL(a=config.APP_NAME, c="default", f="user", args=["login",]),
                            "submenu":{},
                            }, # change_user
                        "change_password": {
                            "position": 10, "label": "Change password",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            }, # change_password
                        "security_policies": {
                            "position": 11, "label": "Security policies",
                            "visible": True, "enabled": False,
                            "action": None,
                            "submenu":{},
                            "separator": True
                            }, # security_policies
                        "quit": {
                            "position": 12, "label": "&Quit\tCtrl+Q",
                            "visible": True, "enabled": True,
                            "action": "%s/file/quit" % config.APP_NAME,
                            "submenu":{},
                            }, # quit
                        } ,# file submenu
                    } ,# file

                "sales":{
                        "position": 1, "label": "Sales",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "price_check":{
                                    "position": -1, "label": "Price check",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # price_check

                            "create_order":{
                                    "position": -1, "label": "Create order",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='crm',f='customer_panel'),
                                    "submenu":{},
                                }, # create_order

                            "create_down_payment":{
                                    "position": -1, "label": "Create down payment",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # create_down_payment

                            "create_invoice":{
                                    "position": -1, "label": "Create invoice",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c="operations", f="movements_start"),
                                    "submenu":{},
                                    "separator": True
                                }, # create_invoice

                            "order_allocation":{
                                    "position": -1, "label": "Order allocation",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='order_allocation'),
                                    "submenu":{},
                                }, # order_allocation

                            "assign_travel":{
                                    "position": -1, "label": "Assign travel",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # assign travel

                            "invoice_batch":{
                                    "position": -1, "label": "Create invoice batch",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    "separator": True,
                                }, # invoice batch

                            "current_accounts":{
                                    "position": -1, "label": "Current accounts",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='financials',f='current_accounts_type'),
                                    "submenu":{},
                                }, # current accounts

                            "queries":{
                                    "position": -1, "label": "Queries",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='index'),
                                    "submenu":{},
                                }, # queries

                            "summary":{
                                    "position": -1, "label": "Summary",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # sales summary

                            "cancel":{
                                    "position": -1, "label": "Cancel",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    "separator": True,
                                }, # cancel

                            "price_lists":{
                                    "position": -1, "label": "Price lists",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["price_list",]),
                                    "submenu":{},
                                    "separator": True,
                                }, # price_lists

                            }, # sales submenu
                    }, # sales

                "purchases":{
                        "position": 2, "label": "Purchases",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "create_invoice":{
                                    "position": -1, "label": "New invoice",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='movements_start'),
                                    "submenu":{},
                                }, # create_invoice

                            "create_expenses_invoice":{
                                    "position": -1, "label": "New expenses invoice",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    "separator": True,
                                }, # create_expenses_invoice

                            "create_payment":{
                                    "position": -1, "label": "Create payment",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # create_payment

                            "apply_payment":{
                                    "position": -1, "label": "Apply payment",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='financials',f='current_accounts_type'),
                                    "submenu":{},
                                    "separator": True
                                }, # apply_payment

                            "revert_application":{
                                    "position": -1, "label": "Revert payment application",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    "separator": True,
                                }, # revert_application

                            "current_accounts":{
                                    "position": -1, "label": "Current accounts",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                    "separator": True,
                                }, # current_accounts

                            "queries":{
                                    "position": -1, "label": "queries",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='index'),
                                    "submenu":{},
                                }, # queries

                            "summary":{
                                    "position": -1, "label": "Summary",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # summary

                            "cancel":{
                                    "position": -1, "label": "Cancel",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{},
                                }, # cancel
                            }, # purchases submenu
                    }, # purchases

                "cash":{
                        "position": 3, "label": "Cash",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{

                            "funds":{
                                    "position": -1, "label": "Funds",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["fund",]),
                                    "submenu":{
                                        }, # funds submenu
                                }, # funds

                            "checks":{
                                    "position": -1, "label": "Checks",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["bank_check",]),
                                    "submenu":{
                                        }, # checks submenu
                                }, # checks

                            "banks":{
                                    "position": -1, "label": "Banks",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["bank",]),
                                    "submenu":{
                                        }, # banks submenu
                                }, # banks
                            }, # cash submenu
                    }, # cash

                "stock":{
                        "position": 4, "label": "Stock",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "activate_deposit":{
                                    "position": -1, "label": "Funds",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        },
                                    "separator": True,
                                }, # activate_deposit
                            "queries":{
                                    "position": -1, "label": "Queries",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='appadmin',f='select', args=["stock",]),
                                    "submenu":{
                                        }, # queries submenu
                                }, # queries

                            "summary":{
                                    "position": -1, "label": "Summary",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # summary submenu
                                }, # summary


                            "articles":{
                                    "position": -1, "label": "Articles",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='scm',f='ria_stock'),
                                    "submenu":{
                                        }, # articles submenu
                                }, # articles


                            "structures":{
                                    "position": -1, "label": "Structures",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # structures submenu
                                }, # structures


                            "formulas":{
                                    "position": -1, "label": "Formulas",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # formulas submenu
                                }, # formulas

                            "production":{
                                    "position": -1, "label": "Production",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # production submenu
                                }, # production
                            }, # stock submenu
                    }, # stock

                "accounting":{
                        "position": 5, "label": "Accounting",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "activate_period":{
                                    "position": -1, "label": "Activate period",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        },
                                }, # activate_period

                            "entries":{
                                    "position": -1, "label": "Entries",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='accounting',f='journal_entries'),
                                    "submenu":{
                                        }, # entries submenu
                                }, # entries

                            "accounts_plan":{
                                    "position": -1, "label": "Accounts plan",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        },
                                }, # accounts_plan

                            "passages":{
                                    "position": -1, "label": "Passages",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # passages submenu
                                }, # passages


                            "processes":{
                                    "position": -1, "label": "Processes",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # processes submenu
                                }, # processes

                            "batch":{
                                    "position": -1, "label": "Batch",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # batch submenu
                                }, # batch
                            }, # accounting submenu
                    }, # accounting


                "reports":{
                        "position": 6, "label": "Reports",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                            "lists":{
                                    "position": -1, "label": "Lists",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # lists submenu
                                }, # lists

                            "labels":{
                                    "position": -1, "label": "Labels",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # labels submenu
                                }, # labels

                            "fiscal_controller":{
                                    "position": -1, "label": "Fiscal controller",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # fiscal_controller submenu
                                }, # fiscal_controller

                            "sales":{
                                    "position": -1, "label": "Sales",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # sales submenu
                                }, # sales

                            "purchases":{
                                    "position": -1, "label": "Purchases",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # purchases submenu
                                }, # purchases

                            "cash":{
                                    "position": -1, "label": "Cash",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # cash submenu
                                }, # cash

                            "securities":{
                                    "position": -1, "label": "Securities",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # securities submenu
                                }, # securities

                            "stock":{
                                    "position": -1, "label": "Stock",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # stock submenu
                                }, # stock

                            "movements":{
                                    "position": -1, "label": "Movements",
                                    "visible": True, "enabled": True,
                                    "action": URL(a=config.APP_NAME, c='operations',f='movements_list'),
                                    "submenu":{
                                        }, # movements submenu
                                }, # movements

                            "accounting":{
                                    "position": -1, "label": "Accounting",
                                    "visible": True, "enabled": False,
                                    "action": None,
                                    "submenu":{
                                        }, # accounting submenu
                                }, # accounting
                            }, # reports submenu
                    }, # reports

                "windows":{
                        "position": 7, "label": "Windows",
                        "visible": True, "enabled": False,
                        "action": None,
                        "submenu":{
                                "treepane":{
                                        "position": -1,
                                        "label": "&Tree pane\tCtrl+T",
                                        "visible": True, "enabled": True,
                                        "handler": "handlers.treepane",
                                        "submenu":{},
                                }, # treepane
                                "workspace":{
                                        "position": -1,
                                        "label": "&Work space\tCtrl+W",
                                        "visible": True, "enabled": True,
                                        "handler": "handlers.workspace",
                                        "submenu":{},
                                }, # workspace
                                "switchpane":{
                                        "position": -1,
                                        "label": "&Switch pane\tCtrl+.",
                                        "visible": True, "enabled": True,
                                        "handler": "handlers.switch_pane",
                                        "submenu":{},
                                }, # workspace
                                "switchpanebkwd":{
                                        "position": -1,
                                        "label": "&Switch pane backwards\tCtrl+,",
                                        "visible": True, "enabled": True,
                                        "handler": "handlers.switch_pane_backwards",
                                        "submenu":{},
                                }, # workspace
                            }, # windows submenu
                }, # windows

                "help":{
                        "position": 8, "label": "Help",
                        "visible": True, "enabled": True,
                        "action": None,
                        "submenu":{
                                "wiki":{
                                        "position": -1, "label": "Wiki",
                                        "visible": True, "enabled": True,
                                        "action": "http://code.google.com/p/erplibre/w/list",
                                        "submenu":{},
                                }, # about
                                "about":{
                                        "position": -1, "label": "About",
                                        "visible": True, "enabled": True,
                                        "action": "http://code.google.com/p/erplibre/",
                                        "submenu":{},
                                }, # about
                            }, # help submenu
                }, # help
        } # MAIN_MENU

