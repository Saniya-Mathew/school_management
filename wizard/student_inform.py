from odoo import fields, models,api


class StudentInform(models.TransientModel):
    _name = "student.inform"
    _description = "Student Report"

    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    club_id = fields.Many2one('school.club',string='Club')