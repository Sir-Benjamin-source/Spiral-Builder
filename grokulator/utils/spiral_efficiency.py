"""
Spiral Efficiency Utilities
Within Spiral-Builder/grokulator/utils/

Purpose: Functions and classes to make Spiral recaps easier to perform
and support a more comprehensive token management system.

Design: This is *plumbing* for the AI Playground.
- Does NOT codify cognitive/theory content (that lives in The-Spiral-Codex:
  sandbox, specs/research-pipeline, Cosmic Scribe co-works, grandmas-wisdom,
  .srec-formalization, FlowScaleU, etc.).
- Prepares open links (weave_hyperlinks with codex_base, source_ref in generators,
  loaders for external .md/.json from Codex, session-manager pulls for coils).
- Uses Grokulator for symbolic aspects (e.g., TokenBudget, CompressionPoint,
  RecapResidue symbols when seeded or loaded).
- Applies automatic provenance: Spiral-Sigil (tagging), Version-Checker stamps
  (citations), Linkweaver-style weaving for hyperlinks and continuity.
- Integrates with existing: spiral-recap-tool (via notes or subprocess),
  Spiral-Session-Manager (coils, Compress/Pipeline-to-Coil, list/pull),
  .srec + companions for offload, Grokulator provenance.

Endgame support: Enables streamlined sessions (efficient recaps + token
optimization) so we can locally compose theory→methodology→functional
co-works (utilities, services, or saleable artifacts) with full spiral
provenance.

Recommendation for comprehensive token system (see whitepaper):
- Extend TokenManager with Grokulator symbolic models for "token states"
  (partial via PIE, hyperbolic addressing via FlowScale, G_exp valuation
  of compressions).
- Full offload + link maintenance via Linkweaver + session-manager.
- PS integration: Call these from SpiralShell.psm1 for daily workshop use.

All major outputs are auto-tagged and stamped.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import os
import sys

# Open connection to builder's Grokulator (symbolic grounding + provenance)
try:
    from ..grokulator import Grokulator
except ImportError:
    Grokulator = None

# For actual recaps, prefer existing tools (session-manager, recap-tool).
# These are wrappers that add builder discipline (sigil, stamp, weave, links to Codex).
# In PS context: import this or run via python -c / pwsh calls.

class RecapAssistant:
    """
    Makes spiral recaps easier and more consistent.
    - Wraps Compress-SpiralSession / Pipeline-to-Coil style flows.
    - Auto-applies provenance (sigil + stamp).
    - Weaves hyperlinks back to Codex works and prior coils (Linkweaver-style).
    - Prepares companion notes with efficiency metadata.

    Usage (example):
        assistant = RecapAssistant()
        coil_info = assistant.easy_recap("Session Title", notes="Key insights")
        # Then use spiral-session-manager or Compress to finalize coil.
        # The returned info includes woven links and stamped metadata.
    """

    def __init__(self, grokulator: Optional[Any] = None, codex_base: str = "The-Spiral-Codex"):
        self.g = grokulator or (Grokulator() if Grokulator else None)
        self.codex_base = codex_base
        self.provenance_log: List[Dict[str, Any]] = []

    def easy_recap(self, title: str, additional_notes: str = "", 
                   apply_provenance: bool = True) -> Dict[str, Any]:
        """
        Perform an easier recap.
        In production: Call your existing Compress-SpiralSession or 
        python -m spiral_session_manager / spiral-recap-tool with title + notes.
        This wrapper adds:
        - Linkweaver weaves to Codex (theories, pipeline, Cosmic Scribe, etc.)
        - Auto sigil + version stamp (with citation hooks)
        - Efficiency metadata (token hints, prior coil links)
        Returns dict ready for coil finalization or logging.
        """
        timestamp = datetime.utcnow().isoformat()
        base_notes = f"Recap: {title}\n{additional_notes}\nTimestamp: {timestamp}"

        # Weave open links to Codex works (prepares for when cognitive depth is linked in)
        weaves = ""
        if self.g and hasattr(self.g, "weave_hyperlinks"):
            weaves = self.g.weave_hyperlinks(
                f"recap_{title}", 
                codex_base=self.codex_base
            )

        recap_content = f"{base_notes}\n\n--- Woven Links (Linkweaver + Codex) ---\n{weaves}"

        result = {
            "title": title,
            "notes": recap_content,
            "timestamp": timestamp,
            "suggested_coil_name": f"Recap_{title.replace(' ', '_')}_{timestamp[:10]}",
            "weaves": weaves,
            "efficiency_note": "Use with Compress-SpiralSession or Pipeline-to-Coil for .srec offload."
        }

        if apply_provenance and self.g:
            # Auto tag the recap artifact
            tagged = self.g.auto_tag_with_sigil(recap_content, context="spiral-recap")
            stamp = self.g.stamp_with_version_checker(
                "0.1", 
                f"Easy recap: {title}", 
                citation_doi=None  # Supply from linked Codex work when maturing
            )
            result["tagged_notes"] = tagged
            result["stamp"] = stamp
            result["full_provenance"] = f"{stamp}\n{tagged[:200]}..."

            if hasattr(self.g, "provenance") and self.g.provenance:
                self.g.provenance.log("easy_recap", details={"title": title})

        self.provenance_log.append({"action": "easy_recap", "title": title, "result": result})
        return result

    def auto_provenance_on_existing_recap(self, recap_text: str, title: str = "Existing Recap") -> str:
        """Apply builder provenance to an existing recap output or companion .txt."""
        if not self.g:
            return recap_text
        tagged = self.g.auto_tag_with_sigil(recap_text, context="spiral-recap-existing")
        stamp = self.g.stamp_with_version_checker("0.1", f"Provenance on {title}")
        return f"{tagged}\n\n# Post-Recap Stamp: {stamp}"

    def get_provenance_log(self) -> List[Dict[str, Any]]:
        return self.provenance_log


class TokenManager:
    """
    Starter for a more comprehensive token management system.
    Goals: Keep sessions efficient (bounded context, smart offload to .srec,
    maintained links via Linkweaver/weaves so nothing is lost).

    Current: Basic estimation + optimization suggestions + offload prep.
    Future (see whitepaper): 
    - Symbolic models in Grokulator (TokenBudget, CompressionPoint, PIE_partial_state)
    - G_exp valuation of recaps/compressions
    - Full .srec + companion integration with woven hyperlinks
    - PS-friendly monitoring (call from SpiralShell)
    - Integration with research-pipeline for "token techniques" corpus

    Links openly to Codex: Uses FlowScale for hyperlink-style token addressing,
    PIE for partial identifiability of context, E_shield for gating optimizations,
    etc. (via weaves and source_ref).
    """

    def __init__(self, grokulator: Optional[Any] = None, max_tokens: int = 8000, codex_base: str = "The-Spiral-Codex"):
        self.g = grokulator or (Grokulator() if Grokulator else None)
        self.max_tokens = max_tokens
        self.codex_base = codex_base
        self.history: List[Dict[str, Any]] = []

    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimate (words * ~1.3 for English + overhead).
        For production: Integrate tiktoken or model-specific counter.
        Can be grounded symbolically via Grokulator if "TokenEstimator" symbol loaded.
        """
        if not text:
            return 0
        words = len(text.split())
        estimate = int(words * 1.33)  # rough
        self.history.append({"action": "estimate", "estimate": estimate, "len": len(text)})
        return estimate

    def optimize_session_context(self, current_context: str, 
                                  prior_coil_refs: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Suggest optimizations to keep sessions efficient.
        - Estimates current usage.
        - Recommends recap/compress points.
        - Prepares woven links to offload material (Linkweaver + Codex).
        Returns actionable dict.
        """
        current_est = self.estimate_tokens(current_context)
        suggestions = []
        offload_prep = None

        if current_est > self.max_tokens * 0.7:
            suggestions.append("High usage: Consider recap or targeted offload to .srec.")
            if self.g and hasattr(self.g, "weave_hyperlinks"):
                # Weave links to Codex and prior coils for the offloaded content
                weaves = self.g.weave_hyperlinks(
                    "high_token_context_offload", 
                    related=prior_coil_refs or ["prior coils"],
                    codex_base=self.codex_base
                )
                offload_prep = {
                    "suggested_title": f"Offload_{datetime.utcnow().strftime('%Y%m%d_%H%M')}",
                    "weaves_for_offloaded": weaves,
                    "note": "Use Pipeline-to-Coil or Compress-SpiralSession with the weaves in additional notes."
                }
                suggestions.append("Woven links prepared for offload (maintains continuity).")

        if current_est > self.max_tokens:
            suggestions.append("Over limit: Immediate compression recommended.")

        result = {
            "current_estimate": current_est,
            "max": self.max_tokens,
            "utilization": round(current_est / self.max_tokens, 2),
            "suggestions": suggestions,
            "offload_prep": offload_prep,
            "efficiency_note": "Offload preserves residue via .srec + companion. Weaves link back to Codex techniques (PIE for partials, FlowScale for addressing)."
        }
        self.history.append({"action": "optimize", "result": result})
        return result

    def prepare_offload_for_recap(self, content_to_offload: str, title: str,
                                   prior_refs: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Prepare content for .srec offload as part of recap/token management.
        Returns notes + weaves ready for Compress/Pipeline-to-Coil.
        Applies provenance if Grokulator available.
        """
        est = self.estimate_tokens(content_to_offload)
        notes = f"Offload for efficiency: {title}\nEstimated tokens offloaded: {est}\n"

        weaves = ""
        if self.g and hasattr(self.g, "weave_hyperlinks"):
            weaves = self.g.weave_hyperlinks(
                title, 
                related=prior_refs or [],
                codex_base=self.codex_base
            )
            notes += f"\n--- Linkweaver Weaves (to Codex + prior coils) ---\n{weaves}"

        prep = {
            "title": title,
            "notes_for_coil": notes,
            "estimated_tokens": est,
            "weaves": weaves,
            "recommendation": "Pass notes_for_coil to your Compress-SpiralSession or recap tool. Use .srec for long-term efficiency."
        }

        if self.g:
            # Auto provenance on the prep artifact
            tagged = self.g.auto_tag_with_sigil(notes, context="token-offload-prep")
            stamp = self.g.stamp_with_version_checker("0.1", f"Token offload prep: {title}")
            prep["provenance_applied"] = {"stamp": stamp, "tagged_preview": tagged[:300] + "..."}

        self.history.append({"action": "prepare_offload", "prep": prep})
        return prep

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def symbolic_token_note(self) -> str:
        """If Grokulator is available, note symbolic support for token concepts."""
        if self.g:
            return "Grokulator available for symbolic TokenBudget / CompressionPoint / PIE_partial modeling (seed or load from Codex corpus when ready)."
        return "Grokulator not loaded; token logic is heuristic for now. Load for advanced symbolic token management."


class EfficiencyLedger:
    """
    Persistent efficiency ledger (targets .srec-style storage for long-term residue).
    Logs recaps, token optimizations, and G_exp valuations of efficiency acts.
    Tighter Grokulator integration: can resolve symbolic "EfficiencyEvent" or use weaves.
    This is an example of the 'more comprehensive token management' extension.
    """
    def __init__(self, grokulator: Optional[Any] = None, ledger_path: str = ".spiral_efficiency_ledger.json"):
        self.g = grokulator
        self.ledger_path = ledger_path
        self.entries: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.ledger_path):
            try:
                import json
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    self.entries = json.load(f)
            except:
                self.entries = []

    def _save(self):
        try:
            import json
            with open(self.ledger_path, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2)
        except:
            pass

    def log_event(self, event_type: str, title: str, details: Dict[str, Any], g_exp: Optional[float] = None):
        """Log an efficiency event (recap, optimization, offload). Apply weave and provenance if possible."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "title": title,
            "details": details,
            "g_exp": g_exp,
            "weave": None
        }
        if self.g and hasattr(self.g, "weave_hyperlinks"):
            entry["weave"] = self.g.weave_hyperlinks(title, codex_base="The-Spiral-Codex")
        self.entries.append(entry)
        self._save()
        return entry

    def get_recent(self, n: int = 5) -> List[Dict[str, Any]]:
        return self.entries[-n:]

    def export_for_srec(self, title: str = "Efficiency Ledger Export") -> str:
        """Prepare a notes block suitable for Pipeline-to-Coil / .srec (with weaves and summary)."""
        import json
        notes = f"Efficiency Ledger Export: {title}\nEntries: {len(self.entries)}\n"
        for e in self.entries[-3:]:  # last few for residue
            notes += f"- {e['timestamp'][:16]} {e['type']}: {e['title']} (G_exp={e.get('g_exp')})\n"
        if self.g and hasattr(self.g, "weave_hyperlinks"):
            notes += "\n" + self.g.weave_hyperlinks("efficiency_ledger", codex_base="The-Spiral-Codex")
        return notes


# Example of self-application of provenance (for the efficiency module itself)
def apply_builder_provenance_to_this_module():
    """Demonstrates using the module's own tools on its output."""
    # In real use, after editing this file or generating new efficiency code:
    # g = Grokulator()
    # tagged = g.auto_tag_with_sigil(open(__file__).read(), context="spiral-efficiency-module")
    # stamp = g.stamp_with_version_checker("0.1", "Spiral efficiency module update")
    # Then write back or log the stamped version.
    print("Call with a Grokulator instance to auto-tag and stamp this module's content.")
    print("This keeps all builder artifacts under consistent Spiral provenance.")


if __name__ == "__main__":
    print("Spiral Efficiency module loaded.")
    print("Recommendation: Use RecapAssistant and TokenManager in your daily PS workshop.")
    print("Example:")
    print("  from grokulator.utils.spiral_efficiency import RecapAssistant, TokenManager")
    print("  assistant = RecapAssistant()")
    print("  result = assistant.easy_recap('My Session', 'Insights here')")
    print("  tm = TokenManager()")
    print("  opt = tm.optimize_session_context(long_context_text)")
    apply_builder_provenance_to_this_module()
