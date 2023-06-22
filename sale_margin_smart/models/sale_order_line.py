# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
_logger = logging.getLogger(__name__)

import ast

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv.expression import OR


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom', 'product_uom_qty')
    def _compute_purchase_price(self):
        super()._compute_purchase_price()
        for line in self:
            if not line.product_id:
                line.purchase_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product_cost = line.product_id.standard_price #we only swap you for fifo, otherwise you take base val
            if line.product_id.categ_id.property_cost_method == 'fifo':
                #considerations for product value: stock_account/models/product.py
                #https://github.com/odoo/odoo/blob/facd44d0bd4352be3d0eb11a2675e7a518c97e59/addons/stock_account/models/product.py#L326
                if line.product_uom == line.product_id.uom_id:
                    qty_to_take_on_candidates = line.product_uom_qty
                else:
                    if line.product_uom.uom_type == 'bigger':
                        qty_to_take_on_candidates = line.product_uom_qty * line.product_uom.ratio
                    elif line.product_uom.uom_type == 'smaller':
                        qty_to_take_on_candidates = line.product_uom_qty / line.product_uom.ratio
                    else:
                        qty_to_take_on_candidates = line.product_uom_qty
                domain = [('product_id', '=', line.product_id.id),('remaining_qty', '>', 0),('company_id', '=', line.order_id.company_id.id)]
                candidates = self.env['stock.valuation.layer'].sudo().search(domain, order='id desc')
                sum_remaining_value = 0
                remaining_qty = qty_to_take_on_candidates
                if candidates:
                    candidate_unit_cost = 0
                    for candidate in candidates:
                        _logger.info(f'\n\n\n sum {sum_remaining_value} remaining_qty {remaining_qty}')
                        #set unit cost here to take the latest value
                        if not candidate_unit_cost: candidate_unit_cost = candidate.remaining_value / candidate.remaining_qty
                        if remaining_qty > 0:
                            if candidate.remaining_qty > remaining_qty:
                                sum_remaining_value += candidate.remaining_value
                                remaining_qty = 0
                            else:
                                #set unit cost here to take the earliest value
                                #candidate_unit_cost = candidate.remaining_value / candidate.remaining_qty
                                sum_remaining_value += candidate.remaining_value
                                remaining_qty -= candidate.remaining_qty
                    if remaining_qty > 0:
                        sum_remaining_value += candidate_unit_cost * remaining_qty
                    product_cost = sum_remaining_value / qty_to_take_on_candidates
            line.purchase_price = line._convert_price(product_cost, line.product_id.uom_id)
