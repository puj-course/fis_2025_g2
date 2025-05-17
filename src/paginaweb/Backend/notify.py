# Backend/notify.py
import requests

# Tu token y chat_id de Telegram
TELEGRAM_TOKEN = "7200520916:AAFB9qSZZd0-mGWpbU-lq2MU9bb_JKD3E2o"
CHAT_ID        = "7326632476"

def send_telegram(message: str):
    """
    Envía un mensaje al chat de Telegram definido por CHAT_ID.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print("⚠️ Error enviando Telegram:", e)
