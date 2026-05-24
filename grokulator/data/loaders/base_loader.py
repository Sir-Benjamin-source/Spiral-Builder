from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLoader(ABC):
    """Abstract base class for Grokulator data loaders."""

    @abstractmethod
    def load(self, source: str) -> Dict[str, Any]:
        """Load symbolic table data from a source."""
        pass

    @abstractmethod
    def supports(self, source: str) -> bool:
        """Return True if this loader supports the given source."""
        pass