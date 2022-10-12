from odoo import api, fields, models, _

class Expense(models.Model):
    _inherit = "hr.expense"