from app.services.ai import chat

SUMMARY_PROMPT = """Ты — AI-ассистент мебельной компании. Сформируй краткое резюме заявки на кухню.

Данные клиента:
{data}

Сформируй резюме в формате:
1. Имя клиента
2. Город
3. Тип кухни
4. Размеры
5. Стиль и пожелания
6. Бюджет и сроки
7. Нужен ли замер
8. Контактное время

Будь кратким и конкретным. Используй тезисы."""


def generate_summary(data: dict) -> str:
    formatted_data = "\n".join(f"- {k}: {v}" for k, v in data.items())
    return chat(SUMMARY_PROMPT.format(data=formatted_data), "Сформируй резюме")
