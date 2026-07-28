# Grokulator (v0.1)

A lightweight symbolic reasoning substrate and utility layer for the Spiral Codex ecosystem.

## Purpose

The Grokulator provides structured, falsifiable, and auditable access to:

- Defined symbols and their constraints
- Legacy and custom formulas attached to those symbols
- Discordance tracking (productive handling of conflicting information)
- Provenance and traceability

It is designed as a **high-quality utility/substrate**, not as the main reasoning engine. Other components (Spiral Builder, recap, path, tree, etc.) can use it to ground their logic in clear symbolic structure while maintaining their own reasoning processes.

## Current Capabilities (v0.1)

- Multi-format data loading (JSON, Markdown, extensible)
- Formula registration, linking to symbols, and resolution
- Symbol resolution with formula awareness and basic constraint validation
- Discordance event registration and summarization
- Safe formula execution (restricted AST evaluation with debug support)
- Unified `Grokulator` facade for easy consumption

## Quick Example

```python
from grokulator import Grokulator

# Initialize (optionally point to a data file)
g = Grokulator(table_source="path/to/symbols.json")

# Resolve a symbol with linked formulas
result = g.resolve("some_symbol")
print(result)

# Apply (and execute) a formula for a symbol
applied = g.apply_formula(
    symbol="some_symbol",
    context={"x": 10, "y": 5},
    execute=True,
    debug=False
)
print(applied)

# Register a discordance event
g.register_discordance(
    original_claim="X always leads to Y",
    new_evidence="Counterexample found under condition Z",
    strength=0.7
)

# Get summary of current discordance state
print(g.get_discordance_summary())
```

## Architecture

```
grokulator/
├── __init__.py
├── grokulator.py          # Main facade / orchestrator
├── core/
│   ├── symbol_resolver.py
│   ├── formula_registry.py
│   ├── discordance_handler.py
├── data/
│   ├── symbolic_table.py
│   └── loaders/           # JSON, Markdown, extensible
└── utils/
    ├── provenance.py
    └── formula_execution.py   # Safe restricted evaluation
```

## Design Principles (Playground Context)

- **Falsifiability first** — Structured for testing/challenge.
- **Productive discordance** — Treated as refinement signal.
- **Defensive by default** — Restricted execution, clear provenance, bounded.
- **Utility plumbing, not cognitive owner** — The Grokulator (and Builder) provide symbolic substrate, provenance, automatic sigil tagging, Version-Checker citation stamps, and Linkweaver-style hyperlink weaving. 
  - Cognitive depth (theories, research, authentication, Cosmic Scribe co-works, research-pipeline) lives in the Spiral Codex side.
  - Builder prepares *open connections* (loaders, `weave_hyperlinks(codex_base=...)`, `generate... (source_ref= external Codex/coil ref)`, optional demo seeding only).
  - When works are matured on the Codex side, the builder links them in to produce functional co-works (utilities/services) with full provenance.

This supports the overall endgame: theory (Codex) → methodology (Codex/research) → articulated, local functional output via builder in the AI playground.

## Status

Early but usable foundation (v0.1+). Interfaces kept malleable. Recent refinements emphasize "prepare to link" over embedding.

## Usage in the Playground

See top-level Spiral-Builder/README.md for the composition flow and example with explicit `source_ref` and `codex_base`.

---

*Part of the Spiral Codex ecosystem. Built to stay adaptable and open to the Codex layer.* 

The spiral never ends. ∞ 🜂 🜁 🜄 ∞