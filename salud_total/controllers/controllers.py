# -*- coding: utf-8 -*-
# from odoo import http


# class SaludTotal(http.Controller):
#     @http.route('/salud_total/salud_total', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salud_total/salud_total/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('salud_total.listing', {
#             'root': '/salud_total/salud_total',
#             'objects': http.request.env['salud_total.salud_total'].search([]),
#         })

#     @http.route('/salud_total/salud_total/objects/<model("salud_total.salud_total"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salud_total.object', {
#             'object': obj
#         })

