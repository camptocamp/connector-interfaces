# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector_importer.utils.mapper_utils import xmlid_to_rel

from ..utils import sanitize_external_id


def xmlids_to_rel(field):
    """Convert xmlids source values to ids."""

    def modifier(self, record, to_attr):
        value = record.get(field)
        if not value:
            return None
        return [
            (
                6,
                0,
                [
                    self.env.ref(x).id
                    for x in value.split(",")
                    if self.env.ref(x, raise_if_not_found=False)
                ],
            )
        ]

    return modifier


class ProductCategoryRecordImporter(Component):
    _name = "product.category.importer"
    _inherit = ["common.importer", "translation.importer"]
    _apply_on = "product.category"
    odoo_unique_key = "id"
    odoo_unique_key_is_xmlid = True

    def prepare_line(self, line):
        res = super().prepare_line(line)
        res["id"] = sanitize_external_id(line["id"])
        res["parent_id/id"] = sanitize_external_id(line["parent_id/id"])
        return res


class ProductCategoryMapper(Component):
    _name = "product.category.mapper"
    _inherit = "importer.base.mapper"
    _apply_on = "product.category"

    _direct = [
        # "id" needs to be in the mapped values to be converted as XML-ID
        # TODO: need to allow the use of fake destination fields like '_xmlid'
        # in direct mapping here:
        # https://github.com/OCA/connector/blob/13.0/connector/components/mapper.py#L891
        ("id", "id"),
        ("name", "name"),
        (xmlid_to_rel("parent_id/id"), "parent_id"),
        (xmlids_to_rel("category_usage_ids/id"), "category_usage_ids"),
    ]
    translatable = ["name"]

    @property
    def direct(self):
        return self._direct

    @mapping
    def default_property_cost_method(self, record):
        return {"property_cost_method": "average"}
