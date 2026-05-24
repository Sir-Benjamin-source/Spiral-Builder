 """
Discordance Handler

Handles situations where new information challenges existing models.
Designed to treat discordance as a productive signal for refinement
rather than simple error detection.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class DiscordanceEvent:
    """Represents a single discordance event."""

    def __init__(
        self,
        original_claim: str,
        new_evidence: str,
        strength: float = 0.5,
        context: Optional[Dict[str, Any]] = None
    ):
        self.original_claim = original_claim
        self.new_evidence = new_evidence
        self.strength = max(0.0, min(1.0, strength))  # Clamp between 0 and 1
        self.context = context or {}
        self.timestamp = datetime.utcnow().isoformat()
        self.status = "registered"
        self.suggested_action = self._determine_action()

    def _determine_action(self) -> str:
        if self.strength > 0.75:
            return "strong_refinement_recommended"
        elif self.strength > 0.5:
            return "review_and_refine"
        elif self.strength > 0.3:
            return "monitor_and_evaluate"
        else:
            return "low_priority"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_claim": self.original_claim,
            "new_evidence": self.new_evidence,
            "strength": self.strength,
            "status": self.status,
            "suggested_action": self.suggested_action,
            "timestamp": self.timestamp,
            "context": self.context
        }


class DiscordanceHandler:
    """
    Manages discordance events and supports productive model refinement.

    Core philosophy: New information that conflicts with existing models
    should be evaluated for its potential to strengthen descriptions.
    """

    def __init__(self):
        self.events: List[DiscordanceEvent] = []

    def register_discordance(
        self,
        original_claim: str,
        new_evidence: str,
        strength: float = 0.5,
        context: Optional[Dict[str, Any]] = None
    ) -> DiscordanceEvent:
        """Register a new discordance event."""
        event = DiscordanceEvent(
            original_claim=original_claim,
            new_evidence=new_evidence,
            strength=strength,
            context=context
        )
        self.events.append(event)
        return event

    def get_events_by_action(self, action: str) -> List[DiscordanceEvent]:
        """Return all events suggesting a specific action."""
        return [e for e in self.events if e.suggested_action == action]

    def get_high_impact_events(self, threshold: float = 0.6) -> List[DiscordanceEvent]:
        """Return events above a certain strength threshold."""
        return [e for e in self.events if e.strength >= threshold]

    def summarize(self) -> Dict[str, Any]:
        """Return a summary of current discordance state."""
        if not self.events:
            return {"total_events": 0, "status": "no_discordance"}

        actions = {}
        for event in self.events:
            actions[event.suggested_action] = actions.get(event.suggested_action, 0) + 1

        return {
            "total_events": len(self.events),
            "high_impact_count": len(self.get_high_impact_events()),
            "action_breakdown": actions,
            "latest_event": self.events[-1].to_dict() if self.events else None
        }