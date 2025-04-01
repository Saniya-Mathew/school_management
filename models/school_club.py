# -*- coding: utf-8 -*-
from odoo import fields,models


class SchoolClub(models.Model):
    """"Displaying the Club Details"""
    _name = "school.club"
    _description = "School Club"
    _inherit = "mail.thread"

    name = fields.Char(string="Club Name")
    members_ids = fields.Many2many('student.registration', string="Members")


    def action_school_event(self):
        """ button triggering the event details"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.event',
            'view_type': 'form',
            'view_mode': 'list,form',
            'domain':[('club_id','=',self.id)],
        }