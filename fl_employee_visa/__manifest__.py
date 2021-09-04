# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Letter Management",
    "category": 'Employee',
    "summary": 'Employee Letter Management',
    "description": """
            Using this app Employees can easily make Visa Request. 
            Visa request will go through HR for approval. 
    """,
    "sequence": 1,
    "author": "EZ Solutions",
    "website": "",
    "version": '14.0.0.1',
    "depends": ['base','hr'],
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/employee_visa_view.xml',
        'views/employee_visa_view_inh.xml',
        'views/employee_visa_embassy_view.xml',
        'views/employee_visa_category_view.xml',
        'reports/intro_letter.xml',
    ],

    "price": 10,
    "currency": 'USD',
    "installable": True,
    "application": False,
    "auto_install": False,
}
