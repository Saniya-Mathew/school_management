# -*- coding: utf-8 -*-
from reportlab.graphics.transform import inverse
from odoo import api, fields, models, _
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import ValidationError
import re
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


class StudentRegistration(models.Model):
    """"Shows all the information related to student registration"""
    _name = "student.registration"
    _description = "Student Registration"
    _rec_name = 'f_name'
    _inherit = 'mail.thread'


    reg_no = fields.Char("Registration Number",copy=False, readonly=True, default=lambda self: _('New'))
    date = fields.Date(string="Registration Date")
    f_name = fields.Char(string="First Name")
    l_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father's Name")
    mother = fields.Char(string="Mother's Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")
    address = fields.Char(string="Communication Address")
    same_as_communication = fields.Boolean(string="permanent address same as communication address")
    permanent_address = fields.Char(string="Permanent Address")
    gender = fields.Selection(string='Gender',
                              selection=[('male', 'Male'),
                                         ('female', 'Female'),
                                         ('others', 'Others')],)
    dob = fields.Date(string="Date of Birth")
    aadhar_no = fields.Integer(string="Aadhaar Number")
    photo = fields.Binary("Passport size photo", attachment=True,
                                    help="This field holds the image used for registration")
    previous_dept_id =fields.Many2one('department',string='Previous academic department')
    previous_class_id = fields.Many2one( 'class',string="Previous Class",domain="[('cls_department_id','=',previous_dept_id)]")
    tc = fields.Binary(string="TC" )
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('registered', 'Registered')], default="draft", track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='School')
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    club_ids = fields.Many2many('school.club', string='Club')
    exam_ids = fields.Many2many('school.exam',string="Exams")
    class_id = fields.Many2one('class', string='class')
    attendance = fields.Selection(string='Attendance',
                                  selection=[('present', 'Present'),
                                             ('absent', 'Absent'), ])

    stu_ids = fields.One2many('school.leave', 'student_id', string='Students')

    _sql_constraints = [
        ('field_unique',
         'unique(aadhar_no)',
         'Choose another value - Aadhar_number is already exist!!!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """ Create a sequence for the student model """
        for vals in vals_list:
            if vals.get('reg_no', _('New')) == _('New'):
                vals['reg_no'] = (self.env['ir.sequence'].next_by_code('student.registration'))
        return super().create(vals_list)

    @api.constrains('email')
    def _check_email(self):
        """ To check the email address in a valid format """
        for rec in self:
            if rec.email:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                 rec.email)
                if match is None:
                    raise ValidationError('Not a valid E-mail ID')

    def action_registered(self):
        """  defining button action  """
        self.write({'state': 'registered'})


    @api.depends('dob')
    def _compute_age(self):
        """calculate age from Date of birth"""
        for rec in self:
            if rec.dob:
                d1 = self.dob
                d2 = date.today()
                rec.age = relativedelta(d2, d1).years

    @api.model
    def update_attendance(self):
        """update attendance automatically"""
        today = fields.Date.today()
        student_id = self.search([])
        for student in student_id:
            if self.env['school.leave'].search([('student_id', '=', student.id), ('date_from', '<=', today),
                                                      ('date_to', '>=', today)]):
                student.attendance = "absent"
            else:
                student.attendance = "present"

    @api.model
    def create_user(self):
        """creating new user from each student registration"""
        # print(self)
        user_vals = {
            'name': self.f_name,
            'email': self.email,
            'login': self.email,
        }
        user_id = self.env['res.users'].create(user_vals)
