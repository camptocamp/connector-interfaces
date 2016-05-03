# -*- coding: utf-8 -*-
import json
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.website_portal.controllers.main import website_account

class website_account(website_account):
    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        if redirect:
            redirect = redirect
        else:
            redirect = ('/my/profile_success')
        response = super(website_account, self).details(redirect, **post)
        categories = request.env['res.partner.category'].sudo().search([])
        areas = request.env['res.partner.area'].sudo().search([])
        category_test = [dict(id=category.id, name=category.name) for category in categories]
        category_test = json.dumps(category_test)
        response.qcontext.update({
            'categories': category_test,
            'areas': areas,
        })
        # FIXME: Workaround for problem with saving of fields website. If required
        # fields are not set, website will be taken out of response dictionary
        # in order to avoid server errors
        if 'website' in response.qcontext:
            del response.qcontext['website']
        # if 'image_medium' in post:
        #     partner = request.env['res.users'].browse(request.uid).partner_id
        #     partner.sudo().write({'partner.image_medium':post['partner.image_medium']})
        if post:
            partner = request.env['res.users'].browse(request.uid).partner_id
            if post['post_categories']:
                categ_ids = post['post_categories'].split(',')
                partner.sudo().write({'category_id':[(4, int(category_id)) for category_id in categ_ids]})
            if post['post_areas']:
                area_ids = post['post_areas'].split(',')
                partner.sudo().write({'area_ids':[(4, int(area_id)) for area_id in area_ids]})
        return response

    @http.route('/my/get_areas', type='http', auth="user", methods=['GET'], website=True)
    def area_read(self, q='', l=25, **post):
        data = request.env['res.partner.area'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route('/my/get_categories', type='http', auth="user", methods=['GET'], website=True)
    def categories_read(self, q='', l=25, **post):
        data = request.env['res.partner.category'].search_read(
            domain=[('name', '=ilike', (q or '') + "%")],
            fields=['id', 'name'],
            limit=int(l),
        )
        return json.dumps(data)

    @http.route('/my/profile_success', type='http', auth='user', website=True)
    def profile_success(self, *args, **kw):
        return request.render('website_portal_profile.profile_success', {})
