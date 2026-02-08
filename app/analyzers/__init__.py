from .base import BaseAnalyzer
from .flutter import FlutterAnalyzer
from .javascript import JavaScriptAnalyzer
from .python_fw import PythonAnalyzer
from .rust import RustAnalyzer
from .go import GoAnalyzer
from .devops import DevOpsAnalyzer
from .languages import LanguageAnalyzer

ALL_ANALYZERS = [
    LanguageAnalyzer(),  # Languages first (from GitHub API)
    FlutterAnalyzer(),
    JavaScriptAnalyzer(),
    PythonAnalyzer(),
    RustAnalyzer(),
    GoAnalyzer(),
    DevOpsAnalyzer(),
]

__all__ = [
    "BaseAnalyzer",
    "FlutterAnalyzer",
    "JavaScriptAnalyzer",
    "PythonAnalyzer",
    "RustAnalyzer",
    "GoAnalyzer",
    "DevOpsAnalyzer",
    "LanguageAnalyzer",
    "ALL_ANALYZERS",
]
