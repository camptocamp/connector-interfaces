# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.component.core import Component


class CommonImporter(Component):
    _name = "common.importer"
    _inherit = "importer.record"

    _break_on_error = True


class TranslationImporter(Component):
    _name = "translation.importer"
    _inherit = "importer.record"

    _break_on_error = True

    def make_translation_key(self, key, lang):
        """Overridden to handle 'name_fr' and 'name_de' fields."""
        return "{}_{}".format(key, lang[:2])
