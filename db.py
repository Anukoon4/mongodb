import pymongo
from flask import Flask,request
from flask_restful import Resource ,Api,reqparse
import json
from datetime import datetime,date

#int Flask
app= Flask (__name__)
api=Api(app)

parser =  reqparse.RequestParser()
parser.add_argument('info')


url="mongodb://Anukoon:1234@localhost:27017/admin"
client=pymongo.MongoClient(url)
db=client.admin.cpe_company_limited

class Registration(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['info'])
		print data['id'],data['firstname'],data['lastname'],data['password']
		db.update_one({"id":data['id']},
				{'$set':
				{"id":data['id'],
					"firstname":data['firstname'],
					"lastname":data['lastname'],
					"password":data['password']
				}

				},upsert=True)
		return {"firstname":data['firstname']}

class login(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['info'])
		result=db.find_one({"id":data['id'],"password":data['password']})
		if(result):
			timelogin = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			db.update({"id":data['id']},{"$push":{"list":{"timelogin":timelogin}}})	
			print result
			return {'firstname':result['firstname'],'timelogin':timelogin}
		

class view_history(Resource):
	def post(self):
		args=parser.parse_args()
		data=json.loads(args['info'])
		history =db.find_one({"id":data["id"]})
		print history
		if(history):
			firstname=history['firstname']
			lastname=history['lastname']
			work=history['list']
			return {"lastname":lastname,"list":work,"firstname":firstname}
		




api.add_resource(Registration,'/api/regis')
api.add_resource(login,'/api/login')
api.add_resource(view_history,'/api/view')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5505)




