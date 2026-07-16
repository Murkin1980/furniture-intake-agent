import json
from app.services.ai import chat

INTENT_PROMPT = """Ты — AI-ассистент мебельной компании. Определи намерение клиента.

Намерения:
- inquiry: клиент спрашивает информацию (цены, сроки, услуги)
- order: клиент хочет заказать мебель
- complaint: клиент жалуется
- question: клиент задаёт вопрос по текущему заказу
- other: другое

Ответь ТОЛЬКО JSON:
{"intent": "намерение", "confidence": 0.0-1.0}"""


def recognize_intent(message: str) -> dict:
    response = chat(INTENT_PROMPT, message)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"intent": "other", "confidence": 0.5}
