# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
_logger = logging.getLogger(__name__)

import ast

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv.expression import OR

class SaleOrder(models.Model):
    _inherit = "sale.order"

    client_req_date = fields.Datetime(
        string="Customer Requested",
        help="Enter the date the customer has asked for the product."
    )

    shipping_notes = fields.Text(
        string="Shipping Notes",
        help="These notes will be passed onto created Transfers."
    )

    so_tracking_number = fields.Text(
        string="Tracking Number",
        compute='_compute_so_tracking_number',
        store=False,
        help="Tracking numbers found on transfers"
    )
    @api.depends('picking_ids')
    def _compute_so_tracking_number(self):
        for rec in self:
            picking_ids = rec.picking_ids.filtered(lambda x: x.picking_type_id.code == 'outgoing' and x.carrier_tracking_ref)
            if picking_ids:
                rec.so_tracking_number = ', '.join(picking_ids.mapped("carrier_tracking_ref"))
            else:
                rec.so_tracking_number = False
