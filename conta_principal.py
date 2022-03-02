from pprint import pprint
from Google import Create_Service, convert_to_RFC_datetime
from teste import listEvents, createCalendar,insertAcl,insertEvent,printCalendarList


CLIENT_SECRET_FILE = 'principal.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


printCalendarList(service)
id = createCalendar(service, "agora vai meu camarada")
insertEvent(service, id)