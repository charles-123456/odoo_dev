from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model) :
    _inherit = "account.move"


    @api.depends('line_ids')
    def _compute_partner_tree_view(self) :
        for val in self :
            if not val.line_ids.partner_id :
                raise UserError(_('Please Choose directly created journal records !!! '))
            else:
                partner = val.line_ids.mapped('partner_id.id')
                val.write({'partner_id' : partner[-1]})
