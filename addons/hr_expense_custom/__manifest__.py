# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Custom Expenses inherit',
    'author': 'Custom By Satria',
    'version': '2.0',
    'category': 'Human Resources/Expenses',
    'sequence': 70,
    'summary': 'Submit, validate and reinvoice employee expenses',
    'description': """
Manage expenses by Employees
============================

This application allows you to manage your employees' daily expenses. It gives you access to your employeesâ€™ fee notes and give you the right to complete and validate or refuse the notes. After validation it creates an invoice for the employee.
Employee can encode their own expenses and the validation flow puts it automatically in the accounting after validation by managers.


The whole flow is implemented as:
---------------------------------
* Draft expense
* Submitted by the employee to his manager
* Approved by his manager
* Validation by the accountant and accounting entries creation

This module also uses analytic accounting and is compatible with the invoice on timesheet module so that you are able to automatically re-invoice your customers' expenses if your work by project.
    """,
    'website': 'https://www.odoo.com/page/expenses',
    'depends': ['hr_expense','hr',

],
    'data': [

        # 'security/ir.model.access.csv',
        'views/hr_expense_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
