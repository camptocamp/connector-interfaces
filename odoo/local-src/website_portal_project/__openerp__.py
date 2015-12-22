# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Portal Project',
    'author': 'Goran Sunjka',
    'website': 'http://www.sunjka.de',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'description': """
This module adds projects inside your account's page on website.
==================================================================================================
    """,
    'depends': ['project', 'website_portal'],
    'data': [
        'views/project_project_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
    'category': 'Hidden',
}
