# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Fluxdock Project specific development',
 'version': '9.0.1.0.0',
 'category': '',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'website': 'http://www.camptocamp.com/',
 'depends': [
     'project',
     'partner_project_expertise',
     'specific_membership',
     'cms_form',
     'cms_delete_content',
     'theme_fluxdocs',
 ],
 'data': [
     'security/ir.model.access.csv',
     'security/record_rules.xml',
     'views/project_reference.xml',
     'views/menu.xml',
     'templates/reference.xml',
     'templates/search_form.xml',
     'templates/my_home.xml',
     'templates/help_msgs.xml',
 ],
 'test': [],
 'installable': True,
 'auto_install': False,
 'application': True,
 }
