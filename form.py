from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length, Optional,NumberRange,URL, AnyOf


class Guessform(FlaskForm):
    """form model to submit a new word guess"""

    guess=StringField("Guess", validators=[InputRequired(message="This field is required, please input a word guess")])

class Dictionaryform(FlaskForm):
    """form model to submit a word to the dictionary api for word information"""

    dictionarysearch=StringField("Search", validators=[InputRequired(message="This field is required, please input a search term")])


class Userform(FlaskForm):
    """form model to add a new user"""

    username=StringField("Username", validators=[InputRequired(message="This field is required, please add a username")])
    password=PasswordField("password",validators=[InputRequired(message="This field is required, please add a secure password!"), EqualTo("confirm_password",message="passwords must match"),Length(min=7, message="password must be at least 7 characters")])
    confirm_password=PasswordField("confirm_password",validators=[InputRequired(message="This field is required, please confirm your password!")])
    image=StringField("image url",validators=[InputRequired(message="This field is required, add a url for profile avatar"), URL(require_tld=False, message="please enter a valid URL for your avatar photo")])

class Loginform(FlaskForm):
    """form model to login a user, contains username and password fields"""
    username=StringField("Username", validators=[InputRequired(message="This field is required, please add a user name")])
    password=PasswordField("password",validators=[InputRequired(message="This field is required, please enter your password")])

