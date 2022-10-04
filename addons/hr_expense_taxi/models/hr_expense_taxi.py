from dataclasses import field
from email.policy import default
from odoo import models, fields, api, _

class hr_expense_taxi (models.Model):
    _name = 'hr.expense.taxi'

    def func_submitted(self):
        if self.status == 'draft':
            self.status = 'submitted'
    def func_approved(self):
        if self.status == 'submitted':
            self.status = 'approved'
    def func_posted(self):
        if self.status == 'approved':
            self.status = 'posted'
    def func_paid(self):
        if self.status == 'posted':
            self.status = 'paid'

    applicant_code = fields.Char(string="Appliciant Code")
    applicant_name = fields.Char(string="Appliciant Name")
    department_code = fields.Char(string="Departemen Code")
    department_name = fields.Char(string="Departemen Name")
    product = fields.Char(string="Product")
    expense_type = fields.Selection([
        ("public","Public"),
        ("personal","Personal")
    ],default='public', tracking=True)
    account = fields.Char(string="Account")
    expense_date = fields.Date(string="Expense Date")
    destination = fields.Char(string="destination")
    froms = fields.Char(string="From")
    to = fields.Char(string="To")
    line = fields.Selection([
        ("oneway","Oneway"),
        ("return","Return")
    ])              
    amount = fields.Float(string="Amount", store=True, required=True, copy=True,
        states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, digits='Product Price')
    voucher = fields.Boolean(string="Voucher", readonly=True, default=True)
    attachment = fields.Binary(string="Attachment") 
    total_calculation = fields.Float(string="Total Calculation")
    status = fields.Selection([
        ("draft","Draft"),
        ("submitted","Submitted"),
        ("approved","Approved"),
        ("posted","Posted"),
        ("paid","Paid"),
        ("refused","Refused")
    ],default='draft')

