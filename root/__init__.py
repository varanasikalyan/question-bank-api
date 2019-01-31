#-------------------------------------------------------------------------------
# Name:        __init__.py
# Purpose:
#
# Author:      kkrishnav
#
# Created:     15/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config["SECRET_KEY"] = "hoderapi"
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questionbank.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
bcrypt = Bcrypt(application)

from controllers import *

print("Creating database and tables")
db.create_all()