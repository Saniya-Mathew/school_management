# -*- coding: utf-8 -*-
from odoo import fields, models,_
from odoo.exceptions import UserError


class StudentInform(models.TransientModel):
    _name = "student.inform"
    _description = "Student Report"

    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    club_id = fields.Many2one('school.club',string='Club')

    def action_student_report(self):
        """printing student report based on some conditions"""

        query = """SELECT f_name,date FROM student_registration s 
                    INNER JOIN school_club_student_registration_rel rel
                    ON s.id = rel.student_registration_id"""
        where_clause = []
        params = []
        if self.class_id:
            where_clause.append("class_id = %s")
            params.append(self.class_id.id)
        if self.dept_id:
            where_clause.append("dept_id = %s")
            params.append(self.dept_id.id)
        if self.club_id:
            where_clause.append('rel.school_club_id = %s')
            params.append(self.club_id.id)
        if where_clause:
                query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query,params)
        report = self.env.cr.fetchall()
        data = {
            'report': report
        }
        return self.env.ref('school.action_report_student').report_action(self, data=data)

