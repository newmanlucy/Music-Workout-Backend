from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    birthdate = DateTimeField('birthdate', format="%m/%d/%Y", validators=[DataRequired()])

class PatternForm(FlaskForm):
    user_id = IntegerField('user_id', validators=[DataRequired()])
    vector = StringField('vector', validators=[DataRequired()])
    default = BooleanField('default', validators=[DataRequired()])