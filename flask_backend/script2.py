import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarAgent:
    def __init__(self):
        self.creds = None
        self.calendar_service = None

    def authenticate_google_calendar(self):
        token_path = "token.json"
        credentials_path = "credentials.json"

        # Set your correct redirect URI here
        REDIRECT_URI = 'http://localhost:8000/'

        creds = self.load_credentials(token_path)
        if not creds or not creds.valid:
            creds = self.refresh_or_obtain_credentials(credentials_path, token_path, REDIRECT_URI)

        self.creds = creds
        self.calendar_service = build('calendar', 'v3', credentials=creds)

    def load_credentials(self, token_path):
        if os.path.exists(token_path):
            return Credentials.from_authorized_user_file(token_path)
        return None

    def refresh_or_obtain_credentials(self, credentials_path, token_path, redirect_uri):
        creds = None
        if os.path.exists(credentials_path):
            creds = self.refresh_credentials(credentials_path)
        else:
            creds = self.obtain_credentials(credentials_path, token_path, redirect_uri)
        return creds

    def refresh_credentials(self, credentials_path):
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", 'w') as token:
            token.write(creds.to_json())
        return creds

    def obtain_credentials(self, credentials_path, token_path, redirect_uri):
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES, redirect_uri=redirect_uri)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        return creds

    def set_appointment(self, event_summary, event_start):
        event = {
            'summary': event_summary,
            'start': {
                'dateTime': event_start.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (event_start + datetime.timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
        }
        calendar_id = 'primary'
        self.calendar_service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Appointment '{event_summary}' set for {event_start}.")

        # Send email reminder
        self.send_email_reminder(event_summary, event_start)

    def review_calendar(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.calendar_service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f'Event "{event["summary"]}" at {start}.')

    def send_email_reminder(self, event_summary, event_start):
        # Email configuration
        sender_email = "ruchikasuryawanshi721@gmail.com"
        receiver_email = "ruchikasuryawanshi710@gmail.com"
        password = "Doremon@6013"

        # Construct email content
        subject = f"Reminder: Upcoming Appointment - {event_summary}"
        body = f"Hi,\n\nThis is a reminder for your upcoming appointment:\n\n" \
               f"Event: {event_summary}\n" \
               f"Start Time: {event_start}\n\n" \
               f"Best regards,\nYour Google Calendar Agent"

        # Create MIMEText object
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    google_calendar_agent = GoogleCalendarAgent()
    google_calendar_agent.authenticate_google_calendar()
    google_calendar_agent.set_appointment("Meeting with ChatGPT", datetime.datetime.now() + datetime.timedelta(days=1))
    google_calendar_agent.review_calendar()
