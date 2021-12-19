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
    # _inherit = 'crm.lead'
    _description = "Sports Management System"


class Session(models.Model):
    _name = 'sports.management.session'
    _description = "Sports Management  Sessions"

    name = fields.Char(required=True)
    start_date = fields.Datetime(
        'Start Date', store=True)
        # compute='_compute_dates', inverse='_inverse_dates')
    end_date = fields.Datetime(
        'End Date', store=True,  readonly=True)
        # compute='_compute_dates', inverse='_inverse_dates')
    duration = fields.Float('Duration',  store=True)
    class_id = fields.Many2one('student.class')

    # @api.onchange('duration')
    # def onchange_end_time(self):
    #     for rec in self:
    #         print('***********************Duration', rec.duration)
    #         duration = datetime.strptime(rec.duration, '%Y-%m-%d %H:%M')
    #         print(duration,'******************************Dur')
    #         rec.end_date = rec.start_date
    #         + duration

    # @api.depends('start_date', 'end_date')
    # def _compute_duration(self):
    #     for rec in self:
    #         print(rec.start_date)
    #         print('95888******', rec.end_date)
    #         hour = rec.end_date-rec.start_date
    #         print(hour , "*****************Duration")
    #         rec.duration = hour

    # @api.constrains('start_date', 'end_date')
    # def _check_ending_date(self):
    #     """ Method to Restrict Start Date should not be Greater than the End Date """
    #     for rec in self:
    #         if (rec.end_date < rec.start_date):
    #             raise ValidationError(_('The End Date cannot be Less than the Start Date.'))

    def _compute_display_time(self):
        print('Meeting time')
        # for meeting in self:
