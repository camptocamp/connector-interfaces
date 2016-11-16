# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http, _
from openerp import fields
from openerp.http import request
from openerp.addons.website_membership.controllers.main import (
    WebsiteMembership as WebsiteMembershipController
)
import json
import werkzeug

# TODO Faire liste des routes nécessaires

# /home                     => members aggreagation
# /members                  => members_list_view
# /members/companyname      => meber_detail_view


class WebsiteMembership(WebsiteMembershipController):
    _references_per_page = 10

    @http.route(['/my/membership'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }
        product = request.env['product.product'].sudo().search([
            ('default_code', '=', 'associate')])

        values.update({
            'partner': partner,
            'product': product,
        })
        return request.website.render(
            "specific_membership.membership_payment_address", values)

    @http.route(['/my/membership/buy'], type='http', auth="user", website=True)
    def confirm_asso_member(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        partner.sudo().button_buy_membership()

        values = {
            'error': {},
            'error_message': []
        }

        product = request.env['product.product'].sudo().search([
            ('default_code', '=', 'associate')])

        values.update({
            'partner': partner,
            'product': product,
        })

        return request.website.render(
            "specific_membership.membership_payment_confirmation", values)

    @http.route(['/my/tiles'], type='http', auth="user", website=True)
    def tiles_member(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }
        product = request.env['product.product'].sudo().search([
            ('default_code', '=', 'associate')])

        values.update({
            'partner': partner,
            'product': product,
            # 'redirect': redirect,
        })
        return request.website.render(
            "specific_membership.member_tile", values)

    def _get_domain(self, search_industries='', search_expertises='',
                    search_country='', **kwargs):
        domain = []
        if search_industries:
            industry_ids = search_industries.split(',')
            domain.append(('category_id', 'in', industry_ids))
        if search_expertises:
            expertise_ids = search_expertises.split(',')
            domain.append(('expertise_ids', 'in', expertise_ids))
        if search_country and search_country.isdigit():
            domain.append(('country_id', '=', int(search_country)))
        return domain

    # FIXME: this method is waaaaay too long! Split it!
    @http.route([], type='http', auth="public", website=True)
    def members(self, membership_id=None, country_name=None,
                country_id=0, page=1, **post):
        """ Overwrite completely the method as we have no hook in it
        Here we define the search on expertise and industries
        """
        env = request.env
        # TODO: we should have proper permissions here instead of useing sudo!
        membership_line_obj = env['membership.membership_line'].sudo()
        partner_obj = env['res.partner'].sudo()
        post_name = post.get('search') or post.get('name', '')
        today = fields.Date.today()

        # base domain for groupby / searches
        base_line_domain = [
            ("partner.website_published", "=", True), ('state', '=', 'paid'),
            ('date_to', '>=', today), ('date_from', '<=', today)
        ]

        membership = None
        if post_name:
            base_line_domain += [
                '|', ('partner.name', 'ilike', post_name),
                ('partner.website_description', 'ilike', post_name)
            ]

        # group by country, based on all customers (base domain)
        membership_lines = membership_line_obj.search(base_line_domain)
        country_domain = [
            '|', ('member_lines', 'in', membership_lines.ids),
            ('membership_state', 'in', ('free', 'asso')),
        ]

        if post_name:
            country_domain += ['|', ('name', 'ilike', post_name),
                               ('website_description', 'ilike', post_name)]
        print 'COUNTRY DOMAIN' + ('*' * 100)
        print country_domain
        countries = partner_obj.read_group(
            country_domain + [("website_published", "=", True)],
            ["id", "country_id"],  # noqa
            groupby="country_id", orderby="country_id")

        countries.insert(0, {
            'country_id': (0, _("All Countries"))
        })

        limit = self._references_per_page
        offset = limit * (page - 1)

        search_domain = [
            ('membership_state', 'in', ('free', 'asso')),
            ('website_published', '=', True)
        ]
        if post_name:
            search_domain += [
                '|',
                ('name', 'ilike', post_name),
                ('website_description', 'ilike', post_name)
            ]

        # add search by industries and expertises
        domain = self._get_domain(**post)
        search_domain += domain
        # TODO: we should have proper permissions here instead of useing sudo!
        Industry = env['res.partner.category'].sudo()
        Expertise = env['partner.project.expertise'].sudo()
        industries = None
        industry_ids = None
        expertises = None
        if post.get('search_industries'):
            industry_ids = post['search_industries'].split(',')
            industry_ids = [int(i) for i in industry_ids]
            industries = [
                dict(id=category.id, name=category.display_name)
                for category in Industry.browse(industry_ids)]
            industries = json.dumps(industries)
        if post.get('search_expertises'):
            expertise_ids = post['search_expertises'].split(',')
            expertise_ids = [int(i) for i in expertise_ids]
            expertises = Expertise.browse(expertise_ids).read(['name'])
            expertises = json.dumps(expertises)

        print 'SEARCH DOMAIN' + ('*' * 100)
        print search_domain
        partners = partner_obj.search(
            search_domain,
            offset=offset,
            limit=limit,
        )
        total_members = partner_obj.search_count(search_domain)
        base_url = '/members/'
        # looks like we are not using these at all
        # base_url = '/members%s%s' % (
        #     '/association/%s' % membership_id if membership_id else '',
        #     '/country/%s' % country_id if country_id else '',
        # )

        # request pager for lines
        pager = request.website.pager(
            url=base_url, total=total_members, page=page,
            step=limit, scope=7, url_args=post)

        values = {
            'partners': partners,
            'membership': membership,
            'memberships_partners': partners,
            'membership_id': membership_id,
            'countries': countries,
            'pager': pager,
            'post': post,
            'search': "?%s" % werkzeug.url_encode(post),
            # custom
            'industries': industries,
            'industry_ids': industry_ids,
            'expertises': expertises,
            'selected_country_id': int(post.get('search_country', 0)),
        }
        return request.website.render("website_membership.index", values)
