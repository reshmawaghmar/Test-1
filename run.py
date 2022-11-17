import mimetypes
from telnetlib import STATUS
from flask import Flask, Response,request, jsonify
import pymongo 
import json
from bson.objectid import ObjectId 

app = Flask(__name__)
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR - Cannot connect to db")    
#1.Read
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )    
    except Exception as ex:
        print("ex") 
        return Response(response=json.dumps({"message":"cannot read users"}))
#2.creat
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = request.json
        print(user)
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        response=json.dumps(
                 {"message":"user created", 
                 "id":f"{dbResponse.inserted_id}"
                 })
        return jsonify (response)
    except Exception as ex:
        print("Reshma") 
        print(ex)    
    return ("datacreated")


#Update
@app.route("/users/<id>", methods = ["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        for attr in dir(dbResponse):
            print(f"**{attr}**")
        return Response(
            response=json.dumps(
                {"message":"user updated"}),
            status=200,
            mimetype="application/json"
        )    

    except Exception as ex:
        print("Hello")
        print(ex)    
        return Response(
            response= json.dumps(
            {"message":"cannot update user"}),
        status = 500,
        mimetype="application/json"
        )
    return id 


@app.route("/delete_task/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    return "task by id is successfully deleted"


# @app.route('/numbers', methods = ['GET'])
# def numbers():
#     number = mongo.db.numbers

#     offset = int(request.args['offset'])
#     limit = int(request.args['limit'])

#     starting_id = number.find().sort('_id', pymongo.DESCENDING)
#     last_id = starting_id['offset']['_id']

#     numbers = number.find({'_id' : {_id}}).sort('_id', pymongo.DESCENDING).limit(limit)

#     output = []

#     for i in numbers:
#         output.append({'number': i['number']})

#     next_url = '/numbers?limit=' + str(limit) + '&offset=' + str(offset + limit)
#     prev_url = '/numbers?limit=' + str(limit) + '&offset=' + str(offset + limit)

#     return  jsonify({'result' : output, 'prev_url' : prev_url, 'next_url' : next_url})

    

if __name__ == "__main__":
    app.run(port=80, debug=True)    
