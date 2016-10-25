# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http, _
from openerp import SUPERUSER_ID
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from openerp.http import request
from openerp.addons.website_membership.controllers.main import (
    WebsiteMembership as WebsiteMembershipController
)
import time
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

        # For tiles view
        partners = request.env['res.users'].sudo().search([
            ('flux_membership', '=', 'asso')])

        values.update({
            'partner': partner,
            'product': product,
            'partners': partners,
            # 'redirect': redirect,
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
        cr, uid, context = request.cr, request.uid, request.context
        product_obj = request.registry['product.product']
        country_obj = request.registry['res.country']
        membership_line_obj = request.registry['membership.membership_line']
        partner_obj = request.registry['res.partner']
        post_name = post.get('search') or post.get('name', '')
        current_country = None
        today = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        # base domain for groupby / searches
        base_line_domain = [
            ("partner.website_published", "=", True), ('state', '=', 'paid'),
            ('date_to', '>=', today), ('date_from', '<=', today)
        ]
        if membership_id and membership_id != 'free':
            membership_id = int(membership_id)
            base_line_domain.append(('membership_id', '=', membership_id))
            membership = product_obj.browse(cr, uid, membership_id, context=context)  # noqa
        else:
            membership = None
        if post_name:
            base_line_domain += ['|', ('partner.name', 'ilike', post_name),
                                      ('partner.website_description', 'ilike', post_name)]  # noqa

        # group by country, based on all customers (base domain)
        if membership_id != 'free':
            membership_line_ids = membership_line_obj.search(cr, SUPERUSER_ID, base_line_domain, context=context)  # noqa
            country_domain = [('member_lines', 'in', membership_line_ids)]
            if not membership_id:
                country_domain = ['|', country_domain[0], ('membership_state', '=', 'free')]  # noqa
        else:
            membership_line_ids = []
            country_domain = [('membership_state', '=', 'free')]
        if post_name:
            country_domain += ['|', ('name', 'ilike', post_name),
                               ('website_description', 'ilike', post_name)]
        countries = partner_obj.read_group(
            cr, SUPERUSER_ID, country_domain + [("website_published", "=", True)], ["id", "country_id"],  # noqa
            groupby="country_id", orderby="country_id", context=request.context)  # noqa
        countries_total = sum(country_dict['country_id_count'] for country_dict in countries)  # noqa

        line_domain = list(base_line_domain)
        if country_id:
            line_domain.append(('partner.country_id', '=', country_id))
            current_country = country_obj.read(cr, uid, country_id, ['id', 'name'], context)  # noqa
            if not any(x['country_id'][0] == country_id for x in countries if x['country_id']):  # noqa
                countries.append({
                    'country_id_count': 0,
                    'country_id': (country_id, current_country["name"])
                })
                countries = filter(lambda d: d['country_id'], countries)
                countries.sort(key=lambda d: d['country_id'][1])

        countries.insert(0, {
            'country_id_count': countries_total,
            'country_id': (0, _("All Countries"))
        })

        # format domain for group_by and memberships
        membership_ids = product_obj.search(cr, uid, [('membership', '=', True)], order="website_sequence", context=context)  # noqa
        memberships = product_obj.browse(cr, uid, membership_ids, context=context)  # noqa
        # make sure we don't access to lines with unpublished membershipts
        line_domain.append(('membership_id', 'in', membership_ids))

        limit = self._references_per_page
        offset = limit * (page - 1)

        count_members = 0
        membership_line_ids = []
        # displayed non-free membership lines
        if membership_id != 'free':
            count_members = membership_line_obj.search_count(cr, SUPERUSER_ID, line_domain, context=context)  # noqa
            if offset <= count_members:
                membership_line_ids = tuple(membership_line_obj.search(cr, SUPERUSER_ID, line_domain, offset, limit, context=context))  # noqa
        membership_lines = membership_line_obj.browse(cr, uid, membership_line_ids, context=context)  # noqa
        # TODO: Following line can be deleted in master. Kept for retrocompatibility.  # noqa
        membership_lines = sorted(membership_lines, key=lambda x: x.membership_id.website_sequence)  # noqa
        page_partner_ids = set(m.partner.id for m in membership_lines)

        google_map_partner_ids = []
        if request.env.ref('website_membership.opt_index_google_map').customize_show:  # noqa
            # ----- FIX ----
            membership_line_ids = membership_line_obj.search(cr, uid, line_domain, context=context)  # noqa
            # ----- END of FIX ----
            google_map_partner_ids = membership_line_obj.get_published_companies(cr, uid, membership_line_ids, limit=2000, context=context)  # noqa

        search_domain = [('membership_state', '=', 'free'), ('website_published', '=', True)]  # noqa
        if post_name:
            search_domain += ['|', ('name', 'ilike', post_name), ('website_description', 'ilike', post_name)]  # noqa

        # ------------ Start change 1/2 ---------------
        domain = self._get_domain(**post)

        search_domain += domain

        Industry = request.env['res.partner.category']
        Expertise = request.env['partner.project.expertise']
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

        selected_country_id = post.get('search_country')
        if selected_country_id and selected_country_id.isdigit():
            selected_country_id = int(selected_country_id)
        # ----------- End of change 1/2 -----------------

        if country_id:
            search_domain += [('country_id', '=', country_id)]
        free_partner_ids = partner_obj.search(cr, SUPERUSER_ID, search_domain, context=context)  # noqa
        memberships_data = []
        for membership_record in memberships:
            memberships_data.append({'id': membership_record.id, 'name': membership_record.name})  # noqa
        memberships_partner_ids = {}
        for line in membership_lines:
            memberships_partner_ids.setdefault(line.membership_id.id, []).append(line.partner.id)  # noqa
        if free_partner_ids:
            memberships_data.append({'id': 'free', 'name': _('Free Members')})
            if not membership_id or membership_id == 'free':
                if count_members < offset + limit:
                    free_start = max(offset - count_members, 0)
                    free_end = max(offset + limit - count_members, 0)
                    memberships_partner_ids['free'] = free_partner_ids[free_start:free_end]  # noqa
                    page_partner_ids |= set(memberships_partner_ids['free'])
                google_map_partner_ids += free_partner_ids[:2000-len(google_map_partner_ids)]  # noqa
                count_members += len(free_partner_ids)

        google_map_partner_ids = ",".join(map(str, google_map_partner_ids))

        partners = {p.id: p for p in partner_obj.browse(request.cr, SUPERUSER_ID, list(page_partner_ids), request.context)}  # noqa

        base_url = '/members%s%s' % ('/association/%s' % membership_id if membership_id else '',  # noqa
                                     '/country/%s' % country_id if country_id else '')  # noqa

        # request pager for lines
        pager = request.website.pager(url=base_url, total=count_members, page=page, step=limit, scope=7, url_args=post)  # noqa

        values = {
            'partners': partners,
            'membership_lines': membership_lines,  # TODO: This line can be deleted in master. Kept for retrocompatibility.  # noqa
            'memberships': memberships,  # TODO: This line too.
            'membership': membership,  # TODO: This line too.
            'memberships_data': memberships_data,
            'memberships_partner_ids': memberships_partner_ids,
            'membership_id': membership_id,
        # ------------ Start change 2/2 ---------------
            'industries': industries,
            'industry_ids': industry_ids,
            'expertises': expertises,
            'selected_country_id': selected_country_id,
        # ------------ End change 2/2 -----------------
            'countries': countries,
            'current_country': current_country and [current_country['id'], current_country['name']] or None,  # noqa
            'current_country_id': current_country and current_country['id'] or 0,  # noqa
            'google_map_partner_ids': google_map_partner_ids,
            'pager': pager,
            'post': post,
            'search': "?%s" % werkzeug.url_encode(post),
        }
        return request.website.render("website_membership.index", values)
