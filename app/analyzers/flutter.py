import re
from .base import BaseAnalyzer, Technology


class FlutterAnalyzer(BaseAnalyzer):
    """Analyzer for Flutter/Dart projects."""

    @property
    def files_to_check(self) -> list[str]:
        return ["pubspec.yaml"]

    def _is_flutter_project(self, content: str) -> bool:
        """Check if this is a Flutter project using multiple patterns."""
        # Pattern 1: sdk: flutter (with flexible spacing)
        if re.search(r'sdk:\s*flutter', content):
            return True
        # Pattern 2: flutter section at root level with uses-material-design
        if re.search(r'^flutter:\s*$', content, re.MULTILINE):
            return True
        # Pattern 3: flutter dependency in dependencies section
        if 'dependencies:' in content and re.search(r'flutter:\s*\n\s+sdk:', content):
            return True
        return False

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        content = await github_client.get_file_content(owner, repo, "pubspec.yaml")
        if not content:
            return technologies

        # Check for Flutter SDK
        if self._is_flutter_project(content):
            technologies.append(
                self._create_tech("Flutter", "framework", "flutter", "#02569B")
            )

            # Also add Dart since Flutter uses Dart
            technologies.append(
                self._create_tech("Dart", "language", "dart", "#0175C2")
            )

        # Check for common Flutter packages
        if "firebase_core:" in content or "firebase_auth:" in content:
            technologies.append(
                self._create_tech("Firebase", "backend", "firebase", "#FFCA28")
            )

        if "bloc:" in content or "flutter_bloc:" in content:
            technologies.append(
                self._create_tech("BLoC", "state", "bloc", "#00B4AB")
            )

        if "provider:" in content:
            technologies.append(
                self._create_tech("Provider", "state", "provider", "#FF7043")
            )

        if "riverpod:" in content or "flutter_riverpod:" in content:
            technologies.append(
                self._create_tech("Riverpod", "state", "riverpod", "#00A0FF")
            )

        if "get:" in content or "get_it:" in content:
            technologies.append(
                self._create_tech("GetX", "state", "getx", "#8E24AA")
            )

        # HTTP clients
        if "dio:" in content:
            technologies.append(
                self._create_tech("Dio", "http", "dio", "#1E88E5")
            )

        if "http:" in content:
            technologies.append(
                self._create_tech("HTTP", "http", "http", "#4CAF50")
            )

        # Local storage
        if "hive:" in content or "hive_flutter:" in content:
            technologies.append(
                self._create_tech("Hive", "storage", "hive", "#FFC107")
            )

        if "shared_preferences:" in content:
            technologies.append(
                self._create_tech("SharedPreferences", "storage", "sharedpref", "#607D8B")
            )

        if "sqflite:" in content:
            technologies.append(
                self._create_tech("SQLite", "database", "sqlite", "#003B57")
            )

        if "drift:" in content or "moor:" in content:
            technologies.append(
                self._create_tech("Drift", "database", "drift", "#4E7EC1")
            )

        # Routing
        if "go_router:" in content:
            technologies.append(
                self._create_tech("GoRouter", "routing", "gorouter", "#00BCD4")
            )

        if "auto_route:" in content:
            technologies.append(
                self._create_tech("AutoRoute", "routing", "autoroute", "#9C27B0")
            )

        # Code generation
        if "freezed:" in content:
            technologies.append(
                self._create_tech("Freezed", "codegen", "freezed", "#00ACC1")
            )

        if "json_serializable:" in content:
            technologies.append(
                self._create_tech("JSON Serializable", "codegen", "json", "#8BC34A")
            )

        # UI
        if "flutter_hooks:" in content:
            technologies.append(
                self._create_tech("Flutter Hooks", "ui", "hooks", "#3F51B5")
            )

        return technologies
