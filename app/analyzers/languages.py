from .base import BaseAnalyzer, Technology


# Language colors from GitHub
LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#F7DF1E",
    "TypeScript": "#3178C6",
    "Java": "#B07219",
    "Kotlin": "#A97BFF",
    "Swift": "#F05138",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
    "C": "#555555",
    "C++": "#F34B7D",
    "C#": "#239120",
    "Ruby": "#CC342D",
    "PHP": "#777BB4",
    "Dart": "#0175C2",
    "Scala": "#DC322F",
    "Elixir": "#6E4A7E",
    "Haskell": "#5D4F85",
    "Lua": "#000080",
    "Perl": "#0298C3",
    "R": "#198CE7",
    "Shell": "#89E051",
    "PowerShell": "#012456",
    "HTML": "#E34C26",
    "CSS": "#1572B6",
    "SCSS": "#C6538C",
    "Vue": "#4FC08D",
    "Svelte": "#FF3E00",
    "Jupyter Notebook": "#F37626",
    "Objective-C": "#438EFF",
    "Groovy": "#4298B8",
    "Clojure": "#5881D8",
    "F#": "#B845FC",
    "OCaml": "#3BE133",
    "Erlang": "#B83998",
    "Zig": "#F7A41D",
    "Nim": "#FFE953",
    "Crystal": "#000100",
    "Julia": "#9558B2",
    "MATLAB": "#E16737",
    "Assembly": "#6E4C13",
    "Solidity": "#AA6746",
    "Move": "#4A137F",
    "Cairo": "#F39C12",
}

# Minimum percentage to include a language
MIN_LANGUAGE_PERCENT = 5


class LanguageAnalyzer(BaseAnalyzer):
    """Analyzer that detects programming languages from GitHub API."""

    @property
    def files_to_check(self) -> list[str]:
        return []  # Uses GitHub API, not file checks

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        languages = await github_client.get_repo_languages(owner, repo)
        if not languages:
            return technologies

        # Calculate total bytes
        total_bytes = sum(languages.values())
        if total_bytes == 0:
            return technologies

        # Add languages that make up at least MIN_LANGUAGE_PERCENT of the codebase
        for lang, bytes_count in languages.items():
            percent = (bytes_count / total_bytes) * 100
            if percent >= MIN_LANGUAGE_PERCENT:
                color = LANGUAGE_COLORS.get(lang, "#6E7681")
                icon = lang.lower().replace(" ", "-").replace("#", "sharp").replace("++", "pp")
                technologies.append(
                    self._create_tech(lang, "language", icon, color)
                )

        return technologies
