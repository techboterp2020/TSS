# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    child_count = fields.Integer(compute='_compute_child_count', string='Child qty')

    # Fetch Student Details model
    def get_child_details(self):
        """
        Return an action that display Student records related for the given partners.
        """
        child_obj = self.env['student.details']
        child_ids = child_obj.search([('parent_id', '=', self.id)]).mapped('id')
        return {
            'domain': [('id', 'in', child_ids)],
            'name': _('Children'),
            'view_type': 'kanban',
            'view_mode': 'kanban,tree,form',
            'res_model': 'student.details',
            'view_id': False,
            'context': {'default_parent_id': self.id},
            'type': 'ir.actions.act_window'
        }

    # COUNT THE STUDENT/CHILD W.R.T PARENT
    def _compute_child_count(self):
        """
        Override original method to
        """
        child_obj = self.env['student.details']
        for partner in self:
            partner.child_count = child_obj.search_count([('parent_id', '=', partner.id)])
            _logger.info("partner.child_count %s", partner.child_count)







