# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import _
from openerp.addons.cms_form.widgets import DEFAULT_WIDGETS

WIDGETS = DEFAULT_WIDGETS.copy()
WIDGETS['image'].data = {
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
        'contact_name',
        'contact_email',
        'contact_phone',
    )
    _form_required_fields = (
        'name',
        'website_short_description',
        'industry_ids',
        'expertise_ids',
    )
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    _form_widgets = WIDGETS

    @property
    def form_description(self):
        return _('Announce here a project your looking for collaborators. ')

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(ProposalForm, self).form_update_fields_attributes(_fields)
        industry_help = self.env.ref(
            'specific_project.ref_form_industry_help',
            raise_if_not_found=False)
        if industry_help:
            help_text = industry_help.render({
                'form_field': _fields['expertise_ids'],
            })
            _fields['expertise_ids']['help'] = help_text

        # limit claim length
        _fields['website_short_description']['widget'].maxlength = 200


class ProposalSearchForm(models.AbstractModel):
    """Proposal model search form."""

    _name = 'cms.form.search.project.proposal'
    _inherit = 'cms.form.search.project.reference'
    _form_model = 'project.proposal'

    only_my = fields.Boolean(string="Show only my proposals")
    fluxdock_search_header_template = \
        'specific_project_proposal.proposal_search_form_header'
