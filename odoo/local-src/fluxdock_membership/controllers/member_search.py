# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo import http
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class MembersSearch(http.Controller, SearchFormControllerMixin):

    @http.route([
        '/dock/partners',
        '/dock/partners/page/<int:page>',
    ], type='http', auth="public", website=True)
    def partners_search(self, **kw):
        model = 'res.partner'
        return self.make_response(model, **kw)
