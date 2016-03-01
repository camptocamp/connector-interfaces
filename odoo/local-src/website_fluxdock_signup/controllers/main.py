# -*- coding: utf-8 -*-
import openerp
import logging
import werkzeug

from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

from openerp.addons.website_portal.controllers.main import website_account
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.auth_signup.res_users import res_users
from openerp.addons.web.controllers.main import ensure_db


class AuthSignupHome(openerp.addons.web.controllers.main.Home):

    @http.route('/web/presignup', type='http', auth='public', website=True)
    def website_fluxdock_presignup(self, *args, **kw):
        return request.render('website_fluxdock_signup.presignup', {})

    # TODO: Weiterleitung auf Profil vervollständigen
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        response = super(AuthSignupHome, self).web_auth_signup()
        countries = request.env['res.country'].sudo().search([])
        cr, uid, context = request.cr, request.uid, request.context
        mail_template = request.registry['mail.template']
        response.qcontext.update({
            'countries': countries,
        })
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                mail_template.send_mail(cr, SUPERUSER_ID, 6, 9, force_send=True, raise_exception=True, context=None)
                return request.render('website_fluxdock_signup.thanks_for_registration', {})
            except (SignupError, AssertionError), e:
                qcontext['error'] = _(e.message)
        else:
            return response
