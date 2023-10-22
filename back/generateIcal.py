from icalendar import Calendar, Event,Alarm
from dateutil.rrule import rrule, WEEKLY, MO
from datetime import date, datetime, timedelta
import pytz
import uuid
import os

def createCalEvent(cal,eventName,start, end):                                
  event = Event()
  event.add('summary', eventName)
  tzone = pytz.timezone('America/Sao_Paulo')

  event.add('dtstart', tzone.localize(start, is_dst=None))
  event.add('dtend', tzone.localize(end, is_dst=None))
  event.add('rrule', {'freq': ['WEEKLY']})

  alarm = Alarm()
  alarm.add('action', 'DISPLAY')
  alarm.add('trigger', timedelta(minutes=-10))
  event.add_component(alarm)
  cal.add_component(event)


def createCalendar(dicionario):
  cal = Calendar()
  cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
  cal.add('version', '2.0')

  for key,value in dicionario.items():
    for dictionary in value:
      next_day = rrule(freq=WEEKLY, dtstart=date.today(), byweekday=key, count=1)[0]
      
      aulas = ajustar(value)
      
      for x in range(len(aulas)):
        time = datetime.strptime(aulas[x][0], '%H:%M')
        end_time = datetime.strptime(aulas[x][1], '%H:%M')
      
        comeco = datetime(next_day.year,next_day.month,next_day.day, time.hour, time.minute)
        fim = datetime(next_day.year,next_day.month,next_day.day, end_time.hour, end_time.minute)

        createEvent(cal,key,comeco, fim)

  
  def writeCalendar():
    basedir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(basedir,f'calendars/{uuid.uuid4().hex}.ics')
    with open(f'{filepath}', 'wb') as fw:
      fw.write(cal.to_ical())
    return filepath