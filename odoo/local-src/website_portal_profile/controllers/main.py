# -*- coding: utf-8 -*-
import base64
import json
import time
import werkzeug.urls

from openerp import _, http, tools, SUPERUSER_ID
from openerp.http import request
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

from openerp.addons.website_portal.controllers.main import website_account
from openerp.addons.website_membership.controllers.main import (
    WebsiteMembership as WebsiteMembershipController
)


class website_account(website_account):

    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        vals = {}
        partner = request.env['res.users'].browse(request.uid).partner_id
        if redirect:
            redirect = redirect
        else:
            redirect = ('/my/home')
        response = super(website_account, self).details(redirect, **post)

        # FIXME: Workaround for problem with saving of fields website.
        # If required fields are not set, website will be taken out of
        # response dictionary in order to avoid server errors.
        if 'website' in response.qcontext:
            del response.qcontext['website']

        industry_ids = []
        expertise_ids = []

        if post:
            country_id = post['country_id']
            if country_id and country_id.isdigit():
                vals.update({'country_id': int(country_id)})
            if post['post_categories']:
                industry_ids = post['post_categories'].split(',')
                industry_ids = [int(rec_id) for rec_id in industry_ids]
                vals['category_id'] = [(6, None, industry_ids)]
            if post['post_expertises']:
                expertise_ids = post['post_expertises'].split(',')
                expertise_ids = [int(rec_id) for rec_id in expertise_ids]
                vals['expertise_ids'] = [(6, None, expertise_ids)]
            if post['uimage']:
                vals['image'] = base64.encodestring(post['uimage'].read())
            response.qcontext.update(vals)
            if 'error' not in response.qcontext:
                vals['website'] = post['website_url']
                partner.sudo().write(vals)

        if industry_ids:
            Industry = request.env['res.partner.category']
            industries = Industry.browse(industry_ids)
        else:
            industries = partner.category_id
        industries = [dict(id=category.id, name=category.display_name)
                      for category in industries]
        industries = json.dumps(industries)

        if expertise_ids:
            Expertise = request.env['partner.project.expertise']
            expertises = Expertise.browse(expertise_ids)
        else:
            expertises = partner.expertise_ids
        expertises = json.dumps(expertises.read(['name']))

        response.qcontext.update(categories=industries, expertises=expertises)
        return response

    def details_form_validate(self, data):
        """ Overwrite checks """
        error = dict()
        error_message = []

        mandatory_fields = ["name", "street2", "zipcode", "city", "country_id",
                            "phone", "email"]
        optional_fields = ["state_id", "vat", "street"]
        additional_fields = ['uimage', 'website_url', 'twitter', 'facebook',
                             'skype', 'website_short_description',
                             'post_expertises', 'post_categories']

        missing = False
        # Validation
        for field_name in mandatory_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'
                missing = True

        # error message for empty required fields
        if missing:
            error_message.append(_('Some required fields are empty.'))

        # email validation
        if data.get('email') and not tools.single_email_re.match(
                data.get('email')):
            error["email"] = 'error'
            error_message.append(
                _('Invalid Email! Please enter a valid email address.'))

        # vat validation
        if data.get("vat") and hasattr(request.env["res.partner"],
                                       "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = request.env["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = request.env["res.partner"].simple_vat_check
            vat_country, vat_number = request.env["res.partner"]._split_vat(
                data.get("vat"))
            if not check_func(vat_country, vat_number):  # simple_vat_check
                error["vat"] = 'error'

        unknown = [
            k for k in data.iterkeys() if k not in
            mandatory_fields
            + optional_fields
            + additional_fields]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    @http.route(
        ['/my/get_expertises'],
        type='http',
        auth="public",
        methods=['GET'],
        website=True)
    def expertise_read(self, q='', l=25, **post):
        data = request.env['partner.project.expertise'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route(
        ['/my/get_categories'],
        type='http',
        auth="public",
        methods=['GET'],
        website=True)
    def categories_read(self, q='', l=25, **post):
        data = request.env['res.partner.category'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'display_name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route(
        ['/my/profile_success'],
        type='http',
        auth='user',
        website=True)
    def profile_success(self, *args, **kw):
        return request.render('website_portal_profile.profile_success', {})


class WebsiteMembership(WebsiteMembershipController):

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

    @http.route([], type='http', auth="public", website=True)
    def members(self, membership_id=None, country_name=None, country_id=0,
                page=1, **post):
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
