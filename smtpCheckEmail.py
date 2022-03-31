import credLib
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from imap_tools import MailBox, AND
import email
def checkemail():
    inbox = []
    with MailBox('imap.gmail.com').login(credLib.returnbykey('email', 'emailU'), credLib.returnbykey('email', 'emailP'), 'INBOX') as mailbox:
    # get unseen emails from INBOX folder
        counter = 0
        print(str(counter) + "  emails")
        for msg in mailbox.fetch(AND(seen=False)):
            print(str(counter) + "  emails", end = " ")
            mtext = msg.html
            inbox.append([msg.from_values["email"], mtext])
    return(inbox)
