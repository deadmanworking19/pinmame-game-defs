"""Materialize the seed-owned Williams Swords of Fury (1988) definition.

The primary curator owns the canonical machine seed, literal knowledge note, excerpts, and
external-evidence binding register.  This tool is deliberately a small deterministic materializer:
it validates those inputs, checks the settled controller topology, and writes only the derived
machine, knowledge, and spatial-report artifacts.  It never updates a catalog or coverage report,
never creates a seed, and never makes a promotion decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping

from build_external_evidence_manifest import check_manifest
from pinmame_flipper_column import FLIPPER_COLUMN_ADDRESSES, LOWER_BUTTON_ADDRESSES
from pinmame_game_defs.jsonio import canonical_bytes, write_json, write_text
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "williams.swords-of-fury.1988"
SEED_RELATIVE_PATH = Path("tools/seeds/williams/swords-of-fury-1988.json")
KNOWLEDGE_SEED_RELATIVE_PATH = Path("tools/seeds/williams/swords-of-fury-1988.md")
EVIDENCE_BINDING_RELATIVE_PATH = Path("tools/seeds/williams/swords-of-fury-1988-evidence.json")
KNOWLEDGE_RELATIVE_PATH = Path("knowledge/williams/swords-of-fury-1988.md")
PARTIAL_RELATIVE_PATH = Path("machines/partial/williams/swords-of-fury-1988.json")
AUTHOR_READY_RELATIVE_PATH = Path("machines/author-ready/williams/swords-of-fury-1988.json")
SPATIAL_REPORT_RELATIVE_PATH = Path("reports/spatial/williams/swords-of-fury-1988.json")
SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH = Path("reports/spatial/williams/swords-of-fury-1988.md")

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
EXTRACTION_GAME = "swrds_l2"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

DRIVER_IDS = frozenset({"swrds_l1", "swrds_l2", "swrds_lg2", "swrds_rr1", "swrds_rr1b"})
EXPECTED_SWITCH_BINDINGS = frozenset(range(-7, -3)) | frozenset(range(1, 65)) | frozenset(FLIPPER_COLUMN_ADDRESSES)
EXPECTED_SOLENOID_BINDINGS = frozenset(range(1, 65))
EXPECTED_LAMP_BINDINGS = frozenset(range(1, 65))
MIXED_LOCATION_LAMPS = frozenset({6, 7, 16, 41, 42, 51, 52})
BACKBOX_ONLY_LAMPS = frozenset(range(57, 65))
PRINTED_BLANK_LAMPS = frozenset({8, 25})
EXTERNAL_ROOT_TAGS = frozenset({"vpx", "manuals", "review"})
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


def _path(root: Path, relative_path: Path) -> Path:
	return root / relative_path


def _sha256_file(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


def _read_json(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
	if not path.is_file():
		raise RuntimeError(f"Swords of Fury {label} is missing: {path}")
	try:
		raw = path.read_bytes()
		value = json.loads(raw.decode("utf-8"))
	except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
		raise RuntimeError(f"Swords of Fury {label} is malformed: {path}: {error}") from error
	if not isinstance(value, dict):
		raise RuntimeError(f"Swords of Fury {label} must be a JSON object: {path}")
	return value, raw


def _canonical_json(path: Path, label: str) -> dict[str, Any]:
	value, raw = _read_json(path, label)
	if raw != canonical_bytes(value):
		raise RuntimeError(f"Swords of Fury {label} is not canonical UTF-8 JSON: {path}")
	return value


def _seed_path(root: Path) -> Path:
	return _path(root, SEED_RELATIVE_PATH)


def _knowledge_seed_path(root: Path) -> Path:
	return _path(root, KNOWLEDGE_SEED_RELATIVE_PATH)


def _definition_paths(definition: Mapping[str, Any], root: Path) -> tuple[Path, Path]:
	coverage = definition.get("coverage")
	status = coverage.get("status") if isinstance(coverage, Mapping) else None
	if status == "partial":
		return _path(root, PARTIAL_RELATIVE_PATH), _path(root, AUTHOR_READY_RELATIVE_PATH)
	if status == "author_ready":
		return _path(root, AUTHOR_READY_RELATIVE_PATH), _path(root, PARTIAL_RELATIVE_PATH)
	raise RuntimeError(
		f"Swords of Fury seed has unsupported coverage status {status!r}; only partial or author_ready can be materialized"
	)


def _validation_errors(definition: dict[str, Any], repository_root: Path | None = None) -> list[str]:
	errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", "Swords of Fury seed")
	errors.extend(validate_machine(definition, repository_root))
	return errors


def _binding_index(definition: Mapping[str, Any], collection_name: str) -> dict[tuple[str, int], dict[str, Any]]:
	collection = definition.get(collection_name)
	if not isinstance(collection, list):
		raise RuntimeError(f"Swords of Fury seed {collection_name} must be an array")
	indexed: dict[tuple[str, int], dict[str, Any]] = {}
	for index, item in enumerate(collection):
		if not isinstance(item, dict):
			raise RuntimeError(f"Swords of Fury seed {collection_name}[{index}] must be an object")
		binding = item.get("binding")
		if not isinstance(binding, dict) or not isinstance(binding.get("group"), str) or not isinstance(binding.get("device"), int):
			raise RuntimeError(f"Swords of Fury seed {collection_name}[{index}] has no numeric controller binding")
		key = (binding["group"], binding["device"])
		if key in indexed:
			raise RuntimeError(f"Swords of Fury seed duplicates {collection_name} binding {key}")
		indexed[key] = item
	return indexed


def _physical_text(device: Mapping[str, Any]) -> str:
	physical = device.get("physical")
	if not isinstance(physical, Mapping):
		return ""
	return " ".join(str(value) for value in physical.values() if isinstance(value, str)).casefold()


def _assert_exact_swords_contract(definition: dict[str, Any]) -> None:
	"""Validate the settled topology and routing without assigning semantic device IDs."""
	errors: list[str] = []
	machine = definition.get("machine")
	if not isinstance(machine, dict) or machine.get("id") != MACHINE_ID:
		errors.append(f"machine.id must be {MACHINE_ID!r}")
	elif machine.get("manufacturer") != "Williams" or machine.get("year") != 1988:
		errors.append("machine must remain the 1988 Williams physical machine")

	drivers = definition.get("drivers")
	driver_ids = {driver.get("id") for driver in drivers if isinstance(driver, dict)} if isinstance(drivers, list) else set()
	if not isinstance(drivers, list) or len(drivers) != len(DRIVER_IDS) or driver_ids != DRIVER_IDS:
		errors.append(f"drivers must be exactly {sorted(DRIVER_IDS)!r}")

	controller = definition.get("controller")
	if not isinstance(controller, dict) or controller.get("platform") != "pinmame.system-11":
		errors.append("controller.platform must be pinmame.system-11")
	elif controller.get("hardware_generation") != "0x100":
		errors.append("controller.hardware_generation must be GEN_S11B-derived 0x100")

	sources = definition.get("sources")
	if not isinstance(sources, list) or not any(
		isinstance(source, dict)
		and source.get("kind") in {"pinmame_catalog", "pinmame_core"}
		and source.get("revision") == PINMAME_REVISION
		for source in sources
	):
		errors.append(f"sources must retain a PinMAME catalog/core record pinned at {PINMAME_REVISION}")

	inputs = _binding_index(definition, "inputs")
	expected_inputs = {(SWITCH_GROUP, address) for address in EXPECTED_SWITCH_BINDINGS} | {(DIP_GROUP, 0)}
	if set(inputs) != expected_inputs or len(inputs) != len(expected_inputs):
		errors.append("inputs must be exactly diagnostics -7..-4, matrix 1..64, flipper column 81..88, and DIP 0")
	if inputs.get((DIP_GROUP, 0), {}).get("kind") != "dip_switch":
		errors.append("DIP 0 must remain a dip_switch input")

	outputs = _binding_index(definition, "outputs")
	expected_outputs = {(SOLENOID_GROUP, address) for address in EXPECTED_SOLENOID_BINDINGS} | {(LAMP_GROUP, address) for address in EXPECTED_LAMP_BINDINGS}
	if set(outputs) != expected_outputs or len(outputs) != len(expected_outputs):
		errors.append("outputs must be exactly solenoids 1..64 and lamps 1..64; System 11 has no separate GI group")
	if any(group == GI_GROUP for group, _address in outputs):
		errors.append("Swords of Fury must not invent a separate GI callback group")

	pairs = {
		(item.get("source"), item.get("destination"))
		for item in definition.get("relationships", [])
		if isinstance(item, dict) and item.get("kind") == "direct"
	}
	for source_address, matrix_address in ((84, 58), (82, 60)):
		source = inputs.get((SWITCH_GROUP, source_address))
		destination = inputs.get((SWITCH_GROUP, matrix_address))
		if not source or source.get("availability") != "used":
			errors.append(f"flipper-column switch {source_address} must be used")
		elif not destination:
			errors.append(f"matrix switch {matrix_address} is missing")
		elif (source.get("id"), destination.get("id")) not in pairs:
			errors.append(f"flipper-column switch {source_address} must directly copy to matrix switch {matrix_address}")

	for address in (46, 47):
		output = outputs.get((SOLENOID_GROUP, address))
		if output is None or output.get("kind") != "virtual":
			errors.append(f"synthetic solenoid {address} must remain virtual, not a physical flasher")

	gi_relay = outputs.get((SOLENOID_GROUP, 10))
	gi_physical = gi_relay.get("physical") if isinstance(gi_relay, Mapping) else None
	gi_text = gi_physical.get("notes", "").casefold() if isinstance(gi_physical, Mapping) and isinstance(gi_physical.get("notes"), str) else ""
	if not gi_relay or gi_relay.get("kind") != "relay" or "playfield" not in gi_text or "backbox" not in gi_text:
		errors.append("solenoid 10 must retain its relay classification and mixed playfield/backbox physical note")

	for address in MIXED_LOCATION_LAMPS:
		lamp = outputs.get((LAMP_GROUP, address))
		physical = lamp.get("physical") if isinstance(lamp, dict) else None
		if not isinstance(physical, dict) or physical.get("quantity") != 2:
			errors.append(f"lamp {address} must retain the two-bulb playfield/backbox quantity")
	for address in BACKBOX_ONLY_LAMPS:
		lamp = outputs.get((LAMP_GROUP, address))
		spatial = lamp.get("spatial") if isinstance(lamp, dict) else None
		if not isinstance(spatial, dict) or (spatial.get("status"), spatial.get("reason")) != ("not_applicable", "cabinet_or_service"):
			errors.append(f"lamp {address} must remain a cabinet/backbox-only spatial record")
	for address in PRINTED_BLANK_LAMPS:
		lamp = outputs.get((LAMP_GROUP, address))
		label = lamp.get("label", "") if isinstance(lamp, dict) else ""
		if not isinstance(lamp, dict) or lamp.get("availability") != "unused" or "blank" not in (str(label) + " " + _physical_text(lamp)).casefold():
			errors.append(f"lamp {address} must remain unused and explicitly preserve the printed blank cell")

	if errors:
		raise RuntimeError("Swords of Fury seed violates its settled controller contract:\n- " + "\n- ".join(errors))


def _safe_relative_path(relative: str, label: str) -> tuple[str, ...]:
	if not isinstance(relative, str) or not relative:
		raise RuntimeError(f"Swords of Fury {label} path must be a non-empty string")
	posix = PurePosixPath(relative)
	windows = PureWindowsPath(relative)
	parts = posix.parts
	if (
		not parts
		or posix.is_absolute()
		or windows.is_absolute()
		or bool(windows.drive)
		or "\\" in relative
		or any(part in {".", ".."} or ":" in part for part in parts)
	):
		raise RuntimeError(f"Swords of Fury {label} path must be a safe relative POSIX path: {relative!r}")
	return parts


def _safe_repository_path(root: Path, relative: str, label: str) -> Path:
	parts = _safe_relative_path(relative, label)
	candidate = root.joinpath(*parts)
	try:
		candidate.resolve().relative_to(root.resolve())
	except (OSError, ValueError) as error:
		raise RuntimeError(f"Swords of Fury {label} path escapes the repository root: {relative!r}") from error
	return candidate


def _verify_file_digest(path: Path, expected_size: int | None, expected_sha256: str, label: str) -> None:
	if not path.is_file():
		raise RuntimeError(f"Swords of Fury {label} is missing: {path}")
	if expected_size is not None and path.stat().st_size != expected_size:
		raise RuntimeError(f"Swords of Fury {label} size drifted: {path}")
	if _sha256_file(path) != expected_sha256:
		raise RuntimeError(f"Swords of Fury {label} SHA-256 drifted: {path}")


def _verify_repository_excerpts(definition: Mapping[str, Any], root: Path) -> None:
	sources = definition.get("sources")
	if not isinstance(sources, list):
		raise RuntimeError("Swords of Fury seed sources must be an array")
	checked = 0
	for source_index, source in enumerate(sources):
		if not isinstance(source, Mapping):
			raise RuntimeError(f"Swords of Fury seed sources[{source_index}] must be an object")
		uri = source.get("uri", "")
		if isinstance(uri, str) and uri.startswith(("evidence/", "tools/seeds/")):
			_verify_file_digest(_safe_repository_path(root, uri, "derived evidence"), None, source["sha256"], "repository derived evidence")
		excerpts = source.get("excerpts", [])
		if not isinstance(excerpts, list):
			raise RuntimeError(f"Swords of Fury source {source.get('id')!r} excerpts must be an array")
		for excerpt_index, excerpt in enumerate(excerpts):
			if not isinstance(excerpt, Mapping):
				raise RuntimeError("Swords of Fury seed contains a malformed source excerpt")
			path_text = excerpt.get("path")
			if not isinstance(path_text, str) or not path_text.startswith(f"evidence/excerpts/{MACHINE_ID}/"):
				raise RuntimeError(f"Swords of Fury excerpt must remain under evidence/excerpts/{MACHINE_ID}/: {path_text!r}")
			sha256 = excerpt.get("sha256")
			if not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
				raise RuntimeError(f"Swords of Fury excerpt has an invalid SHA-256: {path_text!r}")
			_verify_file_digest(_safe_repository_path(root, path_text, "excerpt"), None, sha256, "repository excerpt")
			checked += 1
			image = excerpt.get("image")
			image_sha256 = excerpt.get("image_sha256")
			if image is not None or image_sha256 is not None:
				if not isinstance(image, str) or not isinstance(image_sha256, str) or not SHA256_PATTERN.fullmatch(image_sha256):
					raise RuntimeError(f"Swords of Fury excerpt image is malformed: {path_text!r}")
				_verify_file_digest(_safe_repository_path(root, image, "excerpt image"), None, image_sha256, "repository excerpt image")
	if checked == 0:
		raise RuntimeError("Swords of Fury seed must retain at least one source excerpt")


def _validate_external_entry(entry: Any, label: str) -> tuple[str, str, int, str]:
	if not isinstance(entry, dict) or set(entry) != {"root", "path", "size", "sha256"}:
		raise RuntimeError(f"Swords of Fury evidence binding {label} must contain only root, path, size, and sha256")
	root = entry["root"]
	path = entry["path"]
	size = entry["size"]
	sha256 = entry["sha256"]
	if (
		root not in EXTERNAL_ROOT_TAGS
		or not isinstance(path, str)
		or not isinstance(size, int)
		or isinstance(size, bool)
		or size < 0
		or not isinstance(sha256, str)
		or not SHA256_PATTERN.fullmatch(sha256)
	):
		raise RuntimeError(f"Swords of Fury evidence binding {label} is malformed")
	_safe_relative_path(path, f"evidence binding {label}")
	return root, path, size, sha256


def _validate_extraction(extraction: Any) -> dict[str, Any]:
	if not isinstance(extraction, dict) or set(extraction) != {"root", "path", "game", "sha256", "file_count", "total_bytes"}:
		raise RuntimeError("Swords of Fury evidence binding extraction must contain root, path, game, sha256, file_count, and total_bytes")
	root = extraction["root"]
	path = extraction["path"]
	game = extraction["game"]
	sha256 = extraction["sha256"]
	file_count = extraction["file_count"]
	total_bytes = extraction["total_bytes"]
	if (
		root != "vpx"
		or not isinstance(path, str)
		or not isinstance(game, str)
		or game != EXTRACTION_GAME
		or not isinstance(sha256, str)
		or not SHA256_PATTERN.fullmatch(sha256)
		or not isinstance(file_count, int)
		or isinstance(file_count, bool)
		or file_count < 0
		or not isinstance(total_bytes, int)
		or isinstance(total_bytes, bool)
		or total_bytes < 0
	):
		raise RuntimeError(f"Swords of Fury extraction binding must pin {EXTRACTION_GAME!r} and valid manifest metadata")
	parts = _safe_relative_path(path, "extraction manifest")
	if parts[-1] != "manifest.json":
		raise RuntimeError("Swords of Fury extraction binding path must name the official manifest.json")
	return extraction


def _binding_register(root: Path) -> dict[str, Any]:
	"""Validate the authored external binding register without reading optional roots."""
	register = _canonical_json(_path(root, EVIDENCE_BINDING_RELATIVE_PATH), "external evidence binding register")
	if set(register) != {"files", "extraction"} or not isinstance(register.get("files"), list) or not register["files"]:
		raise RuntimeError("Swords of Fury external evidence binding register must be exactly a non-empty files list plus extraction metadata")
	seen: set[tuple[str, str]] = set()
	for index, entry in enumerate(register["files"]):
		root_name, relative_path, _size, _sha256 = _validate_external_entry(entry, f"files[{index}]")
		key = (root_name, relative_path)
		if key in seen:
			raise RuntimeError(f"Swords of Fury evidence binding register duplicates {root_name}:{relative_path}")
		seen.add(key)
	_validate_extraction(register["extraction"])
	return register


def _external_file(root: Path, relative: str, label: str) -> Path:
	if not root.is_dir():
		raise RuntimeError(f"Swords of Fury {label} requires a readable source root: {root}")
	parts = _safe_relative_path(relative, label)
	candidate = root.joinpath(*parts)
	try:
		candidate.resolve().relative_to(root.resolve())
	except (OSError, ValueError) as error:
		raise RuntimeError(f"Swords of Fury {label} escapes its configured source root: {relative!r}") from error
	return candidate


def _required_external_root(roots: Mapping[str, Path | None], root_name: str, label: str) -> Path:
	external_root = roots.get(root_name)
	if external_root is None or not external_root.is_dir():
		raise RuntimeError(f"Swords of Fury {label} requires a readable {root_name} source root")
	return external_root


def _verify_extraction(extraction: Mapping[str, Any], roots: Mapping[str, Path | None]) -> None:
	root_name = extraction["root"]
	manifest_path = _external_file(_required_external_root(roots, root_name, "extraction"), extraction["path"], "extraction manifest")
	_verify_file_digest(manifest_path, None, extraction["sha256"], "extraction manifest")
	try:
		manifest_digest = check_manifest(manifest_path.parent, EXTRACTION_GAME)
	except (OSError, ValueError) as error:
		raise RuntimeError(f"Swords of Fury extraction content drifted: {error}") from error
	if manifest_digest != extraction["sha256"]:
		raise RuntimeError("Swords of Fury extraction manifest digest does not match its binding register")
	try:
		manifest = json.loads(manifest_path.read_bytes().decode("utf-8"))
	except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
		raise RuntimeError(f"Swords of Fury extraction manifest is malformed: {manifest_path}") from error
	files = manifest.get("files") if isinstance(manifest, dict) else None
	if not isinstance(files, list):
		raise RuntimeError("Swords of Fury extraction manifest has no files list")
	try:
		file_count = len(files)
		total_bytes = sum(item["size"] for item in files if isinstance(item, dict))
	except (KeyError, TypeError) as error:
		raise RuntimeError("Swords of Fury extraction manifest has malformed file metadata") from error
	if len(files) != sum(isinstance(item, dict) and isinstance(item.get("size"), int) and not isinstance(item.get("size"), bool) and item["size"] >= 0 for item in files):
		raise RuntimeError("Swords of Fury extraction manifest has malformed file metadata")
	if file_count != extraction["file_count"]:
		raise RuntimeError("Swords of Fury extraction manifest file count drifted from its binding register")
	if total_bytes != extraction["total_bytes"]:
		raise RuntimeError("Swords of Fury extraction manifest total bytes drifted from its binding register")


def verify_retained(
	vpx_root: Path | str | None,
	manuals_root: Path | str | None,
	review_root: Path | str | None,
	*,
	root: Path = ROOT,
) -> None:
	"""Verify every external file and the complete retained extraction when explicitly requested."""
	register = _binding_register(root)
	roots: dict[str, Path | None] = {
		"vpx": Path(vpx_root) if vpx_root is not None else None,
		"manuals": Path(manuals_root) if manuals_root is not None else None,
		"review": Path(review_root) if review_root is not None else None,
	}
	for index, entry in enumerate(register["files"]):
		root_name, relative_path, size, sha256 = _validate_external_entry(entry, f"files[{index}]")
		external_root = _required_external_root(roots, root_name, f"evidence binding files[{index}]")
		_verify_file_digest(
			_external_file(external_root, relative_path, f"evidence binding files[{index}]"),
			size,
			sha256,
			f"retained {root_name} evidence",
		)
	_verify_extraction(_validate_extraction(register["extraction"]), roots)


def build(root: Path = ROOT) -> dict[str, Any]:
	"""Read and validate the canonical seed without modifying any artifact."""
	definition = _canonical_json(_seed_path(root), "machine seed")
	errors = _validation_errors(definition)
	if errors:
		raise RuntimeError("Swords of Fury machine seed is malformed:\n- " + "\n- ".join(errors))
	_assert_exact_swords_contract(definition)
	_binding_register(root)
	return definition


def knowledge_text(root: Path = ROOT) -> str:
	"""Return the literal seed-owned knowledge note without newline translation."""
	path = _knowledge_seed_path(root)
	if not path.is_file():
		raise RuntimeError(f"Swords of Fury knowledge seed is missing: {path}")
	try:
		return path.read_bytes().decode("utf-8")
	except (OSError, UnicodeDecodeError) as error:
		raise RuntimeError(f"Swords of Fury knowledge seed is malformed UTF-8: {path}: {error}") from error


def _device_report_record(collection: str, device: Mapping[str, Any]) -> dict[str, Any]:
	return {
		"collection": collection,
		"id": device.get("id"),
		"label": device.get("label"),
		"binding": device.get("binding"),
		"kind": device.get("kind"),
		"availability": device.get("availability"),
		"physical": device.get("physical"),
		"provenance": device.get("provenance"),
	}


def _unknown_reasons(device: Mapping[str, Any]) -> list[str]:
	reasons: list[str] = []
	if device.get("availability") == "unknown":
		reasons.append("availability")
	provenance = device.get("provenance")
	if isinstance(provenance, Mapping) and provenance.get("status") == "unknown":
		reasons.append("provenance")
	spatial = device.get("spatial")
	if isinstance(spatial, Mapping) and spatial.get("status") in {"candidate", "conflicted"}:
		reasons.append(f"spatial:{spatial['status']}")
	return reasons


def build_spatial_report(definition: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
	"""Project spatial and provenance state already declared in the canonical seed."""
	coverage = definition["coverage"]
	status = coverage["status"]
	located: list[dict[str, Any]] = []
	not_applicable: list[dict[str, Any]] = []
	missing_spatial: list[dict[str, Any]] = []
	unplaced_physical: list[dict[str, Any]] = []
	unknown_records: list[dict[str, Any]] = []
	projection_disclosures: list[dict[str, Any]] = []

	for collection_name in ("inputs", "outputs", "displays"):
		collection = definition.get(collection_name)
		if not isinstance(collection, list):
			raise RuntimeError(f"Swords of Fury seed {collection_name} must be an array for the spatial report")
		for device in collection:
			if not isinstance(device, Mapping):
				raise RuntimeError(f"Swords of Fury seed {collection_name} contains a non-object device")
			record = _device_report_record(collection_name, device)
			spatial = device.get("spatial")
			if not isinstance(spatial, Mapping):
				missing_spatial.append(record)
				if isinstance(device.get("physical"), Mapping):
					unplaced_physical.append(record)
			elif spatial.get("status") == "not_applicable":
				record["reason"] = spatial.get("reason")
				record["spatial_provenance"] = spatial.get("provenance")
				not_applicable.append(record)
			elif isinstance(spatial.get("placements"), list):
				record["spatial"] = spatial
				located.append(record)
			else:
				missing_spatial.append(record)
				if isinstance(device.get("physical"), Mapping):
					unplaced_physical.append(record)
			if _unknown_reasons(device):
				unknown = dict(record)
				unknown["unknown_fields"] = _unknown_reasons(device)
				unknown_records.append(unknown)
			physical = device.get("physical")
			if isinstance(physical, Mapping) and isinstance(physical.get("notes"), str) and re.search(r"\bproject(?:ion|ed)?\b", physical["notes"], re.IGNORECASE):
				projection_disclosures.append(record)

	source_hashes: list[dict[str, Any]] = []
	for source in definition["sources"]:
		if not isinstance(source, Mapping):
			continue
		source_hashes.append({
			"id": source.get("id"),
			"kind": source.get("kind"),
			"uri": source.get("uri"),
			"locator": source.get("locator"),
			"revision": source.get("revision"),
			"sha256": source.get("sha256"),
			"excerpts": [
				{
					"id": excerpt.get("id"),
					"path": excerpt.get("path"),
					"sha256": excerpt.get("sha256"),
					"image": excerpt.get("image"),
					"image_sha256": excerpt.get("image_sha256"),
				}
				for excerpt in source.get("excerpts", [])
				if isinstance(excerpt, Mapping)
			],
		})

	register = _binding_register(root)
	promotion = {
		"seed_status": status,
		"missing": coverage["missing"],
		"decision": (
			"The seed declares author_ready; this materializer records that status but does not make a promotion decision."
			if status == "author_ready"
			else "Partial: the seed remains unpromoted while coverage.missing is non-empty; this materializer does not make promotion decisions."
		),
	}
	return {
		"format": "pinmame-spatial-audit" if status == "author_ready" else "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"coordinate_convention": {
			"space": "playfield",
			"x": "left=0, right=1 in player view",
			"y": "rear=0, front=1 in player view",
		},
		"definition_sha256": hashlib.sha256(canonical_bytes(definition)).hexdigest(),
		"external_evidence": {"files": register["files"], "extraction": register["extraction"]},
		"source_hashes": source_hashes,
		"located_devices": located,
		"projection_disclosures": projection_disclosures,
		"missing_spatial_records": missing_spatial,
		"unplaced_physical_devices": unplaced_physical,
		"unknown_records": unknown_records,
		"not_applicable_devices": not_applicable,
		"coverage": {"status": status, "missing": coverage["missing"]},
		"promotion_decision": promotion,
		"emitter_policy": "Render-light candidate anchors are not observed physical sockets. Observed fixture anchors are disclosed projections onto their own geometry; actual socket/contact/winding positions remain blocked.",
	}


def _binding_text(record: Mapping[str, Any]) -> str:
	binding = record.get("binding")
	if not isinstance(binding, Mapping):
		return "unbound"
	return f"{binding.get('group')} {binding.get('device')}"


def render_spatial_report(report: dict[str, Any]) -> str:
	"""Render the spatial report from the seed-derived report object only."""
	lines = [
		f"# Spatial report — {report['machine_id']}",
		"",
		f"Format: `{report['format']}` v{report['version']}",
		f"Definition SHA-256: `{report['definition_sha256']}`",
		"",
		"## Coordinate convention",
		"",
		f"- `{report['coordinate_convention']['x']}`",
		f"- `{report['coordinate_convention']['y']}`",
		"",
		"## Coverage and promotion decision",
		"",
		f"- Seed status: `{report['coverage']['status']}`",
		f"- Missing coverage: `{json.dumps(report['coverage']['missing'], ensure_ascii=False)}`",
		f"- Decision: {report['promotion_decision']['decision']}",
		"",
		"## External evidence binding",
		"",
	]
	for entry in report["external_evidence"]["files"]:
		lines.append(f"- `{entry['root']}:{entry['path']}` — {entry['size']} bytes, SHA-256 `{entry['sha256']}`")
	extraction = report["external_evidence"]["extraction"]
	lines.append(
		f"- Extraction `{extraction['root']}:{extraction['path']}` for `{extraction['game']}` — SHA-256 `{extraction['sha256']}`, "
		f"{extraction['file_count']} files, {extraction['total_bytes']} bytes."
	)
	lines.extend(["", "## Source hashes and repository excerpts", ""])
	for source in report["source_hashes"]:
		lines.append(f"- `{source['id']}` ({source['kind']}): `{source['sha256']}`")
		lines.append(f"  - {source['uri']} — {source['locator']}")
		for excerpt in source["excerpts"]:
			lines.append(f"  - `{excerpt['id']}` — `{excerpt['path']}` SHA-256 `{excerpt['sha256']}`")
			if excerpt.get("image") is not None:
				lines.append(f"    - image `{excerpt['image']}` SHA-256 `{excerpt['image_sha256']}`")

	lines.extend(["", "## Exact seeded placements", ""])
	if report["located_devices"]:
		for device in report["located_devices"]:
			lines.append(f"- `{device['collection']}:{device['id']}` ({_binding_text(device)}): `{device['spatial']['status']}`")
			for placement in device["spatial"]["placements"]:
				lines.append(
					f"  - `{placement['id']}` — {placement['role']} at ({placement['x']}, {placement['y']}); "
					f"sources `{', '.join(placement['provenance']['source_refs'])}`"
				)
	else:
		lines.append("- None recorded by the canonical seed.")

	for heading, key in (
		("Projection disclosures", "projection_disclosures"),
		("Missing spatial records", "missing_spatial_records"),
		("Unplaced physical devices", "unplaced_physical_devices"),
		("Unknown records", "unknown_records"),
		("Controlled not-applicable spatial records", "not_applicable_devices"),
	):
		lines.extend(["", f"## {heading}", ""])
		if report[key]:
			for device in report[key]:
				detail = device.get("unknown_fields") or device.get("reason") or device.get("physical", {}).get("notes", "")
				lines.append(f"- `{device['collection']}:{device['id']}` ({_binding_text(device)}): {detail}")
		else:
			lines.append("- None recorded by the canonical seed.")

	lines.extend(["", "## Emitter policy", "", report["emitter_policy"], ""])
	return "\n".join(lines)


def _report_errors(report: dict[str, Any]) -> list[str]:
	return validate_against_schema(report, ROOT / "schemas/spatial-report.schema.json", "Swords of Fury spatial report")


def _verify_generated_artifacts(definition: dict[str, Any], root: Path, expected_knowledge: str) -> None:
	definition_path, opposing_path = _definition_paths(definition, root)
	if opposing_path.exists():
		raise RuntimeError(f"Swords of Fury has a stale opposing-status artifact: {opposing_path}")
	if not definition_path.is_file() or definition_path.read_bytes() != canonical_bytes(definition):
		raise RuntimeError(f"Swords of Fury generated definition drifted from the canonical seed: {definition_path}")
	knowledge_path = _path(root, KNOWLEDGE_RELATIVE_PATH)
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != expected_knowledge.encode("utf-8"):
		raise RuntimeError(f"Swords of Fury generated knowledge note drifted from its literal seed: {knowledge_path}")
	report = build_spatial_report(definition, root)
	errors = _report_errors(report)
	if errors:
		raise RuntimeError("Swords of Fury spatial report is malformed:\n- " + "\n- ".join(errors))
	report_path = _path(root, SPATIAL_REPORT_RELATIVE_PATH)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Swords of Fury spatial report drifted from the canonical seed: {report_path}")
	markdown_path = _path(root, SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH)
	if not markdown_path.is_file() or markdown_path.read_bytes() != render_spatial_report(report).encode("utf-8"):
		raise RuntimeError(f"Swords of Fury spatial report Markdown drifted from the canonical seed: {markdown_path}")


def generate(root: Path = ROOT) -> Path:
	"""Write only the generated definition, literal knowledge note, and spatial reports."""
	definition = build(root)
	knowledge = knowledge_text(root)
	_verify_repository_excerpts(definition, root)
	definition_path, opposing_path = _definition_paths(definition, root)
	if opposing_path.exists():
		if definition["coverage"]["status"] == "partial" and opposing_path == _path(root, AUTHOR_READY_RELATIVE_PATH):
			raise RuntimeError(f"Refusing to overwrite an existing author-ready Swords of Fury artifact with a partial seed: {opposing_path}")
		raise RuntimeError(f"Refusing to generate Swords of Fury while a stale opposing-status artifact exists: {opposing_path}")
	report = build_spatial_report(definition, root)
	errors = _report_errors(report)
	if errors:
		raise RuntimeError("Swords of Fury spatial report is malformed:\n- " + "\n- ".join(errors))
	write_json(definition_path, definition)
	write_text(_path(root, KNOWLEDGE_RELATIVE_PATH), knowledge)
	write_json(_path(root, SPATIAL_REPORT_RELATIVE_PATH), report)
	write_text(_path(root, SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH), render_spatial_report(report))
	return definition_path


def check(root: Path = ROOT) -> None:
	"""Fail closed on missing/drifting inputs, references, excerpts, or generated artifacts."""
	definition = build(root)
	knowledge = knowledge_text(root)
	knowledge_path = definition.get("knowledge", {}).get("path") if isinstance(definition.get("knowledge"), dict) else None
	if knowledge_path != KNOWLEDGE_RELATIVE_PATH.as_posix():
		raise RuntimeError(f"Swords of Fury seed must reference {KNOWLEDGE_RELATIVE_PATH.as_posix()!r}, not {knowledge_path!r}")
	errors = _validation_errors(definition, root)
	if errors:
		raise RuntimeError("Swords of Fury seed has invalid repository references:\n- " + "\n- ".join(errors))
	_verify_repository_excerpts(definition, root)
	_verify_generated_artifacts(definition, root, knowledge)
	print("Swords of Fury definition, literal knowledge note, spatial report, and repository excerpts match the canonical seed.")


def _configured_root(name: str) -> Path | None:
	value = os.environ.get(name)
	return Path(value) if value else None


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true", help="Check Swords of Fury artifacts; this is the default")
	mode.add_argument("--regenerate", action="store_true", help="Materialize only Swords of Fury derived artifacts")
	mode.add_argument("--verify-retained", action="store_true", help="Verify the optional external evidence binding register")
	parser.add_argument("--vpx-root", type=Path, help="Override PINMAME_VPX_SOURCES_ROOT for --verify-retained")
	parser.add_argument("--manuals-root", type=Path, help="Override PINMAME_MANUALS_ROOT for --verify-retained")
	parser.add_argument("--review-root", type=Path, help="Override PINMAME_REVIEW_ARTIFACTS_ROOT for --verify-retained")
	args = parser.parse_args()
	if args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	elif args.verify_retained:
		verify_retained(
			args.vpx_root or _configured_root("PINMAME_VPX_SOURCES_ROOT"),
			args.manuals_root or _configured_root("PINMAME_MANUALS_ROOT"),
			args.review_root or _configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT"),
		)
		print("Swords of Fury retained external evidence matches its binding register.")
	else:
		check(ROOT)


if __name__ == "__main__":
	main()
