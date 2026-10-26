"""Reproduce one reviewed Stern Spike 1 partial definition from its seed.

Each seed is one canonical machine definition at
``tools/seeds/stern/spike1/<driver>.json``.  The accompanying Markdown file
has the same stem.  This curator deliberately does not fill in game facts:
it copies the reviewed definition and recreation note verbatim, then derives
only a compact spatial-blocker inventory from those declared facts.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes, write_json
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
SEED_DIRECTORY = PurePosixPath("tools/seeds/stern/spike1")
GAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
MACHINE_ID_PATTERN = re.compile(r"^stern\.([a-z0-9]+(?:-[a-z0-9]+)*)\.(\d{4})$")
REQUIRED_KNOWLEDGE_SECTIONS = {
	"identity": re.compile(r"\bidentity\b", re.IGNORECASE),
	"recreation": re.compile(r"\b(recreation|construction|mechanism|playfield|ball)\b", re.IGNORECASE),
	"sources": re.compile(r"\b(sources?|evidence)\b", re.IGNORECASE),
}


class CuratorError(RuntimeError):
	"""A deterministic input or artifact failure suitable for the command line."""


def _repository_root(root: Path) -> Path:
	resolved = root.resolve()
	if not resolved.is_dir():
		raise CuratorError(f"Repository root does not exist: {resolved}")
	return resolved


def _inside_repository(root: Path, path: Path, label: str) -> Path:
	resolved = path.resolve()
	try:
		resolved.relative_to(root)
	except ValueError as error:
		raise CuratorError(f"Unsafe {label} outside repository root: {path}") from error
	return resolved


def _repository_path(root: Path, relative: str, label: str) -> Path:
	if not isinstance(relative, str) or not relative:
		raise CuratorError(f"{label} must be a nonempty repository-relative POSIX path")
	if "\\" in relative:
		raise CuratorError(f"Unsafe {label}: backslash paths are not permitted")
	path = PurePosixPath(relative)
	if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
		raise CuratorError(f"Unsafe {label}: {relative}")
	return _inside_repository(root, root.joinpath(*path.parts), label)


def _seed_path(root: Path, game: str) -> Path:
	if not GAME_PATTERN.fullmatch(game):
		raise CuratorError(f"Unknown game {game!r}: expected an exact safe driver ID")
	return _repository_path(root, f"{SEED_DIRECTORY.as_posix()}/{game}.json", "seed path")


def _load_seed(root: Path, game: str) -> tuple[Path, bytes, dict[str, Any]]:
	path = _seed_path(root, game)
	if not path.is_file():
		raise CuratorError(f"Unknown game {game!r}: reviewed seed is missing at {path.relative_to(root).as_posix()}")
	try:
		payload = path.read_bytes()
		definition = load_json(path)
	except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
		raise CuratorError(f"Could not read seed {path.relative_to(root).as_posix()}: {error}") from error
	if not isinstance(definition, dict):
		raise CuratorError(f"Seed {path.relative_to(root).as_posix()} must contain one machine-definition object")
	if payload != canonical_bytes(definition):
		raise CuratorError(f"Seed {path.relative_to(root).as_posix()} is not canonical JSON bytes")
	drivers = definition.get("drivers")
	driver_ids = {driver.get("id") for driver in drivers if isinstance(driver, dict)} if isinstance(drivers, list) else set()
	if game not in driver_ids:
		raise CuratorError(f"Seed {path.relative_to(root).as_posix()} does not declare driver {game!r}")
	return path, payload, definition


def _machine_paths(root: Path, definition: dict[str, Any]) -> tuple[Path, Path, Path, Path, str, str]:
	machine = definition.get("machine")
	if not isinstance(machine, dict):
		raise CuratorError("Seed machine identity is missing")
	machine_id = machine.get("id")
	if not isinstance(machine_id, str):
		raise CuratorError("Seed machine.id is missing")
	match = MACHINE_ID_PATTERN.fullmatch(machine_id)
	if match is None:
		raise CuratorError("Seed machine.id must use stern.<slug>.<year>")
	slug, year = match.groups()
	coverage = definition.get("coverage")
	if not isinstance(coverage, dict) or coverage.get("status") != "partial":
		raise CuratorError("Spike 1 seed coverage.status must remain partial")
	knowledge = definition.get("knowledge")
	if not isinstance(knowledge, dict):
		raise CuratorError("Seed knowledge is missing")
	knowledge_path = knowledge.get("path")
	if not isinstance(knowledge_path, str) or not knowledge_path.startswith("knowledge/") or not knowledge_path.endswith(".md"):
		raise CuratorError("Seed knowledge.path must name a Markdown file under knowledge/")
	definition_path = _repository_path(root, f"machines/partial/stern/{slug}-{year}.json", "definition target")
	knowledge_target = _repository_path(root, knowledge_path, "knowledge.path")
	report_path = _repository_path(root, f"reports/spatial/stern/{slug}-{year}.json", "spatial report target")
	markdown_path = _repository_path(root, f"reports/spatial/stern/{slug}-{year}.md", "spatial Markdown target")
	return definition_path, knowledge_target, report_path, markdown_path, slug, year


def _author_ready_path(root: Path, slug: str, year: str) -> Path:
	return _repository_path(root, f"machines/author-ready/stern/{slug}-{year}.json", "author-ready target")


def _require_no_author_ready(root: Path, slug: str, year: str) -> None:
	path = _author_ready_path(root, slug, year)
	if path.exists():
		raise CuratorError(f"Refusing to overwrite or check an author-ready artifact: {path.relative_to(root).as_posix()}")
	partial_path = _repository_path(root, f"machines/partial/stern/{slug}-{year}.json", "definition target")
	if partial_path.is_file():
		current = load_json(partial_path)
		if isinstance(current, dict) and current.get("coverage", {}).get("status") == "author_ready":
			raise CuratorError(f"Refusing to overwrite or check an author-ready artifact: {partial_path.relative_to(root).as_posix()}")


def _load_knowledge(seed_path: Path, root: Path, definition: dict[str, Any]) -> bytes:
	path = _inside_repository(root, seed_path.with_suffix(".md"), "knowledge companion path")
	if not path.is_file():
		raise CuratorError(f"Required knowledge companion is missing: {path.relative_to(root).as_posix()}")
	try:
		payload = path.read_bytes()
		text = payload.decode("utf-8")
	except (OSError, UnicodeDecodeError) as error:
		raise CuratorError(f"Could not read knowledge companion {path.relative_to(root).as_posix()}: {error}") from error
	_validate_knowledge(text, definition, path.relative_to(root).as_posix())
	return payload


def _headings(text: str) -> list[tuple[str, str]]:
	lines = text.splitlines()
	headings: list[tuple[str, int]] = []
	for index, line in enumerate(lines):
		match = re.fullmatch(r"##\s+(.+?)\s*", line)
		if match is not None:
			headings.append((match.group(1), index))
	result: list[tuple[str, str]] = []
	for index, (heading, start) in enumerate(headings):
		end = headings[index + 1][1] if index + 1 < len(headings) else len(lines)
		result.append((heading, "\n".join(lines[start + 1:end]).strip()))
	return result


def _validate_knowledge(text: str, definition: dict[str, Any], label: str) -> None:
	if not re.search(r"^#\s+\S", text, flags=re.MULTILINE):
		raise CuratorError(f"Knowledge companion {label} must start with a nonempty H1 title")
	sections = _headings(text)
	for name, pattern in REQUIRED_KNOWLEDGE_SECTIONS.items():
		if not any(pattern.search(heading) and body for heading, body in sections):
			raise CuratorError(f"Knowledge companion {label} is missing a nonempty {name} section")
	machine = definition.get("machine", {})
	machine_id = machine.get("id") if isinstance(machine, dict) else None
	machine_name = machine.get("name") if isinstance(machine, dict) else None
	for value, description in ((machine_id, "machine ID"), (machine_name, "machine name")):
		if not isinstance(value, str) or value not in text:
			raise CuratorError(f"Knowledge companion {label} must name the declared {description}")
	sources = definition.get("sources")
	if isinstance(sources, list):
		for source in sources:
			if not isinstance(source, dict) or not isinstance(source.get("id"), str):
				continue
			if source["id"] not in text:
				raise CuratorError(f"Knowledge companion {label} must reference source {source['id']!r}")


def _validate_definition(root: Path, definition: dict[str, Any], knowledge_target: Path) -> None:
	errors = validate_against_schema(definition, root / "schemas" / "machine.schema.json", "Spike 1 seed")
	try:
		semantic_errors = validate_machine(definition, root)
	except (AttributeError, KeyError, TypeError, ValueError) as error:
		raise CuratorError(f"Spike 1 seed could not complete semantic validation: {error}") from error
	if not knowledge_target.is_file():
		knowledge = definition.get("knowledge", {})
		knowledge_path = knowledge.get("path") if isinstance(knowledge, dict) else None
		expected = f"$.knowledge.path: referenced note does not exist: {knowledge_path}"
		semantic_errors = [error for error in semantic_errors if error != expected]
	errors.extend(semantic_errors)
	if errors:
		raise CuratorError("Spike 1 seed validation failed:\n" + "\n".join(f"- {error}" for error in errors))


def _spatial_presence(record: dict[str, Any]) -> tuple[str, str | None, list[str]]:
	spatial = record.get("spatial")
	if not isinstance(spatial, dict):
		return "absent", None, []
	status = spatial.get("status")
	roles = sorted({placement.get("role") for placement in spatial.get("placements", []) if isinstance(placement, dict) and isinstance(placement.get("role"), str)})
	if status == "not_applicable":
		return "not_applicable", "not_applicable", roles
	return "declared", status if isinstance(status, str) else None, roles


def _inventory(definition: dict[str, Any]) -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for collection in ("inputs", "outputs"):
		for record in definition.get(collection, []):
			if not isinstance(record, dict):
				continue
			presence, status, roles = _spatial_presence(record)
			provenance = record.get("provenance")
			items.append({
				"collection": collection,
				"id": record.get("id"),
				"binding": record.get("binding"),
				"provenance_status": provenance.get("status") if isinstance(provenance, dict) else None,
				"source_refs": list(provenance.get("source_refs", [])) if isinstance(provenance, dict) else [],
				"spatial_presence": presence,
				"spatial_status": status,
				"placement_roles": roles,
			})
	for record in definition.get("displays", []):
		if not isinstance(record, dict):
			continue
		presence, status, roles = _spatial_presence(record)
		provenance = record.get("provenance")
		items.append({
			"collection": "displays",
			"id": record.get("id"),
			"provenance_status": provenance.get("status") if isinstance(provenance, dict) else None,
			"source_refs": list(provenance.get("source_refs", [])) if isinstance(provenance, dict) else [],
			"spatial_presence": presence,
			"spatial_status": status,
			"placement_roles": roles,
		})
	return items


def _source_identities(definition: dict[str, Any]) -> list[dict[str, Any]]:
	identities: list[dict[str, Any]] = []
	for source in definition.get("sources", []):
		if not isinstance(source, dict):
			continue
		excerpts = []
		for excerpt in source.get("excerpts", []):
			if isinstance(excerpt, dict):
				excerpts.append({key: excerpt.get(key) for key in ("id", "path", "sha256")})
		identities.append({
			"id": source.get("id"),
			"kind": source.get("kind"),
			"revision": source.get("revision"),
			"sha256": source.get("sha256"),
			"excerpts": sorted(excerpts, key=lambda item: str(item["id"])),
		})
	return sorted(identities, key=lambda item: str(item["id"]))


def spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	coverage = definition["coverage"]
	devices = _inventory(definition)
	blockers = [
		{"collection": device["collection"], "id": device["id"], "binding": device.get("binding"), "spatial_presence": device["spatial_presence"], "spatial_status": device["spatial_status"]}
		for device in devices
		if device["spatial_presence"] == "absent" or device["spatial_status"] in {"candidate", "conflicted"}
	]
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"coordinate_convention": "x=0 left, x=1 right, y=0 rear/backglass end, y=1 apron/front; normalized VPX/player view.",
		"decision": {"status": "partial", "reason": "Copied from the reviewed partial seed; no positions are inferred by this curator."},
		"coverage_missing": list(coverage["missing"]),
		"devices": devices,
		"spatial_blockers": blockers,
		"source_identities": _source_identities(definition),
		"projection_classes": [],
	}


def report_markdown(report: dict[str, Any]) -> str:
	lines = [
		f"# {report['machine_id']} spatial blockers",
		"",
		"Decision: **partial**. This inventory reproduces declared bindings and spatial states; it does not infer positions.",
		"",
		f"Coordinate convention: {report['coordinate_convention']}",
		"",
		"## Coverage blockers",
		"",
		", ".join(f"`{item}`" for item in report["coverage_missing"]) or "None declared.",
		"",
		"## Device inventory",
		"",
		"| Collection | Device | Binding | Provenance | Spatial presence |",
		"| --- | --- | --- | --- | --- |",
	]
	for device in report["devices"]:
		binding = device.get("binding")
		binding_text = "" if not isinstance(binding, dict) else f"{binding.get('group')}:{binding.get('device')}"
		state = device["spatial_presence"] if device["spatial_status"] is None else f"{device['spatial_presence']} ({device['spatial_status']})"
		lines.append(f"| {device['collection']} | {device['id']} | {binding_text} | {device['provenance_status']} | {state} |")
	lines.extend(["", "## Sources", ""])
	for source in report["source_identities"]:
		digest = source["sha256"] or "no SHA-256 asserted"
		lines.append(f"- `{source['id']}` ({source['kind']}): `{digest}`")
	lines.extend(["", "## Projection classes", "", "None declared by the schema-valid seed; no class or coordinate was inferred.", ""])
	return "\n".join(lines)


def artifacts(root: Path, game: str) -> dict[Path, bytes]:
	root = _repository_root(root)
	seed_path, seed_bytes, definition = _load_seed(root, game)
	definition_path, knowledge_path, report_path, markdown_path, slug, year = _machine_paths(root, definition)
	_require_no_author_ready(root, slug, year)
	knowledge_bytes = _load_knowledge(seed_path, root, definition)
	_validate_definition(root, definition, knowledge_path)
	report = spatial_report(definition)
	markdown = report_markdown(report)
	if game == "supreme_101":
		import curate_supreme_x_stern_2018 as supreme
		report = supreme.enrich_spatial_report(root, definition, report)
		markdown = supreme.report_markdown(report)
	return {
		definition_path: seed_bytes,
		knowledge_path: knowledge_bytes,
		report_path: canonical_bytes(report),
		markdown_path: markdown.encode("utf-8"),
	}


def check(game: str, root: Path = ROOT) -> None:
	root = _repository_root(root)
	for path, expected in artifacts(root, game).items():
		if not path.is_file():
			raise CuratorError(f"Artifact is missing: {path.relative_to(root).as_posix()}")
		if path.read_bytes() != expected:
			raise CuratorError(f"Artifact drift: {path.relative_to(root).as_posix()}")
	print(f"Spike 1 {game}: definition, knowledge and spatial blockers match.")


def regenerate(game: str, root: Path = ROOT) -> None:
	root = _repository_root(root)
	for path, payload in artifacts(root, game).items():
		if path.suffix == ".json":
			write_json(path, load_json_bytes(payload))
		else:
			write_bytes(path, payload)
	print(f"Spike 1 {game}: regenerated partial definition, knowledge and spatial blockers.")


def load_json_bytes(payload: bytes) -> dict[str, Any]:
	try:
		value = json.loads(payload.decode("utf-8"))
	except (UnicodeDecodeError, json.JSONDecodeError) as error:
		raise CuratorError(f"Generated JSON payload is invalid: {error}") from error
	if not isinstance(value, dict):
		raise CuratorError("Generated JSON payload must be an object")
	return value


def run(game: str, regenerate_requested: bool, root: Path = ROOT) -> None:
	if regenerate_requested:
		regenerate(game, root)
	else:
		check(game, root)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--game", required=True, help="Exact Stern Spike 1 PinMAME driver ID")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	try:
		run(args.game, args.regenerate)
	except CuratorError as error:
		raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
	main()
