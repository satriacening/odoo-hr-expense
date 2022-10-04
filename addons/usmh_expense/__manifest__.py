{
    'name': 'USMH Expense',
    'version': '14.0.1.0',
    'author': 'Port Cities',
    'website': 'https://www.portcities.net',
    "sequence": 1,
    'category': 'Expense',
    'summary': "Custom HR Expense",
    'description': """
Change Log
==========

Version 0.1.0 (Jan 14th, 2022)
------------------------------
* add a fuel price type
* add a car type
* add a mail template for expense refused
""",
    'depends': ['hr_expense', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_car_type_views.xml',
        'views/hr_department_views.xml',
        'views/hr_fuel_price_views.xml',
        'views/hr_expense_sheet_views.xml',
        'views/hr_expense_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
