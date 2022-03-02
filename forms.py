from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms import SubmitField, StringField

class Horarios(FlaskForm):
    body = TextAreaField()
    submit = SubmitField("Gerar Calendario")
    email = StringField("e-mail")

class Calendario(FlaskForm):
    
    submit = SubmitField("Download .ical")
