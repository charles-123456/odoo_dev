# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression
import base64
import tempfile
import os, sys, time
import subprocess
import imghdr
from odoo.http import request
import odoo

class Citizenship(models.Model):
    _name = "res.member.citizenship"
    _description = "Member Citizenship Status"
    
    name = fields.Char(string="Name", required=True)
    
class BloodGroup(models.Model):
    _name = "res.blood.group"
    _description = "Member Blood Group"
    _order = 'name'
    
    name = fields.Char(string="Name", required=True)

class MaritalStatus(models.Model):
    _name = "res.member.marital.status"
    _description = " Member Marital Status"
    
    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], string="Gender")
    
class Relationship(models.Model):
    _name = "res.member.relationship"
    _description = "Member Relationship"
    
    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], string="Gender")

class Occupation(models.Model):
    _name = 'res.occupation'
    _description = " Occupations"
    
    name = fields.Char(string="Name", required=True)
    
class HouseType(models.Model):
    _name = "res.house.type"
    _description = "House Type"
    
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")

class ResStudyLevel(models.Model):
    _name = 'res.study.level'
    _description = "Study Level"
    
    name = fields.Char(string="Name", required=True)
    study_level_code = fields.Char(string="Code", required=True, size=3)
    sequence = fields.Integer(string="Sequence")
    study_level_ids = fields.Many2many('study.level.member', string="Study Level hide for")
    
class ResMemberProgram(models.Model):
    _name = 'res.member.program'
    _description = "Member Program"
    
    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
    study_level_id = fields.Many2one('res.study.level', string="Study Level")
    
  
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('abbreviation', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))        

class Religion(models.Model):
    _name = "res.member.religion"
    _description = "Member Religion"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    
class MemberRole(models.Model):
    _name = "res.member.role"
    _description = "Member Role"
    
    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender')], string="Gender")
    abbreviation = fields.Char(string="Abbreviation")
    color = fields.Integer(string="Color Index")
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
#         if operator == 'ilike' and not (name or '').strip():
#             domain = []
        if self._context.get('search_all_role',False):
            domain = ['|', ('name', operator, name), ('abbreviation', operator, name)]
        else:
            domain = ['|', ('name', '=ilike', name), ('abbreviation', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))
    
class Patron(models.Model):
    _name = "res.patron"
    _description = "Patron"
    
    name = fields.Char(string="Name", required=True)
    feast_date = fields.Date(string="Feast Date")
    
class CoreDisiplines(models.Model):
    _name = "res.core.disiplines"
    _description = "Core Disiplines"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")

class Rite(models.Model):
    _name = "res.rite"
    _description = "Rite"
    
    name = fields.Char(string="Name", required=True)
    
class DiseaseDisorder(models.Model):
    _name = 'res.disease.disorder'
    _description = "Disease Disorder"
    
    name = fields.Char(string="Name", required=True)
    
class FormationStages(models.Model):
    _name = "res.formation.stage"
    _description = "Formation Stage"
    
    name = fields.Char(string="Name", required=True)
    
class Languages(models.Model):
    _name = "res.languages"
    _description = "Languages"
    _order = 'name'
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    enable_medium = fields.Boolean(string="Enable Medium")

class PartnerTitle(models.Model):
    _inherit = "res.partner.title"
    _description = "Partner Title"
    
    name = fields.Char(string="Title")
    shortcut = fields.Char(string="Abbreviation")
    for_bishop = fields.Boolean(string="For Bishop")
    for_priest = fields.Boolean(string="For Priest")
    for_brother = fields.Boolean(string="For Brother")
    for_deacon = fields.Boolean(string="For Deacon")
    for_sister = fields.Boolean(string="For Sister")
    for_novice = fields.Boolean(string="For Novice")
    for_member = fields.Boolean(string="For Member")
       
class PublicationType(models.Model):
    _name = "publication.type"
    _description = "Publication Type"
    
    name = fields.Char(string="Name")
    
class StudyLevelMember(models.Model):
    _name = "study.level.member"
    _description = "Study Level Member"
    
    name = fields.Char(string="Name")

class RenewalDocumentType(models.Model):
    _name = "renewal.doc.type"
    _description = "Renewal Document Type"
    
    name = fields.Char(string="Name", required=True)
    mail_template_id = fields.Many2one('mail.template',string="Mail Template")
    is_member = fields.Boolean(string="Is Member?")
    is_org = fields.Boolean(string="Is Org?")

class AnniversaryType(models.Model):
    _name = "anniversary.type"
    _description = "Anniversary Type"

    name = fields.Char(string="Name", required=True)
    is_priest = fields.Boolean(string="Is Priest")
    is_sister = fields.Boolean(string="Is Sister")
    is_layperson = fields.Boolean(string="Is Layperson")
    
class ResMonth(models.Model):
    _name = "res.month"
    _description = "Month"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    sequence = fields.Integer(string="Sequence")
        

