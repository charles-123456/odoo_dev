# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from datetime import datetime
from odoo.addons.cristo.tools import cris_tools
from odoo.exceptions import UserError

class Family(models.Model):
    _name = 'res.family'
    _description = "Family"
    _inherit = 'image.mixin'
    
    
    def open_members(self):
        action = self.env.ref('cristo.action_res_member').read()[0]
        action.update({
            'domain': [('family_id','=',self.id)],
            'context': {'default_family_id':self.id,'default_membership_type':'LT','default_member_type':'member'}
        })
        return action
    
    def _compute_member_count(self):
        self.member_count = self.env['res.member'].sudo().search_count([('family_id', '=', self.id),('membership_type','=','LT'),('member_type','=','member')])
    
    name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    reference = fields.Char(string='Family Card Number')
    child_ids = fields.One2many('res.member', 'family_id', string='Members')
    diocese_id = fields.Many2one('res.ecclesia.diocese', string='Diocese')
    vicariate_id = fields.Many2one('res.vicariate', string='Vicariate')
    parish_id = fields.Many2one('res.parish', string='Parish', required=True)
    is_civil_marriage = fields.Boolean(string='Civil Marriage?')
    is_church_marriage = fields.Boolean(string='Church Marriage?', default=False)
    civil_marriage_date = fields.Date(string='Civil Marriage Date')
    church_marriage_date = fields.Date(string='Church Marriage Date')
    family_register_number = fields.Char(string='Register Number', required=True)
    house_ownership = fields.Selection([('own', 'Own'), ('rent', 'Rent')], string='House Ownership', default="own")
    rent_amt = fields.Float(string='Rent Amount')
    settlement_status = fields.Selection([('family-permanent', 'Family-Permanent'), ('family-temporary', 'Family-Temporary'), ('single-permanent', 'Single-Permanent'), ('single-temporary', 'Single-Temporary')], default='family-permanent', required=True, string='Settled as')
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
      
    same_as_above_address = fields.Boolean(string="Same as above")
    permanent_street = fields.Char(string="Street")
    permanent_zip = fields.Char(string="Zip")
    permanent_city = fields.Char(string="City")
    permanent_state_id = fields.Many2one("res.country.state", string='State')
    permanent_country_id = fields.Many2one('res.country', string='Country')
    permanent_website = fields.Char("Permanent Website")
    permanent_phone = fields.Char("Permanent Phone(Landline)")
    permanent_mobile = fields.Char("Permanent Mobile")
    permanent_email = fields.Char("Permanent Email")
    register_date = fields.Date(string='Date of Registration', required=True, default=fields.Date.context_today)
    active_in_parish = fields.Boolean('Active in parish?', default=True, tracking=True)
    date_of_exit = fields.Date('Date of Exit', help="Date of exit from parish", default=fields.Date.context_today)
    inactive_parish_reason = fields.Char(string='Reason', help="Reason for inactive in parish")
    marriage_type = fields.Selection([
    ('C', 'Both Catholic'),
    ('F', 'Husband Catholic'),
    ('W', 'Wife Catholic'),
    ('E', 'Non Catholic but Christianism')
    ],string='Marriage Type')
    
    member_count = fields.Integer(compute='_compute_member_count', string='Members')
    
    @api.onchange('same_as_above_address')
    def onchange_same_as_above_address(self):
        if  self.same_as_above_address:
            self.permanent_street = self.street
            self.permanent_city = self.city
            self.permanent_state_id = self.state_id
            self.permanent_zip = self.zip
            self.permanent_country_id = self.country_id
        else:
            self.permanent_street = self.permanent_city = self.permanent_state_id = self.permanent_zip = self.permanent_country_id = False
    
    @api.onchange('register_date')
    def _validate_regiter_date(self):
        if self.register_date:
            cris_tools.future_date_validation(self.register_date,field_name="Registration Date")
            
    @api.constrains('permanent_mobile', 'permanent_country_id')
    def _check_permanent_mobile(self):
        if self.permanent_country_id.code == 'AU':
            if self.permanent_mobile:
                cris_tools.mobile_validation(self.permanent_mobile)
            
    @api.constrains('permanent_email')
    def _check_permanent_email(self):
        if self.permanent_email:
            cris_tools.email_validation(self.permanent_email)
    
    @api.constrains('civil_marriage_date')
    def _check_civil_marriage_date(self):
        if self.civil_marriage_date:
            cris_tools.future_date_validation(self.civil_marriage_date,field_name="Civil Marriage Date")
    
    @api.constrains('church_marriage_date')
    def _check_civil_marriage_date(self):
        if self.church_marriage_date:
            cris_tools.future_date_validation(self.church_marriage_date,field_name="Church Marriage Date")
        
        
        
        
        
    
    