# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import _, http
from openerp.http import request

from openerp.addons.website_portal_profile.controllers.main import (
    website_account
)

from openerp.addons.website.models.website import slug


class WebsiteAccountProposal(website_account):

    @http.route('/my/account', type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        response = super(website_account, self).details(redirect, **post)
        proposal_overview = request.env['project.proposal'].search(
            [('owner_id', '=', request.uid)],
            order='website_published DESC, start_date DESC',
            limit=4,
        )
        response.qcontext.update({
            'proposals': proposal_overview,
        })
        return response

    @http.route([
        '/proposals',
        '/proposals/<model("res.users"):user>',
    ], type='http', auth="public", website=True)
    def proposals(self, user=None, **kwargs):
        env = request.env

        Proposal = env['project.proposal']

        # List of proposals available to current UID
        domain = []
        if user:
            domain = [('owner_id', '=', user.id)]
        proposals = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )

        # Render page
        return request.website.render(
            "specific_project_proposal.proposal_index",
            {'proposals': proposals})

    @http.route('/my/proposals', type='http', auth="public", website=True)
    def my_proposals(self, **kwargs):
        return request.redirect('/proposals/%s'
                                % slug(request.env.user))

    @http.route(['/proposals/detail/<model("project.proposal"):proposal>',
                 '/my/proposals/detail/<model("project.proposal"):proposal>'],
                type='http', auth="public", website=True)
    def proposals_detail(self, proposal, **kwargs):
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
        })

    @http.route('/my/proposals/add', type='http', auth="user", website=True)
    def proposals_add(self, **kwargs):
        proposal = request.env['project.proposal'].create({
            'name': _('New Proposal'),
            'owner_id': request.uid,
        })
        return request.redirect("/my/proposals/detail/%s"
                                % slug(proposal))
