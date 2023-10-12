from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=12)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Sign Up")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min = 8, max = 12)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message = "Password must match!")])
    submit = SubmitField("Sign Up")

class EditProfile(FlaskForm):
    profile_picture =  StringField("Profile_picture")
    username = StringField("Username")
    nickname = StringField("Nickname")
    bio = TextAreaField("Bio")
    submit = SubmitField("Confirm")

class CreatePost(FlaskForm):
    post = StringField("Post", validators=[DataRequired()])
    caption = StringField("Caption")
    submit = SubmitField("Post")

class EditPost(FlaskForm):
    caption = StringField("Caption", validators=[DataRequired()])
    submit = SubmitField("Confirm ")