# Обработка ошибок и нестандартных ситуаций

## Назначение

Этот документ описывает, как AI-приёмщик должен обрабатывать ошибки, нестандартные ответы и сложные ситуации.

---

## Категории ошибок

### 1. Ошибки ввода данных

#### Непонятный ответ

**Пример:** Клиент пишет «аааа» или набор символов

**Действие:**
```
Извините, я не совсем понял.

Пожалуйста, укажите:
— Какой формы кухня
— Или напишите «Хочу поговорить с менеджером»
```

**Логика:**
```python
def handle_unclear_response(message: str) -> str:
    if is_gibberish(message):
        return "Извините, я не совсем понял. Пожалуйста, опишите вашу кухню."
    
    if len(message) < 3:
        return "Пожалуйста, напишите подробнее."
    
    return None
```

#### Ошибки парсинга размеров

**Пример:** Клиент пишет «метра три»

**Действие:**
```python
def parse_dimensions(text: str) -> dict:
    # Попробовать извлечь числа
    numbers = re.findall(r'\d+', text)
    
    if len(numbers) >= 2:
        return {
            "length_mm": int(numbers[0]) * 1000 if int(numbers[0]) < 100 else int(numbers[0]),
            "width_mm": int(numbers[1]) * 1000 if int(numbers[1]) < 100 else int(numbers[1])
        }
    
    if len(numbers) == 1:
        # Одно число — возможно, длина
        return {
            "length_mm": int(numbers[0]) * 1000 if int(numbers[0]) < 100 else int(numbers[0]),
            "width_mm": None,
            "needs_clarification": True
        }
    
    # Нет чисел — попробовать текстовый парсинг
    return parse_text_dimensions(text)
```

**Если не удаётся распарсить:**
```
Я попробовал определить размеры, но не уверен.

Подскажите точно:
— Длина стены в миллиметрах (например, 3000)
— Ширина стены в миллиметрах (например, 2100)
```

#### Неверный формат телефона

**Пример:** Клиент пишет «987654321» без кода страны

**Действие:**
```python
def validate_phone(phone: str) -> str:
    # Убрать пробелы и дефисы
    phone = re.sub(r'[\s\-]', '', phone)
    
    # Если начинается с 8 или 7 — добавить +7
    if phone.startswith(('8', '7')):
        return f"+7{phone[1:]}"
    
    # Если начинается с + — оставить как есть
    if phone.startswith('+'):
        return phone
    
    # Иначе — попросить уточнить
    return None
```

**Если неверный формат:**
```
Пожалуйста, укажите номер телефона в формате:
+7 (XXX) XXX-XX-XX
```

---

### 2. Ситуационные ошибки

#### Клиент прислал фото без текста

**Действие:**
```python
def handle_photo_without_text(message: Message):
    # Анализировать фото
    analysis = analyze_image(message.image_url)
    
    if analysis.has_dimensions:
        # Извлечь размеры
        save_dimensions(analysis.dimensions)
        return f"Я определил размеры по фото: {format_dimensions(analysis.dimensions)}"
    
    if analysis.is_room_photo:
        return "Отличное фото! Подскажите, какой формы кухня вам нужна?"
    
    return "Спасибо за фото! Расскажите подробнее о вашей кухне."
```

#### Клиент прислал несколько фото сразу

**Действие:**
```python
def handle_multiple_photos(messages: list):
    photos = [m for m in messages if m.type == "image"]
    
    # Сохранить все фото
    for photo in photos:
        save_attachment(photo)
    
    # Проанализировать
    analysis = analyze_images([p.image_url for p in photos])
    
    return f"""
Спасибо за {len(photos)} фото!

Я вижу:
— Помещение {analysis.room_type}
— Примерные размеры: {analysis.estimated_dimensions}

Какой формы кухня вам нужна?
"""
```

#### Клиент прислал видео

**Действие:**
```python
def handle_video(message: Message):
    # Сохранить видео
    save_attachment(message.video_url)
    
    return """
Спасибо за видео! Я его сохранил.

Расскажите, какой формы кухня вам нужна:
1. Прямая
2. Угловая
3. П-образная
4. С островом
"""
```

#### Клиент прислал ссылку на фото

**Пример:** «Вот фото: https://instagram.com/p/xxx»

**Действие:**
```python
def handle_photo_link(message: Message):
    url = extract_url(message.text)
    
    if is_instagram_url(url):
        # Попробовать скачать
        try:
            photo = download_instagram_photo(url)
            save_attachment(photo)
            return "Фото сохранено! Какой формы кухня вам нужна?"
        except:
            return "Я не могу скачать фото по ссылке. Пожалуйста, пришлите его напрямую."
    
    return "Пожалуйста, пришлите фото напрямую, а не по ссылке."
```

---

### 3. Нестандартные ответы

#### Клиент пишет длинное сообщение

**Пример:** Описание всей ситуации в одном сообщении

**Действие:**
```python
def handle_long_message(message: str) -> str:
    # Извлечь ключевые данные
    data = extract_data_from_text(message)
    
    # Сохранить извлечённое
    save_extracted_data(data)
    
    # Определить, чего не хватает
    missing = get_missing_fields(data)
    
    if missing:
        return f"""
Спасибо за подробное описание!

Я записал:
{format_extracted_data(data)}

Для полной заявки мне还需要:
{format_missing_fields(missing)}

Можете уточнить это?
"""
    
    return "Отлично! У меня есть все данные. Передаю заявку менеджеру."
```

#### Клиент отвечает на прошлый вопрос

**Пример:** AI спросил размеры, клиент отвечает через 3 сообщения

**Действие:**
```python
def handle_delayed_answer(message: str, conversation: Conversation):
    # Определить, на какой вопрос ответ
    last_question = conversation.get_last_question()
    
    if last_question and is_answer_to(message, last_question):
        # Сохранить ответ
        save_answer(last_question.key, message)
        return proceed_to_next_question(conversation)
    
    # Не удалось определить — уточнить
    return f"Уточните, пожалуйста: {last_question.text}"
```

#### Клиент меняет тему

**Пример:** Говорили о кухне, клиент突然 спрашивает о шкафах

**Действие:**
```python
def handle_topic_change(message: str, conversation: Conversation):
    intent = classify_intent(message)
    
    if intent == "other_furniture":
        return """
Я занимаюсь только кухнями.

Если вам нужен шкаф или другая мебель, напишите «Хочу поговорить с менеджером».

Продолжим с кухней? Какой формы она будет?
"""
    
    if intent == "general_question":
        return "Давайте сначала закончим с кухней. Какой формы она будет?"
    
    return None
```

#### Клиент спорит или жалуется

**Пример:** «Это глупо, я сам могу замерить»

**Действие:**
```python
def handle_complaint(message: str, conversation: Conversation):
    # Определить тип жалобы
    complaint_type = classify_complaint(message)
    
    if complaint_type == "resistance_to_ai":
        return """
Понимаю! Если хотите, могу передать вашу заявку менеджеру.

Или продолжим вместе — я задам несколько вопросов, и менеджер уже будет готов помочь.

Что предпочитаете?
"""
    
    if complaint_type == "pricing_concern":
        return """
Стоимость действительно зависит от многих факторов.

Чтобы дать точный расчёт, мне нужно узнать:
1. Размеры
2. Материалы
3. Комплектацию

Начнём с размеров?
"""
    
    # Общая жалоба — передать менеджеру
    return "Понимаю вас. Передаю вашу заявку менеджеру, он свяжется с вами."
```

#### Клиент пишет «Хватит» или «Отстаньте»

**Действие:**
```python
def handle_stop_request(message: str, conversation: Conversation):
    return """
Хорошо, больше не буду беспокоить.

Если захотите вернуться — напишите в любой момент.

Удачи с выбором кухни!
"""
    
    # Закрыть диалог
    conversation.status = "closed"
    conversation.save()
```

---

### 4. Технические ошибки

#### Ошибка API

**Действие:**
```python
def handle_api_error(error: Exception):
    # Логировать ошибку
    log_error(error)
    
    # Отправить клиенту общее сообщение
    return "Извините, произошла短暂ная ошибка. Пожалуйста, попробуйте ещё раз."
    
    # Уведомить администратора
    notify_admin(f"API error: {error}")
```

#### Ошибка сохранения данных

**Действие:**
```python
def handle_save_error(error: Exception):
    # Попробовать снова
    try:
        retry_save()
    except:
        # Если не удаётся — сохранить локально
        save_locally(data)
        
        # Уведомить
        return "Данные сохранены временно. Мы обязательно вернёмся к вашей заявке."
```

#### Ошибка анализа фото

**Действие:**
```python
def handle_image_analysis_error(error: Exception):
    return """
Я не смог проанализировать фото.

Пожалуйста, опишите помещение словами:
— Какой формы комната
— Где будет стоять кухня
— Есть ли окна или двери рядом
"""
```

---

### 5. Спам и нецелевые обращения

#### Спам

**Признаки:**
- Ссылки на другие сайты
- Реклама товаров
- Одинаковые сообщения разным компаниям

**Действие:**
```python
def handle_spam(message: Message):
    # Пометить как спам
    mark_as_spam(message)
    
    # Не отвечать
    return None
    
    # Уведомить администратора
    notify_admin(f"Spam detected: {message.id}")
```

#### Конкурент

**Признаки:**
- Предлагает свои услуги
- Спрашивает о технологиях
- Пытается получить информацию

**Действие:**
```python
def handle_competitor(message: Message):
    return "Спасибо за интерес! Мы专注于 производству кухонь. Чем могу помочь?"
    
    # Не раскрывать информацию о компании
    # Не отвечать на вопросы о технологиях
```

#### Ошибочный номер

**Действие:**
```python
def handle_wrong_number(message: Message):
    return "Похоже, вы ошиблись номером. Здесь AI-приёмщик мебельной компании. Чем могу помочь?"
```

---

### 6. Языковые барьеры

#### Клиент пишет на другом языке

**Действие:**
```python
def handle_foreign_language(message: Message):
    detected_lang = detect_language(message.text)
    
    if detected_lang == "kz":
        return "Извините, я пока говорю только на русском. Могу передать вашу заявку менеджеру."
    
    if detected_lang == "en":
        return "Sorry, I only speak Russian. Would you like me to connect you with a manager?"
    
    return "Извините, я понимаю только русский язык. Могу передать вашу заявку менеджеру."
```

#### Смешанный язык

**Пример:** «Привет, I want kitchen»

**Действие:**
```python
def handle_mixed_language(message: Message):
    # Попробовать извлечь данные
    data = extract_data_from_text(message.text)
    
    if data:
        save_extracted_data(data)
        return "Отлично! Я понял. Какой формы кухня?"
    
    return "Пожалуйста, пишите на русском. Какой формы кухня вам нужна?"
```

---

## Логирование ошибок

### Что логировать

```python
def log_error(error: Exception, context: dict):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_type": type(error).__name__,
        "message": str(error),
        "conversation_id": context.get("conversation_id"),
        "lead_id": context.get("lead_id"),
        "user_message": context.get("user_message"),
        "stack_trace": traceback.format_exc()
    }
    
    # Сохранить в лог
    save_to_log(log_entry)
    
    # Уведомить если критично
    if is_critical(error):
        notify_admin(log_entry)
```

### Что НЕ логировать

- Текст сообщений клиентов (кроме ошибок)
- Номера телефонов
- API-ключи
- Пароли

---

## Восстановление после ошибок

### Автоматическое восстановление

```python
def auto_recover(conversation: Conversation):
    # Проверить последнее сообщение
    last_msg = conversation.get_last_message()
    
    if last_msg and last_msg.failed:
        # Попробовать отправить снова
        try:
            resend_message(last_msg)
        except:
            # Если не удаётся — уведомить менеджера
            notify_manager_about_failure(conversation)
```

### Ручное восстановление

Менеджер может:
1. Посмотреть историю диалога
2. Отправить сообщение вручную
3. Обновить заявку вручную

---

## Мониторинг ошибок

### Метрики

| Метрика | Описание | Порог |
|---------|----------|-------|
| Error rate | Процент ошибок | < 5% |
| API failures | Ошибки API | < 1% |
| Parse errors | Ошибки парсинга | < 10% |
| Image analysis failures | Ошибки анализа фото | < 15% |

### Алерты

```python
def check_error_rate():
    rate = get_error_rate_last_hour()
    
    if rate > 0.1:  # 10%
        send_alert(f"High error rate: {rate:.1%}")
    
    if rate > 0.25:  # 25%
        send_critical_alert(f"Critical error rate: {rate:.1%}")
        disable_ai_mode()
```
