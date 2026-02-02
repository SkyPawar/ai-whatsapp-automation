from openai import OpenAI
from config import OPENAI_API_KEY
from ai.rules import apply_rules
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_reply(message: str) -> str:
    rule_reply = apply_rules(message)
    if rule_reply:
        return rule_reply

    prompt = f"""
You are a professional business assistant.
Reply naturally and helpfully.

User message:
{message}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        return response.json()["response"].strip()

    except Exception as e:
        print("Ollama error:", e)
        return "Sorry, I am facing a technical issue right now."

