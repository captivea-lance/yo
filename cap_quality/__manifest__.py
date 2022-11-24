# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Quality Captivea',
    'version': '1.0',
    'category': 'Manufacturing/Quality',
    'sequence': 50,
    'summary': 'Customization to Quality module',
    'depends': ['stock','purchase','purchase_stock','quality','quality_control'],
    'description': """
Quality 
===============
""",
    'data': [
        'security/ir.model.access.csv',
        'views/quality_clause.xml',
        'views/quality_point.xml',
        'views/product_template.xml',
        'views/purchase_order.xml'
    ],
    'demo': [],
    'application': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [

        ],
        'web.assets_qweb': [

        ],
    }
}
