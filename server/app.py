from flask import request, Response

import json
from _mysql_exceptions import IntegrityError

from util import server_log
from server import app
from server.db import add_user, get_user, delete_user
from server.db import add_pattern, get_patterns_for_user, delete_pattern
from server.forms import UserForm, PatternForm

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
    form = UserForm()
    server_log("Validating user form")
    server_log(form.username.data)
    server_log(request.form.get("birthdate"))
    server_log(form.birthdate.data)
    if form.validate_on_submit():
        user = add_user(form.username.data, form.birthdate.data)
        if user is None:
            return get_http_err_response("username must be unique", 400)
        return get_http_response(user.to_dict(), 200)
    return get_http_err_response(
        "POST to /users must contain 'username'(String) and 'birthdate'(DateTime)",
        400
        )
    

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
    form = PatternForm()
    if form.validate_on_submit():
        pattern = add_pattern(form.user_id.data, form.vector.data, form.default.data)
        return get_http_response(pattern.to_dict(), 200)
    return get_http_err_response(
        "POST to /patterns must contain 'user_id'(Integer), 'vector'(Array), and 'default'(Boolean)",
        400
        )


@app.route("/patterns/<pattern_id>", methods=["DELETE"])
def patterns_pattern(pattern_id):
    try:
        pattern_id = int(pattern_id)
    except ValueError:
        return get_http_err_response(
            "Pattern must be an integer",
            400
            )
    pattern = delete_pattern(pattern_id)
    if pattern is None:
        return get_http_err_response("Pattern %d not found" % pattern_id, 404)
    return get_http_response(pattern.to_dict(), 200)

@app.route("/patterns/user/<user_id>", methods=["GET"])
def patterns_user(user_id):
    patterns = get_patterns_for_user(user_id)
    patterns = list(map(lambda p: p.to_dict(), patterns))
    return get_http_response(patterns, 200)

if __name__ == "__main__":
    app.run()
