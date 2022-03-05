from __future__ import print_function
from google.oauth2 import service_account
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Google import Create_Service, convert_to_RFC_datetime

from dateutil.rrule import rrule, WEEKLY, MO
from datetime import date, datetime, timedelta
from create_calendar import ajustar
from service import info          # COMENTAR QUANDO DER DEPLOY
import os
import ast
import pytz

def init_service():
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  
  # string of dictionary was passed as environment variable, this next line converts this string to a dictionary 
  
  #info = ast.literal_eval(os.environ["info"])   
  credentials = service_account.Credentials.from_service_account_info(
          info, scopes=SCOPES)


  service = build('calendar', 'v3', credentials=credentials)
  return service

def printCalendarList(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print (f" {calendar_list_entry['id']}: {calendar_list_entry['summary']}  " )
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def createCalendar(service,summary):

    calendar = {
        'summary': summary,
    }

    try:
      created_calendar = service.calendars().insert(body=calendar).execute()
      calendar_id = created_calendar['id']
      return calendar_id
    
    except Exception as e:
      return False
    

def insertEvent(service,id,summary,begin,end):
    event = {
  'summary': summary,
  'location': '',
  'description': '',
  'start': {
    'dateTime': begin,
    'timeZone': 'America/Sao_Paulo',
  },
  'end': {
    'dateTime': end,
    'timeZone': 'America/Sao_Paulo',
  },
  'recurrence': [
    'RRULE:FREQ=WEEKLY'
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 5},
      {'method': 'popup', 'minutes': 5},
    ],
  }


}
    try:
      event = service.events().insert(calendarId= id, body=event).execute()
      print ('Event created: %s' % (event.get('htmlLink')))
    except Exception as e:
      return False


def insertAcl(service,id,email):
    rule = {
    'scope': {
        'type': 'user',
        'value': email
    },
    'role': 'writer'
}
    try:
     created_rule = service.acl().insert(calendarId=id, body=rule).execute()
     print (created_rule)
    except Exception as e:
      return False
    

def listEvents(service,id):
  page_token = None
  while True:
    events = service.events().list(calendarId=id, pageToken=page_token).execute()
    for event in events['items']:
      print (event['summary'])
    page_token = events.get('nextPageToken')
    if not page_token:
      break

def deleteCalendar(service,id):
  service.calendars().delete(calendarId= id).execute()

def deleteAllCalendars(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            deleteCalendar(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def rename_keys(d, keys):
    return dict([(keys.get(k), v) for k, v in d.items()])


def sum_hours(a,b):
  sum = a+b
  if sum >23:
    return sum-24
  else: return sum 

  
def generate_calendar(dicionario,email):
  conversao = {'SEGUNDA-FEIRA': 0, 'TERÇA-FEIRA':1, 'QUARTA-FEIRA':2,'QUINTA-FEIRA':3,'SEXTA-FEIRA':4,'SÁBADO':5,'DOMINGO':6, 'SABADO' : 5}
  dicionario = rename_keys(dicionario,conversao)
  
  service = init_service()
  calendar_id = createCalendar(service,"Calendario Gerado")
  if calendar_id is False:
    return False 
  
  for k,v in dicionario.items():
    for summary, value in v.items():
      
      next_day = rrule(freq=WEEKLY, dtstart=date.today(), byweekday=k, count=1)[0]   #calculates when will be,for example, the next monday
      begin_time = datetime.strptime(ajustar(value)[0][0], '%H:%M')
      end_time = datetime.strptime(ajustar(value)[0][1], '%H:%M')
      
      HOUR_ADJUSTMENT = 3

      begin_time = datetime(next_day.year,next_day.month,next_day.day, begin_time.hour, begin_time.minute)
      begin_time = begin_time + timedelta(hours= HOUR_ADJUSTMENT)
      begin_time = begin_time.isoformat() + 'Z'   #google calendar api requires RFC format: isoformat() + 'Z'
      
      end_time = datetime(next_day.year,next_day.month,next_day.day, end_time.hour, end_time.minute)
      end_time = end_time + timedelta(hours= HOUR_ADJUSTMENT)
      end_time = end_time.isoformat() + 'Z'   #google calendar api requires RFC format: isoformat() + 'Z'

      if insertEvent(service,calendar_id, summary, begin_time, end_time) is False:
        return False
  
  if insertAcl(service,calendar_id,email)is False: return False
  return calendar_id