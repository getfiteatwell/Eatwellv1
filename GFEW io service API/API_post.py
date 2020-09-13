"""This script deals with all API post methods to post data to database
    -> Users need to exchange access_token for data
    -> Some methods are not accessible to users with insufficient permissions
    -> Methods and permisiions form a hierarchy"""

from flask_app import app
from flask import jsonify, request, session
from bson.objectid import ObjectId
from database import *
import datetime

@app.route('/api/post/<field>', methods=["POST"])
def api_post(field):

    data_json = request.args
    """
        encoded url should look like this:
        {
            "obj_id" = [OBJ_ID]
            query = [query]
            access_token = [ACCESS_TOKEN]
        }
    """
    if "_id" in session and "access_token" in session:
        if field == "profile":
            if data_json["_id"] and data_json["query"] and data_json["access_token"]:
                if data_json["access_token"] == session["access_token"]:
                    if data_json["query"] == "task":
                        if session["_id"] == data_json["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "super admin" or (profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "instructor" and (data_json["_id"] in teamsdb.find_one({"instructor": ObjectId(session["_id"])})["members"])):
                            data = request.get_json()
                            task = tasksdb.insert_one({
                                "title": data["title"],
                                "description": data["description"],
                                "due_date": data["due_date"],
                                "status": "pending",
                                "score": 0,
                                "timestamp": datetime.datetime.now()
                            })
                            tasks_listdb.insert_one({
                                "point_id": str(data_json["_id"]),
                                "tasks": [str(task.inserted_id)],
                                "due_date": data["due_date"],
                                "status": "pending",
                                "score": 0,
                                "timestamp": datetime.datetime.now()
                            })
                            """update system for due_date timer"""
                            return jsonify(200)

                        else:
                            return jsonify({"error": "You don't have the perms to add task"})

                    elif data_json["query"] == "post":
                        if data_json["_id"] == session["_id"]:
                            data = request.get_json()
                            postsdb.insert_one({
                                "user_id": session["_id"],
                                "point_id": None,
                                "content": {
                                    "text": data["text"],
                                    "media": data["media"]
                                },
                                "uvotes": [],
                                "dvotes": [],
                                "comments": [],
                                "shares": [],
                                "timestamp": datetime.datetime.now()
                            })
                            return jsonify(200)
                        else:
                            return jsonify({"error": "You don't have permission to post "})

                    elif data_json["query"] == "follow":
                        if data_json["_id"] != session["_id"]:
                            if session["_id"] in set(profiledb.find_one({"_id": ObjectId(data_json["_id"])})["followers"]):
                                return jsonify({"error": "You already follow this user"})
                            else:
                                profiledb.update_one({"_id": ObjectId(data_json["_id"])},{"$push": {"followers": session["_id"]}})
                                return jsonify(200)

                        else:
                            return jsonify({"error": "You cannot follow yourself"})

                    elif data_json["query"] == "unfollow":
                        if data_json["_id"] != session["_id"]:
                            if session["_id"] in set(
                                    profiledb.find_one({"_id": ObjectId(data_json["_id"])})["followers"]):
                                profiledb.update_one({"_id": ObjectId(data_json["_id"])},
                                                     {"$pull": {"followers": session["_id"]}})
                                return jsonify(200)
                            else:
                                return jsonify({"error": "You don't follow this user"})

                        else:
                            return jsonify({"error": "You cannot unfollow yourself"})

                    elif data_json["query"] == "message":
                        if data_json["_id"] != session["_id"]:
                            if profiledb.find_one({"_id": ObjectId(data_json["_id"])})["perms"]["messages"] == True:
                                data = request.get_json()
                                if messagedb.find_one({"user_id": session["_id"]}):
                                    messagedb.update_one({"user_id": session["_id"]}, {"$push": {"messages": {
                                        "user_id": session["_id"],
                                        "text": data["text"],
                                        "timestamp": datetime.datetime.now()
                                    }}})
                                else:
                                    msg = messagedb.insert_one({
                                        "user_id": session["_id"],
                                        "point_id": data_json["_id"],
                                        "messages": [{
                                            "user_id": session["_id"],
                                            "text": data["text"],
                                            "timestamp": datetime.datetime.now()
                                    }],
                                        "timestamp": datetime.datetime.now()
                                    })

                                    profiledb.update_one({"_id": ObjectId(data_json["_id"])}, {"$push": {"messages": str(msg.inserted_id)}})
                                return jsonify(200)
                            else:
                                return jsonify({"error": "you don't have the perms to message this user"})

                        else:
                            return jsonify({"error": "You cannot message yourself"})


                    else:
                        return jsonify({"error": "invalid query syntax"})



                else:
                    return jsonify({"error": "invalid access token"})
            else:
                return jsonify({"error": "invalid request syntax"})

        elif field == "task":
            if data_json["_id"] and data_json["query"] and data_json["access_token"]:
                if data_json["access_token"] == session["access_token"]:
                    if data_json["query"] == "add":
                        if tasks_listdb.find_one({"_id": ObjectId(session["_id"])})["point_id"] == session["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                            if tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])}):
                                data = request.get_json()
                                task = tasksdb.insert_one({
                                    "title": data["title"],
                                    "description": data["description"],
                                    "due_date": data["due_date"],
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": datetime.datetime.now()
                                })
                                tasks_listdb.update_one({"_id": ObjectId(data_json["_id"])}, {"$push": {"tasks": str(task.inserted_id)}})
                                """update system for due_date timer"""
                                return jsonify(200)
                            else:
                                return jsonify({"error": "Task list not found"})
                        else:
                            return jsonify({"error": "You don't have the permission to add task to this list"})

                    elif data_json["query"] == "update":
                        if tasks_listdb.find_one({"_id": ObjectId(session["_id"])})["point_id"] == session["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                            if tasksdb.find_one({"_id": ObjectId(data_json["_id"])}):
                                data = request.get_json()
                                for i in tasksdb.find_one({"_id": ObjectId(data_json["_id"])}):
                                    if not(i in data):
                                        return jsonify({"error": "invalid post data"})
                                for i in data:
                                    tasksdb.update_one({"_id": ObjectId(data_json["_id"])}, {"$set": {i: data[i]}})
                                return jsonify(200)
                            else:
                                return jsonify({"error": "Task list not found"})
                        else:
                            return jsonify({"error": "You don't have the permission to add task to this list"})

                    else:
                        return jsonify({"error": "invalid query syntax"})

                else:
                    return jsonify({"error": "invalid access token"})
            else:
                return jsonify({"error": "invalid request syntax"})

        elif field == "post":
            if data_json["_id"] and data_json["query"] and data_json["access_token"]:
                if data_json["access_token"] == session["access_token"]:
                    if data_json["query"] == "post":
                        data = request.get_json()
                        postsdb.insert_one({
                            "user_id": session["_id"],
                            "point_id": data_json["_id"],
                            "content": {
                                "text": data["text"],
                                "media": data["media"]
                            },
                            "uvotes": [],
                            "dvotes": [],
                            "comments": [],
                            "shares": [],
                            "timestamp": datetime.datetime.now()
                        })
                        return jsonify(200)
                    elif data_json["query"] == "comment":
                        if postsdb.find_one({"_id": ObjectId(data_json["_id"])}):
                            data = request.get_json()
                            comment = postsdb.insert_one({
                                "user_id": session["_id"],
                                "point_id": data_json["_id"],
                                "content": {
                                    "text": data["text"],
                                    "media": data["media"]
                                },
                                "uvotes": [],
                                "dvotes": [],
                                "comments": [],
                                "shares": [],
                                "timestamp": datetime.datetime.now()
                            })
                            postsdb.update_one({"_id": ObjectId(data_json["_id"])},{"$push": {"comments": str(comment.inserted_id)}})
                            return jsonify(200)
                        else:
                            return jsonify({"error": "post doesnot exist"})

                    elif data_json["query"] == "uvote":
                        if postsdb.find_one({"_id": ObjectId(data_json["_id"])}):
                            if session["_id"] in set(postsdb.find_one({"_id": ObjectId(data_json["_id"])})["uvotes"]):
                                return jsonify({"error": "ypu already upvoted this post"})
                            elif session["_id"] in set(postsdb.find_one({"_id": ObjectId(data_json["_id"])})["dvotes"]):
                                postsdb.update_one({"_id": ObjectId(data_json["_id"])},
                                                   {"$pull": {"dvotes": session["_id"]}})

                            postsdb.update_one({"_id": ObjectId(data_json["_id"])},
                                               {"$push": {"uvotes": session["_id"]}})
                            return jsonify(200)
                        else:
                            return jsonify({"post doesnot exist"})

                    elif data_json["query"] == "dvote":
                        if postsdb.find_one({"_id": ObjectId(data_json["_id"])}):
                            if session["_id"] in set(postsdb.find_one({"_id": ObjectId(data_json["_id"])})["dvotes"]):
                                return jsonify({"error": "ypu already downvoted this post"})
                            elif session["_id"] in set(postsdb.find_one({"_id": ObjectId(data_json["_id"])})["uvotes"]):
                                postsdb.update_one({"_id": ObjectId(data_json["_id"])},
                                                   {"$pull": {"uvotes": session["_id"]}})

                            postsdb.update_one({"_id": ObjectId(data_json["_id"])},
                                               {"$push": {"dvotes": session["_id"]}})
                            return jsonify(200)
                        else:
                            return jsonify({"post doesnot exist"})

                    else:
                        return jsonify({"error": "invalid query syntax"})
                else:
                    return jsonify({"error": "invalid access token"})
            else:
                return jsonify({"error": "invalid request syntax"})

        elif field == "team":
            if data_json["_id"] and data_json["query"] and data_json["access_token"]:
                if data_json["access_token"] == session["access_token"]:
                    if data_json["query"] == "team":
                        if profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "instructor":
                            data = request.get_json()
                            teamsdb.insert_one({
                                "title": data["title"],
                                "instructor": session["_id"],
                                "members": [],
                                "timestamp": datetime.datetime.now(),
                                "tasks": []
                            })
                            return jsonify(200)
                        elif profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                            data = request.get_json()
                            teamsdb.insert_one({
                                "title": data["title"],
                                "instructor": data["instructor"],
                                "members": [],
                                "timestamp": datetime.datetime.now(),
                                "tasks": []
                            })
                            return jsonify(200)
                        else:
                            return jsonify({"error": "you dont' have permission to create a team"})
                    elif data_json["query"] == "update":
                        if profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin" or (profiledb.find_one({"_id": ObjectId(session["_id"])})["instructor"] and teamsdb.find_one({"instructor": session["_id"]})):
                            data = request.get_json()
                            teamsdb.update_one({"_id": ObjectId(data_json["_id"])}, {"$set": {"key": data["key"]}})
                            return jsonify(200)
                        else:
                            return jsonify({"error": "You don't have permission to edit this team"})
                    else:
                        return jsonify({"error": "invalid query syntax"})
                else:
                    return jsonify({"error": "invalid access token"})
            else:
                return jsonify({"error": "invalid request syntax"})

        elif field == "class":
            if data_json["_id"] and data_json["query"] and data_json["access_token"]:
                if data_json["access_token"] == session["access_token"]:
                    if data_json["query"] == "class":
                        if profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                            data = request.get_json()
                            classesdb.insert_one({
                                "title": data["title"],
                                "description": data["description"],
                                "art": {},
                                "instructor": data["instructor"],
                                "session": {
                                    "_id": "",
                                    "session_info": ""
                                },
                                "timestamp": datetime.datetime.now(),
                                "live_date": data["live_date"],
                                "status": False,
                                "type": data["type"],
                                "subscription": data["subscription"],
                                "enrollment": [],
                                "tasks": []
                            })
                            return jsonify(200)
                        elif profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "instructor":
                            data = request.get_json()
                            classesdb.insert_one({
                                "title": data["title"],
                                "description": data["description"],
                                "art": {},
                                "instructor": session["_id"],
                                "session": {
                                    "_id": "",
                                    "session_info": ""
                                },
                                "timestamp": datetime.datetime.now(),
                                "live_date": data["live_date"],
                                "status": False,
                                "type": data["type"],
                                "subscription": data["subscription"],
                                "enrollment": [],
                                "tasks": []
                            })
                            return jsonify(200)
                        else:
                            return jsonify({"error": "you don't have the permision to creata a class"})

                    if data_json["query"] == "update":
                        if profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin" or classesdb.find_one({"_id": ObjectId(data_json["_id"])})["instructor"] == session["_id"]:
                            data = request.get_json()
                            classesdb.update_one({"_id": ObjectId(data_json["_id"])}, {"$set": {"key": data["key"]}})
                        else:
                            return jsonify({"error": "you don't have the permission to update a class"})
                    else:
                        return jsonify({"error": "invalid query syntax"})
                else:
                    return jsonify({"error": "invalid access token"})
            else:
                return jsonify({"error": "invalid request syntax"})
    else:
        return jsonify({"error": "You don't have permision to send request"})