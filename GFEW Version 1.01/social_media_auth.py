"""
This script deals with social media logins
"""

from database import profiledb
from flask import render_template, flash, redirect, url_for, request, send_file, jsonify, session, send_file
from flask_app import app
from user_router import signup
import urllib.parse
import requests
import json
from bson.objectid import ObjectId


#Linkedin proxy for creds send
@app.route('/linkedinproxy')
def linkedin_proxy():
    client_id = '78kthceuu73gx9'
    client_secret = '63BKJKpPvPNKmJI3'
    redirect_url = urllib.parse.quote('redirect_url')
    return jsonify(redirect_url)

#LinkedinAPI Endpoint
@app.route('/socialmedialogin/linkedin', methods=["GET", "POST"])
def linkedin():
    client_id = '78kthceuu73gx9'
    client_secret = '63BKJKpPvPNKmJI3'

    if request.args.get('error'):
        return redirect(url_for('signup'))
    else:
        code = request.args.get('code')
        params = {'grant_type': 'authorization_code',
                  'code': code,
                  'redirect_uri': 'http://_ip_/socialmedialogin/linkedin',
                  'client_id': client_id,
                  'client_secret': client_secret}
        post = requests.post('https://www.linkedin.com/oauth/v2/accessToken', params=params)
        token = post.json()['access-token']

        user = requests.get('https://api.linkedin.com/v2/me', headers={"Authorization": "Bearer " + token}).json()
        contact = requests.get('https://api.linkedin.com/v2/clientAwareMemberHandles?q=members&projection=(elements*(primary,type,handle~))', headers={{"Authorization": "Bearer " + token}}).json()
        email = ''
        phone = ''
        for i in contact["elements"]:
            if i["type"] == 'EMAIL':
                email = i["handle~"]["emailAddress"]
            if i["type"] == 'PHONE':
                phone = i["handle~"]["phoneNumber"]
        profiledb.insert_one({
            "lname": user["localizedLastName"],
            "fname": user["localizedFirstName"],
            "email": email,
            "phone": phone,
            

        })
        return jsonify('It worked')


#FacebookAPI endpoint
@app.route('/socialmedialogin/facebook')
def facebook():
    APP_ID = '2135959493299939'
    APP_SECRET = 'a63343193969d91893b928a034742401'
    print(request.args)
    return 'Facebook API works'


#InstagramAPI endpoint
@app.route('/socialmedialogin/instagram')
def instagram():
    APP_ID = ''
    APP_SECRET = ''

    if request.args.get('code'):
        auth_code = request.args.get('code')
        data = {
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": '',
            "code": auth_code

        }
        token = requests.post('https://api.instagram.com/oauth/access_token', data=data)
        print(token.json())
        return 'Instagram API works'



@app.route('/url?<url_string>', methods=["GET", "POST"])
def url(url_string):
    print(url_string)
    return url_string

@app.route('/urlhtml')
def html():
    return render_template('url.html')