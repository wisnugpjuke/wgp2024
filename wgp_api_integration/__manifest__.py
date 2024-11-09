# -*- coding: utf-8 -*-
{
    'name': "WGP - API Integration",

    'summary': "Module for Integration",

    'description': """

    """,

    'author': "Wisnu Galih Pradita",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_expense.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "images": ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "sequence": 1
}

