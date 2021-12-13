# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
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

from odoo import api, fields, models, _
# import logging
from odoo.exceptions import ValidationError
from datetime import date


# _logger = logging.getLogger(__name__)
# WEEKDAY_SELECTION = [
#     ('MON', 'Monday'),
#     ('TUE', 'Tuesday'),
#     ('WED', 'Wednesday'),
#     ('THU', 'Thursday'),
#     ('FRI', 'Friday'),
#     ('SAT', 'Saturday'),
#     ('SUN', 'Sunday'),
# ]

class BloodGroup(models.Model):
    _name = 'blood.group'
    _description = 'Blood Group'
    _rec_name = 'blood_group'

    blood_group = fields.Char('Blood Group', help='Enter student blood group')

class SportsActivityType(models.Model):
    _name = 'sports.activity.type'
    _description = 'Sports Types'
    _rec_name = 'activity_name'

    activity_name = fields.Char(string="Activity Name")
    # location_id = fields.Many2many('sports.location')


class SportsLocation(models.Model):
    _name = 'sports.location'
    # _inherit = 'hr.employee'
    _description = "Activity Location Places"
    _rec_name = 'location_name'

    location_name = fields.Char(string="Location Name")
    # location_image = fields.Image()
    start_date = fields.Date('Start Date', default=date.today())
    end_date = fields.Date('End Date', required=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',
                                 default=lambda self: self.env.company.country_id, readonly=False, store=True)
    place = fields.Char('Near Place')

    # mon = fields.Boolean()
    # tue = fields.Boolean()
    # wed = fields.Boolean()
    # thu = fields.Boolean()
    # fri = fields.Boolean()
    # sat = fields.Boolean()
    # sun = fields.Boolean()
    # trainer_ids = fields.One2many('hr.employee', 'job_title', string="Trainers")
    # trainer_ids = fields.Many2one('hr.employee', string="Trainers")
    # trainer_ids = fields.Many2many('hr.employee', string="Trainers")

    @api.constrains('start_date', 'end_date')
    def _check_ending_date(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('The End Date cannot be earlier than the Start Date.'))
