from datetime import timedelta

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build


credentials = service_account.Credentials.from_service_account_file(
    settings.GOOGLE_CREDS,
    scopes=['https://www.googleapis.com/auth/calendar']
)
service = build('calendar', 'v3', credentials=credentials)


def get_events(calendar_id, start_datetime, end_datetime):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=(start_datetime + timedelta(hours=1)).isoformat("T") + "Z",
        timeMax=(end_datetime - timedelta(hours=1)).isoformat("T") + "Z",
        singleEvents=True,
        maxResults=5,
    ).execute()
    events = events_result.get('items', [])
    return events


def add_event(calendarId, event):
    return service.events().insert(calendarId=calendarId, body=event).execute()


def get_event(calendarId, eventId):
    return service.events().get(calendarId=calendarId, eventId=eventId).execute()
