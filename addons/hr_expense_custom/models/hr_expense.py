# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email.policy import default
from string import digits
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date
import re

from odoo import api, fields, models, _

class HrExpense(models.Model):
    _inherit = ['hr.expense']

    applicant_code = fields.Char(default=lambda self:self.env.user.name)
    department_code = fields.Char(string="Departemen Code")
    account = fields.Char(string="Account")
    # quantity = fields.Float(required=False, readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits='Product Unit of Measure', default=1)


    destination = fields.Char(string='Destination')
    froms = fields.Char(string='From')
    to = fields.Char(string='To')

    round_type = fields.Selection([
        ("oneway","Oneway"),
        ("return","Return")
    ])              
    payment_mode = fields.Selection(string="Payment", default="own_account", readonly=True)

    # total_amount = fields.Char(compute="_compute_amount")
    total_amounts = fields.Float(string="Amount", compute="_compute_amount", store=True, required=True, copy=True,
        states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits='Product Price')
    def _compute_amount(self):
        for expense in self:
            expense.total_amounts = expense.unit_amount


class HrExpenseSheet(models.Model):
    # _name = 'hr.expense.sheets'
    _inherit = ['hr.expense.sheet']

    user_id = fields.Many2one('res.users', 'Manager', compute='_compute_from_employee_id', store=True, readonly=True, copy=False, states={'draft': [('readonly', False)]}, tracking=True, domain=lambda self: [('groups_id', 'in', self.env.ref('hr_expense.group_hr_expense_team_approver').id)])
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company)
    payment_mode = fields.Selection(related='expense_line_ids.payment_mode', default='own_account', readonly=True, string="Paid By", tracking=True)

    employee_id = fields.Many2one()
    applicant_code = fields.Char(default=lambda self:self.env.user.name)
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user", copy=False)
    departement_code = fields.Char(string="Departemen Code")
    expense_type = fields.Char(string="Expense Type")
    account = fields.Char(string="Account")


    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    def action_submit_sheet(self):
        if self.attachment_number == 0:
            raise ValidationError(_("Attachments Required!"))
        super(HrExpenseSheet, self).action_submit_sheet()
    def action_register_payment(self):
        if self.attachment_number == 0:
            raise ValidationError(_('Attachment Required!!'))