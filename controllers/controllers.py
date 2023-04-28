# -*- coding: utf-8 -*-
from odoo import http

# class Activofijosv(http.Controller):
#     @http.route('/activofijosv/activofijosv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/activofijosv/activofijosv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('activofijosv.listing', {
#             'root': '/activofijosv/activofijosv',
#             'objects': http.request.env['activofijosv.activofijosv'].search([]),
#         })

#     @http.route('/activofijosv/activofijosv/objects/<model("activofijosv.activofijosv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('activofijosv.object', {
#             'object': obj
#         })