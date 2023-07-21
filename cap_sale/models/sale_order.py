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
