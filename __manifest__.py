# -*- coding: utf-8 -*-
{
    'name': "SME Solution Finder",

    'summary': """
        The SME-digital solution matchmaker""",

    'description': """
        The following module is designed to be a framework for SMEs to find out suitable
        digital solutions. Using a matchmaking framework that takes into account functional
        requirements and desired characteristics, the application finds the solution that
        best matches the needs of the SME.
    """,

    'author': "Francisco Raziel Treviño Almaguer",
    'website': "https://www.digitalshoestring.net/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizards/search_solutions.xml',
    ],
}
