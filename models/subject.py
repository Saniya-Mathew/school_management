# -*- coding: utf-8 -*-
from odoo import fields,models


class Subject(models.Model):
    """Displaying the details about the subjects"""
    _name = "subject"
    _description = "Subject"
    _inherit = 'mail.thread'

    name = fields.Char(string="Name of the Subject")
    department_id= fields.Many2one('department',string="Department")
    pass_mark = fields.Integer(string="Passmark")
    max_mark = fields.Integer(string="Maximum Mark")
