# -*- coding: utf-8 -*-

from openerp import http
from openerp import models
from openerp import _
# from openerp.http import request
from openerp.addons.cms_form.controllers import FormControllerMixin
from openerp.addons.cms_form.widgets import DEFAULT_WIDGETS

WIDGETS = DEFAULT_WIDGETS.copy()
WIDGETS['image'].data = {
    'image_preview_width': 600,
    'image_preview_height': 400,
}

EXPERTISE_HELP = _("""Don't find your industry or expertise? Write us an email at
<a href="mailto:expertise@fluxdock.io?subject=new%20industry%20/%20expertise">expertise@fluxdock.io</a>
""") # noqa


LINKED_PARTNERS_HELP = _("""Don't find your partner? Write us an email with the partner company name and email address at
<a href="mailto:newpartner@fluxdock.io?subject=new%20partner">newpartner@fluxdock.io</a> for inviting him.
""") # noqa


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
        _fields['expertise_ids']['help'] = EXPERTISE_HELP
        _fields['linked_partner_ids']['help'] = LINKED_PARTNERS_HELP
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
