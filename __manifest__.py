# -*- coding: utf-8 -*-
{
    'name' : 'Coupon Management',
    'version' : '14.0.1.0.0',
    'summary': 'Coupon Management Software',
    'sequence': 10,
    'description': """Coupon Management Software""",
    'category': 'Human Resources/Employees',
    'website': 'https://www.odoomate.tech',
    'depends' : [
        'sale',
        'sale_coupon'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/order_report_view.xml',
        'views/sale.xml',
        'views/coupon_view.xml',
        'views/partner.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
