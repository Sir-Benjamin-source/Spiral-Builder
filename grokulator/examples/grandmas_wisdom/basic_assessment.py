"""
Grandma's Wisdom Example using the Grokulator

This example shows how core Grandma's Wisdom concepts can be modeled
using Grokulator primitives (symbols, formulas, discordance, provenance).

It is intentionally simple and illustrative for v0.1.
"""

from grokulator import Grokulator


def run_grandma_assessment_example():
    print("=== Grandma's Wisdom Assessment Example ===\n")

    # Initialize Grokulator (in real use this would load from a proper data file)
    g = Grokulator()

    # --- Step 1: Define relevant symbols (in practice these live in the table) ---
    # For this example we manually register a few key symbols
    print("[1] Defining key symbols for Grandma's assessment...")

    # These would normally come from the SymbolicTable
    grandma_symbols = {
        "evidential_claim": {
            "description": "A claim supported by observable evidence",
            "constraints": {"required": ["evidence_strength", "source_reliability"]}
        },
        "supporting_source": {
            "description": "A source that backs the claim",
            "constraints": {"required": ["credibility", "independence"]}
        },
        "bullshit_risk": {
            "description": "Risk that the claim is weak or misleading",
            "constraints": {"range": [0.0, 1.0]}
        }
    }

    # --- Step 2: Register formulas that Grandma might use ---
    print("[2] Registering Grandma-relevant formulas...")

    g.formulas.register_formula(
        formula_id="grandma_evidence_score",
        name="Grandma Evidence Strength",
        expression="evidence_strength * source_reliability * 0.8",
        linked_symbols=["evidential_claim"],
        formula_type="Grandma",
        notes="Simple weighted scoring for evidential support"
    )

    g.formulas.register_formula(
        formula_id="grandma_bullshit_check",
        name="Bullshit Risk Calculator",
        expression="1 - (evidence_strength * 0.6 + source_reliability * 0.4)",
        linked_symbols=["bullshit_risk"],
        formula_type="Grandma",
        notes="Higher values = higher risk of weak claim"
    )

    # --- Step 3: Simulate a Grandma-style assessment ---
    print("[3] Running sample assessment...\n
    )}

    context = {
        "evidence_strength": 0.75,
        "source_reliability": 0.85
    }

    evidence_result = g.apply_formula("evidential_claim", context=context, execute=True)
    bullshit_result = g.apply_formula("bullshit_risk", context=context, execute=True)

    print("Evidence Strength Score:", evidence_result.get("result"))
    print("Bullshit Risk Score:", bullshit_result.get("result"))

    # --- Step 4: Register discordance if evidence and acceptance diverge ---
    if bullshit_result.get("result", 0) > 0.4:
        g.register_discordance(
            original_claim="This claim has wide acceptance",
            new_evidence="High bullshit risk detected despite acceptance",
            strength=0.65,
            context={"assessment_type": "Grandma"}
        )
        print("\n[Discordance registered] Wide acceptance vs high bullshit risk")

    # --- Step 5: Show summary ---
    print("\n=== Assessment Summary ===")
    print(g.get_discordance_summary())
    print("\nProvenance entries:", len(g.get_provenance_history()))


if __name__ == "__main__":
    run_grandma_assessment_example()