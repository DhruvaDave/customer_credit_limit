{
    'name': 'Customer Credit Limit',
    'version': '12',
    'category': 'Partner',
    'author': 'Dhruva Dave',
    'website': 'http://www.odoo.com',
    'summary': 'Customer credit limit',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/payment_grid_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
