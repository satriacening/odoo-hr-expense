from odoo import _, api, fields, models


class HRFuelPrice(models.Model):
    _name = 'hr.fuel.price'
    _description = 'HR Fuel Price'

    name = fields.Char(required=True)
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company)
    product_id = fields.Many2one(comodel_name='product.product', string='Related Expense Product', domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    fuel_price_line_ids = fields.One2many(comodel_name='hr.fuel.price.line',  inverse_name='fuel_price_id', string='Lines')

class HRFuelPriceLine(models.Model):
    _name = 'hr.fuel.price.line'
    _description = 'Line of fuel price'

    fuel_price_id = fields.Many2one(comodel_name='hr.fuel.price')
    name = fields.Char(related='fuel_price_id.name')
    company_id = fields.Many2one(comodel_name='res.company', related='fuel_price_id.company_id')
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    price = fields.Integer(required=True)
    