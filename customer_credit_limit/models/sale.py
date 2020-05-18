# See LICENSE file for full copyright and licensing details.


from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # When sale entries confirms then calculate credits and create entry for payment grid
    @api.multi
    def count_limit(self):
        self.ensure_one()
        max_credit = False
        if self.amount_total > self.partner_id.final_max_limit:
            if self.env.user.has_group('sales_team.group_sale_manager'):
                max_credit = self.amount_total - self.partner_id.final_max_limit 
                self.partner_id.final_max_limit += max_credit
                self.partner_id.balance_limit = 0
            else:
                raise  UserError(_('Opps! Only Manager Can approve for more than credit limits'))
        else:
            self.partner_id.balance_limit = self.partner_id.final_max_limit - self.amount_total

        payment_grid = self.env['payment.grid'].search([('sale_ref','=',self.name)])
        if payment_grid:
            payment_grid.write({'sale_amount':self.amount_total,'credit_amount':self.amount_total,'inc_credit_limit':max_credit if max_credit else 0,
                                'max_credit_limit':self.partner_id.final_max_limit,'balanced_credit':self.partner_id.balance_limit})
        else:
            new_grid = self.env['payment.grid'].create({'sale_ref':self.name,'invoice_ref':'NA','payment_ref':'NA','sale_amount':self.amount_total,'credit_amount':self.amount_total,'inc_credit_limit':max_credit if max_credit else 0,
                                'max_credit_limit':self.partner_id.final_max_limit,'balanced_credit':self.partner_id.balance_limit})

        return True


    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.count_limit()
        return res



class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # When payment entry is made then calculate credit limits
    def action_validate_invoice_payment(self):
        res = super(AccountPayment, self).action_validate_invoice_payment()

        for invoice in self.invoice_ids:
            sale_order_id = invoice.invoice_line_ids.mapped('sale_line_ids').order_id
            payment_grid = self.env['payment.grid'].search([('sale_ref','=',sale_order_id.name)])
            invoice.partner_id.balance_limit += self.amount
            if payment_grid:
                payment_grid.write({'invoice_ref':invoice.name,'payment_ref':self.name,
                                    'balanced_credit':invoice.partner_id.balance_limit})

        return res