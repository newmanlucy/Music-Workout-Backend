from flask import Flask
from server import app, db
import json
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    joindate = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "birthdate": str(self.birthdate),
            "joindate": str(self.joindate)
        }

    def __repr__(self):
        return "<User %r %r>" % (self.username, self.birthdate)


class Pattern(db.Model):
    pattern_id = db.Column(db.Integer, primary_key=True)
    default = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    vector = db.Column(db.String(258), nullable=False)

    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "default": self.default,
            "user_id": self.user_id,
            "vector": self.vector
        }

    def __repr__(self):
        return "<Pattern %r %r %r>" % (self.user_id, self.default, self.vector)


class Workout(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.pattern_id'))
    createdate = db.Column(db.DateTime, default=datetime.now())
    min_percent = db.Column(db.Float, nullable=False)
    max_percent = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "workout_id": self.workout_id,
            "user_id": self.user_id,
            "pattern_id": self.pattern_id,
            "createdate": str(self.createdate),
            "min_percent": self.min_percent,
            "max_percent": self.max_percent,
            "duration": self.duration
        }

    def __repr__(self):
        return "<Workout %r (%r-%r) %rmin>" % (self.createdate, self.min_percent*100, self.max_percent*100, self.duration)


    joshua = User
if __name__ == '__main__':
    db.create_all()
    # vec = [1,2,3]
    # w = Workout(user_id=1, pattern_id=1, min_percent=.6, max_percent=.8, duration=30)
    # db.session.add(w)
    # db.session.commit()
    # print(Workout.query.all())

    joshua = User(username="george", birthdate=datetime.now())
    print(joshua.to_dict())
