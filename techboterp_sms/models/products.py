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
    _description = "Adding Trainers in Product Variant information"

    def _get_default_color(self):
        return randint(1, 11)
    employee_id = fields.Many2one('hr.employee','Main Trainer')
    assistant_employee_id = fields.Many2many(
        'hr.employee')  # 'employee_product_rel', 'hr_employee', "product_product_id"
    color = fields.Integer(string='Color', default=_get_default_color)

    # def create(self, vals):
    #     self._check_emplou(vals)
    #     return super(ProductProductVariants, self).create(vals)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    date_start = fields.Datetime('Date From')
    date_end = fields.Datetime('Date To')

class StockQuant(models.Model):
    _inherit = 'stock.quant'
