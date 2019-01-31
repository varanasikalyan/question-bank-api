from flask import request, Response
from json import dumps
from root import application
from models.questions import *
from models.options import *
from decorators import *

@application.route("/api/v1/questions/all", methods=["GET"])
def api_questions_all():
    responseObject = {
        "status": "success",
        "message": "Retrieved all Questions successfully.",            
        "question": Questions.get_all_questions()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/questions", methods=["GET"])
def api_questions():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Question, no (id) field provided. please specify an (id)."
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

    question = Questions.get_question_from_id(id)
    responseObject = {
        "status": "success",
        "message": "Question retrieved successfully.",            
        "question": question.serialize()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/questions/<int:id>", methods=["GET"])
def api_questions_via_id(id):
    question = Questions.get_question_from_id(id)
    if question.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Question."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')
    responseObject = {
        "status": "success",
        "message": "Question retrieved successfully.",            
        "question": question.serialize()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/questions", methods=["POST"])
@token_required
def api_add_question():
    request_data = request.get_json()
    if(Questions.validate_question(request_data)):
        question = Questions.submit_question_from_json(request_data)
        if question is None or question.id < 0:
            responseObject = {
                "status": "failure",
                "message": "Failed to add an Invalid Question."                
            }
            return Response(dumps(responseObject), 500, mimetype='application/json')
        responseObject = {
            "status": "success",
            "message": "Question added successfully.",            
            "question": question.serialize()
        }
        return Response(dumps(responseObject), 201, mimetype='application/json')
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to add an Invalid Question."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

@application.route("/api/v1/questions/<int:id>", methods=["PUT"])
@token_required
def api_update_question_via_id(id):
    request_data = request.get_json()
    if(validate_question(request_data)):
        for question in questions:
            if question['id'] == id:
                questions[questions.index(question)] = request_data
        response = Response("", 204, mimetype='application/json')
        response.headers['Location'] = "/api/v1/questions/" + str(request_data['id'])
        return response
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to update an Invalid Question."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

@application.route("/api/v1/questions/<int:id>", methods=["DELETE"])
@token_required
def api_delete_question_via_id(id):
    question = Questions.delete_question_from_id(id)
    if question is None or question.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to delete an Invalid Question."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

    responseObject = {
        "status": "success",
        "message": "Question deleted successfully.",            
        "question": question.serialize()
    }
    return Response(dumps(responseObject), 201, mimetype='application/json')