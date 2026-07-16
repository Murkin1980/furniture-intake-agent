import hashlib
import hmac
from fastapi import Request, HTTPException
from app.core.config import settings


WHATSAPP_API = "https://graph.facebook.com/v21.0"


async def send_whatsapp_message(phone: str, text: str) -> dict:
    import httpx

    url = f"{WHATSAPP_API}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"WhatsApp API error: {data}")

        return data


async def verify_webhook(mode: str, token: str, challenge: str) -> str:
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="Forbidden")


def parse_webhook_entry(entry: dict) -> list[dict]:
    messages = []
    for change in entry.get("changes", []):
        value = change.get("value", {})
        for msg in value.get("messages", []):
            messages.append({
                "from": msg.get("from"),
                "id": msg.get("id"),
                "timestamp": msg.get("timestamp"),
                "type": msg.get("type"),
                "text": msg.get("text", {}).get("body"),
            })
    return messages
