import pymongo
from datetime import datetime,date
from flask import Flask,request
from flask_restful import Resource ,Api ,reqparse

client = pymongo.MongoClient('localhost',27017)

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('ID')
parser.add_argument('UseName')
parser.add_argument('Pass')
parser.add_argument('Fname')
parser.add_argument('Lname')
parser.add_argument('Number')

db = client.db_example1

work = db.work
class HistoryWork(Resource):
        def get(self):
                args = parser.parse_args()
                id = args['ID']
                data = work.find_one({"user.Number":id})
                if(data):
                        firstname = data['user']['Fname']
                        lastname = data['user']['Lname']
                        list_work = data['list_work']
                        return {"Ftname":firstname,"Lname":lastname,"list_work":list_work}
                return {}
class Registration(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['Number']
                firstname = args['Fname']
                lastname = args['Lname']
                password = args['Pass']
                data = work.find_one({"user.Number":id})
                if(data):
                        return {"err":"has this id"}
                work.insert({"user":{"Number":id,"Fname":firstname,"Lname":lastname,"Pass":password},"list_work":[]})
                return {"Fname":firstname,"Lname":lastname,"Number":id,"Pass":password}
class Login(Resource):
        def post(self):
                args = parser.parse_args()
                username = args['UseName']
                password = args['Pass']
                data = work.find_one({"user.Number":username,"user.pastword":password})
                if(data):
                        firstname = data['user']['Fname']
                        lastname = data['user']['Lname']
                        datetime_login = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        work.update({"user.Number":username},{"$push":{"list_work":{"datetime":datetime_login}}})
                        return {"Fname":firstname,"Lname":lastname,"datetime":datetime_login}
                return {}
api.add_resource(Registration,'/api/register')
api.add_resource(Login,'/api/login')
api.add_resource(HistoryWork,'/api/list_work')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5500)
