# -*- coding: utf-8 -*-
import logging
import werkzeug
import json

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.auth_signup_verify_email.controllers.main\
    import SignupVerifyEmail
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.web.controllers.main import ensure_db
from openerp.addons.web.controllers.main import db_info

_logger = logging.getLogger(__name__)


class AuthSignupHome(SignupVerifyEmail):

    @http.route('/web/presignup', type='http', auth='public', website=True)
    def website_fluxdock_presignup(self, *args, **kw):
        return request.render('specific_membership.presignup', {})

    @http.route()
    def web_auth_signup(self, *args, **kw):
        """Override to inject countries."""
        response = super(AuthSignupHome, self).web_auth_signup()
        countries = request.env['res.country'].sudo().search([])
        if response and response.qcontext:
            response.qcontext.update({
                'countries': countries,
            })
        return response

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        """Protect backend home.

        Disallow access to backend home if user has no rights for it.
        """
        ensure_db()
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login', 303)
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid

        # check backend permissions
        has_backend_permissions = False
        if request.uid == SUPERUSER_ID:
            has_backend_permissions = True
        else:
            for xmlid in ('base.group_website_designer',):
                if request.env.user.has_group(xmlid):
                    has_backend_permissions = True
                    break

        if not has_backend_permissions:
            # redirect to public homepage
            return http.local_redirect('/my/home',
                                       query=request.params,
                                       keep_hash=True)

        menu_data = request.registry['ir.ui.menu'].load_menus(
            request.cr, request.uid, request.debug, context=request.context)
        return request.render('web.webclient_bootstrap',
                              qcontext={'menu_data': menu_data,
                                        'db_info': json.dumps(db_info())})

    def _get_user_lang(self):
        """Retrieve user language."""
        langs = request.env['res.lang'].search_read([], ['code'])
        supported_langs = [
            lang['code'] for lang in langs
        ]
        lang = 'en_US'
        if request.lang in supported_langs:
            lang = request.lang
        return lang

    def passwordless_signup(self, values):
        """Override to handle country and other values on partner."""
        # normally the lang is computed when you finalize the signup
        # here we need to force it since at this point the user will be created
        # and `auth_signup_verify_email` does not handle this
        # since it does not use `do_signup`.
        # See https://github.com/OCA/server-tools/issues/585
        values['lang'] = self._get_user_lang()
        response = super(AuthSignupHome, self).passwordless_signup(values)
        qcontext = response.qcontext
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                login = qcontext.get('login')
                res_users = request.env['res.users'].sudo()
                user = res_users.search([('login', '=', login)])
                if user:
                    partner = user.partner_id
                    partner.write({
                        'is_company': True,
                        # publish member only after confirm!
                        'website_published': False,
                        'free_member': 'true',
                        # FIXME: make sure partner is attached to its user
                        # sounds like this is no happening ALWAYS
                        # and we really need this for website features.
                        # OTOH the user is always attached to the partner :S
                        'user_id': user.id
                    })
                    qcontext['show_thanks'] = True
                    # return request.render(
                    #     'specific_membership.thanks_for_registration',
                    #     {})
            except (SignupError, AssertionError) as e:
                qcontext['error'] = _(e.message)
        return response


class PrivatePerson(http.Controller):

    @http.route('/web/privateperson', type='http', auth='public', website=True)
    def website_fluxdock_privateperson(self, *args, **kw):
        return request.render('website_fluxdock_signup.privateperson', {})
