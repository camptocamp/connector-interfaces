# Copyright 2016 Simone Orsi (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    def _get_dock_context_menu(self):
        """Defined in fluxdock_theme."""

        # TODO: get rid of this once we have cms.page
        # w/ auto context nav in place.

        menu = super()._get_dock_context_menu()
        path = request.env['project.proposal'].cms_search_url
        menu.append({
            'id': 'dock-proposals',
            'name': _('Proposals'),
            'url': path,
            'active': self.menu_item_is_active(path),
        })
        path = request.env['project.reference'].cms_search_url
        menu.append({
            'id': 'dock-references',
            'name': _('References'),
            'url': path,
            'active': self.menu_item_is_active(path),
        })
        return menu
