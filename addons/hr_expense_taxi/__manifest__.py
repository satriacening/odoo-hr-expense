{
    'name' : 'hr_expense_taxi',
    'versions' : '1.0',
    'category' : 'Expense Management',
    'author': 'Satria',
    'website': '',
    'license': 'OEEL-1',
    'depends': ['web','base'],
    'data': [
        "security/ir.model.access.csv",
        "views/hr_expense_taxi_action.xml",
        "views/hr_expense_taxi_menu.xml",
        "views/hr_expense_taxi_view.xml",
    ],
    'application' : True,
    'installable': True,
}