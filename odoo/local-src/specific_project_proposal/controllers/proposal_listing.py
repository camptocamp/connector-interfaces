# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import http
from openerp.addons.cms_form.controllers.main import SearchFormControllerMixin


class ProposalListing(http.Controller, SearchFormControllerMixin):

    template = 'specific_project_proposal.proposal_search_form_wrapper'

    @http.route([
        '/market',
        '/market/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'project.proposal'
        return self.make_response(model, **kw)
