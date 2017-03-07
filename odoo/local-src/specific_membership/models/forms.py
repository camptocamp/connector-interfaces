# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, _
from openerp import SUPERUSER_ID
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.addons.cms_form.widgets import ImageWidget
from openerp.addons.cms_form.widgets import M2OWidget

import json
import logging
_logger = logging.getLogger(__name__)
try:
    from validate_email import validate_email
except ImportError:
    _logger.debug("Cannot import `validate_email`.")


class PriorityCountryM2OWidget(M2OWidget):

    key = 'theme_fluxdocs.country_field_widget_m2o'

    priority_countries = (
        'base.ch', 'base.de',
        'base.uk', 'base.at',
        'base.fr', 'base.it'
    )

    def country_info(self, opt_item):
        return json.dumps({
            'code': opt_item.code,
            'phone_code': opt_item.phone_code
        })

    @property
    def option_items(self):
        domain = self.domain[:]
        # priority countries
        prio = []
        # switzerland, germany, UK, austria, france
        for xmlid in self.priority_countries:
            prio.append(self.env.ref(xmlid))
        domain.append(('id', 'not in', [x.id for x in prio]))
        _all = self.comodel.search(domain)
        result = prio + list(_all)
        return result


class PartnerForm(models.AbstractModel):
    """Partner model form."""

    _name = 'cms.form.res.partner'
    _inherit = 'cms.form'
    _form_model = 'res.partner'
    _form_fields_order = (
        'image',
        'name',
        'street2',
        'zip',
        'city',
        'country_id',
        'phone',
        'email',
        'website',
        'facebook',
        'twitter',
        'skype',
        'website_short_description',
        # category_id = industry_ids
        'category_id',
        'expertise_ids',
    )
    _form_required_fields = (
        "name", "street2", "zipcode", "city", "country_id", "phone", "email")
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg'
    _form_extra_css_klass = 'center-block main-content-wrapper'
    form_buttons_template = 'specific_membership.profile_form_buttons'

    @property
    def form_title(self):
        return _('Member profile')

    @property
    def help_texts(self):
        texts = {
            'image': _(
                'This field holds the company logo, limited to 1024x1024px'
            ),
        }
        return texts

    @property
    def field_label_overrides(self):
        texts = {
            'image': _('Company logo'),
            'name': _('Company name'),
            'street2': _('Street / No.'),
            'website_short_description': _('Claim'),
            'category_id': _('Industries'),
        }
        return texts

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super(PartnerForm, self).form_update_fields_attributes(_fields)

        # add extra help texts
        for fname, help_text in self.help_texts.iteritems():
            _fields[fname]['help'] = help_text

        # remove some help texts
        for fname in ('website', 'expertise_ids'):
            _fields[fname]['help'] = ''

        # update some labels
        for fname, label in self.field_label_overrides.iteritems():
            _fields[fname]['string'] = label

        # update image widget to force size
        _fields['image']['widget'] = ImageWidget(
            self, 'image', _fields['image'], data={
                'image_preview_width': 200,
                'image_preview_height': 200,
            })
        # use another template for email widget
        _fields['email']['widget'].key = \
            'specific_membership.email_field_widget_char'

        # pre-sorted countries widget
        _fields['country_id']['widget'] = PriorityCountryM2OWidget(
            self, 'country_id', _fields['country_id'], data={})

    def form_validate_email(self, value, **req_values):
        error, message = None, None
        if value and not validate_email(value):
            error = 'email_not_valid'
            message = _('Invalid Email! Please enter a valid email address.')
        return error, message

    def form_before_create_or_update(self, values, extra_values):
        user = self.env.user
        if 'email' in values and user.email != values.get('email'):
            self._handle_email_update(user, values)

    def form_after_create_or_update(self, values, extra_values):
        self.form_redirect = '/my/home'
        partner = self.main_object
        if partner.type == "contact":
            address_fields = {
                'city': values.get('city', None),
                'street': values.get('street', None),
                'street2': values.get('street2', None),
                'zip': values.get('zip', None),
                'country_id': values.get('country_id', None)
            }
            partner.commercial_partner_id.sudo().write(address_fields)
        # handle profile step upgrade
        # TODO: proper permissions
        # should allow user to write on its partner!
        partner.sudo().update_profile_state(step=2)

    def _handle_email_update(self, user, values):
        """Validate email update and handle login update."""
        email = values['email']
        valid = validate_email(email)
        if email and valid and user.id != SUPERUSER_ID:
            exists = user.sudo().search_count(
                ['|', ('login', '=', email), ('email', '=', email)]
            )
            # prevent email save and display friendly message
            values.pop('email')
            if exists and self.o_request.website:
                title = _('Warning')
                msg = _(
                    'Email address `%s` already taken. '
                    'Please check inside your company. '
                ) % email
                self.o_request.website.add_status_message(
                    msg, type_='warning', title=title)
                return False
            try:
                # update login on user
                # this MUST happen BEFORE `reset_password` call
                # otherwise it will not find the user to reset!
                user.sudo().write(
                    {'login': email, 'email': email, }
                )
                # send reset password link to verify email
                user.sudo().reset_password(email)
                can_change = True
            except MailDeliveryException:
                # do not update email / login
                # if for any reason we cannot send email
                can_change = False
            if can_change and self.o_request.website:
                title = _('Important')
                msg = _(
                    'Your login username has changed to: `%s`. '
                    'An email has been sent to verify it. '
                    'You will be asked to reset your password.'
                ) % email
                self.o_request.website.add_status_message(
                    msg, type_='warning', title=title)
            return True
        return False


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
    form_fields_template = 'specific_membership.search_form_fields'
    fluxdock_search_header_template = \
        'specific_membership.members_search_form_header'

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
