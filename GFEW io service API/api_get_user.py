"""
This script contains all the endpoints for returning get request response for user end
Endpoints are build such that multuple request queries can be handled at rhe same time
"""
import get_response_schema_user
from flask_app import app
from flask import request, session, jsonify


@app.route('/api/user/get')
def api_get_user():
    if "access_token" in session:
        encoded_url_params = request.args
        if ("access_token" and "_id" and "query") in encoded_url_params:
            if encoded_url_params["access_token"] == session["access_token"]:
                query_list = encoded_url_params["query"].split
                response = {}
                for query in query_list:
                    callback = get_response_schema_user.requesttoresponsemapper(query)
                    if callback == "error":
                        return jsonify({"error": "invalid query syntax"})
                    else:
                        response[query] = callback(encoded_url_params["_id"])
                return jsonify(response)
            else:
                return jsonify({"error": "invalid access token"})
        else:
            return jsonify({"error": "invalid request syntax"})
    else:
        return jsonify({"error": "you are not authorized to access"})


