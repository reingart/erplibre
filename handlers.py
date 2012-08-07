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
import gui
URL = gui.URL

# Example event handler ( Set config.MAIN_MENU
# dictionary item with "handler": "handlers.MyHandler")
def MyHandler(evt):
    print "event handler MyHandler called with event", evt.Id
    return None


def billing_button_click(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='ria_product_billing_start'))

def current_accounts_button_click(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='crm',f='current_account_report'))

def customers_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="select", args=["customer",]))

def articles_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="operations", f="articles"))

def queries_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="appadmin", f="index"))

def movements_button_click(evt):
    # gui.test_or_create_html_frame()    
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='operations',f='index'))

def user_login(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["login",], vars={"_next": URL(a=config.APP_NAME, c="default", f="index")}))

def user_logout(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["logout",]))

def user_register(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='user', args=["register",], vars={"_next": URL(a=config.APP_NAME, c="default", f="index")}))

def user_specify_tin(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='registration',f='post_register_specify_firm'))

def user_index(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='default',f='index'))

def user_setup(evt):
    # gui.test_or_create_html_frame()
    config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c='setup',f='index'))

def treepane(evt):
    config.html_frame.tree_pane.SetFocus()

def workspace(evt):
    config.html_frame.tree_pane.SetFocus()
    config.html_frame.window.SetFocus()

def switch_pane(evt):
    panes = (config.html_frame.window, config.html_frame.tree_pane, config.html_frame.text_pane)
    search_loop = True
    first = 0
    for i, pane in enumerate(panes):
        focused = config.html_frame.FindFocus()
        if focused is not None:
            search_loop = True
            while search_loop:
                if focused is pane:
                    # focused pane
                    try:
                        panes[i+1].SetFocus()
                    except IndexError:
                        panes[first].SetFocus()
                    finally:
                        return
                elif focused is None:
                    search_loop = False
                else:
                    focused = focused.GetParent()
        else:
            panes[0].SetFocus()
            return

def switch_pane_backwards(evt):
    panes = (config.html_frame.window, config.html_frame.tree_pane, config.html_frame.text_pane)
    search_loop = True
    last = len(panes) -1
    for i, pane in enumerate(panes):
        focused = config.html_frame.FindFocus()
        if focused is not None:
            search_loop = True
            while search_loop:
                if focused is pane:
                    # focused pane
                    try:
                        panes[i-1].SetFocus()
                    except IndexError:
                        panes[last].SetFocus()
                    finally:
                        return
                elif focused is None:
                    search_loop = False
                else:
                    focused = focused.GetParent()
        else:
            panes[0].SetFocus()
            return
