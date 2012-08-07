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

import sys, os

# Keep "erplibre" as app name for consistency
# with gui app controllers
# TODO: application string replacement with APP_NAME call
# for old URL constructions and auto-named web2py/gui paths

# The name given to the installed web2py app
APP_NAME = "erplibre"


# System user (optional)
# used as reference for path construction
SYSTEM_USER_NAME = "user"

arg_counter = 0
for arg in sys.argv:
    arg_counter +=1
    if arg == "--system_user_name":
        try:
            SYSTEM_USER_NAME = sys.argv[arg_counter]
        except IndexError:
            "No system user specified. Default is %s" % SYSTEM_USER_NAME


# send debugging data to standard output
VERBOSE = False

# Gui app installation name
# used for local URLs and titles
WEB2PY_APP_NAME = "erplibre"

# Change paths to match the system's configuration
# Default values (overwritten with config.ini values)
WEB2PY_FOLDER = r"/home/%s/web2py" % SYSTEM_USER_NAME
GUI2PY_FOLDER = r"/home/%s/gui2py-hg" % SYSTEM_USER_NAME
GUI2PY_APP_FOLDER = r"/home/%s/erplibre_gui-hg" % SYSTEM_USER_NAME
DATABASES_FOLDER = r"/home/%s/erplibre_gui-hg/databases/" % SYSTEM_USER_NAME
TEMPLATES_FOLDER = r"/home/%s/erplibre_gui-hg/views/" % SYSTEM_USER_NAME
PDF_TEMPLATES_FOLDER = r"/home/%s/erplibre_gui-hg/pdf_templates/" % SYSTEM_USER_NAME
OUTPUT_FOLDER = r"/home/%s/erplibre_gui-hg/output/" % SYSTEM_USER_NAME
# WEB2PY_APP_FOLDER = r"/home/%s/web2py/applications/%s/" % (SYSTEM_USER_NAME, WEB2PY_APP_NAME)
WEB2PY_APP_FOLDER = ""
LEGACY_DB=False
DB_URI = r'sqlite://storage.sqlite'
IMAP_URI = "" # experimental (for web2py IMAP adapter
# Time in milliseconds to restart db connection (for connection timeout issues)
DB_TIMEOUT = -1
HMAC_KEY = "sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a"
GUI2PY_APP_CLIENT=False


# default language
LANGUAGE="en"


# config.ini

# Parse config values
# Loop trough configuration records
# Change each value if specified or keep
# defaults

try:
    with open("config.ini") as config_ini:
        for line in config_ini.readlines():
            values = line.strip().split("=")
            if len(values) == 2:
                locals()[values[0]] = values[1]

except IOError, e:
    print "Error accessing config.ini: " + str(e)


def write_values(data):
    with open(os.path.join(os.getcwd(), "config.ini"), "w") as config_file:
        for name, value in data.iteritems():
            if name.isupper():
                if isinstance(value, basestring):
                    # static value
                    config_file.write(name + "=" + value + "\n")
                elif value is None:
                    config_file.write(name + "=" + "\n")
                else:
                    config_file.write(name + "=" + str(value) + "\n")

    # write web2py app .ini file
    if WEB2PY_APP_FOLDER != "":
        # Duplicated ini file for web2py app to know ini values
        # It is impossible to use this workaround on environments without access
        # to the file system so this would probably raise exceptions.
        with open(os.path.join(WEB2PY_APP_FOLDER, "private", "webappconfig.ini"), "w") as webapp_config_file:
            for name, value in data.iteritems():
                if isinstance(value, basestring) and name.isupper():
                    # static value
                    webapp_config_file.write(name + "=" + value + "\n")

# send a message to output if verbose
# mode is enabled
def verbose(message):
    if VERBOSE:
        print message

# import wx
# import wx.html

# import gluon
# from gluon import *

WX_HTML_STYLE = None

# CSV first run data for examples (optional)
CSV_CONFIG_FILE = os.path.join(os.getcwd(), "example_db", "spanish.csv")
CSV_TABLES_ROUTE = os.path.join(os.getcwd(), "example_db", "spanish")

# create DAL connection (and create DB if does not exists)
# db = DAL(DB_URI, folder=DATABASES_FOLDER)
db = None

# create a testing frame (wx "window"):
starting_frame = None
html_frame = None
address = None
menu = None
env = None
crud = None
auth = None
menu = None
response = None
request = None
session = None
after_submission = dict()
actions = dict()
event_handlers = dict()
access_control = None

_auth_next = None
_auth_source = None
_this_url = -1
_urls = []

# Dictiary with menu items and event binding
# replace "action"... with "handler": "module.handler" for no URL event handlers
#
#    "name": {
#    "position": -1, "label": "", "visible": True, "enabled": False, "action": None, "submenu":{}
#    }


MAIN_MENU = None


# web colors
COLORS = [
# gray scale
"000000","080808","101010","181818","202020","282828",
"303030","383838","404040","484848","505050","585858",
"606060","686868","707070","787878","808080","888888",
"909090","989898","A0A0A0","A8A8A8","B0B0B0","B8B8B8",
"C0C0C0","C8C8C8","D0D0D0","D8D8D8","E0E0E0","E8E8E8",
"F0F0F0","F8F8F8","FFFFFF",
# other
"000033","000066","000099","0000CC","0000FF",
"003300","003333","003366","003399","0033CC","0033FF",
"006600","006633","006666","006699","0066CC","0066FF",
"009900","009933","009966","009999","0099CC","0099FF",
"00CC00","00CC33","00CC66","00CC99","00CCCC","00CCFF",
"00FF00","00FF33","00FF66","00FF99","00FFCC","00FFFF",
"330000","330033","330066","330099","3300CC","3300FF",
"333300","333333","333366","333399","3333CC","3333FF",
"336600","336633","336666","336699","3366CC","3366FF",
"339900","339933","339966","339999","3399CC","3399FF",
"33CC00","33CC33","33CC66","33CC99","33CCCC","33CCFF",
"33FF00","33FF33","33FF66","33FF99","33FFCC","33FFFF",
"660000","660033","660066","660099","6600CC","6600FF",
"663300","663333","663366","663399","6633CC","6633FF",
"666600","666633","666666","666699","6666CC","6666FF",
"669900","669933","669966","669999","6699CC","6699FF",
"66CC00","66CC33","66CC66","66CC99","66CCCC","66CCFF",
"66FF00","66FF33","66FF66","66FF99","66FFCC","66FFFF",
"990000","990033","990066","990099","9900CC","9900FF",
"993300","993333","993366","993399","9933CC","9933FF",
"996600","996633","996666","996699","9966CC","9966FF",
"999900","999933","999966","999999","9999CC","9999FF",
"99CC00","99CC33","99CC66","99CC99","99CCCC","99CCFF",
"99FF00","99FF33","99FF66","99FF99","99FFCC","99FFFF",
"CC0000","CC0033","CC0066","CC0099","CC00CC","CC00FF",
"CC3300","CC3333","CC3366","CC3399","CC33CC","CC33FF",
"CC6600","CC6633","CC6666","CC6699","CC66CC","CC66FF",
"CC9900","CC9933","CC9966","CC9999","CC99CC","CC99FF",
"CCCC00","CCCC33","CCCC66","CCCC99","CCCCCC","CCCCFF",
"CCFF00","CCFF33","CCFF66","CCFF99","CCFFCC","CCFFFF",
"FF0000","FF0033","FF0066","FF0099","FF00CC","FF00FF",
"FF3300","FF3333","FF3366","FF3399","FF33CC","FF33FF",
"FF6600","FF6633","FF6666","FF6699","FF66CC","FF66FF",
"FF9900","FF9933","FF9966","FF9999","FF99CC","FF99FF",
"FFCC00","FFCC33","FFCC66","FFCC99","FFCCCC","FFCCFF",
"FFFF00","FFFF33","FFFF66","FFFF99","FFFFCC"
]
