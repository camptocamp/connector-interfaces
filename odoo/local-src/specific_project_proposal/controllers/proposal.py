# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import http
from openerp.http import request


class Proposal(http.Controller):

    @http.route('/market/proposals/<model("project.proposal"):proposal>',
                type='http', auth="public", website=True)
    def proposals_detail(self, proposal, filters='all', **kwargs):
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
        })
