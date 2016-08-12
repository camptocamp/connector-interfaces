# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{'name': 'Fluxdock Membership Specific Development',
 'version': '9.0.1.0.0',
 'author': 'Camptocamp',
 'license': 'AGPL-3',
 'category': 'Reports',
 'website': 'http://www.camptocamp.com',
 'images': [],
 'depends': [
    'base',
    'membership',
    'membership_variable_period',
    'website_fluxdock_signup',
    'website',
    'website_portal',
    'website_portal_profile',
     ],
 'data': [
    # views
    'views/membership.xml',
    # datas
    'data/membership_data.xml',
 ],
 'test': [],
 'installable': True,
 'auto_install': False,
 }
