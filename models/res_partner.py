# -*- coding: utf-8 -*-
from odoo import fields,models


class ResPartner(models.Model):
    """add a selection field to the inherited form view of res.partner"""
    _inherit = "res.partner"
    _description = "School Teacher"

    employee = fields.Selection(string='Employee',
                              selection=[('teacher', 'Teacher'),
                                         ('office staff', 'Office Staff'),
                                         ('student', 'Student')], )
    allowed_products = fields.Selection(string='Allowed Products',
                              selection=[('product', 'Product'),
                                         ('product_categories', 'Product Categories '),], )
    product_ids = fields.Many2many('product.product' ,string="Product")
    product_category_ids = fields.Many2many('product.category',string='Product Category')