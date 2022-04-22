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
import time
import chunkGen
import re
import sys
sys.path.insert(0, './google-apis')
import gmailfunctions

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
def readFullInbox():
    #thanks to https://gist.github.com/tihawk/afd7a68648324d9033a77abe8751b8ab
    #for fixing imaplib etc for current python
    q = chunkGen.docprocgen()
    while(next(q)!=True):
        time.sleep(0.01)

def readNewInbox():
    q = gmailfunctions.readAllMail()
    with open("memory/inbox.txt", 'w') as out:
        for x in range(0, len(q)):
            towrite = q[x]
            out.write(str(towrite))
            out.write("\n")
            out.write("==INTERRUPT==")
            out.write("\n")
readNewInbox()
#write_to_txt(receiveMail())
