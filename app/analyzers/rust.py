from .base import BaseAnalyzer, Technology


class RustAnalyzer(BaseAnalyzer):
    """Analyzer for Rust projects."""

    @property
    def files_to_check(self) -> list[str]:
        return ["Cargo.toml"]

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        content = await github_client.get_file_content(owner, repo, "Cargo.toml")
        if not content:
            return technologies

        content_lower = content.lower()

        # Rust is being used
        technologies.append(
            self._create_tech("Rust", "language", "rust", "#DEA584")
        )

        # Web frameworks
        if "actix-web" in content_lower:
            technologies.append(
                self._create_tech("Actix Web", "framework", "actix", "#000000")
            )

        if "rocket" in content_lower:
            technologies.append(
                self._create_tech("Rocket", "framework", "rocket", "#D33847")
            )

        if "axum" in content_lower:
            technologies.append(
                self._create_tech("Axum", "framework", "axum", "#000000")
            )

        if "warp" in content_lower:
            technologies.append(
                self._create_tech("Warp", "framework", "warp", "#000000")
            )

        # Async runtimes
        if "tokio" in content_lower:
            technologies.append(
                self._create_tech("Tokio", "runtime", "tokio", "#000000")
            )

        # Database
        if "diesel" in content_lower:
            technologies.append(
                self._create_tech("Diesel", "database", "diesel", "#000000")
            )

        if "sqlx" in content_lower:
            technologies.append(
                self._create_tech("SQLx", "database", "sqlx", "#000000")
            )

        # WASM
        if "wasm-bindgen" in content_lower or "wasm-pack" in content_lower:
            technologies.append(
                self._create_tech("WebAssembly", "runtime", "wasm", "#654FF0")
            )

        if "yew" in content_lower:
            technologies.append(
                self._create_tech("Yew", "framework", "yew", "#009A5B")
            )

        if "leptos" in content_lower:
            technologies.append(
                self._create_tech("Leptos", "framework", "leptos", "#EF3939")
            )

        return technologies
