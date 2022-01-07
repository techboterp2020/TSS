from odoo import models,fields,api, SUPERUSER_ID
import time
from datetime import datetime
from datetime import time as datetime_time


class AttendanceMarkingWiz(models.TransientModel):
    _name = "attendance.marking.wizard"
    _description = "Attendance Marking"
    
    def get_attendance_domain(self):
        if self.env.context.get('active_model',False) and self.env.context.get('active_model',False) == "employee.sports.session":
            active_record = self.env[self.env.context.get('active_model',False)].browse(self.env.context['active_id'])
            if active_record:
                return [('id','in',active_record.student_ids.ids)]
        return [('id','in',[])]
    
    attendance_ids = fields.Many2many('student.details', 'wiz_student_rel', 'student_id', 'wiz_id',domain=get_attendance_domain)

    def mark_attendance(self):
        active_record = self.env['employee.sports.session'].browse(self.env.context['active_id'])
        if active_record:
            active_record.write({'attendance_ids':[(6,0,self.attendance_ids.ids)]})
