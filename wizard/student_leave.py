# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo.exceptions import UserError
from odoo import fields, models,api,_


class StudentLeaveInform(models.TransientModel):
    _name = "student.leave.inform"
    _description = "Student Report"

    student_id = fields.Many2one('student.registration', string='Student',
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
        """printing PDF report based on certain conditions"""

        query = """SELECT s.f_name,class_id,reg_no,date_from,date_to,reason FROM school_leave l
                INNER JOIN student_registration s ON l.student_id = s.id """
        where_clause = []

        if self.filter_by == 'month':
            where_clause.append("DATE_TRUNC('month', l.date_from) = DATE_TRUNC('month', CURRENT_DATE)")
        if self.filter_by == 'week':
            start_week = date.today() - timedelta(days=date.today().weekday())
            end_week = start_week + timedelta(days=6)
            where_clause.append("l.date_from BETWEEN '%s' AND '%s' " % (start_week, end_week))
        if self.filter_by == 'day':
            where_clause.append("l.date_from = CURRENT_DATE")
        if self.filter_by == 'custom' and self.date_from and self.date_to:
              where_clause.append("l.date_from >= '%s' AND l.date_to <= '%s'" % (self.date_from, self.date_to))
        if self.student_id:
            where_clause.append("l.student_id = '%s'" %( self.student_id.id))
        if self.class_id:
                where_clause.append("s.class_id = '%s'" % (self.class_id.id))
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data ={
            'student_id':self.student_id.f_name,
             'report': report
        }
        return self.env.ref('school.action_report_student_leave').report_action(self,data=data)





