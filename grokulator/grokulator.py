 """
Grokulator

Lightweight orchestrator / facade for the Grokulator symbolic reasoning substrate.

Designed as a high-quality utility layer (not the main reasoning engine).
Provides clean access to symbols, formulas, discordance tracking, and provenance.
"""

from typing import Dict, Any, Optional, List

try:
    from .core.symbol_resolver import SymbolResolver
    from .core.formula_registry import FormulaRegistry
    from .core.discordance_handler import DiscordanceHandler
    from .data.symbolic_table import SymbolicTable
    from .utils.provenance import ProvenanceTracker
except ImportError:
    # Allow running as standalone for testing
    SymbolResolver = None
    FormulaRegistry = None
    DiscordanceHandler = None
    SymbolicTable = None
    ProvenanceTracker = None


class Grokulator:
    """
    Main entry point for the Grokulator utility.

    Wires together:
    - SymbolicTable (multi-format data)
    - SymbolResolver (with formula awareness)
    - FormulaRegistry
    - DiscordanceHandler
    - ProvenanceTracker

    Provides a clean, defensive interface for other systems to use.
    """

    def __init__(self, table_source: Optional[str] = None):
        self.table = SymbolicTable() if SymbolicTable else None
        self.resolver = SymbolResolver() if SymbolResolver else None
        self.formulas = FormulaRegistry() if FormulaRegistry else None
        self.discordance = DiscordanceHandler() if DiscordanceHandler else None
        self.provenance = ProvenanceTracker() if ProvenanceTracker else None

        if table_source and self.table:
            self.table.load(table_source)

        # Wire components together
        if self.resolver:
            if self.table:
                self.resolver.set_table(self.table)
            if self.formulas:
                self.resolver.set_formula_registry(self.formulas)

    def resolve(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Resolve a symbol with full data."""
        if self.resolver:
            result = self.resolver.resolve_with_formulas(symbol)
            if self.provenance:
                self.provenance.log("resolve", symbol=symbol)
            return result
        return None

    def resolve_formula(self, symbol: str, formula_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Resolve and return a usable formula for a symbol."""
        if self.resolver and self.formulas:
            resolved = self.resolver.resolve_with_formulas(symbol)
            formulas = resolved.get("formulas", [])
            if formula_id:
                return self.formulas.get_formula(formula_id)
            return formulas[0] if formulas else None
        return None

    def register_discordance(
        self,
        original_claim: str,
        new_evidence: str,
        strength: float = 0.5,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Register a discordance event and log it."""
        if self.discordance:
            event = self.discordance.register_discordance(
                original_claim=original_claim,
                new_evidence=new_evidence,
                strength=strength,
                context=context
            )
            if self.provenance:
                self.provenance.log("discordance", details={"claim": original_claim, "strength": strength})
            return event
        return None

    def get_discordance_summary(self) -> Dict[str, Any]:
        if self.discordance and hasattr(self.discordance, "summarize"):
            return self.discordance.summarize()
        return {"status": "no_discordance_handler"}

    def get_provenance_history(self) -> List[Dict[str, Any]]:
        if self.provenance:
            return self.provenance.get_history()
        return []

    def validate(self, symbol: str, value: Any) -> Dict[str, Any]:
        """Validate a value against a symbol's constraints."""
        if self.resolver:
            return self.resolver.validate_against_constraints(symbol, value)
        return {"valid": False, "error": "No resolver available"}