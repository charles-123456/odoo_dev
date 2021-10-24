from odoo import models,fields,api,_


class PurchaseOrderInherit(models.Model):
    _inherit="purchase.order"

    insurance=fields.Selection([('cov_by_supplier','Covered By Supplier'),('cov_by_user','Covered By User(Corey)')])
    

    def get_gst(self, inv_id, product_id) :
        print('get_gst', inv_id)
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0

        for num in invoice.order_line :
            if num.product_id.id == product_id :

                tax_rate = 0
                for i in num.taxes_id :

                    if i.children_tax_ids :
                        tax_rate = sum(i.children_tax_ids.mapped('amount'))

                tax_amount = ((tax_rate / 100) * num.price_subtotal) / 2
                rate = tax_rate / 2
        return [rate, tax_amount]

    def get_igst(self, inv_id, product_id) :
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for i in invoice.order_line :
            if i.product_id.id == product_id :
                tax_rate = 0
                for t in i.taxes_id :
                    if not t.children_tax_ids :
                        tax_rate = t.amount
                tax_amount = (tax_rate / 100) * i.price_subtotal
                rate = tax_rate
        return [rate, tax_amount]
