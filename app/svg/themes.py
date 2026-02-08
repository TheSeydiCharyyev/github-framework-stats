from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    background: str
    card_background: str
    text_primary: str
    text_secondary: str
    border: str
    accent: str


THEMES = {
    "light": Theme(
        name="light",
        background="#ffffff",
        card_background="#f6f8fa",
        text_primary="#24292f",
        text_secondary="#57606a",
        border="#d0d7de",
        accent="#0969da",
    ),
    "dark": Theme(
        name="dark",
        background="#0d1117",
        card_background="#161b22",
        text_primary="#c9d1d9",
        text_secondary="#8b949e",
        border="#30363d",
        accent="#58a6ff",
    ),
    "dracula": Theme(
        name="dracula",
        background="#282a36",
        card_background="#44475a",
        text_primary="#f8f8f2",
        text_secondary="#6272a4",
        border="#6272a4",
        accent="#bd93f9",
    ),
    "nord": Theme(
        name="nord",
        background="#2e3440",
        card_background="#3b4252",
        text_primary="#eceff4",
        text_secondary="#d8dee9",
        border="#4c566a",
        accent="#88c0d0",
    ),
    "monokai": Theme(
        name="monokai",
        background="#272822",
        card_background="#3e3d32",
        text_primary="#f8f8f2",
        text_secondary="#75715e",
        border="#49483e",
        accent="#a6e22e",
    ),
    "github-dimmed": Theme(
        name="github-dimmed",
        background="#22272e",
        card_background="#2d333b",
        text_primary="#adbac7",
        text_secondary="#768390",
        border="#444c56",
        accent="#539bf5",
    ),
    "solarized-light": Theme(
        name="solarized-light",
        background="#fdf6e3",
        card_background="#eee8d5",
        text_primary="#657b83",
        text_secondary="#93a1a1",
        border="#93a1a1",
        accent="#268bd2",
    ),
    "solarized-dark": Theme(
        name="solarized-dark",
        background="#002b36",
        card_background="#073642",
        text_primary="#839496",
        text_secondary="#586e75",
        border="#586e75",
        accent="#2aa198",
    ),
    "gruvbox-light": Theme(
        name="gruvbox-light",
        background="#fbf1c7",
        card_background="#ebdbb2",
        text_primary="#3c3836",
        text_secondary="#665c54",
        border="#bdae93",
        accent="#d65d0e",
    ),
    "gruvbox-dark": Theme(
        name="gruvbox-dark",
        background="#282828",
        card_background="#3c3836",
        text_primary="#ebdbb2",
        text_secondary="#a89984",
        border="#504945",
        accent="#fe8019",
    ),
    "one-dark": Theme(
        name="one-dark",
        background="#282c34",
        card_background="#21252b",
        text_primary="#abb2bf",
        text_secondary="#5c6370",
        border="#3e4451",
        accent="#61afef",
    ),
    "tokyo-night": Theme(
        name="tokyo-night",
        background="#1a1b26",
        card_background="#24283b",
        text_primary="#c0caf5",
        text_secondary="#565f89",
        border="#414868",
        accent="#7aa2f7",
    ),
    "catppuccin": Theme(
        name="catppuccin",
        background="#1e1e2e",
        card_background="#313244",
        text_primary="#cdd6f4",
        text_secondary="#a6adc8",
        border="#45475a",
        accent="#cba6f7",
    ),
    "synthwave": Theme(
        name="synthwave",
        background="#262335",
        card_background="#34294f",
        text_primary="#f4eee4",
        text_secondary="#9d8bca",
        border="#495495",
        accent="#ff7edb",
    ),
    "rose-pine": Theme(
        name="rose-pine",
        background="#191724",
        card_background="#1f1d2e",
        text_primary="#e0def4",
        text_secondary="#908caa",
        border="#403d52",
        accent="#ebbcba",
    ),
    "ayu-dark": Theme(
        name="ayu-dark",
        background="#0b0e14",
        card_background="#11151c",
        text_primary="#bfbdb6",
        text_secondary="#565b66",
        border="#1c212b",
        accent="#e6b450",
    ),
    "cobalt": Theme(
        name="cobalt",
        background="#193549",
        card_background="#15232d",
        text_primary="#ffffff",
        text_secondary="#6688aa",
        border="#1f4662",
        accent="#ffc600",
    ),
    "oceanic": Theme(
        name="oceanic",
        background="#1b2b34",
        card_background="#253840",
        text_primary="#cdd3de",
        text_secondary="#65737e",
        border="#4f5b66",
        accent="#6699cc",
    ),
    "night-owl": Theme(
        name="night-owl",
        background="#011627",
        card_background="#0b2942",
        text_primary="#d6deeb",
        text_secondary="#637777",
        border="#1d3b53",
        accent="#82aaff",
    ),
}


def get_theme(name: str) -> Theme:
    """Get theme by name, defaults to light."""
    return THEMES.get(name, THEMES["light"])
