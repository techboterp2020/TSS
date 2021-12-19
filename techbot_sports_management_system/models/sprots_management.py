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

# import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,Warning
from datetime import datetime,date,timedelta

# _logger = logging.getLogger(__name__)

# class CrmLead(models.Model):
#     _inherit = 'crm.lead'

class SportManagement(models.Model):
    _name = 'sports.management'
    _description = "Sports Management System"

class Session(models.Model):
    _name = 'sports.management.session'
    _description = "Sports Management  Sessions"

    name = fields.Char(required=True)
    start_date = fields.Datetime(
        'Start Date', store=True)        # compute='_compute_dates', inverse='_inverse_dates')
    end_date = fields.Datetime(
        'End Date', store=True,  readonly=True)        # compute='_compute_dates', inverse='_inverse_dates')
    duration = fields.Float('Duration',  store=True)
    class_id = fields.Many2one('student.class')
    attendance_ids = fields.One2many('session.attendance.line','session_id')


class SessionAttendanceLine(models.Model):
    _name = 'session.attendance.line'
    _description = 'Session Attendance Line'

    student_id = fields.Many2one('student.details')
    attendance = fields.Boolean()
    remark = fields.Char('Remark')
    session_id = fields.Many2one('sports.management.session')

