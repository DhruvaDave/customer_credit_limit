# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    final_max_limit = fields.Float('Final credit limit')
    balance_limit = fields.Float('Balance limit')

class payment_grid(models.Model):
    _name = 'payment.grid'

    sale_ref = fields.Char(string="Sale Ref.",required=True)
    invoice_ref = fields.Char(string="Invoice Ref.")
    payment_ref = fields.Char(string="Payment Ref.")
    sale_amount = fields.Float(string="Sale Amount")
    invoice_amount = fields.Float(string="Invoice Amount")
    payment_amount = fields.Float(string="Payment Amount")
    credit_amount = fields.Float(string="Credit Amount")
    inc_credit_limit = fields.Float(string="Inc. Credit Limit")
    max_credit_limit = fields.Float(string="Max Credit Limit")
    balanced_credit = fields.Float(string="Balance Credit")
