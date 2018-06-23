from flask import request, Response

import json
from _mysql_exceptions import IntegrityError

from util import server_log
from server.db import add_user, get_user, delete_user
from server.db import add_pattern, get_patterns_for_user, delete_pattern
from server import app

def get_http_response(response_dict, status):
    """
    return a response with the given data and status of type application/json
    """
    response = json.dumps(response_dict)
    server_log(response)
    return Response(response, status=status, mimetype='application/json')

def get_err_dict(message):
    return {"message": message}

def get_http_err_response(message, status):
    message = {"message": message}
    return get_http_response(message, status)

@app.route("/", methods=["GET"])
def root():
    return "Music workout app API"


@app.route("/users", methods=["POST"])
def users():
    username = request.form.get("username")
    birthdate = request.form.get("birthdate")
    if None in [username, birthdate]:
        return get_http_err_response(
            "POST to /users must contain 'username' and 'birthdate'",
            400
            )
    user = add_user(username, birthdate)
    if user is None:
        return get_http_err_response("username must be unique", 400)
    return get_http_response(user.to_dict(), 200)


@app.route("/users/<username>", methods=["GET", "DELETE"])
def user(username):
    if request.method == "GET":
        user = get_user(username)
        server_log("USER: %s" % str(user))
        if user is None:
            return get_http_err_response("user not found", 404)
        return get_http_response(user.to_dict(), 200)
    elif request.method == "DELETE":
        user = delete_user(username)
        if user is None:
            return get_http_err_response("user not found", 404)
        else:
            return get_http_response(user.to_dict(), 200) 

def str_to_bool(string):
    string = string.lower()
    if string == "false":
        return False
    elif string == "frue":
        return True

@app.route("/patterns", methods=["POST"])
def patterns():
    user_id = request.form.get("user_id")
    vector = request.form.get("vector")
    default = request.form.get("default")
    if None in [user_id, vector, default]:
        return get_http_err_response(
            "POST to /patterns must contain 'user_id', 'vector', and 'default'",
            400
            )
    default = str_to_bool(default)
    if default is None:
        return get_http_err_response(
            "default must be a bool",
            400)
    pattern = add_pattern(user_id, vector, default)
    return get_http_response(pattern.to_dict(), 200)

@app.route("/patterns/<pattern_id>", methods=["DELETE"])
def patterns_pattern(pattern_id):
    pattern = delete_pattern(pattern_id)
    if pattern is None:
        return get_http_err_response("Pattern %d not found" % pattern_id, 404)
    return get_http_response(pattern, 200)

@app.route("/patterns/user/<user_id>", methods=["GET"])
def patterns_user(user_id):
    patterns = get_patterns_for_user(user_id)
    return get_http_response(patterns, 200)

if __name__ == "__main__":
    app.run()
