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
    start_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    trainer_id = fields.Many2one('hr.employee', string='Instructor')
    # instructor_id = fields.Many2one('res.partner', string='Instructor')
    activity_id = fields.Many2one('sports.activity.type', string='Course', ondelete='cascade', required=True)
    """
       ON DELETE CASCADE rule to your database which specifies that the child data gets deleted when the parent data is deleted.
           If you wanted the related child records should get deleted automatically, when the parent record is deleted.
           Take an example of Sale Order, if you want the Sale Order Lines should get deleted, when Sale order gets deleted.
       """
    attendee_ids = fields.Many2many('student.details', string="Attendees")
    active = fields.Boolean(default=True)

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')  #

    end_date = fields.Date(string="End Date", compute='_get_end_date', inverse='_set_end_date',store=True)  # c

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    color = fields.Integer()


    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            raise ValidationError(_("Too many attendees Please Increase seats or remove excess attendees"))




    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    # @api.constrains('trainer_id', 'attendee_ids')
    # def _check_instructor_not_in_attendees(self):
    #     for r in self:
    #         if r.trainer_id and r.trainer_id in r.attendee_ids:
    #             raise exceptions.ValidationError("A session's instructor can't be an attendee")




