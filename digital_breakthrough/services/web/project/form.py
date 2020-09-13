from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    name = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
