# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api


class resCompany(models.Model):
    _inherit = "res.company"

    sh_inv_merge_pdf_report_ids = fields.Many2many(
        comodel_name="ir.actions.report",
        relation="sh_inv_merge_pdf_company_report_rel",
        string="Invoice Reports")
