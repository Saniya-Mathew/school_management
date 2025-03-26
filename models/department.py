# -*- coding: utf-8 -*-
from odoo import fields, models


class Department(models.Model):
    """Displaying the department details"""
    _name = "department"
    _description = "Department"
    _inherit = 'mail.thread'

    name = fields.Char(string="Name of the Department", required=True)
    hod_id = fields.Many2one('res.partner', string="Head of the Department")


