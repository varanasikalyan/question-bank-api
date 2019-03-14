from flask import request, Response
from json import dumps
from root import application
from models.modules import *
from decorators import *

@application.route("/api/v1/modules/all", methods=["GET"])
def api_modules_all():
    responseObject = {
        "status": "success",
        "message": "Retrieved all Modules successfully.",            
        "module": Modules.get_all_modules()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules/creator/<int:id>/latest/<int:count>", methods=["GET"])
def api_modules_creator_latest_count(id, count):
    responseObject = {
        "status": "success",
        "message": "Retrieved Modules successfully.",            
        "modules": Modules.get_modules_latest_count(count, id)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules/latest/<int:count>", methods=["GET"])
def api_modules_latest_count(count):
    responseObject = {
        "status": "success",
        "message": "Retrieved Modules successfully.",            
        "modules": Modules.get_modules_latest_count(count, None)
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules", methods=["GET"])
def api_modules():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Module, no (id) field provided. please specify an (id)."
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

    module = Modules.get_module_from_id(id)
    responseObject = {
        "status": "success",
        "message": "Module retrieved successfully.",            
        "module": module.serialize()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules/<int:id>", methods=["GET"])
def api_modules_via_id(id):
    module = Modules.get_module_from_id(id)
    if module.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Module."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')
    responseObject = {
        "status": "success",
        "message": "Module retrieved successfully.",            
        "module": module.serialize()
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules/creator", methods=["GET"])
def api_modules_creator():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Module, no (id) field provided. please specify an (id)."
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

    modules = Modules.get_module_from_creator_id(id)
    responseObject = {
        "status": "success",
        "message": "Module retrieved successfully.",            
        "module": modules
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules/creator/<int:id>", methods=["GET"])
def api_modules_via_creator_id(id):
    modules = Modules.get_module_from_creator_id(id)
    if module.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to retrieve an Invalid Module."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')
    responseObject = {
        "status": "success",
        "message": "Module retrieved successfully.",            
        "module": modules
    }
    return Response(dumps(responseObject), 200, mimetype='application/json')

@application.route("/api/v1/modules", methods=["POST"])
#@token_required
def api_add_module():
    request_data = request.get_json()
    if(Modules.validate_module(request_data)):
        module = Modules.submit_module_from_json(request_data)
        if module is None or module.id < 0:
            responseObject = {
                "status": "failure",
                "message": "Failed to add an Invalid Module."                
            }
            return Response(dumps(responseObject), 500, mimetype='application/json')
        responseObject = {
            "status": "success",
            "message": "Module added successfully.",            
            "module": module.serialize()
        }
        return Response(dumps(responseObject), 201, mimetype='application/json')
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to add an Invalid Module."                
        }
        return Response(dumps(responseObject), 400, mimetype='application/json')

@application.route("/api/v1/modules/<int:id>", methods=["PUT"])
@token_required
def api_update_module_via_id(id):
    request_data = request.get_json()
    if(validate_module(request_data)):
        for module in modules:
            if module['id'] == id:
                modules[modules.index(module)] = request_data
        response = Response("", 204, mimetype='application/json')
        response.headers['Location'] = "/api/v1/modules/" + str(request_data['id'])
        return response
    else:
        responseObject = {
            "status": "failure",
            "message": "Failed to update an Invalid Module."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

@application.route("/api/v1/modules/<int:id>", methods=["DELETE"])
@token_required
def api_delete_module_via_id(id):
    module = Modules.delete_module_from_id(id)
    if module is None or module.id < 0:
        responseObject = {
            "status": "failure",
            "message": "Failed to delete an Invalid Module."                
        }
        return Response(dumps(responseObject), 404, mimetype='application/json')

    responseObject = {
        "status": "success",
        "message": "Module deleted successfully.",            
        "module": module.serialize()
    }
    return Response(dumps(responseObject), 201, mimetype='application/json')