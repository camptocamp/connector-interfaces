# -*- coding: utf-8 -*-
# © 2016 Denis Leemann (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, api
from openerp.http import request
from openerp import _


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

    # TODO: the status_message concept has been borrowed from website_cms
    # we should refactor this in the separate module!

    DEFAULT_STATUS_MSG_TITLE = {
        'info': _('Info'),
        'success': _('Success'),
        'danger': _('Error'),
        'warning': _('Warning'),
    }

    @api.model
    def add_status_message(self, msg, mtitle='', mtype='info'):
        """Inject status message in session."""
        mtitle = mtitle or self.DEFAULT_STATUS_MSG_TITLE.get(mtype or 'info')
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

    @api.model
    def truncate_text(self, text, length=100, suffix='...'):
        """Truncate text."""
        return smart_truncate(text, length=length, suffix=suffix)
