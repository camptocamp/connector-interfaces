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

    @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
    def account(self, **kw):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        response = super(website_account, self).account(**kw)
        proposal_overview = request.env['project.proposal'].search(
            [('owner_id', '=', request.uid)],
            order='website_published DESC, start_date DESC',
            limit=6,
        )
        response.qcontext.update({
            'proposals': proposal_overview,
        })
        return response

    @http.route([
        '/proposals',
        '/proposals/<model("res.users"):user>',
        '/proposals/expertise/'
        '<model("partner_project_expertise.expertise"):expertise>',
        '/proposals/industry/<model("res.partner.category"):industry>',
        ], type='http', auth="public", website=True)
    def proposals(self, user=None, expertise=None, industry=None,
                  **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        env = request.env

        Proposal = env['project.proposal']

        # List of proposals available to current UID
        domain = []
        domain = [('id', 'in', env.user.suggested_proposal_ids.ids)]
        if expertise:
            domain.append(('expertise_ids', 'in', expertise.id))
        elif industry:
            domain.append(('industry_ids', 'in', industry.id))
        proposals = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )

        # Render page
        return request.website.render(
            "specific_project_proposal.proposal_index",
            {'proposals': proposals,
             'view_type': 'suggestions',
             'expertise_tag': expertise,
             'industry_tag': industry})

    @http.route('/my/proposals', type='http', auth="public", website=True)
    def my_proposals(self, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        env = request.env

        domain = [('owner_id', '=', env.user.id)]

        Proposal = env['project.proposal']

        proposals = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )
        return request.website.render(
            "specific_project_proposal.proposal_index",
            {'proposals': proposals,
             'view_type': 'my',
             })

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/hide',
        type='json', auth="public", website=True)
    def hide(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        proposal.blacklist()
        return {}

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
