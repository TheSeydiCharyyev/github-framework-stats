# Mapping from tech icon name to devicon name
# Format: "our_icon": "devicon_name" or "our_icon": ("devicon_name", "variant")
# Default variant is "original", alternatives: "plain", "line"

DEVICON_MAP = {
    # Languages
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "java": "java",
    "kotlin": "kotlin",
    "swift": "swift",
    "go": "go",
    "rust": "rust",
    "c": "c",
    "cpp": "cplusplus",
    "csharp": "csharp",
    "ruby": "ruby",
    "php": "php",
    "dart": "dart",
    "scala": "scala",
    "elixir": "elixir",
    "haskell": "haskell",
    "lua": "lua",
    "perl": "perl",
    "r": "r",
    "shell": "bash",
    "powershell": "powershell",
    "html": "html5",
    "css": "css3",
    "scss": "sass",
    "jupyter-notebook": "jupyter",
    "objective-c": "objectivec",
    "groovy": "groovy",
    "clojure": "clojure",
    "fsharp": "fsharp",
    "ocaml": "ocaml",
    "erlang": "erlang",
    "zig": "zig",
    "julia": "julia",
    "matlab": "matlab",
    "solidity": "solidity",

    # Frontend Frameworks
    "react": "react",
    "vue": "vuejs",
    "angular": "angularjs",
    "svelte": "svelte",
    "nextjs": "nextjs",
    "nuxt": "nuxtjs",
    "gatsby": "gatsby",
    "remix": "remix",
    "astro": "astro",
    "solid": "solidjs",
    "electron": "electron",

    # Backend Frameworks
    "express": "express",
    "nestjs": "nestjs",
    "fastify": "fastify",
    "django": "django",
    "flask": "flask",
    "fastapi": "fastapi",
    "rails": "rails",
    "laravel": "laravel",
    "spring": "spring",

    # Flutter/Dart
    "flutter": "flutter",
    "firebase": "firebase",

    # Databases
    "postgresql": "postgresql",
    "mysql": "mysql",
    "mongodb": "mongodb",
    "redis": "redis",
    "sqlite": "sqlite",
    "prisma": "prisma",
    "sqlalchemy": "sqlalchemy",

    # DevOps
    "docker": "docker",
    "kubernetes": "kubernetes",
    "github-actions": "githubactions",
    "gitlab": "gitlab",
    "jenkins": "jenkins",
    "terraform": "terraform",
    "ansible": "ansible",
    "nginx": "nginx",
    "apache": "apache",
    "aws": "amazonwebservices",
    "azure": "azure",
    "gcp": "googlecloud",
    "vercel": "vercel",
    "netlify": "netlify",
    "heroku": "heroku",

    # Build Tools
    "webpack": "webpack",
    "vite": "vitejs",
    "babel": "babel",
    "npm": "npm",
    "yarn": "yarn",
    "gradle": "gradle",
    "maven": "maven",

    # Testing
    "jest": "jest",
    "pytest": "pytest",
    "mocha": "mocha",

    # State Management
    "redux": "redux",

    # Styling
    "tailwind": "tailwindcss",
    "bootstrap": "bootstrap",
    "sass": "sass",
    "styled": "css3",  # No specific icon, use CSS
    "mui": "materialui",

    # Other
    "graphql": "graphql",
    "nodejs": "nodejs",
    "deno": "denojs",
    "bun": "bun",
    "threejs": "threejs",
    "socketio": "socketio",
    "pandas": "pandas",
    "numpy": "numpy",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "opencv": "opencv",
    "figma": "figma",
    "git": "git",
    "github": "github",
    "vscode": "vscode",
    "vim": "vim",
    "linux": "linux",
    "ubuntu": "ubuntu",
    "debian": "debian",
    "windows": "windows8",
    "apple": "apple",
    "android": "android",
}

# Icons that need "plain" variant instead of "original"
PLAIN_VARIANTS = {
    "express", "nextjs", "github", "githubactions", "vercel"
}

DEVICON_CDN = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons"


def get_icon_url(icon_name: str) -> str:
    """Get devicon CDN URL for a technology icon."""
    devicon_name = DEVICON_MAP.get(icon_name.lower())

    if not devicon_name:
        return ""

    variant = "plain" if devicon_name in PLAIN_VARIANTS else "original"
    return f"{DEVICON_CDN}/{devicon_name}/{devicon_name}-{variant}.svg"
