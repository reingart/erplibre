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
import gluon

import gluon.validators

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db
T = config.env["T"]
session = config.session

import os, csv, datetime

# import psycopg2

"""
Migration module for legacy databases
This is an experiment to transfer ms-access and other csv exportable sources to a DAL managed database
Input is a directory with one .csv file for each table (including a field name header)

Here is the transfering task. Map every field to the new database design structure

LEGACY_TABLES: dictionary with { [table_csv_file_name]: { "table_name": [new table name], fields: [ (fieldname, index or None), ... ] }, ... } structure

"""

LEGACY_TABLES = {}
LEGACY_TABLES_ROUTE = None
PRIVATE_ROUTE = None


# Old database field conversion pattern (from csv to dict)
# Input csv file: a list of records in the following syntax:
# tablearchive.csv, db_table_name, db_field_name, csv_record_field_index,
# data type (web2py dal), default value
def import_csv_pattern(path):
    csvfilename = ""
    tmpdict = {}
    spam_reader = csv.reader(open(path, "rb"))
    for number, line in enumerate(spam_reader):
        # skip header
        if number <= 0:
            continue
        # check table change
        if line[0] != csvfilename:
             # 0: filename, 1: tablename , 2: field, 3: index value, 4 and 5 are type and default value
            tmpdict[line[0]] = dict(table_name = line[1].strip(), fields = [(line[2].strip(), int(line[3]), str(line[4]).strip(), str(line[5]).strip()),])
        else:
            tmpdict[line[0]]["fields"].append((line[2].strip(), int(line[3]), str(line[4]).strip(), str(line[5]).strip()))
        csvfilename = line[0]
    return tmpdict


# data parse for csv input
def parse_value(string_type, string_default, string_value):
    # TODO: handle value, attribute errors
    rt_value = None
    if string_type:
        if string_type == "integer":
            try:
                rt_value = int(string_value)
            except:
                try:
                    rt_value = int(string_default)
                except:
                    rt_value = None
        elif string_type == "double":
            try:
                rt_value = float(string_value)
            except:
                try:
                    rt_value = float(string_default)
                except:
                    rt_value = None
        elif string_type == "date":
            try:
                rt_value = datetime.date(int(string_value[:4]), int(string_value[5:7]), int(string_value[8:]))
            except:
                try:
                    rt_value = datetime.date(int(string_default[:4]), int(string_default[5:7]), int(string_default[8:]))
                except:
                    rt_value = None
        elif string_type == "string":
            try:
                rt_value = str(string_value)
                if len(rt_value) <= 0:
                    rt_value = None
            except:
                rt_value = None

        return rt_value
    else:
        return string_value


# insert database records using a dict pattern from csv tables
# csv tables must be stored in
# applications/application/private/legacy_tables

def populate_with_legacy_db(legacy_tables_route, legacy_tables):
    records = 0
    errors = 0
    voidstrings = 0
    for table_file_name, table_data in legacy_tables.iteritems():
        # open file with csv reader
        try:
            spam_reader = csv.reader(open(os.path.join(legacy_tables_route, table_file_name), 'rb'))
        except IOError:
            continue
        
        table = legacy_tables[table_file_name]["table_name"]
        fields = legacy_tables[table_file_name]["fields"]

        # delete table records
        db(db[table]).delete()
        db.commit()

        # reset the insertion counter
        table_records = 0

        for n, table_record in enumerate(spam_reader):
            if n>0:
                tmpdict = dict()
                try:
                    for v in fields:
                        # v[2] is string data type (or '')
                        # v[3] is string default value (or '')
                        if not ((table_record[v[1]].strip() == '') or (table_record[v[1]] is None)):
                            # filter value
                            tmpdict[v[0].strip()] = parse_value(v[2], v[3], table_record[v[1]])
                        else:
                            voidstrings +=1

                    if len(tmpdict) > 1:
                        """
                        # exclude table_id fields
                        if (table + "_id") in tmpdict:
                            tmpdict.pop(table + "_id")
                        elif "id" in tmpdict: tmpdict.pop("id")
                        """
                        print T("Inserting"), [v for k, v in tmpdict.iteritems()], "in", table

                        the_id = db[table].insert(**tmpdict)
                        table_records += 1
                        records += 1

                except Exception, e:
                    # TODO: catch common db exceptions
                    print str(e)
                    raise
                    # db.debugging.insert(msg="Populate_with_legacy_db Insert Error: Table %s, row %s: %s" % (table, str(n), str(e)))
                    errors += 1

        if table_records > 0:
            db.commit()

    print T("Inserted"), records, T("db records")
        
    return records, errors, voidstrings

def index(): return dict(message="hello from migration.py")

# Get legacy database records and insert them in the app's db
def import_csv_dir(evt, args=[], vars={}):
    config.session.form = FORM(INPUT(_value="Load from CSV", _type="submit"))
    if evt is not None:
        if config.session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            legacy_tables = import_csv_pattern(config.CSV_CONFIG_FILE)
            result = populate_with_legacy_db(config.CSV_TABLES_ROUTE, legacy_tables)
            print T("Load tables from CSV (records, errors and voidstrings)"), result
            config.session.message = ("%s "  % result[0]) + T("records inserted")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="setup", f="index"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, import_csv_dir)

    return dict(form = session.form)


def db_to_csv(evt, args=[], vars={}):
    session.form = SQLFORM.factory(Field("path", comment=T("Storage folder"), requires=IS_NOT_EMPTY()), Field("file", comment="File name"))
    session.form.element("[name=file]").attributes["_class"] = "file"
    session.form.element("[name=path]").attributes["_class"] = "path"
    if evt is not None:
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            f = open(os.path.join(session.form.vars.path, session.form.vars.file), "wb")
            print T("Exporting to CSV format file"), f.name

            db.export_to_csv_file(f)
            f.close()
            print "Done"
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="setup", f="index"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, db_to_csv)
    return dict()


def csv_to_db(evt, args=[], vars={}):
    is_pg = False
    is_pg = ("postgres" in config.db["_uri"])
    session.form = SQLFORM.factory(Field("path", comment=T("Storage folder"), requires=IS_NOT_EMPTY()), Field("file", comment=T("File name")), Field("suspend_integrity_check", "boolean", comment=T("For PostgreSQL databases. Use this option with care. A superuser database conection is required")))
    session.form.element("[name=file]").attributes["_class"] = "file"
    session.form.element("[name=path]").attributes["_class"] = "path"    
    if evt is not None:
        
        if session.form.accepts(evt.args, formname=None, keepvalues=False, dbio=False):
            print T("PostgreSQL database"), is_pg
            print T("Disable integrity check"), (is_pg and session.form.vars.suspend_integrity_check == True)

            if is_pg and session.form.vars.suspend_integrity_check == True:
                # disable integrity triggers (and all others) in PostgreSQL
                print T("Altering tables to disable PostgreSQL triggers temporarily")
                for table in db.tables:
                    try:
                        db.executesql("ALTER TABLE %s DISABLE TRIGGER ALL;" % table)
                    except Exception, e:
                        print str(e)

            f = open(os.path.join(session.form.vars.path, session.form.vars.file), "r")
            print T("Importing from CSV format file"), f.name
            try:
                db.import_from_csv_file(f)
                db.commit()
            except Exception, e:
                print str(e)
            f.close()

            if is_pg and session.form.vars.suspend_integrity_check == True:
                # enable integrity triggers (and all others) in PostgreSQL
                print T("Altering tables to re-enable PostgreSQL triggers")
                for table in db.tables:
                    try:
                        db.executesql("ALTER TABLE %s ENABLE TRIGGER ALL;" % table)
                    except Exception, e:
                        print str(e)
            db.commit()
            print T("Done")
            return config.html_frame.window.OnLinkClicked(URL(a=config.APP_NAME, c="setup", f="index"))
    else:
        config.html_frame.window.Bind(EVT_FORM_SUBMIT, csv_to_db)
    return dict()
