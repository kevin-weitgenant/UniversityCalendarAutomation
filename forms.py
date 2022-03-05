from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms import SubmitField, StringField

class Horarios(FlaskForm):
    body = TextAreaField()
    submit = SubmitField("Calendário GoogleCalendar")
    submit2 = SubmitField("Download .ical")
    email = StringField()

class Calendario(FlaskForm):
    
    submit = SubmitField("Download .ical")
