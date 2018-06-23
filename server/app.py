from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy

import json
from _mysql_exceptions import IntegrityError

from util import server_log
# from server.db import add_user, get_user, delete_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/music_workout"
db = SQLAlchemy(app)

def get_http_response(response_dict, status):
    """
    return a response with the given data and status of type application/json
    """
    response = json.dumps(response_dict)
    server_log(response)
    return Response(response, status=status, mimetype='application/json')


@app.route("/", methods=["GET"])
def root():
    return "Music workout app API"


@app.route("/users", methods=["POST"])
def users():
    username = request.form.get("username")
    if username is None:
        message = {"message": "must provide a username"}
        return get_http_response(message, 400)
    age = request.form.get("age")
    if age is None:
        message = {"message": "must provide an age"}
        res = get_http_response(message, 400)
        return res
    try:
        server_log("HERE")
        user_id = add_user(username, age)
        server_log(str(user_id))
        user = {"username": username, "age": age, "user_id": user_id}
        server_log(user)
        return get_http_response(user, 200)
    except IntegrityError:
        message = {"message": "username must be unique"}
        return get_http_response(message, 400)


@app.route("/users/<username>", methods=["GET", "DELETE"])
def user(username):
    if request.method == "GET":
        user = get_user(username)
        server_log("USER: %s" % str(user))
        if user is None:
            message = {"message": "user not found"}
            return get_http_response(message, 404)
        return get_http_response(user, 200)
    elif request.method == "DELETE":
        ret, count = delete_user(username)
        print(("DELETE", ret, count))
        if count == 0:
            message = {"message": "user not found"}
            return get_http_response(message, 404)
        elif count == 1:
            message = {"message": "success"}
            return get_http_response(message, 200) 

@app.route("/patterns", methods=["POST"])
def patterns():
    pass

@app.route("/patterns/<pattern_id>", methods=["DELETE"])
def patterns_pattern(pattern_id):
    pass

@app.route("/patterns/user/<user_id>", methods=["GET"])
def patterns_user(user_id):
    pass

if __name__ == "__main__":
    app.run()
