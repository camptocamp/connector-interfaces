# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""
TMP workaround for anon sessions
https://github.com/laslabs/web/blob/f8cfa10c4f594dda5a424c0e580e9b5b9d361e57
/web_session_allow_public/models/ir_http.py
"""

from odoo import models
from odoo.http import SessionExpiredException


class IrHttp(models.AbstractModel):

    _inherit = 'ir.http'

    @classmethod
    def _auth_method_user(cls):
        try:
            return super()._auth_method_user()
        except SessionExpiredException:
            return cls._auth_method_public()
