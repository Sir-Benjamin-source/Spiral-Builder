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

## Design Principles

- **Falsifiability first** — Everything should be structured so it can be tested or challenged.
- **Productive discordance** — Conflicting information is treated as a signal for refinement, not just error.
- **Defensive by default** — Restricted execution, clear provenance, and bounded behavior.
- **Utility, not overlord** — The Grokulator provides structured access and mediation. Heavy reasoning stays in the calling systems.

## Status

Early but usable foundation (v0.1). The interfaces are designed to remain malleable as the broader Grandma/Grandpa Wisdom vision develops.

## Future Direction

Planned evolution includes deeper integration with Grandma's Wisdom and the emerging Grandpa's Wisdom layer, using the Grokulator as the structured bridge between evidential/authenticating and adversarial/falsifying perspectives.

---

*Part of the Spiral Codex ecosystem. Built to stay adaptable.*