 """
Discordance Handler

Treats discordance as a productive signal for model refinement
rather than simple error detection.
"""

from typing import Dict, Any, List


class DiscordanceHandler:
    """Handles and evaluates discordance events."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def register(
        self, 
        original_claim: str, 
        new_evidence: str, 
        strength: float = 0.5
    ) -> Dict[str, Any]:
        """Register a discordance event."""
        event = {
            "original_claim": original_claim,
            "new_evidence": new_evidence,
            "strength": strength,
            "status": "registered"
        }
        self.events.append(event)
        return event

    def evaluate(self, event: Dict[str, Any]) -> str:
        """Suggest action based on discordance strength."""
        if event["strength"] > 0.7:
            return "strong_refinement_recommended"
        elif event["strength"] > 0.4:
            return "review_suggested"
        return "monitor"