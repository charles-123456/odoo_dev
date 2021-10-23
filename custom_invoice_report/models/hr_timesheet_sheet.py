from odoo import fields,models,api,_

class HrTimesheetSheetInherit(models.Model):
    _inherit="hr_timesheet.sheet"
    timesheet_invoice_id = fields.Many2one('account.move', string="Invoice")

    customer_name_id= fields.Many2one('res.partner',string="Customer Name")
    account_analytic_id = fields.Many2one('account.analytic.account',string="Account Analytic Account")


    def compute_customer_name(self):
       print('project',self.line_ids.mapped('value_y'))
       all_project = self.line_ids.mapped('value_y')
       sep =""
       if all_project:
            project_split= all_project[0]
            # print('project_split',project_split)
            collect = []
            for val in project_split:
                # print('val',val)
                # print('type val',type(val))
                # print('before collect')
                all = collect.append(val)
                # print('after collect')
                # print('all',all)
                output = sep.join(collect)
                # print('output',output)
                # print('project',project)
                project_id = self.env['project.project'].search([('name','like',output)])
                # print('filtered project',project_id)
                if len(project_id) == 1:
                    # account_list =[]
                    # account_list.append([0,0,{'account_analytic_id':project_id.analytic_account_id.id}])
                    self.write({'customer_name_id':project_id.partner_id.id,
                                'account_analytic_id': project_id.analytic_account_id.id,
                              })
                    print('cusotmer_',self.customer_name_id.name)
            # else:
            #     self.customer_name_id = False


