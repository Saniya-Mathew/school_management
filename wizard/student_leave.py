from odoo import fields, models,api


class StudentLeaveInform(models.TransientModel):
    _name = "student.leave.inform"
    _description = "Student Report"

    student_id = fields.Many2one('student.registration', string='Student')
    class_id = fields.Many2one('class', string="Class")
    filter_by = fields.Selection(string='Filter_by',
                              selection=[('month', 'Month'),
                                         ('weak', 'Weak'),
                                         ('day', 'Day'),
                                         ('custom','Custom')],)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date('End Date',)

    def action_print_report(self):
        print(5)
        query = """ SELECT s.f_name, c.class_id, l.date, l.reason
                             FROM module_school.leave l
                             JOIN student.registration s ON l.student_id = s.id
                             JOIN class c ON l.class_id = c.id
                         """
        # report_data = self.env['school.action_report_student_leave'].fetch_report_data(query, [])
        print(10)
        return self.env.ref('school.action_report_student_leave').report_action(None)



