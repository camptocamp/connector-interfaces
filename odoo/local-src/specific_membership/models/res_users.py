# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models
from openerp import fields
from openerp import _

# just for action_reset_password override >
from datetime import datetime, timedelta
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import UserError


def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
# > just for action_reset_password override


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_associate = fields.Boolean(
        string='Is associate member',
        related='partner_id.is_associate',
        readonly=True,
    )
    is_free = fields.Boolean(
        string='Is free member',
        related='partner_id.is_free',
        readonly=True,
    )

    _sql_constraints = [
        (
            'login',
            'UNIQUE (login)',
            _('A user with this login already exists !')
        )
    ]

    # overridden to be able to use our own email templates!
    def action_reset_password(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """ # noqa
        # prepare reset password signup
        if not context:
            context = {}
        create_mode = bool(context.get('create_user'))
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id
                       for user in self.browse(cr, uid, ids, context)]

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        res_partner.signup_prepare(
            cr, uid, partner_ids,
            signup_type="reset", expiration=expiration, context=context)

        context = dict(context or {})

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                # get_object() raises ValueError if record does not exist
                template = self.pool.get('ir.model.data').get_object(
                    cr, uid, 'specific_membership', 'set_password_email')
            except ValueError:
                pass
        if not bool(template):
            template = self.pool.get('ir.model.data').get_object(
                cr, uid, 'specific_membership', 'reset_password_email')
        assert template._name == 'mail.template'

        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise UserError(
                    _("Cannot send email: user %s has no email address.")
                    % user.name)
            context['lang'] = user.lang
            self.pool.get('mail.template').send_mail(
                cr, uid, template.id, user.id,
                force_send=True, raise_exception=True, context=context)
