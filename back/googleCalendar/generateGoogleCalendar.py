from __future__ import print_function
from google.oauth2 import service_account
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from  .Google import Create_Service, convert_to_RFC_datetime
from typing import Dict, Union
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
    
def generate_Google_Calendar(dicionario: Dict, email: str) -> Union[str, bool]:
    """
    This function generates a Google Calendar with events and returns the Calendar ID.
    
    Parameters:
    dicionario (Dict): A dictionary containing event details.
    email (str): An email address to assign the calendar to.
    
    Returns:
    str: The Google Calendar ID if successful.
    bool: False if an error occurred.
    """
    
    service = init_service()
    calendar_id = createCalendar(service, "Calendario gerado")
    
    # Return False if calendar creation was unsuccessful
    if not calendar_id:
        return False 
    
    for key, value in dicionario.items():
        for eventDetails in value:
            next_day = rrule(freq=WEEKLY, dtstart=date.today(), byweekday=key.value, count=1)[0]   # calculates when will be, for example, the next monday

            begin_time = eventDetails['startTime']
            end_time = eventDetails['endTime']
            HOUR_ADJUSTMENT = 3

            begin_time = datetime(next_day.year, next_day.month, next_day.day, begin_time.hour, begin_time.minute)
            begin_time = begin_time + timedelta(hours=HOUR_ADJUSTMENT)
            begin_time = begin_time.isoformat() + 'Z'   # Google Calendar API requires RFC format: isoformat() + 'Z'
            
            end_time = datetime(next_day.year, next_day.month, next_day.day, end_time.hour, end_time.minute)
            end_time = end_time + timedelta(hours=HOUR_ADJUSTMENT)
            end_time = end_time.isoformat() + 'Z'   # Google Calendar API requires RFC format: isoformat() + 'Z'

            if insertEvent(service, calendar_id, eventDetails, begin_time, end_time) is False:
                return False
  
    if insertAcl(service, calendar_id, email) is False: 
        return False

    # Return the Google Calendar ID
    return calendar_id

if __name__ == "__main__":

  #delete all calendars

  service = init_service()

  # deleteAllCalendars(service)
  # printCalendarList(service)

