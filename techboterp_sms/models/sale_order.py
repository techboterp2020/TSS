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
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    child_id = fields.Many2one('student.details', required=True, store=True)
    age = fields.Char(string='Age', readonly=True, store=True)
    gender = fields.Char('Gender', readonly=True, store=True)

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

    def action_confirm(self):
        for rec in self:
            """Method to Add Children into Product Variant based on Sale order Confirmation"""
            for line in rec.order_line:
                if line.product_id.balance_session > 0:
                    raise UserError("This Session is already in Progress")
                if rec.child_id and rec.child_id.id in line.product_id.student_id.ids:
                    raise UserError("The Student is Already added in the session")
            res = super(SaleOrder, self).action_confirm()
            for line in rec.order_line:
                line.product_id.student_id = [(4, rec.child_id.id)]
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    trainer_id = fields.Many2one('hr.employee', store=True)
    #  Remove the start date and end Dare in Sale order Lines
    # start_date = fields.Datetime("Start Date" , store=True)
    # end_date = fields.Datetime("Start End", store=True)

    @api.onchange('product_id')
    def onchange_child_details(self):
        """Method to Change Trainer and Based on Products in Sale order Lines"""
        for rec in self:
            # rec.trainer_id = rec.start_date = rec.end_date = False
            rec.trainer_id = False
            if rec.product_id:
                rec.trainer_id = rec.product_id.employee_id
                # rec.start_date = rec.product_id.date_start
                # rec.end_date = rec.product_id.date_end
