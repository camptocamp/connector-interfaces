# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import threading
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'profession_ids' in vals:
            self._update_matches()
        return res

    @api.multi
    def _update_matches(self):
        """Retrieve all matching proposals and set them as dirty."""
        matching_props = self.sudo().mapped('user_id.proposal_match_ids')
        # mark them as dirty and rely on cron to create messages
        matching_props.set_notify_dirty(True)

    # TODO: move this to an OCA module
    # to allow to customize email.template by subtype.
    # This method has been barely copied from mail.models.res_partner
    # and only a small patch + PEP8 has been applied.
    # There's already a module for v8 here
    # https://github.com/OCA/social/tree/8.0/mail_notification_email_template
    # but it relies on old model 'mail.notification'.
    # We should migrate and fix it.
    @api.multi
    def _notify_by_email(self, message, force_send=False, user_signature=True):
        """ Method to send email linked to notified messages.
        The recipients are the recordset on which this method is called. """
        if not self.ids:
            return True

        # existing custom notification email
        base_template = None
        if message.model:
            tname = 'mail.mail_template_data_notification_email_%s' \
                % message.model.replace('.', '_')
            base_template = self.env.ref(tname, raise_if_not_found=False)
        if not base_template:
            base_template = self.env.ref(
                'mail.mail_template_data_notification_email_default')

        # #### PATCH START
        matches_subtype = self.env.ref(
            'fluxdock_project.mt_proposal_matches'
        )
        if message.subtype_id == matches_subtype:
            base_template = self.env.ref(
                'fluxdock_project.mail_matches_notification')
        # #### PATCH STOP

        base_template_ctx = self._notify_prepare_template_context(message)
        if not user_signature:
            base_template_ctx['signature'] = False
        base_mail_values = self._notify_prepare_email_values(message)

        # classify recipients: actions / no action
        if message.model and message.res_id and hasattr(
                self.env[message.model], '_message_notification_recipients'):
            recipients = self.env[message.model].browse(
                message.res_id)._message_notification_recipients(message, self)
        else:
            recipients = self.env[
                'mail.thread']._message_notification_recipients(message, self)

        emails = self.env['mail.mail']
        recipients_nbr, recipients_max = 0, 50
        for email_type, recipient_template_values in recipients.items():
            if recipient_template_values['followers']:
                # generate notification email content
                template_fol_values = dict(
                    base_template_ctx,
                    **recipient_template_values
                )  # fixme: set button_unfollow to none
                template_fol_values['button_follow'] = False
                template_fol = base_template.with_context(
                    **template_fol_values)
                # generate templates for followers and not followers
                fol_values = template_fol.generate_email(
                    message.id, fields=['body_html', 'subject'])
                # send email
                new_emails, new_recipients_nbr = self._notify_send(
                    fol_values['body'], fol_values['subject'],
                    recipient_template_values['followers'], **base_mail_values)
                emails |= new_emails
                recipients_nbr += new_recipients_nbr
            if recipient_template_values['not_followers']:
                # generate notification email content
                template_not_values = dict(
                    base_template_ctx,
                    **recipient_template_values
                )  # fixme: set button_follow to none
                template_not_values['button_unfollow'] = False
                template_not = base_template.with_context(
                    **template_not_values)
                # generate templates for followers and not followers
                not_values = template_not.generate_email(
                    message.id, fields=['body_html', 'subject'])
                # send email
                new_emails, new_recipients_nbr = self._notify_send(
                    not_values['body'], not_values['subject'],
                    recipient_template_values['not_followers'],
                    **base_mail_values)
                emails |= new_emails
                recipients_nbr += new_recipients_nbr

        # NOTE:
        #   1. for more than 50 followers, use the queue system
        #   2. do not send emails immediately if the registry is not loaded,
        #      to prevent sending email during a simple update of the database
        #      using the command-line.
        if force_send and recipients_nbr < recipients_max and (
                not self.pool._init or
                getattr(threading.currentThread(), 'testing', False)):
            emails.send()
