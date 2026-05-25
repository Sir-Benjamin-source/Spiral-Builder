# Grokulator Usage Process Guide

> **Note:** This document was originally created as an integration and development roadmap. It has been reshaped into a practical usage guide for working with the Grokulator as a utility layer.

**Related DOI:** 10.5281/zenodo.20369112

---

## Purpose of This Document

This guide explains how to actually *use* the Grokulator in practice — especially when supporting Grandma's Wisdom workflows and preparing for future Grandpa's Wisdom integration.

It focuses on recommended processes, common patterns, and how the different parts of the Grokulator work together.

---

## Core Concepts

| Concept                  | What it represents                                      | Primary Class / Method          |
|--------------------------|---------------------------------------------------------|---------------------------------|
| **Symbol**               | A defined concept with constraints                      | `SymbolicTable`, `SymbolResolver` |
| **Formula**              | Logic or calculation attached to one or more symbols    | `FormulaRegistry`               |
| **Discordance**          | Productive tension between claims and new evidence      | `DiscordanceHandler`            |
| **Provenance**           | Traceability of reasoning steps                         | `ProvenanceTracker`             |
| **Application**          | Resolving + optionally executing a formula              | `Grokulator.apply_formula()`    |

The `Grokulator` class (in `grokulator.py`) acts as the main facade that wires these components together.

---

## Recommended Workflows

### 1. Basic Symbol + Formula Resolution

```python
g = Grokulator(table_source="path/to/your/symbols.json")

# See what a symbol contains + any linked formulas
result = g.resolve("evidential_claim")

# Get and execute the best formula for that symbol
applied = g.apply_formula(
    symbol="evidential_claim",
    context={"evidence_strength": 0.8, "source_reliability": 0.9},
    execute=True
)
```

### 2. Grandma's Wisdom Style Assessment

```python
# Register a formula that reflects Grandma-style evaluation
g.formulas.register_formula(
    formula_id="grandma_support_score",
    name="Grandma Support Score",
    expression="evidence_strength * source_reliability",
    linked_symbols=["evidential_claim"],
    formula_type="Grandma"
)

result = g.apply_formula("evidential_claim", context=..., execute=True)

# Flag discordance if acceptance and evidence diverge
if result["result"] < 0.6:
    g.register_discordance(
        original_claim="This has wide acceptance",
        new_evidence="Evidence strength is low",
        strength=0.65
    )
```

### 3. Handling Discordance Productively

```python
g.register_discordance(
    original_claim=...,
    new_evidence=...,
    strength=0.7,
    context={"source": "new_research"}
)

summary = g.get_discordance_summary()
print(summary)  # See suggested actions and high-impact events
```

### 4. Tracing Reasoning (Provenance)

```python
history = g.get_provenance_history()
for entry in history:
    print(entry)
```

---

## Design Principles (Still Relevant)

| Principle                    | Why it matters for usage                                      |
|-----------------------------|---------------------------------------------------------------|
| **Falsifiability**          | Every output should be testable or challengeable.             |
| **Productive Discordance**  | Conflicting information should lead to refinement, not rejection. |
| **Defensive by Default**    | Execution is restricted. Provenance is always available.      |
| **Utility, Not Overlord**   | The Grokulator mediates and structures. Heavy reasoning lives elsewhere. |

---

## Working with Grandma's Wisdom

The Grokulator is especially useful as a structured bridge for Grandma's Wisdom work:

- Use **symbols** to define key evidential concepts cleanly.
- Use **formulas** to express Grandma-style evaluations (evidence scoring, bullshit risk, support strength, etc.).
- Use **discordance** to flag when acceptance and evidence diverge.
- Use **provenance** to maintain lineage across assessments.

See `grokulator/examples/grandmas_wisdom/` for concrete examples.

---

## Preparing for Grandpa's Wisdom

As we develop Grandpa's Wisdom (the harmonizing / bias-correcting layer), the Grokulator will serve as the common structured substrate that both Grandma and Grandpa perspectives run through. This allows their differences to be mediated rather than forcing one to dominate.

The current interfaces (`resolve_with_formulas`, `apply_formula`, `register_discordance`, etc.) are designed to remain extensible for this future work.

---

## Summary of Key Methods

| Method                        | When to use it                                      |
|-------------------------------|-----------------------------------------------------|
| `resolve(symbol)`             | You want full data + linked formulas for a symbol   |
| `apply_formula(...)`          | You want to evaluate or prepare a formula           |
| `register_discordance(...)`   | New evidence conflicts with an existing claim       |
| `get_discordance_summary()`   | You want an overview of current tension points      |
| `validate(symbol, value)`     | You want to check a value against symbol constraints|

---

*This document will continue to evolve as the Grokulator is used with Grandma's and Grandpa's Wisdom frameworks.*