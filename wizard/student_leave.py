# -*- coding: utf-8 -*-
import json
import xlsxwriter

from odoo import fields, models,api,_
from odoo.tools import json_default


class StudentLeaveInform(models.TransientModel):
    _name = "student.leave.inform"
    _description = "Student Report"

    student_ids = fields.Many2many('student.registration', string='Student',
                                 domain="[('class_id','=',class_id)]")

    class_id = fields.Many2one('class', string="Class")
    filter_by = fields.Selection(string='Filter by',
                              selection=[('month', 'Month'),
                                         ('week', 'Week'),
                                         ('day', 'Day'),
                                         ('custom','Custom')],)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date('End Date',)

    def action_print_report(self):
        """printing PDF report"""
        # data=self.prepare_report_data()
        data = {
            'student_ids': self.student_ids.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'class_id': self.class_id.id,
            'filter_by': self.filter_by,
            'student name': ",".join(self.student_ids.mapped('f_name')),
        }
        return self.env.ref('school.action_report_student_leave').report_action(self,data=data)

    def action_print_exel_report(self):
        """Printing exel report"""
        data = {
            'student_ids': self.student_ids.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'class_id': self.class_id.id,
            'filter_by': self.filter_by,
            'student name': ",".join(self.student_ids.mapped('f_name'))
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.leave.inform',
                     'options': json.dumps(data,default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Leave Excel Report',
                     },
            'report_type': 'xlsx',
        }

