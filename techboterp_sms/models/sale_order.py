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
from odoo import api, fields, models, api, _


# from odoo.exceptions import ValidationError,Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order Inherit'

    child_id = fields.Many2one('student.details' )
    age = fields.Char(string='Age', readonly=True, store=True )
    gender = fields.Char('Gender',readonly=True, store=True)

    @api.onchange('child_id')
    def onchange_child_details(self):
        """Method to Change gender and Age Based on Child Name"""
        for rec in self:
            rec.age = rec.gender = False
            if rec.child_id:
                rec.age = rec.child_id.age
                rec.gender = rec.child_id.gender

    @api.onchange('partner_id')
    def onchange_parent_id(self):
        """Method to Filter Children Based on Partner/Parent Name"""
        for rec in self:
            rec.child_id = False
            if rec.partner_id:
                return {'domain': {'child_id': [('parent_id', '=', rec.partner_id.id)]}}


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trainer_id = fields.Many2one('hr.employee', store=True)
    start_date = fields.Datetime("Start Date" , store=True)
    end_date = fields.Datetime("Start End", store=True)

    @api.onchange('product_id')
    def onchange_child_details(self):
        """Method to Change Trainer and Based on Products"""
        for rec in self:
            rec.trainer_id = rec.start_date = rec.end_date = False
            if rec.product_id:
                rec.trainer_id = rec.product_id.employee_id
                rec.start_date = rec.product_id.date_start
                rec.end_date = rec.product_id.date_end


# Changed The tree name Quantity to Seat
class SaleOrderLine(models.Model):
    _inherit = 'account.move'




