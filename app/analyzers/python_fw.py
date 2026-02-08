from .base import BaseAnalyzer, Technology


class PythonAnalyzer(BaseAnalyzer):
    """Analyzer for Python projects."""

    @property
    def files_to_check(self) -> list[str]:
        return ["requirements.txt", "pyproject.toml", "Pipfile", "setup.py"]

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []
        detected = set()

        # Check all Python dependency files
        for file in self.files_to_check:
            content = await github_client.get_file_content(owner, repo, file)
            if content:
                content_lower = content.lower()
                self._analyze_content(content_lower, technologies, detected)

        return technologies

    def _analyze_content(
        self,
        content: str,
        technologies: list[Technology],
        detected: set[str],
    ) -> None:
        # Web frameworks
        if "django" in content and "django" not in detected:
            technologies.append(
                self._create_tech("Django", "framework", "django", "#092E20")
            )
            detected.add("django")

        if "fastapi" in content and "fastapi" not in detected:
            technologies.append(
                self._create_tech("FastAPI", "framework", "fastapi", "#009688")
            )
            detected.add("fastapi")

        if "flask" in content and "flask" not in detected:
            technologies.append(
                self._create_tech("Flask", "framework", "flask", "#000000")
            )
            detected.add("flask")

        if "starlette" in content and "starlette" not in detected:
            technologies.append(
                self._create_tech("Starlette", "framework", "starlette", "#392E59")
            )
            detected.add("starlette")

        # Async libraries
        if "aiohttp" in content and "aiohttp" not in detected:
            technologies.append(
                self._create_tech("aiohttp", "backend", "aiohttp", "#2C5BB4")
            )
            detected.add("aiohttp")

        # Data science
        if "pandas" in content and "pandas" not in detected:
            technologies.append(
                self._create_tech("Pandas", "data", "pandas", "#150458")
            )
            detected.add("pandas")

        if "numpy" in content and "numpy" not in detected:
            technologies.append(
                self._create_tech("NumPy", "data", "numpy", "#013243")
            )
            detected.add("numpy")

        # ML frameworks
        if "tensorflow" in content and "tensorflow" not in detected:
            technologies.append(
                self._create_tech("TensorFlow", "ml", "tensorflow", "#FF6F00")
            )
            detected.add("tensorflow")

        if "pytorch" in content or "torch" in content:
            if "pytorch" not in detected:
                technologies.append(
                    self._create_tech("PyTorch", "ml", "pytorch", "#EE4C2C")
                )
                detected.add("pytorch")

        if "scikit-learn" in content or "sklearn" in content:
            if "sklearn" not in detected:
                technologies.append(
                    self._create_tech("Scikit-learn", "ml", "sklearn", "#F7931E")
                )
                detected.add("sklearn")

        # Database ORMs
        if "sqlalchemy" in content and "sqlalchemy" not in detected:
            technologies.append(
                self._create_tech("SQLAlchemy", "database", "sqlalchemy", "#D71F00")
            )
            detected.add("sqlalchemy")

        # Testing
        if "pytest" in content and "pytest" not in detected:
            technologies.append(
                self._create_tech("Pytest", "testing", "pytest", "#0A9EDC")
            )
            detected.add("pytest")

        # Async
        if "celery" in content and "celery" not in detected:
            technologies.append(
                self._create_tech("Celery", "backend", "celery", "#37814A")
            )
            detected.add("celery")

        # Additional frameworks
        if "pydantic" in content and "pydantic" not in detected:
            technologies.append(
                self._create_tech("Pydantic", "validation", "pydantic", "#E92063")
            )
            detected.add("pydantic")

        if "httpx" in content and "httpx" not in detected:
            technologies.append(
                self._create_tech("HTTPX", "http", "httpx", "#3B82F6")
            )
            detected.add("httpx")

        if "scrapy" in content and "scrapy" not in detected:
            technologies.append(
                self._create_tech("Scrapy", "scraping", "scrapy", "#60A839")
            )
            detected.add("scrapy")

        if "beautifulsoup" in content or "bs4" in content:
            if "bs4" not in detected:
                technologies.append(
                    self._create_tech("BeautifulSoup", "scraping", "bs4", "#3F4F75")
                )
                detected.add("bs4")

        if "streamlit" in content and "streamlit" not in detected:
            technologies.append(
                self._create_tech("Streamlit", "ui", "streamlit", "#FF4B4B")
            )
            detected.add("streamlit")

        if "gradio" in content and "gradio" not in detected:
            technologies.append(
                self._create_tech("Gradio", "ui", "gradio", "#F97316")
            )
            detected.add("gradio")

        if "alembic" in content and "alembic" not in detected:
            technologies.append(
                self._create_tech("Alembic", "database", "alembic", "#6BA81E")
            )
            detected.add("alembic")

        if "redis" in content and "redis" not in detected:
            technologies.append(
                self._create_tech("Redis", "database", "redis", "#DC382D")
            )
            detected.add("redis")

        if "pymongo" in content or "motor" in content:
            if "mongodb" not in detected:
                technologies.append(
                    self._create_tech("MongoDB", "database", "mongodb", "#47A248")
                )
                detected.add("mongodb")

        if "uvicorn" in content and "uvicorn" not in detected:
            technologies.append(
                self._create_tech("Uvicorn", "server", "uvicorn", "#499848")
            )
            detected.add("uvicorn")

        if "gunicorn" in content and "gunicorn" not in detected:
            technologies.append(
                self._create_tech("Gunicorn", "server", "gunicorn", "#499848")
            )
            detected.add("gunicorn")
