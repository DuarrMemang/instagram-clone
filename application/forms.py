from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    username = StringField("Username", validators=)
    password = PasswordField("")

class SignUpForm(FlaskForm):
    pass

class EditProfile(FlaskForm):
    pass

class CreateForm(FlaskForm):
    pass

class EditPost(FlaskForm):
    pass