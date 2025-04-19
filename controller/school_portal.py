# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomWebsite(http.Controller):
    @http.route(['/students'], type='http', auth='public', website=True)

    def student_registration(self, **kwargs):
        return request.render('school.web_form_template')

    @http.route('/students/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_student_form_submit(self, **post):
         request.env['student.registration'].sudo().create({
                     'f_name': post.get('name'),
                     'phone': post.get('phone'),
                     'email': post.get('email'),
                     'aadhar_no': post.get('Aadhaar Number')
        })

    @http.route(['/leaves'], type='http', auth='public', website=True)
    def student_leave(self, **kwargs):
        students = request.env['student.registration'].sudo().search([])
        values = {
               'student': students,
        }
        return request.render('school.web_leave_template', values)

    @http.route('/leaves/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_leave_form_submit(self, **post):
        request.env['school.leave'].sudo().create({
            'student_id': post.get('name'),
            'date_from': post.get('Start Date'),
            'date_to': post.get('End Date'),
        })

    @http.route(['/events'], type='http', auth='public', website=True)
    def school_event(self, **kwargs):
        return request.render('school.web_event_template')

