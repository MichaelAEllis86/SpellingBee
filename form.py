from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired,Optional,NumberRange,URL, AnyOf


class Guessform(FlaskForm):
    """form model to submit a new word guess"""

    guess=StringField("Guess", validators=[InputRequired(message="This field is required, please input a guess")])
    

