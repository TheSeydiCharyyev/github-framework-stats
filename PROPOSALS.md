# GitHub Framework Stats — Предложения

## Идея проекта
Сервис который анализирует GitHub репозитории и определяет **фреймворки и технологии**, а не только языки программирования.

---

## Как определять фреймворки

| Файл для анализа | Что ищем | Результат |
|------------------|----------|-----------|
| `pubspec.yaml` | `flutter:` в dependencies | Flutter |
| `package.json` | `react-native` | React Native |
| `package.json` | `next` | Next.js |
| `package.json` | `@angular/core` | Angular |
| `package.json` | `vue` | Vue.js |
| `package.json` | `express` | Express.js |
| `requirements.txt` / `pyproject.toml` | `django` | Django |
| `requirements.txt` / `pyproject.toml` | `fastapi` | FastAPI |
| `requirements.txt` / `pyproject.toml` | `flask` | Flask |
| `Dockerfile` | наличие файла | Docker |
| `docker-compose.yml` | наличие файла | Docker Compose |
| `kubernetes/` или `k8s/` | наличие папки | Kubernetes |
| `.github/workflows/` | наличие | GitHub Actions |
| `firebase.json` | наличие | Firebase |
| `vercel.json` | наличие | Vercel |
| `Cargo.toml` | `actix-web`, `rocket` | Actix/Rocket |
| `go.mod` | `gin`, `fiber` | Gin/Fiber |

---

## Стек для разработки

### Вариант 1: Python + FastAPI (рекомендую)
```
github-framework-stats/
├── app/
│   ├── main.py              # FastAPI приложение
│   ├── github_client.py     # Работа с GitHub API
│   ├── analyzers/
│   │   ├── flutter.py       # Анализ Flutter проектов
│   │   ├── react_native.py  # Анализ React Native
│   │   ├── python_frameworks.py
│   │   └── ...
│   ├── svg_generator.py     # Генерация SVG картинок
│   └── cache.py             # Кэширование (Redis/память)
├── templates/
│   └── stats.svg            # SVG шаблон
├── requirements.txt
└── Dockerfile
```

### Вариант 2: TypeScript + Node.js
```
github-framework-stats/
├── src/
│   ├── index.ts
│   ├── github.ts
│   ├── analyzers/
│   └── svg.ts
├── package.json
└── Dockerfile
```

---

## API эндпоинты

```
GET /{username}/frameworks.svg     — SVG картинка с фреймворками
GET /{username}/techstack.svg      — полный стек (языки + фреймворки + инструменты)
GET /{username}/data.json          — JSON данные (опционально)
GET /repo/{owner}/{repo}/tech.svg  — анализ конкретного репо
```

---

## Пример использования в README

```markdown
![My Tech Stack](https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg)
```

---

## Дизайн SVG

Варианты стилей:
1. **Карточки** — как github-readme-stats (тёмная/светлая тема)
2. **Бейджи** — как shields.io (маленькие иконки в ряд)
3. **Круговая диаграмма** — процентное соотношение
4. **Сетка иконок** — логотипы технологий

---

## Кэширование

GitHub API имеет лимиты (5000 запросов/час с токеном).
Решение: кэшировать результаты на 1-24 часа.

---

## Хостинг (бесплатные варианты)

1. **Vercel** — идеально для serverless
2. **Cloudflare Workers** — быстро, бесплатно
3. **Railway** — просто деплоить
4. **Render** — бесплатный tier

---

## MVP (минимальный продукт)

Для начала:
1. Поддержка 5-10 популярных фреймворков
2. Один стиль SVG
3. Кэш в памяти
4. Деплой на Vercel

Потом добавим:
- Больше фреймворков
- Темы оформления
- Кастомизация через URL параметры
- JSON API

---

## Вопросы для обсуждения

1. Python или TypeScript?
2. Какой дизайн SVG нравится больше?
3. Какие фреймворки в первую очередь поддержать?
4. Название проекта? (github-framework-stats, techstack-readme, repo-analyzer...)

---

Когда вернёшься — обсудим и начнём!
