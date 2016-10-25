# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api
from openerp.http import request
from openerp import _

# TODO: this concept has been borrowed from website_cms
# we should refactor this in the separate module!


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def add_status_message(self, msg, mtitle='', mtype='info'):
        """Inject status message in session."""
        mtitle = mtitle or _('Info')
        status_message = {
            'msg': msg,
            'title': mtitle,
            'type': mtype,
        }
        if request.session:
            request.session.setdefault(
                'status_message', []).append(status_message)

    @api.model
    def get_status_message(self):
        if request.session:
            return request.session.pop('status_message', {})
        return {}
