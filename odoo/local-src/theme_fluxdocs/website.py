# -*- coding: utf-8 -*-
# © 2016 Simone Orsi (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api


def smart_truncate(text, length=100, suffix='...'):
    """Smart truncate text."""
    # http://stackoverflow.com/questions/250357/
    # truncate-a-string-without-ending-in-the-middle-of-a-word
    text = text or ''
    if len(text) <= length:
        return text
    else:
        return ' '.join(text[:length + 1].split(' ')[0:-1]) + suffix


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def truncate_text(self, text, length=100, suffix='...'):
        """Truncate text."""
        return smart_truncate(text, length=length, suffix=suffix)
