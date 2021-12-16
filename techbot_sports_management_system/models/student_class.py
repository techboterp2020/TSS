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

import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
_logger = logging.getLogger(__name__)

class StudentClass(models.Model):
    """Defining a Parent relation with child."""

    _name = "student.class"
    _description = "Parent-child relation information"

    name = fields.Char("Name", required=True,
                       help='Parent relation with student')
    start_date = fields.Date('From Date', default=fields.Date.today())
    from_to = fields.Date('To', required="1")
    # trainer_id = fields.Many2one('hr.employee', string='Instructor')
    trainer_id = fields.Many2many('hr.employee', string='Instructor')
    location_id = fields.Many2one('sports.location')

    available_seat = fields.Float(string="Available Seats", required=True)
    filled_seats = fields.Integer(string="Filled seats",  compute='_taken_seats')
    # students_id = fields.Many2many('student.details',  string="Students")
    students_ids = fields.One2many('student.details', 'class_id', string="Students", readonly=True)
    # trainer_ids = fields.One2many('student.details',  'trainer_id', string='Instructor')

    # students_ids = fields.One2many('student.student', 'class_id')

    @api.constrains('from_date', 'from_to')
    def _check_ending_date(self):
        for rec in self:
            if rec.from_to < rec.start_date:
                raise ValidationError(_('The End Date cannot be earlier than the Start Date.'))

    @api.depends('filled_seats', 'students_ids')
    def _taken_seats(self):
        for rec in self:
            if not rec.available_seat:
                rec.filled_seats = 0.0
            else:
                rec.filled_seats = 100.0 * len(rec.students_ids) / rec.available_seat

    # def _default_students(self):
    #     return self.env['student.details'].browse(self._context.get('student_name'))

    # @api.onchange('available_seat', 'students_id')
    # def _get_students(self):
    #     student_obj = self.env['student.details']
    #     print("********************************************", student_obj)
    #     for rec in self:
    #         rec.students_id = student_obj.search([('class_id', '=', rec.id)])
    #         print(rec.students_id)
    #         # _logger.info("partner.vehicle_count %s", partner.vehicle_count)

        # student_ids = student_obj.search([('student_id', '=', self.id)]).mapped('id')
        #     sale_obj = self.env['sale.order']
        #     sale_ids = sale_obj.search([('partner_id', '=', self.id)]).mapped('id')
        #     sale_ids
        #     return {
        #         'domain': [('id', 'in', sale_ids)],
        #         'name': _('Sales'),
        #         'view_type': 'list',
        #         'view_mode': 'list,form',
        #         'res_model': 'sale.order',
        #         'view_id': False,
        #         'context': {'default_partner_id': self.id},
        #         'type': 'ir.actions.act_window'
        #     }


    @api.onchange('available_seat', 'students_ids')
    def _verify_valid_seats(self):
        if self.available_seat < 0:
            raise ValidationError(_("Incorrect 'seats' value , The number of available seats may not be negative"))
        if self.available_seat < len(self.students_ids):
            raise ValidationError(_("Too many Students, Please Increase seats or Remove excess Students"))


# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     child_count = fields.Integer(compute='_compute_child_count', string='Child qty')
#
#     # Fetch Student Details model
#     def get_child_details(self):
#         """
#         Return an action that display Student records related for the given partners.
#         """
#         child_obj = self.env['student.details']
#         child_ids = child_obj.search([('parent_id', '=', self.id)]).mapped('id')
#         return {
#             'domain': [('id', 'in', child_ids)],
#             'name': _('Children'),
#             'view_type': 'kanban',
#             'view_mode': 'kanban,tree,form',
#             'res_model': 'student.details',
#             'view_id': False,
#             'context': {'default_parent_id': self.id},
#             'type': 'ir.actions.act_window'
#         }
#
#     # COUNT THE STUDENT/CHILD W.R.T PARENT
#     def _compute_child_count(self):
#         """
#         Override original method to
#         """
#         child_obj = self.env['student.details']
#         for partner in self:
#             partner.child_count = child_obj.search_count([('parent_id', '=', partner.id)])
#             _logger.info("partner.child_count %s", partner.child_count)
#
#





