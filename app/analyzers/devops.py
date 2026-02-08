from .base import BaseAnalyzer, Technology


class DevOpsAnalyzer(BaseAnalyzer):
    """Analyzer for DevOps tools and configurations."""

    @property
    def files_to_check(self) -> list[str]:
        return [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            ".github/workflows",
            "kubernetes",
            "k8s",
            ".gitlab-ci.yml",
            "Jenkinsfile",
            "terraform",
            ".terraform",
        ]

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        # Check Docker
        if await github_client.check_file_exists(owner, repo, "Dockerfile"):
            technologies.append(
                self._create_tech("Docker", "devops", "docker", "#2496ED")
            )

        # Check Docker Compose
        for compose_file in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]:
            if await github_client.check_file_exists(owner, repo, compose_file):
                technologies.append(
                    self._create_tech("Docker Compose", "devops", "docker", "#2496ED")
                )
                break

        # Check GitHub Actions
        workflows = await github_client.get_directory_files(
            owner, repo, ".github/workflows"
        )
        if workflows:
            technologies.append(
                self._create_tech("GitHub Actions", "ci", "github-actions", "#2088FF")
            )

        # Check Kubernetes
        for k8s_dir in ["kubernetes", "k8s"]:
            files = await github_client.get_directory_files(owner, repo, k8s_dir)
            if files:
                technologies.append(
                    self._create_tech("Kubernetes", "devops", "kubernetes", "#326CE5")
                )
                break

        # Check GitLab CI
        if await github_client.check_file_exists(owner, repo, ".gitlab-ci.yml"):
            technologies.append(
                self._create_tech("GitLab CI", "ci", "gitlab", "#FC6D26")
            )

        # Check Jenkins
        if await github_client.check_file_exists(owner, repo, "Jenkinsfile"):
            technologies.append(
                self._create_tech("Jenkins", "ci", "jenkins", "#D24939")
            )

        # Check Terraform
        for tf_path in ["terraform", "main.tf", "infrastructure"]:
            if await github_client.check_file_exists(owner, repo, tf_path):
                technologies.append(
                    self._create_tech("Terraform", "iac", "terraform", "#7B42BC")
                )
                break

        # Check Vercel
        if await github_client.check_file_exists(owner, repo, "vercel.json"):
            technologies.append(
                self._create_tech("Vercel", "hosting", "vercel", "#000000")
            )

        # Check Netlify
        if await github_client.check_file_exists(owner, repo, "netlify.toml"):
            technologies.append(
                self._create_tech("Netlify", "hosting", "netlify", "#00C7B7")
            )

        return technologies
