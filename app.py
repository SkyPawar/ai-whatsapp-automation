from email_service.email_reader import fetch_unread
from email_service.email_sender import send_reply
from ai.reply_generator import generate_reply
import time

def run_email_bot():
    while True:
        emails = fetch_unread()
        for mail in emails:
            reply = generate_reply(mail["body"])
            send_reply(mail["from"], "Auto Reply", reply)
        time.sleep(60)

if __name__ == "__main__":
    run_email_bot()
