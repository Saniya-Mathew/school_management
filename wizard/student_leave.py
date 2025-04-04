from calendar import month

from certifi import where

from odoo import fields, models,api
from odoo.addons.test_convert.tests.test_env import record


class StudentLeaveInform(models.TransientModel):
    _name = "student.leave.inform"
    _description = "Student Report"

    student_id = fields.Many2one('student.registration', string='Student')
    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    filter_by = fields.Selection(string='Filter_by',
                              selection=[('month', 'Month'),
                                         ('weak', 'Weak'),
                                         ('day', 'Day'),
                                         ('custom','Custom')],)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date('End Date',)

    def action_print_report(self):

        query = """SELECT s.f_name,date_from,date_to FROM school_leave l
                INNER JOIN student_registration s ON l.student_id = s.id """
        where_clause = []

        if self.filter_by == 'month':
            where_clause.append("DATE_TRUNC('month', l.date_from) = DATE_TRUNC('month', CURRENT_DATE)")
        if self.filter_by == 'custom' and self.date_from and self.date_to:
              where_clause = "l.date_from >= '%s' AND l.date_to <= '%s'" % (self.date_from, self.date_to)
        if self.student_id:
            query += "AND l.student_id = '%s'" % self.student_id.id
        if self.class_id:
                query += " AND s.class_id = '%s'" % self.class_id.id
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query)
        report = self.env.cr.fetchall()
        data ={
            'student_id':self.student_id.f_name,
             'report': report
        }
        return self.env.ref('school.action_report_student_leave').report_action(self,data=data)





