"""
This file contains all the routes and methods available to users
These routes will usually be static routes serving static files
"""

from flask import render_template, flash, redirect, url_for, request, send_file, jsonify, session, send_file
from database import profiledb, postsdb, tasksdb, updatedb, classdb
from bson.objectid import ObjectId
from flask_app import app, bcrypt

#Route for homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')



#Route for Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        form = request.form
        pass_hash = bcrypt.generate_password_hash(form["password"]).decode('utf-8')
        Id = profiledb.insert_one({

            "fname": form["fname"],
            "lname": form["lname"],
            "email": form["email"],
            "username": "",
            "pfpURL": "/static/img/profile_pictures/default.png",
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
        return redirect(url_for('profile_create'))

    return render_template('signup.html')


#Route for create profile
@app.route('/profile/create-profile', methods=["GET", "POST"])
def profile_create():
    if "userId" in session:
        if request.method == "POST":
            if request.files and request.files['pfp']:
                file = request.files['pfp']
                url = "static/img/profile_pictures/" + file.filename
                file.save(url)
                profiledb.update({"_id": ObjectId(session["userId"])}, {"$set": {"pfpURL": "/" + url}})
            username = request.form["username"]
            profiledb.update({"_id": ObjectId(session["userId"])}, { "$set": {"username": username}})
            return redirect(url_for('profile', id=session["userId"]))

        else:
            return render_template('create.profile.html')


#Route for on-going username validation
@app.route('/profile/create-profile/validate', methods=["POST"])
def on_goUser():
    username = request.get_json()
    if profiledb.find_one({"username": username["username"]}):
        return jsonify(True)
    else:
        return jsonify(False)




#Route for loginpage
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        session.clear()
        form = request.form
        data = profiledb.find_one({"username": form["username"]})
        if data and bcrypt.check_password_hash(data["password"], form["password"]):
            session.clear()
            update = updatedb.find_one()
            updatedb.update_one({"_id": update["_id"]}, {"$set": {"postId": None}})
            session["userId"] = str(data["_id"])
            session["wall_update"] = ""
            profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
            return redirect(url_for('profile', id=session["userId"]))
        else:
            return render_template('login.html', msg="Username or Password incorrect")
    return render_template("login.html", msg="")



@app.route('/dashboard/profile/id=<id>')
def profile(id):
    if "userId" in session:
        if profiledb.find_one({"_id": ObjectId(session["userId"])})["role"] == "admin":
            return render_template('adminProfile.html', id=id)
        else:
            return render_template('profileTemplate.html', id=id)