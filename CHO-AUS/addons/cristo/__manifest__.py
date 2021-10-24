# -*- coding: utf-8 -*-
{
    'name': 'CristO Aus',
    'version': '13.2.0',
    'category': '',
    'sequence': 2,
    'summary': 'Parish & Religious Management Software',
    'description': """Parish & Religious Management Software""",
    'author': 'Boscosoft Technologies Pvt Ltd',
    'website': 'https://www.boscosofttech.com',
    'depends': [
                'base','mail','web',
               ],
    'data': [
                'security/ir.model.access.csv',
                
                'data/personal_data.xml',
                'data/ecclesial_data.xml',
                'data/educational_data.xml',
                'data/study_level_member.xml',
                
                'views/res_ecclesia_views.xml',
                'views/res_member_views.xml',
                'views/res_family_views.xml',
                'views/res_sacraments_views.xml',
                'views/res_configuration_view.xml',
                'views/menus.xml',
            ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
