 """
Grokulator

A living symbolic reasoning substrate for the Spiral Codex ecosystem.

Core focus:
- Falsifiability
- Productive handling of discordance
- Substantiated, traceable reasoning
"""

from .core.symbol_resolver import SymbolResolver
from .core.discordance_handler import DiscordanceHandler
from .core.formula_registry import FormulaRegistry
from .data.symbolic_table import SymbolicTable
from .utils.provenance import ProvenanceTracker

__version__ = "0.1.0"

__all__ = [
    "SymbolResolver",
    "DiscordanceHandler",
    "FormulaRegistry",
    "SymbolicTable",
    "ProvenanceTracker",
]