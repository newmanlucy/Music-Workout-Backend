from server.app import db
from server.models import User, Pattern, Workout
from datetime import datetime

def add_user(username, birthdate):
    user = User(username=username, birthdate=birthdate)
    db.session.add(user)
    db.session.commit()

def get_user(username):
    user = db.session.query(User).filter_by(username=username).first()
    return user

def delete_user(username):
    user = get_user(username)
    user = db.session.delete(user)

if __name__ == '__main__':
    add_user("fred", datetime.now())
    delete_user("fred")
    print(get_user("fred"))