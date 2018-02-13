# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.addons.website_partner.controllers.main import WebsitePartnerPage
from odoo.http import request


class PartnerDetail(WebsitePartnerPage):

    detail_template = 'fluxdock_membership.partner_detail'

    def _get_partner_user(self, pid):
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

    # Do not use semantic controller due to SUPERUSER_ID
    @http.route([
        '/dock/partners/<partner_id>'
    ], type='http', auth="public", website=True)
    def partner_detail(self, partner_id, **post):
        _, partner_id = unslug(partner_id)
        partner_model = request.env['res.partner']
        if partner_id:
            partner = partner_model.browse(partner_id)
            if partner and partner.exists() \
                    and self._partner_is_visible(partner):
                values = {}
                values['main_object'] = values['partner'] = partner
                values['partner_user'] = self._get_partner_user(partner.id)
                return request.render(self.detail_template, values)
        return request.redirect(partner_model.cms_search_url, code=302)

    @http.route()
    def partners_detail(self, partner_id, **post):
        # Original method from `WebsitePartnerPage`
        # permanent redirect to `/dock/` url
        partner_model = request.env['res.partner']
        return request.redirect(
            partner_model.cms_search_url + partner_id, code=301)
