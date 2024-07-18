import eel
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

eel.init('web')

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_messages(service):
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    return messages

def get_message_details(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    snippet = msg.get('snippet')
    headers = msg.get('payload').get('headers')
    subject = next(header['value'] for header in headers if header['name'] == 'Subject')
    sender = next(header['value'] for header in headers if header['name'] == 'From')
    return {'snippet': snippet, 'subject': subject, 'sender': sender}

@eel.expose
def fetch_gmail_messages():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    messages = get_messages(service)
    message_details = [get_message_details(service, msg['id']) for msg in messages]
    return message_details

eel.start('developer.html', size=(800, 600))
