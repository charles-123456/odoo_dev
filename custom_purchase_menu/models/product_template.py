from odoo import fields,models,api,_

class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    used_for = fields.Selection([('one','XYZ'),('two','Second')],string="Used For")
    new_cost_price= fields.Float(string="Price Per Kg",compute="_compute_per_rate")
    user_id = fields.Many2one('res.users',string="User")
    partner_id=fields.Many2one('res.partner',string="Partner")

    @api.onchange('new_cost_price')
    def _compute_per_rate(self):
        for rec in self:
            rate= rec.qty_available*rec.standard_price
            rec.new_cost_price=rate

    def action_button(self):
        template_id = self.env.ref('custom_purchase_menu.email_template_edi_purchase_price_list').id
        print(template_id)
        all_id = self.search([])
        email=self.env['mail.template'].browse(template_id)
        print(email)
        print('all',all_id)
        values={}
        all_content=[]
        print('self',self)
        name=all_id.mapped('name')
        print('name',name)
        new_cost_price=all_id.mapped('new_cost_price')
        print(type(new_cost_price))
        qty_available=all_id.mapped('qty_available')
        print(type(qty_available))
        print('jjj',qty_available)
        used_for=all_id.mapped('used_for')


        values.update({'body_html':
                               "<table>"
                                "<tbody>"
                                    "<tr>"
                                        "<th style='width:135px'>Name</th>"
                                        "<th style='width: 85px;'>Price Per Kg</th>"
                                        "<th style='width: 125px;'>Available Quantity</th>"
                                        "<th style='width: 125px;'>Used For</th>"
                                    "</tr>"
                               "<t>"
                                "<tr>"
                                    "<td>{first}</td>"
                                    "<td style='text-align: center;'>{second}</td>"
                                    "<td></td>"
                                    "<td></td>"
                                "</tr>"
                               "</t>"
                            "</tbody>"
                        "</table>".format(first="\n".join(map(lambda x : str(x) or "", name)),second="\n".join(map(lambda x : str(x) or "",new_cost_price )))
                    })
        # all_content.append(values)
        # print('all_content',all_content)
        print('values',values)
        # for  val in all_content:
        #     print('val',val)
        # email.update(values)
        for rec in self:
            result=email.send_mail(rec.id, force_send=True)
            return  result

