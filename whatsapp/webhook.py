from flask import Flask, request, render_template, redirect
from ai.reply_generator import generate_reply
from whatsapp.whatsapp_sender import send_whatsapp
import logging
import os
from collections import defaultdict
import time
from admin.dashboard import read_chats
import json


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# -------- RATE LIMIT STORAGE --------
LAST_MSG_TIME = defaultdict(int)

# -------- LOGGING SETUP --------
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/messages.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# -------- HEALTH CHECK --------
@app.route("/", methods=["GET"])
def health():
    return "Server is running"

@app.route("/admin", methods=["GET"])
def admin_dashboard():
    chats = read_chats()
    active_user = request.args.get("user")
    return render_template(
        "dashboard.html",
        chats=chats,
        active_user=active_user
    )

@app.route("/admin/send", methods=["POST"])
def admin_send():
    to = request.form.get("to")
    message = request.form.get("message")

    if not to or not message:
        return redirect("/admin")

    send_whatsapp(to, message)

    logging.info(json.dumps({
        "from": "ADMIN",
        "message": message,
        "reply": f"Sent to {to}"
    }))

    return redirect("/admin")



# -------- WHATSAPP WEBHOOK --------
@app.route("/whatsapp", methods=["POST"])
def receive():
    msg = request.form.get("Body")
    sender = request.form.get("From")
    

    # Safety check
    if not msg or not sender:
        return "Invalid message", 200

    # Rate limiting (5 seconds per user)
    now = time.time()
    if now - LAST_MSG_TIME[sender] < 5:
        return "Please wait a moment.", 200

    LAST_MSG_TIME[sender] = now

    # AI reply
    reply = generate_reply(msg)

    # Send WhatsApp message
    send_whatsapp(sender, reply)

    logging.info(json.dumps({
        "from": sender,
        "message": msg,
        "reply": reply
    }))

    return "OK", 200

# -------- APP RUN --------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
