# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component


class UserMapper(Component):
    _name = 'fluxdock.v9.user.mapper'
    _inherit = 'importer.base.mapper'
    _apply_on = 'res.users'

    direct = [
        ('login', 'login', ),
        ('name', 'name', ),
    ]


class UserRecordImporter(Component):
    _name = 'fluxdock.v9.user.importer'
    _inherit = 'odoorpc.base.importer'
    _apply_on = 'res.users'

    odoo_unique_key = 'login'

    def create_context(self):
        return {'tracking_disable': True, 'no_reset_password': True}

    write_context = create_context
