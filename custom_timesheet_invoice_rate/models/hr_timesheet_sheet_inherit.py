from odoo import models,fields,api,_
from calendar import monthrange
from datetime import datetime,date

class HrTimesheetInherited(models.Model):
    _inherit ="hr_timesheet.sheet"

    @api.onchange('date_start','date_end')
    def calculate_days(self):
        start = self.date_start
        end = self.date_end
        total_days = end - start
        self.document_day = total_days.days+1

    @api.depends('no_of_unpaid_leave')
    def calculate_unpaid_leave(self):
        hr_leave_id =self.env['hr.leave'].search([('employee_id','in',[self.employee_id.id])])
        # print('hr_leave_id',hr_leave_id)
        days = 0
        for val in hr_leave_id:
            if val.holiday_status_id.name == 'Unpaid' and val.state == 'validate' :
                # print('val',val)
                days += val.number_of_days
                # if val.holiday_status_id.name == 'Client Paid Time Off' and val.state == 'validate':
                #     holiday =1
                #     self.client_holiday = holiday
        self.no_of_unpaid_leave = days
        # if self.employee_id.allocation_used_display:
        #     days = self.employee_id.allocation_used_display
        #     self.no_of_unpaid_leave = days
        # else:
        #     self.no_of_unpaid_leave = False
        # if int(self.employee_id.allocation_used_display) > 2:
        #    # print('self allocation_used_display',self.employee_id.allocation_used_display)
        #    days = 0
        #    for i in range(int(self.employee_id.allocation_used_display)):
        #        if i>1:
        #            days +=1
        #            self.no_of_unpaid_leave = days
        #        else:
        #             self.no_of_unpaid_leave = False
        # else:
        #     self.no_of_unpaid_leave = False

    @api.depends('client_holiday')
    def calculate_client_holiday(self):
        hr_leave_id = self.env['hr.leave'].search([('employee_id', 'in', [self.employee_id.id])])
        holiday = 0
        for val in hr_leave_id:
            if val.holiday_status_id.name == 'Client Paid Time Off' and val.state == 'validate' :
                holiday += val.number_of_days
        self.client_holiday = holiday

    @api.depends('no_of_working_day')
    def calculate_working_days(self):
        unpaid_leave = int(float(self.no_of_unpaid_leave))
        client_holiday = self.client_holiday
        if self.document_day > 0:
            work_day = (self.document_day - unpaid_leave) + client_holiday
            self.no_of_working_day = work_day
        else:
            self.no_of_working_day = False

    @api.depends('per_day_rate')
    def calculate_per_day_rate(self):
        po_rate = float(self.employee_id.po_rate)
        # print('po_rate',self.employee_id.po_rate)
        no_of_calender_day  = float(self.document_day)
        if int(po_rate) > 0 and int(no_of_calender_day) > 0 :
            working_days = round(po_rate / no_of_calender_day )
            self.per_day_rate = str(working_days)
        else:
            self.per_day_rate = False

    @api.depends('invoice_rate')
    def calculate_invoice_rate(self):
        no_of_working_day = int(self.no_of_working_day)
        # print('nofw',no_of_working_day)
        per_day_rate = int(self.per_day_rate)
        if int(no_of_working_day) > 0:
            invoice_rate = round(per_day_rate * no_of_working_day )
            # print('invoice rate',per_day_rate * no_of_working_day)
            self.invoice_rate = invoice_rate
        else:
            self.invoice_rate = False




    @api.depends('timesheet_ids')
    def customer_name_tree_view(self):
        self.customer_name =False
        for rec in self:
            if rec.timesheet_ids:
                project = rec.timesheet_ids.mapped('project_id')
                # print('project',project)
            if project:
                final_project = project[-1]
                # print('final_project',final_project)
                # print('final_project',final_project.name)
                customer_name = final_project.partner_id.name
                rec.customer_name = customer_name

    document_day = fields.Integer(compute='calculate_days',string="No of Calendar Day")
    no_of_leave_approved = fields.Integer(string="No of Leave Approve( Paid time off)",default=2,readonly=True)
    no_of_unpaid_leave = fields.Integer(strig="No of Unpaid Leave",compute='calculate_unpaid_leave')
    client_holiday = fields.Integer(string="Client Holiday",compute='calculate_client_holiday')
    no_of_working_day = fields.Char(string="No of Working Day",compute='calculate_working_days')
    per_day_rate = fields.Monetary(string="Per Day Rate",compute='calculate_per_day_rate')
    invoice_rate = fields.Monetary(string="Invoice Rate",compute='calculate_invoice_rate')
    customer_name = fields.Char(string="Customer Name",compute='customer_name_tree_view')
    currency_id = fields.Many2one('res.currency',string="Currency")