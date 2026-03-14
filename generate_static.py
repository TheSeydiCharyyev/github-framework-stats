#!/usr/bin/env python3
"""Generate static tech stack SVGs for a GitHub profile.

Usage:
    python generate_static.py [output_dir]

Requires GITHUB_TOKEN env var for API access.
Output directory defaults to current directory.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

from app.github_client import GitHubClient
from app.analyzers import ALL_ANALYZERS
from app.analyzers.base import Technology
from app.svg.generator import SVGGenerator, CATEGORY_LABELS, CATEGORY_COLORS
from app.svg.icons import fetch_icons
from app.svg.themes import get_theme
from jinja2 import Environment, FileSystemLoader

USERNAME = "TheSeydiCharyyev"

SVGS_TO_GENERATE = [
    {"filename": "techstack_pie.svg", "style": "pie", "theme": "light"},
    {"filename": "techstack_grid.svg", "style": "grid", "theme": "light"},
]


async def analyze_repo(owner: str, repo: str, github_client: GitHubClient) -> list[Technology]:
    """Analyze a single repository with all analyzers."""
    tasks = [analyzer.analyze(owner, repo, github_client) for analyzer in ALL_ANALYZERS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    technologies = []
    for result in results:
        if isinstance(result, list):
            technologies.extend(result)
    return technologies


async def analyze_user(username: str, github_client: GitHubClient, max_repos: int = 30) -> list[Technology]:
    """Analyze all repos for a user."""
    repos = await github_client.get_user_repos(username)

    # Filter out forks and sort by stars
    repos = [r for r in repos if not r.get("fork")]
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    repos = repos[:max_repos]

    print(f"Analyzing {len(repos)} repos for {username}...")

    tasks = [analyze_repo(username, repo["name"], github_client) for repo in repos]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_technologies = []
    for result in results:
        if isinstance(result, list):
            all_technologies.extend(result)
    return all_technologies


CATEGORY_GROUPS = [
    {"label": "Languages", "keys": ["language"], "color": "#f1e05a", "icon_id": "languages"},
    {"label": "Frameworks", "keys": ["framework"], "color": "#61dafb", "icon_id": "frameworks"},
    {"label": "Backend &amp; Server", "keys": ["backend", "server"], "color": "#da3633", "icon_id": "backend"},
    {"label": "HTTP &amp; API", "keys": ["http", "api", "realtime"], "color": "#56d4dd", "icon_id": "http-api"},
    {"label": "Build Tools", "keys": ["build"], "color": "#ff7b72", "icon_id": "build"},
    {"label": "State Mgmt", "keys": ["state"], "color": "#8b949e", "icon_id": "state"},
    {"label": "UI &amp; Styling", "keys": ["styling", "ui", "graphics"], "color": "#e377c2", "icon_id": "ui-styling"},
    {"label": "Testing", "keys": ["testing", "validation"], "color": "#d29922", "icon_id": "testing"},
    {"label": "DevOps &amp; CI", "keys": ["devops", "ci", "iac"], "color": "#f0883e", "icon_id": "devops"},
    {"label": "Database &amp; Storage", "keys": ["database", "storage"], "color": "#3fb950", "icon_id": "database"},
    {"label": "Hosting", "keys": ["hosting"], "color": "#f778ba", "icon_id": "hosting"},
    {"label": "ML &amp; Data Science", "keys": ["ml", "data", "scraping"], "color": "#a371f7", "icon_id": "ml"},
]


def generate_stats_card(technologies: list[Technology], output_dir: Path, total_repos: int):
    """Generate the Tech Stack Stats card."""
    theme = get_theme("light")
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=False)

    # Aggregate by name first, then count unique techs
    tech_map: dict[str, Technology] = {}
    for t in technologies:
        if t.name in tech_map:
            tech_map[t.name].count += t.count
        else:
            tech_map[t.name] = Technology(t.name, t.category, t.icon, t.color, t.count)

    total_techs = len(tech_map)

    # Count techs per raw category
    cat_counts: dict[str, int] = {}
    for t in tech_map.values():
        cat_counts[t.category] = cat_counts.get(t.category, 0) + 1

    # Group into clean categories
    categories = []
    used_keys = set()
    for group in CATEGORY_GROUPS:
        count = sum(cat_counts.get(k, 0) for k in group["keys"])
        if count > 0:
            categories.append({
                "label": group["label"],
                "color": group["color"],
                "count": count,
                "icon_id": group["icon_id"],
            })
            used_keys.update(group["keys"])

    # Catch any ungrouped categories into "Other"
    other_count = sum(v for k, v in cat_counts.items() if k not in used_keys)
    if other_count > 0:
        categories.append({"label": "Other", "color": "#8b949e", "count": other_count, "icon_id": "other"})

    # Sort by count descending
    categories.sort(key=lambda x: x["count"], reverse=True)

    width = 350
    row_height = 32
    header_height = 48
    totals_height = 80
    padding = 24
    height = padding + header_height + len(categories) * row_height + totals_height + padding

    template = env.get_template("stats.svg.jinja2")
    svg = template.render(
        theme=theme,
        width=width,
        height=height,
        total_techs=total_techs,
        total_repos=total_repos,
        categories=categories,
        row_height=row_height,
        header_height=header_height,
        padding=padding,
    )

    path = output_dir / "techstack_stats.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"Generated {path}")

    return height


async def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set. API rate limits will be very low.")

    github = GitHubClient(token=token)
    svg_generator = SVGGenerator()

    try:
        repos = await github.get_user_repos(USERNAME)
        repos = [r for r in repos if not r.get("fork")]
        technologies = await analyze_user(USERNAME, github)
        print(f"Detected {len(technologies)} technology entries")

        # Fetch icons for all detected technologies
        icon_names = list({t.icon for t in technologies})
        await fetch_icons(icon_names)

        # Generate stats card first to get its height
        stats_height = generate_stats_card(technologies, output_dir, len(repos))

        for svg_config in SVGS_TO_GENERATE:
            techs = technologies
            # For pie chart: exclude languages, show only top 8
            if svg_config["style"] == "pie":
                techs = [t for t in technologies if t.category != "language"]

            svg_content = svg_generator.generate(
                technologies=techs,
                username=USERNAME,
                theme_name=svg_config["theme"],
                style_name=svg_config["style"],
                max_items=11 if svg_config["style"] == "pie" else None,
                forced_height=stats_height if svg_config["style"] == "pie" else None,
            )
            output_path = output_dir / svg_config["filename"]
            output_path.write_text(svg_content, encoding="utf-8")
            print(f"Generated {output_path}")

    finally:
        await github.close()

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
