# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json
import werkzeug.urls

from openerp import _, fields, http
from openerp.http import request

from openerp.addons.specific_membership.controllers.main import (
    WebsiteAccount
)

from openerp.addons.website.models.website import slug


class WebsiteAccountProposal(WebsiteAccount):

    @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
    def account(self, **kw):
        env = request.env

        Proposal = env['project.proposal']

        response = super(WebsiteAccountProposal, self).account(**kw)
        proposal_overview = Proposal.search(
            [('owner_id', '=', request.uid)],
            order='website_published DESC, create_date DESC',
        )
        response.qcontext.update({
            'matches': env.user.proposal_match_ids,
            'proposals': proposal_overview,
        })
        return response


class WebsiteProposal(http.Controller):
    _proposal_per_page = 10

    def _get_domain(self, filters='all', search_name='', search_industries='',
                    search_expertises='', search_country='', search_location=''
                    ):
        domain = []
        industry_ids = None
        if filters == 'my':
            domain = [('owner_id', '=', request.env.user.id)]
        elif filters == 'match':
            domain = [('id', 'in', request.env.user.proposal_match_ids.ids)]
        if search_name:
            domain.append(('name', 'ilike', search_name))
        if search_industries:
            industry_ids = search_industries.split(',')
            domain.append(('industry_ids', 'in', industry_ids))
        if search_expertises:
            expertise_ids = search_expertises.split(',')
            domain.append(('expertise_ids', 'in', expertise_ids))
        if search_country and search_country.isdigit():
            domain.append(('country_id', '=', int(search_country)))
        if search_location:
            domain.append(('location', 'ilike', search_location))
        return domain

    def _get_url_args(self, filters, **kwargs):
        search_fields = [
            'search_name', 'search_industries', 'search_expertises',
            'search_country', 'search_location']
        url_args = {k: v for (k, v) in kwargs.iteritems()
                    if k in search_fields and v}
        if filters != 'all':
            url_args['filters'] = filters
        return url_args

    def _url_with_args(self, url, filters, **kwargs):
        url_args = self._get_url_args(filters, **kwargs)
        if not url_args:
            return url
        return "%s?%s" % (url, werkzeug.url_encode(url_args))

    def proposal_index(self, filters='all', page=1, **kwargs):
        """ Generic index for proposals and own proposals
        Search params are:

        search_name, search_industries, search_expertises,
        search_country, search_location
        """
        Proposal = request.env['project.proposal']
        domain = self._get_domain(filters, **kwargs)
        proposal_count = Proposal.search_count(domain)

        sorting = 'website_published DESC, create_date DESC'

        if filters == 'all':
            url = '/market'
        elif filters == 'my':
            url = '/my/proposals'
        url_args = self._get_url_args(filters, **kwargs)

        pager = request.website.pager(url=url, total=proposal_count, page=page,
                                      step=self._proposal_per_page,
                                      scope=self._proposal_per_page,
                                      url_args=url_args)

        detail_url = "/proposals/detail/%s"
        detail_url = "%s?%s" % (detail_url, werkzeug.url_encode(url_args))

        proposals = Proposal.search(
            domain, limit=self._proposal_per_page, offset=pager['offset'],
            order=sorting
        )
        Industry = request.env['res.partner.category']
        Expertise = request.env['expertise']
        industries = None
        industry_ids = None
        expertises = None
        if kwargs.get('search_industries'):
            industry_ids = kwargs['search_industries'].split(',')
            industry_ids = [int(i) for i in industry_ids]
            industries = Industry.browse(industry_ids).read(['name'])
            industries = json.dumps(industries)
        if kwargs.get('search_expertises'):
            expertise_ids = kwargs['search_expertises'].split(',')
            expertise_ids = [int(i) for i in expertise_ids]
            expertises = Expertise.browse(expertise_ids).read(['name'])
            expertises = json.dumps(expertises)
        countries = request.env['res.country'].sudo().search([])
        selected_country_id = kwargs.get('search_country')
        if selected_country_id and selected_country_id.isdigit():
            selected_country_id = int(selected_country_id)
        values = {
            'proposals': proposals,
            'my': filters == 'my',
            'pager': pager,
            'industries': industries,
            'industry_ids': industry_ids,
            'expertises': expertises,
            'selected_country_id': selected_country_id,
            'countries': countries,
            'url': url,
            'detail_url': detail_url,
        }
        values.update(url_args)
        # Render page
        return request.website.render(
            "specific_project_proposal.proposal_index", values)

    @http.route([
        '/market',
        '/market/page/<int:page>',
        ], type='http', auth="public", website=True)
    def proposals(self, **kwargs):
        # List of proposals available to current UID
        return self.proposal_index(filters='all', **kwargs)

    @http.route([
        '/my/proposals',
        '/my/proposals/page/<int:page>',
        ], type='http', auth="user", website=True)
    def my_proposals(self, **kwargs):
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
        type='http', auth="user", website=True)
    def delete_confirm(self, proposal, **kwargs):
        return request.render(
            "specific_project_proposal.proposal_delete_confirm", {
                'proposal': proposal,
                'main_object': proposal,
            })

    @http.route(
        '/proposals/proposal/<model("project.proposal"):proposal>/delete',
        type='http', auth="user", website=True)
    def delete(self, proposal, **kwargs):
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
        base_link = '/proposals/%s/%%s' % slug(proposal)
        base_link = self._url_with_args(base_link, filters, **kwargs)
        previous_link = base_link % "previous"
        next_link = base_link % "next"
        return request.render("specific_project_proposal.proposal_detail", {
            'proposal': proposal,
            'main_object': proposal,
            'filters': filters,
            'previous_link': previous_link,
            'next_link': next_link,
            'return_link': self._url_with_args(return_link, None, **kwargs)
        })

    @http.route(['/proposals/<model("project.proposal"):proposal>/previous'],
                type='http', auth="public", website=True)
    def proposal_previous(self, proposal, filters='all', **kwargs):
        domain = self._get_domain(filters, **kwargs)
        Proposal = request.env['project.proposal']
        proposals = Proposal.search(
            domain, order='website_published DESC, create_date DESC',
        )
        index = proposals.ids.index(proposal.id)
        previous_proposal = proposals[index - 1]
        url = "/proposals/detail/%s" % (slug(previous_proposal))
        return request.redirect(self._url_with_args(url, filters, **kwargs))

    @http.route(['/proposals/<model("project.proposal"):proposal>/next'],
                type='http', auth="public", website=True)
    def proposal_next(self, proposal, filters='all', **kwargs):
        domain = self._get_domain(filters, **kwargs)
        Proposal = request.env['project.proposal']
        proposals = Proposal.search(
            domain, order='website_published DESC, create_date DESC',
        )
        index = proposals.ids.index(proposal.id)
        next_proposal = proposals[(index + 1) % len(proposals)]
        url = "/proposals/detail/%s" % (slug(next_proposal))
        return request.redirect(self._url_with_args(url, filters, **kwargs))

    @http.route(['/my/proposals/edit/<model("project.proposal"):proposal>'],
                type='http', auth="user", website=True)
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

        expertises = [
            dict(id=expertise.id, name=expertise.name)
            for expertise in proposal.expertise_ids]
        expertises = json.dumps(expertises)
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

        mandatory_fields = [
            'name', 'website_short_description',
            'website_description', 'post_industries', 'post_expertises']
        optional_fields = [
            'location', 'country_id',
            'start_date', 'stop_date']

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
