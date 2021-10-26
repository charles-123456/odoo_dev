# -*- coding: utf-8 -*-
# © 2017 Sunflower IT (http://sunflowerweb.nl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from itertools import groupby
import time
from datetime import datetime

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)


class AccountInvoice(models.Model) :
    _inherit = 'account.move'

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

    report_analytic_lines = fields.One2many(comodel_name="account.analytic.line",
                                            inverse_name="timesheet_invoice_id", string="Analytic lines",
                                            help="The analytic lines coupled to this invoice.")
    report_timesheet_lines = fields.One2many(comodel_name="hr_timesheet.sheet", inverse_name='timesheet_invoice_id',
                                             string="Timesheet Line")
    hour_summary_invoice = fields.Boolean(string="Summary of Hours?", default=False)
    personal_info = fields.Boolean(string="Include Personal Info?", default=False)
    # submit_date = fields.Datetime(compute="onchange_submit_date", string="Submit Date")
    timesheet_sheet_id = fields.Many2one('hr_timesheet.sheet', string="Choose Timesheet Employee")
    status = fields.Selection([('Draft','Draft'), ('Paid', 'Paid'), ('cancel', 'Cancelled')], default='draft',
                              compute="compute_status")
    employee_no = fields.Char(string="Employee No")
    unit = fields.Char(compute="compute_unit")
    employee_name = fields.Char(string="Employee Name")
    account_pf_ids = fields.Many2many('pf.statutory','account_pf_rel','account_id','pf_id', string="PF")
    account_esi_ids = fields.Many2many('esi.statutory','account_esi_rel','account_id','esi_id', string="ESI")
    account_pt_ids = fields.Many2many('pt.statutory','account_pt_rel','account_id','pt_id', string="PT")
    inv_insurance_ids = fields.Many2many('insurance.statutory','inv_ins_rel','inv_id','ins_id', string="Insurance")
    # account_insurance_ids = fields.Many2many('insurance.statutory', string="Insurance",store=False)
    account_tds_ids = fields.Many2many('tds.statutory', string="TDS")
    document_day = fields.Integer()
    document_month = fields.Selection(MONTH_SELECTION)
    attachment_ids = fields.Many2many('ir.attachment',string="Timesheet Attachment")
    timesheet_inv_date = fields.Date(string="Invoice Date")

    @api.constrains('document_day')
    def validate_day(self):
        if self.document_day >31:
            raise UserError(_('Please enter the valid date !!!'))

    @api.depends('partner_id')
    def compute_unit(self):
        substring="-"
        if substring in self.partner_id.name:
            name = self.partner_id.name.split('-')
            print(name)
            self.unit = name[1]
        else:
            print('else called')
            self.unit =' '

    # date_start = fields.Date(related='timesheet_sheet_id.date_start')
    # date_start = fields.Date(string="Date Start")
    # date_end = fields.Date(related='timesheet_sheet_id.date_end')
    # date_end = fields.Date(string="Date End")
    # status = fields.Selection(related='timesheet_sheet_id.state')

    @api.depends('state')
    def compute_status(self) :
        for rec in self :
            if rec.state == 'draft' :
                rec.status = 'Draft'
            elif rec.state == 'posted' :
                rec.status = 'Paid'
            elif rec.state == 'cancel' :
                rec.status = 'cancel'

    # @api.depends('state')
    # def onchange_submit_date(self) :
    #     for rec in self :
    #         print('rec callled')
    #         if rec.state == 'posted' :
    #             rec.submit_date = fields.datetime.today()
    #         else :
    #             return False

    # @api.onchange('state')
    # def onchange_status(self):
    #     if self.state == 'draft':
    #         return self.status
    #     if self.state == 'posted':
    #         return self.status = 'invoiced'

    # value1 = fields.Text(string="Value1")
    def get_employee_name(self,inv_id):
        invoice=self.search([('id','=',inv_id)])
        timesheet_id = self.env['hr_timesheet.sheet'].search([('timesheet_invoice_id','=',invoice.id)])
        employee_name = timesheet_id.employee_id.name
        employee_joining= timesheet_id.employee_id.date_of_joining
        employee_id = timesheet_id.employee_id.employee_no
        po_no = timesheet_id.employee_id.po_no
        employee = [employee_name,employee_joining,employee_id,po_no]
        return employee


    def get_date(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        if invoice.timesheet_inv_date :
            result = datetime.strptime(str(invoice.timesheet_inv_date), '%Y-%m-%d')
            print('result', result)
            month = result.strftime("%B")
            year = result.strftime("%Y")
            final = month + " " + "(" + year + ")"
            return final
        else :
            return ''

    def get_contract_rate(self,inv_id):
        invoice = self.search([('id', '=', inv_id)])
        contract = invoice.invoice_line_ids.mapped('contract_rate')
        if contract:
            rate = contract[0]
            return rate
        else:
            return False


    def lines_per_project(self) :
        """ Return analytic lines per project """

        def grouplines(self, field='project_id') :
            for key, group in itertools.groupby(
                    self.sorted(lambda record : record[field].id),
                    lambda record : record[field]
            ) :
                yield key, sum(group, self.browse([]))

        analytic_lines = self.report_analytic_lines

        for issue, lines in grouplines(analytic_lines, 'project_id') :
            print('issue', issue)
            print('lines', lines)
            yield {'category' : issue, 'lines' : lines}

    def lines_timesheet_project(self) :
        """ Return analytic lines per project """

        def grouplines(self, field="add_line_project_id") :
            for key, group in itertools.groupby(
                    self.sorted(lambda record : record[field].id),
                    lambda record : record[field]
            ) :
                yield key, sum(group, self.browse([]))

        analytic_lines = self.report_timesheet_lines

        for issue, lines in grouplines(analytic_lines, "add_line_project_id") :
            print('issue', issue)
            print('lines', lines)
            yield {'category' : issue, 'lines' : lines}

    def get_hsn(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        values = invoice.invoice_line_ids.mapped('product_id.l10n_in_hsn_code')
        if values :
            all = values[0]
            return all
        else :
            return ''

    def get_pay_rate(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        employee = self.env['hr.employee'].search([('name','like',self.employee_name)])
        print('employee',employee)
        if len(employee)==1 :
            return employee.timesheet_cost
        else :
            return ''

    def get_amount(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        employee = self.env['hr.employee'].search([('name', 'like', self.employee_name)])
        print('employee', len(employee))
        hour = invoice.invoice_line_ids.mapped('quantity')
        length =len(employee)
        if length == 1 and hour :
            pay = employee.timesheet_cost
            hr = hour[0]
            return pay * hr
        else :
            return ''

    def get_hours(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        values = invoice.invoice_line_ids.mapped('quantity')
        if values :
            all_hour = values[0]
            return all_hour
        else :
            return ''

    def get_price_subtotal(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        values = invoice.invoice_line_ids.mapped('price_subtotal')
        if values :
            all_price_subtotal = values[0]
            return all_price_subtotal
        else :
            return ''

    def get_timesheet_date(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        all_timesheet = self.env['hr_timesheet.sheet'].search([('timesheet_invoice_id', '=', inv_id)])
        if all_timesheet :
            # print(all_timesheet.date_start)
            return all_timesheet.date_start

    def get_timesheet_end_date(self, inv_id) :
        invoice = self.search([('id', '=', inv_id)])
        all_timesheet = self.env['hr_timesheet.sheet'].search([('timesheet_invoice_id', '=', inv_id)])
        if all_timesheet :
            # print(all_timesheet.date_start)
            return all_timesheet.date_end

    # def get_timesheet_status(self, inv_id) :
    #     invoice = self.search([('id', '=', inv_id)])
    #     all_timesheet = self.env['hr_timesheet.sheet'].search([('timesheet_invoice_id', '=', inv_id)])
    #     if all_timesheet :
    #         # print(all_timesheet.date_start)
    #         return all_timesheet.state

    def get_gst(self, inv_id, product_id) :
        print('get_gst', inv_id)
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0

        for num in invoice.invoice_line_ids :
            if num.product_id.id == product_id :

                tax_rate = 0
                for i in num.tax_ids :

                    if i.children_tax_ids :
                        tax_rate = sum(i.children_tax_ids.mapped('amount'))

                tax_amount = ((tax_rate / 100) * num.price_subtotal) / 2
                rate = tax_rate / 2
        return [rate, tax_amount]

    def get_igst(self, inv_id, product_id) :
        invoice = self.search([('id', '=', inv_id)], limit=1)
        tax_amount = 0
        rate = 0
        for i in invoice.invoice_line_ids :
            if i.product_id.id == product_id :
                tax_rate = 0
                for t in i.tax_ids :
                    if not t.children_tax_ids :
                        tax_rate = t.amount
                tax_amount = (tax_rate / 100) * i.price_subtotal
                rate = tax_rate
        return [rate, tax_amount]

    # @api.onchange('timesheet_sheet_id')
    # def _all_timesheet_obj(self) :
    #     value1 = []
    #     value_y = []
    #     sheet_obj = self.env['hr_timesheet.sheet'].search(
    #         [('employee_id', '=', self.timesheet_sheet_id.employee_id.id)])
    #     for obj in sheet_obj.line_ids :
    #         if obj.value_x not in value1 :
    #             value1.append(obj.value_x)
    #         value_y.append(obj.unit_amount)
    #         # value_y = set(value_y)
    #         print('valuex', value1)
    #         print('valuey', value_y)
    #         print('length', len(obj.value_x))
    #         print('length', len(obj.value_y))
    #     self.value1 = value1
#
class HrEmplioyee(models.Model):
    _inherit="hr.employee"

    employee_no = fields.Char(string="Employee No")