"""Reproduce the reviewed Gold edition, its knowledge note and spatial audit.

Both factual seeds and geometry evidence are pinned. Recompute placements from
their raw anchors, preserve physical quantities and refuse incomplete promotion.
Optional external roots are checked strictly whenever supplied.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import math
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes
from pinmame_game_defs.validation import validate_machine
from build_external_evidence_manifest import build_manifest, canonical_bytes as manifest_bytes
from drawing_callouts import apply, distance, fit

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.the-addams-family-gold.1994"
SLUG = "the-addams-family-gold-1994"
SEED_PATH = Path("tools/seeds/bally") / f"{SLUG}.json"
PARTIAL_PATH = Path("machines/partial/bally") / f"{SLUG}.json"
DEFINITION_PATH = Path("machines/author-ready/bally") / f"{SLUG}.json"
KNOWLEDGE_PATH = Path("knowledge/bally") / f"{SLUG}.md"
REPORT_PATH = Path("reports/spatial/bally") / f"{SLUG}.json"
REPORT_MD_PATH = REPORT_PATH.with_suffix(".md")
EVIDENCE_PATH = Path("tools/seeds/bally") / f"{SLUG}-evidence.json"
SEED_SHA256 = "6665fd05ffa9a2516d7741e27e3e7c12e7523e20f8076d19914d95d3e08db87e"
EVIDENCE_SHA256 = "5848af2fc33119e17936f97314fb28b31177ffa4b52b41771f282704db6027b6"
PARTIAL_SHA256 = "5d76415fe470632b5ed6bd3c81925454965c5a8817d8d911affb0d378d6a38c4"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DRIVERS = {"tafg_da2", "tafg_da3", "tafg_dx3", "tafg_h3", "tafg_i3", "tafg_i3bs", "tafg_la2", "tafg_la3", "tafg_lx3"}
MATRIX = {10 * c + r for c in range(1, 9) for r in range(1, 9)}
UNUSED_SWITCHES = {12, 23, 28, 46, 52, 83, 88}
OPTOS = {53, 54, 55, 56, 57, 84, 85}
EXTRACTION_RELATIVE_PATH = Path("bally") / SLUG / "extracted-vpxtool"
PHONE_PROJECTION_CLASS = "stock-socket-envelope-to-own-mount"
PHONE_MOUNT_BOUNDS = [[916.7273, 227.6914, -198.9924], [928.5227, 239.3077, -195.2097]]
MOJIBAKE_MARKERS = ("\u00e2\u20ac", "\u00c2\u00b1", "\u00c3\u2014")


def bindings(definition: dict[str, Any], collection: str, group: str) -> dict[int, dict[str, Any]]:
	return {v["binding"]["device"]: v for v in definition[collection] if v["binding"]["group"] == group}


def require(condition: bool, message: str) -> None:
	if not condition:
		raise ValueError(f"Gold: {message}")


def assert_reviewed_contract(d: dict[str, Any]) -> None:
	"""Guard historically wrong physical claims independently of the seed hash."""
	prose = canonical_bytes(d).decode("utf-8", "strict")
	require(not any(marker in prose for marker in MOJIBAKE_MARKERS), "UTF-8 prose contains a known Windows decoding roundtrip")
	require(d["machine"]["id"] == MACHINE_ID and d["machine"]["year"] == 1994, "wrong physical edition")
	require(d["machine"]["ipdb_id"] == 21 and d["machine"]["model_number"] == "50038", "wrong Gold identity")
	require(d["coverage"]["status"] == "author_ready" and not d["coverage"]["missing"], "incomplete Gold contribution")
	require(d["knowledge"]["status"] == "complete", "incomplete recreation knowledge")
	require(all(v in {"validated", "not_applicable"} for v in d["coverage"]["dimensions"].values()), "unvalidated coverage dimension")
	require(len(d["drivers"]) == 9 and {v["id"] for v in d["drivers"]} == DRIVERS, "Gold must own exactly nine drivers")
	require(all(v["physical_compatibility"] in {"identical", "compatible"} for v in d["drivers"]), "unresolved driver compatibility")
	sources = {v["id"]: v for v in d["sources"]}
	for identifier, digest in {
		"manual.gold.operations": "f87a3bb06da72277bc610b262ca05e2e3fa0fa04550abe3707729984c42d9dd4",
		"vpx.gold.sliderpoint-1-4-1": "3e317807114197c7a8079ec1ed5d7faa639592da59755a38a8cb007d13f2cb83",
		"vpx-script.gold.sliderpoint-1-4-1": "2c33d2b7bb40fab1f41747170e55a2f2638928f6b33179955f4d0bc6eeca254c",
	}.items():
		require(sources.get(identifier, {}).get("sha256") == digest, f"wrong exact-edition source: {identifier}")
	require(d["controller"]["platform"] == "pinmame.wpc-fliptronic" and d["controller"]["hardware_generation"] == "0x8", "wrong emulator topology")
	require((len(d["inputs"]), len(d["outputs"]), len(d["displays"]), len(d["mechanisms"])) == (88, 119, 1, 15), "incomplete or duplicated Gold inventory")
	s = bindings(d, "inputs", "pinmame.input.switch")
	coils = bindings(d, "outputs", "pinmame.output.solenoid")
	lamps = bindings(d, "outputs", "pinmame.output.lamp")
	gi = bindings(d, "outputs", "pinmame.output.gi")
	require(set(s) == set(range(1, 9)) | MATRIX | set(range(111, 119)), "incomplete switch namespaces")
	require(set(bindings(d, "inputs", "pinmame.input.dip")) == set(range(1, 9)), "incomplete DIP bank")
	require(set(coils) == set(range(1, 51)) and set(lamps) == MATRIX and set(gi) == set(range(5)), "incomplete output namespaces")
	require({a for a in MATRIX if s[a]["availability"] == "unused"} == UNUSED_SWITCHES, "incorrect Gold switch fitment")
	require(s[11]["availability"] == "used" and s[11]["physical"]["part_number"] == "20-9663-9", "buyin lost or wrongly wired")
	for a in MATRIX - UNUSED_SWITCHES - {24}:
		require(s[a]["normally_closed"] == (a in OPTOS), f"wrong matrix polarity {a}")
	for a in (112, 114, 116, 118):
		require(s[a]["physical"]["switch_type"] == "opto" and s[a]["normally_closed"] is False, f"wrong optical button construction {a}")
	for a in (81, 82):
		require(s[a]["physical"]["switch_type"] == "microswitch", "bookcase limits are real mechanical switches")
	require(s[57]["physical"]["assembly_part_number"] == "A-16908/A-16909", "1992 bumper opto copied into Gold")
	require(coils[26]["physical"]["part_number"] == "AE-27-1200", "1992 eject coil copied into Gold")
	require(coils[2]["physical"]["location"] == "cabinet", "magnet bracket confused with cabinet knocker")
	require(coils[49]["kind"] == "virtual" and coils[49]["availability"] == "used", "live simulator shooter state marked dead")
	require(lamps[41]["kind"] == "lamp" and lamps[41]["availability"] == "unused", "ROM buyin state confused with factory lamp fitment")
	require(lamps[41]["spatial"].get("reason") == "unused", "factory-unwired buyin lamp given a physical socket")
	require({a for a, v in lamps.items() if v["availability"] == "unused"} == {41, 76}, "wrong Gold unused lamp set")
	for a in (41, 76):
		require(lamps[a]["kind"] == "lamp" and "quantity" not in lamps[a]["physical"] and lamps[a]["spatial"].get("reason") == "unused", f"unfitted lamp {a} claims a physical bulb")
	require(s[21]["physical"]["quantity"] == 2, "factory amendment's second slam contact lost")
	for a in range(81, 88):
		require(lamps[a]["spatial"].get("reason") == "cabinet_or_service", "speaker-panel bulbs cannot be clamped onto playfield")
	for a in (13, 26):
		require(lamps[a]["physical"]["quantity"] == 2, "two-bulb PCB circuit reduced to one render object")
	for a in range(17, 23):
		require(coils[a]["physical"]["quantity"] == {17: 2, 18: 2, 19: 3, 20: 2, 21: 2, 22: 4}[a], f"wrong physical flasher circuit quantity {a}")
	require(not unresolved_conflicts(d), "unresolved physical conflict")
	for device in d["inputs"] + d["outputs"] + d["displays"]:
		require(device["provenance"]["status"] == "validated", "unvalidated device assertion")
		require(device.get("availability") != "unknown", "unknown physical availability")
		require(device.get("spatial", {}).get("status") in {"validated", "not_applicable"}, "observed or missing placement prevents promotion")
		for placement in device["spatial"].get("placements", []):
			require(placement["provenance"]["status"] == "validated", "unvalidated placement")
	for a in (13, 26):
		require(len(lamps[a]["spatial"].get("placements", [])) == 2, "both physical PCB sockets require evidence")
		require(len({(p["x"], p["y"]) for p in lamps[a]["spatial"]["placements"]}) == 2, "paired PCB sockets collapsed to one location")
	require(len(gi[0]["spatial"].get("placements", [])) == 15, "left GI socket census incomplete")
	require(len(gi[4]["spatial"].get("placements", [])) == 8, "right GI socket census incomplete")
	for a in (0, 4):
		require(len({(p["x"], p["y"]) for p in gi[a]["spatial"]["placements"]}) == len(gi[a]["spatial"]["placements"]), "duplicate GI socket")
	require(all(gi[a]["physical"].get("quantity", 0) >= len(gi[a]["spatial"]["placements"]) for a in (0, 4)), "GI quantity excludes fitted playfield sockets")


def build(root: Path = ROOT) -> dict[str, Any]:
	path = root / SEED_PATH
	require(path.is_file() and file_sha256(path) == SEED_SHA256, "reviewed seed bytes drifted")
	d = load_json(path)
	assert_reviewed_contract(d)
	reconcile_spatial(d, evidence_seed(root))
	errors = validate_machine(d, root)
	require(not errors, "\n".join(errors))
	return copy.deepcopy(d)


def evidence_seed(root: Path = ROOT) -> dict[str, Any]:
	path = root / EVIDENCE_PATH
	require(path.is_file() and file_sha256(path) == EVIDENCE_SHA256, "reviewed geometry/evidence seed drifted")
	return load_json(path)


def phone_projection_metrics(source: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
	"""Bound a disclosed stock-family template about its own mount, not a camera fit."""
	require(source.get("object") == "Primitive72" and source.get("bounds") == PHONE_MOUNT_BOUNDS, "phone projection lost its own socket mount")
	require(source.get("projection_class") == PHONE_PROJECTION_CLASS and source.get("projection") is True, "unreviewed phone projection")
	require(source.get("anchor_kind") == "own_socket_mount" and source.get("observed_glass_centre") is False, "mount misrepresented as observed glass")
	template = source["socket_template"]
	require(template["assembly_part_number"] == "A-12887" and template["dimensioned_replacement"] == "CEC4087-3", "unreconciled socket family")
	require(template["original_manufacturing_dimensions_claimed"] is False, "replacement dimensions misattributed to Williams")
	require(template["pose_scope"] == ["stock_above_plate", "stock_below_plate"], "phone mount configurations lost")
	model = evidence["spatial_candidates"]["gi.string-1"][-1]
	require(model["object"] == "gRGP2_plasticOff" and model["component"] == 30, "wrong same-part glass template")
	require(template["model_glass_bounds"] == model["bounds"] and template["table_bounds"] == model["table_bounds"], "same-part scale drifted")
	dims = template["socket_inches"]
	require(dims == {"overall": 1.15, "width": 0.53, "depth": 0.31, "offset": 0.23, "tolerance": 0.05}, "manufacturer socket dimensions drifted")
	require(template["bulb_mm"] == {"diameter": 10.3, "mol": 26.8}, "manufacturer bulb dimensions drifted")
	tol, diameter, mol = dims["tolerance"], template["bulb_mm"]["diameter"], template["bulb_mm"]["mol"]
	# Entire bulb length beyond the socket top deliberately overbounds insertion.
	extents = [(dims["width"] + tol) * 25.4 / 2 + diameter / 2,
		((dims["depth"] + tol) + (dims["offset"] + tol)) * 25.4 + diameter / 2,
		(dims["overall"] + tol) * 25.4 + mol]
	radius_mm = math.sqrt(sum(v * v for v in extents))
	model_diameter = model["bounds"][1][2] - model["bounds"][0][2]
	calibration = template["scale_calibration"]
	require(calibration["selection"] == "max_mesh_and_stock_ball", "phone scale must retain both calibrations")
	require(calibration["ball_diameter_inches"] == 1.0625 and calibration["vpx_ball_diameter"] == 50, "stock-ball scale operands drifted")
	require(calibration["physical_source_ref"] == "parts.gold.ipdb" and calibration["physical_locator"] == "item2578; part20-6500; ball-steel1-1/16", "stock ball lost its actual parts-list role")
	require(calibration["script_source_ref"] == "vpx-script.geometry.shared.vpw-2-4-41" and calibration["script_locator"] == "script.vbs:164; Const BallSize = 50", "ball convention lost its actual table-script role")
	require(calibration["exact_global_cad_scale_claimed"] is False, "approximate ball cross-check mislabeled exact CAD scale")
	require({calibration["physical_source_ref"], calibration["script_source_ref"]} <= set(source["source_refs"]), "phone scale source roles omitted")
	ball_mm = calibration["ball_diameter_inches"] * 25.4
	mesh_scale, ball_scale = model_diameter / diameter, calibration["vpx_ball_diameter"] / ball_mm
	selected_scale = max(mesh_scale, ball_scale)
	shared = template["table_bounds"]
	require(template["mount_xy"] == [895.0218, 231.1319], "wrong corresponding shared socket mount")
	gold = source["table_bounds"]
	require(gold == [0, 0, 985, 2220], "wrong exact-Gold frame")
	anchor = [(a + b) / 2 for a, b in zip(*PHONE_MOUNT_BOUNDS)]
	gold_xy = [(anchor[i] - gold[i]) / (gold[i + 2] - gold[i]) for i in (0, 1)]
	shared_xy = [(template["mount_xy"][i] - shared[i]) / (shared[i + 2] - shared[i]) for i in (0, 1)]
	anchor_difference = math.dist(gold_xy, shared_xy)
	uncertainty = radius_mm * selected_scale / min(shared[2] - shared[0], shared[3] - shared[1]) + anchor_difference
	result = math.ceil(uncertainty * 1000) / 1000
	require(source.get("normalized_uncertainty") == result, "phone envelope uncertainty does not reproduce")
	return {"extents_mm": extents, "radius_mm": radius_mm, "ball_mm": ball_mm,
		"mesh_vpu_per_mm": mesh_scale, "ball_vpu_per_mm": ball_scale, "selected_vpu_per_mm": selected_scale,
		"radius_vpu": radius_mm * selected_scale, "mount_disagreement": anchor_difference,
		"raw_normalized_uncertainty": uncertainty, "normalized_uncertainty": result}


def phone_projection_uncertainty(source: dict[str, Any], evidence: dict[str, Any]) -> float:
	return phone_projection_metrics(source, evidence)["normalized_uncertainty"]


def source_xy(source: dict[str, Any], evidence: dict[str, Any]) -> tuple[float, float]:
	"""Recompute one physical anchor, without reading its canonical placement."""
	bounds = source.get("table_bounds", [0, 0, 985, 2220])
	require(len(bounds) == 4 and bounds[2] > bounds[0] and bounds[3] > bounds[1], "invalid retained table bounds")
	left, rear, right, apron = bounds
	if source.get("projection_class") == "photographed-bulb-to-adjacent-fixed-edge":
		raise ValueError("Gold: withdrawn phone endpoint projection")
	if source.get("projection_class") == PHONE_PROJECTION_CLASS or source.get("object") == "Primitive72":
		phone_projection_uncertainty(source, evidence)
	if "bounds" in source:
		bounds = source["bounds"]
		low, high = (bounds["lo"], bounds["hi"]) if isinstance(bounds, dict) else bounds
		x, y = ((low[i] + high[i]) / 2 for i in (0, 1))
		if isinstance(bounds, dict):
			require(all(abs(bounds["center"][i] - (low[i] + high[i]) / 2) < 1e-9 for i in range(3)), "mesh centre disagrees with world bounds")
	elif "pixel" in source:
		controls = evidence["coordinate_fits"][source["fit_key"]]["controls"]
		transform = fit([(c["pixel"], c["xy"]) for c in controls])
		return apply(transform, source["pixel"])
	elif "raw_x" in source:
		require(source["object"] == "Diverter" and source["raw_x"] == -2.5, "unreviewed edge clamp")
		x, y = 0, source["raw_y"]
	else:
		require("object" in source and "x" in source and "y" in source, "anchor lacks reproducible raw coordinates")
		x, y = source["x"], source["y"]
	return (x - left) / (right - left), (y - rear) / (apron - rear)


def inside_hull(pixel: list[float], controls: list[dict[str, Any]]) -> bool:
	"""Convex hull in drawing pixels, so extrapolation is not a bounding-box test."""
	def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
		return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
	points = sorted({tuple(v["pixel"]) for v in controls})
	chains = []
	for sequence in (points, list(reversed(points))):
		chain = []
		for point in sequence:
			while len(chain) > 1 and cross(chain[-2], chain[-1], point) <= 0:
				chain.pop()
			chain.append(point)
		chains.append(chain[:-1])
	hull = chains[0] + chains[1]
	return len(hull) >= 3 and all(cross(a, b, tuple(pixel)) >= -1e-9 for a, b in zip(hull, hull[1:] + hull[:1]))


def reconcile_spatial(d: dict[str, Any], evidence: dict[str, Any]) -> None:
	require(not evidence["remaining_research"], "unresolved physical research prevents promotion")
	for key, page in evidence["coordinate_fits"].items():
		controls = page["controls"]
		require(len(controls) >= 4 and max(c["xy"][1] for c in controls) - min(c["xy"][1] for c in controls) >= 0.5, f"insufficient independent drawing controls: {key}")
	for v in d["inputs"] + d["outputs"]:
		placements = v["spatial"].get("placements", [])
		if not placements:
			continue
		sources = evidence["spatial_candidates"].get(v["id"], [])
		require(len(sources) == len(placements), f"missing individual physical anchors: {v['id']}")
		for placement, source in zip(placements, sources):
			if placement["id"].startswith("gi.string-5.phone-555"):
				require(placement["id"] == "gi.string-5.phone-555-mount-projection" and source.get("projection_class") == PHONE_PROJECTION_CLASS, "withdrawn phone coordinate or projection class")
				require(set(source["source_refs"]) <= set(placement["provenance"]["source_refs"]), "phone projection lost its dimensional/source roles")
			x, y = source_xy(source, evidence)
			require((placement["x"], placement["y"]) == (round(x, 6), round(y, 6)), f"coordinate does not reproduce: {placement['id']}")
			if v["kind"] in {"lamp", "flasher", "gi"}:
				require(source.get("physical_emitter") is True, f"render helper is not an emitter: {placement['id']}")
			if "pixel" in source:
				controls = evidence["coordinate_fits"][source["fit_key"]]["controls"]
				inside = inside_hull(source["pixel"], controls)
				require(source.get("inside_control_hull") == inside, f"false control-hull classification: {placement['id']}")
				if not inside:
					second = source.get("secondary_check", {})
					require(second.get("agrees") is True and second.get("fit_key") != source["fit_key"], f"unreconciled extrapolation: {placement['id']}")
					controls2 = evidence["coordinate_fits"][second["fit_key"]]["controls"]
					xy2 = apply(fit([(c["pixel"], c["xy"]) for c in controls2]), second["pixel"])
					require(distance((x, y), xy2) <= 0.07, f"secondary drawing disagrees: {placement['id']}")


def verify_external(root: Path = ROOT) -> None:
	"""Unset optional roots skip external checks; a supplied root must be exact."""
	d = build(root)
	evidence = evidence_seed(root)
	labels = {"pinmame-vpx-sources": "PINMAME_VPX_SOURCES_ROOT", "pinmame-manuals": "PINMAME_MANUALS_ROOT", "pinmame-review-artifacts": "PINMAME_REVIEW_ARTIFACTS_ROOT"}
	for source in d["sources"]:
		uri = source["uri"]
		if not uri.startswith("external:"):
			continue
		label, relative = uri.removeprefix("external:").split("/", 1)
		value = os.environ.get(labels[label])
		if value is None:
			continue
		base = Path(value).expanduser().resolve()
		require(base.is_dir(), f"missing configured evidence root: {base}")
		path = base / relative
		require(path.is_file() and file_sha256(path) == source["sha256"], f"external source mismatch: {path}")
	for label, items in evidence["retained_artifacts"].items():
		value = os.environ.get(labels[label])
		if value is None:
			continue
		base = Path(value).expanduser().resolve()
		for item in items:
			path = base / item["path"]
			require(path.is_file() and path.stat().st_size == item["size"] and file_sha256(path) == item["sha256"], f"retained artifact mismatch: {path}")
	for item in evidence["full_manifests"]:
		value = os.environ.get(labels[item["root"]])
		if value is None:
			continue
		directory = Path(value).expanduser().resolve() / item["path"]
		if item.get("format") == "pinmame-vpx-extraction-manifest":
			# The already-reviewed shared extraction has its original sidecar
			# format. Verify it without writing into that evidence directory.
			manifest = {"format": item["format"], "version": 1, "files": [
				{"path": path.relative_to(directory).as_posix(), "size": path.stat().st_size, "sha256": file_sha256(path)}
				for path in sorted((p for p in directory.rglob("*") if p.is_file()), key=lambda p: p.relative_to(directory).as_posix())
			]}
			serialization = item.get("serialization", "repository-canonical-json")
			require(serialization in {"repository-canonical-json", "compact-json-no-lf"}, "unknown extraction manifest serialization")
			payload = manifest_bytes(manifest) if serialization == "compact-json-no-lf" else canonical_bytes(manifest)
			require(hashlib.sha256(payload).hexdigest() == item["sha256"], f"shared extraction inventory drift: {directory}")
			require(len(manifest["files"]) == item["file_count"] and sum(v["size"] for v in manifest["files"]) == item["total_bytes"], f"shared extraction counts drift: {directory}")
			manifest_path = Path(value).expanduser().resolve() / item["manifest_path"]
			require(manifest_path.is_file() and manifest_path.read_bytes() == payload, f"shared extraction sidecar drift: {manifest_path}")
			continue
		manifest = build_manifest(directory, item["game"])
		payload = manifest_bytes(manifest) + b"\n"
		require(hashlib.sha256(payload).hexdigest() == item["sha256"], f"complete evidence manifest drift: {directory}")
		require(len(manifest["files"]) == item["file_count"] and sum(v["size"] for v in manifest["files"]) == item["total_bytes"], f"evidence inventory drift: {directory}")
		manifest_path = Path(value).expanduser().resolve() / item["manifest_path"] if "manifest_path" in item else directory / "manifest.json"
		digest_path = manifest_path.with_suffix(".sha256") if "manifest_path" in item else directory / "manifest.sha256"
		require(manifest_path.read_bytes() == payload and digest_path.read_text(encoding="ascii") == item["sha256"] + "\n", f"retained manifest bytes drift: {directory}")
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if value:
		base = Path(value).expanduser().resolve()
		extracted = base / EXTRACTION_RELATIVE_PATH
		actual = manifest_bytes(build_manifest(extracted, "tafg_lx3")) + b"\n"
		require(hashlib.sha256(actual).hexdigest() == evidence["extraction"]["manifest_sha256"], "retained extraction files drifted")
		require((extracted / "manifest.json").read_bytes() == actual, "retained extraction manifest is stale")
		require((extracted / "manifest.sha256").read_text(encoding="ascii") == evidence["extraction"]["manifest_sha256"] + "\n", "retained extraction digest is stale")
		for item in evidence["libraries"]:
			path = base / item["path"]
			require(path.is_file() and file_sha256(path) == item["sha256"], f"runtime library mismatch: {path}")
		checkout = base.parent / "source-checkouts/pinmame-46e1a01a"
		for item in evidence["pinmame_sources"]:
			path = checkout / item["path"]
			require(path.is_file() and file_sha256(path) == item["sha256"], f"pinned source mismatch: {path}")


def spatial_report(d: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
	unresolved = []
	for device in d["inputs"] + d["outputs"]:
		spatial = device.get("spatial", {})
		if spatial.get("status") not in {"validated", "not_applicable"}:
			unresolved.append({"device": device["id"], "binding": device["binding"], "status": spatial.get("status", "missing")})
	return {
		"format": "pinmame-spatial-blockers" if unresolved else "pinmame-spatial-audit",
		"version": 1, "machine_id": MACHINE_ID, "status": d["coverage"]["status"],
		"coordinate_convention": "x=0 left,x=1 right;y=0 rear,y=1 apron; exact Gold bounds0,0,985,2220; round only final normalized values to6 decimals",
		"extraction": evidence["extraction"], "source_hashes": {s["id"]:s.get("sha256") for s in d["sources"]},
		"objects": evidence["spatial_candidates"], "unresolved": unresolved,
		"blockers": evidence["remaining_research"],
		"coordinate_fits": evidence["coordinate_fits"],
		"candidate_callout_reconciliation": evidence["candidate_callout_reconciliation"],
		"physical_census": evidence["physical_census"],
		"source_roles": evidence["source_roles"],
		"phone_repair_research": evidence["phone_repair_research"],
		"retained_artifacts": evidence["retained_artifacts"],
		"excluded": ["GI_Light* large surface lighting helpers", "LLightning1,SwampLight,VaultLight optional light mods", "FesterBulb and FesterLight* added figure/proxy", "L81–L87 desktop speaker-panel helpers", "secondary b/c brightness layers except21c–25c physical bumper bulb meshes"],
		"promotion_decision": "Complete fitted-device inventory and individually sourced placements; all measured/projection classes are disclosed and the completeness validator passes. Factory fitment and runtime bindings retain separate authorities.",
	}


def knowledge(d: dict[str, Any]) -> str:
	"""Render durable recreation facts; source roles and uncertainties stay explicit."""
	ready = d["coverage"]["status"] == "author_ready"
	coverage = "author_ready (100%)" if ready else "partial"
	lines = [
		"# The Addams Family Gold (Bally, 1994)", "", f"Coverage: **{coverage}**.", "",
		"The Special Collectors Edition is model 50038, IPDB 21, OPDB G4ODR-MLzY7. This record owns exactly nine tafg_* drivers. It describes the factory 1994 Gold machine. The original 1992 edition, later original-production gold art and the gold-plated production-record commemorative cabinet have separate identities. Williams' archived [Ask Uncle Willy #16](https://www.planetarypinball.com/mm5/Williams/archives/willy16.htm) explicitly distinguishes the commemorative cabinet from Gold production.", "",
		"## Evidence roles", "",
		"The Gold Operations Manual 16-50038-101 controls physical construction. Its complete switch, lamp, coil, GI and flipper table regions are transcribed under evidence/excerpts/bally.the-addams-family-gold.1994, with source-literal blank cells and printing errors preserved. Factory amendment 16-9805 (March 22, 1994) corrects the gold bumper caps and identifies two slam contacts: 27-1066 on the coin door and SW-1A-117 inside the cabinet. The source files remain external; hashes, locators, attribution and reviewed excerpts travel with the definition.", "",
		"Pinned PinMAME revision 46e1a01a controls the nine-driver inventory, public address arithmetic, normalization, simulator channels and 128×32 DMD callback. The retained Sliderpoint Gold 1.4.1 VPX controls its own runtime bindings and geometry. It targets tafg_lx3, uses UseSolenoids=1 and HandleMechanics=0, and implements the hand/bookcase with host cvpmMech objects. Full extraction manifests pin every file. Shared-layout geometry has an explicitly narrower role: a modeled physical bulb can locate a Gold-manual-fitted emitter after reconciliation with the exact Gold table and physical photographs. It supplies neither Gold identity nor Gold runtime behavior.", "",
		"The IPDB-hosted hierarchical 50038 parts list is undated and its original compiler is not credited. Its assembly quantities and wire pairs are cross-checks against the manual and photographs. It lists A-20207.1 inside A-17316, while the contemporary manual specifies A-16384; the definition follows the contemporary manual for original button construction. The listing is not silently treated as a dated factory change notice.", "",
		"## Gold construction and controller", "",
		"Gold adds buyin switch 11 (20-9663-9), optical cabinet button boards A-17316/A-16384, high-power interlock A-17077, revised flipper assemblies and bumper-lane opto A-16908/A-16909. The interlock breaks the +50V/+20V transformer secondary independently of matrix 22 memory protect. Gold retains the J801–J806 flipper controller and separate power-driver bridge: Fliptronics I architecture. The later A-12697-3 power-driver board omits the former relay. Generic Pinside/IPDB platform labels do not override the actual Gold schematic and board photographs.", "",
		"The public contract is GEN_WPCFLIPTRON (0x8): eight dedicated switches, the complete 8×8 switch matrix, flipper inputs 111–118, eight DIP bits, solenoids 1–50, the complete 8×8 lamp matrix and GI indices 0–4. These are address counts, including virtual and unfitted positions. Matrix switches 12,23,28,46,52,83,88 are unused; 24 is the always-closed reference. The 0x7c/0x18 masks cover matrix optos 53–57 and 84–85. Cabinet optical channels 112/114/116/118 use the separate complemented Fliptronic convention and are normally open under the platform contract. Physical EOS leaves 111/113/115/117 are open at rest per Gold 2-15.", "",
		"Solenoids 29–31 publish WPC GPIO/GameOn register state; 32 and 37–44 have no Gold load. Simulator channel 49 publishes manual-shooter release state when the built-in simulator is used; 50 is reserved/zero. Channel 49 is not an auto-plunger. All eight real flipper power/hold winding addresses remain distinct. The printed 'Flasher' drive-bank classification for 25–28 does not make the hand/bookcase motors or eject coils into flash lamps.", "",
		"Buyin button 11 is fitted and wired. Lamp 41 is a different question: the manual prints Not Used, original Gold owners report an unwired factory button lamp, and retained diagnostic photographs identify the live ROM state as BUY IN / LAMP41 / RED-BRN / YEL-BLK. This physical lamp-matrix address is unused because it has no factory wired load; its meaningful ROM state is the buyin lamp state, not evidence of factory fitment. Later owner-added lamp wiring and diode are a retrofit. See the retained [Pinside discussion](https://pinside.com/pinball/forum/topic/addams-family-gold-extra-ball-lamp), including the original-owner account and successful retrofit report.", "",
		"Lamp 76 is also printed Not Used in the Gold lamp matrix (3-2). It has no fitted factory bulb quantity. Both unused addresses 41 and 76 retain their CPU bindings and documented row/column wiring, with spatial reason unused.", "",
		"Lamp 76 is unused. Lamps 81–87 are the seven speaker-panel THING bulbs and 88 is the credit/start-button lamp; they have cabinet spatial records. Jackpot 13 and Cousin It 26 each drive two physical bulbs on their respective four-socket PCBs. Flashers 17/18/20/21 each drive two bulbs. Circuit 19 drives three: one lower-ramp dome plus two jet-bumper sockets. Circuit 22 drives one playfield bulb and three atop the backbox. Gold eject coil 26 is AE-27-1200. The GI summary's connector readings are preserved literally; structured routing follows the actual 3-20 interboard destinations.", "",
		"## Spatial evidence", "",
		"Coordinates use x=0 left, x=1 right, y=0 rear and y=1 apron. Gold bounds are 0,0,985,2220. Each physical emitter gets its own placement. Raw object coordinates, world-space mesh bounds, factory pixel reads, per-page affine controls, normalization and exclusions are pinned in the geometry seed and generated spatial report. Manual pixels are independently read from retained native-resolution crops. A second drawing checks measurements outside the main control hull. The 0.07 normalized callout limit is a curator convention, not a physical manufacturing tolerance. Six decimal places preserve deterministic normalization and do not claim micrometer measurement accuracy.", "",
		"Hidden coils, EOS leaves and feedback sensors use explicitly disclosed projections to their own physical mechanism when internal geometry is unavailable. Actual bulb meshes and factory socket measurements replace insert overlays, bloom and reflection sprites. The two PCB lamp pairs are separate drawn sockets, not offsets invented around one light. Raised red/green bulb primitives are selected by their physical color and binding rather than their misleading L74/L75 names. The hand magnet uses its actual moving body in the retained reference pose; it is not projected onto a fixed saucer magnet.", "",
		"The playfield GI census is 21 #44 bulbs plus two #555 bulbs: 14+1 on the left and 7+1 on the right. One lower-left #555 uses its glass mesh. The phone #555 has no own glass mesh and uses an explicit projection to its identified socket mount, Gold Primitive72 at normalized (0.936675,0.105180), with 0.125 normalized radial uncertainty. This is a stock socket-family envelope, not an observed glass centre at the rivet. A new direct incandescent-body photograph identifies its own foot below the blue plate; an earlier LED repair photograph has an above-plate pose. Neither is claimed untouched factory. The factory A-12887 profile, replacement-family engineering dimensions/tolerances and the maximum of same-part modeled bulb and retained stock-ball physics scales bound the disclosed rigid-pose template without selecting either height. CEC replacement dimensions are not relabelled original Williams manufacturing dimensions, and arbitrary leg deformation is outside this approximation. The phone-GI and socket-dimension excerpts retain the arithmetic, source roles and limits. The old left-edge/0.025 proposal is withdrawn; no camera fit, hotspot, helper or ambiguous washer supplies the new coordinate. The optional Cousin Itt figure's extra lamp is excluded. Orange backbox GI has 15 #555; yellow has eight #555 plus seven self-blink #455. Two coin-door lamps are cabinet loads on the right string.", "",
		"The newly user-supplied 2.4.41 table was also inspected from its actual native meshes and world export. Its script header identifies 2.4.41 while embedded info.json is stale at 2.3.1. No usable own telephone #555 glass/socket was found: the changed PhoneMod_9 is an optional animated telephone toy, including a hidden native mesh inspected separately, and changed RGP8_B_GI2off contains art/plastic surfaces. The separate #906, plates and hardware are not substitute #555 coordinates. Full source/extraction/export manifests and the 2031-component inspection remain pinned; this ancestral geometry is not independent Gold fitment or runtime authority.", "",
		"Trough switches 15 and 16 use separate script-bound functional contact projections from the supplementary RealishTrough model; switch 17 uses the exact Gold BallRelease contact. Their physical B-8925/A-11680 construction and arrangement are independently established by the Gold manual and physical photographs. These are disclosed contact projections, not three copies of a trough centroid or coordinates taken from leaderless labels.", "",
		"## Mechanisms and ball paths", "",
	]
	for mechanism in d["mechanisms"]:
		lines.extend(["### " + mechanism["label"], "", mechanism["behavior"], ""])
	lines.extend([
		"## Gameplay and firmware variants", "",
		"[Keefer's Gold Guide](https://gamefaqs.gamespot.com/pinball/915935-addams-family-special-collectors-edition/faqs/1447), V1.1.1, June 10, 1995, is retained in full with both preformatted blocks and its attribution/distribution notices. It describes Cousin It's belongings, the 3M extra room, 6M dialogue, Super Seance 10/15/20M awards, varying Jackpot, Dirty Pool Super Jackpot, adjustable endgame lock purge and buyin preserving progress. These are attributed gameplay observations. The guide distinguishes L-1/L-2 Jackpot behavior from L-3 behavior and does not establish physical random probabilities or mechanism travel times. Contributors are Jon Biavati, Mark Phaedrus, Mark Valentine and David Stewart.", "",
		"The nine driver notes distinguish production revisions, LED ghost fixes, H-3 source uncertainty and the RedBall ball-saver patch at A.2 setting 36. All run on the documented Gold hardware; software release years do not create another physical machine. [Action Pinball's conversion instructions](https://www.actionpinball.com/tech/tafgconv.php) explain U6/U15/U18 changes that run Gold rules on original hardware, while explicitly noting the absent buyin button. That compatibility does not make a converted original cabinet factory Gold.", "",
		"## Retained-table defects and exclusions", "",
		"The exact Gold script reverses sling switch 36/37; this definition follows both Gold physical charts (left 36/coil14, right 37/coil15) and documents the table defect. Its splash string says 1992 and its embedded info says 1.4 despite the supplied 1.4.1 filename. Neither changes physical identity. Desktop THING helpers supply no playfield sockets. GI_Light* surface glows, duplicate brightness layers and the explicitly optional Chair/Swamp/Vault/Fester lighting are excluded from the factory inventory. Runtime traces or rendered pools cannot determine physical bulb quantity.", "",
	])
	text = "\n".join(lines)
	return text


def artifacts(root: Path = ROOT) -> dict[Path, bytes]:
	d = build(root)
	evidence = evidence_seed(root)
	report = spatial_report(d, evidence)
	lines = ["# Gold spatial evidence audit", "", f"Status: {d['coverage']['status']}.", "", report["coordinate_convention"], "",
		"The JSON companion retains every raw anchor, physical census, source role, native drawing crop/fit, projection and external artifact digest. Actual socket geometry replaces render layers; each emitter is a separate placement. Cabinet/service, virtual, unused and DIP records deliberately have no playfield position.", "",
		"| Device / placement | x | y | Coordinate source or projection |", "| --- | ---: | ---: | --- |"]
	for v in d["inputs"] + d["outputs"]:
		for p, source in zip(v["spatial"].get("placements", []), evidence["spatial_candidates"].get(v["id"], [])):
			origin = source.get("object", source.get("page", "physical measurement"))
			lines.append(f"| {p['id']} | {p['x']:.6f} | {p['y']:.6f} | {origin}: {source['method']} |")
	lines.extend(["", "## Exclusions", ""] + ["- " + v for v in report["excluded"]])
	lines.extend(["", "## Decision", "", report["promotion_decision"], ""])
	text = "\n".join(lines)
	return {DEFINITION_PATH:canonical_bytes(d), KNOWLEDGE_PATH:knowledge(d).encode("utf-8"), REPORT_PATH:canonical_bytes(report), REPORT_MD_PATH:text.encode("utf-8")}


def check(root: Path = ROOT) -> None:
	require(not (root / PARTIAL_PATH).exists(), "stale partial duplicates the promoted Gold record")
	for relative, payload in artifacts(root).items():
		require((root / relative).is_file() and (root / relative).read_bytes() == payload, f"generated artifact drift: {relative}")
	verify_external(root)


def generate(root: Path = ROOT) -> None:
	payloads = artifacts(root)
	path = root / DEFINITION_PATH
	if path.exists():
		require(path.read_bytes() == payloads[DEFINITION_PATH], "refusing to overwrite a changed author-ready definition")
	partial = root / PARTIAL_PATH
	if partial.exists():
		require(file_sha256(partial) == PARTIAL_SHA256, "refusing to prune a changed partial")
	verify_external(root)
	for relative, payload in payloads.items():
		write_bytes(root / relative, payload)
	if partial.exists():
		partial.unlink()


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	check() if args.check else generate()
	print("Gold curator: " + ("checked" if args.check else "regenerated"))


if __name__=="__main__":
	main()
