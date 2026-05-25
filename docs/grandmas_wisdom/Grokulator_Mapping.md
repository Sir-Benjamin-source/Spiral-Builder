# Grandma's Wisdom → Grokulator Mapping

**Purpose:** Map core Grandma's Wisdom concepts to Grokulator primitives so they can be expressed, executed, and tracked in a structured, falsifiable way.

**Status:** First-pass mapping (iterative)

---

## Core Mapping

| Grandma's Wisdom Concept          | Description                                      | Grokulator Primitive(s)                  | Notes / Recommended Pattern                                                                 |
|-----------------------------------|--------------------------------------------------|------------------------------------------|---------------------------------------------------------------------------------------------|
| **Evidential Claim**              | A claim backed by observable or verifiable support | Symbol + Constraints                     | Define as a symbol with required fields (`evidence_strength`, `source_reliability`, etc.)   |
| **Supporting Source**             | A source that lends credibility to a claim       | Symbol + Formula                         | Can be a linked symbol or encoded in a formula that weights source quality                  |
| **Bullshit Risk / Meter**         | Assessment of how weak, misleading, or empty a claim is | Formula (`bullshit_risk` or `support_score`) | Use formulas like `1 - (evidence * 0.6 + reliability * 0.4)`. Higher = more risk            |
| **Evidence vs. Acceptance Gap**   | When popular acceptance diverges from actual evidence strength | Discordance + Formula              | Register discordance when acceptance is high but calculated evidence/support is low         |
| **Authenticity / Provenance**     | Lineage and traceability of a claim or assessment | ProvenanceTracker + Symbol constraints | Log key assessments. Use symbol constraints to require source metadata                      |
| **"What Works" Evaluation**     | Practical judgment of real-world effectiveness   | Formula + Discordance                    | Combine scoring formulas with discordance when real-world outcomes contradict claims        |
| **Helical / Generational Continuity** | Building on prior valid work across time     | Provenance + Versioning (future)         | Track lineage of assessments. Future: Linkweaver + version checker integration              |

---

## Recommended Patterns

### 1. Basic Grandma-Style Assessment

```python
g = Grokulator()

# Register a Grandma-style scoring formula
g.formulas.register_formula(
    formula_id="grandma_support_score",
    name="Grandma Support Score",
    expression="evidence_strength * source_reliability",
    linked_symbols=["evidential_claim"],
    formula_type="Grandma"
)

result = g.apply_formula(
    symbol="evidential_claim",
    context={"evidence_strength": 0.75, "source_reliability": 0.9},
    execute=True
)
```

### 2. Flagging Weak Acceptance

```python
if result["result"] < 0.6:
    g.register_discordance(
        original_claim="This has wide acceptance",
        new_evidence="Calculated support score is low",
        strength=0.7,
        context={"assessment": "Grandma"}
    )
```

### 3. Tracking Assessment Lineage

```python
history = g.get_provenance_history()
# Later: integrate with Linkweaver / version checker for generational tracking
```

---

## Open Questions (to be answered through use)

- How should the "bullshit meter" be normalized across different domains?
- Should Grandma's assessments carry explicit confidence intervals or ranges?
- How do we handle conflicting Grandma-style assessments on the same topic?
- What level of granularity is most useful for symbols in Grandma's work (broad vs. highly specific)?
- How will Grandpa's Wisdom later interact with these Grandma + Grokulator outputs?

---

## Current Examples

See `grokulator/examples/grandmas_wisdom/basic_assessment.py` for a working demonstration of the patterns above.

---

*This mapping will evolve as we actually use it and as Grandpa's Wisdom develops.*