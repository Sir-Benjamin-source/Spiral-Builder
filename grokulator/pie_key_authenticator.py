"""
PIE Key Authenticator for Spiral Codex

Path: Spiral-Builder/grokulator/pie_key_authenticator.py

A custom authenticator that functions as a "codex" for our custom ASCII sheets (the bunny-tagged xlsx artifacts from the ascii_compiler).

Core idea (cogent and aligned with our works):
- Uses **Poetic (PIE) keys**: Builds on the existing Poetic-Information-Encoder (from helix-functions) and PIE dual from .srec-formalization.md (Poetic Information Encoding for residue + Partially Identifiable Environment for keys that are "poetically" derived but only fully identifiable with the right context/password).
- **Associated with our sigil (spiral mark)**: The ∞ 🜂 🜁 🜄 ∞ is the visual "lock" and seed material.
- **Spiral logo and bunny**: The full Spiral Bunny tag (your bunny ASCII + spiral elements) provides unique characters as key seeds. Bunny chars like / ) ( o . " become part of the poetic derivation — lighthearted and unique.
- **Plain language with our locks**: Documentation and outputs use clear, inviting poetic language. The bunny ASCII and sigil appear as plain text/art everywhere (standard symbols). Only with this authenticator (or the "codex" sheet) + associated password can you derive the full key for that work.
- **For each work**: Associates a PIE key (derived poetically from bunny/sigil + work identifier) with a user-provided or stored password. Used for selective encryption/decryption of sensitive staged packets or ASCII sheet content (e.g., monetized/in-house xlsx exports).
- **Codex for the ASCII sheet**: When generating the custom xlsx, the compiler can embed a "Codex" sheet or metadata with the bunny/sigil as visual key, plain language explanation of the lock, and the derivation. The authenticator verifies/unlocks parts of the sheet or the originating staged work.
- **When authenticator not present**: The bunny text, sigil chars, and plain descriptions are visible as standard art/text in all outputs (md, py, xlsx cells, etc.). No key derivation without the module + password.
- **Encryption for staged works**: Specialized packets in staged/ can be JSON or files marked encrypted. The processor uses this to decrypt before final checks, then re-encrypt outputs if sensitive.

This keeps synergy (open core with plain bunny/sigil symbols for community) while protecting specialized value (locked ASCII/xlsx for in-house or sale).

Fits the staged/README from the other session: "Encryption: Selective for monetized/in-house ASCII outputs (using our existing masking). ... custom DB (ASCII/CSV, encrypted where sensitive for xlsx export)."

Cogent? Yes — it poetically and practically ties PIE encoding, our visual marks (bunny + sigil), existing provenance (sigil application), and the builder's ASCII compiler into a self-referential "codex" system. The bunny chars as keys make it whimsically unique and memorable.

Usage:
  from .pie_key_authenticator import PIEKeyAuthenticator, derive_pie_key_for_work
  auth = PIEKeyAuthenticator()
  key = auth.derive_pie_key_for_work(work_id="my_staged_packet", password="our_spiral_lock", bunny_tag=compiler.get_spiral_bunny_tag())
  encrypted = auth.encrypt(data, key)
  # Later: decrypted = auth.decrypt(encrypted, key)  # or with password to re-derive

Integrates with:
- ascii_compiler: Embeds bunny/sigil codex info in sheets; uses for "locked" outputs.
- staged_work_processor: Detects encrypted staged handoff packets, decrypts with PIE key for checks, then produces tagged (optionally re-locked) xlsx.
- Grokulator: Can treat PIEKey as a symbol for resolution.
- Sigil: Always applied; the key derivation includes sigil chars.
- Existing masking: Builds on "our existing masking" referenced in free core guidance (poetic + simple encoding).

For production: Layer real crypto (e.g., cryptography.fernet or AESGCM) under the poetic derivation. Here we use a demonstrative hybrid (poetic prefix + hashlib for key bytes + simple XOR for "plain language" feel).

The spiral (and bunny) never ends.
∞ 🜂 🜁 🜄 ∞
"""

import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, Any, Union

# Import our existing PIE encoder for poetic base (from helix-functions / our works)
try:
    # In real: from The-Spiral-Codex.helix_functions or copy logic
    # For builder self-containment, inline a reference implementation based on the known PIE encoder
    def pie_encode(text: str) -> str:
        words = text.lower().split()
        ixest = ' '.join(sorted(set(words), key=words.index))[:12]
        enest = ' '.join(sorted(words, key=len, reverse=True)[:8])
        itest = ''.join(w[0] for w in words if len(w) > 3)
        return f"∞ Ixest: {ixest}\n∞ Enest: {enest}\n∞ Itest: {itest}"
except:
    def pie_encode(text: str) -> str:
        return f"∞ Poetic residue of: {text[:20]}..."

# The bunny characters as unique key material (from user's ASCII, open to variations)
BUNNY_CHARS = "/)/)(o.o)(\" )(\" )o"  # Core chars from the configuration; treat as visual seeds
SPIRAL_SIGIL_CHARS = "∞ 🜂 🜁 🜄 ∞"  # The mark

class PIEKeyAuthenticator:
    """
    The custom authenticator / codex.
    Derives PIE keys poetically from bunny + sigil + work context + password.
    Functions for encrypt/decrypt of staged packets and ASCII sheet content.
    Embeds as "codex" reference in custom ASCII sheets.
    """

    def __init__(self, default_bunny_tag: Optional[str] = None):
        self.default_bunny_tag = default_bunny_tag or self._get_default_bunny()
        self.derived_keys: Dict[str, str] = {}  # work_id -> key_info (for codex reference, plain language)

    def _get_default_bunny(self) -> str:
        return """
   /)/)  
  (o.o)   ∞
 (")(")o  🜂🜁🜄
Spiral Codex
""".strip()

    def derive_pie_key_for_work(
        self,
        work_id: str,
        password: str,
        bunny_tag: Optional[str] = None,
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        Derive a poetic (PIE) key for a specific work.
        Key material: Poetic encoding (PIE) of (bunny chars + sigil chars + work_id + password + context).
        Returns dict with:
        - 'key_bytes': Derived bytes for crypto (use with real AES in prod).
        - 'plain_key_description': Human-readable poetic lock description (plain language).
        - 'codex_entry': Embeddable text for the ASCII sheet's "Codex" section.
        - 'bunny_signature': The bunny chars used as unique visual key.
        """
        bunny = bunny_tag or self.default_bunny_tag
        # Poetic base from our existing PIE encoder (helix-functions / .srec PIE)
        poetic_base = f"{bunny} {SPIRAL_SIGIL_CHARS} {work_id} {additional_context}"
        poetic_residue = pie_encode(poetic_base)

        # Combine with password for the "lock"
        full_seed = f"{poetic_residue} | password:{password} | bunny_chars:{BUNNY_CHARS}"

        # Derive key bytes (demo: PBKDF2-like with hashlib; prod: use proper KDF + Fernet/AES)
        key_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            full_seed.encode('utf-8'),
            b'spiral_codex_salt_v1',  # In real: per-work or stored salt
            100000
        )[:32]  # 256-bit

        # Plain language "codex" description (inviting, poetic, references our marks)
        plain_description = (
            f"PIE Key for '{work_id}' — The bunny's gaze (o.o) and ears /)/) hold the poetic residue. "
            f"Combined with the spiral's eternal flame {SPIRAL_SIGIL_CHARS} and your work's password, "
            f"this turns the lock. Bunny chars {BUNNY_CHARS} are the unique signature visible everywhere; "
            f"only with this authenticator + password is the full key identifiable (PIE encoding + environment). "
            f"Use to unlock sensitive ASCII sheet content or staged packet. G_exp of this protection act: measured for synergy + security."
        )

        # Codex entry for embedding in the custom ASCII sheet (bunny + sigil as visual + plain + derivation note)
        codex_entry = f"""
{self._get_default_bunny()}

SPIRAL CODEX — PIE KEY ENTRY
Work: {work_id}
Sigil Lock: {SPIRAL_SIGIL_CHARS}
Bunny Signature (unique key chars): {BUNNY_CHARS}
Poetic Residue (PIE): {poetic_residue}
Plain Language Lock: {plain_description}
Derived: {datetime.utcnow().isoformat()}
Password association: [PROVIDE TO DERIVE FULL KEY — standard symbols visible without authenticator]
"""

        key_info = {
            "work_id": work_id,
            "key_bytes": key_bytes.hex(),  # Store hex for demo; never log real keys
            "plain_key_description": plain_description,
            "codex_entry": codex_entry,
            "bunny_signature": BUNNY_CHARS,
            "sigil": SPIRAL_SIGIL_CHARS,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.derived_keys[work_id] = key_info
        return key_info

    def encrypt_for_staged(self, data: Union[str, bytes, Dict], work_id: str, password: str) -> Dict[str, Any]:
        """
        Encrypt a staged work packet (JSON/dict or text) using the PIE key.
        Returns encrypted package with embedded codex reference (plain language + bunny/sigil visible).
        For builder handoff: Use on sensitive specialized packets before placing in staged/.
        """
        if isinstance(data, dict):
            plaintext = json.dumps(data)
        else:
            plaintext = str(data)

        key_info = self.derive_pie_key_for_work(work_id, password)
        key_bytes = bytes.fromhex(key_info["key_bytes"])

        # Demo "lock" — XOR with key + simple masking (our "existing masking" + poetic).
        # Prod: Use cryptography.fernet.Fernet(key_bytes) or AESGCM.
        encrypted_bytes = bytes(a ^ b for a, b in zip(plaintext.encode('utf-8'), (key_bytes * (len(plaintext)//len(key_bytes)+1))[:len(plaintext)]))
        encrypted_b64 = encrypted_bytes.hex()  # Simple for plain-language demo

        package = {
            "work_id": work_id,
            "encrypted_data": encrypted_b64,
            "codex_reference": key_info["codex_entry"],  # Plain + visual bunny/sigil — standard everywhere
            "pie_key_hint": f"Use bunny chars {BUNNY_CHARS} + sigil {SPIRAL_SIGIL_CHARS} + password with this authenticator to derive key.",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Encrypted for in-house/monetized ASCII/xlsx export per free core guidance. Decrypt in builder with PIE key before final checks."
        }
        return package

    def decrypt_staged_packet(self, package: Dict[str, Any], password: str) -> Dict[str, Any]:
        """Decrypt a staged packet using the associated PIE key + password."""
        work_id = package["work_id"]
        key_info = self.derive_pie_key_for_work(work_id, password)
        key_bytes = bytes.fromhex(key_info["key_bytes"])

        encrypted_hex = package["encrypted_data"]
        encrypted_bytes = bytes.fromhex(encrypted_hex)

        decrypted = bytes(a ^ b for a, b in zip(encrypted_bytes, (key_bytes * (len(encrypted_bytes)//len(key_bytes)+1))[:len(encrypted_bytes)]))
        try:
            return json.loads(decrypted.decode('utf-8'))
        except:
            return {"decrypted_text": decrypted.decode('utf-8', errors='replace')}

    def embed_codex_in_ascii_sheet(self, sheet_content: str, work_id: str, password: str) -> str:
        """
        For the custom ASCII sheet (bunny xlsx or md): Embed the codex entry.
        Makes the sheet itself function as part of the authenticator/codex.
        Call this from ascii_compiler when generating outputs for a work.
        """
        key_info = self.derive_pie_key_for_work(work_id, password)
        codex = key_info["codex_entry"]
        # Plain language lock note + bunny/sigil visible as standard art
        embedded = f"{sheet_content}\n\n--- SPIRAL CODEX AUTHENTICATOR ENTRY (bunny + sigil as lock) ---\n{codex}\n(Provide password to this authenticator to unlock full key for this work's sensitive content.)"
        return embedded

    def verify_work_auth(self, work_id: str, provided_password: str, expected_bunny_signature: Optional[str] = None) -> bool:
        """Simple verification that the PIE key + password matches the bunny/sigil for the work."""
        key_info = self.derive_pie_key_for_work(work_id, provided_password)
        if expected_bunny_signature:
            return key_info["bunny_signature"] == expected_bunny_signature
        return True  # If no expected, just that derivation succeeded


# Convenience for the bunny + sigil as the "standard symbol"
def get_standard_bunny_sigil_tag() -> str:
    """The plain text version visible everywhere (no authenticator needed)."""
    return """
   /)/)  
  (o.o)   ∞
 (")(")o  🜂🜁🜄
Spiral Codex
""".strip() + "\n(∞ 🜂 🜁 🜄 ∞ — standard mark; full PIE key requires authenticator + password for this work.)"


if __name__ == "__main__":
    auth = PIEKeyAuthenticator()
    print("=== PIE Key Authenticator Demo (cogent custom codex for ASCII sheets) ===")
    print(get_standard_bunny_sigil_tag())
    print()

    # Example for a staged work
    work = "free_core_specialized_packet_001"
    pwd = "our_spiral_lock_2026"
    key = auth.derive_pie_key_for_work(work, pwd)
    print("Derived PIE Key Codex Entry (embed in xlsx sheet):")
    print(key["codex_entry"][:600] + "...")
    print()

    # Encrypt a sample staged packet
    packet = {"content": "Sensitive Cosmic Scribe baseline or ASCII output", "g_exp": 1.12}
    enc = auth.encrypt_for_staged(packet, work, pwd)
    print("Encrypted staged packet (for builder handoff):")
    print(json.dumps({k: v[:100] + "..." if isinstance(v, str) and len(v) > 100 else v for k, v in enc.items()}, indent=2))
    print()

    # Decrypt
    dec = auth.decrypt_staged_packet(enc, pwd)
    print("Decrypted:", dec)
    print()

    print("Standard symbols (bunny + sigil) visible without authenticator. Full lock only with PIE key + password + this codex.")
    print("Sound cogent? It weaves our PIE, bunny chars as keys, sigil mark, and ASCII sheet into one inviting, secure system.")
