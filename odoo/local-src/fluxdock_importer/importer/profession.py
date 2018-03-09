# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component


class ProfessionMapper(Component):
    _name = 'fluxdock.v9.profession.mapper'
    _inherit = 'importer.base.mapper'
    _apply_on = 'project.partner.profession'

    required = {
        'name': 'name',
    }
    direct = [
        ('name', 'name'),
    ]


class ProfessionRecordImporter(Component):
    _name = 'fluxdock.v9.profession.importer'
    _inherit = 'importer.record'
    _apply_on = 'project.partner.profession'

    odoo_unique_key = 'name'

    def create_context(self):
        return {'tracking_disable': True}

    write_context = create_context

    def odoo_post_create(self, odoo_record, values, orig_values):
        # generate xmlid using dj machinery
        print('XMLID', odoo_record._dj_export_xmlid())
