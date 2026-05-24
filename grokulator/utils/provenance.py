 """
Provenance Tracker

Lightweight provenance tracking for Grokulator reasoning steps.
"""

from typing import Dict, Any, List
from datetime import datetime


class ProvenanceTracker:
    """Tracks reasoning steps for auditability and falsifiability."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def log(
        self, 
        step_type: str, 
        symbol: str = None, 
        formula: str = None, 
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step_type": step_type,
            "symbol": symbol,
            "formula": formula,
            "details": details or {}
        }
        self.history.append(entry)
        return entry

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def clear(self):
        self.history = []