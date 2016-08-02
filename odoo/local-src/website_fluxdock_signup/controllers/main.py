# -*- coding: utf-8 -*-
import openerp
import logging
import werkzeug

from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

from openerp.addons.auth_signup.res_users import SignupError

_logger = logging.getLogger(__name__)


class AuthSignupHome(openerp.addons.web.controllers.main.Home):

    @http.route('/web/presignup', type='http', auth='public', website=True)
    def website_fluxdock_presignup(self, *args, **kw):
        return request.render('website_fluxdock_signup.presignup', {})

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        response = super(AuthSignupHome, self).web_auth_signup()
        countries = request.env['res.country'].sudo().search([])

        response.qcontext.update({
            'countries': countries,
        })

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                cr, uid = request.cr, request.uid
                login = qcontext.get('login')
                res_users = request.registry.get('res.users')
                res_partner = request.env[
                    'res.users'].sudo().browse(uid).partner_id

                res_partner.sudo().write(
                    {'country_id': qcontext['country_id'],
                        'is_company': True, 'free_member':
                        'true'})

                res_users.send_account_confirmation_email(
                    cr,
                    SUPERUSER_ID,
                    login)

                return request.render(
                    'website_fluxdock_signup.thanks_for_registration',
                    {})
            except (SignupError, AssertionError) as e:
                qcontext['error'] = _(e.message)
        else:
            return response

    @http.route('/web/confirmation', type='http', auth='public', website=True)
    def web_auth_account_confirmation(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get(
                'reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext:
            try:
                if qcontext.get('token'):
                    self.do_confirmation(qcontext)
                    return super(AuthSignupHome, self).web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, "No login provided."
                    res_users = request.registry.get('res.users')

                    res_users.send_account_confirmation_email(
                        request.cr,
                        openerp.SUPERUSER_ID,
                        login)

                    qcontext['message'] = _(
                        'An email has been sent for confirming your account')
            except SignupError:
                qcontext['error'] = _('Could not confirm your email')
                _logger.exception('error when confirming account email')
            except Exception as e:
                qcontext['error'] = _(e.message)
        return request.render(
            'website_fluxdock_signup.account_confirmation',
            qcontext)

    def do_confirmation(self, qcontext):
        """ Method that confirms the account """
        values = dict(
            (key, qcontext.get(key))
            for key in('login', 'name', 'password'))

        assert any(
            [k for k in values.values()]), "The form was not properly filled."
        assert values.get('password') == qcontext.get(
            'confirm_password'), "Passwords do not match; please retype them."

        supported_langs = [
            lang
            ['code']
            for lang in request.registry['res.lang'].search_read(
                request.cr, openerp.SUPERUSER_ID, [], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang

        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()

    @http.route('/web/privateperson', type='http', auth='public', website=True)
    def website_fluxdock_privateperson(self, *args, **kw):
        return request.render('website_fluxdock_signup.privateperson', {})
