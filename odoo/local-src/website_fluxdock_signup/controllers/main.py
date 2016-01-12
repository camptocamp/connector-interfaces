# -*- coding: utf-8 -*-
import openerp
from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.website_portal.controllers.main import website_account


class AuthSignupHome(openerp.addons.web.controllers.main.Home):

    @http.route('/web/presignup', type='http', auth='public', website=True)
    def web_fluxdock_pre_signup(self, *args, **kw):
        # qcontext = self.get_auth_signup_qcontext()
        #
        # if not qcontext.get('token') and not qcontext.get('signup_enabled'):
        #     raise werkzeug.exceptions.NotFound()
        #
        # if 'error' not in qcontext and request.httprequest.method == 'POST':
        #     try:
        #         self.do_signup(qcontext)
        #         return super(AuthSignupHome, self).web_login(*args, **kw)
        #     except (SignupError, AssertionError), e:
        #         qcontext['error'] = _(e.message)
        #
        # import ipdb; ipdb.set_trace()
        return request.render('website_fluxdock_signup.presignup', {})
