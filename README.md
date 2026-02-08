# GitHub Tech Stack Analyzer

[![Deploy](https://img.shields.io/badge/Live-github--framework--stats.vercel.app-brightgreen)](https://github-framework-stats.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vercel](https://img.shields.io/badge/Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com)

Generate beautiful SVG cards showing any GitHub user's **real tech stack** — auto-detected from repository code. Languages, frameworks, databases, DevOps tools and more.

<p align="center">
  <img src="https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?theme=light&style=card" alt="Example Tech Stack Card" />
</p>

## Quick Start

Add this to your GitHub profile README:

```markdown
![Tech Stack](https://github-framework-stats.vercel.app/YOUR_USERNAME/techstack.svg)
```

Replace `YOUR_USERNAME` with your GitHub username.

## Live Examples

| Style | URL |
|-------|-----|
| Card (default) | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg` |
| Badges | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?style=badges` |
| Grid | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?style=grid` |
| Pie | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?style=pie` |
| Dark theme | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?theme=dark` |
| Dracula | `https://github-framework-stats.vercel.app/TheSeydiCharyyev/techstack.svg?theme=dracula` |

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/{username}/techstack.svg` | Full tech stack for a user |
| `/{username}/frameworks.svg` | Frameworks only |
| `/repo/{owner}/{repo}/tech.svg` | Single repository analysis |
| `/demo/techstack.svg` | Demo with mock data |
| `/health` | Health check |

## Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| `theme` | `light`, `dark`, `dracula`, `nord`, `monokai`, `github-dimmed`, `solarized-light`, `solarized-dark`, `gruvbox-light`, `gruvbox-dark`, `one-dark`, `tokyo-night`, `catppuccin`, `synthwave`, `rose-pine`, `ayu-dark`, `cobalt`, `oceanic`, `night-owl` | `light` |
| `style` | `card`, `badges`, `grid`, `pie` | `card` |
| `columns` | `1`-`10` | auto |

## Usage Examples

### In your README

```markdown
<!-- Default card style -->
![Tech Stack](https://github-framework-stats.vercel.app/YOUR_USERNAME/techstack.svg)

<!-- Dark theme with badges -->
![Tech Stack](https://github-framework-stats.vercel.app/YOUR_USERNAME/techstack.svg?theme=dark&style=badges)

<!-- Pie chart, nord theme -->
![Tech Stack](https://github-framework-stats.vercel.app/YOUR_USERNAME/techstack.svg?theme=nord&style=pie)

<!-- Frameworks only -->
![Frameworks](https://github-framework-stats.vercel.app/YOUR_USERNAME/frameworks.svg)

<!-- Single repo -->
![Repo Tech](https://github-framework-stats.vercel.app/repo/YOUR_USERNAME/YOUR_REPO/tech.svg)
```

## How It Works

The service analyzes your public GitHub repositories by:

1. Fetching repos via GitHub API (sorted by stars, up to 30)
2. Scanning config files in each repo (`package.json`, `requirements.txt`, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `Dockerfile`, etc.)
3. Detecting languages via GitHub's language API
4. Aggregating results and generating an SVG with embedded icons

All icons are embedded as base64 — works on GitHub, GitLab, Bitbucket, and anywhere SVGs are rendered.

## Supported Technologies (100+)

**Languages:** Python, JavaScript, TypeScript, Java, Kotlin, Swift, Go, Rust, C, C++, C#, Ruby, PHP, Dart, Scala, Elixir, Haskell, Lua, R, Shell, and 20+ more

**Frontend:** React, React Native, Next.js, Vue.js, Nuxt, Angular, Svelte, Remix, Astro, Gatsby, Electron, SolidJS

**Backend:** Express, Fastify, NestJS, Django, FastAPI, Flask, Rails, Laravel, Spring

**Mobile:** Flutter, Dart, Firebase, BLoC, Provider, Riverpod, GetX, Dio

**DevOps:** Docker, Kubernetes, GitHub Actions, GitLab CI, Jenkins, Terraform, Ansible, Vercel, Netlify, AWS, Azure, GCP

**Databases:** PostgreSQL, MySQL, MongoDB, Redis, SQLite, Prisma, SQLAlchemy

**Tools:** Webpack, Vite, Jest, Pytest, Redux, Tailwind CSS, GraphQL, TensorFlow, PyTorch, Pandas, NumPy

## Self-Hosting

### Deploy to Vercel (recommended)

1. Fork this repository
2. Go to [vercel.com/new](https://vercel.com/new) and import the fork
3. Add environment variable `GITHUB_TOKEN` (create at [github.com/settings/tokens](https://github.com/settings/tokens) with `read:user` scope)
4. Deploy

Or via CLI:

```bash
git clone https://github.com/TheSeydiCharyyev/github-framework-stats.git
cd github-framework-stats
vercel
vercel env add GITHUB_TOKEN
vercel --prod
```

### Run Locally

```bash
git clone https://github.com/TheSeydiCharyyev/github-framework-stats.git
cd github-framework-stats
pip install -r requirements.txt

# Optional: set GitHub token for real data
export GITHUB_TOKEN="your_token_here"

python -m uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/demo/techstack.svg to test.

## Tech Stack

- **Python 3.11+** / **FastAPI** — async API
- **httpx** — async HTTP client with connection pooling
- **Jinja2** — SVG templates
- **Vercel** — serverless hosting

## Project Structure

```
github-framework-stats/
├── app/
│   ├── main.py              # FastAPI endpoints
│   ├── github_client.py     # GitHub API client (async, cached)
│   ├── cache.py             # In-memory LRU cache (1h TTL)
│   ├── analyzers/           # Technology detectors
│   │   ├── languages.py     # GitHub API languages
│   │   ├── javascript.py    # package.json parser
│   │   ├── python_fw.py     # requirements.txt parser
│   │   ├── flutter.py       # pubspec.yaml parser
│   │   ├── rust.py          # Cargo.toml parser
│   │   ├── go.py            # go.mod parser
│   │   └── devops.py        # Dockerfile/CI detection
│   └── svg/
│       ├── generator.py     # SVG generator (adaptive layout)
│       ├── themes.py        # 19 color themes
│       ├── styles.py        # 4 layout styles
│       └── icons.py         # Devicon mapping + base64 embedding
├── templates/               # Jinja2 SVG templates
├── api/index.py             # Vercel entry point
├── vercel.json
└── requirements.txt
```

## License

MIT
