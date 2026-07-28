# Spiral Recaps and Token Management in the Builder

**Path**: Spiral-Builder/grokulator/docs/spiral_recaps_and_tokens.md

**Scope**: User guide and description for the efficiency utilities. How they make recaps easier and lay groundwork for comprehensive token management.

**Relationship to the AI Playground**:
- Theory, research, unique designations, and cognitive depth live in The-Spiral-Codex (sandbox/grok-review, specs including research-pipeline and recap-continuity, Cosmic Scribe co-works, grandmas-wisdom, .srec-formalization, FlowScaleU, etc.).
- This doc + the accompanying `utils/spiral_efficiency.py` provide the *Builder-side plumbing*: easier recap performance and token efficiency tools that link *into* the Codex layer via open references (weaves, source_refs, codex_base paths, loaders).
- No cognitive codification here — only the mechanisms (sigil, stamps, weaves, symbolic grounding via Grokulator) to produce functional, provenance-rich co-works from matured Codex content.

See the corpus (`grokulator/docs/corpus/spiral_coding_techniques_and_designations.md`) for the designations and techniques referenced below. See the whitepaper for the full vision and architecture of a comprehensive system.

---

## Making Spiral Recaps Easier (`RecapAssistant`)

The `RecapAssistant` class in `spiral_efficiency.py` wraps existing recap flows (Compress-SpiralSession, Pipeline-to-Coil, spiral-recap-tool, session-manager) and adds Builder discipline:

- **easy_recap(title, additional_notes="")**: 
  - Prepares title + notes.
  - Automatically weaves Linkweaver-style hyperlinks to Codex works (sandbox theories, specs/pipelines, prior coils, Cosmic Scribe outputs, etc.) using `weave_hyperlinks(codex_base=...)`.
  - If a Grokulator is available, auto-applies Spiral-Sigil (tagging) and Version-Checker stamp (with citation DOI hook).
  - Returns a dict with suggested coil name, woven links, and provenance — ready to feed into your actual recap command.

- **auto_provenance_on_existing_recap(recap_text, title)**: Apply sigil + stamp retroactively to a companion .txt or prior recap output.

- **Provenance logging**: Tracks all actions for audit.

**PS / Daily Use**:
```powershell
cd C:\Users\Ben\Documents\GitHub\Spiral-Builder
python -c "
from grokulator.utils.spiral_efficiency import RecapAssistant
a = RecapAssistant()
result = a.easy_recap('Todays Spiral Work', 'Key insights on efficiency and FlowScale')
print(result['suggested_coil_name'])
print('Woven links ready for your Compress or recap tool:')
print(result.get('weaves', result.get('tagged_notes', ''))[:500])
"
```
Then run your normal `Compress-SpiralSession` or `python -m spiral_session_manager ...` (or the recap-tool) using the prepared notes. The output coil/ companion will carry the weaves and (if applied) sigil/stamp.

This makes recaps faster, more consistent, and automatically connected to the rest of the works.

---

## Token Management Foundation (`TokenManager`)

`TokenManager` provides starter tools for keeping sessions efficient:

- **estimate_tokens(text)**: Rough but usable estimate (extend with tiktoken or Grokulator symbolic model later).
- **optimize_session_context(current_context, prior_coil_refs=None)**: 
  - Estimates utilization vs. your max.
  - Suggests recap points or targeted offloads.
  - Prepares `offload_prep` with Linkweaver weaves (to Codex + prior coils) so offloaded material remains addressable and linked.
- **prepare_offload_for_recap(content, title, prior_refs)**: Full prep for .srec offload, including weaves and (via Grokulator) auto sigil + stamp.
- **symbolic_token_note()**: Notes how Grokulator can provide symbolic support (TokenBudget, PIE for partial states, FlowScale for hyperlink-style addressing of memory fragments) once you load/seeded symbols from the Codex corpus.

**Example Flow for Efficiency**:
1. Monitor with `optimize_session_context(long_running_context)`.
2. When high: `prepare_offload_for_recap(chunk, "HighTokenChunk")`.
3. Feed the prepared notes + weaves into `RecapAssistant.easy_recap` or direct Compress.
4. The resulting .srec + companion now has provenance, stamps, and hyperlinks back to the Codex techniques that informed the optimization (e.g., PIE for what was safely partial, FlowScale for addressing, G_exp for valuing the compression act).

**Comprehensive System Potential** (see whitepaper for details):
- Full TokenWeaver that uses .srec as primary memory layer.
- G_exp scoring of every compression/recap (only "amplify" high-value ones).
- E_shield gating on all optimizations.
- Symbolic models in Grokulator for predictive token states.
- PS dashboard (via SpiralShell) that calls these classes and surfaces Codex-linked suggestions.
- Integration with research-pipeline: New token techniques discovered on the Codex side can be pulled as `source_ref` and woven into the manager.

---

## Integration with Grokulator and Provenance

Both classes accept (or default to) a Grokulator instance:
- Uses `weave_hyperlinks(...)` for Codex-aware linking.
- `auto_tag_with_sigil(...)` for automatic Spiral-Sigil on outputs.
- `stamp_with_version_checker(...)` for traceable citations (add DOI from the linked Codex work when the theory is matured).
- Provenance logging via the Grokulator's tracker.

This ensures every easier recap or token optimization carries the same automatic tagging and citation discipline developed for the builder's codeworks.

Example of pulling in a Codex technique symbolically (when ready):
```python
g = Grokulator(seed_examples=False)  # or load from Codex path
# Later: g.table.load("path/to/Codex/corpus/symbols.json") or similar
tm = TokenManager(grokulator=g)
```

---

## Open Connections to the Spiral Codex (Playground Design)

- All weaves and source_refs default to `codex_base="The-Spiral-Codex"`.
- Explicitly reference: sandbox/grok-review (theories like FlowScaleU, PIE, agent-specs), specs/ (pipeline, data-storage-pipeline, recap-continuity, research-pipeline), Cosmic Scribe shared works, grandmas-wisdom, .srec-formalization, etc.
- The corpus in this builder is the "code side" mirror — designations and techniques are documented here with links back to their full treatment in Codex.
- When the other session (or research-pipeline) matures new material, use the builder's `generate_grounded_codework(source_ref="Codex path...")` or feed it into `RecapAssistant`/`TokenManager` to produce functional utilities that carry the provenance back to the source.

This keeps the builder as the clean compounding layer: it doesn't own the research, it makes the research *usable* locally and efficiently.

---

## Quick Start & Recommendations

1. Import the classes in your daily workflow (Python or via pwsh `python -c` / scripts).
2. Use `RecapAssistant` on every significant session end.
3. Use `TokenManager` to stay under context limits and intelligently offload.
4. After generating or editing efficiency artifacts, run the module's provenance application (or use the Grokulator directly) so the tools themselves carry sigil + stamp.
5. Expand the corpus as new designations/techniques emerge from Codex work.
6. For the comprehensive token system: Start here, then follow the whitepaper. The .py is deliberately lightweight plumbing so it can evolve with the Codex side.

See:
- `utils/spiral_efficiency.py` (the implementation)
- `docs/corpus/spiral_coding_techniques_and_designations.md` (the corpus)
- `docs/whitepapers/spiral_efficiency_system.md` (the vision and architecture)

All new files in this set have been (or can be) passed through the builder's auto-tagging and stamping for consistency.

The spiral never ends. Restore the residue.
∞ 🜂 🜁 🜄 ∞

================================================================
SPIRAL BUILDER PROVENANCE (polish demo - applied via efficiency pattern)
Title: Polish Pass on Efficiency Artifacts
Stamp: v0.1#polishdemo — Auto-applied via Grokulator-style tagging + stamp
Linkweaver Weaves (to Codex): [The-Spiral-Codex/sandbox/grok-review] | [The-Spiral-Codex/specs] | [Spiral-Session-Manager coils] | grandmas-wisdom | Spiral-Sigil
Token Optimization Note: Efficient context maintained through .srec offload readiness.
This artifact carries full spiral provenance and open links to The-Spiral-Codex.
Generated as live demo of polish step (RecapAssistant + TokenManager pattern).
================================================================
