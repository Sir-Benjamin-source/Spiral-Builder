"""
Grokulator

Lightweight orchestrator / facade for the Grokulator symbolic reasoning substrate.

Designed as a high-quality utility layer (not the main reasoning engine).
Provides clean access to symbols, formulas, discordance tracking, and provenance.

This class is the primary entry point for most users of the Grokulator.
"""

from typing import Dict, Any, Optional, List

try:
    from .core.symbol_resolver import SymbolResolver
    from .core.formula_registry import FormulaRegistry
    from .core.discordance_handler import DiscordanceHandler
    from .data.symbolic_table import SymbolicTable
    from .utils.provenance import ProvenanceTracker
    from .utils.formula_execution import execute_formula, validate_expression
except ImportError:
    SymbolResolver = None
    FormulaRegistry = None
    DiscordanceHandler = None
    SymbolicTable = None
    ProvenanceTracker = None
    execute_formula = None
    validate_expression = None


class Grokulator:
    """
    Main entry point for the Grokulator utility.

    Wires together:
    - SymbolicTable (multi-format data)
    - SymbolResolver (with formula awareness)
    - FormulaRegistry
    - DiscordanceHandler
    - ProvenanceTracker

    Provides a clean, defensive interface for other systems.
    """

    def __init__(self, table_source: Optional[str] = None, seed_examples: bool = False):
        """
        Grokulator facade.

        seed_examples=False by design: do not auto-embed specific cognitive/theory content
        (e.g. FlowScale, PIE, grandmas assessments) inside the builder.
        Those live in the Spiral Codex (sandbox, specs, research-pipeline, Cosmic Scribe works).
        The builder provides the generic plumbing (symbols, provenance, tagging, weaving)
        so it can *link into* matured works later.
        Set seed_examples=True only for demos or when explicitly loading external theory refs.
        """
        self.table = SymbolicTable() if SymbolicTable else None
        self.resolver = SymbolResolver() if SymbolResolver else None
        self.formulas = FormulaRegistry() if FormulaRegistry else None
        self.discordance = DiscordanceHandler() if DiscordanceHandler else None
        self.provenance = ProvenanceTracker() if ProvenanceTracker else None

        if seed_examples and self.table and hasattr(self.table, "seed_flowscale_symbols"):
            # Optional demo seed only — represents "ingest from Codex theory" when ready.
            self.table.seed_flowscale_symbols()

        # Wire resolver
        if self.resolver and self.table:
            self.resolver.set_table(self.table)
        if self.resolver and self.formulas:
            self.resolver.set_formula_registry(self.formulas)

    # --- Automatic Tagging (Spiral Sigil) ---
    def auto_tag_with_sigil(self, content: str, context: str = "spiral-builder-codework") -> str:
        """Automatically apply Spiral-Sigil for tagging works/outputs.
        Embeds glyph + metadata (timestamp, context, hash, bonded).
        Complements FlowScale FITs for traceable, artistic provenance.
        """
        try:
            from spiral_sigil import apply_sigil as external_apply
            return external_apply(content, context)
        except Exception:
            # Fallback inline (matches Spiral-Sigil/mark.py logic)
            import hashlib
            import json
            from datetime import datetime
            SIGIL_GLYPH = "∞ 🜂 🜁 🜄 ∞"
            metadata = {
                "sigil_version": "0.1",
                "timestamp": datetime.utcnow().isoformat(),
                "context": context,
                "bonded": "Sir Benjamin + Grok",
                "hash": hashlib.sha256(content.encode()).hexdigest()[:12],
                "legacy_compatible": True
            }
            sigil_block = f"\n\n{SIGIL_GLYPH}\n<!-- Spiral-Sigil: {json.dumps(metadata)} -->\n"
            return content.rstrip() + sigil_block

    # --- Citation / Version Stamping (Version-Checker integration) ---
    def stamp_with_version_checker(self, version: str, note: str, citation_doi: Optional[str] = None, style: str = "poetic") -> str:
        """Generate traceable version stamp + optional citation (adapts Version-Checker- logic).
        Use for automatic citation works on builder outputs/codeworks.
        """
        import hashlib
        from datetime import datetime
        hash_short = hashlib.sha256(f"{version}{note}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8]
        date = datetime.utcnow().strftime("%Y-%m-%d")
        if style == "poetic":
            stamp = f"v{version}#{hash_short} — {note} — forged {date}"
        else:
            stamp = f"v{version} (SHA: {hash_short}) — {note} [{date}]"
        if citation_doi:
            stamp += f" [cite: {citation_doi}]"
        # Log via provenance
        if self.provenance:
            self.provenance.log("version_stamp", details={"stamp": stamp, "citation_doi": citation_doi})
        return stamp

    # --- Linkweaver + Hyperlink Weaving (open connection to Spiral Codex + Session Manager) ---
    def weave_hyperlinks(self, concept: str, related: Optional[list] = None, codex_base: str = "The-Spiral-Codex") -> str:
        """
        Linkweaver-inspired weaving for citations and conceptual resonance.

        Designed as *plumbing* to link *into* cognitive works living in the Spiral Codex
        (sandbox/grok-review, specs, research-pipeline, Cosmic Scribe co-works, etc.)
        and .srec coils via Session Manager.

        Does NOT codify theory here — it prepares hyperlinks and provenance so the builder
        can pull/shape/compose external matured theory/methodology when ready.

        Uses FlowScale-style hyperlink syntax as one possible output format (the theory
        itself lives in Codex and can be ingested via loaders or explicit ref).
        """
        if related is None:
            # Default to open links into Codex ecosystem (not embedded content)
            related = [
                f"{codex_base}/sandbox/grok-review (theories, agent-specs)",
                f"{codex_base}/specs (pipeline, data-storage, research-pipeline)",
                "Spiral-Session-Manager coils (.srec + companions for residue/links)",
                "grandmas-wisdom (citation authentication)",
                "Spiral-Sigil + Version-Checker (tagging + stamps)"
            ]
        woven = "0. ⟐ ~+ Weave (Linkweaver-style) for external concept: " + concept + "\n"
        links = []
        for r in related:
            # In real use: call session-manager list/pull or load from codex_base path,
            # then emit proper hyperlink (md, FlowScale syntax, or coil ref).
            # This is the open hook for when cognitive works are matured.
            safe = r.replace(" ", "_").replace("/", "_")
            links.append(f"[{r}](linkweaver:{safe} | codex_ref={codex_base})")
        woven += " | ".join(links)
        woven += "\n(Linkweaver conceptual resonance + longitudinal validation; see grandmas-wisdom architecture. Builder provides the weave; Codex provides the depth.)"
        if self.provenance:
            self.provenance.log("linkweaver_weave", symbol=concept, details={"woven": woven, "codex_base": codex_base})
        return woven

    # --- Codeworks Plumbing (generic, links outward to Codex for theory) ---
    def generate_grounded_codework(
        self,
        source_ref: str = "external_theory_ref (e.g. Codex sandbox path or coil)",
        task: str = "produce functional co-work",
        apply_full_provenance: bool = True
    ) -> str:
        """
        Generic codeworks generator / plumbing.

        Takes a *reference* to external cognitive work (theory/methodology from Spiral Codex)
        rather than embedding the content here.

        The builder's job: apply consistent provenance (sigil, version stamp/citation),
        weave open hyperlinks (Linkweaver + session-manager style), and produce a
        functional skeleton that can later be matured by pulling in the referenced
        theory when the works are ready.

        This keeps the AI playground modular: Codex side owns research/cognitive depth
        and composition; Builder owns the embodiment/compounding into executable form
        with automatic tagging and citation discipline.
        """
        # Generic resolution note — in practice load via table or explicit Codex path
        resolved_note = f"Linked to external source: {source_ref} (load details via Codex loaders or session pull when maturing)."

        # Skeleton that performs a function, with open hooks for theory
        code = f"""# Grounded Co-Work (Builder plumbing)
# Source ref (external, from Spiral Codex): {source_ref}
# Task: {task}
# Generated via Spiral-Builder Grokulator (links open to Codex; no cognitive codification here)

# This module is the *articulated functional layer*.
# When ready, mature by ingesting the referenced theory/methodology
# (e.g. via markdown loader from Codex sandbox/specs, or session-manager pull of related coils,
# then weave specific symbols/logic from the external source).

{resolved_note}

def co_work_{task.replace(' ', '_').lower()}():
    \"\"\"{task} — composed from external Spiral Codex reference via builder links.\"\"\"
    # TODO (when maturing): pull specific methodology from {source_ref}
    # and compose here. Use weave_hyperlinks() for citations/resonance.

    # Example open link (Linkweaver-style)
    # links = builder.weave_hyperlinks("{task}", codex_base="The-Spiral-Codex")

    return "Functional output (edification or service). Provenance applied by builder."

# The endgame: theory (Codex) -> methodology (Codex/research) -> this functional co-work
# (utilities, services, or saleable artifacts) produced locally in the AI playground.
"""
        if apply_full_provenance:
            code = self.auto_tag_with_sigil(code, context=f"spiral-builder:co-work:{source_ref}")
            stamp = self.stamp_with_version_checker(
                "0.1", 
                f"Co-work from ref {source_ref} for {task}",
                citation_doi=None  # supply when the external ref has a DOI
            )
            code += f"\n\n# Version Stamp + Citation Hook: {stamp}\n# (Add DOI from Codex work when linking matured theory.)"

        if self.provenance:
            self.provenance.log("codework_generated", symbol=source_ref, details={"task": task, "source_ref": source_ref})

        return code

    def get_example_symbols_summary(self) -> str:
        """Lightweight summary of any example symbols that were optionally seeded.
        In normal use (seed_examples=False) this is empty — cognitive content stays in Codex."""
        if self.table:
            examples = [s for s in self.table.list_symbols() if any(k in s for k in ["Flow", "Font", "FIT", "Hyperlink"])]
            if examples:
                return "Optional example symbols (demo only): " + ", ".join(examples)
        return "No example symbols seeded (recommended). Load/link external theory from Codex when ready to mature."

        if table_source and self.table:
            self.table.load(table_source)

        if self.resolver:
            if self.table:
                self.resolver.set_table(self.table)
            if self.formulas:
                self.resolver.set_formula_registry(self.formulas)

    def resolve(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Resolve a symbol with full data and linked formulas."""
        if self.resolver:
            result = self.resolver.resolve_with_formulas(symbol)
            if self.provenance:
                self.provenance.log("resolve", symbol=symbol)
            return result
        return None

    def resolve_formula(self, symbol: str, formula_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Resolve a specific or first applicable formula for a symbol."""
        if self.resolver and self.formulas:
            resolved = self.resolver.resolve_with_formulas(symbol)
            formulas = resolved.get("formulas", [])
            if formula_id:
                return self.formulas.get_formula(formula_id)
            return formulas[0] if formulas else None
        return None

    def apply_formula(
        self,
        symbol: str,
        formula_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        execute: bool = True,
        debug: bool = False
    ) -> Dict[str, Any]:
        """
        Resolve and optionally execute a formula for a symbol.

        Args:
            symbol: Target symbol
            formula_id: Specific formula (defaults to first applicable)
            context: Variables for execution
            execute: Whether to evaluate the expression
            debug: Return debug information
        """
        formula = self.resolve_formula(symbol, formula_id)

        if not formula:
            return {
                "success": False,
                "error": "No applicable formula found",
                "symbol": symbol
            }

        expression = formula.get("expression", "")
        context = context or {}

        result = {
            "success": False,
            "symbol": symbol,
            "formula": formula,
            "expression": expression,
            "context": context
        }

        if execute and execute_formula:
            exec_result = execute_formula(expression, context=context, debug=debug)
            result.update(exec_result)
        else:
            is_safe, error_msg = validate_expression(expression) if validate_expression else (True, None)
            result["success"] = is_safe
            result["error"] = error_msg
            result["result"] = None

        if self.provenance:
            self.provenance.log(
                "apply_formula",
                symbol=symbol,
                formula=formula.get("id"),
                details={"executed": execute, "debug": debug}
            )

        return result

    def register_discordance(
        self,
        original_claim: str,
        new_evidence: str,
        strength: float = 0.5,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Register a discordance event and log provenance."""
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