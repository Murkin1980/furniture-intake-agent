# Furniture Intake Agent

AI-приёмная для мебельных компаний. Принимает заявки через WhatsApp, собирает данные о кухне через AI, создаёт структурированные карточки и передаёт менеджеру.

## Как это работает

```
Клиент пишет в WhatsApp
    ↓
AI задаёт вопросы (имя, город, тип кухни, размеры, стиль...)
    ↓
AI формирует резюме заявки
    ↓
Менеджер получает уведомление в Telegram
    ↓
Менеджер берёт заявку в работу
```

## Возможности

- Приём сообщений через WhatsApp
- AI-диалог для сбора данных о кухне
- Автоматическое формирование резюме заявки
- Уведомления менеджеров через Telegram
- Веб-кабинет для просмотра заявок

## Технологии

- **Backend:** FastAPI
- **База данных:** Supabase (PostgreSQL)
- **AI:** OpenAI API
- **Мессенджеры:** WhatsApp Business Platform, Telegram Bot
- **Деплой:** Docker Compose

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Murkin1980/furniture-intake-agent.git
cd furniture-intake-agent
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения

```bash
cp .env.example .env
```

Заполните `.env`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 4. Запустить приложение

```bash
uvicorn app.main:app --reload
```

Откройте http://localhost:8000

## Структура проекта

```
furniture-intake-agent/
├── app/
│   ├── api/              # API-эндпоинты
│   │   ├── leads.py      # CRUD для заявок
│   │   ├── conversations.py  # CRUD для диалогов
│   │   └── webhook.py    # WhatsApp webhook
│   ├── core/
│   │   ├── config.py     # Конфигурация
│   │   └── supabase.py   # Клиент Supabase
│   ├── models/
│   │   └── schemas.py    # Pydantic-модели
│   ├── services/
│   │   ├── ai.py         # AI-сервис (OpenAI)
│   │   ├── intent.py     # Распознавание намерений
│   │   ├── extract.py    # Извлечение фактов
│   │   ├── questions.py  # Менеджер вопросов
│   │   ├── summary.py    # Генератор резюме
│   │   └── intake.py     # Основной сервис сбора
│   ├── static/
│   │   └── index.html    # Веб-кабинет
│   └── main.py           # FastAPI-приложение
├── docs/
│   ├── flows/            # Диаграммы процессов
│   ├── interviews/       # Исследования
│   └── screens/          # Визуальные прототипы
├── tests/                # Тесты
├── scripts/              # Утилиты
├── requirements.txt      # Зависимости
└── README.md
```

## API

### Leads

- `GET /api/leads/?company_id={id}` — список заявок
- `GET /api/leads/{id}` — детали заявки
- `POST /api/leads/` — создать заявку
- `PATCH /api/leads/{id}` — обновить заявку

### Conversations

- `GET /api/conversations/{id}` — детали диалога
- `POST /api/conversations/` — создать диалог
- `GET /api/conversations/{id}/messages` — список сообщений
- `POST /api/conversations/{id}/messages` — отправить сообщение

### Webhook

- `POST /webhook/whatsapp` — WhatsApp webhook

## Статусы заявки

```
new → ai_collecting → waiting_for_client → ready_for_manager
    → manager_review → measurement_scheduled → quote_preparation
    → quote_sent → won/lost
```

## Этапы разработки

- [x] Этап 0: Репозиторий и документы
- [x] Этап 1: Исследования и сценарии
- [x] Этап 2: Визуальный прототип
- [x] Этап 3: Backend-каркас
- [x] Этап 4: AI-логика для кухни
- [ ] Этап 5: Telegram-бот
- [ ] Этап 6: WhatsApp sandbox
- [ ] Этап 7: Первый пилот

## Лицензия

MIT
