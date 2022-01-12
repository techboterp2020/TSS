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
    _description = ''

    child_id = fields.Many2one('student.details', store=True)

    @api.onchange('partner_id')
    def onchange_parent_id(self):
        """Method to Filter Children Based on Partner/Parent Name"""
        for rec in self:
            rec.child_id = False
            if rec.partner_id:
                return {'domain': {'child_id': [('parent_id', '=', rec.partner_id.id)]}}

