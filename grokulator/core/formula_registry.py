"""
Formula Registry

Manages storage, attachment, and lookup of both legacy and custom formulas
for the Grokulator. Designed to support substantiated reasoning.
"""

from typing import Dict, Any, List, Optional


class FormulaRegistry:
    """
    Stores and manages formulas (legacy and custom) that can be attached
    to symbols in the Grokulator.
    """

    def __init__(self):
        self.formulas: Dict[str, Dict[str, Any]] = {}
        self.symbol_links: Dict[str, List[str]] = {}  # symbol -> list of formula_ids

    def register_formula(
        self,
        formula_id: str,
        name: str,
        expression: str,
        linked_symbols: List[str] = None,
        formula_type: str = "Custom",
        version: str = "0.1",
        notes: str = ""
    ) -> Dict[str, Any]:
        """Register a new formula (legacy or custom)."""
        formula = {
            "id": formula_id,
            "name": name,
            "expression": expression,
            "type": formula_type,
            "version": version,
            "notes": notes
        }
        self.formulas[formula_id] = formula

        if linked_symbols:
            for symbol in linked_symbols:
                if symbol not in self.symbol_links:
                    self.symbol_links[symbol] = []
                if formula_id not in self.symbol_links[symbol]:
                    self.symbol_links[symbol].append(formula_id)

        return formula

    def get_formula(self, formula_id: str) -> Optional[Dict[str, Any]]:
        return self.formulas.get(formula_id)

    def get_formulas_for_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """Return all formulas linked to a specific symbol."""
        formula_ids = self.symbol_links.get(symbol, [])
        return [self.formulas[fid] for fid in formula_ids if fid in self.formulas]

    def get_applicable_formulas(self, symbol: str, formula_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get formulas applicable to a symbol, optionally filtered by type."""
        formulas = self.get_formulas_for_symbol(symbol)
        if formula_type:
            formulas = [f for f in formulas if f.get("type") == formula_type]
        return formulas

    def resolve_formula(self, symbol: str, formula_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Resolve a formula for a symbol.
        If formula_id is provided, return that specific one.
        Otherwise return the first applicable formula.
        """
        if formula_id:
            return self.get_formula(formula_id)
        applicable = self.get_applicable_formulas(symbol)
        return applicable[0] if applicable else None

    def list_all_formulas(self) -> List[Dict[str, Any]]:
        return list(self.formulas.values())

    def link_formula_to_symbol(self, formula_id: str, symbol: str) -> bool:
        """Manually link an existing formula to a symbol."""
        if formula_id not in self.formulas:
            return False
        if symbol not in self.symbol_links:
            self.symbol_links[symbol] = []
        if formula_id not in self.symbol_links[symbol]:
            self.symbol_links[symbol].append(formula_id)
        return True