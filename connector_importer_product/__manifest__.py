# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Connector Importer SFTP Product",
    "summary": "Product Importer",
    "version": "14.0.1.0.0",
    "category": "Tools",
    "website": "https://github.com/OCA/connector-interfaces",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        # oca
        "connector_importer_source_sftp",
        # src
        "product",
    ],
    "data": [
        # storage_backend
        "data/storage_backend.xml",
        # Imports to initialize data for production
        "data/import_backend.xml",
        "data/import_type.xml",
        "data/import_source.xml",
        "data/import_recordset.xml",
        # Demo
    ],
    "demo": [
        "demo/import_source.xml",
        "demo/import_recordset.xml",
    ],
    "installable": True,
}
