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
import dateutil.relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils
from dateutil.relativedelta import relativedelta
import time
import pytz
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'hr.employee'

    session_ids = fields.One2many("product.product", 'employee_id', string='Sessions')


class EmployeeSportsSession(models.Model):
    _name = 'employee.sports.session'
    _description = "Sports Management  Sessions"

    date_start = fields.Datetime('Start Date')
    s_created_date = fields.Date('Created Date')
    stop_date = fields.Datetime('Completed Date')
    working_time = fields.Float('Total Hours',  store=True,compute='_compute_working_time', readonly=True, tracking=4)
    student_ids = fields.Many2many('student.details', 'employee_student_rel', 'child_id', 'employee_id', string="Students")
    product_id = fields.Many2one('product.product', string='Session', readonly=True)
    name = fields.Char(string='Name')
    employee_id = fields.Many2one('hr.employee', 'Main Trainer')
    assistant_employee_ids = fields.Many2many('hr.employee', 'employee_product_rel', 'employee_id', 'product_id', string='Assistant Trainer')
    state = fields.Selection([('draft','Draft'),('started','Started'),('completed','Completed')],default='draft',string='State')
    attendance_ids = fields.Many2many('student.details', 'session_student_rel', 'student_id', 'session_id')
    notes = fields.Char('Internal Note')

    def session_start(self):
        for rec in self:
            rec.date_start = datetime.now()
            rec.state = 'started'
            
    def session_completed(self):
        for rec in self:
            rec.stop_date = datetime.now()
            if not self.attendance_ids:
                raise ValidationError("Please Mark The Students Attendance ")
            rec.state = 'completed'
            if rec.product_id:
                rec.product_id.balance_session -= 1
            if rec.product_id.balance_session == 0:
                rec.product_id.student_id = rec.product_id.employee_id = rec.product_id.assistant_employee_id = rec.product_id.no_of_class = False

    @api.depends('date_start', 'stop_date')
    def _compute_working_time(self):
        for rec in self:
            rec.working_time = False
            if rec.date_start and rec.stop_date:
                start_dt = fields.Datetime.from_string(rec.date_start)
                finish_dt = fields.Datetime.from_string(rec.stop_date)
                difference = dateutil.relativedelta.relativedelta(finish_dt, start_dt)
                """ Method to find total Hour """
                time_hour =(24*difference.days)+difference.hours+(difference.minutes/60)+(difference.seconds/3600)
                rec.working_time = time_hour