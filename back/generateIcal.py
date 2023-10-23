from icalendar import Calendar, Event,Alarm
from dateutil.rrule import rrule, WEEKLY, MO
from datetime import date, datetime, timedelta
import pytz
import uuid
import os
from typing import Dict, List
from teste import parse_schedule_text

def createEvent(calendar: Calendar, eventName: str, startDatetime: datetime, endDatetime: datetime, timezoneStr='America/Sao_Paulo') -> Calendar:
    try:
        event = Event()
        event.add('summary', eventName)

        timezone = pytz.timezone(timezoneStr)

        event.add('dtstart', timezone.localize(startDatetime, is_dst=None))
        event.add('dtend', timezone.localize(endDatetime, is_dst=None))
        event.add('rrule', {'freq': ['WEEKLY']})

        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('trigger', timedelta(minutes=-15))

        event.add_component(alarm)

        calendar.add_component(event)

        return calendar
    except Exception as e:
        print(f'An error occurred while creating the event: {e}')
        return None


def rename_keys(dictionary:Dict, conversionDict:Dict)-> Dict:
    return dict([(conversionDict.get(k), v) for k, v in dictionary.items()])

def createCalendar(scheduleDict: Dict[str, List[Dict[str, str]]])-> Calendar:
  
  cal = Calendar()
  cal.add('prodid', '-//Google Inc//Google Calendar 70.9054//EN')
  cal.add('version', '2.0')
  
  # Rename keys for easier use with "rrule"
  dayConversion = {'SEGUNDA-FEIRA': 0, 'TERÇA-FEIRA':1, 'QUARTA-FEIRA':2,'QUINTA-FEIRA':3,'SEXTA-FEIRA':4,'SÁBADO':5,'DOMINGO':6}
  scheduleDict = rename_keys(scheduleDict, dayConversion)

  for day, classes in scheduleDict.items():
      for classDetails in classes:
          nextDay = rrule(freq=WEEKLY, dtstart=date.today(), byweekday=day, count=1)[0]
          startTimeString = classDetails.get('time').split('-')[0].strip()
          endTimeString = classDetails.get('time').split('-')[-1].strip()

          startTime = datetime.strptime(startTimeString, '%H:%M')
          endTime = datetime.strptime(endTimeString, '%H:%M')

          classStartDatetime = datetime(nextDay.year, nextDay.month, nextDay.day, startTime.hour, startTime.minute)
          classEndDatetime = datetime(nextDay.year, nextDay.month, nextDay.day, endTime.hour, endTime.minute)

          cal = createEvent(cal,classDetails.get('subject'),classStartDatetime, classEndDatetime)

  return cal


  
def writeCalendar(calendar: Calendar) -> str:
    # Check if the calendar instance is valid
    if not isinstance(calendar, Calendar):
        raise ValueError("Invalid calendar instance.")

    try:
        baseDir = os.path.abspath(os.path.dirname(__file__))
        calendarDir = os.path.join(baseDir, 'calendars')
        
        # Check if the "calendars" directory exists, if not, create it.
        if not os.path.exists(calendarDir):
            os.makedirs(calendarDir)

        filePath = os.path.join(calendarDir, f'{uuid.uuid4().hex}.ics')

        with open(filePath, 'wb') as fileWriter:
            fileWriter.write(calendar.to_ical())

        return filePath
    except Exception as e:
        print(f'An error occurred while writing the calendar: {e}')
        return ""
    

schedule = parse_schedule_text()

writeCalendar(createCalendar(schedule))