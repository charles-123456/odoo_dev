# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_inv_merge_pdf_report_ids = fields.Many2many(
        related="company_id.sh_inv_merge_pdf_report_ids",
        readonly=False,
        domain=
        "[('model', '=', 'account.move'),('report_type','=','qweb-pdf')]",
        string="Invoice Reports")
