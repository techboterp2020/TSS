# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: TechbotErp(<https://techboterp.com/>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE , Version v1.0

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
# import logging
from random import randint
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
        required_age = 4
        for rec in self:
            rec.age = 0
            if rec.dob and rec.dob <= current_dt:
                start = rec.dob
                age_calc = int((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc
        #   Method to check age should be greater than 4
                if age_calc < required_age:
                    raise ValidationError(_(
                        "Age of student should be greater than %s years!" % ( \
                            required_age)))

    # @api.constrains('date_of_birth')
    # def check_age(self):
    #     '''Method to check age should be greater than 6'''
    #     current_dt = fields.Date.today()
    #     if self.dob:
    #         start = self.dob
    #         age_calc = ((current_dt - start).days / 365)
    #         # Check if age less than required age
    #         if age_calc < self.school_id.required_age:
    #             raise ValidationError(_(
    #                 "Age of student should be greater than %s years!" % ( \self.school_id.required_age)))
    # # @api.onchange('dob')
    # def _calculate_age(self):
    #     for rec in self:
    #         today = date.today()
    #         rec.age = int((today - rec.dob).days/365)

    def _get_default_color(self):
        return randint(1, 11)

    # student_id = fields.Char('ID')
    color = fields.Integer(string='Color', default=_get_default_color)
    student_name = fields.Char(string='Student Name')
    parent_id = fields.Many2one('res.partner', string='Parent Name', index=True)
    # domain=[('active', '=', True)]
    relationship = fields.Many2one('parent.relation')
    student_image = fields.Image('Image', compute_sudo=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male',
                              help='Select student gender')
    # states={'done': [('readonly', True)]},

    dob = fields.Date("DOB")
    #
    age = fields.Char(compute='_compute_student_age', string='Age',
                      readonly=True, help='Enter student age')
    mob = fields.Char('Mobile', compute='onchange_parent_id')
    mob1 = fields.Char('Phone', compute='onchange_parent_id')
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

    blood_group = fields.Many2one('blood.group', help='Enter student blood group')
    student_height = fields.Float('Height', help="Height in C.M")
    student_weight = fields.Float('Weight', help="Weight in K.G")

    remark = fields.Text('Remark', help='Remark can be entered if any')
    #  states={'done': [('readonly', True)]},
    # employee_id = fields.Many2one('hr.employee')
    trainer_id = fields.Many2many('hr.employee')

    comments = fields.Char()

    allergy = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        default='no', required=True,
        help="Does the Student Have any Allergy or Sensitivity to the medication/foods..etc, Please mention it if any.")
    cardiac_disease = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       default='no', required=True,
                                       help="Does the Student Suffer from any Cardiac Problem,Please mention it if any.")
    diabetic = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                default='no', required=True,
                                help=" Is the Student Diabetic ,Please mention it if any")
    hyper_tension = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                     default='no', required=True,
                                     help=" Does the Student any Hypertension ,Please mention it if any")

    asthmatic = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                 default='no', required=True,
                                 help=" Is the Student Asthmatic ,Please mention it if any")
    renal_problem = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                     default='no', required=True,
                                     help=" Does the Student Suffer from any renal problem,Please mention it if any")
    urinary_infection = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         default='no', required=True,
                                         help=" Did the Student Suffer previously from urinary tract infection")

    epilepsy = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                default='no', required=True,
                                help=" Does the Student Suffer from epilepsy/seizures ,Please mention it if any")
    g6pd = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                            default='no', required=True,
                            help=" Is the Student Suffering from G6PD deficiency,Please mention it if any")

    chronic_blood = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                     default='no', required=True,
                                     help=" Does the Student have any chronic blood disease (like Thalassemia,Anemia,Hemophilia..etc, Please mention it if any")

    epistaxis = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                 default='no', required=True,
                                 help=" Does the Student Suffer from Recurrent Epistaxis (Nasal bleeding) ")
    skin_problem = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    default='no', required=True,
                                    help=" Does the Student have any skin problems, Please mention it if any")
    eye = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                           default='no', required=True,
                           help=" Does the Student have any eye(opthalmology)problems (Visual Disturbances), Please mention it if any")
    previous_surgical = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         default='no', required=True,
                                         help=" Have any Surgical Procedure done, Please mention it if any")
