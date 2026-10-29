"""Reproduce the reviewed TX-Sector definition and its evidence audit.

The seed is reviewed factual data, not an import of another machine. External
sources are optional for ordinary regeneration; when configured, they must
match their pinned hashes and complete extraction manifest before any write.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_game_defs.validation import validate_against_schema, validate_machine
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.tx-sector.1988"
SEED = ROOT / "tools/seeds/gottlieb/tx-sector-1988.json"
NOTE_SEED = ROOT / "tools/seeds/gottlieb/tx-sector-1988.md"
AUDIT_SEED = ROOT / "tools/seeds/gottlieb/tx-sector-1988-spatial.json"
PARTIAL = ROOT / "machines/partial/gottlieb/tx-sector-1988.json"
READY = ROOT / "machines/author-ready/gottlieb/tx-sector-1988.json"
NOTE = ROOT / "knowledge/gottlieb/tx-sector-1988.md"
AUDIT = ROOT / "reports/spatial/gottlieb/tx-sector-1988.json"
AUDIT_MD = ROOT / "reports/spatial/gottlieb/tx-sector-1988.md"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_excerpts(definition: dict) -> None:
    for source in definition["sources"]:
        for excerpt in source.get("excerpts", []):
            for key, hash_key in (("path", "sha256"), ("image", "image_sha256")):
                if key not in excerpt:
                    continue
                path = ROOT / excerpt[key]
                if not path.is_file() or digest(path) != excerpt[hash_key]:
                    raise ValueError(f"Missing or changed excerpt: {path}")
                if key == "path" and b"tokens truncated" in path.read_bytes():
                    raise ValueError(f"Truncated source excerpt: {path}")


def verify_external(audit: dict) -> None:
    for artifact in audit["retained_artifacts"]:
        root = os.environ.get(artifact["environment"])
        if not root:
            continue
        path = Path(root) / artifact["relative_path"]
        if artifact.get("directory_manifest"):
            actual = check_manifest(path, "txsector")
        else:
            if not path.is_file():
                raise ValueError(f"Missing retained artifact: {path}")
            actual = digest(path)
        if actual != artifact["sha256"]:
            raise ValueError(f"Changed retained artifact: {path}")


def build() -> dict:
    definition = load_json(SEED)
    if definition["machine"]["id"] != MACHINE_ID:
        raise ValueError("Wrong machine seed")
    if definition["coverage"]["status"] != "partial" or not definition["coverage"]["missing"]:
        raise ValueError("This partial curator cannot authorize promotion")
    verify_excerpts(definition)
    errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", str(SEED)) + validate_machine(definition, ROOT)
    if errors:
        raise ValueError("Invalid reviewed seed: " + "; ".join(errors))
    expected = {
        "pinmame.input.switch": set(range(-8, 0)) | {10 * s + r for s in range(8) for r in range(8)} | set(range(111, 119)),
        "pinmame.input.dip": set(range(1, 43)),
        "pinmame.output.solenoid": set(range(1, 12)) | set(range(45, 49)),
        "pinmame.output.lamp": set(range(64)),
        "pinmame.output.gi": {0},
    }
    for group, addresses in expected.items():
        actual = {d["binding"]["device"] for d in definition["inputs"] + definition["outputs"] if d["binding"]["group"] == group}
        if actual != addresses:
            raise ValueError(f"Incomplete controller address inventory: {group}")
    return definition


def artifacts() -> dict[Path, bytes]:
    definition = build()
    audit = load_json(AUDIT_SEED)
    if audit.get("machine_id") != MACHINE_ID or audit.get("format") != "pinmame-spatial-blockers":
        raise ValueError("Wrong spatial evidence seed")
    verify_external(audit)
    rows = ["# TX-Sector spatial evidence", "", "Coverage: **partial**. " + audit["promotion_decision"], "", audit["coordinate_convention"], "", "## Remaining requirements", ""]
    rows.extend("- " + item for item in audit["blockers"])
    rows.extend(["", "## Evidence and transformation", "", audit["method"], "", "All raw coordinates and exact object bindings are retained in the machine-specific evidence excerpt and mapping. Coordinates are rounded once to six decimals. No proxy is counted as a physical socket.", ""])
    return {PARTIAL: canonical_bytes(definition), NOTE: NOTE_SEED.read_bytes(), AUDIT: canonical_bytes(audit), AUDIT_MD: "\n".join(rows).encode("utf-8")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if args.check == args.regenerate:
        parser.error("choose --check or --regenerate")
    if READY.exists():
        raise ValueError("Refusing to overwrite an existing author-ready artifact")
    for path, data in artifacts().items():
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f"Curator drift: {path}")
        elif path.suffix == ".json":
            write_json(path, load_json(SEED if path == PARTIAL else AUDIT_SEED))
        else:
            write_text(path, data.decode("utf-8"))
    print("TX-Sector: checked" if args.check else "TX-Sector: regenerated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
