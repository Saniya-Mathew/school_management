# -*- coding: utf-8 -*-
from odoo import fields,models


class ManageClass(models.Model):
    """Displaying the details of the class"""
    _name = "class"
    _description = "Manage class"
    _inherit = 'mail.thread'

    name = fields.Char(string="Name of the class")
    cls_department_id = fields.Many2one('department',string="Department")
    company_id = fields.Many2one('res.company', string='School')
    hod_id = fields.Many2one(related='cls_department_id.hod_id')
