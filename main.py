#!/usr/bin/python
# -*- coding: utf-8 -*-

# Main module of wxPython desktop app for GestionLibre.

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

HELP_TEXT = """
    ERP Libre main module command options:

    ./main.py [option 1 [value 1]] ... [option n]

    * --help : Display this text
    * --?: same as help
    * --legacy_db: Do not write db local files (this prevents database errors
    when using a pre-configured database)
    * --user [email:password]: Login with specified credentials on startup
"""

LOGIN_STRING = None

# constants and common memmory storage

import sys
import os
import datetime
import threading
import time

# Make the file folder the cwd
os.chdir(sys.path[0])

# import wxPython:
import wx
import wx.html
# fix windows weird characters in menus
wx.SetDefaultPyEncoding("utf-8")

# wx auto if __name ... code
def action(url):
    gui.action(url)


def configure_event_handlers():
    config.event_handlers = {
        "__rbac": {"requires": [],},
        "handlers":{
            }
        }


def handle_event(evt, event_handler):
    """ searches handler options in a dictionary tree
    for rbac
    and redirects to the event handler function
    """
    route = (None, event_handler.__module__, event_handler.func_name)
    requires_list = set()
    handlers_item = config.event_handlers

    for level in route:
        if level is not None:
            try:
                handlers_item = handlers_item[level]
            except KeyError:
                break

        if "__rbac" in handlers_item.keys():
            if "override" in handlers_item["__rbac"].keys():
                if handlers_item["__rbac"]["override"]:
                    requires_list = set()
            for rb in handlers_item["__rbac"].get("requires", []):
                requires_list.add(rb)

    result = config.access_control(requires_list)
    if result[0]:
        event_handler(evt)
    else:
        print result[1]

    return


# Go to HTML Window action after tree pane item double click
def tree_pane_event(evt):
    the_data = config.html_frame.tree_pane.GetItemData( \
    evt.GetItem()).GetData()

    if type(the_data) == dict:
        if "action" in the_data:
            config.html_frame.window.OnLinkClicked( \
            the_data["action"])
    return None


def menu_event(evt):

    # check if html_frame was closed (throws wx._core.PyDeadObjectError)
    # print "starting_frame.menu_events:"
    # print config.html_frame.menu_events

    # frame menu events: [ (event object, route tuple), ...]
    
    the_event = config.html_frame.menu_events[evt.Id][0]
    # check if string and is url-like
    # TODO: complete url check (web2py validators)

    requires_list = set()

    # check access lists with gui.RBAC class

    # search general menu rbac rules
    menu_item = config.MAIN_MENU
    if "__rbac" in menu_item.keys():
        if "override" in menu_item["__rbac"].keys():
            if menu_item["__rbac"]["override"]:
                requires_list = set()
        for rb in menu_item["__rbac"]["requires"]:
            requires_list.add(rb)
            
    # search trough menu tree

    for k in config.html_frame.menu_events[evt.Id][1]:
        try:
            menu_item = menu_item["submenu"][k]
        except:
            menu_item = menu_item[k]
            
        if "__rbac" in menu_item.keys():
            if "override" in menu_item["__rbac"].keys():
                if menu_item["__rbac"]["override"]:
                    requires_list = set()
            for rb in menu_item["__rbac"].get("requires", []):
                requires_list.add(rb)

    result = config.access_control(requires_list)
    if result[0]:
        if isinstance(the_event, basestring):
            try:
                is_active = config.html_frame.IsActive()
            except wx._core.PyDeadObjectError:
                # html window closed
                # reinitialize it
                print str(e)
                # gui.start_html_frame(config.html_frame, the_event)

            config.html_frame.window.OnLinkClicked(the_event)

        elif callable(the_event):
            the_event(evt)
    else:
        print result[1]
            
    return None


def main_menu_elements(frame,
                       parent_menu,
                       item_count = 0,
                       submenu=None,
                       is_menu_bar=False,
                       route=[],
                       T = lambda t: t):
    import handlers
    menu_item = None

    try:
        menu_items = getattr(parent_menu, "menu_items")
    except AttributeError:
        parent_menu.menu_items = dict()
        menu_items = parent_menu.menu_items

    ordered_items = [(v.get("position", None), k, v) for \
                      k,v in submenu.iteritems()]
    ordered_items.sort()

    # loop replaced by list iteration
    # it follows menu item index position order
    # route is the tree walk tuple (for hierarchical access lists)
    
    for item in ordered_items:

        tmp_route = None
        k = item[1]
        v = item[2]
        pos = item[0]
        item_count += 1

        try:
            menu_items = getattr(parent_menu, "menu_items")
        except:
            parent_menu.menu_items = dict()

        text_label = str(T(v.get("label", "")))

        if v.get("visible", False):
            if is_menu_bar == True:
                parent_menu.menu_items[k] = wx.Menu()
                parent_menu.Append(parent_menu.menu_items[k], \
                text_label)
                route = [k,]
                tmp_route = tuple(route)

                if v.has_key("submenu"):
                    if len(v["submenu"]) > 0:
                         item_count = main_menu_elements(frame, \
                         parent_menu.menu_items[k], \
                         submenu=v["submenu"], \
                         item_count=item_count, \
                         route=route, T=T)
                route.pop()

                if k.lower() == "file":
                    # AUI options (defined at aui.py)
                    config.html_frame.starting_menubar.Append(\
                    config.html_frame._perspectives_menu, T("Perspectives"))
                    config.html_frame.starting_menubar.Append(\
                    config.html_frame.options_menu, T("Options"))

            else:
                if v.has_key("submenu"):
                    if len(v["submenu"]) > 0:
                        route.append(k)
                        tmp_route = tuple(route)
                        parent_menu.menu_items[k] = wx.Menu()
                        parent_menu.AppendMenu(item_count, \
                        text_label, parent_menu.menu_items[k])
                        item_count=main_menu_elements(frame, \
                        parent_menu.menu_items[k], \
                        submenu=v["submenu"], \
                        item_count=item_count, route=route, T=T)
                        route.pop()

                    else:
                        route.append(k)
                        parent_menu.menu_items[k] = v
                        menu_item = parent_menu.Append(item_count, \
                        text_label)
                        tmp_route = tuple(route)
                        
                        # enable/disable
                        parent_menu.Enable(item_count, \
                        v.get("enabled", True))
                        route.pop()

                else:
                    route.append(k)
                    parent_menu.menu_items[k] = v
                    menu_item = parent_menu.Append(item_count, \
                    text_label)
                    tmp_route = tuple(route)

                    # enable/disable
                    parent_menu.Enable(item_count, \
                    v.get("enabled", True))
                    route.pop(k)

                if v.get("separator", False):
                    parent_menu.AppendSeparator()

            if v.has_key("action"):
                if menu_item is not None:
                    if v["action"] is not None:
                        frame.Bind(wx.EVT_MENU, menu_event, menu_item)
                        frame.menu_events[menu_item.Id] = ( \
                        v["action"], tmp_route)

            elif v.has_key("handler"):
                if menu_item is not None:
                    if v["handler"] is not None:
                        handler_list = v["handler"].split(".")
                        the_obj = locals()[handler_list[0]]
                        for x in range(len(handler_list)):
                            if x > 0:
                                the_obj = getattr(the_obj, \
                                handler_list[x])

                        frame.Bind(wx.EVT_MENU, menu_event, menu_item)
                        frame.menu_events[menu_item.Id] = ( \
                        the_obj, tmp_route)

    return item_count


def configure_tree_pane(frame, T=lambda t: t):
    from gluon.html import URL
    tree = frame.tree_pane
    root = tree.AddRoot(str(T("Actions")))
    items = []

    imglist = wx.ImageList(16, 16, True, 2)
    
    folder_icon_id = imglist.Add(\
    wx.ArtProvider_GetBitmap(wx.ART_FOLDER,
                             wx.ART_OTHER,
                             wx.Size(16,16)))
    default_icon_id = imglist.Add(\
    wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE,
                             wx.ART_OTHER,
                             wx.Size(16,16)))
    
    tree.AssignImageList(imglist)

    item_counter = 0
    for k, v in config.address.iteritems():
        if not k.startswith("_"):
            icon_id = folder_icon_id
            if "__icon" in v:
                icon_id = imglist.Add(wx.Bitmap(v["__icon"]))

            the_item = tree.AppendItem(root, str(T(k)), icon_id)

            for j, w in v.iteritems():
                if not j.startswith("_"):
                    icon_id = default_icon_id
                    if "__icon" in w:
                        icon_id = imglist.Add(wx.Bitmap(w["__icon"]))

                    sub_item = tree.AppendItem(the_item,
                                               str(T(j.replace("_",\
                                               " ").capitalize())),
                                               icon_id)

                    tree.GetItemData(sub_item).SetData(\
                    {"action": URL(a=config.APP_NAME, c=k, f=j)})
                    frame.Bind(wx.EVT_TREE_ITEM_ACTIVATED,
                               tree_pane_event, tree)

            item_counter += 1
    tree.Expand(root)

    return None


def on_db_timeout(evt):
    # reset db object to prevent server connection closing
    if "postgres" in config.DB_URI.lower():
        if config.VERBOSE:
            print "Database timeout triggered", datetime.datetime.now()
            print "Database connection", "status", \
            db["_adapter"].connection.status, "closed", \
            db["_adapter"].connection.closed
            print "Reset connection..."

        # reset the connection to avoid timeout issues
        db["_adapter"].connection.reset()

    else:
        stopped = evt.GetEventObject().Stop()
        if config.VERBOSE:
            print "Db timeout option not supported for this database"
            print "Event stopped"

    return


def config_setup():
    # print "Configuring config"
    global LOGIN_STRING
    arg_counter = 0
    for arg in sys.argv:
        name = arg.upper().replace("-", "")
        arg_counter += 1
        if name == "USER":
            try:
                LOGIN_STRING = sys.argv[arg_counter]
            except IndexError:
                print "User login not specified."

        elif name == "LEGACY_DB":
            config.LEGACY_DB = True

        elif name == "DB_TIMEOUT":
            # reset db connection timeout
            # used for psycopg2 connection closed issue
            config.DB_TIMEOUT = int(sys.argv[arg_counter])

        elif name in ("HELP", "?"):
            print HELP_TEXT
            exit(0)
        elif name == "VERBOSE":
            print "Verbose mode"
            config.VERBOSE = True


class GestionLibreApp(wx.PySimpleApp):
    def OnInit(self):
        return True


if __name__ == "__main__":
    # setup for the app-wide config module

    import config
    config_setup()

    # import gui2py support -wxHTML FORM handling- (change the path!)
    sys.path.append(config.GUI2PY_FOLDER)

    # import web2py (change the path!)
    sys.path.append(config.WEB2PY_FOLDER)

    # app initialization
    app = GestionLibreApp(0)
    wx.InitAllImageHandlers()

    # Attributes
    bmp = wx.Bitmap('images/erplibre-screen.png', wx.BITMAP_TYPE_PNG)
    splash = wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN|\
                             wx.SPLASH_NO_TIMEOUT, -1, None)
    splash.Show()

    # app initialization

    # print "Importing web2py gluon"
    # from gluon import *
    try:
      import gluon
    except ImportError as e:
      print e.message
      print "Have you run the install? To install run ./install.py"
      exit(1)
    from gluon.html import URL
    from gluon.html import MENU
    from gluon.dal import DAL
    import gluon
    import gluon.template
    import gluon.shell
    import gluon.tools

    # frame initialization

    # print "More config setup"

    # load web2py app env object for GestionLibre

    config.env = gluon.shell.env(config.APP_NAME,
                                 dir=config.GUI2PY_APP_FOLDER)

    config.current = config.env
    config.request  = config.env["request"]
    config.response  = config.env["response"]
    config.response._vars = gluon.storage.Storage()
    config.session  = config.env["session"]
    config.context = gluon.storage.Storage()

    # set translation options
    # language configuration values are forced
    # because of the non web2py execution environment

    # print "Internationalization"

    T = config.env["T"]
    T.folder = config.GUI2PY_APP_FOLDER
    # Evaluate inmediately
    # to avoid Type exceptions when
    # instantiating wx objects
    T.lazy = False

    # test if language file exists or create it (except for default "en" value)
    if not (config.LANGUAGE in (None, "", "en")):
        language_file_path = os.path.join( \
        config.GUI2PY_APP_FOLDER, \
        "languages", "%s.py" % config.LANGUAGE)

        # config.env["T"].set_current_languages([config.LANGUAGE,])

        T.language_file = language_file_path
        T.accepted_language = config.LANGUAGE
        T.http_accept_language = [config.LANGUAGE,]
        T.requested_languages = [config.LANGUAGE,]

        # force t dictionary load (otherwise translator would overwrite
        # the language file)
        T.t = gluon.languages.read_dict(T.language_file)

    # print "Creating DAL connection"

    # create DAL connection (and create DB if it does not exists)
    config.db = DAL(config.DB_URI, folder=config.DATABASES_FOLDER, pool_size = 10)

    # EXPERIMENTAL (imap connection)
    if config.IMAP_URI:
        config.imapdb = DAL(config.IMAP_URI)
        config.imapdb.define_tables()
    else:
        config.imapdb = None

    # Connection example for PostgreSQL database (set this at installation as DB_URI)
    # or modify the value at [desktopapp]/config.ini and [web2pyapp]/config.ini
    # specify folder path as webapp path + "databases"
    # config.db = DAL("postgres://erplibre:erplibre@localhost:5432/erplibre",
    #                 folder=config.DATABASES_FOLDER)

    db = config.db

    # TODO: Authenticate with wx widgets.
    # A series of hack imports (with shell) and bindings are needed
    # for using auth and crud.

    # print "Creating auth"

    # auth (buggy: has redirection and form submission problems)
    config.auth = gluon.tools.Auth(db=db, hmac_key=config.HMAC_KEY)

    # import all the table definitions and options in web app's model
    # model module

    # custom auth_user definition is required to prevent the "auth_user not
    # found" error
    # import applications.erplibre.modules.db_erplibre as db_erplibre

    # print "Table definitions"

    from modules import db_erplibre, info

    # define the database tables
    # web2py = False forces db.define_table("auth_user"..)

    # define the auth tables (this goes after app tables definition)
    config.auth.settings.hmac_key = config.HMAC_KEY       # before define_tables()

    # activate web2py fake_migrate for client installations
    fake_migrate = False
    if (config.GUI2PY_APP_CLIENT.upper() in ("TRUE", "YES", "1")) \
    or (str(config.LEGACY_DB).upper() in ("TRUE", "YES", "1")):
        fake_migrate = True

    # custom db initialization for ERP Libre
    db_erplibre.define_tables(db,
                                config.auth,
                                config.env,
                                web2py = False,
                                fake_migrate = fake_migrate,
                                T=T)

    # print "Creating crud"

    # crud (buggy: form submission and database transactions problems)
    config.crud = gluon.tools.Crud(config.env, db=db)

    # print "Frame manager setup"

    # print "Application and custom modules"

    # app modules
    import gui
    import handlers

    # import controller modules
    import controllers.default, controllers.operations, controllers.crm, \
    controllers.registration, controllers.fees, \
    controllers.scm, controllers.accounting, controllers.financials, \
    controllers.setup, controllers.file, controllers.migration, \
    controllers.appadmin, controllers.output

    import aui

    # Add the main window
    # print "Creating the app and frame objects"

    config.WX_HTML_STYLE = wx.html.HW_DEFAULT_STYLE | wx.TAB_TRAVERSAL
    config.html_frame = aui.PyAUIFrame(None, -1, u"ERP Libre")
    config.html_frame.SetSize((800, 600))

    # send the frame to the top
    app.SetTopWindow(config.html_frame)

    # AUI Notebook initial configuration
    config.html_frame.start_manager()

    # print "Main window events"

    # Main window button events
    # use lambda event: handle_event(event, function)
    # for rbac
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.billing_button_click), config.html_frame.button_1)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.current_accounts_button_click), config.html_frame.button_2)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.customers_button_click), config.html_frame.button_3)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.articles_button_click), config.html_frame.button_4)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.queries_button_click), config.html_frame.button_5)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.movements_button_click), config.html_frame.button_8)

    # user tab events
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_login), config.html_frame.button_10)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_logout), config.html_frame.button_11)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_register), config.html_frame.button_12)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_specify_tin), config.html_frame.button_13)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_index), config.html_frame.button_14)
    config.html_frame.Bind(wx.EVT_TOOL, lambda event: handle_event(event, \
    handlers.user_setup), config.html_frame.button_15)

    config.html_frame.menu_events = dict()

    # Previous and next button events
    config.html_frame.Bind(wx.EVT_TOOL, gui.OnPreviousClick,
                        config.html_frame.button_6)
    config.html_frame.Bind(wx.EVT_TOOL, gui.OnNextClick,
                        config.html_frame.button_7)
    config.html_frame.Bind(wx.EVT_TOOL, gui.OnHomeClick,
                        config.html_frame.button_9)

    # print "Populate main menu"

    # populate main menu
    import menu
    menu.configure_main_menu(URL)

    # print  "Populate html layout"

    # populate html layout menu
    menu.configure_layout_menu(MENU, URL, T=T)

    main_menu_elements(config.html_frame, config.html_frame.starting_menubar, \
    submenu=config.MAIN_MENU, is_menu_bar=True, T=T)

    config.html_frame.SetMenuBar(config.html_frame.starting_menubar)
    config.html_frame.SetStatusText("")

    # print "Action binding"

    # bind web2py like actions to module functions
    import address

    # print "Configure tree panes"

    # add items to the action tree pane
    configure_tree_pane(config.html_frame, T=T)

    # set the event handler options
    configure_event_handlers()

    gui.load_actions()

    # print "Access control setup"

    config.access_control = gui.RBAC(config.db,
                                    config.auth,
                                    config.request,
                                    config.session,
                                    config.html_frame)

    if isinstance(LOGIN_STRING, basestring) and \
    len(LOGIN_STRING.split(":")) == 2:
        # TODO: move to an authentication function
        # straight login from command line.
        email, password = LOGIN_STRING.split(":")

        if config.access_control.validate_user(email, password):
            print T("Welcome %s") % email
        else:
            print T("Authentication failed")

    elif isinstance(LOGIN_STRING, basestring) and \
    len(LOGIN_STRING.split(":")) != 2:
        print T("Incorrect mail:password argument")

    # load system information in session
    config.session._info = dict()
    config.session._info["version"] = info.version

    # print "Starting action"

    # gui.start_html_frame(config.html_frame)
    config.html_frame.window.OnLinkClicked(\
    URL(a=config.APP_NAME, c="default", f="index"))

    # re-connect periodically to database to prevent connection timeout issue
    try:
        db_timeout_milliseconds = int(config.DB_TIMEOUT)
    except (ValueError, TypeError), e:
        print "Error retrieving the db_timeout parameter ", str(e)
        # no connection timeout by default
        db_timeout_milliseconds = -1

    if db_timeout_milliseconds > 0:
        db_timeout = wx.Timer(config.html_frame)
        config.html_frame.Bind(wx.EVT_TIMER, on_db_timeout, db_timeout)
        db_timeout.Start(db_timeout_milliseconds)

    # print "App initialization complete"

    # end of app initialization

    # show the main window
    config.html_frame.Show()
    splash.Close()
    
    app.MainLoop()
