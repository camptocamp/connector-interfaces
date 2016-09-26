# -*- coding: utf-8 -*-
import json
import base64
from openerp import _, http, tools
from openerp.http import request

from openerp.addons.website_portal.controllers.main import website_account


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

        industries = [
            dict(id=category.id, name=category.display_name)
            for category in partner.category_id]
        industries = json.dumps(industries)

        expertises = partner.expertise_ids.read(['name'])
        expertises = json.dumps(expertises)

        response.qcontext.update({
            'categories': industries,
            'expertises': expertises,
        })

        # FIXME: Workaround for problem with saving of fields website.
        # If required fields are not set, website will be taken out of
        # response dictionary in order to avoid server errors.
        if 'website' in response.qcontext:
            del response.qcontext['website']

        if post:
            if post['post_categories']:
                categ_ids = post['post_categories'].split(',')
                vals.update(
                    {'category_id': [
                        (4, int(category_id)) for category_id in categ_ids]})
            if post['post_expertises']:
                expertise_ids = post[
                    'post_expertises'].split(',')
                vals.update(
                    {'expertise_ids': [
                        (4, int(expertise_id))
                        for expertise_id in expertise_ids]})
            if post['uimage']:
                vals.update(
                    {'image': base64.encodestring(post['uimage'].read())})
            partner.sudo().write(vals)

        return response

    def details_form_validate(self, data):
        """ Overwrite checks """
        error = dict()
        error_message = []

        mandatory_fields = ["name", "street2", "zipcode", "city", "country_id",
                            "phone", "email"]
        optional_fields = ["state_id", "vat", "street"]
        additional_fields = ['uimage', 'website', 'twitter', 'facebook',
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
