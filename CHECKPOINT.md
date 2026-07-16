# CHECKPOINT.md — Текущее состояние проекта

## Текущий этап

**Этап 5: Telegram-бот для менеджеров**

Статус: ✅ Завершён

## Что реально работает

- Структура каталогов создана
- Все управляющие документы созданы
- Продуктовая гипотеза зафиксирована
- Технологический стек определён
- Сценарии диалогов описаны
- AI-логика для кухни определена
- Сценарий передачи менеджеру описан
- Обработка ошибок описана
- Визуальный прототип создан:
  - Главный экран (dashboard.html)
  - Карточка заявки (claim-card.html)
  - История диалога (dialogue-history.html)
  - Кнопки управления (buttons.html)
- Выбран Supabase для хранения данных
- Backend-каркас создан:
  - FastAPI-приложение (app/main.py)
  - Supabase-клиент (app/core/supabase.py)
  - Pydantic-модели (app/models/schemas.py)
  - API-эндпоинты для Leads (app/api/leads.py)
  - API-эндпоинты для Conversations (app/api/conversations.py)
  - Webhook для WhatsApp (app/api/webhook.py)
  - Простой веб-кабинет (app/static/index.html)
- AI-логика для кухни создана:
  - AI-сервис (app/services/ai.py)
  - Распознавание намерений (app/services/intent.py)
  - Извлечение фактов (app/services/extract.py)
  - Менеджер вопросов (app/services/questions.py)
  - Генератор резюме (app/services/summary.py)
  - Основной сервис сбора данных (app/services/intake.py)
- Telegram-бот создан:
  - Telegram-сервис (app/services/telegram.py)
  - Вебхук для кнопок (app/api/telegram.py)
  - Интеграция с intake-сервисом

## Что является mock

- Нет .env файла с ключами Supabase, OpenAI, Telegram
- Нет тестов
- Нет реальных интеграций с внешними сервисами

## Что ещё не подключено

- Supabase (нужен .env файл)
- OpenAI API (нужен .env файл)
- Telegram Bot (нужен .env файл)
- WhatsApp Business Platform
- Docker Compose

## Внешние сервисы

| Сервис | Статус | Назначение |
|--------|--------|------------|
| Supabase | Не подключён | Хранение данных, файлов, авторизация |
| WhatsApp Business Platform | Не подключён | Приём сообщений от клиентов |
| OpenAI API | Не подключён | AI-обработка диалогов |
| Telegram Bot | Не подключён | Уведомления менеджеров |
| Docker Compose | Не подключён | Деплой

## Как запустить проект

```bash
# Клонировать репозиторий
git clone https://github.com/username/furniture-intake-agent.git
cd furniture-intake-agent

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Заполнить SUPABASE_URL и SUPABASE_KEY

# Запустить приложение
uvicorn app.main:app --reload
```

Открыть http://localhost:8000 в браузере.

## Текущий этап

**Этап 5 → Этап 6**

Переход к WhatsApp sandbox.

## Главный блокер

Отсутствие WhatsApp-интеграции.

Нельзя принимать реальные заявки без:
- WhatsApp Business Platform
- Webhook для приёма сообщений
- Отправки ответов клиенту

## Дата последнего обновления

2026-07-15

## Автор последнего изменения

Coding-агент (автоматически)
