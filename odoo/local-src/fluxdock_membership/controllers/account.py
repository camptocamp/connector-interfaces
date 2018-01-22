# Copyright 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
# FIXME: website_portal is gone
# from odoo.addons.website_portal.controllers.main import website_account
#
# from odoo.addons.cms_form.controllers.main import FormControllerMixin
#
# import datetime
#
#
# class MyHome(website_account):
#
#     @http.route(['/my', '/my/home'], type='http', auth="public", website=True)
#     def account(self, **kw):
#         response = super(MyHome, self).account(**kw)
#         response.qcontext.update(self._account_extra_qcontext())
#         if 'sales_rep' in response.qcontext:
#             # default website_portal template wants this
#             # but we don't need it
#             response.qcontext['sales_rep'] = None
#
#         partner = response.qcontext['partner']
#         membership_info = partner.get_membership_cost()
#         response.qcontext['membership_info'] = membership_info
#         return response
#
#     def _account_extra_qcontext(self):
#         partner = request.env['res.users'].browse(request.uid).partner_id
#         yesterday = (
#             datetime.datetime.now() - datetime.timedelta(days=1)
#         ).strftime('%Y-%m-%d')
#         show_profile_progress = not partner.profile_completed or \
#             (partner.profile_completed and not
#                 partner.profile_completed_date <= yesterday)
#         return {
#             'partner': partner,
#             'show_profile_progress': show_profile_progress
#         }
#
#
# class MyProfile(website_account, FormControllerMixin):
#
#     @http.route(['/my/account'], type='http', auth="user", website=True)
#     def details(self, **kw):
#         """Handle partner form."""
#         model = 'res.partner'
#         user = request.env['res.users'].browse(request.uid)
#         partner = user.partner_id
#         return self.make_response(
#             model, model_id=partner.id, **kw)
