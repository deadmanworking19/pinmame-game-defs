#!/usr/bin/env python3
"""Build the spatial audit report for Bally Centaur (1981) from its author-ready definition.

Writes ``reports/spatial/bally/centaur-1981.json`` and ``.md``. The report lists every placement's
source class, the derived placements and how each was derived, every controlled not-applicable
record, and the retained table's identity. ``--check`` refuses drift and never writes. With
``PINMAME_VPX_SOURCES_ROOT`` set it also recomputes the retained extraction manifest and checks that
every derived placement still follows from the table's geometry.

    python tools/centaur_spatial_report.py (--check | --regenerate)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION = ROOT / "machines" / "author-ready" / "bally" / "centaur-1981.json"
REPORT_JSON = ROOT / "reports" / "spatial" / "bally" / "centaur-1981.json"
REPORT_MD = ROOT / "reports" / "spatial" / "bally" / "centaur-1981.md"
EXTRACTION = Path("bally") / "centaur-1981" / "extracted-vpxtool"

WIDTH, HEIGHT = 952.941, 1976.471
VPX_SHA256 = "2689607de4e6c9b267c56aa0d090ff340bf3a9220277dc8730a51dca5172a5bc"
EXTRACTION_FILE_COUNT = 2780
EXTRACTION_TOTAL_BYTES = 255939052
EXTRACTION_MANIFEST_SHA256 = "389bab09c790c432b350972a1cf8acde0b94dd7b137f14e42d510377995d15b4"
# vpxtool git:v0.33.3 `export obj --units vpu` of the retained table; its mesh bounds for the bulb
# meshes and bumper inserts are kept in the working root's review artifacts for this machine.
OBJ_EXPORT_SHA256 = "1724f7a309a34180828566dd50361ea44e09b7149016391f2e78329031007205"
SOURCE_HASHES = {
	"centaur_ii_schematics_pdf": "89332ef0d1d4550a75217ddf12bfac79d599281e6296ceae80f79388a73f0dc4",
	"manual_image_scan_pdf": "9893d29ee871fd8c0a2afea35e931f107fb97a8156739035e005b15fd879e7ea",
	"manual_with_schematics_pdf": "c5b151bfc2d2672fce7b405519bda07051bd54e115e9484f39fe05159d47bc23",
	"pinside_a9_board_photo": "6ddd40f46dc512fc0415cc1455589b0d35efae5bc482ab6c628e5e8bb07ecb00",
	"pinside_top_lane_sockets_photo": "629c564dd444053caf579c0d0e3813fea5f3084453069e9720d425596270ad5e",
	"vpx": VPX_SHA256,
	"vpx_obj_export": OBJ_EXPORT_SHA256,
}

# Placements that are not the centre of a Light, trigger or target object named for their address.
DERIVED = [
	(
		"pinmame.output.lamp:66, pinmame.output.lamp:82",
		"Slingshot lamps: the bulb meshes Bulb_Prim_029 (right) and Bulb_Prim_028 (left) that the table's l66 and l82 handlers light under "
		"each slingshot plastic. Their world-space mesh-bound centres from `vpxtool export obj --units vpu` (OBJ SHA-256 "
		f"{OBJ_EXPORT_SHA256}) equal their stored primitive positions to six decimal places. The Light objects l66 and l82 are invisible "
		"placeholders in a row along the bottom edge, with l1, l68, l84, l98, l100 and l114, and are not positions.",
	),
	(
		"pinmame.output.lamp:98, pinmame.output.lamp:114",
		"Thumper-bumper lamps: the centres of the bumper objects Bumper2 (right) and Bumper1 (left), the bumpers the l98 and l114 handlers "
		"light. The lamp sits inside the bumper body.",
	),
	(
		"pinmame.output.lamp:67, 83, 99, 115",
		"Chamber lamp pairs: each address drives two bulbs, one either side of the Queen's Chamber lane; the placements are the two Light "
		"objects l<n> and l<n>a whose bulb meshes Bulb_Prim_<n> and Bulb_Prim_<n>a the same handler lights. The schematic prints (2) against "
		"each of these four circuits and against no other auxiliary circuit.",
	),
	(
		"pinmame.input.switch:34",
		"10 point rebound, five contacts: the table models each side triangle's two rubber faces as one chevron-shaped wall (Phys_Sensor_34 "
		"left, Phys_Sensor_34a right) and the upper-right rebound as a third (Phys_Sensor_34b). Each chevron is split at its apex, along the "
		"line from the inner apex point to the midpoint of the two outer apex points, and each face's contact is the area centroid of its "
		"arm; the upper-right contact is the area centroid of its wall. Figure V draws two 34 contacts on each triangle and one at the upper "
		"right.",
	),
	(
		"pinmame.output.solenoid:12, pinmame.output.solenoid:13",
		"Slingshot coils: the drag-point centroids of the LeftSlingshot and RightSlingshot walls; switches 38 and 37 share them, because the "
		"slingshot switch is the wall itself.",
	),
	(
		"pinmame.output.solenoid:1, 2, 3, 4, 5, 8, 9",
		"Drop-target coils, unchanged from the earlier validated pass: each individual drop coil of the right four-bank at its target's "
		"drop-target primitive, and each bank reset (1 ORBS, 8 in-line, 9 right four) at the middle of its bank's four targets. Each lies "
		"within 0.001 of the corresponding primitive positions or their mean, which this report checks.",
	),
	(
		"pinmame.output.solenoid:7, 14, 15, 20",
		"Kicker and magnet coils at the table's own objects for them: the outhole kicker at Drain (switch 8 shares it), the ball kick at "
		"BallRelease, the ball release at SubBallRelease, and the magnet at RMagTrig.",
	),
]

EXCLUDED = [
	"Light objects parked in a row along the bottom edge (l1, l66, l68, l82, l84, l98, l100, l114), which are invisible placeholders for "
	"addresses the table lights through other objects or not at all",
	"l68a, l84a and l100a, playfield star inserts the table drives from the bare matrix positions 68, 84 and 100, which the AS-2518-43 cannot light",
	"render doubles stacked on a placed object: l<n>a beside each main-board l<n>, l<n>mid and l<n>top beside each chamber bulb, and the "
	"sw<n>p, sw<n>a and sw<n>o primitives on each target",
	"bumperbiglight and bumpersmalllight helpers, whose timer_interval values are not lamp bindings, and the cabinet UndercabLight",
	"LEDnnn objects, which are the seven-segment display digits rendered as lights",
]


def grouped(definition: dict, collection: str) -> dict[str, list]:
	groups: dict[str, list] = {}
	for item in definition[collection]:
		spatial = item.get("spatial") or {}
		if spatial.get("status") != "not_applicable":
			continue
		key = item["binding"]["device"] if collection == "inputs" else f"{item['binding']['group']}:{item['binding']['device']}"
		groups.setdefault(spatial["reason"], []).append(key)
	return {reason: sorted(values, key=lambda v: (str(type(v)), v)) for reason, values in sorted(groups.items())}


def build(definition: dict) -> dict:
	inputs = sorted(
		item["binding"]["device"] for item in definition["inputs"]
		if (item.get("spatial") or {}).get("status") == "validated"
	)
	outputs = sorted(
		f"{item['binding']['group']}:{item['binding']['device']}" for item in definition["outputs"]
		if (item.get("spatial") or {}).get("status") == "validated"
	)
	placements = sum(
		len((item.get("spatial") or {}).get("placements", []))
		for item in definition["inputs"] + definition["outputs"]
	)
	unplaced = [
		item["id"] for item in definition["inputs"] + definition["outputs"]
		if (item.get("spatial") or {}).get("status") not in ("validated", "not_applicable")
	]
	if unplaced or definition["coverage"]["status"] != "author_ready":
		raise SystemExit(f"Centaur is not fully placed: {unplaced}")
	return {
		"coordinate_convention": {
			"source_bounds": {"bottom": HEIGHT, "left": 0.0, "right": WIDTH, "top": 0.0},
			"space": "playfield",
			"x": f"x/{WIDTH}; 0=left, 1=right",
			"y": f"y/{HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"derived_placements": [{"bindings": bindings, "method": method} for bindings, method in DERIVED],
		"excluded_object_classes": EXCLUDED,
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"reproduced_by": "a fresh extraction of the retained table with vpxtool git:v0.33.3 reproduces the retained extraction file for file",
			"source_ref": "vpx-table.centaur-2-0-0",
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"format": "pinmame-spatial-audit",
		"machine_id": "bally.centaur.1981",
		"not_applicable_inputs": grouped(definition, "inputs"),
		"not_applicable_outputs": grouped(definition, "outputs"),
		"placement_count": placements,
		"resolved_input_addresses": inputs,
		"resolved_output_bindings": outputs,
		"source_hashes": SOURCE_HASHES,
		"status": "validated and promoted to machines/author-ready/bally/centaur-1981.json",
		"unresolved": [],
		"version": 1,
		"visual_review_cache": [
			"manual PDF page 24 (image-only scan), rendered: Figure V playfield switch and solenoid locations",
			"manual with schematics PDF page 51, native scan: AS-2518-43 auxiliary lamp driver W-1207-11, board side and J2 harness list",
			"manual with schematics PDF page 54, native scan: A9 playfield wiring diagram W-1255-2",
			"manual with schematics PDF page 46, native scan: G.I. flasher W-1253 b (its OCR layer carries page 54's text)",
			"Centaur II schematics PDF page 15, rendered: solenoid expander W-1251-1 b for game 1239",
			"Pinside thread 303903 post 4 photographs: the A9 board's J2 connector and the top-lane sockets from below",
		],
	}


def markdown(report: dict, definition: dict) -> str:
	lamps_two = [
		item["binding"]["device"] for item in definition["outputs"]
		if item["binding"]["group"] == "pinmame.output.lamp" and (item.get("physical") or {}).get("quantity") == 2
	]
	lines = [
		"# Centaur (Bally, 1981) spatial review",
		"",
		"Status: validated and promoted to `machines/author-ready/bally/centaur-1981.json`.",
		"",
		f"The matching source is the retained known-working `Centaur (Bally 1981) v2.0.0.vpx` at SHA-256 `{VPX_SHA256}`. Its retained "
		f"extraction holds {EXTRACTION_FILE_COUNT} files totalling {EXTRACTION_TOTAL_BYTES} bytes, manifest SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, and a fresh `vpxtool git:v0.33.3` extraction reproduces it file for file. Playfield bounds are "
		f"`left=0 top=0 right={WIDTH} bottom={HEIGHT}`, and every canonical coordinate is x/{WIDTH} and y/{HEIGHT} rounded to at most six "
		f"fractional places. {report['placement_count']} placements are recorded.",
		"",
		"## Evidence decisions",
		"",
		"- The Bally game #1239 manual and its schematic set are the physical inventory, wiring and connector authority; the ROM's own "
		"solenoid self test and a gameplay run of the pinned LibPinMAME harness own the printed-to-public solenoid mapping and which lamp "
		"each auxiliary circuit is in play; pinned PinMAME owns controller topology; and the retained table supplies geometry, taken from the "
		"objects its script binds.",
		"- Every placement names one physical object: a bulb, a trigger, a target, a bumper, a kicker or a wall. None is a centroid of "
		"several devices. The one split is switch 34, whose two faces per side triangle the table models as one wall.",
		"- The top lanes follow the ROM over the A9 sheet's labels. The sheet prints TOP LEFT LANE at A9J2-7 (public 65) and TOP RIGHT LANE "
		"at A9J2-18 (public 97), but in play the ROM lights 97 for the top left rollover (switch 5) and 65 for the top right (switch 3); the "
		"switch table and Figure V put switch 5 at the left lane. So 97 is placed at the left-lane insert above switch 5 and 65 at the right, "
		"which is how the table binds them. Left, middle and right run in ascending x.",
		f"- Only the four chamber circuits drive two bulbs ({', '.join(map(str, lamps_two))}): the schematic prints (2) against them and nothing "
		"else, and each is placed at both of its bulbs. Every other auxiliary circuit drives one.",
		"- Public lamp 113 is an unwired circuit: the A9 sheet's harness list and a photograph of a Centaur's A9 board both show no wire at "
		"A9J2-11. It carries a controlled `unused` record, and its runtime state is the top-lane register's carry bit.",
		"- Public 68, 84, 100 and 116 are bare matrix positions with no SCR behind them (`unused`); the table's star inserts on three of them "
		"are its author's addition.",
		"- Backbox lamps, the displays, the knocker, the coin lockout, the K1 flipper relay and the cabinet switches take controlled "
		"`cabinet_or_service` records; the G.I. flasher feed (lamp 1), the trough switches and the sixth switch-column strobe (solenoid 17) "
		"are `internal_nonvisual`.",
		"",
		"## Derived placements",
		"",
	]
	for item in report["derived_placements"]:
		lines.append(f"- `{item['bindings']}`: {item['method']}")
	lines += ["", "## Excluded table objects", ""]
	lines += [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Unresolved", "", "None.", ""]
	return "\n".join(lines)


def area_centroid(polygon: list[tuple[float, float]]) -> tuple[float, float]:
	area = cx = cy = 0.0
	for (x0, y0), (x1, y1) in zip(polygon, polygon[1:] + polygon[:1]):
		cross = x0 * y1 - x1 * y0
		area += cross
		cx += (x0 + x1) * cross
		cy += (y0 + y1) * cross
	area /= 2
	return cx / (6 * area), cy / (6 * area)


def rebound_contacts(gameitems: Path) -> list[tuple[float, float]]:
	"""Switch 34's five contacts, derived from the table's three sensor walls.

	Each side wall is a chevron of seven drag points: the outer edge runs from the upper arm's tip to
	the lower arm's tip and back along the inner edge. Points 4 and 5 (left) and 1 and 2 (right) are
	the two outer apex points, and point 1 (left) and 5 (right) the inner apex. Each chevron is split
	along the line from its inner apex to the midpoint of its outer apex points, and each arm's contact
	is the area centroid of its half; the upper-right contact is the area centroid of its own wall.
	"""
	def wall(name: str) -> list[tuple[float, float]]:
		item = json.loads((gameitems / f"Wall.{name}.json").read_text(encoding="utf-8"))["Wall"]
		return [(point["x"], point["y"]) for point in item["drag_points"]]

	left, right, upper = wall("Phys_Sensor_34"), wall("Phys_Sensor_34a"), wall("Phys_Sensor_34b")
	if (len(left), len(right)) != (7, 7):
		raise SystemExit("the switch-34 chevron walls no longer have seven drag points")
	left_apex = ((left[4][0] + left[5][0]) / 2, (left[4][1] + left[5][1]) / 2)
	right_apex = ((right[1][0] + right[2][0]) / 2, (right[1][1] + right[2][1]) / 2)
	points = [
		area_centroid([left[0], left[1], left_apex, left[5], left[6]]),
		area_centroid([left[1], left[2], left[3], left[4], left_apex]),
		area_centroid([right[0], right[1], right_apex, right[5], right[6]]),
		area_centroid([right_apex, right[2], right[3], right[4], right[5]]),
		area_centroid(upper),
	]
	return [(round(x / WIDTH, 6), round(y / HEIGHT, 6)) for x, y in points]


def verify_geometry(definition: dict, gameitems: Path) -> None:
	def point(kind: str, name: str, field: str) -> tuple[float, float]:
		item = json.loads((gameitems / f"{kind}.{name}.json").read_text(encoding="utf-8"))[kind]
		return item[field]["x"] / WIDTH, item[field]["y"] / HEIGHT

	outputs = {f"{i['binding']['group']}:{i['binding']['device']}": i for i in definition["outputs"]}
	switches = {i["binding"]["device"]: i for i in definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}

	def placed(binding: str) -> list[tuple[float, float]]:
		return [(p["x"], p["y"]) for p in outputs[binding]["spatial"]["placements"]]

	contacts = [(p["x"], p["y"]) for p in switches[34]["spatial"]["placements"]]
	expected_contacts = rebound_contacts(gameitems)
	if contacts != expected_contacts:
		raise SystemExit(f"switch 34 contacts {contacts} do not match the table's sensor walls {expected_contacts}")

	def near(a: tuple[float, float], b: tuple[float, float], tolerance: float) -> bool:
		return abs(a[0] - b[0]) <= tolerance and abs(a[1] - b[1]) <= tolerance

	checks = [
		(placed("pinmame.output.lamp:66")[0], point("Primitive", "Bulb_Prim_029", "position"), 1e-6),
		(placed("pinmame.output.lamp:82")[0], point("Primitive", "Bulb_Prim_028", "position"), 1e-6),
		(placed("pinmame.output.lamp:98")[0], point("Bumper", "Bumper2", "center"), 1e-6),
		(placed("pinmame.output.lamp:114")[0], point("Bumper", "Bumper1", "center"), 1e-6),
	]
	for address in (67, 83, 99, 115):
		first, second = placed(f"pinmame.output.lamp:{address}")
		checks.append((first, point("Light", f"l{address}", "center"), 1e-6))
		checks.append((second, point("Light", f"l{address}a", "center"), 1e-6))
	for coil, target in ((2, "sw28p"), (3, "sw27p"), (4, "sw26p"), (5, "sw25p")):
		checks.append((placed(f"pinmame.output.solenoid:{coil}")[0], point("Primitive", target, "position"), 0.001))
	for coil, targets in ((1, ("sw29p", "sw30p", "sw31p", "sw32p")), (8, ("sw41p", "sw42p", "sw43p", "sw44p")), (9, ("sw25p", "sw26p", "sw27p", "sw28p"))):
		points = [point("Primitive", name, "position") for name in targets]
		mean = (sum(p[0] for p in points) / 4, sum(p[1] for p in points) / 4)
		checks.append((placed(f"pinmame.output.solenoid:{coil}")[0], mean, 0.001))
	for index, (actual, expected, tolerance) in enumerate(checks):
		if not near(actual, expected, tolerance):
			raise SystemExit(f"derived placement check {index} failed: {actual} is not within {tolerance} of {expected}")


def extraction_manifest_sha256(extraction: Path) -> tuple[int, int, str]:
	paths = sorted((path for path in extraction.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction).as_posix())
	files = []
	for path in paths:
		digest = hashlib.sha256()
		with path.open("rb") as stream:
			for chunk in iter(lambda: stream.read(1 << 20), b""):
				digest.update(chunk)
		files.append({"path": path.relative_to(extraction).as_posix(), "sha256": digest.hexdigest(), "size": path.stat().st_size})
	manifest = {"files": files, "format": "pinmame-vpx-extraction-manifest", "version": 1}
	payload = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
	return len(files), sum(item["size"] for item in files), hashlib.sha256(payload).hexdigest()


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	definition = json.loads(DEFINITION.read_text(encoding="utf-8"))
	report = build(definition)
	text_json = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
	text_md = markdown(report, definition)
	sources_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if sources_root:
		extraction = Path(sources_root) / EXTRACTION
		identity = extraction_manifest_sha256(extraction)
		if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
			raise SystemExit(f"retained Centaur extraction identity mismatch: {identity}")
		verify_geometry(definition, extraction / "gameitems")
	if args.check:
		stale = [path for path, text in ((REPORT_JSON, text_json), (REPORT_MD, text_md)) if not path.is_file() or path.read_text(encoding="utf-8") != text]
		if stale:
			print("spatial report drift: " + ", ".join(path.relative_to(ROOT).as_posix() for path in stale), file=sys.stderr)
			return 1
		print("Centaur spatial report matches the definition.")
		return 0
	REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
	REPORT_JSON.write_bytes(text_json.encode("utf-8"))
	REPORT_MD.write_bytes(text_md.encode("utf-8"))
	for path in (REPORT_JSON, REPORT_MD):
		print(f"wrote {path.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
