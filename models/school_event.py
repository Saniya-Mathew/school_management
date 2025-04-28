# -*- coding: utf-8 -*-
from odoo import fields,models,api
from datetime import  timedelta


class SchoolEvent(models.Model):
    """displaying the event details """
    _name = "school.event"
    _description = "School event"
    _inherit = "mail.thread"

    name = fields.Char(string="Event Name")
    club_id = fields.Many2one('school.club', string="Organizing Club")
    event_date = fields.Date(string="Event Date")
    active = fields.Boolean(default=True)
    image = fields.Binary("Event picture", attachment=True)

    def write(self, vals):
        """archiving the record"""
        res= super().write(vals)
        today=fields.Date.today()
        for rec in self:
            if rec.event_date and rec.event_date < today:
                rec.action_archive()
            else:
                rec.action_unarchive()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.write({})
        return records

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