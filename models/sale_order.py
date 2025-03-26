from odoo import fields,models


class SaleOrder(models.Model):
    """add a new state to the sale order """
    _description = "Sales Order"
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('admitted', 'Admitted')])
