# -*- coding: utf-8 -*-
from odoo import fields, models,api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta



class SchoolLeave(models.Model):
    """showing the details about student leaves"""
    _name = "school.leave"
    _inherit = "mail.thread"
    _description = "School Leave"
    _rec_name = 'student_id'


    student_id = fields.Many2one('student.registration', string='Student', required=True)
    stu_class = fields.Integer(string="Class")
    date_from = fields.Date('Start Date', copy=False, default=fields.Date.context_today, )
    date_to = fields.Date('End Date', copy=False)
    total_day = fields.Integer(string="Total number of days" , compute="_compute_total_day")
    half_day = fields.Integer(string="Half Day")
    reason = fields.Text(string="Reason")

    @api.depends('date_from', 'date_to')
    def _compute_total_day(self):
        """Method for compute number of leave without include sun and sat"""
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from <= rec.date_to:
                date_from = rec.date_from
                total_days = 0
                while date_from <= rec.date_to:
                    if date_from.weekday() < 5:
                        total_days += 1
                    date_from += timedelta(days=1)
                rec.total_day = total_days
            else:
                rec.total_day = 0