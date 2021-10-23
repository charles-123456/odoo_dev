from odoo import models,fields,api,_
from calendar import monthrange
from datetime import datetime

class PayslipInherit(models.Model):
    _inherit='hr.payslip'

    @api.onchange('date_from')
    def calculate_amount(self):
        for val in self.worked_days_line_ids:
            amount = self.contract_id.wage
            number_of_days = val.number_of_days
            date = datetime.strptime(str(self.date_from),"%Y-%m-%d")
            total_days = monthrange(date.year,date.month)[1]
            one_day_salary=amount/float(total_days)
            total_amount=number_of_days*one_day_salary
            val.write({'amount':total_amount})