# -*- coding: utf-8 -*-
# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models
from openerp.addons.cms_notifications.models.notification_panel_form \
    import master_slave_rules


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

    @property
    def _form_subtype_fields(self):
        res = super(CMSNotificationPanel, self)._form_subtype_fields
        res.update({
            'enable_matches':
                'specific_project_proposal.mt_proposal_matches',
        })
        return res

    def _form_master_slave_info(self):
        info = super(CMSNotificationPanel, self)._form_master_slave_info()
        self._form_info_merge(info, {
            'notify_email': master_slave_rules('enable_matches'),
        })
        return info
