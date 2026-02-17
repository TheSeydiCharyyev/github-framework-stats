import math
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..analyzers.base import Technology
from .themes import Theme, get_theme
from .styles import Style, STYLES
from .icons import get_icon_url, get_icon_data_uri


CATEGORY_LABELS = {
    "language": "Language",
    "framework": "Framework",
    "runtime": "Runtime",
    "devops": "DevOps",
    "database": "Database",
    "ci": "CI/CD",
    "iac": "IaC",
    "hosting": "Hosting",
    "styling": "Styling",
    "build": "Build",
    "testing": "Testing",
    "state": "State Mgmt",
    "backend": "Backend",
    "api": "API",
    "http": "HTTP",
    "realtime": "Realtime",
    "ui": "UI",
    "graphics": "Graphics",
    "data": "Data",
    "ml": "ML",
    "validation": "Validation",
    "scraping": "Scraping",
    "server": "Server",
    "storage": "Storage",
    "routing": "Routing",
    "codegen": "Codegen",
    "mobile": "Mobile",
}

CATEGORY_COLORS = {
    "language": "#f1e05a",
    "framework": "#61dafb",
    "runtime": "#bc8cff",
    "devops": "#f0883e",
    "database": "#3fb950",
    "ci": "#539bf5",
    "iac": "#d2a8ff",
    "hosting": "#f778ba",
    "styling": "#e377c2",
    "build": "#ff7b72",
    "testing": "#d29922",
    "state": "#8b949e",
    "backend": "#da3633",
    "api": "#56d4dd",
    "http": "#79c0ff",
    "realtime": "#7ee787",
    "ui": "#ffa657",
    "graphics": "#d2a8ff",
    "data": "#ff9bce",
    "ml": "#a371f7",
    "validation": "#ffd33d",
    "scraping": "#9ecbff",
    "server": "#f85149",
    "storage": "#3fb950",
    "routing": "#79c0ff",
    "codegen": "#b392f0",
    "mobile": "#56d4dd",
}


class SVGGenerator:
    """Generate SVG images from technology data."""

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=True,
        )
        self.env.globals["math"] = math
        self.env.globals["get_icon_url"] = get_icon_url
        self.env.globals["get_icon_data_uri"] = get_icon_data_uri

    def generate(
        self,
        technologies: list[Technology],
        username: str,
        theme_name: str = "light",
        style_name: str = "card",
        columns: int = None,
    ) -> str:
        """Generate SVG for given technologies.

        Args:
            technologies: List of detected technologies
            username: GitHub username
            theme_name: Theme name
            style_name: Style name (card, badges, grid, pie)
            columns: Number of columns (None = auto)
        """
        theme = get_theme(theme_name)
        style = STYLES.get(style_name, STYLES["card"])

        # Aggregate technologies by name
        tech_map: dict[str, Technology] = {}
        for tech in technologies:
            if tech.name in tech_map:
                tech_map[tech.name].count += tech.count
            else:
                tech_map[tech.name] = Technology(
                    name=tech.name,
                    category=tech.category,
                    icon=tech.icon,
                    color=tech.color,
                    count=tech.count,
                )

        # Sort by count (descending)
        sorted_techs = sorted(tech_map.values(), key=lambda t: t.count, reverse=True)

        # Calculate dimensions
        num_items = len(sorted_techs)
        if num_items == 0:
            return self._generate_empty(username, theme, style)

        # Calculate max_count and category summary
        max_count = max((t.count for t in sorted_techs), default=1)

        cat_counts: dict[str, int] = {}
        for tech in sorted_techs:
            cat_counts[tech.category] = cat_counts.get(tech.category, 0) + 1

        category_summary = []
        for cat, cnt in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
            category_summary.append({
                "key": cat,
                "label": CATEGORY_LABELS.get(cat, cat.replace("-", " ").title()),
                "color": CATEGORY_COLORS.get(cat, "#8b949e"),
                "count": cnt,
            })

        # Calculate adaptive columns
        if columns is not None:
            actual_columns = max(1, min(columns, 10))  # Limit 1-10
        else:
            actual_columns = self._calculate_columns(num_items, style)

        rows = math.ceil(num_items / actual_columns)
        width = (
            style.padding * 2
            + actual_columns * style.item_width
            + (actual_columns - 1) * style.gap
        )
        header_space = 70 if style.name == "card" else 40
        height = (
            style.padding * 2
            + rows * style.item_height
            + (rows - 1) * style.gap
            + header_space
        )

        # Create modified style with actual columns
        actual_style = Style(
            name=style.name,
            template=style.template,
            columns=actual_columns,
            item_width=style.item_width,
            item_height=style.item_height,
            padding=style.padding,
            gap=style.gap,
        )

        # Load and render template
        template = self.env.get_template(style.template)
        total_count = sum(t.count for t in sorted_techs)
        return template.render(
            technologies=sorted_techs,
            username=username,
            theme=theme,
            style=actual_style,
            width=width,
            height=height,
            rows=rows,
            max_count=max_count,
            total_count=total_count,
            category_labels=CATEGORY_LABELS,
            category_colors=CATEGORY_COLORS,
            category_summary=category_summary,
        )

    def _calculate_columns(self, num_items: int, style: Style) -> int:
        """Calculate optimal number of columns based on item count."""
        default = style.columns

        # For pie chart, always 1 column
        if style.name == "pie":
            return 1

        # Adaptive logic
        if num_items <= 2:
            return min(num_items, default)
        elif num_items <= 4:
            return min(4, default)
        elif num_items <= 6:
            return min(3, default) if style.name == "card" else min(6, default)
        elif num_items <= 9:
            return min(3, default) if style.name == "card" else default
        else:
            return default

    def _generate_empty(
        self, username: str, theme: Theme, style: Style
    ) -> str:
        """Generate empty state SVG."""
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120">
  <rect width="100%" height="100%" fill="{theme.background}" rx="8"/>
  <text x="200" y="50" text-anchor="middle" fill="{theme.text_primary}" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600">
    @{username}
  </text>
  <text x="200" y="80" text-anchor="middle" fill="{theme.text_secondary}" font-family="system-ui, -apple-system, sans-serif" font-size="12">
    No technologies detected
  </text>
</svg>'''

    def generate_pie_data(
        self, technologies: list[Technology]
    ) -> list[dict]:
        """Calculate pie chart segments."""
        total = sum(t.count for t in technologies)
        if total == 0:
            return []

        segments = []
        start_angle = 0

        for tech in technologies:
            percentage = tech.count / total
            angle = percentage * 360
            segments.append({
                "tech": tech,
                "percentage": percentage * 100,
                "start_angle": start_angle,
                "end_angle": start_angle + angle,
            })
            start_angle += angle

        return segments
