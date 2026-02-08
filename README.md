# GitHub Tech Stack Analyzer

Сервис для генерации SVG-картинок с технологическим стеком пользователя GitHub.

## Стек технологий

- Python 3.11+
- FastAPI
- httpx (async HTTP клиент)
- Jinja2 (шаблоны SVG)
- Vercel (хостинг)

## Структура проекта

```
github-framework-stats/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI + эндпоинты
│   ├── github_client.py        # GitHub API клиент
│   ├── cache.py                # In-memory кэш (TTL 1 час)
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── base.py             # Базовый интерфейс
│   │   ├── languages.py        # GitHub API → языки программирования
│   │   ├── flutter.py          # pubspec.yaml → Flutter + Dart packages
│   │   ├── javascript.py       # package.json → React/Next/Vue/Angular + 30 технологий
│   │   ├── python_fw.py        # requirements.txt → Django/FastAPI/Flask + 20 технологий
│   │   ├── rust.py             # Cargo.toml → Actix/Rocket
│   │   ├── go.py               # go.mod → Gin/Fiber
│   │   └── devops.py           # Dockerfile/GitHub Actions/K8s
│   └── svg/
│       ├── __init__.py
│       ├── generator.py        # Генератор SVG (адаптивная ширина)
│       ├── themes.py           # 19 тем оформления
│       ├── styles.py           # Стили: card/badges/grid/pie
│       └── icons.py            # Devicon CDN маппинг (100+ иконок)
├── templates/
│   ├── card.svg.jinja2
│   ├── badges.svg.jinja2
│   ├── grid.svg.jinja2
│   └── pie.svg.jinja2
├── api/
│   └── index.py                # Entry point для Vercel
├── requirements.txt
├── vercel.json
└── README.md
```

## Установка и запуск

### Локальный запуск

```bash
cd C:\Users\seydi\github-framework-stats

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### С GitHub токеном (для реальных данных)

```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
python -m uvicorn app.main:app --reload
```

Токен можно создать: https://github.com/settings/tokens (Classic, без специальных scopes)

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Документация |
| GET | `/demo/techstack.svg` | Демо с mock-данными |
| GET | `/{username}/techstack.svg` | Полный стек пользователя |
| GET | `/{username}/frameworks.svg` | Только фреймворки |
| GET | `/repo/{owner}/{repo}/tech.svg` | Анализ одного репо |
| GET | `/health` | Health check |
| GET | `/cache/stats` | Статистика кэша |

### Query параметры

| Параметр | Значения | По умолчанию |
|----------|----------|--------------|
| `theme` | light, dark, dracula, nord, monokai, github-dimmed, solarized-light, solarized-dark, gruvbox-light, gruvbox-dark, one-dark, tokyo-night, catppuccin, synthwave, rose-pine, ayu-dark, cobalt, oceanic, night-owl | light |
| `style` | card, badges, grid, pie | card |
| `columns` | 1-10 | auto |

## Примеры использования

### В браузере

```
http://127.0.0.1:8000/demo/techstack.svg
http://127.0.0.1:8000/demo/techstack.svg?style=badges&theme=dark
http://127.0.0.1:8000/demo/techstack.svg?style=pie&theme=nord
http://127.0.0.1:8000/TheSeydiCharyyev/techstack.svg?theme=dark
```

### В README.md на GitHub

```markdown
![Tech Stack](https://your-vercel-domain.vercel.app/TheSeydiCharyyev/techstack.svg)

![Tech Stack](https://your-vercel-domain.vercel.app/TheSeydiCharyyev/techstack.svg?theme=dark&style=badges)
```

## Поддерживаемые технологии

### Языки (из GitHub API)
Python, JavaScript, TypeScript, Java, Kotlin, Swift, Go, Rust, C, C++, C#, Ruby, PHP, Dart, Scala, Elixir, Haskell, Lua, R, Shell, и 20+ других

### Фреймворки
- **JavaScript/TypeScript**: React, React Native, Next.js, Vue.js, Nuxt, Angular, Svelte, Remix, Astro, Gatsby, Electron, SolidJS, Express, Fastify, NestJS
- **Python**: Django, FastAPI, Flask, Starlette, aiohttp
- **Dart/Flutter**: Flutter, Dart, Firebase, BLoC, Provider, Riverpod, GetX, Dio, Hive, GoRouter, Freezed
- **Rust**: Actix Web, Rocket, Axum, Warp
- **Go**: Gin, Fiber, Echo, Gorilla Mux, Beego

### DevOps
Docker, Kubernetes, GitHub Actions, GitLab CI, Jenkins, Terraform, Ansible, Vercel, Netlify, AWS, Azure, GCP

### Базы данных
PostgreSQL, MySQL, MongoDB, Redis, SQLite, Prisma, SQLAlchemy, Alembic

### Инструменты
- **Build**: Webpack, Vite, Babel
- **Testing**: Jest, Vitest, Pytest, Mocha
- **State**: Redux, Zustand, MobX
- **Styling**: Tailwind CSS, Styled Components, Emotion, MUI, Chakra UI
- **API**: GraphQL, tRPC, Axios, Socket.io
- **ML**: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy
- **Other**: Streamlit, Gradio, Scrapy, Pydantic, HTTPX

## Деплой на Vercel

1. Push проект на GitHub
2. Импортировать в Vercel
3. Добавить переменную окружения `GITHUB_TOKEN`
4. Deploy

Файлы для Vercel уже настроены:
- `vercel.json` — конфигурация
- `api/index.py` — entry point

## TODO

- [x] SVG иконки технологий (Devicon CDN)
- [x] Rust/Go анализаторы
- [x] Больше тем (19 тем)
- [x] Адаптивная ширина
- [x] Параллельные запросы
- [x] Умное кэширование (LRU)
- [x] Языки из GitHub API
- [ ] Кэширование в Redis для Vercel
- [ ] Rate limiting
- [ ] Деплой на Vercel

## Статус

✅ Базовая структура
✅ GitHub клиент с кэшем и connection pooling
✅ Анализаторы (JS, Python, Flutter, Rust, Go, DevOps, Languages)
✅ SVG генератор (4 стиля, 19 тем, 100+ иконок)
✅ Параллельные запросы (asyncio.gather)
✅ Умное кэширование (LRU + user cache)
✅ Адаптивная ширина (auto columns)
✅ Демо эндпоинт
✅ Vercel конфигурация
⏳ Деплой на Vercel
