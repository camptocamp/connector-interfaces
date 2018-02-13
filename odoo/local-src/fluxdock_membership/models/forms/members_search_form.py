# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, _


MEMBERSHIP_STATES = ('free', 'paid', 'invoiced')


class PartnerSearchForm(models.AbstractModel):
    """Partner model search form."""

    _name = 'cms.form.search.res.partner'
    _inherit = 'fluxdock.cms.form.search'
    _form_model = 'res.partner'
    _form_fields_order = (
        'name',
        'category_id',
        'expertise_ids',
        'country_id',
    )
    form_fields_template = 'fluxdock_membership.search_form_fields'

    def listing_options(self):
        return {
            'show_preview': True,
            'show_create_date': False,
        }

    def get_country_domain(self):
        """We want to list only countries that match a partner."""
        search_values = self.form_get_request_values()
        membership_line_obj = self.env['membership.membership_line'].sudo()
        partner_obj = self.env['res.partner'].sudo()
        search_name = search_values.get('name', '')
        today = fields.Date.today()

        # base domain for groupby / searches
        base_line_domain = [
            ("partner.website_published", "=", True), ('state', '=', 'paid'),
            ('date_to', '>=', today), ('date_from', '<=', today)
        ]

        if search_name:
            base_line_domain += [
                '|', ('partner.name', 'ilike', search_name),
                ('partner.website_description', 'ilike', search_name)
            ]

        # group by country, based on all customers (base domain)
        membership_lines = membership_line_obj.search(base_line_domain)
        country_domain = [
            '|', ('member_lines', 'in', membership_lines.ids),
            ('membership_state', 'in', MEMBERSHIP_STATES),
        ]

        if search_name:
            country_domain += ['|', ('name', 'ilike', search_name),
                               ('website_description', 'ilike', search_name)]
        countries = partner_obj.read_group(
            country_domain + [("website_published", "=", True)],
            ["id", "country_id"],  # noqa
            groupby="country_id", orderby="country_id")

        return [
            ('id', 'in', [x['country_id'][0]
                          for x in countries if x['country_id']])
        ]

    def form_update_fields_attributes(self, _fields):
        """Override to change country domain."""
        super(PartnerSearchForm, self).form_update_fields_attributes(_fields)
        # TODO: move this to a custom widget
        # _fields['country_id']['domain'] = self.get_country_domain()
        # TODO: remove when moving to proper industry_ids field
        _fields['category_id']['string'] = _('Industries')

    def form_search_domain(self, search_values):
        """Adapt domain."""
        _super = super(PartnerSearchForm, self)
        domain = _super.form_search_domain(search_values)
        # fixed domain
        domain += [
            ('membership_state', 'in', MEMBERSHIP_STATES),
            ('website_published', '=', True)
        ]
        search_name = search_values.get('name')
        if search_name:
            domain += [
                '|',
                ('name', 'ilike', search_name),
                ('website_description', 'ilike', search_name)
            ]
        # put industry_ids and expertise_ids in OR
        exp = [x for x in domain if x[0] == 'category_id']
        ind = [x for x in domain if x[0] == 'expertise_ids']
        if ind and exp:
            common_domain = [
                x for x in domain
                if x[0] not in ('category_id', 'expertise_ids')
            ]
            domain = ['&', '|', ] + ind + exp + ['&'] + common_domain
        return domain
