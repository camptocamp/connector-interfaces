# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import http
from odoo.http import request


class Proposal(http.Controller):

    @http.route('/dock/proposals/<model("project.proposal"):proposal>',
                type='http', auth="public", website=True)
    def proposal_detail(self, proposal, filters='all', **kwargs):
        return request.render("fluxdock_project.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
        })
