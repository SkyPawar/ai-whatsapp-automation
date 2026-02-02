import imaplib
from config import EMAIL_ID, EMAIL_PASSWORD, IMAP_SERVER

def fetch_unread():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ID, EMAIL_PASSWORD)
    mail.select("inbox")

    status, data = mail.search(None, 'UNSEEN')
    return data[0].split()
