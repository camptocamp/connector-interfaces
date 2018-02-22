# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models
from odoo import fields
from odoo import _


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
    _form_required_fields = ('name', 'website_short_description', )
    _form_wrapper_extra_css_klass = 'bg-flux_dark_grid white_content_wrapper'
    _form_extra_css_klass = 'center-block main-content-wrapper'

    @property
    def form_description(self):
        return _('Register here projects '
                 'your company accomplished successfully.')

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(ReferenceForm, self).form_update_fields_attributes(_fields)
        industry_help = self.env.ref(
            'fluxdock_project.ref_form_industry_help',
            raise_if_not_found=False)
        if industry_help:
            help_text = industry_help.render({
                'form_field': _fields['expertise_ids'],
            })
            _fields['expertise_ids']['help'] = help_text
        partner_help = self.env.ref(
            'fluxdock_project.ref_form_partner_help',
            raise_if_not_found=False)
        if partner_help:
            help_text = partner_help.render({
                'form_field': _fields['linked_partner_ids'],
            })
            _fields['linked_partner_ids']['help'] = help_text
        if self.env.user and self.env.user.partner_id:
            _fields['linked_partner_ids']['domain'] = \
                '[["id","!=",{}]]'.format(self.env.user.partner_id.id)

        # FIXME: widgets have changed in cms_form
        # # update image widget to force size
        # _fields['image']['widget'] = ImageWidget(
        #     self, 'image', _fields['image'], data={
        #         'image_preview_width': 600,
        #         'image_preview_height': 400,
        #     })


class ReferenceSearchForm(models.AbstractModel):
    """Reference model search form."""

    _name = 'cms.form.search.project.reference'
    _inherit = 'fluxdock.cms.form.search'
    _form_model = 'project.reference'
    _form_fields_order = (
        'name',
        'industry_ids',
        'expertise_ids',
        'country_id',
        'location',
        'only_my',
    )
    form_fields_template = 'fluxdock_project.search_form_fields'

    only_my = fields.Boolean(string="Show only my references")

    def listing_options(self):
        return {
            'show_preview': False,
            'show_create_date': True,
        }

    def form_search_domain(self, search_values):
        """Adapt domain to filter on personal items."""
        _super = super(ReferenceSearchForm, self)
        domain = _super.form_search_domain(search_values)
        # make sure only_my is not used
        domain = [x for x in domain if x[0] != 'only_my']
        # if value is submitted then filter by owner
        if self.o_request.session.uid and search_values.get('only_my'):
            domain.append(('create_uid', '=', self.env.user.id))
        # put industry_ids and expertise_ids in OR
        exp = [x for x in domain if x[0] == 'industry_ids']
        ind = [x for x in domain if x[0] == 'expertise_ids']
        if ind and exp:
            common_domain = [
                x for x in domain
                if x[0] not in ('industry_ids', 'expertise_ids')
            ]
            domain = ['&', '|', ] + ind + exp + ['&'] + common_domain
        return domain
