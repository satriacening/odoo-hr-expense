from odoo import fields, models


class HrDepartment(models.Model):
    """Inherit HR Department"""
    _inherit = 'hr.department'
    
    department_code = fields.Char()