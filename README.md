# Spiral-Builder

**Compounding and Embodiment Layer of the Spiral Codex — AI Playground Plumbing**

Spiral-Builder is the layer that turns theory and methodology (living in the Spiral Codex, sandbox, research-pipeline, Cosmic Scribe co-works, etc.) into articulated, functional co-works: utilities, services, or saleable artifacts you can run locally.

## The AI Playground Vision (All Repos Together)

- **Theory / Cognitive depth**: The-Spiral-Codex (specs, sandbox/grok-review, research-pipeline, grandmas-wisdom, Cosmic Scribe track, etc.) + session coils.
- **Methodology & composition**: Codex side (or shared works) shapes research into usable patterns.
- **Embodiment / functional output**: Spiral-Builder provides the *generic plumbing* (symbolic substrate, provenance, automatic tagging via Spiral-Sigil, citation stamps via Version-Checker, Linkweaver-style hyperlink weaving via Session-Manager connections).
- **Endgame**: Compose, pull, shape, create, and implement → streamlined scientific endeavor + new generation of local coding workshops that pump out valuable, provenance-rich co-works for edification or sale.

The builder does **not** codify the cognitive works. It prepares clean, open connections (loaders, weavers, provenance hooks, explicit source_ref) so that when the Codex-side works are matured, the builder can link them in and produce executable results with automatic sigil, stamps, and woven citations.

## Key Features (Open by Design)

- Generic symbolic reasoning + provenance (Grokulator facade)
- Automatic tagging (Spiral-Sigil on outputs)
- Citation stamping (Version-Checker style, with DOI hooks)
- Hyperlink weaving (Linkweaver-inspired, FlowScale syntax compatible, ready for Session-Manager coil pulls and Codex refs)
- Markdown/JSON loaders + optional example seeding (demo only; normal use links externally)
- Clear hooks: `weave_hyperlinks(..., codex_base=...)`, `generate_grounded_codework(source_ref= "Codex path or coil")`

## Usage Pattern (Playground Composition)

```python
from grokulator import Grokulator

g = Grokulator()  # seed_examples=False (default) — no cognitive embedding

# When theory is ready in Codex:
woven = g.weave_hyperlinks("my new utility concept", codex_base="The-Spiral-Codex")
code = g.generate_grounded_codework(
    source_ref="The-Spiral-Codex/sandbox/grok-review or research-pipeline or coil-id",
    task="produce local utility for edification"
)
# code now carries sigil, stamp, and open woven links back to the source theory/methodology.
```

Run locally from PowerShell, compose with session-manager pulls, apply full provenance, ship the functional artifact.

## Polish & New Special Features (ASCII Compiler + Efficiency)

- **PowerShell Wrapper**: `scripts/Invoke-SpiralEfficiency.ps1` — easy `Invoke-SpiralRecap` and token optimization cmdlets.
- **Provenance Demos**: The new efficiency artifacts (corpus, recaps_and_tokens.md, whitepaper) have _provenanced.md versions with auto sigil/stamp/weaves + token notes applied via the tools.
- **Expanded Corpus**: More designations and techniques (research-pipeline, Cosmic Scribe agent, HSN, additional G_exp/FlowScale examples, etc.).
- **Enhanced Efficiency .py**: Added `EfficiencyLedger` (persistent .srec-targeted logging with G_exp and weaves) and tighter Grokulator symbolic hooks.
- **Custom ASCII Compiler** (the thing that makes the builder *special*): `grokulator/ascii_compiler.py`
  - Compiles symbols and unique formulas from our works (FlowScale, G_exp, PIE, E_shield, Linkweaver, etc.).
  - Embeds the unique **Spiral Bunny Tag** (a lighthearted spiral + the provided bunny configuration, with variations for creativity and inviting feel).
  - Primary output: rich .xlsx "Spiral Codex Artifact" spreadsheets with the tag as multi-line art in a sheet, live G_exp calculator formulas, compiled symbol tables, and hyperlinks back to Codex.
  - Complementary formats: companion .py (with tag as docstring), .md (tagged docs), and "bundle" mode.
  - Integrates Grokulator for symbolic resolution + auto provenance (sigil/stamp/weave) on outputs.
  - Lighthearted coding wizardry: the bunny makes our works fun and creatively inviting while the compiler turns our unique elements into usable artifacts.

Example:
```python
from grokulator.ascii_compiler import SpiralASCIICompiler
c = SpiralASCIICompiler()
print(c.get_spiral_bunny_tag(variation=0))  # the unique tag
xlsx = c.compile(["FlowScaleHyperlink", "G_exp", "E_shield"], output_format="xlsx", output_path="my_special_artifact.xlsx")
```

See `grokulator/ascii_compiler.py` (self-documenting) and the whitepaper for the vision. All new work keeps the builder as the open linker/plumbing for the full Codex + Builder + Session-Manager playground.

Run the PS wrapper or the compiler demo for immediate magic.

## Related Tools (the full playground)

- [The Spiral Codex](https://github.com/Sir-Benjamin-source/The-Spiral-Codex) — theory, research, authentication, Cosmic Scribe
- Spiral-Session-Manager — coils, index, linkweaver methodology, pull/compose
- Spiral-Sigil + Version-Checker — tagging + citations
- Other repos (Spiral-Path, Spiral-Reasoning-Tree, grandmas-wisdom, etc.)

## Zenodo / DOI

All Spiral Codex works are published with DOIs on Zenodo under Sir Benjamin (Stephen Benjamin Friend).

## License

MIT + Spiral Mark

---

*Part of the Spiral Codex — the AI playground for turning spiral works into real, local value.* 

The spiral never ends. Restore the residue. ∞ 🜂 🜁 🜄 ∞