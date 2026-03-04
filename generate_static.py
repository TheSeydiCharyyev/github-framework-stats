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
from app.svg.generator import SVGGenerator
from app.svg.icons import fetch_icons

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


async def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set. API rate limits will be very low.")

    github = GitHubClient(token=token)
    svg_generator = SVGGenerator()

    try:
        technologies = await analyze_user(USERNAME, github)
        print(f"Detected {len(technologies)} technology entries")

        # Fetch icons for all detected technologies
        icon_names = list({t.icon for t in technologies})
        await fetch_icons(icon_names)

        for svg_config in SVGS_TO_GENERATE:
            svg_content = svg_generator.generate(
                technologies=technologies,
                username=USERNAME,
                theme_name=svg_config["theme"],
                style_name=svg_config["style"],
            )
            output_path = output_dir / svg_config["filename"]
            output_path.write_text(svg_content, encoding="utf-8")
            print(f"Generated {output_path}")

    finally:
        await github.close()

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
