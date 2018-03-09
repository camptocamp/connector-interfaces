# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component
# from odoo.addons.connector_importer.utils.mapper_utils import (
#     backend_to_rel,
#     # to_safe_int,
#     convert,
#     concat,
#     from_mapping,
# )


class PartnerMapper(Component):
    _name = 'fluxdock.v9.partner.mapper'
    _inherit = 'importer.base.mapper'
    _apply_on = 'res.partner'

    required = {
        'name': 'name',
    }

    defaults = [
    ]

    direct = [
        ('name', 'name'),
    ]


class PartnerRecordImporter(Component):
    _name = 'fluxdock.v9.partner.importer'
    _inherit = 'odoorpc.base.importer'
    _apply_on = 'res.partner'

    odoo_unique_key = 'ref'

    def create_context(self):
        return {'tracking_disable': True}

    write_context = create_context

    # def odoo_post_create(self, odoo_record, values, orig_values):
    #     self.handle_address(odoo_record, values, orig_values)
    #
    # odoo_post_write = odoo_post_create
