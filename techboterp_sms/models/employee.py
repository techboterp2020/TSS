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
from odoo import models, fields, api, _
from datetime import date, datetime

class ResPartner(models.Model):
    _inherit = 'hr.employee'

    session_ids = fields.One2many("product.product", 'employee_id', string='Sessions')


class EmployeeSportsSession(models.Model):
    _name = 'employee.sports.session'
    _description = "Sports Management  Sessions"

    date_start = fields.Date('Start Date')
    s_created_date = fields.Date('Created Date')
    stop_date = fields.Datetime('Completed Date')
    student_ids = fields.Many2many('student.details', 'employee_student_rel', 'child_id', 'employee_id')
    product_id = fields.Many2one('product.product', string='Session')
    name = fields.Char(string='Name')
    employee_id = fields.Many2one('hr.employee', 'Main Trainer')
    assistant_employee_ids = fields.Many2many('hr.employee', 'employee_product_rel', 'employee_id', 'product_id', string='Assistant Trainer')
    state = fields.Selection([('draft','Draft'),('started','Started'),('completed','Completed')],default='draft',string='State')
    attendance_ids = fields.Many2many('student.details', 'session_student_rel', 'student_id', 'session_id')
    
    def session_start(self):
        for rec in self:
            rec.date_start = date.today()
            rec.state = 'started'
            
    def session_completed(self):
        for rec in self:
            rec.stop_date = datetime.now()
            rec.state = 'completed'
            if rec.product_id:
                rec.product_id.balance_session -= 1
            
            
            
    

