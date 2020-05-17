# See LICENSE file for full copyright and licensing details.


from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def count_limit(self):
        self.ensure_one()
        max_credit = False
        if self.amount_total > self.partner_id.final_max_limit:
            print("-------------grater blanmace-----------")
            if self.env.user.has_group('sales_team.group_sale_manager'):
                print("--------manager--------grp------")
                max_credit = self.amount_total - self.partner_id.final_max_limit 
                self.partner_id.final_max_limit += max_credit
                self.partner_id.balance_limit = 0
                print("--------self.partner_id.final_max_limit------------",self.partner_id.final_max_limit)
            else:
                raise  UserError(_('Opps! Only Manager Can approve for more than credit limits'))
        else:
            self.partner_id.balance_limit = self.partner_id.final_max_limit - self.amount_total
            print("----------self.partner_id.balance_limit-------------ELSE--",self.partner_id.balance_limit)

        payment_grid = self.env['payment.grid'].search([('sale_ref','=',self.name)])
        print("--------payment_grid-----------",payment_grid)
        if payment_grid:
            payment_grid.write({'sale_amount':self.amount_total,'credit_amount':self.amount_total,'inc_credit_limit':max_credit if max_credit else 0,
                                'max_credit_limit':self.partner_id.final_max_limit,'balanced_credit':self.partner_id.balance_limit})
        else:
            new_grid = self.env['payment.grid'].create({'sale_ref':self.name,'invoice_ref':'NA','payment_ref':'NA','sale_amount':self.amount_total,'credit_amount':self.amount_total,'inc_credit_limit':max_credit if max_credit else 0,
                                'max_credit_limit':self.partner_id.final_max_limit,'balanced_credit':self.partner_id.balance_limit})

            print("----------new_grid------------",new_grid)

        return True


    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.count_limit()
        return res


# class AccountInvoice(models.Model):
#     _inherit = 'account.invoice'

    # @api.multi
    # def write(self, values):
    #     print("------------self------------",self)
    #     result = super(AccountInvoice, self).write(values)
    #     print(result)
    #     print("------------values------------",values)
    #     print(a)

    #     if values.get('state') == 'open':
    #         print("-----------self------",self)
    #         for invoice in self:
    #             print(a)  

    #             sale_order_id = invoice.invoice_line_ids.mapped('sale_line_ids').order_id
    #             print("---------sale_order_id-------",sale_order_id)
    #             payment_grid = self.env['payment.grid'].search([('sale_ref','=',sale_order_id.name)])
    #             print("--------payment_grid-----------",payment_grid)
    #             print("-----self.amount_total>>>>>>>>>>>>>>>",invoice.payments_widget)
    #             invoice.partner_id.balance_limit += invoice.payments_widget
    #             print("---------invoice.partner_id.balance_limit------",invoice.partner_id.balance_limit)
    #             print(a)
    #             if payment_grid:
    #                 payment_grid.write({'invoice_ref':invoice.name,
    #                                     'balanced_credit':invoice.partner_id.balance_limit})
    #             # print(a)

        
    #     return result


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_validate_invoice_payment(self):
        res = super(AccountPayment, self).action_validate_invoice_payment()

        print("-----------invoice_ids----------",self.invoice_ids)
        # print(a)

        for invoice in self.invoice_ids:
            sale_order_id = invoice.invoice_line_ids.mapped('sale_line_ids').order_id
            print("---------sale_order_id-------",sale_order_id)
            payment_grid = self.env['payment.grid'].search([('sale_ref','=',sale_order_id.name)])
            print("--------payment_grid-----------",payment_grid)
            print("-----self.amount_total>>>>>>>>>>>>>>>",self.amount)
            print("-----self.amount_total>>>>>>>>>>>>>>>",self.payment_reference)
            # print(a)
            invoice.partner_id.balance_limit += self.amount
            print("---------invoice.partner_id.balance_limit------",invoice.partner_id.balance_limit)
            # print(a)
            if payment_grid:
                payment_grid.write({'invoice_ref':invoice.name,'payment_ref':self.name,
                                    'balanced_credit':invoice.partner_id.balance_limit})

        # self.mapped('payment_transaction_id').filtered(lambda x: x.state == 'done' and not x.is_processed)._post_process_after_done()
        return res