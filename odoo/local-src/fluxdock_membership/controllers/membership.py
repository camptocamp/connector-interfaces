# Copyright 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
from odoo.addons.website_membership.controllers.main import (
    WebsiteMembership as WebsiteMembershipController
)
from odoo.addons.http_routing.models.ir_http import unslug

from odoo.addons.cms_form.controllers.main import SearchFormControllerMixin


class WebsiteMembership(WebsiteMembershipController,
                        SearchFormControllerMixin):

    @http.route([
        '/members',
        '/members/page/<int:page>',
    ], type='http', auth="public", website=True)
    def market(self, **kw):
        model = 'res.partner'
        return self.make_response(model, **kw)

    def _get_partner_user(self, pid):
        # FIXME: this is super-weird
        # a partner HAS NO USER associated
        # while the user HAS A PARTNER associated
        partner_user = request.env['res.users'].sudo().search(
            [('partner_id', '=', pid)],
            limit=1
        )
        return partner_user

    def _partner_is_visible(self, partner, raise_exception=False):
        try:
            partner.check_access_rights('read')
            partner.check_access_rule('read')
            can = True
        except Exception:
            if raise_exception:
                raise
            can = False
        return can

    @http.route()
    def partners_detail(self, partner_id, **post):
        _, partner_id = unslug(partner_id)
        if partner_id:
            partner = request.env['res.partner'].browse(partner_id)
            if partner and partner.exists() \
                    and self._partner_is_visible(partner):
                values = {}
                values['main_object'] = values['partner'] = partner
                values['partner_user'] = self._get_partner_user(partner.id)
                return request.website.render(
                    "website_membership.partner", values)
        return request.redirect('/members', code=302)

    # TODO: drop this stuff as we drop membership upgrades

    @http.route(['/my/membership'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        if not request.session.uid:
            return request.not_found()
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': [],
            'partner': partner,
        }
        values.update(partner.get_membership_cost())
        return request.website.render(
            "fluxdock_membership.membership_payment_address", values)

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
            "fluxdock_membership.membership_payment_confirmation", values)
