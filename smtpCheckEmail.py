import credLib
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from imap_tools import MailBox, AND
import email
import smtplib
import time
import imaplib
import email
from bs4 import BeautifulSoup
import html2text
import traceback
import re
def write_to_txt(inbo):
    with open('memory/inbox.txt', 'w') as f:
        for x in range(0, len(inbo)):
            print(inbo[0])
            f.write('\n'.join(inbo[x]))
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
    f.close()

def dirty_clean(mess):
    for x in range(0, 9):
        slicer = mess.find("quotedprintable")+ len("quotedprintable")
        mess = mess[slicer:]
        slicer = mess.find("textplain")+ len("textplain")
        mess = mess[slicer:]
        slicer = mess.find("Sent to usatodaytwitter7gmailcom")
        mess = mess[:slicer]
    return(mess)
def remove_tags(em):
    if(em is None):
        return("")
    try:
        soup = BeautifulSoup(em, "html.parser")
        for data in soup(['style', 'script']):
            data.decompose()
            rt = ' '.join(soup.stripped_strings)
            rt = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|", "", rt)
            return(rt)
    except:
        return(em)

def receiveMail():
    #thanks to https://gist.github.com/tihawk/afd7a68648324d9033a77abe8751b8ab
    #for fixing imaplib etc for current python
    inbo = []
    try:
        imapServer = "imap.gmail.com"
        imapPort = 993
        imap = imaplib.IMAP4_SSL(imapServer, imapPort)
        print("logging in...")
        imap.login(credLib.returnbykey('email', 'emailU'),  credLib.returnbykey('email', 'emailP'))
    except Exception as err:
        print(err)
    print("logged in")
    imap.select('inbox')
    print("searching...")
    typ, data = imap.search(None, "ALL")
    mailIds = str(data[0])[2:-1]
    idList = mailIds.split()
    print("fetching...")
    try:
        for i, emailId in enumerate(idList):
            typ, data = imap.fetch(emailId, '(RFC822)' )
            print("parsing...")
            for response_part in data:
                if(isinstance(response_part, tuple)):
                    email_msg = email.message_from_string(response_part[1].decode('utf8'))
                    #email_msg2 = email.message_from_string(response_part[len(response_part)-1].decode('utf8'))
                    email_subject = email_msg["subject"]
                    email_from = email_msg["from"]
                    if(not("<notify@twitter.com>" in email_from or "<info@twitter.com>" in email_from)):
                        efrom, encoding = email.header.decode_header(email_from)[0]
                        print("From: {}\n".format(efrom))
                        subj, encoding = email.header.decode_header(email_subject)[0]
                        print("Subject: {}\n".format(subj))
                        contents = remove_tags(email_msg.get_payload(decode=True))
                        if(contents == ''):
                            contents = dirty_clean(str(email_msg))
                            contents = remove_tags(contents)
                        print(contents)
                        inbo.append([str(efrom), str(subj), str(contents)])
    except Exception as err:
        print(err)
    finally:
        imap.logout()
        return(inbo)


write_to_txt(receiveMail())
