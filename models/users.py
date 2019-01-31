#-------------------------------------------------------------------------------
# Name:     Users
# Purpose:
#
# Author:     kkrishnav
#
# Created:   15/10/2018
# Copyright:   (c) kkrishnav 2018
# Licence:   <your licence>
# Sample JSON:  {"username":"RF","email":"fedex@gmail.com","password":"fedex"}
#-------------------------------------------------------------------------------
from root import application, db, bcrypt
from jwt import encode
from datetime import datetime, timedelta

class Users(db.Model):
	__tablename__ =  "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
	admin = db.Column(db.Boolean, nullable=False, default=False)

	def __repr__(self):
		return "{'id': {0}, 'username': {1}, 'email': {2}, 'creation': {3}, 'admin': {4} }".format(self.id, self.username, self.email, self.registered_on, self.admin)

	@classmethod
	def username_password_match(classname, _email, _password):
		user = classname.query.filter_by(email=_email).first()
		if user and bcrypt.check_password_hash(user.password, _password):
			return user
		else:
			return None
			
	@classmethod
	def add_user(classname, _user):
		try:
			db.session.add(_user)
			db.session.commit()
		except Exception as e:
			return e
		
		return classname.get_user_by_username(_user.username)

	@classmethod
	def get_all_users(classname):
		return [user.serialize() for user in classname.query.all()]

	@classmethod
	def get_user_by_username(classname, _username):
		try:
			user_object = classname.query.filter_by(username=_username).first()
			if(user_object == None):
				return user_object
			else:
				return user_object.serialize()
		except:
			return False

	@classmethod
	def get_user_by_email(classname, _email):
		try:
			user_object = classname.query.filter_by(email=_email).first()
			if(user_object == None):
				return user_object
			else:
				return user_object.serialize()
		except:
			return False

	@classmethod
	def delete_user_by_username(classname, _username):
		try:
			classname.query.filter_by(username=_username).delete()
			db.session.commit()
		except:
			return False
		
		return True


	@classmethod
	def update_user_by_username(classname, _username, _user):
		try:
			user_to_update = classname.query.filter_by(username=_username).first()
			user_to_update.email = _user.email
			user_to_update.password = _user.password
			db.session.commit()
		except:
			return False

		return classname.get_user_by_username(_user.username)

	@staticmethod
	def validate_user(user):
		if ("username" in user and "email" in user and "password" in user):
			return True
		else:
			return False

	def encode_auth_token(self):
		"""
		Generates the Auth Token
		:return: string
		"""
		try:
			header = {
				"alg": "HS256",
				"typ": "JWT"
			}
			# Max value = timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)
			payload = {
				"exp": datetime.utcnow() + timedelta(days=2, hours=0, minutes=0, seconds=0, microseconds=0),
				"iat": datetime.utcnow(),
				"sub": self.id,
				"name": self.username
			}
			return encode(payload, self.username, headers=header)
		except Exception as e:
			return e

	def serialize(self):
		json_user = {
			"id": self.id,
			"username": self.username,
			"email": self.email,
			"password": self.password,
			"registered_on": str(self.registered_on),
			"admin": self.admin
		}
		return json_user