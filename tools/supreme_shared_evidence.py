"""Scoped shared-design references and exact Supreme archive identity checks."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import zipfile
import zlib

from pinmame_game_defs.jsonio import file_sha256, load_json
from supreme_shared_playfield import build_crosswalk

CROSSWALK = "evidence/excerpts/stern.supreme-x-stern.2018/shared-design-crosswalk.json.txt"
IDENTITY = "evidence/excerpts/stern.supreme-x-stern.2018/driver-map-identity.json.txt"
MANUAL_SOURCE = "supreme.shared-design.manual"
CROSSWALK_SOURCE = "supreme.shared-design.crosswalk"

DONOR_ASSEMBLIES = {
    "mech.trough": "p.22: 500-9820-4BALL Trough Assembly",
    "mech.launch": "p.22: 511-1013-02 Auto Launch Assembly",
    "mech.left-flipper": "p.22: 500-6543-13-ND Left Flipper Assembly",
    "mech.right-flipper": "p.22: 500-6543-03-ND Right Flipper Assembly",
    "mech.sling-combined": "p.22: separate Left Slingshot and Right Slingshot rows, both 500-9920-01",
    "mech.pop-combined": "p.22: 515-6459-04-ND Pop Bumper - Bottom Assembly; p.21: donor top-cap parts 516-0033-WHT and 516-6794-08",
    "mech.pop-bottom": "p.22: 515-6459-04-ND Pop Bumper - Bottom Assembly",
    "mech.drop-bank": "p.22: 500-7216-13 Drop Target Assembly",
    "mech.gate": "p.21: 511-5033-01 Electric Gate Assembly",
    "mech.spinner": "p.21: 511-7781-00 Spinner Assembly",
}


def hardware_references(crosswalk):
    """Return qualified donor text, never populated Supreme hardware fields."""
    notes = {}
    for section, collection, prefix in (("switches", "inputs", "sw"), ("coils", "outputs", "sol"), ("leds", "outputs", "lamp")):
        for row in crosswalk["sections"][section]["shared"]:
            if row["node"] != 8 or "manual_row" not in row:
                continue
            manual = row["manual_row"]
            page = 13 if section == "coils" else int(re.search(r"page(\d+)", row["manual_page"])[1])
            note = (f"Donor-only reference, not validated Supreme hardware: Spider-Man The Pin manual 780-50H8-00 p.{page}, "
                    f"ID {manual['ID']} {manual['Name']}, {manual['Address']}, type {manual['Type']}, part {manual['Part Number']}. "
                    f"This matches Supreme node {row['node']}, position {row['position']}, public {row['public_address']}. "
                    "Supreme fitment, harness wiring, polarity and quantities remain unconfirmed; the complete donor row is retained in the shared-design crosswalk.")
            if section == "switches" and row["public_address"] in (9, 11):
                note += " PinMAME synthesizes this public EOS state; the donor's printed physical leaf does not make the controller input physical."
            if section == "leds" and row["public_address"] in (1, 2, 3):
                note += " This reference concerns only the node-8 playfield row; the colliding node-1 cabinet emitter remains unconfirmed."
            notes[collection, f"{prefix}.{row['public_address']}"] = note
    return notes


def mechanism_reference(identifier):
    return (f"Shared-design candidate only: Spider-Man The Pin manual 780-50H8-00 {DONOR_ASSEMBLIES[identifier]}. "
            "The donor part, wiring, fitted quantity and complete physical behavior have not been confirmed for Supreme; no Supreme assembly part number is asserted from this reference.")


def source_rom_manifest(text):
    blocks = re.findall(r"ROM_START\(supreme_101\)(.*?)ROM_END", text, re.S)
    if len(blocks) != 1:
        raise ValueError("Expected one Supreme ROM manifest")
    rows = re.findall(r'ROM_LOAD\("([^\"]+)",\s*0x[\da-fA-F]+,\s*0x([\da-fA-F]+),\s*CRC\(([\da-fA-F]+)\)\s*SHA1\(([\da-fA-F]+)\)\)', blocks[0])
    result = {name: {"size": int(size, 16), "crc32": crc.lower(), "sha1": sha.lower()} for name, size, crc, sha in rows}
    if len(rows) != 10 or len(result) != len(rows):
        raise ValueError("Supreme source manifest must contain ten distinct payloads")
    return result


def verify_rom_archive(archive, source, identity):
    """Recompute all payload digests, not merely ZIP central-directory metadata."""
    if file_sha256(source) != identity["source"]["sha256"]:
        raise ValueError("Supreme current source hash mismatch")
    expected = source_rom_manifest(source.read_text(encoding="utf-8"))
    indexed = {row["name"]: row for row in identity["members"]}
    if len(indexed) != 10 or len(identity["members"]) != 10 or set(indexed) != set(expected):
        raise ValueError("Supreme indexed payload inventory mismatch")
    for name, row in expected.items():
        if any(indexed[name][key] != value for key, value in row.items()):
            raise ValueError(f"{name}: indexed identity disagrees with current source")
    if archive.stat().st_size != identity["archive"]["bytes"] or file_sha256(archive) != identity["archive"]["sha256"]:
        raise ValueError("Supreme archive identity mismatch")
    with zipfile.ZipFile(archive) as stream:
        members = [entry for entry in stream.infolist() if not entry.is_dir()]
        if len(members) != 10 or {entry.filename for entry in members} != set(expected):
            raise ValueError("Supreme ZIP payload inventory mismatch")
        for entry in members:
            crc = size = 0
            sha1, sha256 = hashlib.sha1(), hashlib.sha256()
            with stream.open(entry) as payload:
                while chunk := payload.read(1024 * 1024):
                    size += len(chunk)
                    crc = zlib.crc32(chunk, crc)
                    sha1.update(chunk)
                    sha256.update(chunk)
            actual = {"size": size, "crc32": f"{crc & 0xffffffff:08x}", "sha1": sha1.hexdigest(), "sha256": sha256.hexdigest()}
            if any(indexed[entry.filename][key] != value for key, value in actual.items()):
                raise ValueError(f"{entry.filename}: independently decompressed payload identity mismatch")


def _external_uri(working, uri):
    if not uri.startswith("working-root:"):
        raise ValueError("Expected a retained working-root source")
    path = (working / uri.removeprefix("working-root:")).resolve()
    if not path.is_relative_to(working.resolve()):
        raise ValueError("Retained source escapes the working root")
    return path


def verify_external(root):
    manual_root = os.environ.get("PINMAME_MANUALS_ROOT")
    if manual_root:
        manual = Path(manual_root) / "by-machine/stern.spider-man-the-pin.2016/official-stern/Spider-Man_ThePin_web.pdf"
        if file_sha256(manual) != "5bfe21f7c3f0a71823ca225612d9514604347c6b2d37978c128954a9b87a49b5":
            raise ValueError("Shared-design donor manual hash mismatch")
    review_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review_root:
        working = Path(review_root).resolve().parent
        identity = load_json(root / IDENTITY)
        verify_rom_archive(_external_uri(working, identity["archive"]["uri"]), _external_uri(working, identity["source"]["uri"]), identity)


def verify_contract(root, definition):
    crosswalk = build_crosswalk(root)
    if crosswalk != load_json(root / CROSSWALK):
        raise ValueError("Supreme shared-design comparison drift")
    if definition["machine"]["id"] != "stern.supreme-x-stern.2018" or [d["id"] for d in definition["drivers"]] != ["supreme_101"]:
        raise ValueError("Supreme exact driver ownership changed")
    if "driver_mapping" in definition["coverage"]["missing"]:
        raise ValueError("Supreme exact driver mapping must reflect the verified archive/catalog")
    devices = {(collection, d["id"]): d for collection in ("inputs", "outputs") for d in definition[collection]}
    for key, note in hardware_references(crosswalk).items():
        device = devices[key]
        if note not in device.get("physical", {}).get("notes", ""):
            raise ValueError(f"{key}: qualified donor reference missing")
        if not {MANUAL_SOURCE, CROSSWALK_SOURCE} <= set(device["provenance"]["source_refs"]):
            raise ValueError(f"{key}: donor reference provenance missing")
    mechanisms = {m["id"]: m for m in definition["mechanisms"]}
    for identifier in DONOR_ASSEMBLIES:
        if mechanism_reference(identifier) not in mechanisms[identifier]["behavior"]:
            raise ValueError(f"{identifier}: donor assembly qualification missing")
    verify_external(root)
    return crosswalk
