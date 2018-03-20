# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import http, _
from odoo.http import request
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class ProposalSearch(http.Controller, SearchFormControllerMixin):

    @http.route([
        '/dock/proposals',
        '/dock/proposals/page/<int:page>',
    ], type='http', auth="public", website=True)
    def references(self, **kw):
        model = 'project.proposal'
        section_vals = {
            'section_logo':
                '/fluxdock_project/static/src/img/market.png',
            'section_title': _('Proposals'),
            'context_menu': self._get_context_menu(),
            'custom_header_template':
                'fluxdock_project.dock_proposals_editable_header',
        }
        kw.update(section_vals)
        return self.make_response(model, **kw)

    def _get_context_menu(self):
        return request.env['website']._get_dock_context_menu()
