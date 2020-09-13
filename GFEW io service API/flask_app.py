import os
from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iusdfiuewyrf87ewfnyh'
#Bcrypt for encrypting passwords
bcrypt = Bcrypt(app)


