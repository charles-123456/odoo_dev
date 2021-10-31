from odoo import models,fields,api
from odoo.tools import  float_round

class AccountMoveLineInherit(models.Model):
    _inherit ='account.move.line'

    contract_rate = fields.Float(string="Contract Rate")
    working_day = fields.Float(string="Working Day(Hrs/Days)")