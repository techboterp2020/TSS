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


class ProductProductVariants(models.Model):
    _inherit = "product.product"
    _description = "Adding Trainers,students and Session details in Product Variant information"

    def _get_default_color(self):
        return randint(1, 11)

    date_start = fields.Date('Date From')
    date_end = fields.Date('Date To')
    employee_id = fields.Many2one('hr.employee', 'Main Trainer')
    student_id = fields.Many2many('student.details', 'product_student_rel', 'child_id', 'product_id')
    assistant_employee_id = fields.Many2many(
        'hr.employee')  # 'employee_product_rel', 'hr_employee', "product_product_id"
    color = fields.Integer(string='Color', default=_get_default_color)
    no_of_class = fields.Integer(' Total Class  ', required=True)
    no_of_sessions = fields.Integer(' Sessions ', default=1, required=True)
    session_based_on = fields.Selection([('weekly', 'Weekly'), ('month', 'Month')], string='Session Type',
                                        required=True, default='weekly', readonly=False)

    mon = fields.Boolean(readonly=False)
    mon_time = fields.Float(string='Time')
    tue = fields.Boolean(readonly=False)
    tue_time = fields.Float(string='Time')
    wed = fields.Boolean(readonly=False)
    wed_time = fields.Float(string='Time')
    thu = fields.Boolean(readonly=False)
    thu_time = fields.Float(string='Time')
    fri = fields.Boolean(readonly=False)
    fri_time = fields.Float(string='Time')
    sat = fields.Boolean(readonly=False)
    sat_time = fields.Float(string='Time')
    sun = fields.Boolean(readonly=False)
    sun_time = fields.Float(string='Time')

    def delete_students_button(self):
        """Method to delete M2M field details"""
        for rec in self:
            rec.student_id = [(5, 0, 0)]
    #     self._check_emplou(vals)
    #     return super(ProductProductVariants, self).create(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'



class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # def _compute_timeframes(self, company):
    #     start_datetime = datetime.utcnow()
    #     tz_name = company.resource_calendar_id.tz
    #     if tz_name:
    #         start_datetime = pytz.timezone(tz_name).localize(start_datetime)
    #     return [
    #         (_('Last 24 hours'), (
    #             (start_datetime + relativedelta(days=-1), start_datetime),
    #             (start_datetime + relativedelta(days=-2), start_datetime + relativedelta(days=-1)))
    #         ), (_('Last 7 Days'), (
    #             (start_datetime + relativedelta(weeks=-1), start_datetime),
    #             (start_datetime + relativedelta(weeks=-2), start_datetime + relativedelta(weeks=-1)))
    #         ), (_('Last 30 Days'), (
    #             (start_datetime + relativedelta(months=-1), start_datetime),
    #             (start_datetime + relativedelta(months=-2), start_datetime + relativedelta(months=-1)))
    #         )
    #     ]
