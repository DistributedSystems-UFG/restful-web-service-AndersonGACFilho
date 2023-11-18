endpoints = [
    {
        'url': '/empdb/employee',
        'method': 'GET',
        'description': 'Get all employees'
    },
    {
        'url': '/empdb/employee/<empId>',
        'method': 'GET',
        'description': 'Get an employee by employee id'
    },
    {
        'url': '/empdb/employee/<empId>',
        'method': 'PUT',
        'description': 'Update an employee by employee id'
    },
    {
        'url': '/empdb/employee/<empId>/<empSal>',
        'method': 'PUT',
        'description': 'Update an employee salary by employee id'
    },
    {
        'url': '/empdb/employee',
        'method': 'POST',
        'description': 'Create an employee'
    },
    {
        'url': '/empdb/employee/<empId>',
        'method': 'DELETE',
        'description': 'Delete an employee by employee id'
    },
    {
        'url': '/empdb/employee/multiple',
        'method': 'DELETE',
        'description': 'Delete multiple employees by employee id'
    },
    {
        'url': '/empdb/employee/multiple',
        'method': 'PUT',
        'description': 'Update multiple employees by employee id'
    },
    {
        'url': '/empdb/employee/title/<title>',
        'method': 'GET',
        'description': 'Get all employees with a given title'
    },
    {
        'url': '/empdb/employee/endpoints',
        'method': 'GET',
        'description': 'Get all endpoints'
    },
    {
        'url': '/empdb/salary/<salary>', 
        'method': 'GET',
        'description': 'Get all employees with a given salary'
    },
    {
        'url': '/empdb/salary/increase_salary_by_id/<percentage>',
        'method': 'PUT',
        'description': 'Increase salary by percentage'
    },
    {
        'url': '/empdb/salary/increase_all_salary/<percentage>',
        'method': 'PUT',
        'description': 'Increase all salary by percentage'
    }
]