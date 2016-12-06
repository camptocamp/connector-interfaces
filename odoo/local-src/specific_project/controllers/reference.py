# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import json
import base64
import werkzeug.urls

from openerp import _, http
from openerp.http import request

# from openerp.addons.website.models.website import slug


class WebsiteReference(http.Controller):
    """Controller for reference model."""

    form_mandatory_fields = ("name", "website_short_description", "image")
    form_optional_fields = (
        "implementation_date", "location", "industry_ids",
        "expertise_ids", "linked_partner_ids",
        "video_url", "country_id"
    )
    # TODO: determine this by inspecting the field on the model
    form_file_fields = ('image', )
    form_fields = form_mandatory_fields + form_optional_fields
    form_control_fields = ('image_keepcheck', )

    def details_form_validate(self, data):
        error = {}
        errors_message = []

        missing = False

        for field_name in self.form_mandatory_fields:
            if not data.get(field_name):
                if field_name == 'image' \
                        and not data.get('image_keepcheck') == 'no':
                    continue
                error[field_name] = 'missing'
                missing = True

        # error message for empty required fields
        if missing:
            errors_message.append(_('Some required fields are empty.'))

        return error, errors_message

    def extract_values(self, form_data):
        """Override to manipulate POST values."""
        values = {}
        valid_fields = self.form_fields
        form_values = {
            k: v for k, v in form_data.iteritems()
            if k in valid_fields or k in self.form_control_fields
        }
        for fname in valid_fields:
            value = form_values.get(fname)
            # TODO: lookup by field type 1st
            custom_handler = getattr(self, '_extract_' + fname, None)
            if custom_handler:
                value = custom_handler(value, form_values)
            if fname in form_values and value is not None:
                # a custom handler could pop a field
                # to discard it from submission, ie: keep an image as it is
                values[fname] = value
        # FIXME:
        # we do this to prevent submitting
        # of bad empty values for specific fields
        # we should retrieve field info/type via real model fields
        _values = values.copy()
        for k, v in _values.iteritems():
            if k.endswith(('_ids', '_id', '_date')) \
                    and isinstance(v, basestring) and len(v) == 0:
                values.pop(k)
        return values

    def _extract_image(self, field_value, form_values):
        if form_values.get('image_keepcheck') == 'yes':
            # prevent discarding image
            if form_values.get('image'):
                form_values.pop('image')
            form_values.pop('image_keepcheck')
            return None
        if hasattr(field_value, 'read'):
            image_content = field_value.read()
            value = base64.encodestring(image_content)
        else:
            value = field_value.split(',')[-1]
        return value

    def _extract_m2m_ids(self, field_value, form_values):
        value = False
        if len(field_value) > 0:
            ids = field_value.split(',')
            ids = [int(rec_id) for rec_id in ids]
            value = [(6, None, ids)]
        return value

    def _extract_industry_ids(self, field_value, form_values):
        return self._extract_m2m_ids(field_value, form_values)

    def _extract_expertise_ids(self, field_value, form_values):
        return self._extract_m2m_ids(field_value, form_values)

    def _extract_linked_partner_ids(self, field_value, form_values):
        return self._extract_m2m_ids(field_value, form_values)

    def _extract_country_id(self, field_value, form_values):
        return int(field_value or False)

    def load_defaults(self, item, **kw):
        """Override to load default values."""
        defaults = {}
        if not item:
            return defaults
        for fname in self.form_fields:
            value = item[fname]
            custom_handler = getattr(self, '_load_default_' + fname, None)
            if custom_handler:
                value = custom_handler(item, value, **kw)
            defaults[fname] = value
            if fname in kw:
                # maybe a POST request with new values
                # TODO: load particular fields too
                defaults[fname] = kw.get(fname)
        for fname in self.form_file_fields:
            defaults['has_' + fname] = bool(item[fname])
        return defaults

    def _load_default_m2m_ids(self, item, value):
        value = [{'id': x.id, 'name': x.display_name} for x in value]
        value = json.dumps(value)
        return value

    def _load_default_industry_ids(self, item, value):
        return self._load_default_m2m_ids(item, value)

    def _load_default_expertise_ids(self, item, value):
        return self._load_default_m2m_ids(item, value)

    def _load_default_linked_partner_ids(self, item, value):
        return self._load_default_m2m_ids(item, value)


    # TODO: do we really need 2 routes per 'my'/'all'?
    @http.route([
        '/my/references/add',
        '/my/references/<model("project.reference"):reference>/edit',
        '/references/add',
        '/references/<model("project.reference"):reference>/edit',
    ], type='http', auth='user', website=True)
    def reference_edit(self, reference=None, **post):
        countries = request.env['res.country'].sudo().search([])
        values = {
            'reference': reference,
            'errors': {},
            'error_messages': {},
            'countries': countries,
        }
        if request.httprequest.method == 'GET':
            values.update(self.load_defaults(reference))
        elif request.httprequest.method == 'POST':
            errors, errors_message = self.details_form_validate(post)
            if not errors:
                values = self.extract_values(post)
                if reference:
                    reference.write(values)
                else:
                    reference = request.env['project.reference'].create(values)
                return werkzeug.utils.redirect(reference.website_url)

            values.update({
                'errors': errors,
                'errors_message': errors_message,
            })
            values.update(self.load_defaults(reference), **post)
        return request.website.render("specific_project.reference_form",
                                      values)

    @http.route([
        '/references/<model("project.reference"):reference>',
        '/my/references/<model("project.reference"):reference>',
    ], type='http', auth='public', website=True)
    def reference_detail(self, reference, **kw):
        values = {
            'reference': reference
        }
        return request.website.render("specific_project.reference_detail",
                                      values)
