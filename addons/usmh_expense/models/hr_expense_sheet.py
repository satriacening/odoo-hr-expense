import json
from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrExpenseSheet(models.Model):
    """Inherit HR Expense Sheet"""
    _inherit = 'hr.expense.sheet'
    
    applicant_code = fields.Char(default=lambda self:self.env.user.name)
    department_code = fields.Char(tracking=True, related='department_id.department_code')
    expense_type = fields.Selection([
        ('public_transportation', 'Public Transportation'),
        ('consumable', 'Consumable'),
        ('small_withdrawal', 'Small Withdrawal'),
        ('car', 'Transportation Expenses'),
        ('business_trip', 'Application for Business Trip Expenses')],
        required=True,
        readonly=True,
        default='public_transportation',
        states={'draft': [('readonly', False)]})
    account_id = fields.Many2one(comodel_name='account.account', tracking=True)
    has_voucher = fields.Boolean(string='Voucher')

    @api.onchange('expense_type')
    def _onchange_expense_type(self):
        """Reset Lines"""
        for order in self:
            if order.expense_type:
                order.expense_line_ids = False

    def action_submit_sheet(self):
        """Call Constrain"""
        self._constrain_attachment_number()
        return super(HrExpenseSheet, self).action_submit_sheet()

    def approve_expense_sheets(self):
        """Call Constrain"""
        self._constrain_attachment_number()
        return super(HrExpenseSheet, self).approve_expense_sheets()

    def _constrain_attachment_number(self):
        """Mandatory Attachment in the lines"""
        if self.expense_line_ids and self.has_voucher:
            for line in self.expense_line_ids:
                if line.attachment_number == 0:
                    raise UserError(_("You have to upload an attachment file for the line %s") % line.name)


    def refuse_sheet(self, reason):
        """Redefine"""
        if not self.user_has_groups('hr_expense.group_hr_expense_team_approver'):
            raise UserError(_("Only Managers and HR Officers can approve expenses"))
        elif not self.user_has_groups('hr_expense.group_hr_expense_manager'):
            current_managers = self.employee_id.expense_manager_id | self.employee_id.parent_id.user_id | self.employee_id.department_id.manager_id.user_id

            if self.employee_id.user_id == self.env.user:
                raise UserError(_("You cannot refuse your own expenses"))

            if not self.env.user in current_managers and not self.user_has_groups('hr_expense.group_hr_expense_user') and self.employee_id.expense_manager_id != self.env.user:
                raise UserError(_("You can only refuse your department expenses"))

        # self.write({'state': 'cancel'})
        mail_template_id = self.env.ref('hr_expense.hr_expense_template_refuse_reason')
        rendered_body = mail_template_id._render({'reason': reason}, engine='ir.qweb')
        body = self.env['mail.render.mixin']._replace_local_links(rendered_body)
        email_to = False
        if self.employee_id.work_email:
            email_to = self.employee_id.work_email
        if self.employee_id.user_id and self.employee_id.user_id.email_formatted:
            email_to = self.employee_id.user_id.email_formatted

        if self.state == 'submit':
            self.write({'state': 'draft'})
        if self.state == 'approve':
            self.write({'state':'submit' })
        for sheet in self:
            sheet.message_post_with_view('hr_expense.hr_expense_template_refuse_reason', values={'reason': reason, 'is_sheet': True, 'name': sheet.name})

            if email_to:
                self.env['mail.mail'].sudo().create({
                    'email_from': self.env.user.email_formatted,
                    'author_id': self.env.user.partner_id.id,
                    'body_html': body,
                    'subject': '%s : Expense Refuse Reason' % sheet.name,
                    'auto_delete': True,
                }).send()
        self.activity_update()

    @api.model
    def create(self, values):
        if 'expense_line_ids' in values:
            if len(values['expense_line_ids']) == 1:
                expense_id = self.env['hr.expense'].browse(values['expense_line_ids'][0][2])
                values.update({
                    'expense_type': expense_id.expense_type,
                    'account_id': expense_id.account_id.id
                })
        return super(HrExpenseSheet, self).create(values)

