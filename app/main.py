from fastapi import FastAPI, Response, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from dotenv import load_dotenv
import asyncio

load_dotenv()

from .github_client import GitHubClient
from .analyzers import ALL_ANALYZERS
from .analyzers.base import Technology
from .svg.generator import SVGGenerator
from .cache import cache, user_cache

app = FastAPI(
    title="GitHub Tech Stack Analyzer",
    description="Generate SVG badges showing your GitHub tech stack",
    version="1.0.0",
)

github = GitHubClient()
svg_generator = SVGGenerator()


@app.on_event("shutdown")
async def shutdown_event():
    """Close HTTP client on shutdown."""
    await github.close()


async def analyze_repo(
    owner: str, repo: str, github_client: GitHubClient
) -> list[Technology]:
    """Analyze a single repository with all analyzers."""
    tasks = [analyzer.analyze(owner, repo, github_client) for analyzer in ALL_ANALYZERS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    technologies = []
    for result in results:
        if isinstance(result, list):
            technologies.extend(result)

    return technologies


async def analyze_user(username: str, max_repos: int = 30) -> list[Technology]:
    """Analyze repositories for a user in parallel with caching.

    Args:
        username: GitHub username
        max_repos: Maximum number of repos to analyze (sorted by stars)
    """
    # Check user cache first
    cache_key = f"user:{username}:{max_repos}"
    cached = user_cache.get(cache_key)
    if cached is not None:
        return cached

    repos = await github.get_user_repos(username)

    # Filter out forks and sort by stars (most popular first)
    repos = [r for r in repos if not r.get("fork")]
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    repos = repos[:max_repos]

    # Analyze all repos in parallel
    tasks = [analyze_repo(username, repo["name"], github) for repo in repos]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_technologies = []
    for result in results:
        if isinstance(result, list):
            all_technologies.extend(result)

    # Cache the result
    user_cache.set(cache_key, all_technologies)

    return all_technologies


@app.get("/")
async def root():
    """API documentation."""
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Tech Stack Analyzer</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #0969da; }
        code { background: #f6f8fa; padding: 2px 6px; border-radius: 4px; }
        pre { background: #f6f8fa; padding: 16px; border-radius: 8px; overflow-x: auto; }
        .example { margin: 20px 0; }
        img { max-width: 100%; border: 1px solid #d0d7de; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>GitHub Tech Stack Analyzer</h1>
    <p>Generate SVG badges showing your GitHub tech stack.</p>

    <h2>Usage</h2>
    <pre>![Tech Stack](https://your-domain.vercel.app/{username}/techstack.svg)</pre>

    <h2>Endpoints</h2>
    <ul>
        <li><code>/{username}/techstack.svg</code> - Full tech stack</li>
        <li><code>/{username}/frameworks.svg</code> - Frameworks only</li>
        <li><code>/repo/{owner}/{repo}/tech.svg</code> - Single repo analysis</li>
    </ul>

    <h2>Parameters</h2>
    <ul>
        <li><code>theme</code> - light, dark, dracula, nord, monokai (default: light)</li>
        <li><code>style</code> - card, badges, grid, pie (default: card)</li>
    </ul>

    <h2>Example</h2>
    <pre>![Tech Stack](https://your-domain.vercel.app/TheSeydiCharyyev/techstack.svg?theme=dark&style=card)</pre>

    <h2>Demo</h2>
    <p>Test without GitHub API: <a href="/demo/techstack.svg">/demo/techstack.svg</a></p>
</body>
</html>
    """)


# Mock data for testing (defined before routes to avoid conflicts)
DEMO_TECHNOLOGIES = [
    Technology("React", "framework", "react", "#61DAFB", 8),
    Technology("TypeScript", "language", "typescript", "#3178C6", 7),
    Technology("Next.js", "framework", "nextjs", "#000000", 5),
    Technology("Flutter", "framework", "flutter", "#02569B", 4),
    Technology("Python", "language", "python", "#3776AB", 4),
    Technology("FastAPI", "framework", "fastapi", "#009688", 3),
    Technology("Docker", "devops", "docker", "#2496ED", 6),
    Technology("GitHub Actions", "ci", "github-actions", "#2088FF", 5),
    Technology("Tailwind CSS", "styling", "tailwind", "#06B6D4", 4),
    Technology("PostgreSQL", "database", "postgresql", "#4169E1", 3),
    Technology("Redis", "database", "redis", "#DC382D", 2),
    Technology("Vue.js", "framework", "vue", "#4FC08D", 2),
]


@app.get("/demo/techstack.svg")
async def get_demo_techstack(
    theme: Optional[str] = Query("light", regex="^(light|dark|dracula|nord|monokai|github-dimmed|solarized-light|solarized-dark|gruvbox-light|gruvbox-dark|one-dark|tokyo-night|catppuccin|synthwave|rose-pine|ayu-dark|cobalt|oceanic|night-owl)$"),
    style: Optional[str] = Query("card", regex="^(card|badges|grid|pie)$"),
    columns: Optional[int] = Query(None, ge=1, le=10, description="Number of columns (1-10, auto if not set)"),
):
    """Demo endpoint with mock data for testing."""
    svg = svg_generator.generate(
        technologies=DEMO_TECHNOLOGIES,
        username="demo-user",
        theme_name=theme,
        style_name=style,
        columns=columns,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "no-cache",
        },
    )


@app.get("/{username}/techstack.svg")
async def get_user_techstack(
    username: str,
    theme: Optional[str] = Query("light", regex="^(light|dark|dracula|nord|monokai|github-dimmed|solarized-light|solarized-dark|gruvbox-light|gruvbox-dark|one-dark|tokyo-night|catppuccin|synthwave|rose-pine|ayu-dark|cobalt|oceanic|night-owl)$"),
    style: Optional[str] = Query("card", regex="^(card|badges|grid|pie)$"),
    columns: Optional[int] = Query(None, ge=1, le=10, description="Number of columns (1-10, auto if not set)"),
):
    """Generate SVG for user's complete tech stack."""
    technologies = await analyze_user(username)

    svg = svg_generator.generate(
        technologies=technologies,
        username=username,
        theme_name=theme,
        style_name=style,
        columns=columns,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
            "Content-Disposition": f"inline; filename={username}-techstack.svg",
        },
    )


@app.get("/{username}/frameworks.svg")
async def get_user_frameworks(
    username: str,
    theme: Optional[str] = Query("light", regex="^(light|dark|dracula|nord|monokai|github-dimmed|solarized-light|solarized-dark|gruvbox-light|gruvbox-dark|one-dark|tokyo-night|catppuccin|synthwave|rose-pine|ayu-dark|cobalt|oceanic|night-owl)$"),
    style: Optional[str] = Query("card", regex="^(card|badges|grid|pie)$"),
    columns: Optional[int] = Query(None, ge=1, le=10, description="Number of columns (1-10, auto if not set)"),
):
    """Generate SVG for user's frameworks only."""
    technologies = await analyze_user(username)

    # Filter to frameworks only
    frameworks = [t for t in technologies if t.category == "framework"]

    svg = svg_generator.generate(
        technologies=frameworks,
        username=username,
        theme_name=theme,
        style_name=style,
        columns=columns,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
        },
    )


@app.get("/repo/{owner}/{repo}/tech.svg")
async def get_repo_tech(
    owner: str,
    repo: str,
    theme: Optional[str] = Query("light", regex="^(light|dark|dracula|nord|monokai|github-dimmed|solarized-light|solarized-dark|gruvbox-light|gruvbox-dark|one-dark|tokyo-night|catppuccin|synthwave|rose-pine|ayu-dark|cobalt|oceanic|night-owl)$"),
    style: Optional[str] = Query("card", regex="^(card|badges|grid|pie)$"),
    columns: Optional[int] = Query(None, ge=1, le=10, description="Number of columns (1-10, auto if not set)"),
):
    """Generate SVG for a single repository's tech stack."""
    technologies = await analyze_repo(owner, repo, github)

    svg = svg_generator.generate(
        technologies=technologies,
        username=f"{owner}/{repo}",
        theme_name=theme,
        style_name=style,
        columns=columns,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
        },
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/cache/stats")
async def cache_stats():
    """Cache statistics endpoint."""
    return {
        "api_cache": cache.stats(),
        "user_cache": user_cache.stats(),
    }
