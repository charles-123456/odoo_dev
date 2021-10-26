{
    'name': 'Employee Invoice Rate',
    'version': '14.0.1.0.0',
    'summary': 'Set Invoice Rate Based on Per Day rate',
    'author': 'Primoris Systems India Pvt Ltd',
    'website':'https://www.primorissystems.com/',
    'category': 'Human Resources',
    'depends': ['hr','hr_timesheet_sheet','account'],
    'data': [
            'views/hr_timesheet_sheet.xml',
            'views/account_move_inherit.xml',
        ],
    'installable': True,
}
