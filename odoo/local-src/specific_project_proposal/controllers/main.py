# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json

from openerp import _, http
from openerp.http import request

from openerp.addons.specific_membership.controllers.main import (
    WebsiteAccount
)

from openerp.addons.website.models.website import slug


class WebsiteAccountProposal(WebsiteAccount):

    @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
    def account(self, **kw):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        env = request.env

        Proposal = env['project.proposal']

        response = super(WebsiteAccountProposal, self).account(**kw)
        proposal_overview = Proposal.search(
            [('owner_id', '=', request.uid)],
            order='website_published DESC, start_date DESC',
        )
        domain = [('id', 'in', env.user.proposal_match_ids.ids)]
        proposal_matches = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )
        response.qcontext.update({
            'matches': proposal_matches,
            'proposals': proposal_overview,
        })
        return response


class WebsiteProposal(http.Controller):

    @http.route([
        '/market',
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
             })

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/hide',
        type='json', auth="public", website=True)
    def hide(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        proposal.blacklist()
        return {}

    @http.route(['/proposals/detail/<model("project.proposal"):proposal>'],
                type='http', auth="public", website=True)
    def proposals_detail(self, proposal, **kwargs):
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
        })

    @http.route(['/my/proposals/edit/<model("project.proposal"):proposal>'],
                type='http', auth="public", website=True)
    def my_proposals_detail(self, proposal, redirect=None, **post):
        values = {
            'error': {},
            'error_message': []
        }

        error = None
        error_message = None

        if post:
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                if post.get('post_industries'):
                    industry_ids = post['post_industries'].split(',')
                    post['industrie_ids'] = [
                        (4, int(industry_id)) for industry_id
                        in industry_ids
                    ]
                if post.get('post_expertises'):
                    expertise_ids = post['post_expertises'].split(',')
                    post['expertise_ids'] = [
                        (4, int(expertise_id)) for expertise_id
                        in expertise_ids
                    ]
                proposal.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        industries = [
            dict(id=industry.id, name=industry.name)
            for industry in proposal.industry_ids]
        industries = json.dumps(industries)

        expertise = [
            dict(id=expertise.id, name=expertise.name)
            for expertise in proposal.expertise_ids]
        expertises = json.dumps(expertise)
        countries = request.env['res.country'].sudo().search([])

        values.update({
            'proposal': proposal,
            'industries': industries,
            'expertises': expertises,
            'countries': countries,
            'redirect': redirect,
        })

        return request.render("specific_project_proposal.proposal_edit",
                              values)

    @http.route('/my/proposals/add', type='http', auth="user", website=True)
    def proposals_add(self, **kwargs):
        proposal = request.env['project.proposal'].sudo().create({
            'name': _('New Proposal'),
            'owner_id': request.uid,
        })
        return request.redirect("/my/proposals/edit/%s"
                                % slug(proposal))
