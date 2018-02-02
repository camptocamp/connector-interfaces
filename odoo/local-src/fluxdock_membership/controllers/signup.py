import logging
import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.auth_signup_verify_email.controllers.main\
    import SignupVerifyEmail
from odoo.addons.web.controllers.main import ensure_db
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class AuthSignupHome(SignupVerifyEmail):

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

    # TODO: split this to website module
    # and make redirect and groups configurable
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

        backend_access = self._check_home_access()
        if not backend_access:
            # redirect to public homepage
            return http.local_redirect('/my/home',
                                       query=request.params,
                                       keep_hash=True)

        request.uid = request.session.uid

        try:
            context = request.env['ir.http'].webclient_rendering_context()
            response = request.render(
                'web.webclient_bootstrap', qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        except AccessError:
            return werkzeug.utils.redirect('/web/login?error=access')

    def _check_home_access(self):
        # check backend permissions
        has_backend_permissions = False
        user = request.env.user
        # surprisingly enough: sometimes you don't get the user here
        # even if you are logged in :(
        if not user and request.session.uid:
            user = request.env['res.users'].browse(request.session.uid)
        if user._is_admin() or user._is_system():
            has_backend_permissions = True
        else:
            for xmlid in ('base.group_website_designer', ):
                if request.env.user.has_group(xmlid):
                    has_backend_permissions = True
                    break
        return has_backend_permissions
