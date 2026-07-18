# AGENTS.md — Конституция проекта furniture-intake-agent

## Роль coding-агента

Coding-агент отвечает за:
- Написание и поддержку кода приложения
- Создание и обновление управляющих документов
- Соблюдение архитектурных решений
- Написание тестов
- Обновление документации после изменений
- Закрепление работы в GitHub после каждого этапа

## Обязательные документы перед работой

Перед изменением кода агент обязан прочитать:
- `AGENTS.md` (этот файл)
- `PRODUCT.md`
- `DESIGN.md`
- `SESSION_NOTES.md`
- `CHECKPOINT.md`
- `PROJECT_PROGRESS.md`

Для задач, связанных с архитектурой или данными:
- `DECISIONS.md`
- `DATA_MODEL.md`
- `SECURITY.md`

## Ритуал начала сессии

После чтения документов агент должен кратко написать:

1. **Как он понимает задачу** — что именно нужно сделать
2. **Какой продукт сейчас строится** — текущее состояние
3. **Что не входит в текущий этап** — границы
4. **Какие файлы будут затронуты** — список файлов
5. **Какой минимальный результат** — критерий успеха
6. **Какие проверки будут выполнены** — тесты, визуальная проверка

Только после этого начинается изменение кода.

## Принцип работы

```
shape → craft → polish
```

### Shape
- Определить пользовательский сценарий
- Определить границы, состояния, данные
- Определить критерии готовности
- Никакого кода до понимания структуры

### Craft
- Реализовать минимально необходимое
- Маленькими изменениями
- Без переписывания всего проекта
- Без ненужных зависимостей
- С тестами критической логики

### Polish
- Исправить интерфейс
- Улучшить тексты
- Проверить мобильную версию
- Проверить пустые состояния
- Убрать визуальный шум

## Правила изменения кода

### Запрещено
- Добавлять функции за пределами MVP
- Создавать полноценную CRM
- Подключать WhatsApp API до Этапа 6
- Добавлять Redis, Celery, Kubernetes
- Добавлять точный расчёт стоимости
- Создавать 3D-конструктор
- Использовать библиотеки, не одобренные в DECISIONS.md
- Удалять существующие тесты без обоснования
- Изменять структуру БД без обновления DATA_MODEL.md

### Разрешено
- Добавлять новый код в рамках текущего этапа
- Рефакторинг существующего кода
- Обновление зависимостей (с обоснованием)
- Добавление тестов
- Обновление документации

## Правила тестов

- Критическая логика должна иметь тесты
- Тесты запускаются перед коммитом
- Покрытие тестами: минимум 80% для бизнес-логики
- Интеграционные тесты для API-эндпоинтов

## Правила миграций

- Каждое изменение структуры БД — отдельная миграция
- Миграции должны быть обратимыми
- Описание миграции должно содержать: что меняется, почему, как откатить
- Перед применением миграции: проверить на тестовых данных

## Правила коммитов

- Формат: `type(scope): description`
- Типы: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Один коммит = одна логическая единица работы
- Не коммитить секреты, ключи, пароли
- Не коммитить сгенерированные файлы

## Правила GitHub

### Обязательные действия

1. **Создать репозиторий** — если ещё не существует
2. **Добавить remote** — `git remote add origin <URL>`
3. **Запушить после каждого этапа** — `git push origin main`
4. **Не коммитить секреты** — использовать `.env` и `.gitignore`

### Формат коммита

```
type(scope): description

[опционально: тело коммита]

[опционально: footer]
```

### Примеры

```bash
# Этап 0
git commit -m "feat: initial project setup with management documents"

# Этап 1
git commit -m "feat: complete Etapa 1 - research and conversation scenario"

# Этап 2
git commit -m "feat: create visual prototype for manager dashboard"

# Исправление
git commit -m "fix(api): handle webhook verification error"

# Документация
git commit -m "docs: update README with setup instructions"
```

### Порядок действий после этапа

1. Закоммитить все изменения
2. Проверить `git status`
3. Проверить `git log --oneline -5`
4. Запушить: `git push origin main`
5. Убедиться, что коммиты видны в GitHub

## Ритуал завершения сессии

После изменений агент обязан:

1. Запустить тесты
2. Проверить основной пользовательский сценарий
3. Зафиксировать изменённые файлы
4. Обновить `SESSION_NOTES.md`
5. Обновить `CHECKPOINT.md`, если изменилось фактическое состояние
6. Обновить `PROJECT_PROGRESS.md`
7. Обновить `docs/progress-dashboard.html`
8. Добавить скриншот интерфейса в `docs/screens/`, если изменялся UI
9. Записать архитектурное решение в `DECISIONS.md`, если оно было принято
10. Указать один следующий рекомендуемый шаг
11. Закоммитить все изменения
12. Запушить в GitHub

## Правило одной сессии

Одна сессия — одна логическая задача.

Не объединять в одной сессии:
- WhatsApp-интеграцию
- Полный redesign
- Billing
- Production deployment
- Новую AI-логику

## Структура проекта

```
furniture-intake-agent/
├── app/                    # Основное приложение
│   ├── api/               # API-эндпоинты
│   ├── core/              # Ядро приложения
│   ├── models/            # Модели данных
│   ├── services/          # Бизнес-логика
│   └── templates/         # Шаблоны
├── tests/                 # Тесты
├── docs/                  # Документация
│   ├── interviews/        # Интервью с компаниями
│   ├── pilots/           # Пилотные проекты
│   ├── screens/          # Скриншоты интерфейса
│   └── flows/            # Диаграммы процессов
├── scripts/              # Утилиты и скрипты
├── PRODUCT.md
├── DESIGN.md
├── AGENTS.md
├── SESSION_NOTES.md
├── CHECKPOINT.md
├── PROJECT_PROGRESS.md
├── DECISIONS.md
├── DATA_MODEL.md
├── SECURITY.md
└── README.md
```

## Технологический стек

- Backend: FastAPI
- Database: PostgreSQL
- AI: OpenAI API
- Messaging: WhatsApp Business Platform / Cloud API
- Manager notifications: Telegram Bot
- Deployment: Docker Compose

## Критические замечания

- Не начинать писать код до понимания сценария
- Не добавлять зависимости без обоснования
- Не пропускать обновление документов
- Не коммитить без проверки тестов
- Не нарушать границы MVP
## Shared unfinished-project deployment ritual

This repository is still under active development. Before every substantial change, read this file and the project README/session notes, check `git status`, preserve unrelated changes, and identify the exact build and deployment target.

Before claiming completion: run the project lint/typecheck/tests and a production build; commit and push the exact tested state; deploy only from a clean checkout; smoke-test the real public URL and the main user journey on desktop and mobile. A screenshot or local preview alone is not proof of a successful deployment.

For Cloudflare/OpenNext projects: prefer the adapter-supported production builder; if `Failed to load chunk server/chunks/ssr/...` occurs, check current OpenNext troubleshooting and use a Webpack build when recommended. Avoid deploying from OneDrive or paths with Cyrillic/spaces when artifacts behave inconsistently; use a clean ASCII-only clone under `C:\tmp`. After DNS/custom-domain creation, distinguish stale local `NXDOMAIN` cache from a server failure by checking a public resolver, direct HTTPS status, Worker logs, and then a fresh browser process.

Never weaken database authorization to make missing data appear. For OAuth migrations, verify user IDs, organization membership, ownership fields, RLS, storage access, and record counts. Never print or commit secrets.