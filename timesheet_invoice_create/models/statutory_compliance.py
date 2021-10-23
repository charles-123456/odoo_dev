from odoo import fields,models,api,_
from odoo.exceptions import UserError

class StatutoryComplaince(models.Model):
     _name = "statutory.compliance"
     _description = "Maintain Statutory Compliance"
     _rec_name = 'name_seq'

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
     document_day = fields.Integer(default=1,required=True)
     document_month = fields.Selection(MONTH_SELECTION, required=True)
     name_seq = fields.Char(string="Name Sequence",required=True,copy=False,readonly=True,index=True,default=lambda self: _('New'))
     pf = fields.Many2many('pf.statutory',string="PF",required="True")
     esi = fields.Many2many('esi.statutory',string="ESI")
     pt = fields.Many2many('pt.statutory',string="PT")
     insurance = fields.Many2many('insurance.statutory',string="Insurance")
     tds = fields.Many2many('tds.statutory',string="TDS")
     company_id = fields.Many2one('res.company',string="Company")

     @api.constrains('document_day')
     def validate_day(self) :
          if self.document_day > 31 :
               raise UserError(_('Please enter the valid date !!!'))

     @api.model
     def create(self,vals):
          if vals.get('name_seq',_('New')) == _('New'):
               vals['name_seq'] =self.env['ir.sequence'].next_by_code('statutory.compliance') or _('New')
          result = super(StatutoryComplaince,self).create(vals)
          return result

class PfDocument(models.Model):
     _name ="pf.statutory"
     _rec_name = "pf_name"
     pf_doc = fields.Binary(string="PF Documents")
     pf_name =fields.Char(string="Pf Name")


class EsiDocument(models.Model) :
     _name = "esi.statutory"
     _rec_name = "esi_name"

     esi_doc = fields.Binary(string="ESI Documents")
     esi_name = fields.Char(string="Esi Name")


class InsuranceDocument(models.Model) :
     _name = "insurance.statutory"
     _rec_name = "insurance_name"

     insurance_doc = fields.Binary(string="Insurance Documents")
     insurance_name = fields.Char(string="Insurance Name")

class PtDocument(models.Model) :
     _name = "pt.statutory"
     _rec_name = "pt_name"

     pt_doc = fields.Binary(string="PT Documents")
     pt_name = fields.Char(string="PT Name")

class TDSocument(models.Model) :
     _name = "tds.statutory"
     _rec_name = "tds_name"

     tds_doc = fields.Binary(string="TDS Documents")
     tds_name = fields.Char(string="TDS Name")