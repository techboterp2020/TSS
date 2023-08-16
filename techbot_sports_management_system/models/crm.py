# -*- coding: utf-8 -*-
#
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

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'Fetch place and Sports Activity Crm Lead'

    location_id = fields.Many2one('sports.location', help='Enter student Sports Location')
    program_id = fields.Many2one('sports.activity.type', string='Program', help='Enter student Sports Location')
