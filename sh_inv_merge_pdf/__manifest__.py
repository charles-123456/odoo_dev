# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Invoice Merge PDF Attachment",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "version": "14.0.1",
    "summary": "Merge PDF Attachment, Merge Attachments In Report,Account Merge PDF Attachment,Bill Merge PDF Attachment,Credit Note Merge PDF Attachment, Merge Attachment Odoo ",
    "description": """This module allows to merge PDF attachments with the invoice/bill/credit note/debit note reports. When you print a report it automatically merges those PDF attachments with that report. You can merge additional PDF attachments like terms and conditions, privacy policy, return policy, copyright, after sales service, support service etc with the report.""",
    'sequence': 10,
    'depends': ['account'],
    'data': ['views/res_config_setting.xml', 'views/inv_merge_pdf.xml'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "price": 50,
    "currency": "EUR"
}
