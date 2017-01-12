# -*- coding: utf-8 -*-

from openerp import http
from openerp import models
from openerp.addons.cms_form.controllers import FormControllerMixin
from openerp.addons.cms_form.widgets import DEFAULT_WIDGETS

WIDGETS = DEFAULT_WIDGETS.copy()
WIDGETS['image'].data = {
    'image_preview_width': 600,
    'image_preview_height': 400,
}


class ReferenceForm(models.AbstractModel):
    """Reference model form."""

    _name = 'cms.form.project.reference'
    _inherit = 'cms.form'
    _form_model = 'project.reference'
    _form_fields_order = (
        'name',
        'implementation_date',
        'location',
        'country_id',
        'industry_ids',
        'expertise_ids',
        'website_short_description',
        'image',
        'video_url',
        'ext_website_url',
        'linked_partner_ids',
    )
    _form_required_fields = ('name', 'website_short_description', 'image')
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    _form_widgets = WIDGETS

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(ReferenceForm, self).form_update_fields_attributes(_fields)
        industry_help = self.env.ref(
            'specific_project.ref_form_industry_help',
            raise_if_not_found=False)
        if industry_help:
            _fields['expertise_ids']['help'] = industry_help.render()
        partner_help = self.env.ref(
            'specific_project.ref_form_partner_help',
            raise_if_not_found=False)
        if partner_help:
            _fields['linked_partner_ids']['help'] = partner_help.render()
        if self.env.user and self.env.user.partner_id:
            _fields['linked_partner_ids']['domain'] = \
                '[["id","!=",{}]]'.format(self.env.user.partner_id.id)


class ReferenceFormController(http.Controller, FormControllerMixin):
    """Reference form controller."""

    @http.route([
        '/references/add',
        '/references/<model("project.reference"):reference>/edit',
    ], type='http', auth='user', website=True)
    def cms_form(self, reference=None, **kw):
        """Handle a `form` route.
        """
        model = 'project.reference'
        return self.make_response(
            model, model_id=reference and reference.id, **kw)
