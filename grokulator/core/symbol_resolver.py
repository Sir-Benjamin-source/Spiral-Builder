 """
Symbol Resolver

Resolves symbols from the Grokulator Symbolic Elements Table with
clear support for falsifiability and provenance.
"""

from typing import Dict, Any, Optional


class SymbolResolver:
    """Resolves symbols and their associated constraints."""

    def __init__(self, table: Optional[Dict[str, Any]] = None):
        self.table = table or {}

    def resolve(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return the definition and constraints for a symbol, or None."""
        return self.table.get(symbol)

    def get_constraints(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return only the constraints for a given symbol."""
        data = self.resolve(symbol)
        return data.get("constraints") if data else None