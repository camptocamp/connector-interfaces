# Copyright 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _

# just for action_reset_password override >
from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
# > just for action_reset_password override


class ResUsers(models.Model):
    _inherit = 'res.users'

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

    # FIXME: user_id is used by odoo for "salesman". Yes, I know... :(
    # So we should rely on user_ids[0]
    @api.model
    def _handle_partner_user(self, user):
        if user.has_group('base.group_portal') \
                and not self.env.context.get('partner_no_portal_user') \
                and not user.user_id:
            user.partner_id.write({'user_id': user.id})

    @api.model
    def create(self, vals):
        # make sure user_id is propagated to partner for portal users
        user = super(ResUsers, self).create(vals)
        self._handle_partner_user(user)
        return user

    @api.multi
    def write(self, vals):
        # make sure user_id is propagated to partner for portal users
        res = super(ResUsers, self).write(vals)
        for user in self:
            self._handle_partner_user(user)
        return res

    @api.multi
    def action_reset_password(self):
        """Overridden to be able to use our own email templates!"""
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        self.mapped('partner_id').signup_prepare(
            signup_type="reset", expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref(
                    'fluxdock_membership.set_password_email',
                    raise_if_not_found=False)
            except ValueError:
                pass
        if not template:
            template = self.env.ref('fluxdock_membership.reset_password_email')
        assert template._name == 'mail.template'

        for user in self:
            if not user.email:
                raise UserError(_(
                    "Cannot send email: user %s has no email address."
                ) % user.name)
            template.with_context(lang=user.lang).send_mail(
                user.id, force_send=True, raise_exception=True)
            _logger.info(
                "Password reset email sent for user <%s> to <%s>",
                user.login, user.email)
