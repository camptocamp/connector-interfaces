# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from openerp import tools
from openerp.tools.translate import _

from openerp.addons.website_portal.controllers.main import website_account

class website_account(website_account):
    @http.route(['/my/account'], type='http', auth="user", website=True)
    def details(self, redirect=None, **post):
        if redirect:
            redirect = redirect
        else:
            redirect = ('/my/account')
        response = super(website_account, self).details(redirect, **post)
        # categories = request.env['res.partner.category'].sudo().search([])
        # areas = request.env['res.partner.area'].sudo().search([])
        # response.qcontext.update({
        #     'categories': categories,
        #     'areas': areas,
        # })
        # FIXME: Workaround for problem with saving of field website. If required
        # fields are not set, website will be taken out of response dictionary
        # in order to avoid server errors
        if 'website' in response.qcontext:
            del response.qcontext['website']
        # return request.redirect('/my/account')
        return response

    @http.route('/my/attachment/add', type='http', auth='user', methods=['POST'])
    def attach(self, func, upload=None, url=None, disable_optimization=None, **kwargs):
        Attachments = request.registry['ir.attachment']  # registry for the attachment table

        uploads = []
        message = None
        if not upload: # no image provided, storing the link and the image name
            name = url.split("/").pop()                       # recover filename
            attachment_id = Attachments.create(request.cr, request.uid, {
                'name': name,
                'type': 'url',
                'url': url,
                'public': True,
                'res_model': 'ir.ui.view',
            }, request.context)
            uploads += Attachments.read(request.cr, request.uid, [attachment_id], ['name', 'mimetype', 'checksum', 'url'], request.context)
        else:                                                  # images provided
            try:
                attachment_ids = []
                for c_file in request.httprequest.files.getlist('upload'):
                    data = c_file.read()
                    try:
                        image = Image.open(cStringIO.StringIO(data))
                        w, h = image.size
                        if w*h > 42e6:
                            raise ValueError(
                                u"Image size excessive, uploaded images must be smaller "
                                u"than 42 million pixel")
                        if not disable_optimization and image.format in ('PNG', 'JPEG'):
                            data = tools.image_save_for_web(image)
                    except IOError, e:
                        pass

                    attachment_id = Attachments.create(request.cr, request.uid, {
                        'name': c_file.filename,
                        'datas': data.encode('base64'),
                        'datas_fname': c_file.filename,
                        'public': True,
                        'res_model': 'ir.ui.view',
                    }, request.context)
                    attachment_ids.append(attachment_id)
                uploads += Attachments.read(request.cr, request.uid, attachment_ids, ['name', 'mimetype', 'checksum', 'url'], request.context)
            except Exception, e:
                logger.exception("Failed to upload image to attachment")
                message = unicode(e)

        return """<script type='text/javascript'>
            window.parent['%s'](%s, %s);
        </script>""" % (func, json.dumps(uploads), json.dumps(message))
