# GitHub Tech Stack Analyzer — Roadmap

Open source project for generating SVG badges with GitHub user's tech stack.

---

## Phase 1: Setup & Configuration

- [x] Create GitHub Personal Access Token
- [x] Add token to environment (`.env` file)
- [x] Add `.gitignore` to protect secrets
- [x] Test with real GitHub data (12 technologies detected)

---

## Phase 2: Оптимизация и улучшения

### 2.1 Оптимизация скорости
- [x] Параллельные запросы к GitHub API (asyncio.gather)
- [x] Лимит на количество репозиториев (топ-30 по звёздам)
- [x] Connection pooling (shared httpx client)
- [x] Semaphore для контроля concurrent requests (max 10)
- [x] Умное кэширование результатов (LRU + user_cache)

### 2.2 Улучшение анализаторов
- [x] Добавить больше технологий (Remix, Astro, Gatsby, Electron, Prisma, GraphQL, Axios, Socket.io, MUI, Chakra, tRPC, Pydantic, Streamlit, Gradio, Scrapy, Redis, MongoDB)
- [x] Улучшить детекцию Flutter (regex паттерны + 15 новых технологий)
- [x] Добавить языки программирования из GitHub API (40+ языков)

### 2.3 Улучшение SVG
- [x] Настоящие иконки (Devicon CDN, 100+ маппингов)
- [x] Больше тем оформления (19 тем)
- [x] Адаптивная ширина (auto columns + параметр columns=1-10)

---

## Phase 3: Деплой

- [ ] Настроить Vercel
- [ ] Добавить GITHUB_TOKEN в Vercel environment
- [ ] Тестирование production
- [ ] Документация для пользователей

---

## Notes

- Current status: Works with real GitHub data
- Server: `python -m uvicorn app.main:app --reload --port 8000`
- Test: http://127.0.0.1:8000/TheSeydiCharyyev/techstack.svg
- Demo: http://127.0.0.1:8000/demo/techstack.svg
