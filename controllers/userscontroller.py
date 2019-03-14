from flask import request, Response
from json import dumps
from root import application
from models.users import *
from decorators import *

#---------------------------------------Valiate Token----------------------------------------------#

@application.route("/api/v1/token/validate", methods=["POST"])
@token_required
def api_token_validate():
    request_data = request.get_json()
    responseObject = {
        "status": "success",
        "message": "Token Valid.",
        "token": True,
        "user": Users.get_user_by_username(request_data["username"], False)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#---------------------------------------GET all users----------------------------------------------#

@application.route("/api/v1/users/all", methods=["GET"])
@token_required
def api_users_all():
    responseObject = {
        "status": "success",
        "message": "Users found.",
        "user": Users.get_all_users()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#---------------------------GET user by username from query string---------------------------------#

@application.route("/api/v1/users/username", methods=["GET"])
@token_required
def api_user_by_username():
    if 'username' in request.args:
        username = request.args['username']
    else:
        responseObject = {
            "status": "failure",
            "message": "Error: No username field provided. Please specify an username."
        }
        response = Response(dumps(responseObject), 400, mimetype='application/json')

    user = Users.get_user_by_username(username, False)
    if user == None:
        responseObject = {
            "status": "failure",
            "message": "User not found.",
            "user": user
        }
    else:
        responseObject = {
            "status": "success",
            "message": "User found.",
            "user": user
        }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#---------------------------GET user by username from query string---------------------------------#

@application.route("/api/v1/users/username/exist", methods=["GET"])
def api_user_by_username_exist():
    if 'username' in request.args:
        username = request.args['username']
    else:
        responseObject = {
            "status": "no",
            "message": "Error: No username field provided. Please specify an username."
        }
        response = Response(dumps(responseObject), 400, mimetype='application/json')

    user = Users.get_user_by_username(username, False)
    if user == None:
        responseObject = {
            "status": "no",
            "message": "User not found."
        }
    else:
        responseObject = {
            "status": "yes",
            "message": "User found."
        }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#-----------------------------GET user by email from query string----------------------------------#

@application.route("/api/v1/users/email", methods=["GET"])
@token_required
def api_user_by_email():
    if 'email' in request.args:
        email = request.args['email']
    else:
        responseObject = {
            "status": "failure",
            "message": "Error: No email field provided. Please specify an email."
        }
        response = Response(dumps(responseObject), 400, mimetype='application/json')
    
    user = Users.get_user_by_email(email)
    if user == None:
        responseObject = {
            "status": "failure",
            "message": "User not found.",
            "user": user
        }
    else:
        responseObject = {
            "status": "success",
            "message": "User found.",
            "user": user
        }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#-----------------------------GET user by email from query string----------------------------------#

@application.route("/api/v1/users/email/exist", methods=["GET"])
def api_user_by_email_exist():
    if 'email' in request.args:
        email = request.args['email']
    else:
        responseObject = {
            "status": "no",
            "message": "Error: No email field provided. Please specify an email."
        }
        response = Response(dumps(responseObject), 400, mimetype='application/json')
    
    user = Users.get_user_by_email(email)
    if user == None:
        responseObject = {
            "status": "no",
            "message": "User not found."
        }
    else:
        responseObject = {
            "status": "yes",
            "message": "User found."
        }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#---------------------------GET user by username from url extension--------------------------------#

@application.route("/api/v1/users/<string:username>", methods=["GET"])
def api_user_via_username(username):
    responseObject = {
        'status': 'success',
        'message': 'Successfully registered.',
        'user': Users.get_user_by_username(username, False)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

#------------------------------------------POST user-----------------------------------------------#

@application.route("/api/v1/users", methods=["POST"])
def api_add_user():
    request_data = request.get_json()
    if(Users.validate_user(request_data)):
        new_user = Users()
        new_user.username = request_data["username"]
        new_user.password = request_data["password"]
        new_user.email = request_data["email"]
        #TODO: add admin from client
        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.',            
            'user': new_user.username
        }
        Users.add_user(new_user)
        response = Response(dumps(responseObject), 201, mimetype='application/json')
        return response
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Failed to registered the user.',
            'user': None
        }
        response = Response(dumps(responseObject), 400, mimetype='application/json')
        return response

#-----------------------------------------DELETE user----------------------------------------------#

@application.route("/api/v1/users/<string:username>", methods=["DELETE"])
def api_delete_user_via_username(username):
    responseObject = {
        'status': 'success',
        'message': 'Successfully deleted user.',
        'user': Users.delete_user_by_username(username)
    }
    response = Response(dumps(responseObject), 201, mimetype='application/json')
    return response

#--------------------------------------------------------------------------------------------------#