from dataclasses import dataclass


@dataclass
class Style:
    name: str
    template: str
    columns: int
    item_width: int
    item_height: int
    padding: int
    gap: int


STYLES = {
    "card": Style(
        name="card",
        template="card.svg.jinja2",
        columns=3,
        item_width=150,
        item_height=140,
        padding=24,
        gap=16,
    ),
    "badges": Style(
        name="badges",
        template="badges.svg.jinja2",
        columns=6,
        item_width=80,
        item_height=28,
        padding=15,
        gap=8,
    ),
    "grid": Style(
        name="grid",
        template="grid.svg.jinja2",
        columns=5,
        item_width=60,
        item_height=60,
        padding=15,
        gap=10,
    ),
    "pie": Style(
        name="pie",
        template="pie.svg.jinja2",
        columns=1,
        item_width=400,
        item_height=400,
        padding=20,
        gap=0,
    ),
}


def get_style(name: str) -> Style:
    """Get style by name, defaults to card."""
    return STYLES.get(name, STYLES["card"])
