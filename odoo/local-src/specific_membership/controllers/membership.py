# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_membership.controllers.main import (
    WebsiteMembership as WebsiteMembershipController
)
from openerp.addons.website.models.website import unslug


from openerp.addons.cms_form.controllers.main import SearchFormControllerMixin


class WebsiteMembership(WebsiteMembershipController,
                        SearchFormControllerMixin):

    @http.route([
        '/members',
        '/members/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'res.partner'
        return self.make_response(model, **kw)

    @http.route()
    def partners_detail(self, partner_id, **post):
        _, partner_id = unslug(partner_id)
        if partner_id:
            partner = request.registry['res.partner'].browse(
                request.cr, SUPERUSER_ID, partner_id, context=request.context)
            if partner.exists() and partner.website_published:
                values = {}
                values['main_object'] = values['partner'] = partner
                # FIXME: this is super-weird
                # a partner HAS NO USER associated
                # while the user HAS A PARTNER associated
                partner_user = request.env['res.users'].sudo().search(
                    [('partner_id', '=', partner.id)],
                    limit=1
                )
                values['partner_user'] = partner_user
                return request.website.render(
                    "website_membership.partner", values)
        return request.redirect('/members', code=302)

    @http.route(['/my/membership'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        if not request.session.uid:
            return request.not_found()
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }
        product = request.env['product.product'].sudo().search([
            ('default_code', '=', 'associate')])
        total_price = product.list_price
        tax_amount = 0
        if product.taxes_id:
            tax_amount = product.list_price * (
                product.taxes_id[0].amount / 100)
            total_price += tax_amount
        values.update({
            'partner': partner,
            'product': product,
            'total_price': total_price,
            'tax_amount': tax_amount,
        })
        return request.website.render(
            "specific_membership.membership_payment_address", values)

    @http.route(['/my/membership/buy'],
                type='http', auth="user", website=True, methods=['POST'])
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
