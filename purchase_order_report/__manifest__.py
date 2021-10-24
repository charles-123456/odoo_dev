{
    'name': 'Custom Purchase Report',
    'version': '14.0.1.0.0',
    'summary': 'Hour overview in purchase',
    'author': 'Primoris Systems India Pvt Ltd',
    'website':'https://www.primorissystems.com/',
    'category': 'Purchase Management',
    'depends': ['purchase','web'],
    'data': [
            'views/purchase_order_inherit.xml',
            'report/purchase_order.xml',
            'report/report.xml',
        ],
    'installable': True,
}