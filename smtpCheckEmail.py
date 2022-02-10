import credLib
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from imap_tools import MailBox, AND
import email
def checkemail():
    inbox = []
    with MailBox('imap.gmail.com').login(credLib.returnbykey('email', 'emailU'), credLib.returnbykey('email', 'emailP'), 'INBOX') as mailbox:
    # get unseen emails from INBOX folder
        for msg in mailbox.fetch(AND(seen=False)):
            mtext = msg.html
            b = mtext.find("<td>")
            e = mtext.find("</td>")
            mtext = mtext[b+4:e]
            cutter = False
            counter = -1
            unpad = len(mtext)-48
            mtext = mtext.replace("\n", "")
            mtext = mtext.replace("\r", "")
            mtext = mtext.lstrip()
            mtext = mtext.rstrip()
            inbox.append([msg.from_values["email"], mtext])
            return(inbox)
