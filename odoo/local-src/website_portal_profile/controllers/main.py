# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
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
        # categories = request.env['res.partner.category'].sudo().search([])
        # areas = request.env['res.partner.area'].sudo().search([])
        # response.qcontext.update({
        #     'categories': categories,
        #     'areas': areas,
        # })
        # FIXME: Workaround for problem with saving of fields website. If required
        # fields are not set, website will be taken out of response dictionary
        # in order to avoid server errors
        if 'website' in response.qcontext:
            del response.qcontext['website']
        # if 'partner.image_medium' in post:
        #     partner = request.env['res.users'].browse(request.uid).partner_id
        #     partner.sudo().write({'partner.image_medium':post['partner.image_medium']})
        return response

    @http.route('/my/profile_success', type='http', auth='user', website=True)
    def profile_success(self, *args, **kw):
        return request.render('website_portal_profile.profile_success', {})
