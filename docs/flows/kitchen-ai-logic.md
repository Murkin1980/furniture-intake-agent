# Детальный сценарий: Заявка на кухню (AI-логика)

## Назначение

Этот документ описывает точную логику AI-приёмщика при обработке заявки на кухню. Каждое действие AI должно соответствовать этому сценарию.

---

## Состояния разговора

```python
class ConversationState:
    GREETING = "greeting"
    KITCHEN_TYPE = "kitchen_type"
    DIMENSIONS = "dimensions"
    CITY = "city"
    PHOTOS = "photos"
    STYLE = "style"
    FACADES = "facades"
    APPLIANCES = "appliances"
    BUDGET = "budget"
    DEADLINE = "deadline"
    MEASUREMENT = "measurement"
    CONTACT_TIME = "contact_time"
    SUMMARY = "summary"
    HANDOFF = "handoff"
    HUMAN_MODE = "human_mode"
```

---

## Логика переходов

### 1. Начальное сообщение

**Триггер:** Первое сообщение от клиента

**Анализ:**
- Если содержит «кухня» → переход в `GREETING`
- Если содержит фото без текста → переход в `GREETING` с анализом фото
- Если не по теме → вежливый ответ с наведением на тему

**AI-действие:**
```
Создать Lead (status: new)
Создать Conversation (mode: ai_mode)
Создать IntakeSession (furniture_type: kitchen)
Переход в GREETING
```

### 2. Приветствие (GREETING)

**Вопрос:**
```
Здравствуйте! Я помогу рассчитать стоимость вашей кухни.

Подскожите, какой формы кухня вам нужна?
1. Прямая
2. Угловая
3. П-образная
4. С островом
5. Ещё не определился
```

**Обработка ответа:**
- Если выбрал вариант 1–4 → извлечь тип, переход в `DIMENSIONS`
- Если выбрал 5 → переход в `DIMENSIONS` с пометкой `kitchen_type: unknown`
- Если ответ не по варианту → попробовать извлечь из текста
- Если не удаётся → повторить вопрос с вариантами

**Сохранение:**
```json
{
  "question_key": "kitchen_type",
  "question_text": "Какой формы кухня вам нужна?",
  "answer_text": "Угловая",
  "answer_data": {"type": "corner"}
}
```

### 3. Размеры (DIMENSIONS)

**Вопрос:**
```
Подскажите примерные размеры кухни?
Можно в сантиметрах, метрах или просто описать.
```

**Подсказка (если клиент затрудняется):**
```
Например:
— Длинная стена: 3000 мм
— Короткая стена: 2100 мм
— Высота: 2500 мм

Или просто: «3 метра на 2.5»
```

**Обработка ответа:**
- Если есть числа → парсинг в формат `{length, width, height}`
- Если есть фото с размерами → анализ изображения
- Если «не знаю» → пометить как `missing`, переход в `CITY`
- Если описание → попробовать извлечь

**Сохранение:**
```json
{
  "question_key": "dimensions",
  "question_text": "Подскажите примерные размеры кухни?",
  "answer_text": "3000 × 2100 мм",
  "answer_data": {
    "length_mm": 3000,
    "width_mm": 2100,
    "height_mm": null,
    "source": "client"
  }
}
```

### 4. Город (CITY)

**Вопрос:**
```
В каком городе или районе вы находитесь?
```

**Обработка ответа:**
- Если город из списка → сохранить
- Если район → сохранить как `{city: "Алматы", district: "Алатау"}`
- Если неизвестный город → сохранить как есть
- Если «не важно» → пометить как `missing`

**Сохранение:**
```json
{
  "question_key": "city",
  "question_text": "В каком городе или районе вы находитесь?",
  "answer_text": "Алматы, район Алатау",
  "answer_data": {
    "city": "Алматы",
    "district": "Алатау"
  }
}
```

### 5. Фото помещения (PHOTOS)

**Вопрос:**
```
Пришлите, пожалуйста, фото помещения, где будет стоять кухня.

Если есть план или эскиз — тоже пришлите.
```

**Обработка ответа:**
- Если есть изображения → сохранить в `attachments`
- Если есть видео → сохранить, пометить как `video`
- Если нет фото → пометить как `missing`, переход в `STYLE`
- Если фото с размерами → извлечь размеры

**Сохранение:**
```json
{
  "question_key": "photos",
  "question_text": "Пришлите фото помещения",
  "answer_text": "4 фото",
  "answer_data": {
    "count": 4,
    "has_dimensions": false,
    "has_plan": false
  }
}
```

### 6. Стиль (STYLE)

**Вопрос:**
```
Какой стиль кухни вам нравится?

Например:
— Минимализм
— Классика
— Лофт
— Скандинавский
— Современный
```

**Обработка ответа:**
- Если из списка → сохранить
- Если описание → классифицировать
- Если «не знаю» → пометить как `missing`
- Если фото/ссылка → сохранить как `reference`

**Сохранение:**
```json
{
  "question_key": "style",
  "question_text": "Какой стиль кухни вам нравится?",
  "answer_text": "Минимализм",
  "answer_data": {
    "style": "minimalism",
    "confidence": 0.9
  }
}
```

### 7. Фасады (FACADES)

**Вопрос:**
```
Какой материал фасадов вы рассматриваете?

Возможные варианты:
— МДФ крашеный
— Эмаль
— Пластик
— Массив
— Плёнка
— Не знаю
```

**Обработка ответа:**
- Если из списка → сохранить
- Если описание → классифицировать
- Если «не знаю» → пометить как `missing`
- Если фото → сохранить как `reference`

**Сохранение:**
```json
{
  "question_key": "facades",
  "question_text": "Какой материал фасадов вы рассматриваете?",
  "answer_text": "МДФ крашеный",
  "answer_data": {
    "material": "painted_mdf",
    "color": null,
    "confidence": 0.85
  }
}
```

### 8. Техника (APPLIANCES)

**Вопрос:**
```
Нужна ли встроенная техника?

Если да, укажите какая:
— Духовка
— Варочная панель
— Вытяжка
— Посудомоечная машина
— Другое
```

**Обработка ответа:**
- Если «да» + список → сохранить
- Если «нет» → сохранить `built_in: false`
- Если «уже есть» → сохранить `existing: true`
- Если «не знаю» → пометить как `missing`

**Сохранение:**
```json
{
  "question_key": "appliances",
  "question_text": "Нужна ли встроенная техника?",
  "answer_text": "Да, духовка и варочная панель",
  "answer_data": {
    "built_in": true,
    "items": ["духовка", "варочная панель"],
    "existing": false
  }
}
```

### 9. Бюджет (BUDGET)

**Вопрос:**
```
Какой примерный бюджет вы рассматриваете?

Это поможет подобрать подходящие материалы.
```

**Подсказка:**
```
Например:
— До 1 000 000 тенге
— 1 000 000 – 2 000 000 тенге
— 2 000 000 – 3 000 000 тенге
— Свыше 3 000 000 тенге
— Ещё не определился
```

**Обработка ответа:**
- Если число → сохранить
- Если диапазон → сохранить `{min, max}`
- Если «не знаю» → пометить как `missing`
- Если «дешевле» → сохранить `budget: "economy"`

**Сохранение:**
```json
{
  "question_key": "budget",
  "question_text": "Какой примерный бюджет вы рассматриваете?",
  "answer_text": "До 3 000 000 тенге",
  "answer_data": {
    "amount": 3000000,
    "currency": "KZT",
    "type": "max"
  }
}
```

### 10. Сроки (DEADLINE)

**Вопрос:**
```
Когда вы хотите получить готовую кухню?
```

**Обработка ответа:**
- Если дата → сохранить
- Если «срочно» → сохранить `priority: "urgent"`
- Если «не спешу» → сохранить `priority: "flexible"`
- Если описание → классифицировать

**Сохранение:**
```json
{
  "question_key": "deadline",
  "question_text": "Когда вы хотите получить готовую кухню?",
  "answer_text": "В течение двух месяцев",
  "answer_data": {
    "timeframe": "2 months",
    "priority": "normal"
  }
}
```

### 11. Замер (MEASUREMENT)

**Вопрос:**
```
Нужен ли вам выезд замерщика?

Замер нужен для точного расчёта стоимости.
```

**Обработка ответа:**
- Если «да» → сохранить, предложить время
- Если «нет» → сохранить
- Если «может быть» → сохранить `measurement: "undecided"`

**Сохранение:**
```json
{
  "question_key": "measurement",
  "question_text": "Нужен ли вам выезд замерщика?",
  "answer_text": "Да, нужен",
  "answer_data": {
    "needed": true,
    "preferred_time": null
  }
}
```

### 12. Удобное время (CONTACT_TIME)

**Вопрос:**
```
Когда вам удобно, чтобы менеджер связался с вами?
```

**Обработка ответа:**
- Если время → сохранить
- Если «сейчас» → сохранить `immediate: true`
- Если «в любое время» → сохранить `flexible: true`

**Сохранение:**
```json
{
  "question_key": "contact_time",
  "question_text": "Когда вам удобно, чтобы менеджер связался с вами?",
  "answer_text": "Завтра утром после 10:00",
  "answer_data": {
    "time": "tomorrow_morning",
    "specific": "10:00+"
  }
}
```

---

## Проверка готовности

### Обязательные поля

```python
REQUIRED_FIELDS = [
    "kitchen_type",
    "city",
    "dimensions",
    "photos"
]

def check_readiness(answers: dict) -> dict:
    filled = [f for f in REQUIRED_FIELDS if answers.get(f)]
    missing = [f for f in REQUIRED_FIELDS if not answers.get(f)]
    
    return {
        "is_ready": len(missing) == 0,
        "filled_count": len(filled),
        "missing_fields": missing,
        "readiness_percent": len(filled) / len(REQUIRED_FIELDS) * 100
    }
```

### Желательные поля

```python
DESIRED_FIELDS = [
    "style",
    "facades",
    "appliances",
    "budget",
    "deadline",
    "measurement",
    "contact_time"
]
```

---

## Формирование резюме

### Структура резюме

```python
def generate_summary(answers: dict, session: IntakeSession) -> str:
    summary = f"""
Новая заявка №{session.lead.id}

Клиент: {answers.get('name', 'Не указано')}
Город: {answers.get('city', 'Не указано')}
Изделие: {answers.get('kitchen_type', 'Кухня на заказ')}

Параметры:
— Размеры: {format_dimensions(answers.get('dimensions'))}
— Стиль: {answers.get('style', 'Не указан')}
— Фасады: {answers.get('facades', 'Не указан')}
— Техника: {format_appliances(answers.get('appliances'))}

Финансы:
— Бюджет: {answers.get('budget', 'Не указан')}
— Срок: {answers.get('deadline', 'Не указан')}

Данные:
— Фото: {answers.get('photos', {}).get('count', 0)} шт.
— Замер: {'Нужен' if answers.get('measurement', {}).get('needed') else 'Не нужен'}

"""
    
    # Добавить недостающие данные
    missing = get_missing_fields(answers)
    if missing:
        summary += "Не хватает:\n"
        for field in missing:
            summary += f"— {field}\n"
    
    # Добавить рекомендацию
    summary += f"\nРекомендуемый следующий шаг:\n{get_recommendation(answers)}"
    
    return summary
```

### Рекомендации

```python
def get_recommendation(answers: dict) -> str:
    if not answers.get('measurement', {}).get('needed'):
        return "Назначить выезд замерщика"
    
    if not answers.get('budget'):
        return "Уточнить бюджет клиента"
    
    if not answers.get('dimensions', {}).get('height_mm'):
        return "Уточнить высоту потолка"
    
    return "Связаться с клиентом для обсуждения деталей"
```

---

## Передача менеджеру

### Условия передачи

```python
def should_handoff(answers: dict, conversation: Conversation) -> bool:
    # Автоматическая передача
    if check_readiness(answers)['is_ready']:
        return True
    
    # Клиент попросил о человеке
    if conversation.last_message_contains(['человек', 'менеджер', 'оператор']):
        return True
    
    # Прошло 24 часа без ответа
    if conversation.time_since_last_message() > timedelta(hours=24):
        return True
    
    return False
```

### Действия при передаче

```python
def handoff_to_manager(lead: Lead, session: IntakeSession):
    # 1. Обновить статус заявки
    lead.status = "ready_for_manager"
    lead.save()
    
    # 2. Завершить сессию
    session.status = "completed"
    session.completed_at = datetime.now()
    session.summary = generate_summary(session.answers, session)
    session.save()
    
    # 3. Обновить режим диалога
    conversation = lead.conversation
    conversation.mode = "human_mode"
    conversation.save()
    
    # 4. Отправить уведомление менеджеру
    send_telegram_notification(lead, session)
    
    # 5. Отправить сообщение клиенту
    send_client_confirmation(lead)
```

### Уведомление менеджеру

```python
def send_telegram_notification(lead: Lead, session: IntakeSession):
    message = f"""
🆕 Новая заявка №{lead.id}

Клиент: {lead.name}
Город: {lead.city}
Изделие: {session.furniture_type}
Бюджет: {session.answers.get('budget', 'Не указан')}

[Открыть заявку]({get_lead_url(lead.id)})
[Взять в работу]({get_take_over_url(lead.id)})
"""
    
    telegram_bot.send_message(
        chat_id=lead.company.telegram_chat_id,
        text=message,
        parse_mode="Markdown"
    )
```

---

## Обработка ошибок

### Клиент не отвечает

```python
def handle_no_response(lead: Lead, conversation: Conversation):
    time_since = conversation.time_since_last_message()
    
    if time_since > timedelta(hours=24):
        # Напоминание
        send_reminder(lead)
    
    if time_since > timedelta(days=7):
        # Автоматическое закрытие
        lead.status = "lost"
        lead.save()
```

### Клиент пишет не по теме

```python
def handle_off_topic(message: str, conversation: Conversation):
    # Попробовать извлечь данные
    extracted = extract_data_from_text(message)
    
    if extracted:
        # Сохранить извлечённые данные
        save_extracted_data(extracted, conversation)
        return True
    
    # Вернуть к теме
    send_back_to_topic(conversation)
    return False
```

### Клиент спрашивает точную цену

```python
def handle_price_question(conversation: Conversation):
    response = """
Стоимость зависит от:
— Размеров кухни
— Материалов фасадов
— Комплектации техникой

Чтобы рассчитать, мне нужно узнать:
1. Размеры
2. Материал фасадов
3. Нужна ли техника

Начнём с размеров?
"""
    
    send_message(conversation, response)
```

### AI не может обработать запрос

```python
def handle_ai_error(conversation: Conversation, error: str):
    response = """
Извините, я не совсем понял ваш вопрос.

Пожалуйста, опишите:
— Какой формы кухня
— Какие размеры
— Где будет стоять

Или напишите «Хочу поговорить с менеджером».
"""
    
    send_message(conversation, response)
```

---

## Приоритет вопросов

### Если мало времени

Задавать только обязательные:
1. Тип кухни
2. Город
3. Размеры
4. Фото

### Если клиент активен

Задавать все вопросы по порядку.

### Если клиент торопится

Сократить до:
1. Тип кухни
2. Город
3. Размеры
4. Бюджет

---

## Лимиты

| Параметр | Лимит |
|----------|-------|
| Максимум вопросов за раз | 3 |
| Время ожидания ответа | 24 часа |
| Максимум напоминаний | 2 |
| Максимум фото | 20 |
| Максимум текста сообщения | 1000 символов |
