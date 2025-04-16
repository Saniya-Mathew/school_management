# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomWebsite(http.Controller):
    @http.route(['/school'], type='http', auth='public', website=True)

    def display_calculations(self, **kwargs):

        # Fetch calculations from your custom model
        calculation_model = request.env['student.registration']
        calculations = calculation_model.search([])

        values = {
            'calculations': calculations,
        }

        return http.request.render('school.template_id', values)