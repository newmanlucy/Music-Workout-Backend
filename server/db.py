from server import db
from server.models import User, Pattern, Workout
from datetime import datetime
from sqlalchemy import or_
import json

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

def add_pattern(user_id, vector, default):
    pattern = Pattern(user_id=user_id, default=default, vector=json.dumps(vector))
    db.session.add(pattern)
    db.session.commit()
    return pattern

def get_patterns_for_user(user_id):
    patterns = db.session.query(Pattern).\
        filter(or_(Pattern.user_id == user_id, Pattern.default)).\
        all()
    db.session.commit()
    return patterns

def get_pattern_by_id(pattern_id):
    pattern = db.session.query(Pattern).\
        filter_by(pattern_id=pattern_id).\
        first()
    db.session.commit()
    return pattern

def delete_pattern(pattern_id):
    pattern = get_pattern_by_id(pattern_id)
    if pattern is not None:
        db.session.delete(pattern)
        db.session.commit()
    return pattern


if __name__ == '__main__':
    patterns = get_patterns_for_user(59)
    print(patterns)