# DATA_MODEL.md — Модель данных

## Обзор сущностей

```
Company → User → Channel → Lead → Conversation → Message → Attachment
                                    ↓
                              IntakeSession → IntakeAnswer
                                    ↓
                                  Task → Activity
```

## Среда хранения: Supabase

**Supabase** — managed PostgreSQL сервис с доп. функциями.

**Преимущества для проекта:**
- Хранилище файлов (фото кухонь) — Supabase Storage
- Авторизация — Supabase Auth
- Real-time подписки — обновления статусов
- Dashboard для администрирования
- PostgreSQL совместимость

**Клиент:** `supabase-py`

**Структура проекта:**
```
app/
├── core/
│   └── supabase.py      # Инициализация клиента
├── models/
│   └── database.py      # Модели данных (Pydantic)
└── services/
    └── storage.py       # Работа с Supabase Storage
```

## Сущности

### Company

Мебельная компания, использующая сервис.

```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    city VARCHAR(100),
    website VARCHAR(255),
    whatsapp_number VARCHAR(50),
    telegram_chat_id VARCHAR(100),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### User

Пользователь системы (менеджер, владелец).

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'manager',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Channel

Канал привлечения клиентов.

```sql
CREATE TABLE channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- whatsapp, instagram, website, referral
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Lead

Потенциальный клиент.

```sql
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id),
    channel_id UUID REFERENCES channels(id),
    phone VARCHAR(50),
    name VARCHAR(255),
    city VARCHAR(100),
    source VARCHAR(100),
    status VARCHAR(50) DEFAULT 'new',
    -- Статусы: new, ai_collecting, waiting_for_client, ready_for_manager,
    --         manager_review, measurement_scheduled, quote_preparation,
    --         quote_sent, won, lost
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Conversation

Диалог с клиентом.

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    channel_id UUID REFERENCES channels(id),
    mode VARCHAR(50) DEFAULT 'ai_mode',
    -- Режимы: ai_mode, human_mode
    status VARCHAR(50) DEFAULT 'active',
    started_at TIMESTAMP DEFAULT NOW(),
    last_message_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);
```

### Message

Сообщение в диалоге.

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    sender_type VARCHAR(50) NOT NULL, -- client, ai, manager
    content TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text',
    -- Типы: text, image, document, audio
    external_id VARCHAR(255), -- ID в WhatsApp/Telegram
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Attachment

Вложение к сообщению.

```sql
CREATE TABLE attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(id),
    file_type VARCHAR(50) NOT NULL, -- image, document
    file_url VARCHAR(500) NOT NULL,
    file_name VARCHAR(255),
    file_size INTEGER,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### IntakeSession

Сессия сбора данных от клиента.

```sql
CREATE TABLE intake_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    conversation_id UUID REFERENCES conversations(id),
    furniture_type VARCHAR(50) NOT NULL, -- kitchen, wardrobe, etc.
    status VARCHAR(50) DEFAULT 'in_progress',
    -- Статусы: in_progress, completed, abandoned
    summary TEXT, -- AI-резюме заявки
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### IntakeAnswer

Ответ клиента на вопрос AI.

```sql
CREATE TABLE intake_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES intake_sessions(id),
    question_key VARCHAR(100) NOT NULL, -- name, city, kitchen_type, etc.
    question_text TEXT NOT NULL,
    answer_text TEXT,
    answer_data JSONB, -- Структурированные данные (размеры, бюджет)
    is_confirmed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Task

Задача для менеджера.

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    assigned_to UUID REFERENCES users(id),
    type VARCHAR(50) NOT NULL, -- call, measurement, follow_up
    status VARCHAR(50) DEFAULT 'pending',
    -- Статусы: pending, in_progress, completed, cancelled
    priority VARCHAR(20) DEFAULT 'normal',
    due_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Activity

Активность по заявке.

```sql
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    user_id UUID REFERENCES users(id),
    type VARCHAR(50) NOT NULL, -- status_change, note, task_created
    description TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Связи

```
Company 1 ──── * User
Company 1 ──── * Channel
Company 1 ──── * Lead
Channel  1 ──── * Lead
Lead     1 ──── * Conversation
Lead     1 ──── * IntakeSession
Lead     1 ──── * Task
Lead     1 ──── * Activity
Conversation 1 ──── * Message
Message  1 ──── * Attachment
IntakeSession 1 ──── * IntakeAnswer
User     1 ──── * Task
User     1 ──── * Activity
```

## Статусы заявки (Lead)

```
new                 → Новая заявка
ai_collecting       → AI собирает данные
waiting_for_client  → Ожидание ответа клиента
ready_for_manager   → Готова для менеджера
manager_review      → Менеджер.review
measurement_scheduled → Замер назначен
quote_preparation   → Подготовка расчёта
quote_sent          → Расчёт отправлен
won                 → Заказ выигран
lost                → Заказ потерян
```

## Жизненный цикл заявки

```
Новое сообщение клиента
    ↓
Создание Lead (status: new)
    ↓
Создание Conversation
    ↓
Создание IntakeSession (status: in_progress)
    ↓
AI задаёт вопросы, создаёт IntakeAnswer
    ↓
Клиент отвечает, обновляется IntakeAnswer
    ↓
Все обязательные поля заполнены
    ↓
IntakeSession (status: completed)
    ↓
Lead (status: ready_for_manager)
    ↓
Уведомление менеджеру через Telegram
    ↓
Менеджер нажимает «Взять в работу»
    ↓
Lead (status: manager_review)
    ↓
Conversation (mode: human_mode)
    ↓
Создание Task (type: call/measurement)
    ↓
Менеджер выполняет задачу
    ↓
Lead (status: won/lost)
```

## Обязательные поля для кухни

| Ключ | Описание | Тип | Обязательно |
|------|----------|-----|-------------|
| name | Имя клиента | string | Да |
| city | Город | string | Да |
| kitchen_type | Тип кухни | enum | Да |
| dimensions | Размеры | object | Да |
| photos | Фото помещения | array | Да |
| style | Стиль | string | Нет |
| facades | Материал фасадов | string | Нет |
| countertop | Столешница | string | Нет |
| appliances | Техника | boolean | Нет |
| budget | Бюджет | object | Нет |
| deadline | Срок | string | Нет |
| measurement | Нужен замер | boolean | Да |
| contact_time | Удобное время | string | Нет |

## Индексы

```sql
-- Быстрый поиск по компаниям
CREATE INDEX idx_leads_company_id ON leads(company_id);
CREATE INDEX idx_conversations_lead_id ON conversations(lead_id);

-- Поиск по статусам
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_tasks_status ON tasks(status);

-- Поиск по датам
CREATE INDEX idx_leads_created_at ON leads(created_at);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```
