# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Captivea Sales Customizations',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 50,
    'summary': 'Changes to Sales App',
    'depends': ['sale_margin','stock_account','sale','sale_stock'],
    'description': """
Container module for extensions to Odoo Sales.
""",
    'data': [
        'views/sale_order.xml'
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
