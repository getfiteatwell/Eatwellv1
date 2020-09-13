"""This script deals with all API get methods to fetch data from database
    -> Users need to exchange access_token for data
    -> Some methods are not accessible to users with insufficient permissions
    -> Methods and permisiions form a hierarchy"""

from flask_app import app
from flask import jsonify, request, session, render_template
from bson.objectid import ObjectId
from database import *


@app.route('/page')
def page():
    return render_template('API.html')


#Endpoint to get profile data
@app.route('/api/get/<field>')
def api_get(field):
    #Get all the url encoded parameters
    data_json = request.args
    print(data_json)
    """
        encoded url should look like this:
        {
            "_id" = [OBJ_ID]
            query = [list of queries]
            access_token = [ACCESS_TOKEN]
        }
    """
    if field == "profile":
        if data_json["_id"] and data_json["query"] and data_json["access_token"]:
            if data_json["access_token"] == session["access_token"]:
                if profiledb.find_one({"_id": ObjectId(data_json["_id"])}):
                    user = profiledb.find_one({"_id": ObjectId(data_json["_id"])})
                    response = {}
                    for i in data_json["query"].split():
                        if i == "profile":
                            if session["_id"] == data_json["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                                response["profile"] = {
                                    "_id": str(user["_id"]),
                                    "fname": user["fname"],
                                    "lname": user["lname"],
                                    "location": user["location"],
                                    "email": user["email"],
                                    "phone": user["phone"],
                                    "social_media": user["social_media"],
                                    "username": user["username"],
                                    "pfpURL": user["pfpURL"],
                                    "role": user["role"],
                                    "meals": len(user["meals"]),
                                    "followers": len(user["followers"]),
                                    "following": len(user["following"]),
                                    "notifications": user["notifications"],
                                    "messages": user["messages"],
                                    "timestamp": user["timestamp"],
                                    "perms": user["perms"]
                                }
                            else:
                                response["profile"] = {
                                    "_id": str(user["_id"]),
                                    "pfpURL": user["pfpURL"],
                                    "username": user["username"],
                                    "role": user["role"],
                                    "meals": len(user["meals"]),
                                    "followers": len(user["followers"]),
                                    "following": len(user["following"])
                                }

                        elif i == "progress":
                            if session["_id"] == data_json["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin" or (profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "instructor" and (ObjectId(data_json["_id"]) in set(teamsdb.find_one({"instructor": ObjectId(session["_id"])})["members"]))):
                                '''badges = []
                                activities = []
                                rewards = []
                                for j in profiledb.find_one({"_id": ObjectId(data_json["_id"])})["progress"]:
                                    badge = badgesdb.find_one({"id": ObjectId(j)})
                                    badges.append({
                                        "_id": badge["_id"],
                                        "title": badge["title"],
                                        "description": badge["description"],
                                        "art": badge["art"]
                                    })
                                response["progress"]["badges"] = badges

                                for j in progressdb.find_one({"_id": ObjectId(data_json["_id"])})["activities"]:
                                    activity = activitiesdb.find_one({"id": ObjectId(j)})
                                    activities.append({
                                        "_id": activity["_id"],
                                        "title": activity["title"],
                                        "description": activity["description"],
                                        "art": activity["art"]
                                    })
                                response["progress"]["activities"] = activities

                                for j in progressdb.find_one({"_id": ObjectId(data_json["_id"])})["rewards"]:
                                    reward = rewardsdb.find_one({"id": ObjectId(j)})
                                    rewards.append({
                                        "_id": reward["_id"],
                                        "title": reward["title"],
                                        "description": reward["description"],
                                        "art": reward["art"]
                                    })
                                response["progress"]["rewards"] = rewards'''
                                response["progress"] = profiledb.find_one({"_id": ObjectId(data_json["_id"])})["progress"]

                            else:
                                '''badges = []
                                activities = []
                                rewards = []
                                for j in progressdb.find_one({"_id": ObjectId(data_json["_id"])})["badges"]:
                                    badge = badgesdb.find_one({"id": ObjectId(j)})
                                    badges.append({
                                        "_id": badge["_id"],
                                        "title": badge["title"],
                                        "description": badge["description"],
                                        "art": badge["art"]
                                    })
                                response["progress"]["badges"] = badges

                                for j in progressdb.find_one({"_id": ObjectId(data_json["_id"])})["activities"]:
                                    activity = activitiesdb.find_one({"id": ObjectId(j)})
                                    activities.append({
                                        "_id": activity["_id"],
                                        "title": activity["title"],
                                        "description": activity["description"],
                                        "art": activity["art"]
                                    })
                                response["progress"]["activities"] = activities

                                for j in progressdb.find_one({"_id": ObjectId(data_json["_id"])})["rewards"]:
                                    reward = rewardsdb.find_one({"id": ObjectId(j)})
                                    rewards.append({
                                        "_id": reward["_id"],
                                        "title": reward["title"],
                                        "description": reward["description"],
                                        "art": reward["art"]
                                    })
                                response["progress"]["rewards"] = rewards'''
                                return jsonify({"error": "you dont have permission to view progress"})

                        elif i == "tasks":
                            if session["_id"] == data_json["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin" or (profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "instructor" and (data_json["_id"] in teamsdb.find_one({"instructor": ObjectId(session["_id"])})["members"])):
                                tasks = []
                                for j in tasks_listdb.find_one({"point_id": data_json["_id"]})["tasks"]:
                                    task = tasksdb.find_one({"_id": ObjectId(j)})
                                    tasks.append({
                                        "_id": str(task["_id"]),
                                        "title": task["title"],
                                        "description": task["description"],
                                        "due_date": task["due_date"],
                                        "status": task["status"]
                                    })
                                response["tasks"] = {
                                    "_id": str(tasks_listdb.find_one({"point_id": data_json["_id"]})["_id"]),
                                    "point_id": tasks_listdb.find_one({"point_id": data_json["_id"]})["point_id"],
                                    "tasks": tasks,
                                    "due_date": tasks_listdb.find_one({"point_id": data_json["_id"]})["due_date"],
                                    "status": tasks_listdb.find_one({"point_id": data_json["_id"]})["status"],
                                    "score": tasks_listdb.find_one({"point_id": data_json["_id"]})["score"],
                                    "timestamp": tasks_listdb.find_one({"point_id": data_json["_id"]})["timestamp"]
                                }
                            else:
                                return jsonify({"error": "you dont have permission to view tasks"})

                        elif i == "posts":
                            if session["_id"] == data_json["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin":
                                posts = []
                                for j in postsdb.find({"user_id": session["_id"]}).sort("_id", -1):
                                    posts.append({
                                        "_id": str(j["_id"]),
                                        "user_id": j["user_id"],
                                        "point_id": j["point_id"],
                                        "content": {
                                            "text": j["content"]["text"],
                                            "media": j["content"]["media"]
                                        },
                                        "uvotes": len(j["uvotes"]),
                                        "dvotes": len(j["dvotes"]),
                                        "comments": len(j["comments"]),
                                        "shares": len(j["shares"]),
                                        "timestamp": j["timestamp"]
                                    })
                                response["posts"] = posts
                            else:
                                return jsonify({"error": "you don't have perms to view post"})

                        else:
                            return jsonify({"error": "invalid request query"})

                    return jsonify(response)

                else:
                    return jsonify({"error": "profile does not exist"})

            else:
                return jsonify({"error": "invalid access token"})

        else:
            return jsonify({"error": "invalid request syntax"})
    elif field == "task":
        if tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])}):
            if tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["point_id"] == session["_id"] or profiledb.find_one({"_id": ObjectId(session["_id"])})["role"] == "admin" or (data_json["_id"] in set(teamsdb.find_one({"instructor": session["_id"]})["tasks"])) or (data_json["_id"] in set(classesdb.find_one({"instructor": session["_id"]}))):
                tasks = []
                for j in tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["tasks"]:
                    task = tasksdb.find_one({"_id": ObjectId(j)})
                    tasks.append({
                        "_id": str(task["_id"]),
                        "title": task["title"],
                        "description": task["description"],
                        "due_date": task["due_date"],
                        "status": task["status"]
                    })
                return jsonify({
                    "_id": str(tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["_id"]),
                    "point_id": tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["point_id"],
                    "tasks": tasks,
                    "due_date": tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["due_date"],
                    "status": tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["status"],
                    "score": tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["score"],
                    "timestamp": tasks_listdb.find_one({"_id": ObjectId(data_json["_id"])})["timestamp"]
                })
            else:
                return jsonify({"error": "you don't have the permission to view this task list"})
        else:
            return jsonify({"error": "task list not found"})

    elif field == "post":
        if data_json["query"] == "post":
            if postsdb.find_one({"_id": ObjectId(data_json["_id"])}):
                post = postsdb.find_one({"_id": ObjectId(data_json["_id"])})
                return jsonify({"posts": [{
                    "_id": str(post["_id"]),
                    "user_id": post["user_id"],
                    "point_id": post["point_id"],
                    "content": {
                        "text": post["content"]["text"],
                        "media": post["content"]["media"]
                    },
                    "uvotes": len(post["uvotes"]),
                    "dvotes": len(post["dvotes"]),
                    "comments": len(post["comments"]),
                    "shares": len(post["shares"]),
                    "timestamp": post["timestamp"]
                }]})
            elif walldb.find_one({"_id": ObjectId(data_json["_id"])}) and postsdb.find({"point_id": data_json["_id"]}):
                posts = []
                for post in postsdb.find({"point_id": data_json["_id"]}):
                    posts.append({
                        "_id": str(post["_id"]),
                        "user_id": post["user_id"],
                        "point_id": post["point_id"],
                        "content": {
                            "text": post["content"]["text"],
                            "media": post["content"]["media"]
                        },
                        "uvotes": len(post["uvotes"]),
                        "dvotes": len(post["dvotes"]),
                        "comments": len(post["comments"]),
                        "shares": len(post["shares"]),
                        "timestamp": post["timestamp"]
                    })
                return jsonify({
                    "posts": posts
                })

            else:
                return jsonify({"error": "post not found"})

        elif data_json["query"] == "comment":
            if postsdb.find_one({"_id": ObjectId(data_json["_id"])})["comments"]:
                posts = []
                for i in postsdb.find_one({"_id": ObjectId(data_json["_id"])}):
                    post = postsdb.find_one({"_id": ObjectId(i)})
                    posts.append({
                        "_id": str(post["_id"]),
                        "user_id": post["user_id"],
                        "point_id": post["point_id"],
                        "content": {
                            "text": post["content"]["text"],
                            "media": post["content"]["media"]
                        },
                        "uvotes": len(post["uvotes"]),
                        "dvotes": len(post["dvotes"]),
                        "comments": len(post["comments"]),
                        "shares": len(post["shares"]),
                        "timestamp": post["timestamp"]
                    })
                return jsonify({
                    "posts": posts
                })
            else:
                return jsonify({"error": "comments not found"})




