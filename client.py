import requests


BASE_URL = "http://127.0.0.1:5000"

def get_path(route):
    return BASE_URL + route

def make_post_request(route, data):
    path = get_path(route)
    r = requests.post(path, data=data)
    return r

def post_user(username, birthdate):
    route = "/users"
    data = {"username": username, "birthdate": birthdate}
    return make_post_request(route, data)

def get_user(username):
    route = "/users/%s" % username
    path = get_path(route)
    return requests.get(path)

def delete_user(username):
    route = "/users/%s" % username
    path = get_path(route)
    return requests.delete(path)

def post_pattern(user_id, vector, default):
    route = "/patterns"
    data = {
        "user_id": user_id,
        "vector": vector,
        "default": default
    }
    return make_post_request(route, data)

def get_patterns(user_id):
    route = "/patterns/user/%d" % user_id
    path = get_path(route)
    return requests.get(path)

def delete_pattern(pattern_id):
    route = "/patterns/%d" % pattern_id
    path = get_path(route)
    return requests.delete(path)