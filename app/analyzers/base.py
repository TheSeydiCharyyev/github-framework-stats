from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Technology:
    name: str
    category: str  # framework, runtime, devops, database, etc.
    icon: str  # icon identifier
    color: str  # brand color (hex)
    count: int = 1  # number of repos using this


class BaseAnalyzer(ABC):
    """Base class for technology analyzers."""

    @property
    @abstractmethod
    def files_to_check(self) -> list[str]:
        """List of file paths to analyze."""
        pass

    @abstractmethod
    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        """Analyze repository and return detected technologies."""
        pass

    def _create_tech(
        self, name: str, category: str, icon: str, color: str
    ) -> Technology:
        return Technology(
            name=name,
            category=category,
            icon=icon,
            color=color,
        )
