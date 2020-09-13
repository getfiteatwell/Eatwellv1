import pymongo
from datetime import datetime
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["db"]


"""
Database schema
"""
profile = {
    "_id": "",
    "fname": "",
    "lname": "",
    "location": "",
    "email": "",
    "phone": "",
    "social_media": [],
    "username": "",
    "pfpURL": "",
    "password": "",
    "role": "",
    "meals": [],
    "followers": [],
    "following": [],
    "notifications": ["""list of not"""],
    "messages": ["""list of message ids"""],
    "timestamp": "",
    "progress": {
        "score": 0,
        "level": "",
        "badges": ["""badge ids"""],
        "rewards": ["""reward ids"""],
        "activities": [{
            "activity_": "activity id",
            "score": 0
                    }],
        "curve": ["""list of values over time"""]
            },
    "perms": {
        "posts": True,
        "messages": True
    }
}

message = {
    "_id": "",
    "user_id": "",
    "point_id": "",
    "message": {},
    "timestamp": ""
}

teams = {
    "_id": "",
    "title": "",
    "instructor": "",
    "members": [],
    "timestamp": "",
    "tasks": ["""list of tasks"""]
}








tasks = {
    "_id": "",
    "content": {},
    "due_date": "",
    "status": "",
    "score": 0,
    "timestamp": ""
}

tasks_list = {
    "_id": "",
    "point_id": "",
    "tasks": ["""list of task ids"""],
    "blocks": [],
    "status": "",
    "score": 0,
    "timestamp": ""
}






posts = {
    "_id": "",
    "user_id": "",
    "point_id": "",
    "content": {
        "text": "",
        "media": ["""list of media objects"""]
    },
    "uvotes": ["""list of users"""],
    "dvotes": ["""list of users"""],
    "comments": ["""list of posts"""],
    "shares": ["""list of users"""],
    "timestamp": ""
}

wall = {
    "_id": "",
    "title": "",
    "description": "",
    "posts": ["""list of post ids"""],
    "timestamp": ""
}







classes = {
    "_id": "",
    "title": "",
    "description": "",
    "art": {},
    "instructor": "",
    "session": {
        "_id": "",
        "session_info": ""
    },
    "timestamp": "",
    "live_date": "",
    "status": "",
    "type": "",
    "subscription": "",
    "enrollment": ["""list of user ids"""],
    "tasks": ["""list of tasks"""]
}

course = {
    "_id": "",
    "title": "",
    "description": "",
    "classes": ["""list of class ids"""],
    "timestamp": ""
}

activity = {
    "_id": "",
    "title": "",
    "description": "",
    "type": "",
    "score": 0,
    "content": {},
    "art": {},
    "timestamp": ""
}





badge = {
    "_id": "",
    "title": "",
    "description": "",
    "art": {},
    "score": 0,
    "timestamp": ""
}

reward = {
    "_id": "",
    "title": "",
    "description": "",
    "art": {},
    "content": {},
    "score": 0,
    "timestamp": ""
}



Planner = {
    "_id": "",
    "share": [],
    "timestamp": "",
    "weeks": ["""list of week ids"""]
}

week = {
    "_id": "",
    "days": ["""list of day ids"""]
}

day = {
    "_id": "",
    "chunks": ["""list of task_list ids"""]
}













#database objects
profiledb = db["profiles"]
messagedb = db["messages"]
teamsdb = db["teams"]
tasksdb = db["tasks"]
tasks_listdb = db["tasks_list"]
postsdb = db["posts"]
walldb = db["walls"]
classesdb = db["classes"]
coursedb = db["course"]
badgesdb = db["badges"]
activitiesdb = db["activities"]
plannerdb = db["planner"]
weekdb = db["week"]
daydb = db["day"]
rewardsdb = db["reward"]
otsessiondb = db["otsession"]


