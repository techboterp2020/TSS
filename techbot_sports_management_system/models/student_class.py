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
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class StudentClass(models.Model):
    """Defining a Parent relation with child."""
    _name = "student.class"
    _description = "Parent-child relation information"

    @api.depends('start_date', 'duration')
    def date_end_calculation(self):
        for record in self:
            record.end_date = False
            if record.start_date:
                record.end_date = record.start_date + timedelta((record.duration * 365) / (12 * 4))

    name = fields.Char("Name", required=True,
                       help='Parent relation with student')
    state = fields.Selection([('draft', 'Draft'),
                              ('started', 'Start'),
                              ('completed', 'Completed'),
                              ('cancel', 'Cancelled')], string="Status", required=True, default='draft', tracking=True)
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('To', compute='date_end_calculation', readonly=True, store=True)
    # trainer_id = fields.Many2one('hr.employee', string='Instructor')
    activity_id = fields.Many2one('sports.activity.type', 'Activity', store=True, )
    main_trainer_id = fields.Many2one('hr.employee', string='Instructor', required=True, store=True, )
    assistant_trainer_id = fields.Many2one('hr.employee', string='Assistant Instructor', required=True, store=True, )
    location_id = fields.Many2one('sports.location')
    available_seat = fields.Integer(string="Available Seats", required=True)
    filled_seats = fields.Integer(string="Filled seats", compute='_taken_seats')
    # students_id = fields.Many2many('student.details',  string="Students")
    students_ids = fields.One2many('student.details', 'class_id', string="Students", readonly=True)

    def draft(self):
        self.ensure_one()
        self.state = 'draft'
        # self.unlink()

    def done(self):
        self.ensure_one()
        self.state = 'completed'

    def cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    # """The End Date cannot be earlier than the Start Date"""
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
            raise ValidationError(
                _("Incorrect 'seats' value , The number of available seats may not be negative or Zero"))
        if self.available_seat < len(self.students_ids):
            raise ValidationError(_("Too many Students, Please Increase seats or Remove excess Students"))

    session_based_on = fields.Selection([('weekly', 'Weekly'), ('month', 'Month')], string='Session Type',
                                        required=True,
                                        default='weekly', readonly=False)

    # compute='_compute_recurrence',
    # mon = fields.Boolean(readonly=False)
    # tue = fields.Boolean(readonly=False)
    # wed = fields.Boolean(readonly=False)
    # thu = fields.Boolean(readonly=False)
    # fri = fields.Boolean(readonly=False)
    # sat = fields.Boolean(readonly=False)
    # sun = fields.Boolean(readonly=False)
    duration = fields.Integer(' No.of Class ', required=True)
    session_ids = fields.One2many('sports.management.session', 'class_id')
    number = fields.Char(string='Number')

    def class_start_button_fun(self):
        self.ensure_one()
        self.state = 'started'
        if not self.activity_id:
            raise UserError(_("Please enter proper Program/Activity"))
        if not self.location_id:
            raise UserError(_("Please Enter Proper Location"))
        if not self.start_date:
            raise UserError(_("Please enter proper Start Date"))
        if not self.available_seat or self.available_seat < 0:
            raise UserError(_("Please enter proper value for Available seats"))
        # if not self.session_id:
        #     raise UserError(_("Please enter proper Session"))
        if self.session_based_on == 'month':
            if not self.duration or self.duration < 0:
                raise UserError(_("Please enter proper value for Session Duration"))
        self.compute()

    def compute(self):
        for rec in self:
            for i in range(0, self.duration):
                if rec.session_based_on == 'month':
                    next_date = relativedelta(months=i)
                else:
                    next_date = relativedelta(days=7 * i)
                self.session_ids = [
                    (0, 0, {
                        'name': self.name,
                        'duration': 1.0,
                        'date_from': rec.start_date + next_date,

                    })]

class Session(models.Model):
    _name = 'sports.management.session'
    _description = "Sports Management  Sessions"

    number = fields.Char(string='Number')
    name = fields.Char(required=True, string='Session Name')
    date_from = fields.Datetime('Start date' , readonly=True)
    duration = fields.Float('Duration', store=True)
    trainer_id = fields.Many2many('hr.employee')
    class_id = fields.Many2one('student.class')
    attendance_ids = fields.One2many('session.attendance.line', 'session_id', computr='_compute_attendance_ids')
    start_time = fields.Datetime('Start Time', readonly=True)
    end_time = fields.Datetime('Start End Time', readonly=True)
    working_time = fields.Char('Total Working Time',compute='_compute_working_time')

    @api.depends('start_time','end_time')
    def _compute_working_time(self):
        for rec in self:
            difference = (rec.end_time - rec.start_time)
            rec.working_time = difference
            print(rec.working_time,'1747452875245dsfs5afc45saf5f5s4')
            # if rec.end_time:
            #     rec.working_time = datetime.time(rec.end_time - rec.start_time).hour

        # self.working_time= (self.end_time- self.start_time)
    state = fields.Selection([('draft', 'Draft'),
                              ('started', 'Start'),
                              ('completed', 'Completed'),
                              ('cancel', 'Cancelled')], string="Status", required=True, default='draft', tracking=True)

    def draft(self):
        self.ensure_one()
        self.state = 'draft'

    def start(self):
        self.ensure_one()
        self.state = 'started'
        self.start_time = datetime.now()
        student_obj = self.env['student.class']
        print(student_obj, '78558*********************')
        # student_ids = student_obj.search([('class_id', '=', self.id)]).mapped('id')
        # print((student_ids,'****************stsfgf******************'))

    # @api.multi
    @api.depends('class_id')
    def _compute_attendance_ids(self):
        for rec in self:
            # if i in range(0, rec.available_seat):
            #     self.attendance_ids= [
            #         (0, 0, {
            #             'attendance_ids': i*self.attendance_ids,
            #             # 'duration': 1.0,
            #             # 'date_from': rec.start_date + next_date,
            #
            #         })]
            rec.attendance_ids = rec.students_ids.ids
            print('rec.attendance_ids', rec.attendance_ids)
        self.start()

    def done(self):
        self.ensure_one()
        self.state = 'completed'
        self.end_time = datetime.now()


class SessionAttendanceLine(models.Model):
    _name = 'session.attendance.line'
    _description = 'Session Attendance Line'

    student_id = fields.Many2one('student.details')
    attendance = fields.Boolean()
    class_id = fields.Many2one('student.class')
    remark = fields.Char('Remark')
    session_id = fields.Many2one('sports.management.session')
