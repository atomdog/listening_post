from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText
import base64
import html
from bs4 import BeautifulSoup
def initservice():
    creds = ""
    if os.path.exists('./google-apis/token.json'):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose', 'https://mail.google.com/']
        creds = Credentials.from_authorized_user_file('./google-apis/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    service = build('gmail', 'v1', credentials=creds)
    return(service)

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def create_message_with_attachment(sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
    #return(message)
    except Exception as e:
        print(e)

def fetch_messages(service, userid):
    results = service.users().messages().list(userId=userid,labelIds = ['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])
    messagelist = []
    for message in messages:
        msg = service.users().messages().get(userId=userid, id=message['id']).execute()
        time = msg['payload']['headers'][1]['value']
        whena = time.find(";")+1
        when = time[whena:len(time)]
        x = 0
        while(when[x] == ' '):
            when = when[1:len(when)]
        contents = msg['snippet']
        contents= html.unescape(contents)
        messagelist.append([when,msg['payload']['headers'][19]['value'], contents])
        service.users().messages().modify(userId=userid, id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    #print(messagelist)
    return(messagelist)

def fetch_all_messages(service, userid, boxname):
    results = service.users().messages().list(userId=userid,labelIds = [boxname]).execute()
    messages = results.get('messages', [])
    messagelist = []
    best_decode = []
    count = 0
    for message in messages:
        print(str(count)+" of "+ str(len(messages))+ " emails...")
        count+=1
        msg = service.users().messages().get(userId=userid, id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']

        if(payload.get('parts')!=None):
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
            soup = BeautifulSoup(decoded_data , "lxml")
            if(data!=None and soup!=None):
                try:
                    body = soup.body()
                except:
                    body = decoded_data
            else:
                body = decoded_data
            best_decode.append({"Subject": subject, "From": sender, "Message": body})
            #print("Subject: ", subject)
            #print("From: ", sender)
            #print("Message: ", body)
            #print('\n')
    #print(messagelist)
    return(best_decode)
def readMail():
    return(fetch_messages(initservice(), "usatodaytwitter7@gmail.com"))

def readAllMail():
    return(fetch_all_messages(initservice(), "usatodaytwitter7@gmail.com", 'SPAM') + fetch_all_messages(initservice(), "usatodaytwitter7@gmail.com", 'INBOX'))
