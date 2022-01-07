from flask import Flask, request 
import requests
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'garima'
api = Api(app)
jwt = JWT(app, authenticate, identity)   #/auth  jwt creates another end point i.e 
data  = []
class Employee(Resource):
    @jwt_required()
    def get(self, name):
        # for employee in data:
        #     if employee['name'] == name:
        #         return employee
            employee = next(filter(lambda x:x['name'] == name, data), None)
            return {'employee': employee}, 200 if  employee is not None else 404 
    
    def post(self,name):

        if next(filter(lambda x:x['name'] == name, data), None) is not None:
            return{"message": f"an item with {name} name exits"}

        request_data = request.get_json()   #If we do not give the (get_json(force =False) )content type to application/json i.e seetng the header in postman, this line will give errors 
        employee={'name':name, 'salary':request_data['salary']}
        # for employee in data:
        #     if employee[name] == name:
        # new_employee = [{
        #     "id": request_data[id],
        #     "name": request_data[name],
        #     "salary": request_data[salary]
        #     }]
        data.append(employee)
        return employee, 201

class EmployeeList(Resource):
        def get(self):
            return {'employee': data}

api.add_resource(Employee, '/employee/<string:name>')
api.add_resource(EmployeeList, '/data' )
app.run(port=5005, debug = True)
       
    