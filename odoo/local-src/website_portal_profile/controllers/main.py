# -*- coding: utf-8 -*-
import json
import base64
from openerp import http
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
            redirect = ('/my/profile_success')
        response = super(website_account, self).details(redirect, **post)

        categories = [
            dict(id=category.id, name=category.name)
            for category in partner.category_id]
        categories = json.dumps(categories)

        expertise = [
            dict(id=expertise.id, name=expertise.name)
            for expertise in partner.expertise_ids]
        expertises = json.dumps(expertise)

        response.qcontext.update({
            'categories': categories,
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
        error = dict()
        error_message = []

        mandatory_billing_fields = [
            "name",
            "phone",
            "email",
            "street2",
            "city",
            "country_id"]
        optional_billing_fields = ["zipcode", "state_id", "vat", "street"]
        additional_fields = [
            'uimage',
            'website',
            'twitter',
            'facebook',
            'skype',
            'website_short_description',
            'post_expertises',
            'post_categories']

        error, error_message = super(
            website_account, self).details_form_validate(data)

        # clear previous unknown field error
        if 'common' in error:
            error.pop('common')
        for item in error_message:
            if 'Unknown field' in item:
                error_message.remove(item)

        unknown = [
            k for k in data.iterkeys() if k not in
            mandatory_billing_fields
            + optional_billing_fields
            + additional_fields]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    @http.route(
        ['/my/get_expertises'],
        type='http',
        auth="user",
        methods=['GET'],
        website=True)
    def expertise_read(self, q='', l=25, **post):
        data = request.env['partner_project_expertise.expertise'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route(
        ['/my/get_categories'],
        type='http',
        auth="user",
        methods=['GET'],
        website=True)
    def categories_read(self, q='', l=25, **post):
        data = request.env['res.partner.category'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
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
