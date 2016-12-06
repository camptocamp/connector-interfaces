# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json
import werkzeug.urls

from openerp import _, http
from openerp.http import request

# from openerp.addons.website.models.website import slug

# TODO: we should really cleanup this mess and merge
# the code for listing and search between references and proposals
# having a base common class for every listing/search


class WebsiteReference(http.Controller):
    _reference_per_page = 10

    def _get_domain(self, filters='all', search_name='', search_industries='',
                    search_expertises='', search_country='', search_location=''
                    ):
        domain = []
        industry_ids = None
        if filters == 'my':
            domain = [('create_uid', '=', request.env.user.id)]
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

    def reference_listing(self, filters='all', page=1, **kwargs):
        """ Generic index for references and own references
        Search params are:

        search_name, search_industries, search_expertises,
        search_country, search_location
        """
        Reference = request.env['project.reference']
        # make debug feasible!
        kwargs.pop('debug', None)
        domain = self._get_domain(filters, **kwargs)
        reference_count = Reference.search_count(domain)

        sorting = 'website_published DESC, create_date DESC'

        if filters == 'all':
            url = '/references'
        elif filters == 'my':
            url = '/my/references'
        url_args = self._get_url_args(filters, **kwargs)

        pager = request.website.pager(url=url, total=reference_count,
                                      page=page,
                                      step=self._reference_per_page,
                                      scope=self._reference_per_page,
                                      url_args=url_args)

        detail_url = "%s/{}?%s" % (url, werkzeug.url_encode(url_args))
        references = Reference.search(
            domain, limit=self._reference_per_page, offset=pager['offset'],
            order=sorting
        )
        Industry = request.env['res.partner.category']
        Expertise = request.env['partner.project.expertise']
        industries = None
        industry_ids = None
        expertises = None
        if kwargs.get('search_industries'):
            industry_ids = kwargs['search_industries'].split(',')
            industry_ids = [int(i) for i in industry_ids]
            industries = [
                dict(id=category.id, name=category.display_name)
                for category in Industry.browse(industry_ids)]
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
            'references': references,
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
            "specific_project.reference_listing", values)

    @http.route([
        '/my/references',
        '/my/references/page/<int:page>',
    ], type='http', auth="user", website=True)
    def my_references(self, **kwargs):
        return self.reference_listing(filters='my', **kwargs)

    @http.route([
        '/references',
        '/references/page/<int:page>',
    ], type='http', auth="user", website=True)
    def references(self, **kwargs):
        return self.reference_listing(filters='all', **kwargs)

    @http.route(
        '/references/<model("project.reference"):reference>/'
        'delete_confirm',
        type='http', auth="user", website=True)
    def delete_confirm(self, reference, **kwargs):
        return request.render(
            "specific_project.reference_delete_confirm", {
                'reference': reference,
                'main_object': reference,
            })

    @http.route(
        '/references/<model("project.reference"):reference>/delete',
        type='http', auth="user", website=True)
    def delete(self, reference, **kwargs):
        reference.unlink()
        return request.redirect('/my/home')

    @http.route(
        ['/references/<model("project.reference"):reference>/previous'],
        type='http', auth="public", website=True)
    def reference_previous(self, reference, filters='all', **kwargs):
        domain = self._get_domain(filters, **kwargs)
        Reference = request.env['project.reference']
        references = Reference.search(
            domain, order='website_published DESC, create_date DESC',
        )
        index = references.ids.index(reference.id)
        previous_reference = references[index - 1]
        url = previous_reference.website_url
        return request.redirect(self._url_with_args(url, filters, **kwargs))

    @http.route(['/references/<model("project.reference"):reference>/next'],
                type='http', auth="public", website=True)
    def reference_next(self, reference, filters='all', **kwargs):
        domain = self._get_domain(filters, **kwargs)
        Reference = request.env['project.reference']
        references = Reference.search(
            domain, order='website_published DESC, create_date DESC',
        )
        index = references.ids.index(reference.id)
        next_reference = references[(index + 1) % len(references)]
        url = next_reference.website_url
        return request.redirect(self._url_with_args(url, filters, **kwargs))
