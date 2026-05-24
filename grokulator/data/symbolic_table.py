 """
Symbolic Table

Manages loading and access to the Grokulator's Symbolic Elements Table.
Supports multiple formats via loader plugins (JSON, Markdown, .srec, spreadsheet).
"""

from typing import Dict, Any, Optional

import json

try:
    from .loaders import get_loader
except ImportError:
    get_loader = None


class SymbolicTable:
    """Loads and provides access to the symbolic elements table."""

    def __init__(self):
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.source: Optional[str] = None
        self.format: Optional[str] = None

    def load(self, source: str, format_hint: Optional[str] = None):
        """Load from a file path or source, auto-detecting format when possible."""
        self.source = source

        if get_loader:
            loader = get_loader(source, format_hint)
            if loader:
                self.symbols = loader.load(source)
                self.format = getattr(loader, "__class__", type(loader)).__name__
                return

        # Fallback basic support
        if source.lower().endswith(".json"):
            with open(source, "r", encoding="utf-8") as f:
                self.symbols = json.load(f)
            self.format = "json"
        else:
            self.symbols = {"_source": source, "_warning": "No suitable loader found"}
            self.format = "unknown"

    def get(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self.symbols.get(symbol)

    def list_symbols(self) -> list:
        return list(self.symbols.keys())