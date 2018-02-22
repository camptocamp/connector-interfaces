# Copyright 2017 Simone Orsi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class NotificationSearchForm(models.AbstractModel):
    """Partner model search form."""

    _inherit = 'cms.notification.listing'
    _form_wrapper_extra_css_klass = 'bg-flux_dark_grid white_content_wrapper'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    form_show_search_form = 0
