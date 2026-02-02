from twilio.rest import Client
from config import TWILIO_AUTH, TWILIO_SID, WHATSAPP_FROM

def send_whatsapp(to, msg):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    client.messages.create(
        body=msg,
        from_=WHATSAPP_FROM,
        to=to
    )
