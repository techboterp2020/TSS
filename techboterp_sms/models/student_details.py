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

class BloodGroup(models.Model):
    _name = 'blood.group'
    _description = 'Blood Group'
    _rec_name = 'blood_group'

    blood_group = fields.Char('Blood Group', help='Enter student blood group')


class StudentDetails(models.Model):
    _name = 'student.details'
    _description = "Children Details based on Parents"
    _rec_name = "student_name"

    # invoice_count = fields.Integer(compute='_compute_invoice_count', string='Child qty')

    def _get_default_color(self):
        return randint(1, 11)

    # def draft(self):
    #     self.ensure_one()
    #     self.state = 'draft'

    def confirm(self):
        self.ensure_one()
        self.state = 'confirm'

    state = fields.Selection([('draft', 'Draft'), ('invoice', 'Invoiced'),
                              ('confirm', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], string="Status", required=True, default='draft')

    # invoice_id = fields.Many2one('account.move')
    color = fields.Integer(string='Color', default=_get_default_color)
    student_image = fields.Image('Image', compute_sudo=True)
    # name = fields.Char('Student Number', size=64, required=True, default=_('New'))
    student_name = fields.Char(string='Student Name', required=1)
    parent_id = fields.Many2one('res.partner', string='Parent Name', required=1, index=True)
    relationship = fields.Many2one('parent.relation', string=" Parent Relation :")
    street = fields.Char('Street')
    street2 = fields.Char("Street2")
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True)
    city = fields.Char('City', readonly=False, store=True)
    state_id = fields.Many2one("res.country.state", string='State', readonly=False, store=True,
                               domain= "[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', readonly=False, store=True)
    mob = fields.Char('Mobile', compute='onchange_parent_id')
    mob1 = fields.Char('Phone', compute='onchange_parent_id')
    email = fields.Char('Email', compute='onchange_parent_id')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male',
                              help='Select student gender')
    nationality_id = fields.Many2one('res.country')
    dob = fields.Date("DOB", required=1)
    age = fields.Char(compute='_compute_student_age', string='Age',
                      readonly=True, help='Enter student age')
    contact_phone = fields.Char()
    contact_mobile = fields.Char()
    blood_group = fields.Many2one('blood.group', help='Enter student blood group')
    student_height = fields.Float('Height', help="Height in C.M")
    student_weight = fields.Float('Weight', help="Weight in K.G")
    remark = fields.Text('Remark', help='Remark can be entered if any')
    comments = fields.Char()
    # class_id = fields.Many2one('student.class')
    # class_id = fields.Many2many('student.class','student_class_rel','student_id','class_id')
    # trainer_id = fields.Many2many('hr.employee')
    # trainer_id2 = fields.Many2many('hr.employee', 'student_employee_rel', 'student_id', 'employee_id', 'Assistant Trainer')
    # session_student_id = fields.Many2one('sports.management.session')

    # currency_id = fields.Many2one('res.currency', string='Currency',
    #                               required=True, readonly=True,
    #                               states={'draft': [('readonly', False)]},
    #                               default=lambda self: self.env.company.currency_id.id)
    # total_invoiced = fields.Monetary( string="Total Invoiced",)
    # compute='_invoice_total', groups='account.group_account_invoice,account.group_account_readonly'
    # def _invoice_total(self):
    #     self.total_invoiced = 0
    #     if not self.ids:
    #         return True
    #
    #     all_partners_and_children = {}
    #     all_partner_ids = []
    #     for partner in self.filtered('id'):
    #         # price_total is in the company currency
    #         all_partners_and_children[partner] = self.with_context(active_test=False).search(
    #             [('id', 'child_of', partner.id)]).ids
    #         all_partner_ids += all_partners_and_children[partner]
    #
    #     domain = [
    #         ('partner_id', 'in', all_partner_ids),
    #         ('state', 'not in', ['draft', 'cancel']),
    #         ('move_type', 'in', ('out_invoice', 'out_refund')),
    #     ]
    #     price_totals = self.env['account.invoice.report'].read_group(domain, ['price_subtotal'], ['partner_id'])
    #     for partner, child_ids in all_partners_and_children.items():
    #         partner.total_invoiced = sum(
    #             price['price_subtotal'] for price in price_totals if price['partner_id'][0] in child_ids)

    # def action_view_partner_invoices(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
    #     action['domain'] = [
    #         ('move_type', 'in', ('out_invoice', 'out_refund')),
    #         ('partner_id', 'child_of', self.parent_id.id),
    #     ]
    #     action['context'] = {'default_move_type': 'out_invoice', 'move_type': 'out_invoice', 'journal_type': 'sale',
    #                          'search_default_open': 1}
    #     return action


    # def make_invoices(self):
    #     self.ensure_one()
    #     self.state = 'invoice'
    #     # for rec in self:
    #     invoice = self.env['account.move'].create({
    #         'move_type': 'out_invoice',
    #         'state': 'draft',
    #         'partner_id': self.parent_id.id,
    #         'invoice_date': datetime.now(),
    #         'invoice_line_ids': [(0, 0, {
    #             # 'product_id': self.product_a.id,
    #             # 'product_id': "Session'",
    #             'name': 'Session',
    #             'quantity': 4.0,
    #             'discount': 0.00,
    #             'price_unit': 100,
    #         })]
    #     })
    #     return invoice

    #  Automatically fetch student Address based on Parents
    @api.onchange('parent_id')
    def onchange_parent_id(self):
        """ Method to Fetch student address """
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
        for rec in self:
            required_age = 3
            current_dt = fields.Date.today()
            rec.age = 0
            if rec.dob and rec.dob < current_dt:
                start = rec.dob
                age_calc = int((current_dt - start).days / 365)
                #   Method to check age should be greater than 4
                if age_calc < required_age:
                    raise ValidationError(_(
                        "Age of student should be greater than %s years!" % ( \
                            required_age)))
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains('current_dt', 'dob')
    def _check_ending_date(self):
        """ Method to Restrict DOB should not be Greater than Current Date """
        current_dt = fields.Date.today()
        for rec in self:
            if current_dt < rec.dob:
                raise ValidationError(_('The DOB Date cannot be Greater than the Current Date.'))

    # @api.onchange('class_id')
    # def onchange_class_seate(self):
    #     """ Method to Restrict Add Students in A Class """
    #     for rec in self:
    #         rec.trainer_id = rec.trainer_id2 = False
    #             # [(5,0,0)]
    #         # if rec.class_id:
    #         #     """ Method to get Students Trainers in A Class """
    #         #     rec.trainer_id = [(6, 0, [rec.class_id.main_trainer_id.id])]
    #         #     # rec.trainer_id2 = [(6, 0, [rec.class_id.assistant_trainer_id.id])]
    #         #     # assistant_trainer_id rec.class_id.assistant_trainer_id.id
    #         #     if (rec.class_id.available_seat== (len(rec.class_id.students_ids.ids))):
    #         #         raise ValidationError(_("Too many Students, Please Increase seats or Remove excess Students"))
    #
    # # @api.onchange('class_id')
    # # def onchange_trainers(self):
    # #     """ Method to get Students Trainers in A Class """
    # #     for rec in self:
    # #         rec.trainer_id = rec.trainer_id2 = False
    # #         if rec.class_id:
    # #             rec.trainer_id = rec.class_id.main_trainer_id
    # #             rec.trainer_id2 = rec.class_id.assistant_trainer_id

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
