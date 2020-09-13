"""This script deals with authentication to access the API

    -> Only users with existing account can get an access token
    -> User access token is saved in session data
"""

from uuid import uuid4
from flask_app import app
from flask import jsonify, session, request
from bson.objectid import ObjectId
from database import *

#Endpoint for requesting access token
@app.route('/api/auth')
def api_auth():
    data_json = request.args
    print(data_json)
    session.clear()
    if profiledb.find_one({"username": data_json["username"]}):
        session["_id"] = str(profiledb.find_one({"username": data_json["username"]})["_id"])
        access_token = str(uuid4())
        session["access_token"] = access_token
        return jsonify({"access_token": access_token})

    else:
        return jsonify({"error": "You don't have permission to request access token"})

