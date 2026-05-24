 """
Symbolic Table

Manages loading and access to the Grokulator's Symbolic Elements Table.
"""

from typing import Dict, Any, Optional
import json


class SymbolicTable:
    """Loads and provides access to the symbolic elements table."""

    def __init__(self):
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.source: Optional[str] = None

    def load_from_dict(self, data: Dict[str, Any], source: str = "memory"):
        self.symbols = data
        self.source = source

    def load_from_json(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.load_from_dict(data, source=path)

    def get(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self.symbols.get(symbol)

    def list_symbols(self) -> list:
        return list(self.symbols.keys())