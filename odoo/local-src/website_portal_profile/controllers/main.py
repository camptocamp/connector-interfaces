# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.website_portal.controllers.main import website_account

class website_account(website_account):
    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        response = super(website_account, self).details()
        categories = request.env['res.partner.category'].sudo().search([])
        areas = request.env['res.partner.area'].sudo().search([])
        response.qcontext.update({
            'categories': categories,
            'areas': areas,
        })
        return response
