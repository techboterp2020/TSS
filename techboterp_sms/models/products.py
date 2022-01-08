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

from odoo import models, fields, api, _
from random import randint
from odoo.exceptions import UserError, ValidationError
from datetime import date


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_session = fields.Boolean(string='Session')

class ProductProductVariants(models.Model):
    _inherit = "product.product"
    _description = "Adding Trainers,students and Session details in Product Variant information"

    def _get_default_color(self):
        return randint(1, 11)

    date_start = fields.Date('Date From')
    date_end = fields.Date('Date To')
    employee_id = fields.Many2one('hr.employee', 'Main Trainer')
    student_id = fields.Many2many('student.details', 'product_student_rel', 'child_id', 'product_id')
    assistant_employee_id = fields.Many2many('hr.employee', string='Assistant Trainer')
    # 'employee_product_rel', 'hr_employee', "product_product_id"
    color = fields.Integer(string='Color', default=_get_default_color)
    no_of_class = fields.Integer(' Total Sessions  ', required=True)
    no_of_sessions = fields.Integer(' Sessions ', default=1, required=True)
    session_based_on = fields.Selection([('weekly', 'Weekly'), ('month', 'Month')], string='Session Type',
                                        required=True, default='weekly', readonly=False)

    # mon = fields.Boolean(readonly=False)
    # mon_time = fields.Float(string='Time')
    # tue = fields.Boolean(readonly=False)
    # tue_time = fields.Float(string='Time')
    # wed = fields.Boolean(readonly=False)
    # wed_time = fields.Float(string='Time')
    # thu = fields.Boolean(readonly=False)
    # thu_time = fields.Float(string='Time')
    # fri = fields.Boolean(readonly=False)
    # fri_time = fields.Float(string='Time')
    # sat = fields.Boolean(readonly=False)
    # sat_time = fields.Float(string='Time')
    # sun = fields.Boolean(readonly=False)
    # sun_time = fields.Float(string='Time')

    # additional fields added
    balance_session = fields.Integer('Balance Sessions',readonly=True)

    # session adding function
    def add_session(self):
        for rec in self:
            if not rec.employee_id or not rec.student_id or not rec.no_of_class:
                raise ValidationError("Please fill Trainers, Total Class and Students")
            if rec.employee_id == rec.assistant_employee_id:
                raise UserError("Instructors/ Assistant Trainers are same Please Choose Different Trainers")
            for i in range(0, rec.no_of_class):
                self.env['employee.sports.session'].create({'name':rec.name+'-'+str(i+1),
                                                            'employee_id': rec.employee_id and rec.employee_id.id or False,
                                                            'student_ids': [(6, 0, rec.student_id.ids)] or [],
                                                            'assistant_employee_ids': [(6, 0, rec.assistant_employee_id.ids)] or [],
                                                            'product_id': rec.id,
                                                            's_created_date': date.today()})
            rec.balance_session = rec.no_of_class
    
    def delete_students_button(self):
        """Method to delete M2M field details"""
        for rec in self:
            rec.student_id = [(5, 0, 0)]


