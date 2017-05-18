# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import http
from openerp.http import request


class Proposal(http.Controller):

    @http.route('/market/proposals/<model("project.proposal"):proposal>',
                type='http', auth="public", website=True)
    def proposals_detail(self, proposal, filters='all', **kwargs):
        try:
            proposal.check_access_rights('read')
            proposal.check_access_rule('read')
            redirect = ''
        except:
            redirect = '/market'
        if redirect:
            return request.redirect(redirect)
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
        })
