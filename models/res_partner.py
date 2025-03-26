# -*- coding: utf-8 -*-
from odoo import fields,models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "School Teacher"

    employee = fields.Selection(string='Employee',
                              selection=[('teacher', 'Teacher'),
                                         ('office staff', 'Office Staff'),
                                         ('student', 'Student')], )
