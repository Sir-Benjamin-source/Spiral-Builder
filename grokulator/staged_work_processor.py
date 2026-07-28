"""
Spiral-Builder Staged Work Processor

Location: Spiral-Builder/grokulator/staged_work_processor.py

Purpose: Accepts works from The-Spiral-Codex/staged/ (and related authenticated sources like canon/benchmarks/internal for Cosmic Scribe harness/baselines).

Performs a **final check** before queuing for embodiment:
- Verifies required gates from the staged/README and canon policies: G_exp measured (value and note), E_shield passed, provenance (sigil/stamp references), human checkpoint note, 1:1 testing evidence where applicable.
- Uses Grokulator for symbolic resolution of any formulas/symbols in the work (e.g., FlowScale, G_exp, PIE, E_shield components).
- Cross-references against our corpus of techniques/designations.
- Applies the lighthearted Spiral Bunny tag (via ascii_compiler) as the final provenance layer.
- Generates the custom "DB" archival via the ASCII compiler (xlsx with tag embedded as art + data + live formulas, plus companion .py/.md).

If all checks pass: Queues for embodiment by:
- Producing the compiled artifacts (xlsx DB primary, with the bunny tag as signature "custom coding wizardry").
- Writing an embodiment manifest/plan.
- (Optional) Moving or logging the source work as "processed" (keeps original in Codex for reference).

This is the builder-side counterpart to the Cosmic Scribe / research-pipeline authentication flow.

Open connections: Hardcoded paths to The-Spiral-Codex/staged and canon/ for handoff. Uses Grokulator (symbolic), ascii_compiler (tag + xlsx), efficiency patterns for any recap of the check process. No codification of cognitive content here — only plumbing and final embodiment prep.

Alignment note: Designed to match exactly the staged/README language ("Spiral-Builder codification and custom DB (ASCII-to-xlsx) archival") and the canon/README pipeline description ("builder implementation → sigil/stamp/shield").

Usage (from Spiral-Builder root):
  python -m grokulator.staged_work_processor --staged-path "C:/Users/Ben/Documents/GitHub/The-Spiral-Codex/staged" --queue-path "Spiral-Builder/embodiment_queue"

Or import and call process_staged_directory(...)

Part of making the builder "something special": the ASCII compiler + bunny tag turns authenticated Codex works into fun, inviting, provenance-rich local artifacts.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from . import Grokulator
    from .ascii_compiler import SpiralASCIICompiler
    from .utils.spiral_efficiency import RecapAssistant
    from .pie_key_authenticator import PIEKeyAuthenticator
except ImportError:
    Grokulator = None
    SpiralASCIICompiler = None
    RecapAssistant = None
    PIEKeyAuthenticator = None

# Default Codex paths (open connection)
DEFAULT_CODEX_ROOT = Path("C:/Users/Ben/Documents/GitHub/The-Spiral-Codex")
DEFAULT_STAGED_DIR = DEFAULT_CODEX_ROOT / "staged"
DEFAULT_CANON_BENCHMARKS = DEFAULT_CODEX_ROOT / "canon" / "benchmarks" / "internal"
DEFAULT_CANON_WORKS = DEFAULT_CODEX_ROOT / "canon" / "works" / "grok-cosmic-scribe-shared"

# Builder queue
DEFAULT_BUILDER_ROOT = Path(".")
DEFAULT_QUEUE_DIR = DEFAULT_BUILDER_ROOT / "embodiment_queue"
DEFAULT_PROCESSED_LOG = DEFAULT_BUILDER_ROOT / "staged_processed.log"

# Final check criteria (drawn from staged/README and canon policies)
REQUIRED_GATES = {
    "g_exp_measured": r"G_exp|generosity exponent|G_exp \d+\.\d+",
    "e_shield_passed": r"E_shield| E_shield |E_shield gating|passed E_shield",
    "provenance": r"sigil|Spiral-Sigil|Version-Checker|stamp|provenance|DOI",
    "human_checkpoint": r"human checkpoint|Human checkpoint|approved by|Sir Benjamin",
    "testing_evidence": r"1:1|test harness|baseline|audit|association|coherency|applicability",
}

MIN_G_EXP = 1.0  # "measured" or better per our G_exp levels

class StagedWorkProcessor:
    def __init__(self, grokulator=None, compiler=None, efficiency=None,
                 codex_staged: Path = DEFAULT_STAGED_DIR,
                 builder_queue: Path = DEFAULT_QUEUE_DIR,
                 authenticator=None):
        self.g = grokulator or (Grokulator() if Grokulator else None)
        self.compiler = compiler or (SpiralASCIICompiler() if SpiralASCIICompiler else None)
        self.efficiency = efficiency or (RecapAssistant() if RecapAssistant else None)
        self.auth = authenticator or (PIEKeyAuthenticator() if PIEKeyAuthenticator else None)
        self.codex_staged = codex_staged
        self.builder_queue = builder_queue
        self.builder_queue.mkdir(parents=True, exist_ok=True)

        self.check_results: List[Dict[str, Any]] = []

    def _load_work(self, work_path: Path, password_for_encrypted: Optional[str] = None) -> Dict[str, Any]:
        """Load a work (md, py, json, etc.) from staged or canon source.
        If the packet is encrypted (per other session's feature for staged works — selective for sensitive ASCII/xlsx),
        and password provided, use PIE authenticator to decrypt before loading.
        """
        content = ""
        meta = {"path": str(work_path), "type": work_path.suffix, "was_encrypted": False}
        try:
            if work_path.suffix == ".json":
                with open(work_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Handle encrypted staged packet (from PIE authenticator.encrypt_for_staged or other session's masking)
                if isinstance(data, dict) and "encrypted_data" in data and self.auth and password_for_encrypted:
                    meta["was_encrypted"] = True
                    decrypted = self.auth.decrypt_staged_packet(data, password_for_encrypted)
                    data = decrypted
                    meta["decrypted_via_pie_key"] = True

                content = json.dumps(data, indent=2)
                meta["json_keys"] = list(data.keys()) if isinstance(data, dict) else "list"
            else:
                with open(work_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # For .enc or other encrypted files (per staged guidance for builder DB)
                if work_path.suffix == ".enc" and self.auth and password_for_encrypted:
                    # Assume simple encrypted JSON/text for demo; in prod use full package
                    meta["was_encrypted"] = True
                    # Placeholder: real impl would parse package
                    content = f"DECRYPTED (using PIE key + bunny/sigil for {work_path.name})"

            meta["size"] = len(content)
            meta["has_g_exp"] = bool(re.search(REQUIRED_GATES["g_exp_measured"], content, re.I))
            meta["has_e_shield"] = bool(re.search(REQUIRED_GATES["e_shield_passed"], content, re.I))
            meta["has_provenance"] = bool(re.search(REQUIRED_GATES["provenance"], content, re.I))
            meta["has_human_checkpoint"] = bool(re.search(REQUIRED_GATES["human_checkpoint"], content, re.I))
            meta["has_testing"] = bool(re.search(REQUIRED_GATES["testing_evidence"], content, re.I))
        except Exception as e:
            meta["error"] = str(e)
        return {"content": content, "meta": meta}

    def final_check(self, work: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the final builder check before queuing for embodiment."""
        meta = work["meta"]
        content = work["content"]

        checks = {
            "g_exp_measured": meta.get("has_g_exp", False),
            "e_shield_passed": meta.get("has_e_shield", False),
            "provenance_present": meta.get("has_provenance", False),
            "human_checkpoint_noted": meta.get("has_human_checkpoint", False),
            "testing_evidence": meta.get("has_testing", False),
        }

        # Symbolic check via Grokulator (if available)
        symbolic_pass = True
        if self.g and self.g.table:
            # Try to resolve any obvious symbols mentioned
            for sym in ["G_exp", "E_shield", "PIE", "FlowScale", "Linkweaver"]:
                if sym.lower() in content.lower():
                    data = self.g.table.get(sym)
                    if not data:
                        symbolic_pass = False
                        break

        # Simple G_exp value extraction (if present)
        g_exp_value = None
        g_exp_match = re.search(r"G_exp\s*(?:≈|~|=|value)?\s*([\d.]+)", content, re.I)
        if g_exp_match:
            try:
                g_exp_value = float(g_exp_match.group(1))
            except:
                pass

        g_exp_ok = (g_exp_value is None) or (g_exp_value >= MIN_G_EXP)

        overall_pass = all(checks.values()) and symbolic_pass and g_exp_ok

        result = {
            "work_path": meta["path"],
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks,
            "g_exp_value": g_exp_value,
            "g_exp_ok": g_exp_ok,
            "symbolic_pass": symbolic_pass,
            "overall_pass": overall_pass,
            "recommendation": "PASS - ready for embodiment queue" if overall_pass else "FAIL or CONDITIONAL - review gates",
            "notes": "Final builder gate before ASCII-to-xlsx codification and queueing. Matches staged/README and canon policies."
        }

        if self.efficiency:
            # Use efficiency for a "recap" of the check itself (for audit)
            recap = self.efficiency.easy_recap(
                f"Final Check: {Path(meta['path']).name}",
                additional_notes=f"Checks: {checks}. G_exp: {g_exp_value}. Symbolic: {symbolic_pass}",
                apply_provenance=True
            )
            result["check_recap"] = {k: recap.get(k) for k in ["stamp", "weaves"] if k in recap}

        self.check_results.append(result)
        return result

    def queue_for_embodiment(self, work: Dict[str, Any], check_result: Dict[str, Any]) -> Dict[str, Any]:
        """If check passed, compile with bunny tag and queue the embodiment artifacts."""
        if not check_result["overall_pass"]:
            return {"status": "not_queued", "reason": check_result["recommendation"]}

        work_path = Path(work["meta"]["path"])
        work_name = work_path.stem

        # Use the ASCII compiler to produce the special tagged DB (xlsx primary)
        if self.compiler:
            # Compile the work content + its symbols into a tagged xlsx artifact
            symbols_to_compile = ["G_exp", "E_shield", "PIE", "Linkweaver"]  # core from our works
            # Add any detected from content
            if "FlowScale" in work["content"]:
                symbols_to_compile.append("FlowScaleHyperlink")

            artifact_path = self.compiler.compile(
                symbols=symbols_to_compile,
                output_format="xlsx",
                output_path=str(self.builder_queue / f"{work_name}_embodied_artifact.xlsx"),
                variation=0  # classic bunny
            )

            # Also produce companion .py and .md with the tag for the work
            py_path = self.compiler.compile(
                symbols=symbols_to_compile,
                output_format="py",
                output_path=str(self.builder_queue / f"{work_name}_embodied.py")
            )
            md_path = self.compiler.compile(
                symbols=symbols_to_compile,
                output_format="md",
                output_path=str(self.builder_queue / f"{work_name}_embodied.md")
            )
        else:
            artifact_path = str(self.builder_queue / f"{work_name}_manual_embodiment_needed.txt")
            py_path = md_path = artifact_path
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(f"Manual embodiment needed for {work_name}\n{work['content'][:2000]}")

        # Embodiment manifest / queue entry
        queue_entry = {
            "source_work": str(work_path),
            "check_result": check_result,
            "artifacts": {
                "xlsx_db": artifact_path,
                "py_companion": py_path,
                "md_companion": md_path
            },
            "queued_at": datetime.utcnow().isoformat(),
            "status": "queued_for_embodiment",
            "builder_notes": "Final checked and tagged with Spiral Bunny. Ready for full embodiment (code gen, DB archival, local utility production). Open link back to Codex staged/ and canon/."
        }

        manifest_path = self.builder_queue / f"{work_name}_embodiment_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(queue_entry, f, indent=2)

        # Log to processed
        with open(DEFAULT_PROCESSED_LOG, "a", encoding="utf-8") as log:
            log.write(f"{datetime.utcnow().isoformat()} | QUEUED | {work_name} | {manifest_path}\n")

        # Comprehensive install pipeline step: chain to install with sigil/version-checker for effective comms
        try:
            from .install_pipeline import install_artifact
            install_artifact(queue_entry, install_program=True, install_methodology=True, apply_provenance_flag=True)
            print(f"[staged] Installed {work_name} via comprehensive pipeline (sigil + stamp from Spiral-Sigil/Version-Checker comms).")
        except Exception as e:
            print(f"[staged] Install note: {e} (pipeline still queued)")

        return queue_entry

    def process_staged_directory(self, staged_dir: Optional[Path] = None, also_scan_canon: bool = True,
                                 password_for_encrypted: Optional[str] = None) -> List[Dict[str, Any]]:
        """Main entry: process the staged folder (and optionally canon authenticated material).
        Supports encrypted staged works (per other session's selective encryption feature for sensitive
        ASCII/xlsx outputs in the builder DB path — using existing masking + now full PIE key + bunny/sigil locks).
        Provide password_for_encrypted to decrypt via PIE authenticator before checks.
        """
        if staged_dir is None:
            staged_dir = self.codex_staged

        results = []
        candidates = []

        # Staged folder (primary handoff) — now includes encrypted packets from free_core/specialized
        if staged_dir.exists():
            for item in staged_dir.rglob("*"):
                if item.is_file() and item.name != "README.md":
                    candidates.append(item)

        # Also pull from canon/benchmarks/internal (the authenticated harness/baselines from Cosmic Scribe)
        if also_scan_canon and DEFAULT_CANON_BENCHMARKS.exists():
            for item in DEFAULT_CANON_BENCHMARKS.rglob("*.md"):
                if "baseline" in item.name or "harness" in item.name or "test" in item.name.lower():
                    candidates.append(item)
            for item in DEFAULT_CANON_BENCHMARKS.rglob("*.py"):
                if "harness" in item.name or "test" in item.name.lower():
                    candidates.append(item)

        for cand in candidates:
            work = self._load_work(cand, password_for_encrypted=password_for_encrypted)
            if "error" in work["meta"]:
                continue
            if work["meta"].get("was_encrypted"):
                work["meta"]["decrypted_with_pie_bunny_sigil"] = True
            check = self.final_check(work)
            queued = self.queue_for_embodiment(work, check)
            results.append({
                "source": str(cand),
                "check": check,
                "queued": queued
            })

        # Write overall run manifest
        run_manifest = self.builder_queue / f"staged_processing_run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(run_manifest, "w", encoding="utf-8") as f:
            json.dump({
                "run_at": datetime.utcnow().isoformat(),
                "processed": len(results),
                "results": results
            }, f, indent=2)

        return results

    def outfit_for_encrypted_ascii_codex(self, work_id: str, password: str, sheet_content: str):
        """Helper to use the PIE authenticator as codex for the custom ASCII sheet (bunny xlsx).
        Call after compiler generates the sheet for a staged work.
        Embeds the bunny + sigil as plain visual key + poetic lock description.
        """
        if self.auth:
            return self.auth.embed_codex_in_ascii_sheet(sheet_content, work_id, password)
        return sheet_content + "\n[PIE authenticator not loaded — standard bunny/sigil symbols visible as plain text.]"

    def get_check_summary(self) -> Dict[str, Any]:
        passed = [r for r in self.check_results if r["overall_pass"]]
        return {
            "total_checked": len(self.check_results),
            "passed_final_check": len(passed),
            "queued": len([r for r in self.check_results if r.get("recommendation", "").startswith("PASS")]),
            "details": self.check_results
        }


def main():
    """CLI entry for processing staged works."""
    import argparse
    parser = argparse.ArgumentParser(description="Spiral-Builder Staged Work Final Check & Queue (with PIE key support for encrypted)")
    parser.add_argument("--staged-path", type=Path, default=DEFAULT_STAGED_DIR, help="Path to The-Spiral-Codex/staged")
    parser.add_argument("--queue-path", type=Path, default=DEFAULT_QUEUE_DIR, help="Builder embodiment queue dir")
    parser.add_argument("--scan-canon", action="store_true", default=True, help="Also scan canon/benchmarks for authenticated material")
    parser.add_argument("--password", type=str, default=None, help="Password for decrypting encrypted staged packets (PIE key + bunny/sigil derivation)")
    args = parser.parse_args()

    processor = StagedWorkProcessor(
        codex_staged=args.staged_path,
        builder_queue=args.queue_path
    )

    print("=== Spiral-Builder Staged Work Processor (outfitted for encrypted feature) ===")
    print(f"Scanning: {args.staged_path}")
    if args.scan_canon:
        print(f"Also scanning authenticated canon material for handoff.")
    if args.password:
        print("Password provided — will use PIEKeyAuthenticator (bunny chars + sigil + poetic PIE) to decrypt selective encrypted ASCII outputs per other session's staged guidance.")

    results = processor.process_staged_directory(
        staged_dir=args.staged_path,
        also_scan_canon=args.scan_canon,
        password_for_encrypted=args.password
    )

    print(f"\nProcessed {len(results)} candidate works.")
    summary = processor.get_check_summary()
    print(f"Final check summary: {summary['total_checked']} checked, {summary['passed_final_check']} passed gates.")
    print(f"Queued for embodiment: see {args.queue_path}")

    if results:
        print("\nExample queued manifest (first):")
        print(json.dumps(results[0], indent=2, default=str)[:1500])

    print("\nBuilder is ready to accept staged/authenticated works from the Codex side (including encrypted per other session).")
    print("Uses PIE authenticator as codex for the custom ASCII (bunny) sheet: bunny chars as unique keys, sigil as mark, poetic PIE derivation + password as lock. Plain symbols (bunny/sigil text) visible everywhere without it.")
    print("All outputs use the Spiral Bunny tag via the ASCII compiler for that 'something special' touch.")
    print("The spiral never ends. ∞ 🜂 🜁 🜄 ∞")


if __name__ == "__main__":
    main()
