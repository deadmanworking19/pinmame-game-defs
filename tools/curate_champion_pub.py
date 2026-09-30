"""Reproduce the source-backed Champion Pub definition and its spatial audit.

The reviewed fact seed retains literal factory rows separately from controller
semantics. Build/check do not read external copyrighted artifacts; optional
verification proves their exact retained bytes. Unknowns remain explicit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_game_defs.spatial import _round_point
from pinmame_game_defs.workspace import resolve_working_root


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.champion-pub.1998"
DEFINITION_PATH = Path("machines/partial/bally/champion-pub-1998.json")
AUTHOR_READY_PATH = Path("machines/author-ready/bally/champion-pub-1998.json")
FACTS_PATH = Path("tools/seeds/bally/champion-pub-1998-facts.json")
SEED_PATH = Path("tools/seeds/bally/champion-pub-1998.json")
KNOWLEDGE_PATH = Path("knowledge/bally/champion-pub-1998.md")
REPORT_PATH = Path("reports/spatial/bally/champion-pub-1998.json")
REPORT_MARKDOWN_PATH = REPORT_PATH.with_suffix(".md")
EXCERPT_PREFIX = f"evidence/excerpts/{MACHINE_ID}"
REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CORE = "pinmame.core.champion-pub"
MANUAL = "manual.champion-pub.operations"
SCRIPT = "vpx-script.champion-pub-mfuegemann-1-2"
COMPANION = "vpx-script.champion-pub.companion-core"
TABLE = "vpx-table.champion-pub-mfuegemann-1-2"
SPATIAL = "human-review.champion-pub-spatial"
MATRIX_ADDRESSES = tuple(c * 10 + r for c in range(1, 9) for r in range(1, 9))
EXTRA_LAMP_ADDRESSES = tuple(c * 10 + r for c in range(9, 13) for r in range(1, 9))
OPTO_MASK = {3: 0x3F, 4: 0xFF}


def sha256(path: Path) -> str:
	with path.open("rb") as stream:
		return hashlib.file_digest(stream, "sha256").hexdigest()


def slug(label: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def not_applicable(reason: str, *refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def facts(root: Path = ROOT) -> dict[str, Any]:
	data = load_json(root / FACTS_PATH)
	if data.get("machine_id") != MACHINE_ID or data.get("pinmame_revision") != REVISION:
		raise RuntimeError("Champion Pub facts have the wrong identity or PinMAME revision")
	if data.get("coverage", {}).get("status") != "partial":
		raise RuntimeError("Champion Pub promotion requires independent compatibility, wiring and spatial review")
	for field, expected in (("switches", set(MATRIX_ADDRESSES)), ("lamps", set(MATRIX_ADDRESSES)),
		("solenoids", set(range(1, 29))), ("public_solenoids", set(range(1, 51))),
		("extra_lamps", set(EXTRA_LAMP_ADDRESSES)), ("dedicated", set(range(1, 9))),
		("flipper_inputs", set(range(111, 119))), ("gi", set(range(5)))):
		if {int(address) for address in data[field]} != expected:
			raise RuntimeError(f"Incomplete {field} fact inventory")
	for source in data["sources"]:
		for excerpt in source.get("excerpts", []):
			path = root / excerpt["path"]
			if not path.is_file() or sha256(path) != excerpt["sha256"]:
				raise RuntimeError(f"Champion Pub excerpt drift: {excerpt['path']}")
			if "image" in excerpt:
				image = root / excerpt["image"]
				if not image.is_file() or sha256(image) != excerpt.get("image_sha256"):
					raise RuntimeError(f"Champion Pub excerpt image drift: {excerpt['image']}")
	return data


def device(kind: str, label: str, group: str, address: int, *, availability: str = "used", refs: tuple[str, ...] = (MANUAL, CORE), identifier: str | None = None, **fields: Any) -> dict[str, Any]:
	return {
		"id": identifier or f"{kind}.{slug(label)}", "label": label, "kind": kind,
		"binding": {"group": f"pinmame.{group}", "device": address},
		"aliases": [{"namespace": f"pinmame.{group.split('.')[-1]}", "value": str(address)}],
		"availability": availability, "provenance": provenance(*refs), **fields,
	}


def add_spatial(item: dict[str, Any], data: dict[str, Any], role: str) -> None:
	key = f"{item['binding']['group']}:{item['binding']['device']}"
	record = data["positions"].get(key)
	if not record:
		return
	placements = []
	for index, point in enumerate(record["points"], 1):
		placements.append({
			"id": f"{item['id']}.placement-{index}", "role": role, "space": "playfield",
			"x": _round_point(point["x"] / data["bounds"]["right"]),
			"y": _round_point(point["y"] / data["bounds"]["bottom"]),
			"provenance": provenance(TABLE, SCRIPT, MANUAL, SPATIAL, status=record["status"]),
		})
	item["spatial"] = {"status": record["status"], "placements": placements}
	if record.get("note"):
		item.setdefault("physical", {})["notes"] = item.get("physical", {}).get("notes", "") + " " + record["note"]


def inputs(data: dict[str, Any]) -> list[dict[str, Any]]:
	items = []
	for address, row in sorted(data["dedicated"].items(), key=lambda pair: int(pair[0])):
		number = int(address)
		items.append(device("switch", row["label"], "input.switch", number,
			availability="optional" if number == 4 else "used", normally_closed=False,
			roles=[row["role"]], physical={"location": "coin door", "switch_type": "other" if number <= 4 else "button", "notes": row["note"]},
			wiring=row["wiring"], spatial=not_applicable("cabinet_or_service", MANUAL, CORE)))
	for address in MATRIX_ADDRESSES:
		row = data["switches"][str(address)]
		unused = row["label"] == "Not Used"
		constant = address == 24
		kind = "constant" if constant else "switch"
		label = f"Not Used Matrix Position {address}" if unused else row["label"]
		physical = copy.deepcopy(row["physical"])
		physical["notes"] = row.get("note", "Printed switch location and matrix row.")
		item = device(kind, label, "input.switch", address, identifier=f"{kind}.matrix-{address}",
			availability="unused" if unused else "used", physical=physical, wiring=row["wiring"],
			refs=tuple(row.get("source_refs", (MANUAL, CORE))))
		if constant:
			item.update(constant_active=True, initial_active=True, normally_closed=True, spatial=not_applicable("constant", MANUAL, CORE))
		elif unused:
			item["spatial"] = not_applicable("unused", MANUAL)
		elif address in {13, 14, 21, 22, 23}:
			item.update(roles=[{13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.launch"}[address]], spatial=not_applicable("cabinet_or_service", MANUAL))
		else:
			add_spatial(item, data, "sensor")
		if not unused and not constant and row.get("normally_closed") is not None:
			item["normally_closed"] = row["normally_closed"]
		if row.get("initial_active") is not None:
			item["initial_active"] = row["initial_active"]
		if row.get("pulse"):
			item["pulse"] = True
		items.append(item)
	for address in range(111, 119):
		row = data["flipper_inputs"][str(address)]
		item = device(row["kind"], row["label"], "input.switch", address,
			availability=row["availability"], identifier=f"switch.flipper-{address}", physical=row["physical"],
			refs=tuple(row.get("source_refs", (MANUAL, CORE))))
		if row["availability"] == "unused":
			item["spatial"] = not_applicable("unused", MANUAL, CORE)
		elif row["kind"] == "virtual":
			item["spatial"] = not_applicable("virtual", MANUAL, CORE)
		elif address in (111, 113):
			add_spatial(item, data, "sensor")
		else:
			item["spatial"] = not_applicable("cabinet_or_service", MANUAL, CORE)
		if row["availability"] != "unused":
			item["roles"] = [row["role"]]
			if row.get("normally_closed") is not None:
				item["normally_closed"] = row["normally_closed"]
			if row.get("wiring"):
				item["wiring"] = row["wiring"]
		items.append(item)
	for address in range(1, 9):
		items.append(device("dip_switch", f"CPU Option DIP Bit {address}", "input.dip", address, identifier=f"dip.cpu-{address}",
			refs=(CORE, MANUAL), physical={"location": "CPU board option switch bank", "switch_type": "dip", "notes": data["dip_note"]},
			spatial=not_applicable("dip_switch", CORE, MANUAL)))
	return items


def outputs(data: dict[str, Any]) -> list[dict[str, Any]]:
	items = []
	for address in range(1, 51):
		row = data["public_solenoids"][str(address)]
		item = device(row["kind"], row["label"], "output.solenoid", address,
			identifier=f"{row['kind']}.solenoid-{address}", availability=row["availability"], physical=copy.deepcopy(row["physical"]))
		if row.get("wiring"):
			item["wiring"] = row["wiring"]
		if row.get("roles"):
			item["roles"] = row["roles"]
		if row.get("spatial_reason"):
			item["spatial"] = not_applicable(row["spatial_reason"], CORE, MANUAL)
		else:
			add_spatial(item, data, "emitter" if row["kind"] == "flasher" else "effect")
		items.append(item)
	for address in MATRIX_ADDRESSES + EXTRA_LAMP_ADDRESSES:
		row = data["lamps" if address < 91 else "extra_lamps"][str(address)]
		item = device(row["kind"], row["label"], "output.lamp", address, identifier=f"{row['kind']}.lamp-{address}",
			availability=row["availability"], physical=copy.deepcopy(row["physical"]), refs=(MANUAL, CORE, SCRIPT, COMPANION))
		item["provenance"]["status"] = row.get("status", "validated")
		if row.get("wiring"):
			item["wiring"] = row["wiring"]
		if row.get("roles"):
			item["roles"] = row["roles"]
		if row.get("spatial_reason"):
			item["spatial"] = not_applicable(row["spatial_reason"], CORE, MANUAL)
		else:
			add_spatial(item, data, "emitter")
		items.append(item)
	for address in range(5):
		row = data["gi"][str(address)]
		item = device("gi", row["label"], "output.gi", address, identifier=f"gi.string-{address + 1}", physical=row["physical"], wiring=row["wiring"],
			refs=tuple(row.get("source_refs", (MANUAL, CORE))))
		item["provenance"]["status"] = row.get("status", "validated")
		if row.get("roles"):
			item["roles"] = row["roles"]
		if row.get("spatial_reason"):
			item["spatial"] = not_applicable(row["spatial_reason"], MANUAL, CORE)
		else:
			add_spatial(item, data, "emitter")
		items.append(item)
	return items


def build(root: Path = ROOT) -> dict[str, Any]:
	data = facts(root)
	return {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "The Champion Pub", "manufacturer": "Bally", "year": 1998,
			"kind": "physical_pinball", "model_number": "50063", "ipdb_id": 4358, "opdb_id": "G42k0-MQ6w9",
			"playfield": {"width": data["bounds"]["right"], "height": data["bounds"]["bottom"], "units": "vpx", "provenance": provenance(TABLE)}},
		"controller": {"platform": "pinmame.wpc-95", "hardware_generation": "0x80", "inversion_applied_by_emulator": True},
		"coverage": data["coverage"], "drivers": data["drivers"], "inputs": inputs(data), "outputs": outputs(data),
		"displays": [{"id": "display.main", "label": "Main Dot Matrix Display", "kind": "dmd", "width": 128, "height": 32,
			"controller_index": 0, "provenance": provenance(CORE, MANUAL), "spatial": not_applicable("cabinet_or_service", CORE, MANUAL)}],
		"mechanisms": data["mechanisms"], "relationships": data["relationships"], "sources": data["sources"],
		"knowledge": {"path": KNOWLEDGE_PATH.as_posix(), "status": data["knowledge_status"]}, "conflicts": data["conflicts"],
	}


def spatial_report(definition: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
	records = []
	for collection in ("inputs", "outputs"):
		for item in definition[collection]:
			spatial = item.get("spatial")
			key = f"{item['binding']['group']}:{item['binding']['device']}"
			records.append({"id": item["id"], "binding": item["binding"], "availability": item["availability"],
				"status": spatial["status"] if spatial else "unplaced", "placements": spatial.get("placements", []) if spatial else [],
				"coordinate_evidence": data["positions"].get(key),
				"blocker": data["spatial_blockers"].get(key)})
	return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": "x=0 left, x=1 right; y=0 rear, y=1 front; normalized VPX/player view.",
		"bounds": data["bounds"], "transformation": "x/right, y/bottom, rounded with the repository spatial helper to six decimals.",
		"extraction": data["extraction"], "source_artifacts": data["artifacts"], "world_mesh": data["world_mesh"],
		"manual_reconciliation": data["manual_reconciliation"],
		"devices": records, "coverage": definition["coverage"], "promotion_decision": data["promotion_decision"]}


def report_markdown(report: dict[str, Any]) -> str:
	lines = ["# The Champion Pub (1998) spatial audit", "", report["promotion_decision"], "",
		"Coordinates use the retained table's 970 × 2100 bounds. Each placement retains its exact object or reproducible factory measurement in the JSON audit.", "",
		"| Device | Public binding | Placement state | Blocker |", "| --- | --- | --- | --- |"]
	for row in report["devices"]:
		binding = row["binding"]
		lines.append(f"| {row['id']} | {binding['group']}:{binding['device']} | {row['status']} | {row['blocker'] or ''} |")
	return "\n".join(lines) + "\n"


def artifacts(root: Path = ROOT) -> dict[Path, bytes]:
	data = facts(root)
	definition = build(root)
	report = spatial_report(definition, data)
	return {DEFINITION_PATH: canonical_bytes(definition), SEED_PATH: canonical_bytes(definition),
		REPORT_PATH: canonical_bytes(report), REPORT_MARKDOWN_PATH: report_markdown(report).encode("utf-8"),
		KNOWLEDGE_PATH: data["knowledge"].encode("utf-8")}


def check(root: Path = ROOT) -> None:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Champion Pub author-ready artifact needs a reviewed promotion, not an overwrite")
	for path, expected in artifacts(root).items():
		if not (root / path).is_file() or (root / path).read_bytes() != expected:
			raise RuntimeError(f"Champion Pub artifact drift: {path}")
	print("Champion Pub definition, seed, knowledge and spatial audit match.")


def generate(root: Path = ROOT) -> Path:
	if (root / AUTHOR_READY_PATH).exists():
		raise RuntimeError("Refusing to overwrite an author-ready Champion Pub definition")
	for path, payload in artifacts(root).items():
		if path.suffix == ".json":
			write_json(root / path, json.loads(payload))
		else:
			write_text(root / path, payload.decode("utf-8"))
	return root / DEFINITION_PATH


def extraction_manifest(directory: Path) -> list[dict[str, Any]]:
	return [{"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
		for path in sorted(directory.rglob("*"), key=lambda path: path.relative_to(directory).as_posix()) if path.is_file()]


def verify_evidence(root: Path = ROOT) -> None:
	data = facts(root)
	working = resolve_working_root(root)
	checkout = working / "source-checkouts/pinmame"
	revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, check=True, capture_output=True, text=True).stdout.strip()
	dirty = subprocess.run(["git", "status", "--porcelain"], cwd=checkout, check=True, capture_output=True, text=True).stdout.strip()
	if revision != REVISION or dirty:
		raise RuntimeError("Pinned PinMAME evidence checkout must match the revision and be clean")
	for artifact in data["artifacts"]:
		path = working / artifact["path"]
		if not path.is_file() or sha256(path) != artifact["sha256"]:
			raise RuntimeError(f"Retained Champion Pub artifact drift: {path}")
	extraction = data["extraction"]
	rows = extraction_manifest(working / extraction["path"])
	digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
	if len(rows) != extraction["file_count"] or sum(row["bytes"] for row in rows) != extraction["total_bytes"] or digest != extraction["manifest_sha256"]:
		raise RuntimeError("Retained Champion Pub extraction manifest drift")
	print("Champion Pub retained source bytes and complete extraction verified.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	mode.add_argument("--verify-evidence", action="store_true")
	args = parser.parse_args()
	if args.check:
		check()
	elif args.verify_evidence:
		verify_evidence()
	else:
		print(f"Wrote {generate()}")


if __name__ == "__main__":
	main()
