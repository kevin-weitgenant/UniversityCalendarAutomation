from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms import SubmitField

class Horarios(FlaskForm):
    body = TextAreaField()
    submit = SubmitField("Gerar Calendario")