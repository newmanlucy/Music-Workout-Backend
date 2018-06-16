from flask import Flask, request, Response
import json
from _mysql_exceptions import IntegrityError

from util import server_log
from server.db import add_user, get_user, delete_user

app = Flask(__name__)

def get_http_response(response_dict, status):
    """
    return a response with the given data and status of type application/json
    """
    response = json.dumps(response_dict)
    return Response(response, status=status, mimetype='application/json')


@app.route("/", methods=["GET"])
def root():
    return "Music workout app API"


@app.route("/users", methods=["POST"])
def users():
    server_log(request.data)
    server_log(str(request.form.get("username")))
    username = request.form.get("username")
    if username is None:
        message = {"message": "must provide a username"}
        return get_http_response(message, 400)
    age = request.form.get("age")
    if age is None:
        message = {"message": "must provide an age"}
        res = get_http_response(message, 400)
        server_log("RES: " + str(res))
        return res
    try:
        add_user(username, age)
        user = {"username": username, "age": age}
        return get_http_response(user, 200)
    except IntegrityError:
        message = {"message": "username must be unique"}
        return get_http_response(message, 400)
    except Exception as e:
        message = {"message": "unexpected error: %s" % str(e)}
        return get_http_response(message, 500)


@app.route("/user/<username>", methods=["GET", "DELETE"])
def user(username):
    if request.method == "GET":
        pass
    elif request.method == "DELETE":
        pass

if __name__ == "__main__":
    app.run()
