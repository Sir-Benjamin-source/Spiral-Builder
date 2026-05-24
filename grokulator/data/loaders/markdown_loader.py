from typing import Dict, Any

from .base_loader import BaseLoader


class MarkdownLoader(BaseLoader):
    """Basic Markdown loader for Grokulator symbolic data.

    Note: Full structured Markdown table parsing will be implemented later.
    This currently returns metadata only."""

    def supports(self, source: str) -> bool:
        return source.lower().endswith(".md") or source.lower().endswith(".markdown")

    def load(self, source: str) -> Dict[str, Any]:
        return {
            "_source": source,
            "_format": "markdown",
            "_note": "Markdown parsing not yet fully implemented"
        }