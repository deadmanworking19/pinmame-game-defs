"""Blackout (1980) placements from the retained S34 v1.1 table; physical facts stay in the curator.

Every placement is an `observed` reading of one pinned table object (or the mean of a pinned bank of
drop targets for a bank's series switch and reset coil). No drawing callout check backs any of them,
and no lamp is placed because no public lamp in the retained table sits on a bulb.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.spatial import _round_point

SEED = Path("tools/seeds/williams/blackout-1980-spatial.json")
SEED_SHA = "0afb8cedd8d45765c7e72f322ab8ef89a241f67536affda6a53179999d4f44e2"
EXCERPT = Path("evidence/excerpts/williams.blackout.1980/spatial-method.md")
EXCERPT_SHA = "61744cf8bee9121898a78a81fbc6178e1ce38ebbaacd9284bbfae6bb4b191c06"
RETENTION_SHA = "c60e94aab17d75dcef9f18150871d1834e1b4b0610c2abc8fa09c72cc6348846"
MACHINE_ID = "williams.blackout.1980"
GAME = "blkou_l1"
TABLE = "geometry.blackout-s34"
EMBEDDED = "script.blackout-embedded"
GROUPS = {"switch": "pinmame.input.switch", "lamp": "pinmame.output.lamp", "solenoid": "pinmame.output.solenoid"}
ROLES = {"switch": "sensor", "lamp": "emitter", "solenoid": "effect"}


def sha(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def read_seed(root: Path) -> dict[str, Any]:
	for path, digest in [(SEED, SEED_SHA), (EXCERPT, EXCERPT_SHA)]:
		if not (root / path).is_file() or sha(root / path) != digest:
			raise RuntimeError(f"spatial evidence absent or changed: {path}")
	return load_json(root / SEED)


def normalized(seed: dict[str, Any], raw: tuple[float, float]) -> tuple[float, float]:
	b = seed["table"]["bounds"]
	point = ((raw[0] - b["left"]) / (b["right"] - b["left"]), (raw[1] - b["top"]) / (b["bottom"] - b["top"]))
	if not all(0 <= v <= 1 for v in point):
		raise ValueError(f"out-of-range source point: {raw}")
	return tuple(_round_point(v) for v in point)


def object_point(seed: dict[str, Any], name: str, method: str) -> tuple[float, float]:
	fields = seed["objects"][name]["fields"]
	if method == "drag_point_centroid":
		pts = fields["drag_points"]
		return tuple(sum(p[a] for p in pts) / len(pts) for a in ("x", "y"))
	if method == "slingshot_edge_midpoint":
		pts = fields["drag_points"]
		edges = [(p, pts[(i + 1) % len(pts)]) for i, p in enumerate(pts) if p["is_slingshot"]]
		if len(edges) != 1:
			raise ValueError(f"expected one active sling edge: {name}")
		return tuple((edges[0][0][a] + edges[0][1][a]) / 2 for a in ("x", "y"))
	if method not in {"center", "position"} or method not in fields:
		raise ValueError(f"object {name} has no {method}")
	return (fields[method]["x"], fields[method]["y"])


def spec_point(seed: dict[str, Any], spec: dict[str, Any]) -> tuple[float, float]:
	if spec["method"] == "object_centroid":
		points = [object_point(seed, name, "position") for name in spec["objects"]]
		return tuple(sum(p[i] for p in points) / len(points) for i in (0, 1))
	if len(spec["objects"]) != 1:
		raise ValueError(f"one object expected for {spec['group']} {spec['address']}")
	return object_point(seed, spec["objects"][0], spec["method"])


def rows(seed: dict[str, Any]) -> list[dict[str, Any]]:
	out = []
	for spec in seed["specs"]:
		x, y = normalized(seed, spec_point(seed, spec))
		out.append({**spec, "placement_id": f"placement.{spec['group']}-{spec['address']}", "x": x, "y": y, "status": "observed"})
	keys = [(r["group"], r["address"]) for r in out]
	if len(keys) != len(set(keys)):
		raise RuntimeError("a device has two placement specs")
	return out


def devices_by_key(definition: dict[str, Any]) -> dict[str, dict[str, Any]]:
	inverse = {v: k for k, v in GROUPS.items()}
	return {f"{inverse[d['binding']['group']]}-{d['binding']['device']}": d
			for kind in ("inputs", "outputs") for d in definition[kind] if d["binding"]["group"] in inverse}


def apply(definition: dict[str, Any], root: Path) -> dict[str, Any]:
	seed = read_seed(root)
	devices = devices_by_key(definition)
	for row in rows(seed):
		d = devices[f"{row['group']}-{row['address']}"]
		if "spatial" in d:
			raise RuntimeError(f"{d['id']} already carries a spatial disposition")
		placement = {"id": row["placement_id"], "role": ROLES[row["group"]], "space": "playfield", "x": row["x"], "y": row["y"],
			"provenance": {"status": "observed", "source_refs": [TABLE, EMBEDDED]}}
		d["spatial"] = {"status": "observed", "placements": [placement]}
		objects = ", ".join(row["objects"])
		d.setdefault("physical", {})
		d["physical"]["notes"] = (d["physical"].get("notes", "") + f" Spatial: {row['classification'].replace('_', ' ')} from retained-table object {objects} "
			f"({row['method'].replace('_', ' ')}); observed only, no drawing check.").strip()
	for key, reason in seed["unplaced"].items():
		d = devices[key]
		if "spatial" in d:
			raise RuntimeError(f"unplaced device {d['id']} carries a spatial disposition")
		d.setdefault("physical", {})
		d["physical"]["notes"] = (d["physical"].get("notes", "") + " Spatial unresolved: " + reason).strip()
	b = seed["table"]["bounds"]
	definition["machine"]["playfield"] = {"width": int(b["right"] - b["left"]), "height": int(b["bottom"] - b["top"]), "units": "vpx",
		"provenance": {"status": "observed", "source_refs": [TABLE]}}
	return definition


def report(definition: dict[str, Any], root: Path) -> dict[str, Any]:
	seed = read_seed(root)
	devices = devices_by_key(definition)
	placed = rows(seed)
	for row in placed:
		row["device_id"] = devices[f"{row['group']}-{row['address']}"]["id"]
		row["raw_point"] = [round(v, 5) for v in spec_point(seed, row)]
	missing = sorted(d["id"] for kind in ("inputs", "outputs") for d in definition[kind] if "spatial" not in d)
	if missing != sorted(devices[k]["id"] for k in seed["unplaced"]):
		raise RuntimeError("spatial unresolved-device accounting differs from the definition")
	candidates = [{"object": name, "drag_points": seed["objects"][name]["fields"]["drag_points"],
		"normalized_drag_point_centroid": list(normalized(seed, object_point(seed, name, "drag_point_centroid"))),
		"normalized_slingshot_edge_midpoint": list(normalized(seed, object_point(seed, name, "slingshot_edge_midpoint"))),
		"role": "rubber hit edge; not a leaf-switch position"} for name in seed["standup_candidates"]]
	bulbs = [{"object": name, "raw_center": [seed["objects"][name]["fields"]["center"][a] for a in ("x", "y")],
		"normalized_center": list(normalized(seed, object_point(seed, name, "center"))),
		"show_bulb_mesh": seed["objects"][name]["fields"]["show_bulb_mesh"],
		"role": "general-illumination bulb geometry switched by the script from solenoid 15; no public lamp drives it"}
		for name in seed["unbound_bulb_lights"]["lights"]]
	return {
		"format": "pinmame-spatial-blockers", "version": 2, "machine_id": MACHINE_ID, "decision": "partial",
		"coordinate_convention": "x 0 left / 1 right; y 0 rear / 1 apron, player view; VPX normalized by the table's own bounds with the shared six-decimal rounding",
		"table_geometry": {**seed["table"], "retention_sha256": RETENTION_SHA},
		"extraction_manifest": {"algorithm": "tools/build_external_evidence_manifest.py canonical sorted POSIX path/size/SHA256 entries, compact sorted-key JSON plus LF; exclude only manifest.json/manifest.sha256",
			"sha256": seed["table"]["manifest_sha256"], "file_count": seed["table"]["file_count"], "byte_count": seed["table"]["byte_count"]},
		"seed": {"path": SEED.as_posix(), "sha256": SEED_SHA}, "method_excerpt": {"path": EXCERPT.as_posix(), "sha256": EXCERPT_SHA},
		"counts": dict(sorted(Counter(r["group"] for r in placed).items())),
		"placements": placed,
		"unplaced_devices": missing,
		"unplaced_reasons": {devices[k]["id"]: v for k, v in sorted(seed["unplaced"].items(), key=lambda kv: devices[kv[0]]["id"])},
		"not_applicable": {d["id"]: d["spatial"]["reason"] for kind in ("inputs", "outputs", "displays") for d in definition[kind]
			if d.get("spatial", {}).get("status") == "not_applicable"},
		"standup_candidate_geometry": candidates,
		"unbound_bulb_geometry": {"authority": seed["unbound_bulb_lights"]["authority"], "lights": bulbs},
		"blockers": [
			"Lamps 1-10, 12-49 and 56 have no placement: the retained table draws every playfield lamp as an insert light with no bulb (and has no light for 56), and no lamp-location drawing was measured. A table that models the bulbs, or a measured factory drawing, would supply them.",
			"Switches 9, 19, 32 and 38 and solenoid 1 have no defensible contact or coil geometry in the retained table; the reasons are listed per device.",
			"Every placement is observed from one community table that is not known to have been played; none is checked against a factory drawing.",
		],
	}


def report_markdown(report: dict[str, Any]) -> str:
	counts = report["counts"]
	return ("# Blackout (1980) spatial blockers\n\nCoverage remains **partial**. "
		f"The retained S34 v1.1 table supplies {counts.get('switch', 0)} switch placements and {counts.get('solenoid', 0)} coil placements, all `observed`; "
		"no lamp is placed. The JSON report lists each object, method, raw and normalized point, every unplaced device with its reason, "
		"the two standup rubber walls and the 24 general-illumination bulb lights.\n\n"
		+ "\n".join("- " + s for s in report["blockers"]) + "\n")


def verify_external(root: Path, configured_root: Callable[[str], Path | None]) -> None:
	seed = read_seed(root)
	t = seed["table"]
	vpx = configured_root("PINMAME_VPX_SOURCES_ROOT")
	if vpx is None:
		return
	directory = vpx / t["path"]
	source = directory / t["filename"]
	if not source.is_file() or sha(source) != t["sha256"] or source.stat().st_size != t["size"]:
		raise RuntimeError("retained spatial VPX absent or changed")
	if not (directory / "retention.json").is_file() or sha(directory / "retention.json") != RETENTION_SHA:
		raise RuntimeError("spatial retention metadata absent or changed")
	extracted = directory / t["extraction"]
	if check_manifest(extracted, GAME) != t["manifest_sha256"]:
		raise RuntimeError("spatial extraction manifest changed")
	manifest = load_json(extracted / "manifest.json")
	if len(manifest["files"]) != t["file_count"] or sum(f["size"] for f in manifest["files"]) != t["byte_count"]:
		raise RuntimeError("spatial extraction totals changed")
	for rel, digest in t["inputs"].items():
		if sha(extracted / rel) != digest:
			raise RuntimeError(f"spatial source changed: {rel}")
	if sha(extracted / "script.vbs") != t["script_sha256"]:
		raise RuntimeError("embedded script changed")
	data = load_json(extracted / "gamedata.json")
	if {k: data[k] for k in t["bounds"]} != t["bounds"]:
		raise RuntimeError("spatial normalization bounds changed")
	for name, o in seed["objects"].items():
		if sha(extracted / o["path"]) != o["sha256"]:
			raise RuntimeError(f"spatial object changed: {name}")
		typ, value = next(iter(load_json(extracted / o["path"]).items()))
		fields = {k: value[k] for k in o["fields"] if k != "drag_points"}
		for k in ("center", "position"):
			if k in fields:
				fields[k] = {"x": fields[k]["x"], "y": fields[k]["y"]}
		if "drag_points" in o["fields"]:
			fields["drag_points"] = [{k: p[k] for k in ("x", "y", "is_slingshot")} for p in value["drag_points"]]
		if typ != o["type"] or fields != o["fields"]:
			raise RuntimeError(f"spatial derived fields differ: {name}")
	collections = {c["name"]: c["items"] for c in load_json(extracted / "collections.json")}
	gi = collections.get("GI", [])
	if sorted(gi) != seed["unbound_bulb_lights"]["gi_collection"] or not set(seed["unbound_bulb_lights"]["lights"]) <= set(gi):
		raise RuntimeError("table light grouping changed")
	bulbs = []
	for path in (extracted / "gameitems").glob("Light.*.json"):
		value = next(iter(load_json(path).values()))
		if value.get("is_bulb_light") and value.get("show_bulb_mesh"):
			bulbs.append(path.name[len("Light."):-len(".json")])
	if sorted(bulbs) != sorted(seed["unbound_bulb_lights"]["lights"]):
		raise RuntimeError("table bulb-mesh lights changed")
