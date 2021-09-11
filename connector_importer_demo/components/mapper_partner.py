# Author: Simone Orsi
# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component


class ImportMapperPartner(Component):
    _name = "importer.mapper.partner"
    _inherit = ["importer.mapper.auto"]
    _usage = "importer.mapper"

    required = {
        # source key: dest key
        # You can declare here the keys the importer must have
        # to import a record.
        # `source key` means a key in the source record
        # either a line in a csv file or a lien from an sql table.
        # `dest key` is the destination the for the source one.
        # Eg: in your mapper you could have a mapping like
        #     direct = [
        #         ('title', 'name'),
        #         (concat(('title', 'foo', ), separator=' - '), 'baz'),
        #     ]
        # You want the record to be skipped if:
        # 1. title or name are not valued in the source
        # 2. title is valued but the conversion gives an empty value for name
        # 3. title or foo are not valued in the source
        # 4. title and foo are valued but the conversion
        #    gives an empty value for baz
        # You can achieve this like:
        # required = {
        #     'title': ('name', 'baz'),
        #     'foo': 'baz',
        # }
        # If you want to check only the source or the destination key
        # use the same name and prefix it w/ double underscore, like:
        # {'__foo': 'baz', 'foo': '__baz'}
        "name": "name",
        # Uncomment this id to test skip_info
        # 'id': 'external_id',
    }
    translatable = ["city"]
    defaults = [
        # odoo field, value
        # ('sale_ok', True),
        # defaults can be also retrieved via xmlid to other records.
        # The format is: `_xmlid::$record_xmlid::$record_field_value`
        # whereas `$record_xmlid` is the xmlid to retrieve
        # and ``$record_field_value` is the field to be used as value.
        # Example:
        # ('company_id', '_xmlid:base.main_company:id'),
    ]
