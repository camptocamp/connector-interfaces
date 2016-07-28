# -*- coding: utf-8 -*-
from openerp import http

# class WebsiteTermsOfUse(http.Controller):
#     @http.route('/website_terms_of_use/website_terms_of_use/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_terms_of_use/website_terms_of_use/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_terms_of_use.listing', {
#             'root': '/website_terms_of_use/website_terms_of_use',
#             'objects': http.request.env['website_terms_of_use.website_terms_of_use'].search([]),
#         })

#     @http.route('/website_terms_of_use/website_terms_of_use/objects/<model("website_terms_of_use.website_terms_of_use"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_terms_of_use.object', {
#             'object': obj
#         })