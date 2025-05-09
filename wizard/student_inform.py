# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools import json_default
import json


class StudentInform(models.TransientModel):
    _name = "student.inform"
    _description = "Student Report"

    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    club_id = fields.Many2one('school.club',string='Club')

    def action_student_report(self):
        """Button function to Print normal Qweb report"""
        data = {
            'class_id': self.class_id.id,
            'dept_id': self.dept_id.id,
            'club_id': self.club_id.id,
        }
        return self.env.ref('school.action_report_student').report_action(self,data=data)

    def action_student_exel_report(self):
        """Button function to Print Excel report"""
        data = {
            'class_id': self.class_id.id,
            'dept_id': self.dept_id.id,
            'club_id': self.club_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data':
                {
                    'model': 'report.school.report_student_inform',
                    'options': json.dumps(data, default=json_default),
                    'output_format': 'xlsx',
                    'report_name': 'Student Excel Report',
                },
        }

