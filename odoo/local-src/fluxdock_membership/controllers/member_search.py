# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo import http, _
from odoo.http import request
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class MembersSearch(http.Controller, SearchFormControllerMixin):

    @http.route([
        '/dock/partners',
        '/dock/partners/page/<int:page>',
    ], type='http', auth="public", website=True)
    def partners_search(self, **kw):
        model = 'res.partner'
        section_vals = {
            'section_logo':
                # TODO: pick the right image
                '/fluxdock_membership/static/src/img/members-white.png',
            'section_title': _('Partners'),
            'context_menu': self._get_context_menu(),
        }
        kw.update(section_vals)
        return self.make_response(model, **kw)

    def _get_context_menu(self):
        return request.env['website']._get_dock_context_menu()
