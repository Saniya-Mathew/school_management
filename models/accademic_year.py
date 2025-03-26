# -*- coding: utf-8 -*-
from odoo import fields,models


class AcademicYear(models.Model):
    """showing the academic year details"""
    _name = "academic.year"
    _description = "Academic Year"

    name = fields.Char(string="Name ", required=True)


