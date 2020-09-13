"""
This script contains all the get response schema/tenplates for returning data from database
This script does minimal processing and sorting and tries to present data to the user as is in the database
This script only gets data from database. It neither modifies nor processes it in heavy duty
"""

from database import *
from bson.objectid import ObjectId

"""Delivers all data from profiledb"""
def profile_private(profile_id):
    profile = profiledb.find_one({"_id": ObjectId(profile_id)})
    posts = []
    for i in postsdb.find({"user_id": profile_id}):
        posts.append({
            "_id": str(i["_id"]),
            "user_id": i["user_id"],
            "point_id": i["point_id"],
            "content": i["content"],
            "uvotes": len(i["uvotes"]),
            "dvotes": len(i["dvotes"]),
            "comments": len(i["comments"]),
            "shares": len(i["shares"]),
            "timestamp": i["timestamp"]
        })
    badges = []
    for badge_id in profile["progress"]["badges"]:
        badge = badgesdb.find_one({"_id": ObjectId(badge_id)})
        badges.append({
            "_id": str(badge["_id"]),
            "title": badge["title"],
            "description": badge["description"],
            "art": badge["art"],
            "score": badge["score"]
        })

    rewards = []
    for j in profile["progress"]["rewards"]:
        reward = rewardsdb.find_one({"_id": ObjectId(j["reward"])})
        rewards.append({
            "_id": str(reward["_id"]),
            "title": reward["title"],
            "description": reward["description"],
            "type": reward["type"],
            "timestamp": j["timestamp"]
        })


    return {"profile": {
        "_id": str(profile["_id"]),
        "fname": profile["fname"],
        "lname": profile["lname"],
        "loc": profile["loc"],
        "email": profile["email"],
        "phone": profile["phone"],
        "social_media": profile["social_media"],
        "username": profile["username"],
        "pfpURL": profile["pfpURL"],
        "role": profile["role"],
        "meals": profile["meals"],
        "followers": profile["followers"],
        "following": profile["following"],
        "notifications": profile["notifications"],
        "messages": profile["messages"],
        "timestamp": profile["timestamp"],
        "perms": profile["perms"],
        "feed": posts,
        "badges": badges
    }}

def get_messages(profile_id):
    messages = {}
    for message in (messagedb.find({"user_id": ObjectId(profile_id)}) or messagedb.find({"point_id": ObjectId(profile_id)})):
        if messages:
            messages[message["point_id"]].append(message)
        else:
            messages[message["point_id"]] = [message]
    return {"messages": messages}

"""need to figure out a way to display log"""


def profile_public(profile_id):
    profile = profiledb.find_one({"_id": ObjectId(profile_id)})
    posts = []
    for i in postsdb.find({"user_id": profile_id}):
        posts.append({
            "_id": str(i["_id"]),
            "user_id": i["user_id"],
            "point_id": i["point_id"],
            "content": i["content"],
            "uvotes": len(i["uvotes"]),
            "dvotes": len(i["dvotes"]),
            "comments": len(i["comments"]),
            "shares": len(i["shares"]),
            "timestamp": i["timestamp"]
        })
    return {"profile": {
        "_id": str(profile["_id"]),
        "username": profile["username"],
        "pfpURL": profile["pfpURL"],
        "role": profile["role"],
        "meals": len(profile["meals"]),
        "followers": len(profile["followers"]),
        "following": len(profile["following"]),
        "feed": posts
    }}


def profile_lite(profile_id):
    profile = profiledb.find_one({"_id": ObjectId(profile_id)})
    return {"profile": {
        "_id": str(profile["_id"]),
        "username": profile["username"],
        "pfpURL": profile["pfpURL"],
        "role": profile["role"]
    }}


"""planner_id and profile_id are the same"""
def planner(profile_id):
    planner = plannerdb.find_one({"_id": ObjectId(profile_id)})
    weeks = []
    for week_id in planner["weeks"]:
        week = weekdb.find_one({"_id": ObjectId(week_id)})
        days = []
        for day_id in week["days"]:
            day = daydb.find_one({"_id": ObjectId(day_id)})
            tasks_lists = []
            for tasks_list_id in day["chunks"]:
                tasks_list = tasks_listdb.find_one({"_id": ObjectId(tasks_list_id)})
                tasks = []
                for task_id in tasks_list["tasks"]:
                    task = tasksdb.find_one({"_id": ObjectId(task_id)})
                    tasks.append({
                        "_id": str(task["_id"]),
                        "content": task["content"],
                        "status": task["status"],
                        "score": task["score"],
                        "timestamp": task["timestamp"]
                    })
                tasks_lists.append({
                    "_id": str(tasks_list["_id"]),
                    "point_id": tasks_list["point_id"],
                    "tasks": tasks,
                    "blocks": tasks_list["blocks"],
                    "status": tasks_list["status"],
                    "score": tasks_list["score"],
                    "timestamp": tasks_list["timestamp"]
                })
            days.append({
                "_id": str(day["_id"]),
                "chunks": tasks_lists
            })
        weeks.append({
            "_id": str(week["_id"]),
            "days": days
        })
    return {"planner": {
        "_id": str(planner["_id"]),
        "share": planner["share"],
        "timestamp": planner["timestamp"],
        "weeks": weeks,
        "week_count": planner["week_count"]
    }}





"""getting posts from wall or comments from post/comments"""
def wall(wall_id=None):
    walls = []
    for wall in walldb.find():
        walls.append({
            "_id": str(wall["_id"]),
            "title": wall["title"],
            "description": wall["description"]
        })
    return {"walls": walls}


def post_from_wall(wall_id):
    posts = []
    wall = walldb.find_one({"_id": ObjectId(wall_id)})
    for post_id in walldb.find_one({"_id": ObjectId(wall_id)})["posts"]:
        post = postsdb.find_one({"_id": ObjectId(post_id)})
        posts.append({
            "_id": str(post["_id"]),
            "user_id": post["user_id"],
            "point_id": post["point_id"],
            "content": post["content"],
            "uvotes": len(post["uvotes"]),
            "dvotes": len(post["dvotes"]),
            "comments": len(post["comments"]),
            "shares": len(post["shares"]),
            "timestamp": len(post["timestamp"])
        })
    return {"wall": {
        "_id": str(wall["_id"]),
        "title": wall["title"],
        "description": wall["description"],
        "posts": posts
    }}


def post(post_id):
    post = postsdb.find_one({"_id": ObjectId(post_id)})
    return {"post": {
        "_id": str(post["_id"]),
        "user_id": post["user_id"],
        "point_id": post["point_id"],
        "content": post["content"],
        "uvotes": len(post["uvotes"]),
        "dvotes": len(post["dvotes"]),
        "comments": len(post["comments"]),
        "shares": len(post["shares"]),
        "timestamp": len(post["timestamp"])
    }}

def comment(post_id):
    comments = []
    for comment_id in postsdb.find_one({"_id": ObjectId(post_id)})["comments"]:
        post = postsdb.find_one({"_id": ObjectId(comment_id)})
        comments.append({
            "_id": str(post["_id"]),
            "user_id": post["user_id"],
            "point_id": post["point_id"],
            "content": post["content"],
            "uvotes": len(post["uvotes"]),
            "dvotes": len(post["dvotes"]),
            "comments": len(post["comments"]),
            "shares": len(post["shares"]),
            "timestamp": len(post["timestamp"])
        })

    return {"comments": comments}



"""Display list of classes/classes and/or courses which include list of classes"""

"""aka classes_short"""
def class_list(class_id=None):
    classes = []
    for Class in classesdb.find():
        classes.append({
            "_id": str(Class["_id"]),
            "title": Class["title"],
            "description": Class["description"],
            "art": Class["art"],
            "live_date": Class["live_date"],
            "status": Class["status"]
        })
    return {"classes": classes}


def show_class(class_id):
    Class = classesdb.find_one({"_id": ObjectId(class_id)})
    return {"class": {
        "_id": str(Class["_id"]),
        "title": Class["title"],
        "description": Class["description"],
        "art": Class["art"],
        "instructor": Class["instructor"],
        "live_date": Class["live_date"],
        "status": Class["status"],
        "type": Class["type"],
        "subscription": Class["subscription"],
        "enrollment": Class["enrollment"]
    }}



"""This part deals with request query to function mapping"""
def requesttoresponsemapper(request_query):
    if request_query == "show_class":
        return show_class
    elif request_query == "class_list":
       return class_list
    elif request_query == "comment":
        return comment
    elif request_query == "post":
        return post
    elif request_query == "post_from_wall":
        return post_from_wall
    elif request_query == "wall":
        return wall
    elif request_query == "planner":
        return planner
    elif request_query == "profile_lite":
        return profile_lite
    elif request_query == "profile_public":
        return profile_public
    elif request_query == "get_messages":
        return get_messages
    elif request_query == "profile_private":
        return profile_private
    else:
        return "error"
