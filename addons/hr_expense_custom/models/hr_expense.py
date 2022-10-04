# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email.policy import default
import re

from odoo import api, fields, models, _

class HrExpense(models.Model):

    _inherit = ['hr.expense']

    destination = fields.Char(string='Destination')
    froms = fields.Char(string='From')
    to = fields.Char(string='To')
    total_amount = fields.Monetary(string="total")
    unit_amount = fields.Float(string="Amount")
    payment_mode = fields.Selection(string="Payment", default="own_account", readonly=True)
    
    def _compute_amount(self):
        for expense in self:
            expense.total_amount = expense.unit_amount

class HrExpenseSheet(models.Model):
    """
        Here are the rights associated with the expense flow

        Action       Group                   Restriction
        =================================================================================
        Submit      Employee                Only his own
                    Officer                 If he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        Approve     Officer                 Not his own and he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        Post        Anybody                 State = approve and journal_id defined
        Done        Anybody                 State = approve and journal_id defined
        Cancel      Officer                 Not his own and he is expense manager of the employee, manager of the employee
                                             or the employee is in the department managed by the officer
                    Manager                 Always
        =================================================================================
    """

    _inherit = ['hr.expense.sheet']
    
    destination = fields.Char(string='Destination')
    froms = fields.Char(string='From')
    to = fields.Many2one('hr.expense',string='To')
