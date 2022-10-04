from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date

class HrExpense(models.Model):
    """Inherit HR Expense"""
    _inherit = 'hr.expense'
    
    # Business Field -> Public Transportation
    location_destination = fields.Char(string='Destination', tracking=True)
    location_from = fields.Char(string='From', tracking=True)
    location_to = fields.Char(string='To', tracking=True)
    journey_type = fields.Selection([
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
    ], string='One way or Round Trip', tracking=True)


    use_content = fields.Char(string='Contents of use', tracking=True)
    use_purpose = fields.Char(string='Purpose of use', tracking=True)
    section = fields.Char(tracking=True)
    lot_name = fields.Char(string='Parking Lot Name', tracking=True)
    commuting_kilometer = fields.Float(string='Commuting Kilometers', tracking=True)
    route = fields.Char(string='Route of use', tracking=True)
    business_use = fields.Float(tracking=True)
    commuting_use = fields.Float(tracking=True)
    means_transport = fields.Char(string='Means of transport', tracking=True)
    temporary_storate = fields.Char()
    support = fields.Char()
    date_planned = fields.Date(string='Planned Date for first Night of accomodation')
    number_accommodation = fields.Integer(string='Number of nights Hotel/Accommodation is needed')
    address_business = fields.Text(string='Address of Business Trip')
    allowance = fields.Float()
    reason_business = fields.Char(string='Reason/Customer of Business Trip')
    cost_accommodation = fields.Float(string='Cost of Accommodation')
    car_type_id = fields.Many2one(comodel_name='hr.car.type')
    date_string = fields.Char(compute='_compute_expense_date')
    expense_type = fields.Selection([
        ('public_transportation', 'Public Transportation'),
        ('consumable', 'Consumable'),
        ('small_withdrawal', 'Small Withdrawal'),
        ('car', 'Transportation Expenses'),
        ('business_trip', 'Application for Business Trip Expenses')], 
        readonly=True,
        required=True,
        default='public_transportation',
        states={'draft': [('readonly', False)]})
    light_car = fields.Char()
    
    @api.depends('quantity', 'unit_amount', 'tax_ids', 'currency_id')
    def _compute_amount(self):
        """Update price unit if the car type is selected"""
        for expense in self:
            if expense.car_type_id:
                expense.untaxed_amount = expense.unit_amount * expense.commuting_kilometer
                taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.commuting_kilometer, expense.product_id, expense.employee_id.user_id.partner_id)
                expense.total_amount = taxes.get('total_included')
            else:
                return super(HrExpense, self)._compute_amount()

    @api.depends('date')
    def _compute_expense_date(self):
        """Set Format Expense Date"""
        for order in self:
            if order.date:
                self.date_string = format_date(order.env, order.date, date_format='yyyyMMdd')
    
    @api.onchange('car_type_id')
    def _onchange_car_type(self):
        """Get Fuel Price"""
        for line in self:
            fuel_price_id = False
            unit_amount = 0
            if line.car_type_id:
                fuel_price_id = line.car_type_id.fuel_type_id
            if fuel_price_id:
                result = line.get_fuel_pricelist(fuel_price_id.id)
                unit_amount = sum([res[1] for res in result])
            
            if unit_amount == 0:
                raise UserError(_("The date of fuel price is not found"))

            line.update({'unit_amount': unit_amount})
            line._compute_amount()
    
    @api.onchange('commuting_kilometer')
    def _onchange_commuting_kilometer(self):
        """Trigger compute amount"""
        for line in self:
            line._compute_amount()

    @api.onchange('product_id', 'date', 'account_id')
    def _onchange_product_id_date_account_id(self):
        """Set Line of the hr expense sheet to empty"""
        if self.product_id != self._origin.product_id:
            self.sheet_id.expense_line_ids = False
        return super()._onchange_product_id_date_account_id()
    
    def get_fuel_pricelist(self, price_id):
        """List Fuel Price"""
        date_start = date_end = fields.Date.to_string(self.date)
        
        query = """
            SELECT
                fl.id,
                CASE WHEN %s >= fl.start_date and %s <= fl.end_date then COALESCE(SUM(fl.price), 0) else 0 END as price
            FROM
                hr_fuel_price_line fl
            LEFT JOIN hr_fuel_price f on (f.id = fl.fuel_price_id)
            WHERE fl.fuel_price_id = %s
            GROUP BY fl.id
            LIMIT 1
        """
        params = (date_start, date_end, price_id)
        self.env.cr.execute(query, params)
        return self.env.cr.fetchall()