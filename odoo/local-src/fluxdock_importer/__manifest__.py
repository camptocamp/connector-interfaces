# Author: Simone Orsi
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Fluxdock Importer',
    'summary': 'Fluxdock Importer TODO',
    'version': '11.0.1.0.0',
    'category': 'Generic Modules',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'depends': [
        'connector_importer_source_odoorpc',
        'fluxdock_membership',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'data/import_data.xml',
    ],
}
