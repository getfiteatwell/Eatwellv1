from flask import render_template, flash, redirect, url_for, request, send_file, jsonify, session, send_file
import os
from database import postsdb, profiledb, classdb, updatedb
import flask_app
from flask_app import app
from bson.objectid import ObjectId
from opentok import OpenTok


#Route for homepage
""""@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')"""



#Route for Signup
""""@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        form = request.form
        pass_hash = flask_app.bcrypt.generate_password_hash(form["password"]).decode('utf-8')
        Id = profiledb.insert_one({

            "fname": form["fname"],
            "lname": form["lname"],
            "email": form["email"],
            "username": "",
            "pfpURL": "",
            "phone": form["phone"],
            "password": pass_hash,
            "meals": 0,
            "followers": 0,
            "following": 0,
            "level": "beginner",
            "role": "student",
            "post_update": False,
            "task_update": False,
            "notification_update": False,
        })
        session.clear()
        session["userId"] = str(Id.inserted_id)
        session["wall_update"] = updatedb.find_one()["postId"]

    return render_template('signup.html')


#Route for profile picture
@app.route('/profile/id=<id>/create-profile', methods=["GET", "POST"])
def profile_picture(id):
    if "userId" in session:
        if request.method == "POST":
            file = request.files['pfp']
            username = request.form["username"]
            url = "static/profile pictures/" + file.filename
            file.save(url)
            profiledb.update({"_id": ObjectId(id)}, { "$set": {"pfpURL": "/" + url,
                                                               "username": username}})
            return redirect(url_for('profile', id=id))

        else:
            return render_template('profilepicture.html')



#Route for loginpage
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        session.clear()
        form = request.form
        data = profiledb.find_one({"username": form["username"]})
        if data and flask_app.bcrypt.check_password_hash(data["password"], form["password"]):
            session.clear()
            update = updatedb.find_one()
            updatedb.update_one({"_id": update["_id"]}, {"$set": {"postId": None}})
            session["userId"] = str(data["_id"])
            session["wall_update"] = ""
            profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
            return redirect(url_for('profile', id=session["userId"]))
        else:
            return jsonify(401)
    return render_template("login.html")



@app.route('/dashboard/profile/id=<id>')
def profile(id):
    if "userId" in session:
        if profiledb.find_one({"_id": ObjectId(session["userId"])})["role"] == "admin":
            return render_template('adminProfile.html', id=id)
        else:
            return render_template('profileTemplate.html', id=id)"""


#route for getting profile
@app.route('/dashboard/profile/id=<id>/get')
def profile_get(id):
    if "userId" in session:
        user = profiledb.find_one({"_id": ObjectId(id)})
        posts = []
        for i in postsdb.find({"userId": id}).sort("_id", 1):
            posts.append({
                "_id": str(i["_id"]),
                "username": user["username"],
                "role": user["role"],
                "body": i["body"],
                "date": i["date"],
                "pfpURL": user["pfpURL"]
            })
        return jsonify({
            "_id": id,
            "pfpURL": user["pfpURL"],
            "username": user["username"],
            "role": user["role"],
            "meals": user["meals"],
            "followers": user["followers"],
            "following": user["following"],
            "posts": posts,
            #"notifications": user["notifications"]
        })


#route for notifications

#route for posting posts
@app.route('/dashboard/posts/action=post', methods=["POST"])
def post_post():
    if "userId" in session:
        data = request.get_json()
        postId = postsdb.insert_one({
            "userId": session["userId"],
            "body": data["body"],
            "date": data["date"]
        })
        profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": True}})
        obj = updatedb.find_one()
        updatedb.update_one({"_id": ObjectId(obj["_id"])}, {"$set": {"postId": str(postId.inserted_id)}})
        session["wall_update"] = str(postId.inserted_id)

        return jsonify(200)


#post notification
"""@app.route('/dashboard/posts/action=get/<self>', methods=["GET"])
def post_get(self):
    if "userId" in session:

        if self == "wall":
            while True:
                status = updatedb.find_one()
                if status["postId"] != session["wall_update"]:
                    profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
                    session["wall_update"] = status["postId"]
                    for i in postsdb.find().sort("_id", -1):
                        user = profiledb.find_one({"_id": ObjectId(i["userId"])})
                        return jsonify([{
                            "_id": str(i["_id"]),
                            "username": user["username"],
                            "role": user["role"],
                            "body": i["body"],
                            "date": i["date"],
                            "pfpURL": user["pfpURL"]
                        }])

        elif self == "self":
            while True:
                status = profiledb.find_one({"_id": ObjectId(session["userId"])})
                if status["post_update"] == True:
                    profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
                    for i in postsdb.find({"userId": session["userId"]}).sort("_id", -1):
                        user = profiledb.find_one({"_id": ObjectId(i["userId"])})
                        return jsonify([{
                            "_id": str(i["_id"]),
                            "username": user["username"],
                            "role": user["role"],
                            "body": i["body"],
                            "date": i["date"],
                            "pfpURL": user["pfpURL"]
                        }])"""




#route fot create task
@app.route('/dashboard/profile/id=<id>/tasks/create', methods=["GET", "POST"])
def taskCreate(id):
    if "userId" in session:
        if request.method == "POST":
            profiledb.update_one({"_id": ObjectId(session["userId"])}, { "$set": {"task_update": True}})
            query = request.form
            user = profiledb.update({"_id": ObjectId(session["userId"])}, {'$push': {"tasks": {"title": query["title"],
                                                                                                "description": query["description"],
                                                                                                "type": query["type"],
                                                                                               "pfpURL": profiledb.find_one({"_id": ObjectId(id)})["pfpURL"]
                                                                                                }}})
            return redirect(url_for('profile', id=session["userId"]))
        else:
            return render_template('taskcreate.html')


#route for getting tasks
"""@app.route('/dashboard/profile/id=<id>/tasks/get', methods=["GET"])
def taskGet(id):
    if "userId" in session:
        if session["userId"] == id:
            while True:
                status = profiledb.find_one({"_id": ObjectId(session["userId"])})
                if status["task_update"] == True:
                    profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"task_update": False}})
                    user = profiledb.find_one({"_id": ObjectId(id)})
                    tasks = user["tasks"]
                    return jsonify([{
                        "title": tasks[-1]["title"],
                        "pfpURL": user["pfpURL"],
                        "type": tasks[-1]["type"]
                    }])"""


#route for classroom
@app.route('/dashboard/classes/action=get', methods=["GET"])
def classroom():
    if "userId" in session:
        list = []
        for i in classdb.find():
            list.append({
                "_id": str(i["_id"]),
                "title": i["title"],
                "body": i["body"],
                "pfpURL": "/static/images/profile-img.png",
            })
        return jsonify(list)

@app.route('/dashboard/profile/id=<id>/classroom', methods=["GET"])
def class_list(id):
    return render_template('classroom.html', id=id)

#route for class
@app.route('/class/id=<classId>', methods=["GET", "POST"])
def video(classId):
    if "userId" in session:
        if request.method == "POST":
            api_key = '46838544'
            api_secret = 'c727ac0672a3ae6c1490b68e4032d8e982531450'
            opentok = OpenTok(api_key, api_secret)
            session_id = classdb.find_one({"_id": ObjectId(classId)}, {"session_id": 1})["session_id"]
            Tk = opentok.generate_token(session_id)
            # Sending Video API credentials
            return jsonify({'apiKey': api_key, 'sessionId': session_id, 'token': Tk})

        return render_template('class.html')



#route for wall
@app.route('/dashboard/profile/id=<id>/wall', methods=["GET"])
def wall(id):
    if "userId" in session:
        return render_template('wall.html', id=id)

@app.route('/dashboard/wall/get', methods=["GET"])
def wall_get():
    if "userId" in session:
        profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
        posts = []
        for i in postsdb.find().sort("_id", 1):
            user = profiledb.find_one({"_id": ObjectId(i["userId"])})
            posts.append({
                "_id": str(i["_id"]),
                "username": user["username"],
                "role": user["role"],
                "body": i["body"],
                "date": i["date"],
                "pfpURL": user["pfpURL"]
            })
        return jsonify(posts)





#Route for dashboard
"""@app.route('/main', methods=['GET', 'POST'])
def index():
    #if user was already logged in
    if "user" in session:
        if request.method == 'POST':
            Tk = opentok.generate_token(session_id)
            # Sending Video API credentials
            return jsonify({'apiKey': api_key, 'sessionId': session_id, 'token': Tk})

        return render_template('index.html')
    else:
        #If user was not logged in, redirect to loginpage
        return redirect(url_for('login'))


@app.route('/picture')
def picture():
    return send_file('redesign/back.png')


    #Mobile endpoint

@app.route('/mobile', methods=['POST'])
def mob_signup():
    query = request.json
    user = User.query.filter_by(username=query["username"]).first()
    Tkn = opentok.generate_token(session_id)
    if user:
        return jsonify({'apiKey': api_key, 'sessionId': session_id, 'token': Tkn})
    else:
        pass_hash = bcrypt.generate_password_hash(query["password"]).decode('utf-8')
        # Adding user and hashed password to database
        user = User(name=query["name"], username=query["username"], email=query["email"], password=pass_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify({'apiKey': api_key, 'sessionId': session_id, 'token': Tkn})"""




#test route
"""@app.route('/dashboard/profile/id=<id>/notifications', methods=["GET"])
def notifications(id):
    if "userId" in session:
        if session["userId"] == id:
            while True:
                if profiledb.find_one({"_id": ObjectId(id)})["notification_update"] == True:
                    profiledb.update_one({"_id": ObjectId(id)}, {"$set": {"notification_update": False}})
                    user = profiledb.find_one({"_id": ObjectId(id)})
                    return jsonify([user["notifications"][-1]])"""





"""-----------------------------------------------------------------------------------------------------"""

"""Admin routes"""


@app.route('/dashboard/profile/id=<id>/getusers')
def admin_get(id):
    if profiledb.find_one({"_id": ObjectId(id)})["role"] == "admin":
        list = []
        for i in profiledb.find():
            list.append({
                "_id": str(i["_id"]),
                "username": i["username"],
                "role": i["role"],
                "date": "",
                "body": str(i["_id"]),
                "pfpURL": i["pfpURL"]
            })
        return jsonify(list)



@app.route('/dashboard/profile/createtask', methods=["POST"])
def admin_tasks():
    if profiledb.find_one({"_id": ObjectId(session["userId"])})["role"] == "admin":
        query = request.form
        user = profiledb.update({"_id": ObjectId(query["_id"])}, {'$push': {"tasks": {"title": query["title"],
                                                                                           "description": query[
                                                                                               "description"],
                                                                                           "type": query["type"],
                                                                                           "pfpURL": profiledb.find_one(
                                                                                               {"_id": ObjectId(query["_id"])})[
                                                                                               "pfpURL"]
                                                                                           }}})
        profiledb.update_one({"_id": ObjectId(query["_id"])}, {"$push": {"notifications": {
            "sender": "Administrator",
            "action": "created a task for",
            "object": "You"
        }}})
        profiledb.update_one({"_id": ObjectId(query["_id"])}, {"$set": {"task_update": True}})
        profiledb.update_one({"_id": ObjectId(query["_id"])}, {"$set": {"notification_update": True}})
        return redirect(url_for('profile', id=profiledb.find_one({"role": "admin"})["_id"]))


@app.route('/dashboard/profile/createclass', methods=["POST"])
def admin_class():
    if profiledb.find_one({"_id": ObjectId(session["userId"])})["role"] == "admin":
        query = request.form
        api_key = '46838544'
        api_secret = 'c727ac0672a3ae6c1490b68e4032d8e982531450'
        opentok = OpenTok(api_key, api_secret)
        video_session = opentok.create_session()

        classdb.insert_one({
            "title": query["title"],
            "body": query["body"],
            "session_id": video_session.session_id
        })
        return redirect(url_for('profile', id=profiledb.find_one({"role": "admin"})["_id"]))



    """Only one endpoint for long polling"""

@app.route('/dashboard/notifications')
def notification():
    if "userId" in session:
        while True:
            #checking for post update_self
            status_self = profiledb.find_one({"_id": ObjectId(session["userId"])})
            if status_self["post_update"] == True:
                profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
                for i in postsdb.find({"userId": session["userId"]}).sort("_id", -1):
                    user = profiledb.find_one({"_id": ObjectId(i["userId"])})
                    return jsonify({"type": "posts_self", "payload": [{
                        "_id": str(i["_id"]),
                        "username": user["username"],
                        "role": user["role"],
                        "body": i["body"],
                        "date": i["date"],
                        "pfpURL": user["pfpURL"]
                    }]})


            #checking for post update_wall
            status_wall = updatedb.find_one()
            if status_wall["postId"] != session["wall_update"]:
                profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
                session["wall_update"] = status_wall["postId"]
                for i in postsdb.find().sort("_id", -1):
                    user = profiledb.find_one({"_id": ObjectId(i["userId"])})
                    return jsonify({"type": "posts_wall", "payload": [{
                        "_id": str(i["_id"]),
                        "username": user["username"],
                        "role": user["role"],
                        "body": i["body"],
                        "date": i["date"],
                        "pfpURL": user["pfpURL"]
                    }]})


            #checking for task updates
            status_task = profiledb.find_one({"_id": ObjectId(session["userId"])})
            if status_task["task_update"] == True:
                profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"task_update": False}})
                user = profiledb.find_one({"_id": ObjectId(session["userId"])})
                tasks = user["tasks"]
                task = tasks[-1]
                return jsonify({"type": "tasks", "payload": [{
                    "title": task["title"],
                    "pfpURL": user["pfpURL"],
                    "type": task["type"]
                }]})

            #checking for classe updates
            #---------------------------


            #checking for notification updates
            if profiledb.find_one({"_id": ObjectId(session["userId"])})["notification_update"] == True:
                profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"notification_update": False}})
                user = profiledb.find_one({"_id": ObjectId(session["userId"])})
                notifications = user["notifications"]
                notification = notifications[-1]
                return jsonify({"type": "notifications", "payload": [notification]})


#logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))