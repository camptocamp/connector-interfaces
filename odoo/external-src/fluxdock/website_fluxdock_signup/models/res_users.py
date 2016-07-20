# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
import random
from urlparse import urljoin
import werkzeug

from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.osv import osv, fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from ast import literal_eval
from openerp.tools.translate import _
from openerp.exceptions import UserError


class res_users(osv.Model):
    _inherit = 'res.users'


    def _now(self, **kwargs):
        dt = datetime.now() + timedelta(**kwargs)
        return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def send_account_confirmation_email(self, cr, uid, login, context=None):
        """ retrieve the user corresponding to login (login or email),
            and reset their password
        """
        user_ids = self.search(cr, uid, [('login', '=', login)], context=context)
        if not user_ids:
            user_ids = self.search(cr, uid, [('email', '=', login)], context=context)
        if len(user_ids) != 1:
            raise Exception(_('Reset password: invalid username or email'))
        return self.action_account_confirmation_email(cr, uid, user_ids, context=context)

    def action_account_confirmation_email(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id for user in self.browse(cr, uid, ids, context)]
        res_partner.signup_prepare(cr, uid, partner_ids, signup_type="confirmation", expiration=self._now(days=+7), context=context)

        if not context:
            context = {}

        # send email to users with their signup url
        template = False
        if not bool(template):
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'website_fluxdock_signup', 'account_confirmation_email')
        assert template._name == 'mail.template'

        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
            self.pool.get('mail.template').send_mail(cr, uid, template.id, user.id, force_send=True, raise_exception=True, context=context)

    _sql_constraints = [
        ('login', 'UNIQUE (login)',  'A user with this login already exists !')
    ]
