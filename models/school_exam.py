# -*- coding: utf-8 -*-
from odoo import fields,models


class SchoolExam(models.Model):
    """Displaying the department details"""
    _name = "school.exam"
    _description = "School Exam"
    _inherit = 'mail.thread'

    name = fields.Char(string="Exam Name")
    exm_class_id = fields.Many2one( 'class',string="Class")
    paper =fields.Many2many('subject', string="Papers")
    stu_ids =fields.Many2many('student.registration',string="Student")

    def action_add_exam(self):
        """button action to add exam for the student """
        self.stu_ids = self.env['student.registration'].search([('class_id','=',self.exm_class_id.id)]).ids


