import smtplib
from email.message import EmailMessage
from config import EMAIL_ID, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_reply(to, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ID
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ID, EMAIL_PASSWORD)
        server.send_message(msg)
