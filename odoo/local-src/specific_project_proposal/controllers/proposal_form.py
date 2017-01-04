# -*- coding: utf-8 -*-

from openerp import http
from openerp import models
# from openerp import _
# from openerp.http import request
from openerp.addons.cms_form.controllers import FormControllerMixin
from openerp.addons.cms_form.models.cms_form import DEFAULT_WIDGETS

WIDGETS = DEFAULT_WIDGETS.copy()
WIDGETS['image']['params'] = {
    'image_preview_width': 600,
    'image_preview_height': 400,
}


class ProposalForm(models.AbstractModel):
    """Proposal model form."""

    _name = 'cms.form.project.proposal'
    _inherit = 'cms.form'
    _form_model = 'project.proposal'
    _form_fields_order = (
        'name',
        'location',
        'country_id',
        'website_short_description',
        'website_description',
        'start_date',
        'stop_date',
        'industry_ids',
        'expertise_ids',
    )
    _form_required_fields = (
        'name',
        'website_short_description',
        'website_description',
        'industry_ids',
        'expertise_ids',
    )
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    _form_widgets = WIDGETS


class ProposalFormController(http.Controller, FormControllerMixin):
    """Proposal form controller."""

    @http.route([
        '/proposals/add',
        '/proposals/<model("project.proposal"):main_object>/edit',
    ], type='http', auth='user', website=True)
    def cms_form(self, main_object=None, **kw):
        """Handle a `form` route.
        """
        model = 'project.proposal'
        return self.make_response(
            model, model_id=main_object and main_object.id, **kw)
