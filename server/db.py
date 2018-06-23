from server import db
from server.models import User, Pattern, Workout
from datetime import datetime

def add_user(username, birthdate):
    if get_user(username):
        return None
    user = User(username=username, birthdate=birthdate)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(username):
    user = db.session.query(User).filter_by(username=username).first()
    db.session.commit()
    return user

def delete_user(username):
    user = get_user(username)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return user

if __name__ == '__main__':
    add_user("fred", datetime.now())
    delete_user("fred")
    print(get_user("fred"))