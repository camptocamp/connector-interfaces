# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class CMSNotificationPanel(models.AbstractModel):
    """Hold users notifications settings."""
    _inherit = 'cms.notification.panel.form'
    _form_fields_order = (
        'notify_email',
        'notify_frequency',
        'enable_matches',
    )
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'

    enable_matches = fields.Boolean(
        string='Enable matches notifications',
        help=("If active, you will receive notifications "
              "about proposals matches.")
    )

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(CMSNotificationPanel,
              self).form_update_fields_attributes(_fields)
        if self.env.context.get('lang') == 'de_DE':
            # FIXME: brute force translation for "Digest".
            # The only translation that is not loaded
            # BUT IS IN THE PO in `mail_digest` is "Digest".
            # We wasted so much time to get this translated
            # that here is the last resort...
            self.env.cr.execute(
                "select value from ir_translation where src='Digest'")
            try:
                val = self.env.cr.fetchone()[0]
            except Exception:
                val = None
            if val:
                options = dict(_fields['notify_email']['selection'])
                options['digest'] = val
                _fields['notify_email']['selection'] = options.items()

    @property
    def _form_subtype_fields(self):
        res = super(CMSNotificationPanel, self)._form_subtype_fields
        res.update({
            'enable_matches':
                'fluxdock_project.mt_proposal_matches',
        })
        return res

    def _form_master_slave_info(self):
        info = super(CMSNotificationPanel, self)._form_master_slave_info()
        self._form_info_merge(info, {
            'notify_email': {
                'hide': {
                    'enable_matches': ('none', ),
                },
                'show': {
                    'enable_matches': ('digest', 'always', ),
                },
            },
        })
        return info
