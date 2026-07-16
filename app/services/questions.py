from typing import Optional

QUESTIONS = [
    {
        "key": "name",
        "text": "Как вас зовут?",
        "required": True,
    },
    {
        "key": "city",
        "text": "В каком городе вы находитесь?",
        "required": True,
    },
    {
        "key": "kitchen_type",
        "text": "Какой тип кухни вы рассматриваете: угловая, прямая, П-образная или с островом?",
        "required": True,
    },
    {
        "key": "dimensions",
        "text": "Подскажите размеры помещения: ширина, высота, глубина (в сантиметрах)",
        "required": True,
    },
    {
        "key": "photos",
        "text": "Пришлите, пожалуйста, фото помещения (план или несколько ракурсов)",
        "required": True,
    },
    {
        "key": "style",
        "text": "Какой стиль кухни вам нравится? (современный, классический, минимализм, лофт)",
        "required": False,
    },
    {
        "key": "facades",
        "text": "Какой материал фасадов предпочитаете? (МДФ, пластик, массив, эмаль)",
        "required": False,
    },
    {
        "key": "countertop",
        "text": "Какую столешницу рассматриваете? (ламинат, камень, дерево, пластик)",
        "required": False,
    },
    {
        "key": "appliances",
        "text": "Нужна ли встроенная техника? Если да, какая?",
        "required": False,
    },
    {
        "key": "budget",
        "text": "Какой бюджет вы рассматриваете?",
        "required": False,
    },
    {
        "key": "deadline",
        "text": "Какие сроки изготовления вас интересуют?",
        "required": False,
    },
    {
        "key": "measurement",
        "text": "Вам нужен бесплатный замер?",
        "required": True,
    },
    {
        "key": "contact_time",
        "text": "Когда вам удобно, чтобы менеджер позвонил для уточнения деталей?",
        "required": False,
    },
]


def get_next_question(answered: dict) -> Optional[dict]:
    for q in QUESTIONS:
        if q["key"] not in answered:
            return q
    return None


def get_required_missing(answered: dict) -> list:
    missing = []
    for q in QUESTIONS:
        if q["required"] and q["key"] not in answered:
            missing.append(q["key"])
    return missing


def is_complete(answered: dict) -> bool:
    return len(get_required_missing(answered)) == 0
