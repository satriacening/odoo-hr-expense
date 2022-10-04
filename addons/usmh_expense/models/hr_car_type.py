from odoo import _, api, fields, models


class HRCarType(models.Model):
    _name = 'hr.car.type'
    _description = 'HR Car Type'

    name = fields.Char(required=True)
    fuel_type_id = fields.Many2one(comodel_name='hr.fuel.price')
    product_id = fields.Many2one(comodel_name='product.product', related='fuel_type_id.product_id')

    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company)
    