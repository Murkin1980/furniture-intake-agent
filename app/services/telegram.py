import httpx
from app.core.config import settings

TELEGRAM_API = "https://api.telegram.org/bot{token}"


async def send_message(chat_id: int, text: str, reply_markup: dict | None = None) -> dict:
    url = f"{TELEGRAM_API.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()


async def send_lead_notification(chat_id: int, lead: dict, summary: str, lead_id: str) -> dict:
    text = format_lead_message(lead, summary)
    reply_markup = build_lead_buttons(lead_id)

    return await send_message(chat_id, text, reply_markup)


def format_lead_message(lead: dict, summary: str) -> str:
    name = lead.get("name") or "Не указано"
    city = lead.get("city") or "Не указан"
    phone = lead.get("phone") or "Не указан"

    return f"""🆕 <b>Новая заявка</b>

<b>Клиент:</b> {name}
<b>Телефон:</b> {phone}
<b>Город:</b> {city}

<b>Резюме:</b>
{summary}"""


def build_lead_buttons(lead_id: str) -> dict:
    base_url = "http://localhost:8000"

    return {
        "inline_keyboard": [
            [
                {"text": "✅ Взять в работу", "callback_data": f"take:{lead_id}"},
                {"text": "💬 Запросить данные", "callback_data": f"request:{lead_id}"},
            ],
            [
                {"text": "📏 Назначить замер", "callback_data": f"measure:{lead_id}"},
            ],
            [
                {"text": "📋 Открыть заявку", "url": f"{base_url}/lead/{lead_id}"},
            ],
        ]
    }


async def answer_callback_query(callback_query_id: str, text: str | None = None) -> dict:
    url = f"{TELEGRAM_API.format(token=settings.TELEGRAM_BOT_TOKEN)}/answerCallbackQuery"

    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()


async def edit_message_reply_markup(chat_id: int, message_id: int, reply_markup: dict | None = None) -> dict:
    url = f"{TELEGRAM_API.format(token=settings.TELEGRAM_BOT_TOKEN)}/editMessageReplyMarkup"

    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()
