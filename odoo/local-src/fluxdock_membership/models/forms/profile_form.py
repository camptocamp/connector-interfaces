# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, _
import json


class PriorityCountryM2OWidget(models.AbstractModel):
    _name = 'fluxdock.form.widget.country_m2o'
    _inherit = 'cms.form.widget.many2one'
    _w_template = 'fluxdock_theme.country_field_widget_m2o'

    priority_countries = (
        'base.ch',
        'base.de',
        'base.fr',
        'base.it',
        'base.at',
        'base.uk',
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


class EmailWidget(models.AbstractModel):
    _name = 'fluxdock.form.widget.email'
    _inherit = 'cms.form.widget.char'
    _w_template = 'fluxdock_membership.email_field_widget_char'


class ProfileForm(models.AbstractModel):
    _inherit = 'cms.form.my.account'
    _form_model_fields = (
        'image',
        'name',
        'street',
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
        # TODO:: add `industry_ids` field
        # category_id = industry_ids
        'category_id',
        'expertise_ids',
    )
    _form_fields_order = _form_model_fields
    _form_required_fields = (
        "name", "street", "zip", "city", "country_id", "phone", "email")
    _form_wrapper_extra_css_klass = 'opt_dark_grid_bg white_content_wrapper'
    _form_extra_css_klass = 'center-block main-content-wrapper'

    @property
    def help_texts(self):
        texts = {
            'expertise_ids':
                '_xmlid:fluxdock_membership.partner_form_industry_help',
            'website': '',
        }
        return texts

    @property
    def field_label_overrides(self):
        texts = {
            'image': _('Company logo'),
            'name': _('Company name'),
            'street': _('Street / No.'),
            'website_short_description': _('Claim'),
            'category_id': _('Industries'),
        }
        return texts

    def form_update_fields_attributes(self, _fields):
        """Override to add help messages."""
        super().form_update_fields_attributes(_fields)

        # add extra help texts
        for fname, help_text in self.help_texts.items():
            if help_text.startswith('_xmlid:'):
                tmpl = self.env.ref(
                    help_text[len('_xmlid:'):], raise_if_not_found=False)
                if not tmpl:
                    continue
                help_text = tmpl.render({
                    'form_field': _fields[fname],
                })
            _fields[fname]['help'] = help_text

        # update some labels
        for fname, label in self.field_label_overrides.items():
            _fields[fname]['string'] = label

    @property
    def form_widgets(self):
        widgets = super().form_widgets

        # FIXME: handle this param w/ new widgets
        # update image widget to force size
        # data = {
        #     'image_preview_width': 200,
        #     'image_preview_height': 200,
        # }
        # data['forced_style'] = (
        #     'width:{image_preview_width}px;'
        #     'height:{image_preview_height}px;'
        # ).format(**data)
        # _fields['image']['widget'] = ImageWidget(
        #     self, 'image', _fields['image'], data=data)

        widgets.update({
            'email': 'fluxdock.form.widget.email',
            'country_id': 'fluxdock.form.widget.country_m2o'
        })
        return widgets
