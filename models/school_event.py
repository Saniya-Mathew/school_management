# -*- coding: utf-8 -*-
import dateutil.utils
from odoo import fields,models,api
import datetime
from datetime import date, timedelta ,datetime


class SchoolEvent(models.Model):
    """displaying the event details """
    _name = "school.event"
    _description = "School event"
    _inherit = "mail.thread"

    name = fields.Char(string="Event Name")
    club_id = fields.Many2one('school.club', string="Organizing Club")
    event_date = fields.Date(string="Event Date")
    active = fields.Boolean(default=True)

    @api.onchange("event_date")
    def archive_record(self):
        """archiving the record"""
        if self.event_date != 0:
            today=fields.Date.today()
            if self.search([('event_date', '<',today)]):
                self.write({'active': False})
            else:
                self.write({'active': True})

    def action_send_mail(self):
        """button action to send email to all of the employee"""
        partner_ids = self.env['res.partner'].search([])
        template = self.env.ref('school.event_reminder_email')
        if template:
            for partner in partner_ids:
                template.send_mail(self.id, force_send=True,email_values={'email_from':'self.user_id.email',
                                                                          'email_to':partner.email})

    def send_email(self):
        """send email automatically"""
        records = self.search([])
        for rec in records:
            scheduled_day = rec.event_date - timedelta(days=2)
            if scheduled_day == fields.Date.today():
                partner_ids = self.env['res.partner'].search([])
                template = self.env.ref('school.event_reminder_email')
                if template:
                    for partner in partner_ids:
                        template.send_mail(self.id, force_send=True,
                                   email_values={'email_from': 'self.user_id.email','email_to': partner.email})