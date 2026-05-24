import json
from typing import Dict, Any

from .base_loader import BaseLoader


class JSONLoader(BaseLoader):
    """Loads Grokulator symbolic data from JSON files."""

    def supports(self, source: str) -> bool:
        return source.lower().endswith(".json")

    def load(self, source: str) -> Dict[str, Any]:
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)