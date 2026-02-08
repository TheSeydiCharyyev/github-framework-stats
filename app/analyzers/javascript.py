import json
from .base import BaseAnalyzer, Technology


class JavaScriptAnalyzer(BaseAnalyzer):
    """Analyzer for JavaScript/TypeScript projects."""

    @property
    def files_to_check(self) -> list[str]:
        return ["package.json"]

    async def analyze(
        self,
        owner: str,
        repo: str,
        github_client,
    ) -> list[Technology]:
        technologies = []

        content = await github_client.get_file_content(owner, repo, "package.json")
        if not content:
            return technologies

        try:
            pkg = json.loads(content)
        except json.JSONDecodeError:
            return technologies

        deps = {}
        deps.update(pkg.get("dependencies", {}))
        deps.update(pkg.get("devDependencies", {}))

        # Frontend frameworks
        if "react" in deps:
            technologies.append(
                self._create_tech("React", "framework", "react", "#61DAFB")
            )

        if "react-native" in deps:
            technologies.append(
                self._create_tech("React Native", "framework", "react", "#61DAFB")
            )

        if "next" in deps:
            technologies.append(
                self._create_tech("Next.js", "framework", "nextjs", "#000000")
            )

        if "vue" in deps:
            technologies.append(
                self._create_tech("Vue.js", "framework", "vue", "#4FC08D")
            )

        if "nuxt" in deps:
            technologies.append(
                self._create_tech("Nuxt", "framework", "nuxt", "#00DC82")
            )

        if "@angular/core" in deps:
            technologies.append(
                self._create_tech("Angular", "framework", "angular", "#DD0031")
            )

        if "svelte" in deps:
            technologies.append(
                self._create_tech("Svelte", "framework", "svelte", "#FF3E00")
            )

        # Backend frameworks
        if "express" in deps:
            technologies.append(
                self._create_tech("Express", "backend", "express", "#000000")
            )

        if "fastify" in deps:
            technologies.append(
                self._create_tech("Fastify", "backend", "fastify", "#000000")
            )

        if "nest" in deps or "@nestjs/core" in deps:
            technologies.append(
                self._create_tech("NestJS", "backend", "nestjs", "#E0234E")
            )

        # Build tools
        if "typescript" in deps:
            technologies.append(
                self._create_tech("TypeScript", "language", "typescript", "#3178C6")
            )

        if "vite" in deps:
            technologies.append(
                self._create_tech("Vite", "build", "vite", "#646CFF")
            )

        if "webpack" in deps:
            technologies.append(
                self._create_tech("Webpack", "build", "webpack", "#8DD6F9")
            )

        # Testing
        if "jest" in deps:
            technologies.append(
                self._create_tech("Jest", "testing", "jest", "#C21325")
            )

        if "vitest" in deps:
            technologies.append(
                self._create_tech("Vitest", "testing", "vitest", "#6E9F18")
            )

        # State management
        if "redux" in deps or "@reduxjs/toolkit" in deps:
            technologies.append(
                self._create_tech("Redux", "state", "redux", "#764ABC")
            )

        if "zustand" in deps:
            technologies.append(
                self._create_tech("Zustand", "state", "zustand", "#433D3C")
            )

        # Styling
        if "tailwindcss" in deps:
            technologies.append(
                self._create_tech("Tailwind CSS", "styling", "tailwind", "#06B6D4")
            )

        # Additional frameworks
        if "remix" in deps or "@remix-run/react" in deps:
            technologies.append(
                self._create_tech("Remix", "framework", "remix", "#000000")
            )

        if "astro" in deps:
            technologies.append(
                self._create_tech("Astro", "framework", "astro", "#FF5D01")
            )

        if "gatsby" in deps:
            technologies.append(
                self._create_tech("Gatsby", "framework", "gatsby", "#663399")
            )

        if "electron" in deps:
            technologies.append(
                self._create_tech("Electron", "framework", "electron", "#47848F")
            )

        if "solid-js" in deps:
            technologies.append(
                self._create_tech("SolidJS", "framework", "solid", "#2C4F7C")
            )

        # Database & API
        if "prisma" in deps or "@prisma/client" in deps:
            technologies.append(
                self._create_tech("Prisma", "database", "prisma", "#2D3748")
            )

        if "graphql" in deps or "@apollo/client" in deps:
            technologies.append(
                self._create_tech("GraphQL", "api", "graphql", "#E10098")
            )

        if "axios" in deps:
            technologies.append(
                self._create_tech("Axios", "http", "axios", "#5A29E4")
            )

        if "socket.io" in deps or "socket.io-client" in deps:
            technologies.append(
                self._create_tech("Socket.io", "realtime", "socketio", "#010101")
            )

        # Styling libraries
        if "styled-components" in deps:
            technologies.append(
                self._create_tech("Styled Components", "styling", "styled", "#DB7093")
            )

        if "@emotion/react" in deps or "@emotion/styled" in deps:
            technologies.append(
                self._create_tech("Emotion", "styling", "emotion", "#D36AC2")
            )

        if "@mui/material" in deps or "@material-ui/core" in deps:
            technologies.append(
                self._create_tech("MUI", "ui", "mui", "#007FFF")
            )

        if "@chakra-ui/react" in deps:
            technologies.append(
                self._create_tech("Chakra UI", "ui", "chakra", "#319795")
            )

        # Others
        if "three" in deps:
            technologies.append(
                self._create_tech("Three.js", "graphics", "threejs", "#000000")
            )

        if "@trpc/client" in deps or "@trpc/server" in deps:
            technologies.append(
                self._create_tech("tRPC", "api", "trpc", "#2596BE")
            )

        return technologies
