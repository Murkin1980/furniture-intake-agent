import json
from app.services.ai import chat

EXTRACT_PROMPT = """Ты — AI-ассистент мебельной компании. Извлеки факты из сообщения клиента о кухне.

Доступные поля:
- name: имя клиента
- city: город
- kitchen_type: тип кухни (угловая, прямая, П-образная, островная)
- width: ширина (число в см)
- height: высота (число в см)
- depth: глубина (число в см)
- style: стиль (современный, классический, минимализм, лофт)
- facades: материал фасадов (МДФ, пластик, массив, эмаль)
- countertop: столешница (ламинат, камень, дерево, пластик)
- appliances: нужна ли техника (да/нет)
- budget_min: минимальный бюджет (число)
- budget_max: максимальный бюджет (число)
- deadline: сроки (например, "2 недели", "в августе")
- measurement: нужен ли замер (да/нет)
- contact_time: удобное время для связи

Извлеки ТОЛЬКО те поля, которые есть в сообщении.
Ответь ТОЛЬКО JSON:
{"field": "value"}"""


def extract_facts(message: str) -> dict:
    response = chat(EXTRACT_PROMPT, message)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {}
