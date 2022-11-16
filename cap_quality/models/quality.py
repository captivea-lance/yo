# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import ast

from datetime import datetime

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv.expression import OR

class QualityClause(models.Model):
    _name = "quality.clause"
    #this object should be existing in another module, don't need to create it.
    name = fields.Char(string='Name', required=False)
    description = fields.Char(string='Description', required=False)
    details = fields.Text(string='Details', required=False)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    #is this field already existing?
    quality_clauses = fields.Many2many(comodel_name="quality.clause", string="Quality Clause")

class QualityPoint(models.Model):
    _inherit = "quality.point"
    
    quality_clause = fields.Many2one("quality.clause", "Quality Clause")

    @api.model
    def _get_domain(self, product_ids, picking_type_id, measure_on='operation'):
        """ Helper that returns a domain for quality.point based on the products and picking type
        pass as arguments. It will search for quality point having:
        - No product_ids and no product_category_id
        - At least one variant from product_ids
        - At least one category that is a parent of the product_ids categories

        :param product_ids: the products that could require a quality check
        :type product: :class:`~odoo.addons.product.models.product.ProductProduct`
        :param picking_type_id: the products that could require a quality check
        :type product: :class:`~odoo.addons.stock.models.stock_picking.PickingType`
        :return: the domain for quality point with given picking_type_id for all the product_ids
        :rtype: list
        """
        
        domain = [('picking_type_ids', 'in', picking_type_id.ids)]
        domain_in_products_or_categs = ['|', ('product_ids', 'in', product_ids.ids), ('product_category_ids', 'parent_of', product_ids.categ_id.ids)]
        domain_no_products_and_categs = [('product_ids', '=', False), ('product_category_ids', '=', False)]
        domain += OR([domain_in_products_or_categs, domain_no_products_and_categs])
        domain += [('measure_on', '=', measure_on)]

        #CFS ticket 744 Quality Clause. Add clauses from product template and PO lines
        domain += ['|', (self.quality_clause.id, 'in', product_ids.quality_clauses.ids), (self.quality_clause, '=', False)]
        #raise UserError(domain) #picking_type_ids,in,,|,|,product_ids,in,,product_category_ids,parent_of,,&,product_ids,=,false,product_category_ids,=,false,measure_on,=,product,|,quality.clause(),in,quality.clause(),quality.clause(),=,false

        return domain
