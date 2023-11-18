#
# The original code for this example is credited to S. Subramanian,
# from this post on DZone: https://dzone.com/articles/restful-web-services-with-python-flask
#

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import Response
import codecs
import json
import const
import endpoints

"""
New Features:
    Endpoints:
        1 - Delete more than one employee
        2 - Multiple employees update
        3 - Get all employees with a given title
        4 - get all endpoints
        5 - Get all employees with a given salary
        6 - Increase employee salary by id by percentage
        7 - Increase all employees salary by percentage
    Database is now a json file:
        - employees.json
"""

app = Flask(__name__)

#Load from DB
empDB= codecs.open(const.DB_filename, 'r', encoding='utf-8').read()
empDB = json.loads(empDB)

#Save on DB
def saveOnDB():
    formatted = json.dumps(empDB, indent=4, sort_keys=True)
    with codecs.open(const.DB_filename, 'w', encoding='utf-8') as f:
        f.write(formatted)

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():
    return jsonify({'emps':empDB})


@app.route('/empdb/employee/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 

    if len(usr) == 0:
        return Response("{'error': 'Employee with id: " + empId + " not found'}", status=404 , mimetype='application/json')
    return jsonify({'emp':usr})


@app.route('/empdb/employee/<empId>',methods=['PUT'])
def updateEmp(empId):

    em = [ emp for emp in empDB if (emp['id'] == empId) ]

    if len(em) > 0:
        if 'name' in request.json : 
            em[0]['name'] = request.json['name']

        if 'title' in request.json:
            em[0]['title'] = request.json['title']
        
        saveOnDB()
    else:
        return Response("{'error': 'Employee with id: " + empId + " not found'}", status=404 , mimetype='application/json')
    return jsonify(em)

@app.route('/empdb/employee/<empId>/<empSal>',methods=['PUT'])
def updateEmpSal(empId,empSal):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]
    if len(em) > 0:
        em[0]['salary'] = empSal
        saveOnDB()
    else:
        return Response("{'error': 'Employee with id: " + empId + " not found'}", status=404 , mimetype='application/json')
    return jsonify(em)

@app.route('/empdb/employee',methods=['POST'])
def createEmp():

    emp = [ emp for emp in empDB if (emp['id'] == request.json['id']) ]
    if len(emp) > 0:
        response = Response("{'error': 'Employee with id: " + request.json['id'] + " already exists'}"
                            , status=400 , mimetype='application/json')
        return response
    dat = {
    'id':request.json['id'],
    'name':request.json['name'],
    'title':request.json['title'],
    'salary':request.json['salary']
    }
    empDB.append(dat)
    saveOnDB()
    return jsonify(dat)

@app.route('/empdb/employee/<empId>',methods=['DELETE'])
def deleteEmp(empId):
    em = [ emp for emp in empDB if (emp['id'] == empId) ]

    if len(em) > 0:
        empDB.remove(em[0])
        saveOnDB()
        return jsonify({'response':'Success'})
    else:
        return  Response("{'error': 'Employee with id: " + empId + " not found'}", status=404 , mimetype='application/json')

#New Feature 1 - Delete more than one employee
@app.route('/empdb/employee/multiple',methods=['DELETE'])
def MultipleDeleteEmployee():
    ids = request.json['ids']
    response = []
    for id in ids:
        em = [ emp for emp in empDB if (emp['id'] == id) ]
        if len(em) > 0:
            try:
                empDB.remove(em[0])
                response.append({
                        'id': id,
                        'response':'Success'
                    })
            except ValueError:
                response.append({
                        'id': id,
                        'response':'Failure'
                    })
        else:
            response.append({
                    'id': id,
                    'response':'Not Found'
                })
    saveOnDB()
    return jsonify(response)

#New Feature 2 - Multiple employees update
@app.route('/empdb/employee/multiple',methods=['PUT'])
def MultipleEmployeesUpdate():
    updatedEmployees = request.json['employees']
    response = []
    for employee in updatedEmployees:
        em = [ emp for emp in empDB if (emp['id'] == employee['id']) ]
        if len(em) > 0:
            try:
                em[0]['name'] = employee['name']
                em[0]['title'] = employee['title']
                em[0]['salary'] = employee['salary']
                response.append( em[0] )
            except ValueError:
                response.append({
                        'id': employee['id'],
                        'response':'Failure'
                    })
        else:
            response.append({
                    'id': employee['id'],
                    'response':'Not Found'
                })
    saveOnDB()
    return jsonify(response)

#New Feature 3 - Get all employees with a given title
@app.route('/empdb/employee/title/<title>',methods=['GET'])
def getEmpByTitle(title):
    emps = [ emp for emp in empDB if (emp['title'] == title) ] 

    if len(emps) == 0:
        return Response("{'error': 'Employees with title: " + title + " not found'}", status=404 , mimetype='application/json')

    return jsonify({
            'title':title,
            'Employees':emps
        })

#New Feature 4 - get all endpoints
@app.route('/empdb/employee/endpoints',methods=['GET'])
def getAllEndpoints():
    return jsonify({
            'endpoints': endpoints.endpoints
        })

#New Feature 5 - Get all employees with a given salary
@app.route('/empdb/salary/<salary>',methods=['GET'])
def getEmpBySalary(salary):
    emps = [ emp for emp in empDB if (emp['salary'] == salary)]

    if len(emps) == 0:
        return Response("{'error': 'Employees with salary: " + salary + " not found'}", status=404 , mimetype='application/json')

    return jsonify({
            'salary':salary,
            'Employees':emps
        })

#New Feature 6 - Increase employee salary by id by percentage
@app.route('/empdb/salary/increase_salary_by_id/<percentage>',methods=['PUT'])
def increaseEmpSalary(salary, percentage):
    ids = request.json['ids']
    response = []
    for id in ids:
        em = [ emp for emp in empDB if (emp['id'] == id) ]
        if len(em) > 0:
            try:
                em[0]['salary'] = int(em[0]['salary']) * (1 + int(percentage)/100)
                response.append( em[0] )
            except ValueError:
                response.append({
                        'id': id,
                        'response':'Failure'
                    })
        else:
            response.append({
                    'id': id,
                    'response':'Not Found'
                })
    saveOnDB()
    return jsonify(response)

#New Feature 7 - Increase all employees salary by percentage
@app.route('/empdb/salary/increase_all_salary/<percentage>',methods=['PUT'])
def increaseAllEmpSalary(percentage):
    response = []
    for employee in empDB:
        try:
            employee['salary'] = int(employee['salary']) * (1 + int(percentage)/100)
            response.append( employee )
        except ValueError:
            response.append({
                    'id': employee['id'],
                    'response':'Failure'
                })
    saveOnDB()
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

