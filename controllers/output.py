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

import os
import os.path

import gluon
import gluon.validators
from gluon import *

from gui2py.form import EVT_FORM_SUBMIT

import config
db = config.db

T = config.env["T"]
session = config.session

def utftolatin(text):
    try:
        return unicode(text, "utf-8").encode("latin-1")
    except TypeError:
        return ""

def amountorzero(amount):
    try: amount = float(amount)
    except (ValueError, TypeError): amount = 0.00
    return amount


def operation(evt, args=[], vars={}):
    # Creates a pdf with operation data
    # args: "operation", "[operation_id]"

    operation_id = args[1]

    operation = db.operation[operation_id]
    supplier = db(db.supplier.supplier_id == operation.supplier_id).select().first()
    document = db(db.document.document_id == operation.document_id).select().first()
    payment_terms = db(db.payment_terms.payment_terms_id == operation.payment_terms_id).select().first()
    customer = db(db.customer.customer_id == operation.customer_id).select().first()

    vat_q = db.movement.operation_id == operation_id
    vat_q &= db.movement.concept_id == db.concept.concept_id
    vat_q &= db.concept.tax == True

    vat_amount = sum([amountorzero(row.movement.amount) for row in db(vat_q).select()], 0.00)

    if payment_terms is not None:
        payment_terms = payment_terms.code
        
    try:
        point_of_sale = document.point_of_sale_id.code
    except (AttributeError, RuntimeError), e:
        # no point of sale defined
        # or db query error
        point_of_sale = "0000"

    from gluon.contrib.pyfpdf import Template

    # generate sample invoice (according Argentina's regulations)
    the_details = db(db.movement.operation_id == operation_id).select()

    import random
    from decimal import Decimal

    # Instantiate the PyFPDF template
    f = Template(format="A4",
             title=T("Operation number") + " %s" % operation_id, author="GestionLibre",
             subject=utftolatin(document.description), keywords="Sales/Stock/Purchases document")
             
    # Complete the template object with .csv file element difinition
    f.parse_csv(infile=os.path.join(config.PDF_TEMPLATES_FOLDER, 'invoice.csv'), delimiter=";", decimal_sep=",")

    detail = ""
    items = []
    i = 0

    # Here goes the actual document data
    
    for detail in the_details:
        concept = db(db.concept.concept_id == detail.concept_id).select().first()

        i += 1
        ds = utftolatin(concept.description)
        qty = "%.3f" % float(detail.quantity)
        price = str(detail.value)
        code = str(detail.code)

        items.append(dict(code=code, unit=str(concept.measure),
                          qty=qty, price=price,
                          amount=str(detail.amount),
                          ds="%s: %s" % (i,ds)))

    # divide and count lines
    lines = 0
    li_items = []

    unit = qty = code = None

    for it in items:
        qty = it['qty']
        code = it['code']
        unit = it['unit']
        
        for ds in f.split_multicell(it['ds'], 'item_description01'):
            # add item description line (without price nor amount)
            li_items.append(dict(code=code, ds=ds, qty=qty, unit=unit, price=None, amount=None))
            # clean qty and code (show only at first)
            unit = qty = code = None
            
        # set last item line price and amount
        li_items[-1].update(amount = it['amount'],
                            price = it['price'])

    obs="\n<U>" + T("Observations") + "</U>\n\n" + str(detail.description)

    for ds in f.split_multicell(obs, 'item_description01'):
        li_items.append(dict(code=code, ds=ds, qty=qty, unit=unit, price=None, amount=None))

    # calculate pages:
    lines = len(li_items)
    max_lines_per_page = 24
    pages = lines / (max_lines_per_page - 1)
    if lines % (max_lines_per_page - 1): pages = pages + 1

    # field and page completion
    
    for page in range(1, pages+1):
        f.add_page()
        f['page'] = T(u'Page') + " %s %s %s" % (page, T("of"), pages)
        if pages>1 and page<pages:
            s = T(u'Continues at page %s') % (page+1)
        else:
            s = ''
        f['item_description%02d' % (max_lines_per_page+1)] = s

        logo = (os.path.join(config.PDF_TEMPLATES_FOLDER, "logo_fpdf.png"))

        f["company_name"] = utftolatin(supplier.legal_name)
        f["company_logo"] = logo
        
        f["company_header1"] = utftolatin(supplier.address)
        f["company_header2"] = "CUIT " + str(supplier.tax_identification)
        
        f["company_footer1"] = utftolatin(document.description)
        f["company_footer2"] = T("Generic operation")
        
        f['number'] = str(point_of_sale).zfill(4) + "-" + str(operation.operation_id).zfill(7)
        
        f['payment'] = utftolatin(payment_terms)
        
        f['document_type'] = "X"

        f['customer_address'] = T(utftolatin('Dirección'))
        f['item_description'] = T(utftolatin('Descripción'))

        f['barcode'] = "0000000000"
        f['barcode_readable'] = T(u"No document code")

        try:
            issue_date = operation.posted.strftime("%d-%m-%Y")
        except (TypeError, AttributeError):
            issue_date = ""

        try:
            due_date = operation.posted.strftime("%d-%m-%Y")
        except (TypeError, AttributeError):
            due_date = ""

        f['issue_date'] = issue_date
        f['due_date'] = due_date

        f['customer_name'] = utftolatin(customer.legal_name)
        f['customer_address'] = utftolatin(customer.address)
        f['customer_vat'] = utftolatin(customer.tax_identification)
        f['customer_phone'] = utftolatin(customer.telephone)
        
        if customer.city_id is not None:
            f['customer_city'] = utftolatin(customer.city_id.description)
        else:
            f['customer_city'] = None
        f['customer_taxid'] = utftolatin(customer.tax_identification)

        # print line item...
        li = 0
        k = 0
        total = 0.00
        for it in li_items:
            k = k + 1
            if k > page * (max_lines_per_page - 1):
                break
            if it['amount']:
                try:
                    total += float(it['amount'])
                except (ValueError, TypeError), e:
                    print "Total amount update failed: ", str(e)

            if k > (page - 1) * (max_lines_per_page - 1):
                li += 1
                if it['qty'] is not None:
                    f['item_quantity%02d' % li] = it['qty']
                if it['code'] is not None:
                    f['item_code%02d' % li] = it['code']
                if it['unit'] is not None:
                    f['item_unit%02d' % li] = it['unit']
                f['item_description%02d' % li] = it['ds']
                if it['price'] is not None:
                    try:
                        f['item_price%02d' % li] = "%0.2f" % float(it['price'])
                    except (TypeError, ValueError), e:
                        print "Price field error: ", str(e) 
                if it['amount'] is not None:
                    try:
                        f['item_amount%02d' % li] = "%0.2f" % float(it['amount'])
                    except (TypeError, ValueError), e:
                        print "Amount field error: ", str(e)

        if pages == page:
            f['net'] = "%0.2f" % (amountorzero(operation.amount) -vat_amount)
            f['vat'] = "%0.2f" % vat_amount
            f['total_label'] = T('Total:')
        else:
            f['total_label'] = T('SubTotal:')
        f['total'] = "%0.2f" % amountorzero(operation.amount)

    document_name = '%s_%s.pdf' % ("_".join(document.description.split()), operation_id)
    
    f.render(os.path.join(config.OUTPUT_FOLDER, document_name), dest='F')

    return dict(message = T("The document %s was created sucessfully") % document_name)

