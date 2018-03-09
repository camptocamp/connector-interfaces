# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Partner Project Profession',
    'version': '11.0.1.0.0',
    'category': 'Projects & Services',
    'summary': """
Partner Project Profession
==========================
Add profession to partner and project.
    """,
    'author': 'Camptocamp',
    'website': 'www.camptomcamp.com',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/project_view.xml',
        'view/partner_view.xml',
        'view/profession_view.xml',
    ],
    'demo': [
        'demo/partner_profession_demo.xml',
    ],
}
