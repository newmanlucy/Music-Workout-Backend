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
        add_user(username, age)
        user = {"username": username, "age": age}
        return get_http_response(user, 200)
    except IntegrityError:
        message = {"message": "username must be unique"}
        return get_http_response(message, 400)
    except Exception as e:
        message = {"message": "unexpected error: %s" % str(e)}
        return get_http_response(message, 500)


@app.route("/users/<username>", methods=["GET", "DELETE"])
def user(username):
    if request.method == "GET":
        try:
            user = get_user(username)
            server_log("USER: %s" % str(user))
            if user is None:
                message = {"message": "user not found"}
                return get_http_response(message, 404)
            return get_http_response(user, 200)
        except Exception as e:
            message = {"message": "unexpected error: %s" % str(e)}
            return get_http_response(message, 500)
    elif request.method == "DELETE":
        ret, count = delete_user(username)
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

# routes

@app.route("/workouts", methods=["POST"])
def workouts():
    pass

@app.route("/workouts/<workout_id>", methods=["DELETE"])
def workouts_workout(workout_id):
    pass

@app.route("/workouts/user/<user_id>", methods=["GET"])
def workouts_user(user_id):
    pass

if __name__ == "__main__":
    app.run()
