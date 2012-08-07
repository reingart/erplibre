#! /usr/bin/python
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

if __name__ == "__main__":
    import sys
    import os
    print "##############################################"
    print "For installation options type:"
    print "]$setup.py --help"
    print "from the unzipped ERP Libre folder"
    print "##############################################"
    print
    print "Changing the cwd to %s" % sys.path[0]
    os.chdir(sys.path[0])
    sys.argv.append("--install")
    sys.argv.append("--client")
    import setup
    sys.exit(0)
