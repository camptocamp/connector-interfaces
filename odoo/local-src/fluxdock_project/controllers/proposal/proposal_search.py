# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import http
from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class ProposalListing(http.Controller, SearchFormControllerMixin):

    @http.route([
        '/market',
        '/market/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'project.proposal'
        return self.make_response(model, **kw)
