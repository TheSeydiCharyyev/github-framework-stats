from .base import BaseAnalyzer, Technology


class GoAnalyzer(BaseAnalyzer):
    """Analyzer for Go projects."""

    @property
    def files_to_check(self) -> list[str]:
        return ["go.mod"]

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        content = await github_client.get_file_content(owner, repo, "go.mod")
        if not content:
            return technologies

        content_lower = content.lower()

        # Go is being used
        technologies.append(
            self._create_tech("Go", "language", "go", "#00ADD8")
        )

        # Web frameworks
        if "github.com/gin-gonic/gin" in content_lower:
            technologies.append(
                self._create_tech("Gin", "framework", "gin", "#00ADD8")
            )

        if "github.com/gofiber/fiber" in content_lower:
            technologies.append(
                self._create_tech("Fiber", "framework", "fiber", "#00ACD7")
            )

        if "github.com/labstack/echo" in content_lower:
            technologies.append(
                self._create_tech("Echo", "framework", "echo", "#00ADD8")
            )

        if "github.com/gorilla/mux" in content_lower:
            technologies.append(
                self._create_tech("Gorilla Mux", "framework", "gorilla", "#00ADD8")
            )

        if "github.com/beego/beego" in content_lower:
            technologies.append(
                self._create_tech("Beego", "framework", "beego", "#00ADD8")
            )

        # Database
        if "gorm.io/gorm" in content_lower:
            technologies.append(
                self._create_tech("GORM", "database", "gorm", "#00ADD8")
            )

        if "github.com/jmoiron/sqlx" in content_lower:
            technologies.append(
                self._create_tech("sqlx", "database", "sqlx", "#00ADD8")
            )

        # GraphQL
        if "github.com/99designs/gqlgen" in content_lower:
            technologies.append(
                self._create_tech("gqlgen", "api", "graphql", "#E10098")
            )

        # gRPC
        if "google.golang.org/grpc" in content_lower:
            technologies.append(
                self._create_tech("gRPC", "api", "grpc", "#244C5A")
            )

        return technologies
