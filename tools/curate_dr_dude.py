"""Materialize Dr. Dude seeds without inventing machine facts.

The spatial JSON seed includes a literal ``markdown`` field for its companion
report. Both production and WPC prototype seeds and reports are mandatory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any

from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.jsonio import canonical_bytes, write_bytes
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = "dr-dude-and-his-excellent-ray-1990"
PROTOTYPE = "dr-dude-and-his-excellent-ray-wpc-prototype-1990"
PRODUCTION_ID = "bally.dr-dude-and-his-excellent-ray.1990"
PROTOTYPE_ID = "bally.dr-dude-and-his-excellent-ray-wpc-prototype.1990"
SEEDS = Path("tools/seeds/bally")
EVIDENCE_REGISTER = SEEDS / f"{PRODUCTION}-evidence.json"
SPATIAL_SEED = SEEDS / f"{PRODUCTION}-spatial.json"
SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"
SWITCHES = frozenset(range(-7, -3)) | frozenset(range(1, 65)) | frozenset(range(81, 89))
SOLENOIDS = frozenset(range(1, 51))
LAMPS = frozenset(range(1, 65))
WPC_MATRIX = frozenset(col * 10 + row for col in range(1, 9) for row in range(1, 9))
WPC_SWITCHES = frozenset(range(1, 9)) | WPC_MATRIX | frozenset(range(111, 119))
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _json(path: Path, label: str) -> dict[str, Any]:
	try:
		raw = path.read_bytes()
		value = json.loads(raw.decode("utf-8"))
	except (OSError, UnicodeError, json.JSONDecodeError) as error:
		raise RuntimeError(f"{label} missing or malformed: {path}: {error}") from error
	if not isinstance(value, dict) or raw != canonical_bytes(value):
		raise RuntimeError(f"{label} must be a canonical JSON object: {path}")
	return value


def _text(path: Path, label: str) -> bytes:
	try:
		raw = path.read_bytes()
		raw.decode("utf-8")
		return raw
	except (OSError, UnicodeError) as error:
		raise RuntimeError(f"{label} missing or malformed: {path}: {error}") from error


def _safe_path(root: Path, relative: str) -> Path:
	if not isinstance(relative, str) or not relative or "\\" in relative:
		raise RuntimeError(f"unsafe relative POSIX path: {relative!r}")
	path = PurePosixPath(relative)
	if path.is_absolute() or any(part in {".", ".."} or ":" in part for part in relative.split("/")) or "//" in relative:
		raise RuntimeError(f"unsafe relative POSIX path: {relative!r}")
	candidate = root.joinpath(*path.parts)
	try:
		candidate.resolve().relative_to(root.resolve())
	except ValueError as error:
		raise RuntimeError(f"path escapes its root: {relative!r}") from error
	return candidate


def _digest(path: Path, size: int | None, expected: str) -> None:
	if not isinstance(expected, str) or not SHA256.fullmatch(expected):
		raise RuntimeError(f"invalid SHA-256 for {path}")
	try:
		data = path.read_bytes()
	except OSError as error:
		raise RuntimeError(f"evidence file missing: {path}") from error
	if (size is not None and len(data) != size) or hashlib.sha256(data).hexdigest() != expected:
		raise RuntimeError(f"evidence size or SHA-256 drift: {path}")


def _excerpts(definition: dict[str, Any], root: Path) -> None:
	for source in definition.get("sources", []):
		for excerpt in source.get("excerpts", []):
			path = excerpt["path"]
			if not path.startswith("evidence/excerpts/"):
				raise RuntimeError(f"excerpt outside evidence/excerpts: {path!r}")
			_digest(_safe_path(root, path), None, excerpt["sha256"])
			if "image" in excerpt:
				image = excerpt["image"]
				if not image.startswith("evidence/excerpts/"):
					raise RuntimeError(f"excerpt image outside evidence/excerpts: {image!r}")
				_digest(_safe_path(root, image), None, excerpt.get("image_sha256"))


def _bindings(definition: dict[str, Any], collection: str) -> set[tuple[str, int]]:
	result: set[tuple[str, int]] = set()
	for device in definition[collection]:
		binding = device["binding"]
		address = binding["device"]
		if isinstance(address, bool) or not isinstance(address, int):
			raise RuntimeError(f"{collection} binding is not an integer")
		key = (binding["group"], address)
		if key in result:
			raise RuntimeError(f"duplicate {collection} binding: {key!r}")
		result.add(key)
	return result


def _production_contract(definition: dict[str, Any]) -> None:
	inputs = {(SWITCH_GROUP, n) for n in SWITCHES} | {(DIP_GROUP, 0)}
	outputs = {(SOLENOID_GROUP, n) for n in SOLENOIDS} | {(LAMP_GROUP, n) for n in LAMPS}
	if _bindings(definition, "inputs") != inputs:
		raise RuntimeError("production inputs must enumerate switch -7..-4, 1..64, 81..88 and DIP 0 exactly")
	if _bindings(definition, "outputs") != outputs:
		raise RuntimeError("production outputs must enumerate solenoids 1..50 and lamps 1..64 exactly")


def _prototype_contract(definition: dict[str, Any]) -> None:
	inputs = {(SWITCH_GROUP, n) for n in WPC_SWITCHES} | {(DIP_GROUP, n) for n in range(1, 9)}
	outputs = {(SOLENOID_GROUP, n) for n in SOLENOIDS} | {(LAMP_GROUP, n) for n in WPC_MATRIX} | {(GI_GROUP, n) for n in range(5)}
	if _bindings(definition, "inputs") != inputs:
		raise RuntimeError("prototype inputs must enumerate service 1..8, matrix 11..88, flipper 111..118, and DIP 1..8 exactly")
	if _bindings(definition, "outputs") != outputs:
		raise RuntimeError("prototype outputs must enumerate solenoids 1..50, matrix lamps 11..88, and GI 0..4 exactly")


def _definition(root: Path, slug: str, machine_id: str) -> tuple[dict[str, Any], bytes, Path, Path]:
	definition = _json(root / SEEDS / f"{slug}.json", "machine seed")
	errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", "machine seed")
	errors.extend(validate_machine(definition))
	if errors:
		raise RuntimeError("invalid machine seed:\n- " + "\n- ".join(errors))
	if definition["machine"]["id"] != machine_id:
		raise RuntimeError(f"machine seed must identify {machine_id}")
	status = definition["coverage"]["status"]
	if status not in {"partial", "author_ready"}:
		raise RuntimeError(f"unsupported seed status: {status!r}")
	knowledge_path = Path("knowledge/bally") / f"{slug}.md"
	if definition["knowledge"]["path"] != knowledge_path.as_posix():
		raise RuntimeError(f"knowledge path must be {knowledge_path.as_posix()}")
	if slug == PRODUCTION:
		_production_contract(definition)
	elif slug == PROTOTYPE:
		_prototype_contract(definition)
	_excerpts(definition, root)
	knowledge = _text(root / SEEDS / f"{slug}.md", "knowledge seed")
	target = root / "machines" / ("author-ready" if status == "author_ready" else "partial") / "bally" / f"{slug}.json"
	opposing = root / "machines" / ("partial" if status == "author_ready" else "author-ready") / "bally" / f"{slug}.json"
	if opposing.exists():
		raise RuntimeError(f"refusing to materialize with opposing-status artifact: {opposing}")
	return definition, knowledge, target, root / knowledge_path


def _report(root: Path, definition: dict[str, Any], slug: str, machine_id: str) -> tuple[dict[str, Any], bytes]:
	report = _json(root / SEEDS / f"{slug}-spatial.json", "spatial seed")
	errors = validate_against_schema(report, ROOT / "schemas/spatial-report.schema.json", "spatial seed")
	if errors:
		raise RuntimeError("invalid spatial seed:\n- " + "\n- ".join(errors))
	status = definition["coverage"]["status"]
	expected = "pinmame-spatial-audit" if status == "author_ready" else "pinmame-spatial-blockers"
	if report["machine_id"] != machine_id or report["format"] != expected:
		raise RuntimeError("spatial report envelope disagrees with machine identity or coverage status")
	if "coverage" in report and report["coverage"] != definition["coverage"]:
		raise RuntimeError("spatial report coverage disagrees with machine seed")
	if "definition_sha256" in report and report["definition_sha256"] != hashlib.sha256(canonical_bytes(definition)).hexdigest():
		raise RuntimeError("spatial report definition SHA-256 drifted")
	markdown = report.get("markdown")
	if not isinstance(markdown, str) or not markdown.strip():
		raise RuntimeError("spatial seed must contain non-empty literal markdown")
	return report, markdown.encode("utf-8")


def _outputs(root: Path) -> list[tuple[Path, bytes]]:
	outputs: list[tuple[Path, bytes]] = []
	for slug, machine_id in ((PRODUCTION, PRODUCTION_ID), (PROTOTYPE, PROTOTYPE_ID)):
		definition, knowledge, target, knowledge_path = _definition(root, slug, machine_id)
		report, markdown = _report(root, definition, slug, machine_id)
		outputs.extend([(target, canonical_bytes(definition)), (knowledge_path, knowledge),
			(root / "reports/spatial/bally" / f"{slug}.json", canonical_bytes(report)),
			(root / "reports/spatial/bally" / f"{slug}.md", markdown)])
	return outputs


def generate(root: Path = ROOT) -> None:
	"""Validate all inputs and opposing paths before writing any output."""
	for path, data in _outputs(root):
		write_bytes(path, data)


def check(root: Path = ROOT) -> None:
	for path, expected in _outputs(root):
		if not path.is_file() or path.read_bytes() != expected:
			raise RuntimeError(f"generated artifact missing or drifted: {path}")
	for slug in (PRODUCTION, PROTOTYPE):
		path = root / SEEDS / f"{slug}.json"
		errors = validate_machine(_json(path, "machine seed"), root)
		if errors:
			raise RuntimeError("invalid repository references:\n- " + "\n- ".join(errors))


def verify_retained(vpx: Path | None, manuals: Path | None, review: Path | None, *, root: Path = ROOT) -> None:
	register = _json(root / EVIDENCE_REGISTER, "retained evidence register")
	if set(register) != {"files", "extraction"} or not isinstance(register["files"], list) or not register["files"]:
		raise RuntimeError("retained register must contain nonempty files and extraction")
	roots = {"vpx": vpx, "manuals": manuals, "review": review}
	for name, directory in roots.items():
		if directory is None or not Path(directory).is_dir():
			raise RuntimeError(f"a readable {name} root is required")
	seen: set[tuple[str, str]] = set()
	for entry in register["files"]:
		if not isinstance(entry, dict) or set(entry) != {"root", "path", "sha256", "size"}:
			raise RuntimeError("malformed retained file entry")
		name, relative, size = entry["root"], entry["path"], entry["size"]
		if name not in roots or not isinstance(relative, str) or not isinstance(size, int) or isinstance(size, bool) or size < 0:
			raise RuntimeError("malformed retained file entry")
		key = (name, relative)
		if key in seen:
			raise RuntimeError(f"duplicate retained file: {key!r}")
		seen.add(key)
		path = _safe_path(Path(roots[name]), relative)
		_digest(path, size, entry["sha256"])
		if name == "review" and path.name == "manifest.json":
			try:
				manifest = json.loads(path.read_text(encoding="utf-8"))
				check_manifest(path.parent, manifest["game"])
			except (OSError, ValueError, KeyError, TypeError, UnicodeError) as error:
				raise RuntimeError(f"retained bundle manifest verification failed: {path}: {error}") from error
	extraction = register["extraction"]
	if not isinstance(extraction, dict) or set(extraction) != {"root", "path", "game", "manifest_sha256", "file_count", "total_bytes"}:
		raise RuntimeError("malformed extraction register")
	if extraction["root"] != "vpx" or extraction["game"] != "dd_l2":
		raise RuntimeError("extraction must identify vpx and dd_l2")
	for field in ("file_count", "total_bytes"):
		if not isinstance(extraction[field], int) or isinstance(extraction[field], bool) or extraction[field] < 0:
			raise RuntimeError(f"invalid extraction {field}")
	directory = _safe_path(Path(vpx), extraction["path"])
	try:
		digest = check_manifest(directory, "dd_l2")
		manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
	except (OSError, ValueError, UnicodeError) as error:
		raise RuntimeError(f"extraction manifest verification failed: {error}") from error
	if digest != extraction["manifest_sha256"] or len(manifest["files"]) != extraction["file_count"] or sum(item["size"] for item in manifest["files"]) != extraction["total_bytes"]:
		raise RuntimeError("extraction digest, file count, or total bytes drifted")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true", help="check seed-owned artifacts (default)")
	mode.add_argument("--regenerate", action="store_true", help="materialize seed-owned artifacts")
	mode.add_argument("--verify-retained", action="store_true", help="verify pinned external evidence")
	args = parser.parse_args()
	if args.regenerate:
		generate()
	elif args.verify_retained:
		values = [os.environ.get(name) for name in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")]
		verify_retained(*(Path(value) if value else None for value in values))
	else:
		check()


if __name__ == "__main__":
	main()
