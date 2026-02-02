import os
import json
from collections import defaultdict

LOG_FILE = "logs/messages.log"

def read_chats(limit=200):
    chats = defaultdict(list)

    if not os.path.exists(LOG_FILE):
        return {}

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[-limit:]:
        try:
            _, json_part = line.split("|", 1)
            data = json.loads(json_part.strip())
            sender = data.get("from")

            if sender:
                chats[sender].append(data)
        except:
            continue

    return chats
