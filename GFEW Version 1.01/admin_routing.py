from flask import render_template, flash, redirect, url_for, request, send_file, jsonify, session, send_file
import os
from database import postsdb, profiledb, classdb, updatedb
import flask_app
from flask_app import app
from bson.objectid import ObjectId
from opentok import OpenTok

from flask_app import app

#route to get profiles
@app.route('/admin/login')
def login():

    if request.method == "POST":
        session.clear()
        form = request.form
        data = profiledb.find_one({"_id": ObjectId(form["_id"])})
        if data and flask_app.bcrypt.check_password_hash(data["password"], form["password"]):
            session.clear()
            session["userId"] = str(data["_id"])
            session["wall_update"] = ""
            profiledb.update_one({"_id": ObjectId(session["userId"])}, {"$set": {"post_update": False}})
            return redirect(url_for('profile'))
        else:
            return jsonify(401)
    return render_template("login.html")

@app.route('/admin/profile')
def profile():
    return render_template('adminProfile.html')