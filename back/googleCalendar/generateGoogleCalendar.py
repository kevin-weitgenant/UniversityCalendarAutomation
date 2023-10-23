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
import base64
import json
import os

import pytz

def init_service():
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  
  
  apiInfo = os.environ["CALENDAR_API"]
  # Step 1: Decode the Base64 data
  binary_data = base64.b64decode(apiInfo)

  # Step 2: Deserialize the binary data into a JSON object
  apiInfoJson = json.loads(binary_data)
   
  
  credentials = service_account.Credentials.from_service_account_info(
        apiInfoJson, scopes=SCOPES)      
  
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
        

def countCalendars(service):
    count = 0
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        count += len(calendar_list.get('items', []))
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return count


def createCalendar(service,calendarName):

    calendar = {
        'summary': calendarName,
    }

    try:
      created_calendar = service.calendars().insert(body=calendar).execute()
      calendar_id = created_calendar['id']
      return calendar_id
    
    except Exception as e:
      return False
    

def insertEvent(service,id,eventDetails:dict,beginDateTime,endDateTime):
    event = {
  'summary': eventDetails.get('subject'),
  'location': eventDetails.get('location'),
  'description': '',
  'start': {
    'dateTime': beginDateTime,
    'timeZone': 'America/Sao_Paulo',
  },
  'end': {
    'dateTime': endDateTime,
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


def insertAcl(service,calendarId,email):
    rule = {
    'scope': {
        'type': 'user',
        'value': email
    },
    'role': 'writer'
}
    try:
     created_rule = service.acl().insert(calendarId=calendarId, body=rule).execute()
     print (created_rule)
    except Exception as e:
      return False
    

def listEvents(service,calendarId):
  page_token = None
  while True:
    events = service.events().list(calendarId=calendarId, pageToken=page_token).execute()
    for event in events['items']:
      print (event['summary'])
    page_token = events.get('nextPageToken')
    if not page_token:
      break

def deleteCalendar(service,calendarId):
  print(f"{calendarId} deleted")
  service.calendars().delete(calendarId= calendarId).execute()

def deleteAllCalendars(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            deleteCalendar(service, calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    
def rename_keys(d, keys):
    return dict([(keys.get(k), v) for k, v in d.items()])
 
#delete all calendars

service = init_service()

deleteAllCalendars(service)
# printCalendarList(service)