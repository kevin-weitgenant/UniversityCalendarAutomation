from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms import SubmitField, StringField

class Horarios(FlaskForm):
    body = TextAreaField()
    submit = SubmitField("Calendário GoogleCalendar")
    submit = SubmitField("Arquivo .ical")
    email = StringField()


