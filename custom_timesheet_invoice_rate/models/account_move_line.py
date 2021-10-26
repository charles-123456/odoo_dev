from odoo import models,fields,api

class AccountMoveLineInherit(models.Model):
    _inherit ='account.move.line'

    contract_rate = fields.Float(string="Contract Rate")
