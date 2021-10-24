# -*- coding: utf-8 -*-
import base64

from odoo import fields, api, models, _
from datetime import datetime,date,timedelta
from odoo.addons.cristo.tools import cris_tools
from odoo.exceptions import UserError, ValidationError

YEAR = []
current_year = datetime.now().year
while(current_year >= 1900):
    YEAR.append((str(current_year), str(current_year)))
    current_year -= 1

DAYS = []
for d in range(1, 32):
    DAYS.append((str(d),str(d)))
    
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

class Member(models.Model):
    _name = 'res.member'
    _description = "Member"
    _inherit = 'image.mixin'
    
    @api.model
    def default_get(self, fields):
        data = super(Member, self).default_get(fields)
        user = self.env.user
        religion_id = self.env['res.member.religion'].search([('code','=', 'CAT')], limit=1)
        citizenship_id = self.env['res.member.citizenship'].search([('name', '=', 'Australian')], limit=1)
#         country_id = self.env['res.country'].search([('code', '=', 'AU')], limit=1)
        data['citizenship_id'] = citizenship_id.id
        data['religion_id'] = religion_id.id
#         data['country_id'] = country_id.id
        return data
    
    @api.constrains('dob')
    def _validate_future_dob_date(self):
        if self.dob:
            cris_tools.future_date_validation(self.dob)
    
    @api.constrains('bapt_date')
    def _validate_future_bapt_date(self):
        if self.bapt_date:
            cris_tools.future_date_validation(self.bapt_date,field_name="Baptism date")
    
    @api.constrains('fhc_date')
    def _validate_future_fhc_date(self):
        if self.fhc_date:
            cris_tools.future_date_validation(self.fhc_date,field_name="First Holy Communion date")
            
    @api.constrains('cnf_date')
    def _validate_future_cnf_date(self):
       if self.cnf_date:
           cris_tools.future_date_validation(self.cnf_date,field_name="Confirmation Date")
    
    @api.constrains('death_date')
    def _validate_future_death_date(self):
        if self.death_date:
            cris_tools.future_date_validation(self.death_date,field_name="Death Date")
    
    @api.constrains('dob','bapt_date')
    def _validate_bapt_date(self):
        if self.bapt_date and self.dob:
            if self.bapt_date < self.dob:
                raise UserError(_("Baptism date should not be lesser than Date of Birth."))
    
    @api.constrains('dob','mrg_date')
    def _validate_mrg_date(self):
        if self.mrg_date and self.dob:
            if self.mrg_date < self.dob:
                raise UserError(_("Marriage date should not be lesser than Date of Birth."))
            
    @api.constrains('fhc_date','bapt_date')
    def _validate_fhc_and_bapt_date(self):
        if self.fhc_date and self.bapt_date:
            if self.fhc_date < self.bapt_date:
                raise UserError(_("First Holy Communion date should not be lesser than Baptism Date."))
    
    @api.constrains('fhc_date','dob')
    def _validate_fhc_and_dob_date(self):
        if self.fhc_date and self.dob:
            if self.fhc_date < self.dob:
                raise UserError(_("First Holy Communion date should not be lesser than Date of Birth."))
    
    @api.constrains('bapt_date','cnf_date')
    def _validate_bapt_and_cnf_date(self):
        if self.bapt_date and self.cnf_date:
            if self.bapt_date > self.cnf_date:
                raise UserError(_("Confirmation date should not be lesser then Baptism date."))
        
    @api.constrains('cnf_date','dob')
    def _validate_cnf_and_dob_date(self):
        if self.cnf_date and self.dob:
            if self.cnf_date < self.dob:
                raise UserError(_("Confirmation date should not be lesser than Date of Birth."))
    
    @api.constrains('death_date','dob')
    def _validate_death_date(self):
        if self.death_date and self.dob:
            if self.death_date < self.dob:
                raise UserError(_("Death date should not be lesser than Date of Birth."))
    
    @api.depends('name','middle_name','last_name','title_id')
    def _compute_member_full_name(self):
        for mem in self:
            mem.member_full_name = False
            name = (mem.title_id.name+' '+mem.name) if mem.title_id else mem.name
            if name:
                name += ' '+mem.middle_name if mem.middle_name else ''
                if name:
                    name += ' '+mem.last_name if mem.last_name else ''
                    mem.member_full_name = name
                    
    name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    member_full_name = fields.Char(compute="_compute_member_full_name",string="Member Full Name",store=True)
    title_id = fields.Many2one('res.partner.title')
    member_code = fields.Char(string="Member #")
    monthly_income = fields.Float(string="Monthly Income")
    unique_code = fields.Char(string="User Identification No.")
    alias_name = fields.Char(string="Alias/Called As")
    gender = fields.Selection([('male','Male'),('female','Female'),('transgender','Transgender')],string="Gender")
    membership_type = fields.Selection([('LT','Lay Person'),('RE','Religious'),('SE','Secular Clergy')],string="Membership Type")
    member_type = fields.Selection([('member','Member'),('bishop','Bishop'),
                                     ('priest','Priest'),('deacon','Deacon'),
                                     ('lay_brother','Lay Brother'),('brother','Brother'),
                                     ('sister','Sister'), ('junior_sister', 'Junior Sister'),
                                     ('novice','Novice')], string="Member Type")
    living_status = fields.Selection([('yes','Yes'),('no','No')],string="Living Status", default='yes')
    occupation_id = fields.Many2one('res.occupation',string="Occupation")
    occupation_status = fields.Selection([('working','Working'),('not working','Not Working'),('retired','Retired'),('other','Other')])
    occupation_type  = fields.Selection([('govt','Government'),('pvt','Private'),('self','Self')],string="Occupation Type")
    dob = fields.Date(string="DOB")
    is_dob_or_age = fields.Selection([('dob','DOB'),('age','Age')],default="dob", string="Is DOB/Age?")
    age = fields.Integer(string="Age")
    religion_id = fields.Many2one('res.member.religion',required=True, ondelete="restrict", string="Religion")
    marital_status_id = fields.Many2one('res.member.marital.status', string="Marital Status")
    marital_status = fields.Char(related='marital_status_id.name', string="Marital Status")
    blood_group_id = fields.Many2one('res.blood.group',string="Blood Group")
    mother_tongue_id = fields.Many2one('res.languages',string="Mother Tongue")
    relationship_id = fields.Many2one('res.member.relationship', string="Relationship")
    citizenship_id = fields.Many2one('res.member.citizenship',string="Citizenship")
    diocese_id = fields.Many2one('res.ecclesia.diocese', string="Diocese")
    vicariate_id = fields.Many2one('res.vicariate', string="Vicariate")
    parish_id = fields.Many2one('res.parish',string="Parish")
    is_parish_member = fields.Selection([('yes','Yes'),('no','No')], string="Is Parish Member?", default='yes')
    present_diocese_id = fields.Many2one('res.ecclesia.diocese',string="Present Diocese")
    bapt_diocese_id = fields.Many2one('res.ecclesia.diocese',string="Diocese of Baptism")
    fhc_diocese_id = fields.Many2one('res.ecclesia.diocese', string="Diocese of Communion")
    cnf_diocese_id = fields.Many2one('res.ecclesia.diocese', string="Diocese of Confirmation")
    name_in_regional_language = fields.Char(string="Name in Regional Language")
    baptism_parish_id = fields.Many2one('res.parish',string="Parish of Baptism")
    baptism_diocese_id = fields.Many2one(related="baptism_parish_id.diocese_id", string="Bapt Diocese")
    bapt_date =  fields.Date(string="Date of Baptism")
    cnf_parish_id = fields.Many2one('res.parish',string="Parish of Confirmation")
    cnf_diocese_id = fields.Many2one(related="cnf_parish_id.diocese_id", string="CNF Diocese")
    cnf_date = fields.Date(string="Date of Confirmation")
    fhc_parish_id = fields.Many2one('res.parish',string="Parish of First Holy Communion")
    fhc_diocese_id = fields.Many2one(related="fhc_parish_id.diocese_id", string="FHC Diocese")
    fhc_date = fields.Date(string="Date of First Holy Communion")
    mrg_parish_id = fields.Many2one('res.parish', string="Parish of Marriage")
    mrg_diocese_id = fields.Many2one(related="mrg_parish_id.diocese_id", string="MRG Diocese")
    mrg_date = fields.Date(string="Date of Marriage")
    death_parish_id = fields.Many2one('res.parish', string="Parish of Death")
    death_date = fields.Date(string="Date of Death")
    native_diocese_id = fields.Many2one('res.ecclesia.diocese', string="Native Diocese")
    native_parish_id = fields.Many2one('res.parish', string="Native Parish")
    place_of_birth = fields.Char(string="Place of Birth")
    minister_of_baptism = fields.Char(string="Minister of Baptism")
    minister_of_cnf = fields.Char(string="Minister of Confirmation")
    minister_of_fhc = fields.Char(string="Minister of First Holy Communion")
    minister_of_marriage = fields.Char(string="Minister of Marriage")
    place_of_death = fields.Char("Death Place")
    passport_no = fields.Char(string="Passport No.", size=8)
    attachment_ids = fields.Many2many('ir.attachment', string="Attach Files")
    email = fields.Char(string="Email")
    website = fields.Char(string='Website Link')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="Fax")
    comment = fields.Text(string="Comment")
    family_id = fields.Many2one('res.family', string="Family")
    member_education_ids = fields.One2many('res.member.education','member_id',string="Education")
    profession_ids = fields.One2many('res.profession', 'member_id', string="Profession")
    holyorder_ids = fields.One2many('res.holyorder', 'member_id', string="Holy Order")
    
#   Address
    street = fields.Char(string="Street")
    zip = fields.Char(string="Zip")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    
    _sql_constraints = [
        ('uid_uniq', 'unique (unique_code)', "UID already exists. UID is Unique for a Member!"),
    ]
    
    @api.onchange('state_id')
    def _onchange_parish_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id.id
    
class ResMemberEducation(models.Model):
    _name = "res.member.education"
    _description = "Member Education"
    
    def check_binary_data(self,binary):
        if (len(binary) / 1024 / 1024) > 1:
            raise UserError(_("The maximum attachment upload size is 1 MB."))
        
    @api.constrains('attachment')
    def _validate_attachment(self):
        for rec in self:
            if rec.attachment:
                binary = base64.b64decode(rec.attachment or "")
                rec.check_binary_data(binary)
    
    @api.constrains('year_of_passing','member_id.dob')
    def _validate_year_of_passing(self):
        member_dob = self.member_id.dob.year
        for rec in self:
            if rec.year_of_passing < str(member_dob):
                raise UserError(_("Year of Passing should not be lesser than Date of Birth"))
    
    member_id = fields.Many2one('res.member', string='Member', ondelete='cascade')
    study_level_id = fields.Many2one('res.study.level', string='Study Level', required=True)
    program_id = fields.Many2one('res.member.program', string='Program', domain="[('study_level_id', '=', study_level_id)]")
    year_of_passing = fields.Selection(YEAR, string='Year of Passing')
    institution = fields.Char(string="Institution")
    note = fields.Text(string='Note')
    core_disiplines_ids = fields.Many2many('res.core.disiplines', string="Core Disiplines")
    particulars = fields.Char(string="Particulars")
    duration = fields.Float(string="Duration (in Years)")
    mode = fields.Selection([('regular','Regular'),('private','Private'),('not_applicable','Not Applicable')], string="Mode")
    result = fields.Char(string="Result")
    state = fields.Selection([('open','Active'),('done','Completed')],string="Status")
    member_type = fields.Char(string="Member Type")
    attachment = fields.Binary(string="Attachment")
    store_name = fields.Char(string="Name")
    board_or_university = fields.Char(string="Board / University")
    
class ResProfession(models.Model):
    _name = "res.profession"
    _description = "Profession"
    
    member_id = fields.Many2one('res.member', string='Member',ondelete="cascade")
    profession_date = fields.Date(string="Date", required=True)
    place = fields.Char(string="Place")
    type = fields.Selection([('first', 'First'),('renewal','Renewal'),('final','Final')], string="Type", required=True)
    years = fields.Integer(string="Years")
    state = fields.Selection([('open','Active'),('done','Completed')],string="Status")   
    
class ResHolyOrder(models.Model):
    _name = "res.holyorder"
    _description = "HolyOrder"
    
    member_id = fields.Many2one('res.member', string="Member",ondelete="cascade")
    date = fields.Date(string="Date", required=True)
    place = fields.Char(string="Place")
    order = fields.Selection([('lector','Lector'),('acolyte','Acolyte'),('deacon','Deacon'),('priest','Priest'),('bishop','Bishop')], string="Order", required=True)
    minister = fields.Char(string="Minister")    
    state = fields.Selection([('open','Active'),('done','Completed')],string="Status")
    
    
    
