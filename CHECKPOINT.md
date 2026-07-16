# CHECKPOINT.md — Текущее состояние проекта

## Текущий этап

**Этап 3: Backend-каркас**

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

## Что является mock

- Нет .env файла с ключами Supabase
- Нет тестов
- Нет AI-логики
- Нет интеграций

## Что ещё не подключено

- Supabase (нужен .env файл)
- WhatsApp Business Platform
- OpenAI API
- Telegram Bot
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

**Этап 3 → Этап 4**

Переход к AI-логике для кухни.

## Главный блокер

Отсутствие AI-логики.

Нельзя обрабатывать сообщения клиентов без:
- Распознавания намерений
- Извлечения фактов
- Формирования резюме заявки

## Дата последнего обновления

2026-07-15

## Автор последнего изменения

Coding-агент (автоматически)
