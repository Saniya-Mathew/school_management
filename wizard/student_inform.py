from odoo import fields, models


class StudentInform(models.TransientModel):
    _name = "student.inform"
    _description = "Student Report"

    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    club_id = fields.Many2one('school.club',string='Club')

    def action_student_report(self):
        """printing student report based on some conditions"""

        query = """SELECT f_name,date FROM student_registration s 
                    INNER JOIN school_club c ON s.student_id = c.members_ids.id"""
        if self.class_id:
            query += "WHERE class_id = '%s'" % self.class_id.id
        elif self.club_id:
            query += "student_id = '%s'" % self.club_id.id
        elif self.dept_id:
            query += "WHERE dept_id = '%s'" % self.dept_id.id


        self.env.cr.execute(query)
        report = self.env.cr.fetchall()
        data = {
            # 'student_id': self.student_id.f_name,
            'report': report
        }
        return self.env.ref('school.action_report_student').report_action(self, data=data)

