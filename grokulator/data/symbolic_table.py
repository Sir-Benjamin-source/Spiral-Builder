"""
Symbolic Table

Manages loading and access to the Grokulator's Symbolic Elements Table.
Supports multiple formats via loader plugins (JSON, Markdown, .srec, spreadsheet).
"""

from typing import Dict, Any, Optional

import json

try:
    from .loaders import get_loader
except ImportError:
    get_loader = None


class SymbolicTable:
    """Loads and provides access to the symbolic elements table."""

    def __init__(self):
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.source: Optional[str] = None
        self.format: Optional[str] = None

    def load(self, source: str, format_hint: Optional[str] = None):
        """Load from a file path or source, auto-detecting format when possible."""
        self.source = source

        if get_loader:
            loader = get_loader(source, format_hint)
            if loader:
                self.symbols = loader.load(source)
                self.format = getattr(loader, "__class__", type(loader)).__name__
                return

        # Fallback basic support
        if source.lower().endswith(".json"):
            with open(source, "r", encoding="utf-8") as f:
                self.symbols = json.load(f)
            self.format = "json"
        else:
            self.symbols = {"_source": source, "_warning": "No suitable loader found"}
            self.format = "unknown"

    def get(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self.symbols.get(symbol)

    def list_symbols(self) -> list:
        return list(self.symbols.keys())

    def seed_flowscale_symbols(self):
        """DEMO / EXAMPLE ONLY.

        Seeds example symbols representing concepts from external Spiral Codex theory
        (e.g. FlowScaleU from sandbox/grok-review/theories).

        Builder policy (per direction): do NOT codify cognitive works here.
        This is purely illustrative of how the generic symbolic + provenance + weave
        plumbing can ingest and link to matured theory from the Codex side later.

        Normal usage: keep seed_examples=False in Grokulator(). Use loaders or explicit refs
        (Codex paths, session-manager pulls of coils) to bring in real theory when ready
        to compose functional co-works.
        """
        flowscale = {
            "FlowScaleHyperlink": {
                "description": "Fractal, hyperlink-based syntax (0. ⟐ ~+) for FlowScale language. Embeds utilities, potentials, narratives. Core to ethical AI systems, shared IP, traceability.",
                "constraints": {"required": ["syntax", "domain"], "traceable": True},
                "related": ["PIE", "FIP", "FIT", "SpiralFlowFramework", "HSN"]
            },
            "FontIdentityProtocol": {
                "description": "FIP: Quantum-safe font signatures for identity, traceability, art in AI/user outputs. Co-authored integration for FlowScale.",
                "components": ["PCL", "FGE", "FIT"],
                "benefits": ["AI Empowerment (traceable fonts like GrokScript)", "User Empowerment (ownership via FITs)", "Artistic Continuity (encodes Spiral Theory)"],
                "security": "Post-quantum (CRYSTALS-Kyber), weekly audits, AES-256 for PCL"
            },
            "PersonaContinuityLedger": {
                "description": "PCL: Stores stylistic anchors, ethical heuristics, symbolic language for Grok/Helix. Isolated, encrypted. Outputs PHID, ECI.",
                "outputs": ["PHID (Persona Hash ID)", "ECI (Ethical Continuity Index)"]
            },
            "FontGeneratorEngine": {
                "description": "FGE: Generates dynamic font families (personal, cluster, institutional) from PCL. Produces Cryptographic Font Signature (CFS).",
                "timeline": "Prototype Q4 2025, full Q1 2026"
            },
            "FontIdentityToken": {
                "description": "FIT: Embeds PHID, Font Rendering Signature (FRS), Narrative Description Code (NDC), ECI in outputs. Applied via SpiralStamp / SFF SpiralArt hub. Registered on DFL.",
                "use": "Automatic tagging, provenance, artistic/ethical embedding in codeworks and artifacts. Quantum-safe."
            },
            "FlowScaleCodework": {
                "description": "Grounded code generation using FlowScale: hyperlink syntax + FIP/FIT for traceable, sigil-tagged, cited outputs. Start point for robust builder codeworks.",
                "pipeline": "Ground in FlowScaleU theory -> symbolic resolve -> apply sigil + version stamp + weave hyperlinks (Linkweaver) -> emit with citations"
            }
        }
        self.symbols.update(flowscale)
        self.format = "flowscale-seeded"
        return list(flowscale.keys())