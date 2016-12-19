# -*- coding: utf-8 -*-
# © 2016 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Fluxdock Project Proposals specific development',
 'version': '9.0.1.0.0',
 'category': '',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'website': 'http://www.camptocamp.com/',
 'depends': [
     'project',
     'partner_project_expertise',
     'specific_membership',
 ],
 'data': [
     'security/ir.model.access.csv',
     'security/record_rules.xml',
     'views/menu.xml',
     'views/project_proposal.xml',
     'templates/assets.xml',
     'templates/layout.xml',
     'templates/proposal.xml',
     'templates/proposal_listing.xml',
     'templates/my_home.xml',
 ],
 'demo': [
     # 'demo/project_proposal.xml'
 ],
 'test': [],
 'installable': True,
 'auto_install': False,
 'application': True,
 }
