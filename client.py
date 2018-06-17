import requests


BASE_URL = "http://127.0.0.1:5000"

def get_path(route):
    return BASE_URL + route

def make_post_request(route, data):
    path = get_path(route)
    r = requests.post(path, data=data)
    return r

def post_user(username, age):
    route = "/users"
    data = {"username": username, "age": age}
    return make_post_request(route, data)

def get_user(username):
    route = "/users/%s" % username
    path = get_path(route)
    return requests.get(path)

def delete_user(username):
    route = "/user/%s" % username
    path = get_path(route)
    return requests.delete(path)
