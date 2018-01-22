# -*- coding: utf-8 -*-

from openerp import models


class MailDigest(models.Model):
    _inherit = 'mail.digest'

    def _get_template_values(self):
        values = super(MailDigest, self)._get_template_values()
        values.update({
            'matches_subtype': self.env.ref(
                'fluxdock_project.mt_proposal_matches')
        })
        return values
