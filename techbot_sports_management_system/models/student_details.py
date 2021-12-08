# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
# import logging

from datetime import date, datetime, timedelta, time


# _logger = logging.getLogger(__name__)

class StudentDetails(models.Model):
    _name = 'student.details'
    _description = "Children Details based on Parents"
    _rec_name = "student_name"

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        for rec in self:
            rec.email = rec.mob = rec.mob1 = rec.street = rec.street2 = rec.city = rec.state_id = rec.zip = rec.country_id = False
            if rec.parent_id:
                rec.email = rec.parent_id.email
                rec.mob = rec.parent_id.phone
                rec.mob1 = rec.parent_id.mobile
                rec.street = rec.parent_id.street
                rec.street2 = rec.parent_id.street2
                rec.city = rec.parent_id.city
                rec.state_id = rec.parent_id.state_id
                rec.zip = rec.parent_id.zip
                rec.country_id = rec.parent_id.country_id

    @api.depends('dob')
    def _compute_student_age(self):
        """ Method to calculate student age """
        current_dt = fields.Date.today()
        for rec in self:
            rec.age = 0
            if rec.dob and rec.dob <= current_dt:
                start = rec.dob
                age_calc = int((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc
            #
            # else:
            #     raise ValidationError(_('Please Enter the Proper Date of Birth.'))

    # @api.onchange('dob')
    # def _calculate_age(self):
    #     for rec in self:
    #         today = date.today()
    #         rec.age = int((today - rec.dob).days/365)

    # student_id = fields.Char('ID')
    student_name = fields.Char(string='Student Name')
    parent_id = fields.Many2one('res.partner', string='Parent Name', index=True)
    # domain=[('active', '=', True)]
    student_image = fields.Image('Image')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male',
                              help='Select student gender')
    # states={'done': [('readonly', True)]},

    dob = fields.Date("DOB")
    #
    age = fields.Integer(compute='_compute_student_age', string='Age',
                         readonly=True, help='Enter student age')
    mob = fields.Char('Mobile', compute='onchange_parent_id')
    mob1 = fields.Char('Mobile', compute='onchange_parent_id')
    email = fields.Char('Email', compute='onchange_parent_id')

    street = fields.Char('Street')
    street2 = fields.Char("Street2")
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True)
    city = fields.Char('City', readonly=False, store=True)
    state_id = fields.Many2one(
        "res.country.state", string='State',
        readonly=False, store=True, domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', readonly=False, store=True)

    contact_phone = fields.Char()
    contact_mobile = fields.Char()

    blood_group = fields.Char('Blood Group', help='Enter student blood group')
    student_height = fields.Float('Height', help="Height in C.M")
    student_weight = fields.Float('Weight', help="Weight in K.G")
    eye = fields.Boolean('Eyes', help='Eye for medical info')
    ear = fields.Boolean('Ears', help='Eye for medical info')
    remark = fields.Text('Remark',  help='Remark can be entered if any')
    #  states={'done': [('readonly', True)]},
