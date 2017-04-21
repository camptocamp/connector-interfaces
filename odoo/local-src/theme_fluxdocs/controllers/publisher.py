# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp.addons.web import http
from openerp.addons.web.http import request


class Publisher(http.Controller):
    """Controller for handling publish buttons."""

    @http.route(['/flux/publisher'], type='json', auth="public", website=True)
    def publish(self, id, object):
        _id = int(id)
        _object = request.registry[object]
        obj = _object.browse(request.cr, request.uid, _id)

        values = {}
        if 'website_published' in _object._fields:
            values['website_published'] = not obj.website_published
        _object.write(request.cr, request.uid, [_id],
                      values, context=request.context)

        obj = _object.browse(request.cr, request.uid, _id)

        redirect = ''
        if hasattr(obj, 'redirect_after_publish') \
                and obj.redirect_after_publish():
            redirect = '/my/home'
        if hasattr(obj, 'do_after_publish'):
            obj.do_after_publish()
        return {
            'ok': True,
            'status': bool(obj.website_published),
            'redirect': redirect,
        }
