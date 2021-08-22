# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Product Brands",
    "summary": 'Product Brands',
    'description': """
       By using this app user can filtere results of products based on different brands. 
       This app facilitates you to add new brands in your inventory, 
       assign them to respective products and easily filter, view products by their assigned brand.
    """,
    "sequence": 1,
    "category": "Inventory Management",

    "author": "EZ SOlutions",
    "website": "",
    "version": '14.0.0.1',
    'price': 11.99,
    'currency': 'USD',
    'license': 'OPL-1',
    "depends": ['base','stock'],
    'images': [
        'static/description/web-banner.gif',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/product_brands.xml',
        'views/product_brands_inherited_views.xml',
    ],

    "installable": True,
    "application": False,
    "auto_install": False,
}
