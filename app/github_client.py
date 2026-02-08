import os
import base64
import httpx
import asyncio
import logging
from typing import Optional
from .cache import cache

logger = logging.getLogger(__name__)


class GitHubClient:
    """Async GitHub API client with connection pooling and concurrency control."""

    BASE_URL = "https://api.github.com"
    MAX_CONCURRENT_REQUESTS = 10  # Limit concurrent requests to avoid rate limiting

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TechStack-Analyzer",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
        self._rate_limited = False
        self._client: Optional[httpx.AsyncClient] = None
        self._semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create a shared HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers=self.headers,
                timeout=10.0,
                limits=httpx.Limits(max_connections=20, max_keepalive_connections=10)
            )
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def _request(self, endpoint: str) -> Optional[dict | list]:
        # Skip requests if we're rate limited
        if self._rate_limited:
            return None

        cache_key = f"github:{endpoint}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        async with self._semaphore:  # Limit concurrent requests
            client = await self._get_client()
            try:
                response = await client.get(f"{self.BASE_URL}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    cache.set(cache_key, data)
                    return data
                elif response.status_code == 403:
                    # Rate limited
                    self._rate_limited = True
                    logger.warning("GitHub API rate limit exceeded")
                    return None
                elif response.status_code == 404:
                    # Cache 404s briefly to avoid repeated lookups
                    cache.set(cache_key, None, ttl=300)
                    return None
                return None
            except httpx.RequestError as e:
                logger.error(f"GitHub API request error: {e}")
                return None

    async def get_user_repos(self, username: str, per_page: int = 100) -> list[dict]:
        """Get all public repos for a user."""
        repos = []
        page = 1
        while True:
            data = await self._request(
                f"/users/{username}/repos?per_page={per_page}&page={page}&sort=updated"
            )
            if not data:
                break
            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return repos

    async def get_repo_contents(
        self, owner: str, repo: str, path: str = ""
    ) -> Optional[list[dict] | dict]:
        """Get contents of a repo directory or file."""
        return await self._request(f"/repos/{owner}/{repo}/contents/{path}")

    async def get_file_content(
        self, owner: str, repo: str, path: str
    ) -> Optional[str]:
        """Get decoded content of a file."""
        data = await self._request(f"/repos/{owner}/{repo}/contents/{path}")
        if data and isinstance(data, dict) and "content" in data:
            try:
                return base64.b64decode(data["content"]).decode("utf-8")
            except Exception:
                return None
        return None

    async def check_file_exists(
        self, owner: str, repo: str, path: str
    ) -> bool:
        """Check if a file exists in the repo."""
        data = await self._request(f"/repos/{owner}/{repo}/contents/{path}")
        return data is not None

    async def get_directory_files(
        self, owner: str, repo: str, path: str
    ) -> list[str]:
        """Get list of files in a directory."""
        data = await self._request(f"/repos/{owner}/{repo}/contents/{path}")
        if data and isinstance(data, list):
            return [item["name"] for item in data if item["type"] == "file"]
        return []

    async def get_repo_languages(
        self, owner: str, repo: str
    ) -> dict[str, int]:
        """Get languages used in a repository with byte counts."""
        data = await self._request(f"/repos/{owner}/{repo}/languages")
        if data and isinstance(data, dict):
            return data
        return {}
