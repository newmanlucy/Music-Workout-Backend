from flask import request, Response

import json
from _mysql_exceptions import IntegrityError

from util import server_log
from server.db import add_user, get_user, delete_user
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
    if username is None:
        return get_http_err_response("must provide a username", 400)
    birthdate = request.form.get("birthdate")
    if birthdate is None:
        return get_http_err_response("must provide a birthdate", 400)
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

@app.route("/patterns", methods=["POST"])
def patterns():
    user_id = request.form.get("user_id")
    if user_id is None:
        pass
    vector = request.form.get("vector")
    default = request.form.get("default")

@app.route("/patterns/<pattern_id>", methods=["DELETE"])
def patterns_pattern(pattern_id):
    pass

@app.route("/patterns/user/<user_id>", methods=["GET"])
def patterns_user(user_id):
    pass

if __name__ == "__main__":
    app.run()
