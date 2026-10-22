"""Apply the reviewed table geometry and the factory-drawing callout check to the semantic Terminator 2 definition."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_game_defs.registry import rebuild_catalog

import curate_terminator_2 as semantic
import drawing_callouts


ROOT = semantic.ROOT
DEFINITION_PATH = ROOT / "machines/author-ready/williams/terminator-2-judgment-day-1991.json"
FORMER_DEFINITION_PATH = ROOT / "machines/partial/williams/terminator-2-judgment-day-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/terminator-2-judgment-day-1991.md"
AUDIT_PATH = ROOT / "reports/spatial/williams/terminator-2-judgment-day-1991.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/williams/terminator-2-judgment-day-1991-callouts.json"
CALLOUT_SEED_RELATIVE = "tools/seeds/williams/terminator-2-judgment-day-1991-callouts.json"
X_MAX = 964.0
Y_MAX = 2162.0
NFOZZY_X_MAX = 952.94116
NFOZZY_Y_MAX = 2164.706


def point(x: float, y: float) -> tuple[float, float]:
	return round(x / X_MAX, 6), round(y / Y_MAX, 6)


def placement(device: dict[str, Any], object_name: str, xy: tuple[float, float], role: str, sources: tuple[str, ...], status: str) -> dict[str, Any]:
	return {"id": f"{device['id']}.{role}.{semantic.slug(object_name)}", "role": role, "space": "playfield", "x": xy[0], "y": xy[1], "provenance": semantic.provenance(*sources, status=status)}


def located(device: dict[str, Any], objects: list[tuple[str, tuple[float, float]]], role: str, status: str = "validated", sources: tuple[str, ...] = (semantic.VPX_TABLE_SOURCE,)) -> None:
	device["spatial"] = {"status": status, "placements": [placement(device, name, xy, role, sources, status) for name, xy in objects]}


def not_applicable(device: dict[str, Any], reason: str, *sources: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": semantic.provenance(*sources)}


def add_note(device: dict[str, Any], text: str) -> None:
	physical = device.setdefault("physical", {})
	physical["notes"] = f"{physical['notes']} {text}" if physical.get("notes") else text


BUMPER1 = point(464.7151, 398.11743)
BUMPER2 = point(539.35254, 587.8717)
BUMPER3 = point(690.91473, 451.42084)
DROP_TARGET = point(290.89508, 298.64487)
T2_GUN = point(865.51874, 1029.3837)

# Switch placements: exact named table objects bound by the retained script, except the projections listed in
# INPUT_PROJECTIONS. Switch 62 is measured on the 2-37 drawing (see the callout seed's measurements).
INPUT_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	15: [("Drain-to-BallRelease trough projection 1", point(592.37544, 1994.622))], 16: [("Drain-to-BallRelease trough projection 2", point(671.94506, 1960.7174))],
	17: [("Drain-to-BallRelease trough projection 3", point(751.51468, 1926.8128))], 18: [("Drain", point(433.2362, 2062.4312))],
	25: [("Trigger.sw25", point(50.719437, 1729.4485))],
	26: [("Trigger.sw26", point(118.22889, 1613.9412))], 27: [("Trigger.sw27", point(748.96356, 1613.7274))], 28: [("Trigger.sw28", point(815.3944, 1665.8789))],
	31: [("Kicker.sw31", point(865.5187, 919.1969))], 32: [("Primitive.T2_Gun assembly", T2_GUN)], 33: [("Primitive.T2_Gun assembly", T2_GUN)],
	36: [("HitTarget.sw36", point(425.02313, 660.554))], 37: [("HitTarget.sw37", point(467.14813, 700.679))], 38: [("HitTarget.sw38", point(511.39816, 738.179))],
	41: [("Bumper.Bumper1", BUMPER1)], 42: [("Bumper.Bumper3", BUMPER3)], 43: [("Bumper.Bumper2", BUMPER2)],
	44: [("Wall.LeftSlingshot drag-point centroid", point(198.959384, 1596.17412))], 45: [("Wall.RightSlingshot drag-point centroid", point(666.839608, 1590.44232))],
	46: [("HitTarget.sw46", point(763.21747, 1245.4951))], 47: [("HitTarget.sw47", point(763.09247, 1296.8701))], 48: [("HitTarget.sw48", point(763.09247, 1347.8701))],
	51: [("Kicker.sw51", point(52.74919, 961.93243))], 53: [("Trigger.sw53", point(55.627926, 315.2049))], 54: [("Trigger.sw54", point(70.66557, 150.56776))], 55: [("Kicker.sw55", point(741.06757, 70.96199))],
	56: [("Trigger.sw56", point(468.81967, 203.57411))], 57: [("Trigger.sw57", point(568.8115, 225.40366))], 58: [("Trigger.sw58", point(671.2108, 246.00197))],
	61: [("Gate.sw61", point(197.30371, 513.38696))], 63: [("Gate.sw63", point(756.97565, 627.8825))],
	65: [("Trigger.sw65", point(880.5173, 279.71756))], 66: [("Trigger.sw66", point(799.59924, 195.73581))],
	71: [("HitTarget.sw71", point(173.69376, 694.7722))], 72: [("HitTarget.sw72", point(183.5637, 747.14056))], 73: [("HitTarget.sw73", point(192.89772, 799.7795))], 74: [("HitTarget.sw74", point(202.12245, 852.956))], 75: [("HitTarget.sw75", point(211.54387, 907.3085))],
	76: [("Kicker.sw76", point(276.99594, 211.89403))], 77: [("HitTarget.sw77", DROP_TARGET)], 78: [("Kicker.sw78", point(904.33246, 1945.6531))],
}
INPUT_PROJECTIONS = {15, 16, 17, 32, 33, 44, 45}

# Coil placements: the object each solenoid callback moves. Coils 5, 6, 11 and 12 are assembly projections.
EFFECT_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	1: [("Kicker.sw76", point(276.99594, 211.89403))], 2: [("Kicker.sw31", point(865.5187, 919.1969))], 3: [("Drain", point(433.2362, 2062.4312))], 4: [("Kicker.BallRelease", point(831.0843, 1892.9082))],
	5: [("Wall.RightSlingshot drag-point centroid", point(666.839608, 1590.44232))], 6: [("Wall.LeftSlingshot drag-point centroid", point(198.959384, 1596.17412))],
	8: [("Plunger.Plunger1", point(50.694122, 1926.4977))], 9: [("Kicker.sw78", point(904.33246, 1945.6531))], 10: [("Kicker.sw55", point(741.06757, 70.96199))],
	11: [("Primitive.T2_Gun", T2_GUN)], 12: [("HitTarget.sw77 drop-target assembly", DROP_TARGET)], 13: [("Bumper.Bumper1", BUMPER1)], 14: [("Bumper.Bumper3", BUMPER3)],
	15: [("Bumper.Bumper2", BUMPER2)], 16: [("Kicker.sw51", point(52.74919, 961.93243))], 28: [("HitTarget.sw77", DROP_TARGET)],
}
EFFECT_PROJECTIONS = {5, 6, 11, 12}

LAMP_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	11: [("L11", point(287.39496, 1643.4208))], 12: [("L12", point(358.5831, 1606.2587))], 13: [("L13", point(430.1694, 1588.9508))], 14: [("L14", point(505.71988, 1606.4674))], 15: [("L15", point(570.69257, 1644.9978))], 16: [("L16", point(429.96292, 1918.5978))], 17: [("L17", point(436.8856, 1484.8107))],
	21: [("L21", point(50.183113, 1647.6917))], 22: [("L22a", point(50.288, 1536.8124)), ("L22b", point(816.0358, 1537.0868))], 23: [("L23", point(118.31302, 1467.4066))], 24: [("L24", point(749.2248, 1467.3746))], 25: [("L25", point(374.6901, 809.52014))], 26: [("L26", point(355.82285, 705.24164))], 27: [("L27", point(339.6643, 601.6882))], 28: [("L28", point(322.85495, 496.36966))],
	31: [("L31", point(254.28519, 734.0496))], 32: [("L32", point(263.2487, 783.1297))], 33: [("L33", point(277.42532, 831.569))], 34: [("L34", point(290.36966, 875.9949))], 35: [("L35", point(303.47177, 923.73987))], 36: [("L36", point(426.90973, 776.25714))], 37: [("L37", point(469.18896, 811.4169))], 38: [("L38", point(510.19342, 852.4468))],
	41: [("L41", point(150.76582, 939.15454))], 42: [("L42", point(177.86926, 1050.7529))], 43: [("L43", point(216.63107, 1137.259))], 44: [("L44", point(238.982, 1210.2062))], 45: [("L45", point(257.1247, 1280.9836))], 46: [("L46", point(280.75662, 1355.6615))], 47: [("L47", point(296.22644, 1435.5078))], 48: [("L48", point(315.97357, 1512.3365))],
	51: [("L51a", point(400.10486, 1401.8247)), ("L51b", point(467.63043, 1401.209))], 52: [("Primitive.L52 skull mesh world-bounds centre", point(290.655179, 308.123654))],
	53: [("L53", point(679.52106, 1136.9258))], 54: [("L54", point(652.94305, 1210.1489))], 55: [("L55", point(625.4195, 1282.5437))], 56: [("L56", point(598.9009, 1359.3146))], 57: [("L57", point(569.5661, 1434.337))], 58: [("L58", point(541.4647, 1508.2344))],
	61: [("L61", point(315.07635, 1016.63745))], 62: [("L62", point(330.0013, 1081.9806))], 63: [("L63", point(344.0438, 1146.8193))], 64: [("L64", point(358.65793, 1210.6841))], 65: [("L65", point(374.3634, 1274.9163))], 66: [("L66", point(112.11431, 1207.7814))], 67: [("L67", point(162.73505, 1318.2964))], 68: [("L68", point(226.74431, 642.4249))],
	71: [("L71", point(614.18414, 1018.8931))], 72: [("L72", point(592.16174, 1083.2053))], 73: [("L73", point(569.44775, 1146.943))], 74: [("L74", point(547.6057, 1211.571))], 75: [("L75", point(525.92194, 1276.051))], 76: [("L76", point(742.40247, 1241.3405))], 77: [("L77", point(741.8852, 1292.462))], 78: [("L78", point(743.76636, 1346.3873))],
	81: [("L81", point(750.78827, 956.7337))], 82: [("L82", point(637.8953, 940.2964))], 83: [("L83", point(719.845, 1051.8195))], 85: [("L85", point(305.93045, 398.8359))], 86: [("L86", point(469.6026, 108.398186))], 87: [("L87", point(569.9467, 130.69623))], 88: [("L88", point(673.7177, 152.81792))],
}
# The script fades Primitive.L52's skull images for lamp 52; its mesh is stored at the origin with RotX 90 and sizes 19.8/19.5/19.5,
# so world x = 19.8 * obj x and world y = 19.5 * obj z, whose bounds centre is checked against the retained OBJ export.
SKULL_MESH = {"object": "Primitive.L52", "size": (19.8, 19.5, 19.5), "rot_x": 90.0, "centre": (290.655179, 308.123654)}

# Flashers on script-driven Lights; 20 and 25 are measured on the 2-39 drawing (callout seed measurements).
FLASHER_POSITIONS: dict[int, list[tuple[str, tuple[float, float]]]] = {
	17: [("F117", point(392.1405, 1747.9479)), ("F1172", point(469.02628, 1748.8044))], 18: [("F118", point(729.04016, 1755.8896))], 19: [("F119", point(142.0577, 1754.0991))], 21: [("F121", point(865.69476, 936.60376)), ("F121b", point(870.1298, 1124.9872))], 22: [("F122", point(765.19946, 634.2644))], 23: [("F123", point(121.169914, 280.81564))], 26: [("F126", point(216.68967, 326.0185)), ("F126a", point(169.21431, 199.84035))], 27: [("F127", point(370.31763, 306.4764)), ("F127a", point(381.96442, 250.69917))],
}

# Playfield G.I. sockets of public 2 and 4: each is a light the retained VPW UpdateGI handler drives (raw VPW coordinates) that
# lies within 0.01 normalized of a bulb the nFozzy 1.12a table models for the same public string (raw nFozzy coordinates,
# normalized by its own bounds): a connected piece of its per-string bulb mesh or a jet-cap bulb primitive. Its lights and
# sprites are render effects, not bulbs, and never make a socket. Public 3 is the four lights of the VPW UpdateGI Case 3.
GI_SOCKETS: dict[int, tuple[tuple[str, float, float, tuple[str, ...]], ...]] = {
	2: (
		("GI_17", 417.48743, 192.5585, ("GI_bulbR piece",)), ("GI_18", 527.64984, 213.36194, ("GI_bulbR piece",)),
		("GI_19", 626.28754, 237.39903, ("GI_bulbR piece",)), ("GI_001", 724.08636, 261.08545, ("GI_bulbR piece",)),
		("GI_21", 380.64868, 348.83136, ("GI_bulbR piece",)), ("B1", 462.8119, 395.5301, ("GIjet_BulbP1",)),
		("GI_22", 380.77527, 434.00882, ("GI_bulbR piece",)), ("B5", 690.51373, 449.71698, ("GIjet_BulbP2",)),
		("B3", 539.27167, 588.8766, ("GIjet_BulbP3",)), ("GI_15", 467.59897, 634.80756, ("GI_bulbR piece",)),
		("GI_34", 721.5083, 654.1311, ("GI_bulbR piece",)), ("GI_33", 761.3623, 675.28876, ("GI_bulbR piece",)),
		("GI_16", 532.62964, 681.36774, ("GI_bulbR piece",)), ("GI_30", 912.45087, 802.47614, ("GI_bulbR piece",)),
		("GI_31", 909.7719, 893.68713, ("GI_bulbR piece",)), ("GI_32", 909.37305, 1171.214, ("GI_bulbR piece",)),
		("GI_10", 826.9222, 1388.5323, ("GI_bulbR piece",)),
		("GI_6", 703.8457, 1538.6958, ("GI_bulbR piece",)), ("GI_5", 665.32666, 1670.2496, ("GI_bulbR piece",)),
		("GI_2", 658.5137, 1799.7385, ("GI_bulbR piece",)),
	),
	3: (
		("Light3", 467.96497, 901.41626, ("VPW UpdateGI Case 3",)), ("Light2", 466.31747, 949.0672, ("VPW UpdateGI Case 3",)),
		("Light4", 466.2919, 993.3501, ("VPW UpdateGI Case 3",)), ("Light5", 462.55188, 1041.23, ("VPW UpdateGI Case 3",)),
	),
	4: (
		("GI_24", 161.63599, 332.33954, ("GI_bulbL piece",)), ("GI_25", 122.198, 344.06424, ("GI_bulbL piece",)),
		("GI_23", 255.7749, 464.9249, ("GI_bulbL piece",)), ("GI_7", 44.246094, 1361.1478, ("GI_bulbL piece",)),
		("GI_4", 161.66125, 1536.2029, ("GI_bulbL piece",)), ("GI_3", 199.2124, 1672.1221, ("GI_bulbL piece",)),
		("GI_1", 201.67297, 1801.213, ("GI_bulbL piece",)),
	),
}
GI_DRIVEN_CASE_2 = ("B1", "B2", "B3", "B4", "B5", "B6", *(f"GI_{index}" for index in range(1, 21)), "GI_001", "GI_002", *(f"GI_{index}" for index in range(21, 36)))
GI_DRIVEN_CASE_3 = ("Light2", "Light3", "Light4", "Light5")
GI_NOT_PLACED = {
	"B2": "render double of B5 under the same right jet cap", "B4": "render double of B1 under the same upper-left jet cap", "B6": "render double of B3 under the same lower jet cap",
	"GI_002": "render double of GI_17 at the left top-lane guide", "GI_20": "render double of GI_001 at the right top-lane guide",
	"GI_8": "left lane, no nFozzy socket", "GI_9": "left lane, no nFozzy socket", "GI_12": "left lane, no nFozzy socket",
	"GI_13": "left lane, no nFozzy socket; within 0.03 of the lower socket the 2-39 drawing gives flasher 25",
	"GI_14": "left lane, no nFozzy socket; within 0.03 of the upper socket the 2-39 drawing gives flasher 25",
	"GI_26": "top-right corner, no nFozzy socket", "GI_27": "top-right corner, no nFozzy socket", "GI_28": "top-right corner, no nFozzy socket",
	"GI_11": "right side, just above GI_10; nFozzy has only a GIRT_5 render light here and no bulb within 0.01 (the nearest, GI_10's bulb-mesh piece, is 0.033 away)",
	"GI_29": "right side, no nFozzy socket", "GI_35": "upper left on the skull-eye height surface, no nFozzy socket",
}
NFOZZY_BULB_MESHES = {2: "GI_bulbR", 4: "GI_bulbL"}
NFOZZY_JET_BULBS = ("GIjet_BulbP1", "GIjet_BulbP2", "GIjet_BulbP3")
GI_MATCH_LIMIT = 0.01


def _item(root: Path, kind: str, name: str) -> dict[str, Any]:
	return json.loads((root / "gameitems" / f"{kind}.{name}.json").read_text(encoding="utf-8"))[kind]


def _mesh_pieces(path: Path, scale: float) -> list[tuple[float, float]]:
	"""Bulb pieces of a baked-mesh primitive at the origin with RotX 180: connected islands above the socket plane."""
	verts: list[tuple[float, float, float]] = []
	faces: list[list[int]] = []
	for line in path.read_text(encoding="utf-8").splitlines():
		if line.startswith("v "):
			x, y, z = (float(value) for value in line.split()[1:4])
			verts.append((x, y, z))
		elif line.startswith("f "):
			faces.append([int(token.split("/")[0]) - 1 for token in line.split()[1:]])
	parent = list(range(len(verts)))

	def find(index: int) -> int:
		while parent[index] != index:
			parent[index] = parent[parent[index]]
			index = parent[index]
		return index

	for face in faces:
		for other in face[1:]:
			a, b = find(face[0]), find(other)
			if a != b:
				parent[a] = b
	groups: dict[int, list[tuple[float, float, float]]] = {}
	for index, vertex in enumerate(verts):
		groups.setdefault(find(index), []).append(vertex)
	pieces = []
	for members in groups.values():
		xs, ys, zs = zip(*members)
		if (min(zs) + max(zs)) / 2 < 0:
			continue
		pieces.append(((min(xs) + max(xs)) / 2 * scale, -(min(ys) + max(ys)) / 2 * scale))
	return sorted(pieces)


def derive_gi_sockets(source_root: Path) -> dict[int, list[tuple[str, float, float, tuple[str, ...]]]]:
	"""Recompute GI_SOCKETS from the two retained extractions; only nFozzy bulbs (mesh pieces and jet-cap primitives) count."""
	vpw = source_root / semantic.EXTRACTION_RELATIVE_PATH
	nf = source_root / semantic.NFOZZY_EXTRACTION_RELATIVE_PATH
	lights = {name: (_item(vpw, "Light", name)["center"]["x"], _item(vpw, "Light", name)["center"]["y"]) for name in (*GI_DRIVEN_CASE_2, *GI_DRIVEN_CASE_3)}
	sockets: list[tuple[int, str, float, float]] = []
	for address, mesh in NFOZZY_BULB_MESHES.items():
		primitive = _item(nf, "Primitive", mesh)
		if primitive["rot_and_tra"][0] != 180.0 or any(abs(value) > 1e-9 for value in primitive["position"].values()):
			raise RuntimeError(f"nFozzy {mesh} is no longer an origin primitive with RotX 180")
		for x, y in _mesh_pieces(nf / "gameitems" / f"Primitive.{mesh}.obj", primitive["size"]["x"]):
			sockets.append((address, f"{mesh} piece", x, y))
	for name in NFOZZY_JET_BULBS:
		position = _item(nf, "Primitive", name)["position"]
		sockets.append((2, name, position["x"], position["y"]))
	result: dict[int, dict[str, tuple[float, float, list[str]]]] = {2: {}, 3: {name: (*lights[name], ["VPW UpdateGI Case 3"]) for name in GI_DRIVEN_CASE_3}, 4: {}}
	owner: dict[str, int] = {}
	for address, label, x, y in sockets:
		target = (x / NFOZZY_X_MAX, y / NFOZZY_Y_MAX)
		best = min(GI_DRIVEN_CASE_2, key=lambda name: math.dist(target, (lights[name][0] / X_MAX, lights[name][1] / Y_MAX)))
		if math.dist(target, (lights[best][0] / X_MAX, lights[best][1] / Y_MAX)) > GI_MATCH_LIMIT:
			continue
		if owner.setdefault(best, address) != address:
			raise RuntimeError(f"VPW light {best} matches sockets of two strings")
		entry = result[address].setdefault(best, (lights[best][0], lights[best][1], []))
		if label not in entry[2]:
			entry[2].append(label)
	return {
		address: sorted(((name, x, y, tuple(sorted(evidence))) for name, (x, y, evidence) in entries.items()), key=lambda item: (item[2], item[1]))
		for address, entries in result.items()
	}


def verify_gi_sockets(source_root: Path) -> None:
	derived = derive_gi_sockets(source_root)
	expected = {address: sorted(((name, x, y, tuple(sorted(evidence))) for name, x, y, evidence in sockets), key=lambda item: (item[2], item[1])) for address, sockets in GI_SOCKETS.items()}
	if derived != expected:
		raise RuntimeError("T2 G.I. sockets no longer derive from the two retained extractions")
	placed = {name for sockets in GI_SOCKETS.values() for name, *_ in sockets}
	if placed | set(GI_NOT_PLACED) != set(GI_DRIVEN_CASE_2) | set(GI_DRIVEN_CASE_3) or placed & set(GI_NOT_PLACED):
		raise RuntimeError("every G.I. light the VPW script drives must be placed or listed as not placed, once")


def verify_skull_mesh(source_root: Path) -> None:
	extraction = source_root / semantic.EXTRACTION_RELATIVE_PATH
	primitive = _item(extraction, "Primitive", "L52")
	size = (primitive["size"]["x"], primitive["size"]["y"], primitive["size"]["z"])
	if any(abs(value) > 1e-9 for value in primitive["position"].values()) or primitive["rot_and_tra"][0] != SKULL_MESH["rot_x"] or size != SKULL_MESH["size"]:
		raise RuntimeError("Primitive.L52 transform changed")
	verts = [tuple(float(value) for value in line.split()[1:4]) for line in (extraction / "gameitems/Primitive.L52.obj").read_text(encoding="utf-8").splitlines() if line.startswith("v ")]
	xs, _, zs = zip(*verts)
	centre = ((min(xs) + max(xs)) / 2 * size[0], (min(zs) + max(zs)) / 2 * size[2])
	if math.dist(centre, SKULL_MESH["centre"]) > 1e-5:
		raise RuntimeError(f"Primitive.L52 world-bounds centre is {centre}, not {SKULL_MESH['centre']}")


def verify_retained_geometry(source_root: Path) -> None:
	semantic.verify_extraction_manifest(source_root)
	semantic.verify_nfozzy_manifest(source_root)
	verify_gi_sockets(source_root)
	verify_skull_mesh(source_root)


def _by_binding(definition: dict[str, Any], collection: str, group: str) -> dict[int, dict[str, Any]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _measured(device: dict[str, Any], seed: dict[str, Any], role: str) -> None:
	"""Place a device from its drawing measurements in the callout seed."""
	entries = sorted(key for key, item in seed["measurements"].items() if item["device"] == device["id"])
	if not entries:
		raise RuntimeError(f"no drawing measurement for {device['id']}")
	placements = []
	for key in entries:
		x, y = drawing_callouts.measured(seed, key)
		if not key.startswith(f"{device['id']}.{role}."):
			raise RuntimeError(f"measurement {key} does not belong to {device['id']}")
		placements.append({"id": key, "role": role, "space": "playfield", "x": x, "y": y, "provenance": semantic.provenance(semantic.MANUAL_SOURCE, semantic.CALLOUT_SOURCE)})
	device["spatial"] = {"status": "validated", "placements": placements}


def apply_spatial(definition: dict[str, Any], seed: dict[str, Any]) -> None:
	switches = _by_binding(definition, "inputs", "pinmame.input.switch")
	table_object = (semantic.VPX_TABLE_SOURCE,)
	projection = (semantic.MANUAL_SOURCE, semantic.VPX_TABLE_SOURCE, semantic.VPX_SCRIPT_SOURCE)
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = device["binding"]["group"]
		address = device["binding"]["device"]
		if group == "pinmame.input.dip":
			not_applicable(device, "dip_switch", semantic.CONTROLLER_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", semantic.MANUAL_SOURCE)
		elif device["kind"] == "constant":
			not_applicable(device, "constant", semantic.MANUAL_SOURCE)
		elif address in {1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 21, 22, 23}:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
		elif address in {11, 12, 112, 114}:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.CORE_SOURCE)
		elif address in {111, 113}:
			not_applicable(device, "internal_nonvisual", semantic.CORE_SOURCE)
		elif address == 34:
			device["roles"] = ["cabinet.grip-trigger"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.VPX_SCRIPT_SOURCE)
			add_note(device, "The physical trigger is on the cabinet gun grip; the working VPX maps PlungerKey directly to Controller.Switch(34), so it must not receive a playfield coordinate.")
		elif address == 62:
			_measured(device, seed, "sensor")
			add_note(device, "Measured on the 2-37 Switch Locations drawing, where callout 62's leader crosses the playfield wall and ends with a tick on the left ramp's return wireform. The retained VPW table's Trigger.sw62 sits 0.13 normalized higher, at the top bend of the ramp, and the nFozzy table puts its own ramp trigger elsewhere again, so neither table object is the switch's place.")
		elif address == 64:
			_measured(device, seed, "sensor")
			add_note(device, "Measured on the 2-37 Switch Locations drawing, where callout 64's long leader, traced pixel by pixel, ends on the right ramp's outer rail. The retained VPW table's Trigger.sw64 sits higher up the ramp, 0.07 normalized away, and the nFozzy table's ramp trigger further still, so neither table object is the switch's place.")
		elif address in INPUT_POSITIONS:
			if address in INPUT_PROJECTIONS:
				located(device, INPUT_POSITIONS[address], "sensor", "observed", projection)
			else:
				located(device, INPUT_POSITIONS[address], "sensor", "validated", table_object)
			if address in {15, 16, 17}:
				device["roles"] = [*(device.get("roles") or []), "internal.trough"]
				add_note(device, "The exact VPX exposes Drain and BallRelease but no separate trough-contact objects. This is an ordered 40/60/80-percent projection between those anchors, consistent with the manual left/center/right map, with practical uncertainty of about plus or minus 0.03 normalized in both axes; the 2-37 drawing prints 15, 16 and 17 along the trough in that order.")
			elif address in {32, 33}:
				add_note(device, "The contact is internal to the moving cannon mechanism. The exact T2_Gun centre is a shared assembly projection confirmed by the manual mechanism map and the working cvpmMech windows, not an invented leaf-contact centre.")
			elif address in {44, 45}:
				add_note(device, "The switch is implicit in the exact named slingshot collision wall. The extractor's drag-point centroid is the physical assembly projection, not an invented internal leaf-contact centre.")
		else:
			raise RuntimeError(f"used switch {address} has no spatial disposition")
	if switches[24]["spatial"]["reason"] != "constant":
		raise RuntimeError("switch 24 must keep its constant disposition")

	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = device["binding"]["group"]
		address = device["binding"]["device"]
		if device["kind"] == "virtual":
			not_applicable(device, "virtual", semantic.CORE_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", semantic.MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address == 84:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and address == 7:
			device["roles"] = ["cabinet.knocker"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.VPX_SCRIPT_SOURCE)
			add_note(device, "The knocker is an internal cabinet sound device; the working table models only its callback sound, so it has no normalized playfield coordinate.")
		elif group == "pinmame.output.solenoid" and address == 24:
			device["roles"] = ["cabinet.backbox"]
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE)
			add_note(device, "The manual locates this flasher in the backglass/backbox (#906, 1 BB), outside normalized playfield space; the working script has no callback for it.")
		elif group == "pinmame.output.solenoid" and address == 31:
			not_applicable(device, "cabinet_or_service", semantic.CORE_SOURCE)
		elif group == "pinmame.output.lamp" and address == 52:
			located(device, LAMP_POSITIONS[address], "emitter", "observed", projection)
			add_note(device, "The working script fades the skull images of Primitive.L52, the T-800 skull mesh above the drop target, for this lamp; the 2-35 lamp drawing prints 52 (in head) with two leaders into the skull for its two #44 bulbs. The primitive is stored at the origin with its geometry baked into the mesh, so the placement is the world-bounds centre of the mesh (world x = 19.8 obj x, world y = 19.5 obj z), a projection of both eye bulbs onto the head.")
		elif group == "pinmame.output.lamp" and address in LAMP_POSITIONS:
			located(device, LAMP_POSITIONS[address], "emitter")
		elif group == "pinmame.output.solenoid" and address in {20, 25}:
			_measured(device, seed, "emitter")
			if address == 20:
				add_note(device, "Measured on the 2-39 Solenoid Locations drawing, whose solid balloon 20 is printed on the left-lock flashlamp between the left lane and the five-target bank. The retained VPW table only has glow lights for it (F120/F120a, falloff 300, in the left lane 0.10 normalized away), so the drawing gives the socket.")
			else:
				add_note(device, "Measured on the 2-39 Solenoid Locations drawing, where callout 25's two leaders end at two round sockets in the left lane behind the five-target bank. The retained VPW table only has two coincident glow lights for it (F125/F125a, on the targets 0.10 normalized away), so the drawing gives both sockets.")
		elif group == "pinmame.output.solenoid" and address in FLASHER_POSITIONS:
			located(device, FLASHER_POSITIONS[address], "emitter")
			add_note(device, "Named retained VPX Light.F objects are direct table geometry; closely coincident render-layer duplicates are not promoted unless they are distinct named emitter centres.")
			if address == 17:
				add_note(device, "The manual prints four #906 playfield bulbs under the Hot Dog insert; the table models them as two lights (F117/F1173 and F1172/F1174 render pairs), so each placement stands for two bulbs.")
		elif group == "pinmame.output.solenoid" and address in EFFECT_POSITIONS:
			if address in EFFECT_PROJECTIONS:
				located(device, EFFECT_POSITIONS[address], "effect", "observed", projection)
			else:
				located(device, EFFECT_POSITIONS[address], "effect", "validated", table_object)
			if address in {5, 6}:
				add_note(device, "The exact named slingshot-wall centroid is the physical actuator assembly projection; the manual and controller semantics preserve the right/left coil identity.")
			elif address == 8:
				add_note(device, "SolAPlunger fires Plunger1, the table's kickback plunger at the foot of the left outlane, so that object is the coil's effect.")
			elif address == 9:
				add_note(device, "The 2-39 drawing's leader for 9 ends on the dashed outline of the C-9638 ball shooter assembly below the playfield's front edge; the placement is the shooter-lane ball seat (Kicker.sw78, the saucer bsShooter kicks) that the assembly's plunger strikes.")
			elif address == 11:
				add_note(device, "The gun motor turns the A-14504 platform; the placement is the T2_Gun pivot the retained cvpmMech rotates, a projection of the under-playfield motor.")
			elif address == 12:
				add_note(device, "The knock-down sub-assembly is bolted to the A-14615 drop-target assembly; the placement is the drop target the coil acts on, and the 2-39 drawing prints balloon 12 on that assembly.")
			elif address == 16:
				add_note(device, "The 2-39 drawing's leader for 16 ends at the lower end of the left lane, 0.13 normalized below the lock, while the 2-4 underside map draws the B-9361-R-6 left ball-eject assembly with its B-11203-L-1 coil beside the left lock, where both retained tables put their lock kicker and the 2-37 callout 51 puts the lock switch; the placement is the lock saucer the coil ejects from.")
			elif address in {13, 14, 15}:
				add_note(device, "The exact named bumper centre is the shared pop-bumper coil/effect anchor.")
		elif group == "pinmame.output.gi" and address in {0, 1}:
			not_applicable(device, "cabinet_or_service", semantic.MANUAL_SOURCE, semantic.RUNTIME_GI_SOURCE)
		elif group == "pinmame.output.gi":
			sources = (semantic.VPX_TABLE_SOURCE, semantic.VPX_SCRIPT_SOURCE, semantic.NFOZZY_TABLE_SOURCE, semantic.NFOZZY_EXTRACTION_SOURCE)
			located(device, [(name, point(x, y)) for name, x, y, _ in GI_SOCKETS[address]], "emitter", "validated", sources)
			if address == 3:
				add_note(device, "Placements: the four lights Light2-Light5 that the retained VPW script's UpdateGI Case 3 switches, under the four CPU inserts the 2-35 drawing shows on the playfield centre line, which is where the 2-4 map puts the four-socket A-14518 G. I. lamp board.")
			else:
				side = "RIGHT PLAYFIELD" if address == 2 else "LEFT PLAYFIELD"
				add_note(device, f"Placements: the {len(GI_SOCKETS[address])} sockets both retained tables model for this string. Each is a light the VPW script's UpdateGI drives that lies within 0.01 normalized of a bulb the nFozzy table models for public {address} (a connected piece of its {NFOZZY_BULB_MESHES[address]} bulb mesh{' or a jet-cap bulb primitive' if address == 2 else ''}); nFozzy's render lights and sprites make no socket. The membership is the nFozzy table's split, which agrees with the ROM's own name for this string ({side}) and the 3-9 routing of the yellow string to the playfield and the violet one to the playfield and the coin door; the VPW table drives the whole playfield from public 2 and leaves its Left Playfield handler (Case 4) empty, a simplification rather than a different split. The manual prints no per-string bulb count, so the quantity is not asserted. The VPW lights without such a bulb, listed in the spatial audit, are not placed.")
		else:
			raise RuntimeError(f"used output {group} {address} has no spatial disposition")


def located_definition() -> dict[str, Any]:
	"""The definition with table placements applied and before the factory-drawing check promotes any."""
	definition = semantic.build_semantic()
	definition["sources"].append(callout_source_record(hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest()))
	apply_spatial(definition, load_json(CALLOUT_SEED_PATH))
	return definition


def promote_from_drawings(definition: dict[str, Any], seed: dict[str, Any]) -> dict[str, Any]:
	measured = {key: drawing_callouts.measured(seed, key) for key in seed.get("measurements", {})}
	placed = drawing_callouts.placements_of(definition)
	for key, value in measured.items():
		if placed.get(key) != value:
			raise RuntimeError(f"T2 measured placement {key} is {placed.get(key)}, but its drawing read reproduces {value}")
	decisions = drawing_callouts.apply_to_definition(definition, seed, semantic.CALLOUT_SOURCE)
	failed = sorted(pid for pid, decision in decisions["placements"].items() if not decision["agrees"] and decision["read"] is not None)
	if failed:
		raise RuntimeError(f"T2 placements disagree with their factory-drawing callouts: {failed}")
	return decisions


def callout_source_record(seed_sha256: str) -> dict[str, Any]:
	return {
		"id": semantic.CALLOUT_SOURCE, "kind": "human_review", "uri": f"internal:{CALLOUT_SEED_RELATIVE}", "sha256": seed_sha256,
		"locator": (
			"2026-10-22 factory location-drawing callout check of the manual's drawings 2-35 (lamps), 2-37 (switches) and 2-39 "
			"(solenoids and flashlamps), on the committed native-resolution excerpt crops: every callout transcribed by an independent "
			"reader working only from the page, the curator's verified corrections, per-page control fits from the three jet-bumper caps "
			"and the two flipper pivots, and the callout fit; a table placement whose own callout lands within 0.07 normalized under "
			"both fits is validated (tools/drawing_callouts.py), and the seed's measurements give the placements read off the drawing "
			"where no table object marks the part. Reads, tiles, overlays and generators are retained under review-artifacts with a "
			"pinned manifest."
		),
		"license": "NOASSERTION", "attribution": "PinMAME game definitions contributors",
	}


PROJECTION_CLASSES = {
	"switch": "The retained table's collision object for the switch (trigger, gate, target, saucer kicker, bumper or slingshot wall), chosen by what the script binds. The trough contacts 15-17 are an ordered projection between Drain and BallRelease, the cannon mark and home contacts 32/33 share the T2_Gun pivot, and the slingshot switches 44/45 take their wall's drag-point centroid; the drawing check validates those. The jet switches 42 and 43 follow the drawings, not the script's swapped binding. Switch 62 is measured on the 2-37 drawing. The cabinet, coin-door and flipper-button switches (1-8, 11-14, 21-23, 34, 112, 114) are not placed.",
	"lamp": "The script-driven Light's own centre (L11-L88; L22 and L51 have two bulbs each), validated by the 2-35 drawing. Lamp 52 drives the skull mesh Primitive.L52 and takes that mesh's world-bounds centre. The start-button lamp 84 is a cabinet lamp.",
	"solenoid": "The object the solenoid callback moves (kicker, plunger, drop target, bumper, slingshot wall, the T2_Gun pivot for the gun motor) or the Light the script fades for a flasher, validated by the 2-39 drawing where it marks the part. Flashers 20 and 25 are measured on the 2-39 drawing. The knocker 7 and the backglass flasher 24 are cabinet devices.",
	"gi": "Public G.I. 0 and 1 light the backbox insert panel and are not placed. Public 2 and 4 take the VPW lights that coincide with a bulb the nFozzy table models for the same public string (a bulb-mesh piece or a jet-cap bulb; its render lights and sprites make no socket), and public 3 the four CPU-insert lights of UpdateGI Case 3 on the A-14518 board.",
}


def audit_report(definition: dict[str, Any], seed: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
	located_inputs = sorted(device["binding"]["device"] for device in definition["inputs"] if device.get("spatial", {}).get("status") == "validated")
	located_outputs = sorted((device["binding"]["group"], device["binding"]["device"]) for device in definition["outputs"] if device.get("spatial", {}).get("status") == "validated")
	not_validated = sorted(device["id"] for device in [*definition["inputs"], *definition["outputs"]] if device.get("spatial", {}).get("status") not in {"validated", "not_applicable"})
	if not_validated:
		raise RuntimeError(f"T2 devices without validated or not-applicable spatial records: {not_validated}")
	seed_sha256 = hashlib.sha256(CALLOUT_SEED_PATH.read_bytes()).hexdigest()
	return {
		"format": "pinmame-spatial-audit", "version": 1, "machine_id": definition["machine"]["id"], "status": "author_ready",
		"coordinate_convention": {"space": "playfield", "x": "x/964; 0=left, 1=right", "y": "y/2162; 0=rear/backglass, 1=apron/player", "source_bounds": {"left": 0, "top": 0, "right": 964, "bottom": 2162}},
		"extraction": {"source_ref": semantic.VPX_EXTRACTION_SOURCE, "manifest_uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json", "manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.", "manifest_sha256": semantic.EXTRACTION_MANIFEST_SHA256, "file_count": semantic.EXTRACTION_FILE_COUNT, "total_bytes": semantic.EXTRACTION_TOTAL_BYTES, "fail_closed": True},
		"comparison_extraction": {"source_ref": semantic.NFOZZY_EXTRACTION_SOURCE, "manifest_uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/nfozzy-1-12a/extracted-vpxtool.manifest.json", "manifest_sha256": semantic.NFOZZY_MANIFEST_SHA256, "file_count": semantic.NFOZZY_FILE_COUNT, "total_bytes": semantic.NFOZZY_TOTAL_BYTES, "source_bounds": {"left": 0, "top": 0, "right": NFOZZY_X_MAX, "bottom": NFOZZY_Y_MAX}, "use": "general-illumination sockets and their public strings only", "fail_closed": True},
		"source_hashes": {"table_sha256": semantic.TABLE_SHA256, "embedded_script_sha256": semantic.SCRIPT_SHA256, "comparison_table_sha256": semantic.NFOZZY_TABLE_SHA256, "comparison_script_sha256": semantic.NFOZZY_SCRIPT_SHA256, "manual_sha256": semantic.MANUAL_SHA256, "rom_sha256": semantic.ROM_SHA256, "callout_seed_sha256": seed_sha256},
		"drawing_callout_check": drawing_callouts.summary(seed, decisions, CALLOUT_SEED_RELATIVE, seed_sha256),
		"excluded_checks": seed.get("excluded_checks", {}),
		"drawing_measurements": {key: {"page": item["page"], "label": item["label"], "pixel": item["pixel"], "normalized": item["normalized"], "note": item["note"]} for key, item in sorted(seed.get("measurements", {}).items())},
		"general_illumination": {
			"method": "A right- or left-playfield G.I. socket is a light the retained VPW script's UpdateGI handler drives that lies within 0.01 normalized of a bulb the nFozzy 1.12a table models for the same public string (a connected piece of its per-string bulb mesh or a jet-cap bulb primitive); the two tables' coordinates are each normalized by their own bounds. The CPU string's sockets are the four lights of the VPW UpdateGI Case 3 on the A-14518 board. The ROM's T.6 test names the strings; the nFozzy split, which agrees with those names and the 3-9 routing and which no retained table contradicts, assigns each socket to one (docs/SPATIAL.md, G.I. string membership).",
			"placed": {str(address): [{"light": name, "raw": [x, y], "evidence": list(evidence)} for name, x, y, evidence in sockets] for address, sockets in GI_SOCKETS.items()},
			"not_placed": GI_NOT_PLACED,
		},
		"skull_mesh": {"object": SKULL_MESH["object"], "transform": "position (0,0,0), RotX 90, size (19.8,19.5,19.5): world x = 19.8 * obj x, world y = 19.5 * obj z", "world_bounds_centre": list(SKULL_MESH["centre"])},
		"projection_classes": PROJECTION_CLASSES,
		"resolved_input_addresses": located_inputs, "resolved_output_bindings": [{"group": group, "address": address} for group, address in located_outputs],
		"unresolved": [],
		"blockers": [],
		"promotion_decision": "author_ready: every used switch, coil, flasher, lamp and G.I. string has a validated placement or a controlled not-applicable record, the factory drawings agree with every checked placement, and the definition carries no unresolved conflict.",
	}


KNOWLEDGE = """# Terminator 2: Judgment Day (Williams, 1991)

Coverage: **author_ready.** This is the physical Williams machine only. The FreeWPC builds are alternative firmware for the same hardware and stay controller variants; virtual and community rethemes are not claimed.

## Evidence precedence and exact identity

The retained known-working VPW 0022 embedded script is the semantic controller authority. The Williams operations manual is the physical wiring, switch/coil/lamp, G.I., assembly and placement authority. Pinned PinMAME revision `4ec52ff0ac13` controls public address routing, the WPC-DMD hardware generation (`0x4`), and the driver family; two hash-pinned LibPinMAME runs of the authorized `t2_l8` ROM supply what the ROM itself prints and drives in its service tests. The retained VPW table SHA-256 is `3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c`; its embedded script SHA-256 is `b5153ac46f6d4b58afb676c1f7bfdff17c6ffb953941daed8dd841c679f4e831`. The retained nFozzy 1.12a table (SHA-256 `2bae1ce5cf8c17233b5d4679032d6aa8c81e31ed32b2219a9363ad8cba244ded`) is used for its general-illumination model only. The manual SHA-256 is `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`; the authorized external `t2_l8.zip` SHA-256 is `4cdd95d435334c3bd6fe19556b410b558e67266b30e7fb767f52f4d14ed525b1`.

The canonical driver set is `t2_d2`, `t2_d3`, `t2_d4`, `t2_d6`, `t2_d8`, `t2_l2`, `t2_l2sp1`, `t2_l3`, `t2_l4`, `t2_l6`, `t2_l8`, `t2_l81`, `t2_l82`, `t2_l83`, `t2_l84`, `t2_p2f`, `t2_p2g`, `t2_f19`, `t2_f20`, and `t2_f32`. D-series ghost fixes, sound/attract/profanity revisions, and the L83/L84 physical-compatible MODs keep the same physical I/O.

## Controller inventory

All 64 switch-matrix positions `11` through `88` are present, including the printed Not Used positions; the manual numbers them column first. Cabinet/service inputs `1`-`8`, generic flipper inputs `111`-`118`, and DIP inputs `1`-`8` are explicit. The flippers are cabinet-wired (`FLIP_SWNO(12,11)` with no `FLIP_SOL`): a consumer drives the button bits `112`/`114`, which PinMAME copies into matrix switches `11`/`12` on every update. The end-of-stroke bits `111`/`113` have no CPU-side contact and nothing synthesizes them; no Williams T2 program ROM in the authorized library addresses the `WPC_FLIPPERS` register (0x3FD4) through which `wpc_r` serves that column, but the FreeWPC 0.19 build reads it, so the two bits stay optional. `115`-`118` are unused.

All lamp addresses `11`-`88` are present, including lamp `18` Not Used and the optional cabinet start-button lamp `84`. Public lamp addresses remain WPC matrix addresses; do not replace them with sequential 1-64 values. Lamps 51 Eyes Lower (two inserts in the middle of the playfield) and 52 Eyes Upper (in the skull) are two #44 bulbs each.

Solenoids `1`-`28` are all fitted. Public `29`/`30` are WPC J111 state channels and `31` the real Game-On relay that enables the cabinet-wired flippers. Public `45`-`48` are PinMAME's synthetic lower-flipper states (power `45`/`47`, combined `46`/`48`), fabricated from the buttons while the Game-On relay is on; the retained script animates the bats from `46`/`48`. The rest of `32`-`50` is unused. The five G.I. strings are public `0`-`4`, and the display is one 128x32 DMD.

The retained script callbacks are: 1 `SolSkull` (Ball Popper, opening the skull path from switch 76), 2 gun fire, 3 outhole, 4 trough ball release, 7 knocker, 8 `SolAPlunger` (fires Plunger1, the left-outlane kickback), 9 `SolShooter` (the auto plunger at switch 78), 10 top lock, 11 gun motor, 16 left lock, and 28 drop-target reset. Flashers 17-27 use `SetLamp 117` through `SetLamp 127` except 24, which the table never renders: the manual prints a backglass flashlamp on solenoid 24, and the ROM's T.5 FLASHER TEST names it F.L. C. BACKGLASS (BLU-GRY RED-WHT) and pulses public 24. The table pulses switch 42 from its lower bumper and 43 from its right one; both factory drawings put the Right Jet (42, coil 14) on the right-hand bumper and the Bottom Jet (43, coil 15) on the lowest, and the definition follows the drawings.

The manual's solenoid table wire/connector/transistor/part-number data is on every physical solenoid output; the 1-28 copy and the 3-8 interboard table agree on every pin, and the 2-38 copy prints its six J125 insert pins half a row lower (a wiring detail, noted on flashers 18-26). The printed flashlamp bulbs give the quantities: Hot Dog 17 has four playfield #906 bulbs, flashers 18-20, 22 and 23 one playfield #89 and one backbox #906 each, 21 and 25-27 two playfield #89 each, and 24 one backbox #906.

## Solenoid 12: the drop-target knock-down coil

Solenoid 12 is fitted. The A-14615 1-Bank Drop Target Assembly (printed 2-23) includes item 23, the A-14908 Target Knock Down Assembly (actuator 01-8647-L, frame and eyelet A-14913, coil SM1-26-600), bolted beside the AE-26-1200 reset coil of solenoid 28. The 1-28 solenoid table and the 2-39 Solenoid Locations list print 12 as Knock Down with that coil, the 2-39 drawing prints balloon 12 on the drop-target assembly, and the 3-8 interboard table wires it Brown/Yellow to J127-5 and Q52. The 2-38 copy of the table prints the row Not Used with a blank part number but keeps the same wire, connector and transistor. The ROM's T.4 SOLENOID TEST names 12 KNOCK DOWN and pulses it. Neither retained script fires it (the nFozzy script keeps a commented-out handler): the coil is fitted and wired and the ROM's test drives it, but the tables leave it idle in play, which is how Not Used on 2-38 reads. A recreation fits it so that a pulse drops the target and closes switch 77, the same switch solenoid 28's reset opens.

## General illumination

The ROM's own T.6 GEN'L. ILLUM. test settles the strings (`evidence/runtime/wpc-alpha/terminator-2-t2_l8-gi-test.json`): each step changes one public output alone while the display names it.

| Public | String | ROM prints | Return wire, connection, triac | Lights |
| --- | --- | --- | --- | --- |
| 0 | Top Insert String | TOP INSERT, WHT-BRN BRN | Wht-Brn, J120-7, Q18 | upper backbox insert panel |
| 1 | Bottom Insert String | BOTTOM INSERT, WHT-ORN ORN | Wht-Orn, J120-8, Q10 | lower backbox insert panel |
| 2 | Right Playfield String | RIGHT PLAYFIELD, WHT-YEL YEL | Wht-Yel, J121-9, Q14 | playfield: right side, top lanes, jets, upper centre (nFozzy's split) |
| 3 | CPU String | CPU STRING, WHT-GRN GRN | Wht-Grn, J121-10, Q16 | the four CPU inserts (A-14518 G. I. lamp board) |
| 4 | Left Playfield String | LEFT PLAYFIELD, WHT-VIO VIO | Wht-Vio, J121-11 + J119-1, Q12 | playfield: left side, top and bottom (nFozzy's split); cabinet: the coin-door lamps (3-9 J119) |

The 2-39 Solenoid Locations list prints the same five names in the same order. The 1-28 and 2-38 solenoid tables print their triac column in that order but misassign the names, wires and pins of three rows (02 Left Playfield Wht-Vio J119-1, 04 Not Used Wht-Orn J120-8, 05 Bottom Insert Wht-Grn J120-10), and the 3-9 interboard table numbers its feeds differently again, repeating those rows' wire-to-triac pairs, while routing the brown string to the insert only, yellow to the playfield only, violet to the playfield and the coin door, and green to playfield pins J121-5/J121-10; its Orange row shows no connector and its Green row also carries the insert pins J120-2/J120-8 that the orange string uses. The triacs follow the power driver board: each is fixed to its connector pins, and the Doctor Who chart and The Addams Family handbook, printed for the same board, drive J120-7 brown from Q18, J120-8 orange from Q10, J121-9 yellow from Q14, J121-10 green from Q16 and J121-11/J119-1 violet from Q12. T2's tables print exactly those pins for those wires, so their triac column follows the string numbers and it is the names, wires and pins of rows 02, 04 and 05 that are misplaced. After the fresh-NVRAM restart the ROM flickers the CPU string by itself.

No table is the wiring, and the manual draws no G.I. socket. The VPW script drives every playfield G.I. light from public 2 (Case 2), switches four lights under the CPU inserts from public 3 (Case 3: Light2-Light5) and does nothing for 0, 1 and 4; its Case 4 is an empty handler commented Left Playfield, so its single-string playfield is a simplification. The nFozzy table reads `ChangedGIStrings` and splits the playfield between public 2 and 4 with per-string bulb meshes (`GI_bulbR`, `GI_bulbL`), jet-cap bulbs, and lightmaps and render lights. Its split is the only socket-level membership there is; it agrees with the ROM's names for the two strings and with the 3-9 routing, and no retained table contradicts it, so the placements are validated under the G.I. membership rule in `docs/SPATIAL.md`. The placed sockets are the VPW lights that coincide, within 0.01 normalized, with a bulb the nFozzy table models for the same string: 20 for public 2 (seventeen bulb-mesh pieces and the three jet caps) and 7 for public 4. nFozzy's render lights and sprites make no socket, so GI_11, which sits under its GIRT_5 light but 0.033 from the nearest bulb, is not placed. The CPU string's four placements are the VPW Case 3 lights on the A-14518 board. The manual gives no per-string bulb count, so the playfield quantities are not asserted; the spatial audit lists the sixteen VPW G.I. lights without an nFozzy bulb: five render doubles under the jet caps and top-lane guides, five lights in the left lane, three in the top-right corner, two on the right side and one at the upper left. Two of the left-lane lights, GI_13 and GI_14, sit within 0.03 normalized of the two sockets the 2-39 drawing gives flasher 25.

## Mechanisms and physical assemblies

The three-ball trough initializes `bsTrough.InitSw 18,17,16,15`, with switch 18 as the outhole/exit and switches 17, 16, and 15 as the three stack seats, and sets `Balls=3`; BallRelease kicks at 90 degrees and strength 8. The shooter lane is switch 78 with a 0-degree/50-strength kick and variance 3. The left lock is switch 51 at 160/13; the top lock is switch 55 at 270/5 with variance 6. The single drop target under the skull is switch 77, raised by solenoid 28 and dropped by solenoid 12.

The cannon is a `cvpmMech` one-solenoid, reverse, non-linear mechanism driven by solenoid 11, length 240, steps 240. Home switch 33 is the 0-5 window and mark switch 32 is the 98-105 window. The retained firing callback kicks switch 31 by `-CurrentPos` with strength 45 and clears the loaded ball; the visual callback uses `CurrentPos=aNewPos/3`. Recreating the cannon requires a motorized traverse and loaded-ball/fire state, not the modern comparison script's keyframed or magnet device. Switch 34 is the trigger on the cabinet gun grip; the working script maps `PlungerKey` directly to it, so it has no playfield coordinate.

The two lower flippers are C-13174 assemblies with FL-11630 coils, powered from the power driver board (right Blu-Yel J109-7, left Gry-Yel J109-5) through the Game-On relay and switched by the cabinet buttons; there is no CPU flipper drive. The manual mechanism map and assembly pages identify the A-8039-3 outhole/trough, C-9638 shooter, A-14525 right kickback, B-11873 left kickback, B-12665 kicker arms with B-13935 coils, A-14507 gun-kicker assembly, A-14504 cannon platform, A-13892-2 motor regulator, ball eject assemblies, A-14501 ball popper, A-14615 single-bank drop target with its A-14908 knock-down, and lamp boards A-K (board C is the A-14518 G. I. lamp assembly).

## Normalized playfield geometry

The coordinate convention is `x=raw_x/964`, `y=raw_y/2162`, with x=0 left and x=1 right, y=0 rear/backglass and y=1 apron/player. Table placements name their exact retained VPX object; the extraction contains 548 files totaling 132,477,924 bytes, and its canonical manifest hashes to `f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9`. The nFozzy extraction (938 files, 53,404,733 bytes, manifest `ce5765a02329975e00b0e52d9bba1be86eea49f01def99c62221b8621a902213`) is compared after normalizing by its own bounds (952.94116 x 2164.706). The curator re-derives the G.I. sockets and the skull-mesh centre from both extractions whenever the evidence root is configured.

Every located placement was checked against the manual's three factory location drawings (2-35 lamps, 2-37 switches, 2-39 solenoids and flashlamps) with `tools/drawing_callouts.py`: per-page control fits from the three jet-bumper caps and the two flipper pivots, and a placement agrees when its own callout lands within 0.07 normalized under both fits. Every checked placement whose callout the drawing prints agrees; the second bulbs of flashers 17 and 21 have no callout of their own (each drawn callout marks the nearer bulb) and keep their table status. Where no table object marks the part the drawing shows, the placement is measured on the drawing through the same control fit: switches 62 and 64 (the ramps' made switches, on the left return wireform and the right ramp's outer rail), flasher 20 (the left-lock flashlamp) and flasher 25 (two sockets in the left lane). Coils 9 and 16 are not checked: their leaders end at the far end of the shooter assembly and at the bottom of the left lane, while the placements are the ball seats their callbacks kick from, and for 16 the 2-4 underside map puts the left eject assembly beside the lock.

The trough contacts are an ordered 40/60/80-percent projection between the exact drain and ball-release anchors (about plus or minus 0.03 normalized), in the order the 2-37 drawing prints 15, 16 and 17 along the trough. The cannon contacts 32/33 share the T2_Gun pivot, the slingshot switches and coils take their wall's drag-point centroid, and lamp 52 takes the world-bounds centre of the skull mesh `Primitive.L52`, which sits over the drop target. Cabinet grip switch 34, the flipper buttons, knocker output 7, backglass flasher 24, start-button lamp 84, the two backbox G.I. strings and the DMD are controlled non-playfield records rather than fake playfield points.
"""


def expected(root: Path) -> tuple[dict[str, Any], str, dict[str, Any]]:
	seed = load_json(CALLOUT_SEED_PATH)
	definition = located_definition()
	decisions = promote_from_drawings(definition, seed)
	return definition, KNOWLEDGE.rstrip() + "\n", audit_report(definition, seed, decisions)


def check(root: Path = ROOT) -> None:
	source_root = semantic.configured_vpx_sources_root(required=False)
	if source_root is not None:
		verify_retained_geometry(source_root)
	definition, knowledge, audit = expected(root)
	actual_definition = root / DEFINITION_PATH.relative_to(ROOT)
	actual_knowledge = root / KNOWLEDGE_PATH.relative_to(ROOT)
	actual_audit = root / AUDIT_PATH.relative_to(ROOT)
	if not actual_definition.is_file() or actual_definition.read_bytes() != canonical_bytes(definition):
		raise SystemExit(f"T2 curator check failed: {actual_definition} is not deterministic output")
	if (root / FORMER_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise SystemExit("T2 curator check failed: the former partial definition still exists")
	if not actual_knowledge.is_file() or actual_knowledge.read_text(encoding="utf-8") != knowledge:
		raise SystemExit(f"T2 curator check failed: {actual_knowledge} is not deterministic output")
	if not actual_audit.is_file() or actual_audit.read_bytes() != canonical_bytes(audit):
		raise SystemExit(f"T2 curator check failed: {actual_audit} is not deterministic output")
	verified_suffix = " and configured retained extractions" if source_root is not None else ""
	print(f"T2 curator check: deterministic canonical definition, knowledge, and spatial audit{verified_suffix}")


def generate(root: Path = ROOT) -> None:
	source_root = semantic.configured_vpx_sources_root(required=True)
	assert source_root is not None
	verify_retained_geometry(source_root)
	definition, knowledge, audit = expected(root)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	former = root / FORMER_DEFINITION_PATH.relative_to(ROOT)
	if former.exists():
		former.unlink()
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), knowledge)
	write_json(root / AUDIT_PATH.relative_to(ROOT), audit)
	rebuild_catalog(root)
	print("T2 curator regeneration: definition, knowledge, spatial audit, and catalog rebuilt")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--regenerate", action="store_true")
	args = parser.parse_args()
	if args.check:
		check()
	else:
		generate()


if __name__ == "__main__":
	main()
