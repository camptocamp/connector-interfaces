# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _
from openerp import api, fields, models

from openerp.addons.website_portal.controllers.main import website_account

class website_account(http.Controller):
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
            # 'redirect': redirect,
        })
        return request.website.render("specific_membership.membership_payment_address", values)

    @http.route(['/my/membership/buy'], type='http', auth="user", website=True)
    def confirm_asso_member(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        partner.sudo().buttonBuyMembership()

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

        return request.website.render("specific_membership.membership_payment_address", values)

