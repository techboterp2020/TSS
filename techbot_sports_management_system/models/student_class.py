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
    state = fields.Selection([('draft', 'Draft'),
                              ('started', 'Started'),
                              ('completed', 'Completed'),
                              ('cancel', 'Cancelled')], string="Status", required=True, default='draft', tracking=True)
    start_date = fields.Date('From Date', default=fields.Date.today())
    from_to = fields.Date('To')
    # trainer_id = fields.Many2one('hr.employee', string='Instructor')
    activity_id = fields.Many2one('sports.activity.type', 'Activity')
    main_trainer_id = fields.Many2one('hr.employee', string='Instructor', required=True)
    assistant_trainer_id = fields.Many2one('hr.employee', string='Assistant Instructor', required=True)
    location_id = fields.Many2one('sports.location')
    repeat_type = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('month', 'Month')], string='Repeats',
                                   required=True, readonly=False)

    # compute='_compute_recurrence',
    mon = fields.Boolean(readonly=False)
    tue = fields.Boolean(readonly=False)
    wed = fields.Boolean(readonly=False)
    thu = fields.Boolean(readonly=False)
    fri = fields.Boolean(readonly=False)
    sat = fields.Boolean(readonly=False)
    sun = fields.Boolean(readonly=False)

    available_seat = fields.Float(string="Available Seats", required=True)
    filled_seats = fields.Integer(string="Filled seats", compute='_taken_seats')
    # students_id = fields.Many2many('student.details',  string="Students")
    students_ids = fields.One2many('student.details', 'class_id', string="Students", readonly=True)

    def draft(self):
        self.ensure_one()
        self.state = 'draft'

    def done(self):
        self.ensure_one()
        self.state = 'completed'

    def cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    """The End Date cannot be earlier than the Start Date"""
    # @api.constrains('from_date', 'from_to')
    # def _check_ending_date(self):
    #     for rec in self:
    #         if rec.from_to < rec.start_date:
    #             raise ValidationError(_('The End Date cannot be earlier than the Start Date.'))

    @api.depends('filled_seats', 'students_ids')
    def _taken_seats(self):
        for rec in self:
            if not rec.available_seat:
                rec.filled_seats = 0.0
            else:
                rec.filled_seats = 100.0 * len(rec.students_ids) / rec.available_seat

    @api.onchange('available_seat', 'students_ids')
    def _verify_valid_seats(self):
        if self.available_seat < 0:
            raise ValidationError(_("Incorrect 'seats' value , The number of available seats may not be negative"))
        if self.available_seat < len(self.students_ids):
            raise ValidationError(_("Too many Students, Please Increase seats or Remove excess Students"))

    no_of_session = fields.Integer(' No.of Session ', required=True)
    session_ids = fields.One2many('sports.management.session', 'class_id')

    def started_button(self):
        self.ensure_one()
        self.state = 'started'
        for i in range(0, self.no_of_session):
            self.session_ids = [
                (0, 0, {
                    'name': self.name,
                    'duration': 1.0,
                    'start_date': '1-2-3',
                })]

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
