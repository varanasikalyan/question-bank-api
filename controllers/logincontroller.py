from root import application
from flask import request, Response
from json import dumps
from models.users import *

@application.route("/api/v1/auth/login", methods=["POST"])
def get_token():
	try:
		request_data = request.get_json()
		email = request_data["email"]
		password = request_data["password"]
		user = Users.username_password_match(email, password)
		if user:
			auth_token = user.encode_auth_token()
			responseObject = {
				"status": "success",
				"message": "Login Success.",
				"auth_token": auth_token.decode(),
				"username": user.username
			}
			return Response(dumps(responseObject), 201, mimetype="application/json")
		else:
			responseObject = {
				"status": "failure",
				"message": "Login failed. Please try again.",
			}
			return Response(dumps(responseObject), 401, mimetype="application/json")
	except Exception as e:
		responseObject = {
			"status": "failure",
			"message": "Some error occured. Please try again."
		}
		return Response(dumps(responseObject), 401, mimetype="application/json")