"""
This script deals with all the post request methods to either process or add/modify data on the database
This script only includes methods for users
"""
import time
import datetime
from datetime import timedelta, date
from database import *
from bson.objectid import ObjectId

"""profile methods"""
def follow(profile_id, follower_id):
    profile = profiledb.find_one({"_id": ObjectId(profile_id)})
    if follower_id in profile["followers"]:
        return {"error": "you already follow this user"}
    elif profile_id == follower_id:
        return {"error": "you cannot follow yourself"}
    else:
        profiledb.update_one({"_id": ObjectId(profile_id)}, {"$push": {"followers": follower_id}})
        profiledb.update_one({"_id": ObjectId(follower_id)}, {"$push": {"following": profile_id}})
        return 200

def unfollow(profile_id, follower_id):
    if profile_id == follower_id:
        return {"error": "you cannot unfollow ypurself"}
    elif follower_id not in profiledb.find_one({"_id": ObjectId(profile_id)})["followers"]:
        return {"error": "you don't follow this user"}
    else:
        profiledb.update_one({"_id": ObjectId(profile_id)}, {"$pull": {"followers": follower_id}})
        profiledb.update_one({"_id": ObjectId(follower_id)}, {"$pull": {"following": profile_id}})
        return 200

def message(profile_id, sender_id, message):
    if profile_id == sender_id:
        return {"error": "you cannot message yourself"}
    elif profiledb.find_one({"_id": ObjectId(profile_id)})["perms"]["messages"] == False:
        return {"error": "you don't have permission to message this user"}
    else:
        msg = messagedb.insert_one({
            "user_id": sender_id,
            "point_id": profile_id,
            "message": message,
            "timestamp": time.time()
        })
        profiledb.update_one({"_id": ObjectId(profile_id)}, {"$push": {"messages": msg.inserted_id}})
        profiledb.update_one({"_id": ObjectId(sender_id)}, {"$push": {"messages": msg.inserted_id}})
        return 200






"""planner methods"""


def add_planner(profile_id):
    if plannerdb.find_one({"_id": ObjectId(profile_id)}):
        return {"error": "a planner already exists"}
    else:
        weeks = []
        for i in range(6):
            days = []
            for j in range(7):
                day_id = daydb.insert_one({
                    "chunks": []
                })
                days.append(str(day_id.inserted_id))
            week = weekdb.insert_one({
                "days": days
            })
            weeks.append(str(week.inserted_id))
        plannerdb.insert_one({
            "_id": ObjectId(profile_id),
            "share": [],
            "timestamp": time.time(),
            "weeks": weeks,
            "week_count": 6
        })
        return 200


def append_planner(planner_id):
    if not plannerdb.find_one({"_id": ObjectId(planner_id)}):
        return {"error": "planner does not exist"}
    else:
        for i in range(6):
            days = []
            for j in range(7):
                day_id = daydb.insert_one({
                    "chunks": []
                })
                days.append(str(day_id.inserted_id))
            week = weekdb.insert_one({
                "days": days
            })
            plannerdb.update_one({"_id": ObjectId(planner_id)}, {"$push": {"weeks": str(week.inserted_id)}})
        return 200


def add_task(planner_id, task, day_id):
    if not plannerdb.find_one({"_id": ObjectId(planner_id)}):
        return {"error": "planner does not exist"}
    else:
        for task_list in tasks_listdb.find({"point_id": planner_id}):
            if not set(task_list["blocks"]).isdisjoint(task["blocks"]):
                return {"error": "block already occupied"}
        added_task = tasksdb.insert_one({
            "content": task["content"],
            "status": "pending",
            "score": 0,
            "timestamp": time.time()
        })
        added_task_list = tasks_listdb.insert_one({
            "point_id": planner_id,
            "tasks": [str(added_task.inserted_id)],
            "blocks": task["blocks"],
            "status": "pending",
            "score": 0,
            "timestamp": time.time()
        })
        daydb.update_one({"_id": ObjectId(day_id)}, {"$push": {"chunks": str(added_task_list.inserted_id)}})
        return str(added_task_list.inserted_id)



def append_task(task_list_id, task):
    if not tasks_listdb.find_one({"_id": ObjectId(task_list_id)}):
        return {"error": "task list does not exist"}
    else:
        added_task = tasksdb.insert_one({
            "content": task["content"],
            "status": "pending",
            "score": 0,
            "timestamp": time.time()
        })

        tasks_listdb.update_one({"_id": ObjectId(task_list_id)}, {"$push": {"tasks": str(added_task.inserted_id)}})
        return 200


def remove_task(task_list_id, task_id):
    if not tasks_listdb.find_one({"_id": ObjectId(task_list_id)}):
        return {"error": "task list does not exist"}
    else:
        tasksdb.delete_one({"_id": ObjectId(task_id)})
        tasks_listdb.update_one({"_id": ObjectId(task_list_id)}, {"$pull": {"tasks": task_id}})
        return 200


def remove_task_list(task_list_id, planner_id, day_id):
    """Does not delete tasks or task list from database"""

    if not plannerdb.find_one({"_id": ObjectId(planner_id)}):
        return {"error": "planner does not exist"}
    elif not tasks_listdb.find_one({"_id": ObjectId(task_list_id)}):
        return {"error": "task list does not exist"}
    else:
        daydb.update_one({"_id": ObjectId(day_id)}, {"$pull": {"chunks": task_list_id}})
        return 200


def update_task(task_id):
    tasksdb.update_one({"_id": ObjectId(task_id)}, {"$set": {"status": "completed"}})
    return 200




"""Post methods"""


def add_post(wall_id, profile_id, post):
    _id = postsdb.insert_one({
        "user_id": profile_id,
        "point_id": wall_id,
        "content": post,
        "uvotes": [],
        "dvotes": [],
        "comments": [],
        "shares": [],
        "timestamp": time.time()
    })
    return str(_id.inserted_id)


def uvote_post(post_id, profile_id):
    if profile_id in set(postsdb.find_one({"_id": ObjectId(post_id)})["uvotes"]):
        return {"error": "you already upvoted this post"}
    else:
        postsdb.update_one({"_id": ObjectId(post_id)}, {"$push": {"uvotes": profile_id}})
        if profile_id in set(postsdb.find_one({"_id": ObjectId(post_id)})["dvotes"]):
            postsdb.update_one({"_id": ObjectId(post_id)}, {"$pull": {"dvotes": profile_id}})
            return 200


def dvote_post(post_id, profile_id):
    if profile_id in set(postsdb.find_one({"_id": ObjectId(post_id)})["dvotes"]):
        return {"error": "you already downvoted this post"}
    else:
        postsdb.update_one({"_id": ObjectId(post_id)}, {"$push": {"dvotes": profile_id}})
        if profile_id in set(postsdb.find_one({"_id": ObjectId(post_id)})["dvotes"]):
            postsdb.update_one({"_id": ObjectId(post_id)}, {"$pull": {"uvotes": profile_id}})
            return 200

def add_comment(post_id, profile_id, comment):
    comment_id = postsdb.insert_one({
        "user_id": profile_id,
        "point_id": post_id,
        "content": comment,
        "uvotes": [],
        "dvotes": [],
        "comments": [],
        "shares": [],
        "timestamp": time.time()
    })

    postsdb.update_one({"_id": ObjectId(post_id)}, {"$push": {"comments": str(comment_id.inserted_id)}})
    return str(comment_id.inserted_id)