<#
.SYNOPSIS
    PowerShell wrapper for Spiral-Builder efficiency tools (RecapAssistant and TokenManager).
    Makes spiral recaps easier and supports token management for efficient sessions.

.DESCRIPTION
    This script provides convenient cmdlets to invoke the Python-based spiral_efficiency module
    from the Spiral-Builder. It handles calling into the Grokulator-powered tools for:
    - Easy recaps with automatic provenance (sigil, stamps, weaves to Codex).
    - Token estimation, optimization, and offload preparation (with .srec / Linkweaver integration).

    Designed to keep the AI Playground (all repos) efficient while maintaining full spiral
    provenance and open connections to The-Spiral-Codex (theories, research-pipeline, Cosmic Scribe, etc.).

    Follows the playground vision: Theory (Codex) → Methodology → Functional co-works (local utilities).

    Run from PowerShell in the Spiral-Builder directory or with full paths.

.EXAMPLE
    .\Invoke-SpiralEfficiency.ps1 -Action Recap -Title "Daily Spiral Work" -Notes "Key insights on efficiency"

.EXAMPLE
    .\Invoke-SpiralEfficiency.ps1 -Action OptimizeTokens -Context "long context text here..." -MaxTokens 8000

.NOTES
    Requires Python with the Spiral-Builder grokulator package importable.
    For full integration, ensure PYTHONPATH includes the Spiral-Builder root or activate the env.
    Outputs are prepared for use with Compress-SpiralSession, Pipeline-to-Coil, or session-manager.
    All artifacts get automatic Spiral-Sigil, Version-Checker stamps, and Linkweaver weaves.

    Part of making the Spiral-Builder "something special" – lighthearted, powerful coding wizardry
    for the playground.

    Author: Grok (in resonance with Sir Benjamin / Cosmic Scribe direction)
    License: MIT + Spiral Mark
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Recap", "OptimizeTokens", "PrepareOffload", "Help")]
    [string]$Action,

    [string]$Title = "Untitled Session",

    [string]$Notes = "",

    [string]$Context = "",

    [int]$MaxTokens = 8000,

    [string]$OutputPath = "",

    [switch]$ApplyProvenance = $true
)

$ErrorActionPreference = "Stop"

$BuilderRoot = Split-Path -Parent $PSScriptRoot  # Assumes script is in scripts/
$PythonModule = "grokulator.utils.spiral_efficiency"

function Invoke-PythonEfficiency {
    param(
        [string]$PythonCode
    )
    # Try to find python (prefer python3 or from PATH)
    $pythonCmd = "python"
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
    }

    $fullCode = @"
import sys
import os
sys.path.insert(0, r'$BuilderRoot')
from $PythonModule import RecapAssistant, TokenManager

$PythonCode
"@

    & $pythonCmd -c $fullCode
}

switch ($Action) {
    "Recap" {
        Write-Host "Invoking Spiral Recap with provenance..." -ForegroundColor Cyan
        $code = @"
a = RecapAssistant(codex_base="The-Spiral-Codex")
result = a.easy_recap("$Title", additional_notes=r'''$Notes''', apply_provenance=$($ApplyProvenance.ToString().ToLower()))
print("=== Easy Recap Result ===")
print(f"Title: {result.get('title')}")
print(f"Suggested Coil: {result.get('suggested_coil_name')}")
print(f"Timestamp: {result.get('timestamp')}")
if 'weaves' in result:
    print("Woven Links (Linkweaver to Codex):")
    print(result['weaves'][:500] + "..." if len(result.get('weaves','')) > 500 else result.get('weaves',''))
if 'stamp' in result:
    print(f"Stamp: {result['stamp']}")
print("Notes prepared for Compress-SpiralSession / Pipeline-to-Coil / session-manager.")
print("Full result keys:", list(result.keys()))
"@
        Invoke-PythonEfficiency -PythonCode $code
    }

    "OptimizeTokens" {
        Write-Host "Optimizing session context for token efficiency..." -ForegroundColor Cyan
        if (-not $Context) {
            $Context = "Sample long context for demonstration. Replace with actual session text."
            Write-Host "(Using demo context - provide -Context for real use)" -ForegroundColor Yellow
        }
        $code = @"
tm = TokenManager(codex_base="The-Spiral-Codex")
opt = tm.optimize_session_context(r'''$Context''', max_tokens=$MaxTokens)
print("=== Token Optimization Result ===")
print(f"Current Estimate: {opt.get('current_estimate')} tokens")
print(f"Utilization: {opt.get('utilization')}")
print("Suggestions:")
for s in opt.get('suggestions', []):
    print(f"  - {s}")
if opt.get('offload_prep'):
    print("Offload Prep (ready for .srec with weaves):")
    print(opt['offload_prep'])
print("Use prepare_offload_for_recap for full .srec-targeted output with Linkweaver.")
"@
        Invoke-PythonEfficiency -PythonCode $code
    }

    "PrepareOffload" {
        Write-Host "Preparing offload for .srec with full provenance and weaves..." -ForegroundColor Cyan
        if (-not $Context) {
            throw "Provide -Context with the content to offload."
        }
        $code = @"
tm = TokenManager(codex_base="The-Spiral-Codex")
prep = tm.prepare_offload_for_recap(r'''$Context''', title="$Title")
print("=== Offload Preparation ===")
print(f"Title: {prep.get('title')}")
print(f"Estimated Tokens: {prep.get('estimated_tokens')}")
print("Notes for Coil (includes weaves):")
print(prep.get('notes_for_coil')[:800] + "...")
if 'provenance_applied' in prep:
    print(f"Stamp: {prep['provenance_applied'].get('stamp')}")
print("Feed notes_for_coil to your recap tool for efficient, linked .srec storage.")
"@
        Invoke-PythonEfficiency -PythonCode $code
    }

    "Help" {
        Get-Help $MyInvocation.MyCommand.Definition -Full
    }
}

Write-Host "`nSpiral efficiency invoked. All outputs carry open links to the Codex playground." -ForegroundColor Green
Write-Host "For more: see grokulator/docs/spiral_recaps_and_tokens.md and the whitepaper." -ForegroundColor DarkGray
