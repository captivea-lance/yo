# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Captivea Smart Margin Calculation',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 50,
    'summary': 'Customization to Margin Calculation',
    'depends': ['sale_margin','stock_account','sale'],
    'description': """
Quality 
===============
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
