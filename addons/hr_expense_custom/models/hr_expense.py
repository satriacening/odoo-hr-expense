# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import Store
from email.policy import default
from string import digits
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date
import re

from odoo import api, fields, models, _

class HrExpense(models.Model):
    _inherit = ['hr.expense']

    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    @api.model
    def _get_employee_id_domain(self):
        res = [('id', '=', 0)] # Nothing accepted by domain, by default
        if self.user_has_groups('hr_expense.group_hr_expense_user') or self.user_has_groups('account.group_account_user'):
            res = "['|', ('company_id', '=', False), ('company_id', '=', company_id)]"  # Then, domain accepts everything
        elif self.user_has_groups('hr_expense.group_hr_expense_team_approver') and self.env.user.employee_ids:
            user = self.env.user
            employee = self.env.user.employee_id
            res = [
                '|', '|', '|',
                ('department_id.manager_id', '=', employee.id),
                ('parent_id', '=', employee.id),
                ('id', '=', employee.id),
                ('expense_manager_id', '=', user.id),
                '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id),
            ]
        elif self.env.user.employee_id:
            employee = self.env.user.employee_id
            res = [('id', '=', employee.id), '|', ('company_id', '=', False), ('company_id', '=', employee.company_id.id)]
        return res
    employee_id = fields.Many2one('hr.employee', compute='_compute_employee_id', string="Employee",
        store=True, required=True, readonly=False, tracking=True,
        states={'approved': [('readonly', True)], 'done': [('readonly', True)]},
        default=_default_employee_id, domain=lambda self: self._get_employee_id_domain(), check_company=True)
    account = fields.Char(string="Account")
    destination = fields.Char(string='Destination')
    froms = fields.Char(string='From')
    to = fields.Char(string='To')
    round_type = fields.Selection([
        ("oneway","Oneway"),
        ("return","Return")
    ], default="oneway")              
    payment_mode = fields.Selection(string="Payment", default="own_account", readonly=True)
    total_amount = fields.Float(string="Total Amount", compute="_compute_amount", store=True, copy=True,
        states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits='Product Price')
    def _compute_amount(self):
        for expense in self:
            expense.total_amount = expense.unit_amount

    @api.depends('company_id')
    def _compute_employee_id(self):
        if not self.env.context.get('default_employee_id'):
            for expense in self:
                expense.employee_id = self.env.user.with_company(expense.company_id).employee_id
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            if self.employee_id.name:
                name = self.employee_id.name
                dep_id = self.employee_id.department_id.id
                employee = self.env['hr.employee'].search([('name', '=', name)])
                for x in employee:
                    self.barcode = x.barcode
                departement = self.env['hr.department'].search([('id', '=', dep_id)])
                for x in departement:
                    self.department_name = x.name
                    self.department_code = x.id
            
    barcode = fields.Char(string="Applicant Code")   
    department_name = fields.Char(string="Departemen Name")
    department_code = fields.Integer(string="Departement Code")





class HrExpenseSheet(models.Model):
    _inherit = ['hr.expense.sheet']

    user_id = fields.Many2one('res.users', 'Manager', compute='_compute_from_employee_id', store=True, readonly=True, copy=False, states={'draft': [('readonly', False)]}, tracking=True, domain=lambda self: [('groups_id', 'in', self.env.ref('hr_expense.group_hr_expense_team_approver').id)])
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company)
    payment_mode = fields.Selection(related='expense_line_ids.payment_mode', default='own_account', readonly=True, string="Paid By", tracking=True)

    employee_id = fields.Many2one()
    applicant_code = fields.Char(default=lambda self:self.env.uid)
    departement_code = fields.Char(string="Departemen Code")
    expense_type = fields.Char(string="Expense Type")
    account = fields.Char(string="Account")
    total_amount = fields.Monetary(digits="Product Price")

    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    def action_submit_sheet(self):
        if self.attachment_number == 0:
            raise ValidationError(_("Attachments Required!"))
        super(HrExpenseSheet, self).action_submit_sheet()
    def action_register_payment(self):
        if self.attachment_number == 0:
            raise ValidationError(_('Attachment Required!!'))


