# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json

from openerp import _, fields, http
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
        response.qcontext.update({
            'matches': env.user.proposal_match_ids,
            'proposals': proposal_overview,
        })
        return response


class WebsiteProposal(http.Controller):
    _proposal_per_page = 10

    def _get_domain(self, filters='all'):
        domain = []
        if filters == 'my':
            domain = [('owner_id', '=', request.env.user.id)]
        elif filters == 'matches':
            domain = [('id', 'in', request.env.user.proposal_match_ids.ids)]
        return domain

    def proposal_index(self, filters='all', page=1,
                       expertise=None, industry=None, **kwargs):
        """ Generic index for proposals and own proposals

        """
        env = request.env
        Proposal = env['project.proposal']

        domain = self._get_domain(filters)

        if filters == 'all':
            base_url = '/market'
        elif filters == 'my':
            base_url = '/my'

        if expertise:
            domain.append(('expertise_ids', 'in', expertise.id))
        elif industry:
            domain.append(('industry_ids', 'in', industry.id))

        proposal_count = Proposal.search_count(domain)

        url = base_url
        if expertise:
            url += '/expertise/%s' % slug(expertise)
        elif industry:
            url += '/industry/%s' % slug(industry)

        sorting = 'website_published DESC, start_date DESC'
        url_args = {
            'sorting': sorting
        }

        pager = request.website.pager(url=url, total=proposal_count, page=page,
                                      step=self._proposal_per_page,
                                      scope=self._proposal_per_page,
                                      url_args=url_args)

        proposals = Proposal.search(
            domain, limit=self._proposal_per_page, offset=pager['offset'],
            order=sorting
        )
        values = {
            'proposals': proposals,
            'base_url': base_url,
            'my': filters == 'my',
            'pager': pager,
            'expertise_tag': expertise,
            'industry_tag': industry,
            'filters': filters,
        }
        # Render page
        return request.website.render(
            "specific_project_proposal.proposal_index", values)

    @http.route([
        '/market',
        '/market/page/<int:page>',
        ('/market/expertise/'
         '<model("partner_project_expertise.expertise"):expertise>'),
        ('/market/expertise/'
         '<model("partner_project_expertise.expertise"):expertise>'
         '/page/<int:page>'),
        '/market/industry/<model("res.partner.category"):industry>',
        ('/market/industry/<model("res.partner.category"):industry>'
         '/page/<int:page>'),
        ], type='http', auth="public", website=True)
    def proposals(self, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        # List of proposals available to current UID
        return self.proposal_index(filters='all', **kwargs)

    @http.route([
        '/my/proposals',
        '/my/proposals/page/<int:page>',
        ('/my/proposals/expertise/'
         '<model("partner_project_expertise.expertise"):expertise>'),
        ('/my/proposals/expertise/'
         '<model("partner_project_expertise.expertise"):expertise>'
         '/page/<int:page>'),
        '/my/proposals/industry/<model("res.partner.category"):industry>',
        ('/my/proposals/industry/<model("res.partner.category"):industry>'
         '/page/<int:page>'),
        ], type='http', auth="public", website=True)
    def my_proposals(self, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}

        return self.proposal_index(filters='my', **kwargs)

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/hide',
        type='json', auth="public", website=True)
    def hide(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        proposal.blacklist()
        return {}

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/publish',
        type='json', auth="public", website=True)
    def toggle_publish(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        proposal.website_published = not proposal.website_published
        return {}

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/'
        'delete_confirm',
        type='http', auth="public", website=True)
    def delete_confirm(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        return request.render(
            "specific_project_proposal.proposal_delete_confirm", {
                'proposal': proposal,
                'main_object': proposal,
            })

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/delete',
        type='http', auth="public", website=True)
    def delete(self, proposal, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        proposal.unlink()
        return request.redirect('/my/home')

    @http.route('/proposals/detail/<model("project.proposal"):proposal>',
                type='http', auth="public", website=True)
    def proposals_detail(self, proposal, filters='all', **kwargs):
        if filters == 'match':
            return_link = '/my'
        elif filters == 'my':
            return_link = '/my/proposals'
        else:
            return_link = '/market'
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
            'filters': filters,
            'return_link': return_link,
        })

    @http.route(['/proposals/<model("project.proposal"):proposal>/previous'],
                type='http', auth="public", website=True)
    def proposal_previous(self, proposal, filters='all', **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        domain = self._get_domain(filters)
        Proposal = request.env['project.proposal']
        proposals = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )
        index = proposals.ids.index(proposal.id)
        previous_proposal = proposals[index - 1]
        params = ''
        if filters != 'all':
            params = '?filters=%s' % filters
        return request.redirect("/proposals/detail/%s%s"
                                % (slug(previous_proposal), params))

    @http.route(['/proposals/<model("project.proposal"):proposal>/next'],
                type='http', auth="public", website=True)
    def proposal_next(self, proposal, filters='all', **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        domain = self._get_domain(filters)
        Proposal = request.env['project.proposal']
        proposals = Proposal.search(
            domain, order='website_published DESC, start_date DESC',
        )
        index = proposals.ids.index(proposal.id)
        next_proposal = proposals[(index + 1) % len(proposals)]
        params = ''
        if filters != 'all':
            params = '?filters=%s' % filters

        return request.redirect("/proposals/detail/%s%s"
                                % (slug(next_proposal), params))

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
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                if post.get('post_industries'):
                    industry_ids = post['post_industries'].split(',')
                    post['industry_ids'] = [
                        (4, int(industry_id)) for industry_id
                        in industry_ids
                    ]
                if post.get('post_expertises'):
                    expertise_ids = post['post_expertises'].split(',')
                    post['expertise_ids'] = [
                        (4, int(expertise_id)) for expertise_id
                        in expertise_ids
                    ]
                if not values.get('start_date'):
                    post['start_date'] = False
                if not values.get('stop_date'):
                    post['stop_date'] = False
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

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        mandatory_fields = ['name']
        optional_fields = [
            'location', 'country_id', 'website_short_description',
            'website_description', 'start_date', 'stop_date',
            'post_industries', 'post_expertises']

        # Validation
        for field_name in mandatory_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # date validation
        if data.get('start_date') and data.get('stop_date'):
            start = fields.Date.from_string(data['start_date'])
            stop = fields.Date.from_string(data['stop_date'])
            if (stop - start).days < 0:
                error['start_date'] = 'error'
                error['stop_date'] = 'error'
                error_message.append(
                    _("End Date cannot be set before Start Date."))

        unknown = [k for k in data.iterkeys()
                   if k not in mandatory_fields + optional_fields]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    @http.route('/my/proposals/add', type='http', auth="user", website=True)
    def proposals_add(self, **kwargs):
        proposal = request.env['project.proposal'].sudo().create({
            'name': _('New Proposal'),
            'owner_id': request.uid,
        })
        return request.redirect("/my/proposals/edit/%s"
                                % slug(proposal))
