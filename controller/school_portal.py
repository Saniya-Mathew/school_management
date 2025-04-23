# -*- coding: utf-8 -*-
from os.path import exists

from odoo import http
from odoo.http import request


class CustomWebsite(http.Controller):
    @http.route(['/students'], type='http', auth='public', website=True)

    def student_registration(self, **kwargs):
        records = request.env['student.registration'].sudo().search([])
        values = {
            'student': records,
        }
        return request.render('school.student_list_template',values)

    @http.route(['/students/new'], type='http', auth='public', website=True)
    def create_student_registration(self, **kwargs):
        return request.render('school.web_form_template')


    @http.route('/students/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_student_form_submit(self, **post):
         request.env['student.registration'].sudo().create({
                      'f_name': post.get('name'),
                      'phone': post.get('phone'),
                      'email': post.get('email'),
                      'aadhar_no': post.get('Aadhaar Number'),
                      'dob':post.get('date of birth')
         })
         return request.redirect('/students')

    @http.route(['/leaves'], type='http', auth='public', website=True)
    def student_leave(self, **kwargs):
        students = request.env['school.leave'].sudo().search([])
        values = {
               'student': students,
        }
        return request.render('school.leave_list_template', values)

    @http.route(['/leaves/new'], type='http', auth='public', website=True)
    def create_student_leave(self, **kwargs):
        students = request.env['student.registration'].sudo().search([])
        values = {
            'student': students,
        }
        return request.render('school.web_leave_template',values)

    @http.route('/leaves/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_leave_form_submit(self, **post):
        request.env['school.leave'].sudo().create({
            'student_id': post.get('student_id'),
            'stu_class': post.get('class'),
            'date_from': post.get('s_date'),
            'date_to': post.get('e_date'),
            'reason': post.get('reason')
        })

    @http.route(['/events'], type='http', auth='public', website=True)
    def school_event(self, **kwargs):
        records = request.env['school.event'].sudo().search([])
        values = {
            'club': records,
        }
        return request.render('school.event_list_template', values)

    @http.route(['/events/new'], type='http', auth='public', website=True)
    def create_school_event(self, **kwargs):
        club = request.env['school.club'].sudo().search([])
        values = {
            'club': club,
        }
        return request.render('school.web_event_template', values)

    @http.route('/events/submit', type='http', auth='public', website=True, methods=['POST'])
    def web_event_form_submit(self, **post):
        request.env['school.event'].sudo().create({
            'name': post.get('Name'),
            'club_id': post.get('club_id'),
            'event_date': post.get('date'),
        })


    @http.route('/students/delete/<int:student_id>', type='http', auth='public', website=True, methods=['GET'])
    def delete_student_record(self, student_id):
        student = request.env['student.registration'].sudo().browse(student_id)
        if student:
            student.unlink()
        return request.redirect('/students')



