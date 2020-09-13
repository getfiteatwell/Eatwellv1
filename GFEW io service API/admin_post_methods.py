"""
This script deals with all the administrative tasks and methods
"""

from database import *
from bson.objectid import ObjectId
import time

def add_badge(badge):
    _id = badgesdb.insert_one({
        "content": badge,
        "timestamp": time.time()
    })
    return str(_id.inserted_id)

def remove_badge(badge_id):
    badgesdb.delete_one({"_id": ObjectId(badge_id)})
    return 200







def add_reward(reward):
    _id = rewardsdb.insert_one({
        "content": reward,
        "timestamp": time.time()
    })
    return str(_id.inserted_id)

def remove_reward(reward_id):
    rewardsdb.delete_one({"_id": ObjectId(reward_id)})
    return 200








def create_wall(wall):
    wall_id = walldb.insert_one({
        "content": wall,
        "timestamp": time.time()
    })
    return str(wall_id.inserted_id)

def remove_wall(wall_id):
    posts = []
    for post in walldb.find_one({"_id": ObjectId(wall_id)})["posts"]:
        posts.append(post)

    walldb.delete_one({"_id": ObjectId(wall_id)})
    def post_iter(post_id_list):
        for post_id in post_id_list:
            comments = postsdb.find_one({"_id": ObjectId(post_id)})["comments"]
            if comments:
                postsdb.delete_one({"_id": ObjectId(post_id)})
                post_iter(comments)
            else:
                postsdb.delete_one({"_id": ObjectId(post_id)})
    post_iter(posts)
    return 200


def remove_posts(post_id_list):
    def post_iter(post_id_list):
        for post_id in post_id_list:
            comments = postsdb.find_one({"_id": ObjectId(post_id)})["comments"]
            if comments:
                postsdb.delete_one({"_id": ObjectId(post_id)})
                post_iter(comments)
            else:
                postsdb.delete_one({"_id": ObjectId(post_id)})
    post_iter(post_id_list)
    return 200




def add_ot_session(api_key, api_session):
    from opentok import OpenTok
    opentok = OpenTok(api_key, api_session)
    otsession = opentok.create_session()

    otsessiondb.insert_one({
        "_id": otsession.session_id,
        "timestamp": time.time(),
        "status": "open"
    })
    return 200

def add_class(class_info):
    return 200

def assign_class(otsession_id):
    """assign otsession and change status"""
    return 200

def remove_class(class_id):
    """remove class and change otsession status"""
    return 200