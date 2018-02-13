# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import http, _
from odoo.http import request
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class ReferenceSearch(http.Controller, SearchFormControllerMixin):

    @http.route([
        '/dock/references',
        '/dock/references/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'project.reference'
        section_vals = {
            'section_logo':
                '/fluxdock_project/static/src/img/market.png',
            'section_title': _('References'),
            'context_menu': self._get_context_menu(),
        }
        kw.update(section_vals)
        return self.make_response(model, **kw)

    def _get_context_menu(self):
        return request.env['website']._get_dock_context_menu()
