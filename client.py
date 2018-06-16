import requests

BASE_URL = "http://127.0.0.1:5000"

def make_post_request(route, data):
    path = BASE_URL + route
    r = requests.post(path, data=data)
    return r

def post_user(username, age):
    route = "/users"
    data = {"username": username, "age": age}
    return make_post_request(route, data)

def get_user(username):
    pass

def delete_user(username):
    pass
