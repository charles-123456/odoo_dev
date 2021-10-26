from odoo import models,fields,api,_
from odoo.exceptions import UserError
from datetime import datetime

class TimesheetToInvoice(models.TransientModel):
    _name ="timesheet.sheet.to.invoice"

    MONTH_SELECTION = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    @api.constrains('document_day')
    def validate_day(self) :
        if self.document_day > 31 :
            raise UserError(_('Please enter the valid date !!!'))

    @api.model
    def _count(self):
        return len(self._context.get('active_ids',[]))

    def calulate_attachment(self,obj_id):
        # print('objid',obj_id)
        attachment = self.env['ir.attachment'].search([('res_id','=',obj_id)])
        # print('attachment',attachment)
        all = self.write({'attachment_ids':[[6, False,attachment.mapped(lambda att: att.id)]]})
        # print('all',all)
        # print('attachment_ids',self.attachment_ids)


    def create_invoice(self):
        inv_obj = self.env['hr_timesheet.sheet'].browse(self._context.get('active_ids',[]))
        print(inv_obj)
        for obj in inv_obj:
            var = [
                'Description:'+str(obj.name),
                'Project:'+str(obj.timesheet_ids.mapped('project_id.name')),
                'Task:'+str(obj.timesheet_ids.mapped('task_id.name')),
                'Amount:'+str(obj.total_time),
                'Date From:'+str(obj.timesheet_ids.mapped('date')),
                'Employee:'+str(obj.employee_id.name)]
            if self.is_task :
                if obj.employee_id.name:
                    var[0] = "Employee:" + str(obj.employee_id.name)
                else:
                    var[0]=''
            else:
                var[0] = ""
            if self.is_project :
                if obj.timesheet_ids.mapped('project_id.name') !=[] :
                     var[1] = 'Project:' + str(obj.timesheet_ids.mapped('project_id.name')[0])
                else:
                    var[1] =""
            else :
                var[1] = ""
            if self.is_task:
                if obj.timesheet_ids.mapped('task_id.name') !=[]:
                    var[2] = 'Task:' +str(obj.timesheet_ids.mapped('task_id.name')[0])
                else:
                    var[2]=""
            else :
                var[2] = ""
            if self.is_hour :
                if obj.total_time:
                    var[3] = 'Hour:' + str(obj.total_time)
                else:
                    var[3]=""
            else :
                var[3] = ""
            if self.is_date_from:
                if obj.timesheet_ids.mapped('date') !=[]:
                    var[4] = 'Date:' + str(obj.timesheet_ids.mapped('date')[0])
                else:
                    var[4]=""
            else:
                var[4]=""
            if self.is_description :
                if obj.name:
                    var[5] = 'Description:' + str(obj.name)
                else:
                    var[5]=""
            else :
                var[5] = ""
            while ("" in var):
                var.remove("")
            name = "\n".join(map(lambda x : str(x) or "", var))
            obj.compute_customer_name()
            self.calulate_attachment(obj.id)
            invoice_vals = {
                # 'ref' : obj.ref,
                # 'name': 'Draft',
                'move_type' : 'out_invoice',
                'l10n_in_gst_treatment':'regular',
                'invoice_origin' : obj.name,
                'invoice_date':datetime.now(),
                'invoice_user_id' : obj.user_id.id,
                'partner_id' : obj.customer_name_id.id,
                'journal_id':self.journal_id.id,
                'currency_id' : self.currency_id.id,
                'state':'draft',
                'employee_no':obj.employee_id.employee_no,
                'employee_name':obj.employee_id.name,
                'partner_bank_id':obj.company_id.partner_id.bank_ids[:1].id,
                'timesheet_inv_date':self.timesheet_inv_date,
                'invoice_line_ids' : [(0, 0, {
                    'name': name,
                    'contract_rate': obj.employee_id.po_rate,
                    'quantity' :obj.no_of_working_day,
                    'analytic_account_id':obj.account_analytic_id.id,
                    'price_unit':obj.per_day_rate,
                    'product_id' : self.invoice_product_id.id,
                    # 'product_uom_id' : obj.product_uom_id.id,
                })],
                'account_pf_ids':[[6, False,self.pf_ids.mapped(lambda pf: pf.id)]],
                'account_esi_ids':[[6, False,self.esi_ids.mapped(lambda esi: esi.id)]],
                'account_pt_ids':[[6, False, self.pt_ids.mapped(lambda pt: pt.id)]],
                'account_tds_ids':[[6, False, self.tds_ids.mapped(lambda pt: pt.id)]],
                'inv_insurance_ids':[[6, False,self.insurance_ids.mapped(lambda ins: ins.id)]],
                'attachment_ids':[[6, False,self.attachment_ids.mapped(lambda att: att.id)]],
                'document_day':self.document_day,
                'document_month':self.document_month,

            }
            print('values',invoice_vals)
            invoice_exist_check = obj.mapped('timesheet_invoice_id.id')
            duplicate = obj.search([('timesheet_invoice_id','in',invoice_exist_check)])
            # print('duplicate',duplicate)
            if duplicate:
                raise UserError(_('You Cannot create Invoice already timesheet invoiced record!!!'))
            else:
                 invoice =self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
            # print('invoice',invoice)
            invoice._compute_name()
            res=[]
            res.append((invoice.id,invoice.name))
            # print('res',res)
            # print('res[]',res[0])
            obj.write({'timesheet_invoice_id':res[0]})
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self' : invoice, 'origin' : obj},

                                           subtype_id=self.env.ref('mail.mt_note').id)

        return invoice



    count = fields.Integer(default=_count,readonly=True,string="Order Count")
    journal_id = fields.Many2one('account.journal',string="Journal")
    invoice_product_id = fields.Many2one('product.product',string="Invoice Product")
    currency_id = fields.Many2one('res.currency',string="Currency")
    is_project = fields.Boolean(string="Project",default=False)
    is_task = fields.Boolean(string="Task",default=False)
    is_description = fields.Boolean(string="Description",default=False)
    is_hour = fields.Boolean(string="Hour",default=False)
    is_date_from = fields.Boolean(string="Date",default=False)
    is_employee = fields.Boolean(string="Employee",default=False)
    merge = fields.Boolean(string='Merge', default=False)
    pf_ids = fields.Many2many('pf.statutory',string="PF")
    esi_ids = fields.Many2many('esi.statutory',string="ESI")
    pt_ids = fields.Many2many('pt.statutory',string="PT")
    insurance_ids = fields.Many2many('insurance.statutory',string="Insurance")
    tds_ids = fields.Many2many('tds.statutory',string="TDS")
    attachment_ids = fields.Many2many('ir.attachment',string="Attachments")
    document_day = fields.Integer(default=1,required=True)
    document_month = fields.Selection(MONTH_SELECTION,required=True)
    timesheet_inv_date = fields.Date(string="Invoice Date")
