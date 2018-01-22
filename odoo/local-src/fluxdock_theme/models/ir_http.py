# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""
TMP workaround for anon sessions
https://github.com/laslabs/web/blob/f8cfa10c4f594dda5a424c0e580e9b5b9d361e57
/web_session_allow_public/models/ir_http.py
"""

from odoo import models
from odoo.http import SessionExpiredException


class IrHttp(models.Model):

    _inherit = 'ir.http'

    def _auth_method_user(self):
        try:
            return super(IrHttp, self)._auth_method_user()
        except SessionExpiredException:
            return self._auth_method_public()
