# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.cristo.tools import cris_tools


DAYS = []
for d in range(1, 32):
    DAYS.append((str(d), str(d)))

MONTHS = [
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

class EcclesiaDiocese(models.Model):
    _name = 'res.ecclesia.diocese'
    _description = 'Ecclesia Diocese'
    _inherit = ['mail.thread','image.mixin']
    
    def open_vicariates(self):
        action = self.env.ref('cristo.action_vicariate').read()[0]
        action.update({
            'domain': [('diocese_id','=',self.id)],
            'context': "{'default_diocese_id':%d}" % (self.id),
        })
        return action
    
    def open_parishes(self):
        action = self.env.ref('cristo.action_parish').read()[0]
        action.update({
            'domain': [('diocese_id','=',self.id)],
            'context': "{'default_diocese_id':%d}" % (self.id),
        })
        return action
    
    def open_families(self):
        action = self.env.ref('cristo.action_res_family').read()[0]
        action.update({
            'domain': [('diocese_id','=',self.id)],
            'context': "{'default_diocese_id':%d}" % (self.id),
        })
        return action
    
    def open_members(self):
        action = self.env.ref('cristo.action_res_member').read()[0]
        action.update({
            'domain': [('diocese_id','=',self.id),('member_type','=','member'),('membership_type','=','LT')],
            'context': "{'default_diocese_id':%d}" % (self.id),
        })
        return action
    
    def _compute_vicariate_count(self):
        for rec in self:
            rec.vicariate_count = self.env['res.vicariate'].sudo().search_count([('diocese_id', '=', rec.id)])
    
    def _compute_parish_count(self):
        self.parish_count = self.env['res.parish'].sudo().search_count([('diocese_id', '=', self.id)])
    
    def _compute_family_count(self):
        self.family_count = self.env['res.family'].sudo().search_count([('diocese_id', '=', self.id)])
        
    def _compute_member_count(self):
        self.member_count = self.env['res.member'].sudo().search_count([('diocese_id', '=', self.id),('member_type', '=', 'member'),('membership_type','=','LT')])
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    diocese_motto = fields.Char(string="Motto")
    establishment_date = fields.Date(string="Establishment Date")
    cathedral = fields.Char(string="Cathedral")
    history = fields.Html(string="History")
    diocese_logo = fields.Binary(string="Diocese Logo")
    income_type = fields.Selection([('income','Income Range'),('exact','Exact Range')], string="Income Type")
    feast_day = fields.Selection(DAYS, string="Feast Day")
    feast_month = fields.Selection(MONTHS, string="Feast Month")
    deputy_bishop_role_id = fields.Many2one('res.member.role', string='Deputy Bishop called as')
    vicariate_ids = fields.One2many('res.vicariate', 'diocese_id', string="Vicariates")
    parish_ids = fields.One2many('res.parish', 'diocese_id', string="Parishes")
    family_ids = fields.One2many('res.family','diocese_id', string="Family")
    current_bishop_id = fields.Many2one('res.member', string="Bishop", tracking=True)
    bishop_emeritus_id = fields.Many2one('res.member', string='Bishop Emeritus')
    patron_id = fields.Many2one('res.patron', string="Patron Saint")
    language_ids = fields.Many2many('res.languages', string="Languages")
    is_archdiocese = fields.Boolean(string="Is Archdiocese?")
    email = fields.Char(string="Email")
    website = fields.Char(string='Website Link')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="Fax")
    comment = fields.Text(string="Comment")
#   Address
    street = fields.Char(string="Street")
    zip = fields.Char(string="Zip")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')  
    
    vicariate_count = fields.Integer(compute="_compute_vicariate_count", string="Vicariates")
    parish_count = fields.Integer(compute='_compute_parish_count', string='Parishes')
    family_count = fields.Integer(compute='_compute_family_count', string='Families')
    member_count = fields.Integer(compute='_compute_member_count', string='Members')
    
    @api.constrains('establishment_date')
    def _validate_futuristic_est_date(self):
        if self.establishment_date:
            cris_tools.future_date_validation(self.establishment_date,field_name="Establishment date")
    
class Vicariate(models.Model):
    _name = 'res.vicariate'
    _description = 'Vicariate'
    _inherit = ['mail.thread','image.mixin']
     
    def open_parishes(self):
        action = self.env.ref('cristo.action_parish').read()[0]
        action.update({
            'domain': [('vicariate_id','=',self.id)],
            'context': "{'default_vicariate_id':%d,'default_diocese_id': %d}" % (self.id,self.diocese_id.id),
        })
        return action
    
    def open_families(self):
        action = self.env.ref('cristo.action_res_family').read()[0]
        action.update({
            'domain': [('vicariate_id','=',self.id)],
            'context': "{'default_vicariate_id':%d}" % (self.id),
        })
        return action
    
    def open_members(self):
        action = self.env.ref('cristo.action_res_member').read()[0]
        action.update({
            'domain': [('vicariate_id','=',self.id),('member_type','=','member'),('membership_type','=','LT')],
            'context': "{'default_vicariate_id':%d}" % (self.id),
        })
        return action
    
    def _compute_parish_count(self):
        self.parish_count = self.env['res.parish'].sudo().search_count([('vicariate_id', '=', self.id)])
    
    def _compute_family_count(self):
        self.family_count = self.env['res.family'].sudo().search_count([('vicariate_id', '=', self.id)])
        
    def _compute_member_count(self):
        self.member_count = self.env['res.member'].sudo().search_count([('vicariate_id', '=', self.id),('member_type','=','member'),('membership_type','=','LT')])
         
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")  
    establishment_date = fields.Date(string="Establishment Date")
    diocese_id = fields.Many2one('res.ecclesia.diocese', string="Diocese", required=True, ondelete="restrict")
    parish_ids = fields.One2many('res.parish','vicariate_id', string="Parish")
    email = fields.Char(string="Email")
    website = fields.Char(string='Website Link')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="Fax")
    comment = fields.Text(string="Comment")
#   Address
    street = fields.Char(string="Street")
    zip = fields.Char(string="Zip")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')  
    
    parish_count = fields.Integer(compute='_compute_parish_count', string='Parishes')
    family_count = fields.Integer(compute='_compute_family_count', string='Families')
    member_count = fields.Integer(compute='_compute_member_count', string='Members')
    
    @api.constrains('establishment_date')
    def _validate_futuristic_est_date(self):
        if self.establishment_date:
            cris_tools.future_date_validation(self.establishment_date,field_name="Establishment date")
    
class Parish(models.Model):
    _name = 'res.parish'
    _description = 'Parish/Mission Station'
    _inherit = ['mail.thread','image.mixin']
    _order = 'name'
    
    def open_families(self):
        action = self.env.ref('cristo.action_res_family').read()[0]
        action.update({
            'domain': [('parish_id','=',self.id)],
            'context': "{'default_parish_id':%d}" % (self.id),
        })
        return action
    
    def open_members(self):
        action = self.env.ref('cristo.action_res_member').read()[0]
        action.update({
            'domain': [('parish_id','=',self.id),('member_type','=','member'),('membership_type','=','LT')],
            'context': "{'default_parish_id': %d,'default_member_type': '%s','default_membership_type': '%s'}" % (self.id,'member','LT'),
        })
        return action
    
    def _compute_family_count(self):
        self.family_count = self.env['res.family'].sudo().search_count([('parish_id', '=', self.id)])
        
    def _compute_member_count(self):
        self.member_count = self.env['res.member'].sudo().search_count([('parish_id', '=', self.id),('member_type','=','member'),('membership_type','=','LT')])
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code") 
    diocese_id = fields.Many2one('res.ecclesia.diocese', string="Diocese",required=True, ondelete="restrict")
    vicariate_id = fields.Many2one('res.vicariate', string="Vicariate")
    establishment_date = fields.Date(string="Establishment Date")
    current_parishpriest_id = fields.Many2one('res.member', string="Parish Priest", tracking=True)
    history = fields.Html(string="History")
    parish_logo = fields.Binary(string="Parish Logo")
    language_ids = fields.Many2many('res.languages', string="Church in Regional Language")
    patron_id = fields.Many2one('res.patron', string="Patron", tracking=True)
    rite_id = fields.Many2one('res.rite', string="Rite")
    member_ids = fields.One2many('res.member', 'parish_id', string="Members")
    family_ids = fields.One2many('res.family','parish_id', string="Family")
    email = fields.Char(string="Email")
    website = fields.Char(string='Website Link')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="Fax")
    comment = fields.Text(string="Comment")
#   Address
    street = fields.Char(string="Street")
    zip = fields.Char(string="Zip")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')  
    
    family_count = fields.Integer(compute='_compute_family_count', string='Families')
    member_count = fields.Integer(compute='_compute_member_count', string='Members')
    
    @api.constrains('establishment_date')
    def _validate_futuristic_est_date(self):
        if self.establishment_date:
            cris_tools.future_date_validation(self.establishment_date,field_name="Establishment date")
