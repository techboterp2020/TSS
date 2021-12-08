# -*- coding: utf-8 -*-

# import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,Warning

# _logger = logging.getLogger(__name__)

class SportManagement(models.Model):
    _name = 'sports.management'
    # _inherit = 'sale.subscription'
    _description = "Sports Management System"

    # vehicle_count = fields.Integer(compute='_compute_vehicle_count', string='Vehicles')
    #
    # def _compute_vehicle_count(self):
    #     """
    #     Override original method to
    #     """
    #     fleet_obj = self.env['fleet.vehicle']
    #     for partner in self:
    #         partner.vehicle_count = fleet_obj.search_count([('driver_id', '=', partner.id)])
    #         _logger.info("partner.vehicle_count %s", partner.vehicle_count)
    #
    # def get_partner_vehicles(self):
    #     """
    #     Return an action that display fleet records related for the given partners.
    #     """
    #     fleet_obj = self.env['fleet.vehicle']
    #     vehicle_ids = fleet_obj.search([('driver_id', '=', self.id)]).mapped('id')
    #     return {
    #         'domain': [('id', 'in', vehicle_ids)],
    #         'name': _('Vehicles'),
    #         'view_type': 'kanban',
    #         'view_mode': 'kanban,tree,form',
    #         'res_model': 'fleet.vehicle',
    #         'view_id': False,
    #         'context': {'default_driver_id': self.id},
    #         'type': 'ir.actions.act_window'
    #     }




