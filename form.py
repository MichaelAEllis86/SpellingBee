from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired,Optional,NumberRange,URL, AnyOf


class Guessform(FlaskForm):
    """form model to submit a new word guess"""

    guess=StringField("Guess", validators=[InputRequired(message="This field is required, please input a guess")])

class Userform(FlaskForm):
    """form model to add a new user"""

    # email=StringField("Email", validators=[Email(message="hey hey hey u cant park here! no parking!")])
    username=StringField("Username", validators=[InputRequired(message="This field is required, please add a user name")])
    image=StringField("image url",validators=[Optional(), URL(require_tld=False, message="please enter a valid URL for your avatar photo")])

