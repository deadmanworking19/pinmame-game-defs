from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_corvette as curator  # noqa: E402
import corvette_runtime_evidence as evidence_tool  # noqa: E402
import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "corvette-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "corvette-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "corvette-1994.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "corvette-1994.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-security"
SCENARIO_DIRECTORY = ROOT / "tools" / "harness-scenarios" / "wpc-security"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.corvette.1994"

DRIVER_IDS = {"corv_21", "corv_px3", "corv_px4", "corv_px5", "corv_la1", "corv_lx1", "corv_dx1", "corv_la2", "corv_lx2", "corv_f61"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# src/wpc/sims/wpc/prelim/corv.c corvGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
CORV_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x7F, 0x07, 0x33, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00)
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "20e161d4e397650d436fc85ef01ce78bc144905444bd7e5fb4331f58edd5e211"
SCRIPT_SHA256 = "d30534b6664ed214a3c8b33597ab1021bcc66e979363611e218d4fccb35e5bb5"
# Seed entries whose coordinate is a script constant, not the named object's own point: the race encoders sit at each
# lane's finish end (BlueCarXFinish/BlueCarYFinish and RedCarXFinish/RedCarYFinish).
SCRIPT_CONSTANT_POINTS = {("switch", "55"): (878.0, 117.0), ("switch", "56"): (936.0, 117.0)}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class CorvetteTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.corvette.1994", 570, 1994, "50036", "GrjDz-MJKN6"), (machine["id"], machine["ipdb_id"], machine["year"], machine["model_number"], machine["opdb_id"]))
		self.assertEqual(("pinmame.wpc-security", "0x20"), (self.definition["controller"]["platform"], self.definition["controller"]["hardware_generation"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual({"corv_px3", "corv_px4", "corv_px5"}, {k for k, v in drivers.items() if v["physical_compatibility"] == "unknown"})
		self.assertEqual("identical", drivers["corv_f61"]["physical_compatibility"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual(["conflict.gi-string-halves"], [conflict["id"] for conflict in self.definition["conflicts"]])
		conflict = self.definition["conflicts"][0]
		self.assertNotIn("status", conflict)
		self.assertIn("Resolution path:", conflict["description"])
		self.assertEqual([curator.MANUAL_SOURCE, curator.GI_TEST_SOURCE, curator.VPX_SCRIPT_SOURCE], conflict["source_refs"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 54)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		self.assertEqual({53, 54, 73, 74, 85, 115}, {a for a, s in self.switches.items() if s["availability"] == "unused"})
		self.assertEqual({4, 25, 26, 27, 28}, {a for a, s in self.switches.items() if s["availability"] == "optional"})
		self.assertEqual({6, 14, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {a for a, c in self.coils.items() if c["availability"] == "unused"})

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (CORV_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(set(curator.MASKED_SWITCHES), inverted)
		self.assertEqual(inverted, set(evidence_tool.PINMAME_MASKED))
		self.assertEqual(curator.SHADED_SWITCHES - {112, 114, 116, 118}, inverted)
		for address in inverted:
			self.assertTrue(self.switches[address]["normally_closed"], address)
		for address in set(self.switches) - inverted - {24}:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])

	def test_fliptronic_column_roles(self) -> None:
		self.assertEqual(["flipper.lower.right.button"], self.switches[112]["roles"])
		self.assertEqual(["flipper.lower.right.button"], self.switches[116]["roles"])
		self.assertEqual(["flipper.lower.left.button"], self.switches[114]["roles"])
		self.assertEqual(["flipper.upper.left.button"], self.switches[118]["roles"])
		self.assertIn("writes 112 and 116 together", self.switches[116]["physical"]["notes"])
		self.assertIn("writes 114 and 118 together", self.switches[118]["physical"]["notes"])
		for address in (111, 113, 117):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"], address)
		self.assertIn("J906-4 Not Used", self.switches[115]["physical"]["notes"])

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			if address == 24:
				continue
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual(curator.ROM_SWITCH_NAMES, {k: v for k, v in evidence_tool.EDGE_NAMES.items() if v != "NOT USED"})
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES}, evidence_tool.T4_NAMES)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual({number: (name, wires) for number, name, wires, _ in evidence_tool.T12_ORDER}, {
			{45: 1, 46: 2, 47: 3, 48: 4, 35: 7, 36: 8}[a]: v for a, v in curator.ROM_SOLENOID_NAMES.items() if a in curator.T12_ADDRESSES
		})
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})
		self.assertEqual(curator.ROM_LAMP_NAMES, evidence_tool.LAMP_NAMES)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f'names it "{name}"', self.lamps[address]["physical"]["notes"], address)

	def test_outputs_kinds_and_the_engine_and_race_controls(self) -> None:
		self.assertEqual(set(range(20, 29)), {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual({17, 51, 52, 53}, {a for a, c in self.coils.items() if c["kind"] == "control_signal"})
		self.assertEqual({18, 19}, {a for a, c in self.coils.items() if c["kind"] == "motor"})
		for address in (22, 23, 24, 25, 26, 27):
			self.assertEqual(2, self.coils[address]["physical"]["quantity"], address)
		self.assertNotIn("quantity", self.coils[28]["physical"])
		self.assertIn("engine power enable", self.coils[51]["physical"]["notes"])
		self.assertIn("EXTBOARD", json.dumps(self.definition["sources"]))
		self.assertEqual(["flipper.upper.left"], self.coils[35]["roles"])
		self.assertEqual(("device.diverter-power", "device.diverter-hold"), (self.coils[33]["id"], self.coils[34]["id"]))
		for address in (7, 20):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		self.assertEqual({87: ["cabinet.buy-in"], 88: ["cabinet.start-button-lamp"]}, {a: self.lamps[a]["roles"] for a in (87, 88)})
		self.assertEqual("not_applicable", self.gi[4]["spatial"]["status"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		engine = mechanisms["mechanism.zr1-engine"]
		self.assertEqual([self.coils[a]["id"] for a in (51, 52, 53)], engine["actuators"])
		self.assertEqual(["switch.matrix-71", "switch.matrix-72"], engine["sensors"])
		self.assertIn("GetMech(2)", engine["behavior"])
		self.assertIn("four coils", engine["behavior"])
		self.assertIn("ENGINE COILS (4)", (EXCERPT_DIRECTORY / "unit-disassembly-engine.md").read_text(encoding="utf-8"))
		race = mechanisms["mechanism.race-track"]
		self.assertEqual([self.coils[a]["id"] for a in (17, 18, 19)], race["actuators"])
		self.assertEqual([f"switch.matrix-{a}" for a in (51, 55, 52, 56)], race["sensors"])
		lock = mechanisms["mechanism.zr1-lock"]["behavior"]
		for phrase in ("LGate", "Wall12", "GateU", "Kicker1", "Kicker3", "the ROM decides when to fire them"):
			self.assertIn(phrase, lock, phrase)
		self.assertIn("table approximation", engine["behavior"])
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
			for placement in spatial.get("placements", []):
				cited.update(placement["provenance"]["source_refs"])
		for conflict in self.definition["conflicts"]:
			cited.update(conflict["source_refs"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		self.assertEqual(set(sources), cited | {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE})
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				self.assertNotIn(b"\r", (ROOT / excerpt["path"]).read_bytes(), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("rendered at its native resolution", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.webp")}, {"switch-locations", "lamp-locations", "solenoid-flasher-locations"})
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])
		contract = (EXCERPT_DIRECTORY / "vpx-script-contract.md").read_text(encoding="utf-8")
		self.assertIn(SCRIPT_SHA256, contract)
		for snippet in ('SolCallback(2) = "SolLGate"', "bsLock.InitKick Kicker3,235,1", "For each xx in GI1:xx.State = 1: Next", "NFadeLm 128,  L128"):
			self.assertIn(snippet, contract, snippet)
		for path in EXCERPT_DIRECTORY.glob("*.md"):
			self.assertIsNone(re.search(r"[A-Z]:[\\/]", path.read_text(encoding="utf-8")), path.name)

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertLessEqual(len(f"{value:.10f}".rstrip("0").split(".")[1]), 6, placement["id"])
			quantity = item.get("physical", {}).get("quantity")
			if quantity is not None and item["kind"] in {"lamp", "flasher"}:
				self.assertGreaterEqual(quantity, len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))
		# The jet bumpers pair as the script's events fire them: left 63 on Bumper2, bottom 64 on Bumper1, right 65 on Bumper3.
		seed = load(curator.SPATIAL_SEED_PATH)
		self.assertEqual({"63": "Bumper2", "64": "Bumper1", "65": "Bumper3"}, {a: seed["switch"][a][0]["object"] for a in ("63", "64", "65")})
		self.assertEqual({}, seed["gi"])
		# Every fitted playfield device is placed except the four playfield G.I. strings the conflict holds back and the devices
		# the table draws only on Flasher sprites (a glow, not a socket) or a light parked off the playfield.
		report = load(SPATIAL_REPORT_PATH)
		sprite_only = [f"lamp.matrix-{a}" for a in (76, 77, 78, 81, 82, 83, 84, 85, 86)]
		self.assertEqual(sorted(["device.zr-1-underside-flasher", "gi.string-1", "gi.string-2", "gi.string-3", "gi.string-4", *sprite_only]), report["without_placements"])
		self.assertEqual((2, 2), (self.lamps[83]["physical"]["quantity"], self.lamps[84]["physical"]["quantity"]))
		for address in (76, 77, 78, 81, 82, 83, 84, 85, 86):
			self.assertIn("a Flasher sprite is a glow, not evidence of a socket", self.lamps[address]["physical"]["notes"], address)
		# 53 and 68 sit on the table's stacked bulb meshes, not on their glow sprites.
		self.assertEqual({"53": "L81P1", "68": "L81P4"}, {a: seed["lamp"][a][0]["object"] for a in ("53", "68")})
		for category in ("lamp", "solenoid"):
			self.assertEqual([], [entry["object"] for entries in seed[category].values() for entry in entries if entry["object"].casefold().startswith(("f5", "f6", "f7", "f8", "flasher"))], category)
		# Placement provenance names the coordinate source, the script binding and, for a projection, the manual.
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				refs = placement["provenance"]["source_refs"]
				self.assertLessEqual({curator.VPX_TABLE_SOURCE, curator.VPX_SCRIPT_SOURCE}, set(refs), placement["id"])
				address = item["binding"]["device"]
				category = "switch" if item["binding"]["group"] == curator.SWITCH_GROUP else "solenoid" if item["binding"]["group"] == curator.SOLENOID_GROUP else "lamp"
				self.assertEqual((category, address) in curator.PROJECTED_PLACEMENTS, curator.MANUAL_SOURCE in refs, placement["id"])
		for address in range(4):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertIn("G.I. string conflict", self.gi[address]["physical"]["notes"], address)

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition), seed.get("limit", drawing_callouts.LIMIT))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		validated = {
			placement["id"]
			for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]
			for placement in (item.get("spatial") or {}).get("placements", [])
			if placement["provenance"]["status"] == "validated"
		}
		self.assertEqual(agreeing, validated)
		self.assertGreaterEqual(len(validated), 90)
		self.assertEqual({"2-45", "2-47", "2-49"}, set(seed["pages"]))
		for key, page in seed["pages"].items():
			self.assertEqual(5, len(page["controls"]), key)
			self.assertLessEqual(decisions["pages"][key]["control_loo_max"], 0.025, key)
			for read in page["reads"]:
				if read["region"] != "playfield":
					self.assertIn(read["region"], {"race-track", "race-tree-inset", "cabinet"}, (key, read["label"]))
		self.assertEqual({}, seed["measurements"])
		projected = {f"switch.matrix-{a}.sensor" for a in (31, 32, 33, 34, 37, 51, 52, 55, 56, 71, 72, 76, 77, 78)}
		self.assertLessEqual(projected, set(seed["excluded_checks"]))
		self.assertEqual(set(), projected & validated)
		self.assertEqual(set(), {f"lamp.matrix-{a}.emitter" for a in range(81, 87)} & validated)
		for pid, reason in seed["excluded_checks"].items():
			self.assertNotIn(pid, seed["checks"])
			self.assertTrue(reason)
		corrected = {(key, read["label"]) for key, page in seed["pages"].items() for read in page["reads"] if "verifier_note" in read}
		self.assertEqual({("2-47", "18"), ("2-47", "64"), ("2-47", "65"), ("2-47", "68"), ("2-47", "86"), ("2-49", "11"), ("2-49", "12")}, corrected)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_retained_callout_artifacts_match_the_seed(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		checked = drawing_callouts.verify_retained(seed, ROOT, None, Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))
		self.assertGreater(checked, 3)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "corvette-1994" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		for snippet in (
			'Const cGameName="corv_21"', ".HandleMechanics = 7", 'SolCallback(15) ="bsLock.SolOut"', "bsLock.InitSw 0,76,77,78,0,0,0,0",
			"bsLock.InitKick Kicker3,235,1", "Sub SolLGate(Enabled) 'Lock Gate 1", "'SolCallback(33) =", "engnew=Controller.getmech(2)",
			"For each xx in GI1:xx.State = 1: Next",
		):
			self.assertIn(snippet, text, snippet)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_every_table_coordinate_recomputes_from_the_retained_gameitems(self) -> None:
		"""Each table-derived seed coordinate is its object's own point: a light, kicker, bumper, gate, flipper, spinner or
		plunger centre, a trigger's, wall's or rubber's drag-point centroid, or a hit target's or primitive's position; never a
		Flasher sprite, which is a glow rather than a socket. The race encoders take the script's finish constants instead (SCRIPT_CONSTANT_POINTS)."""
		gameitems = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		by_name = {path.stem.split(".", 1)[1].lower(): path for path in gameitems.glob("*.json")}

		def point(name: str) -> tuple[float, float]:
			path = by_name[name.lower()]
			kind = path.stem.split(".")[0]
			data = json.loads(path.read_text(encoding="utf-8"))[kind]
			if kind in {"Trigger", "Wall", "Rubber"}:
				vertices = [item.get("vertex", item) for item in data["drag_points"]]
				return sum(v["x"] for v in vertices) / len(vertices), sum(v["y"] for v in vertices) / len(vertices)
			if kind in {"Primitive", "HitTarget"}:
				return data["position"]["x"], data["position"]["y"]
			self.assertNotEqual("Flasher", kind, name)
			return data["center"]["x"], data["center"]["y"]

		script = (Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / curator.EXTRACTION_RELATIVE_PATH / "script.vbs").read_text(encoding="utf-8", errors="replace")
		for car, (x, y) in (("BlueCar", SCRIPT_CONSTANT_POINTS[("switch", "55")]), ("RedCar", SCRIPT_CONSTANT_POINTS[("switch", "56")])):
			self.assertRegex(script, rf"Const {car}XFinish\s*=\s*{int(x)}\b")
			self.assertRegex(script, rf"Const {car}YFinish\s*=\s*{int(y)}\b")
		seed = load(curator.SPATIAL_SEED_PATH)
		checked = 0
		for category in ("switch", "solenoid", "lamp"):
			for address, entries in seed[category].items():
				for entry in entries:
					x, y = SCRIPT_CONSTANT_POINTS.get((category, address)) or point(entry["object"])
					self.assertAlmostEqual(x / curator.PLAYFIELD_WIDTH, entry["x"], delta=2e-6, msg=(category, address, entry["object"]))
					self.assertAlmostEqual(y / curator.PLAYFIELD_HEIGHT, entry["y"], delta=2e-6, msg=(category, address, entry["object"]))
					checked += 1
		self.assertGreater(checked, 120)

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Catalog driver ids that are ordinary words in this record's prose.
		ordinary_words = {"corvette", "engine", "pitstop", "race", "racetrack", "real"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"bally.corvette.1994"}
		)
		self.assertIn("ts_lx5", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_corvette.py", ROOT / "tools" / "corvette_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "bally").glob("corvette-1994*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted(SCENARIO_DIRECTORY.glob("cv-*.json")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			self.assertEqual([], found, path.name)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("engine", "race track", "GetMech(2)", "shifter", "spatial_placement", "unresolved_conflicts", "112 and 116", "LGate"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (_directory, scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = SCENARIO_DIRECTORY / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.corvette.1994"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn(f"--handle-mechanics {mechanics} ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id, name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "corvette-corv_21-switch-edges.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		for address in curator.UNUSED_MATRIX_ADDRESSES:
			self.assertTrue(texts[f"{address} -> 1"].startswith("NOT USED"), address)
		self.assertTrue(texts["115 -> 1"].startswith("SWITCH EDGES"))
		solenoids = load(RUNTIME_DIRECTORY / "corvette-corv_21-solenoid-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[a] for a in evidence_tool.T4_ORDER], [item["transitioned_solenoid_addresses"] for item in solenoids])
		lamps = load(RUNTIME_DIRECTORY / "corvette-corv_21-single-lamps.json")["runtime"]["observations"]["diagnostic_snapshots"]
		self.assertEqual(65, len(lamps))

	def test_every_reading_is_pinned_to_its_frame(self) -> None:
		seed = load(evidence_tool.FRAME_SEED_PATH)
		self.assertEqual(set(evidence_tool.RUNS), set(seed))
		for filename in evidence_tool.RUNS:
			snapshots = load(RUNTIME_DIRECTORY / filename)["runtime"]["observations"]["diagnostic_snapshots"]
			self.assertEqual(seed[filename], {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in snapshots}, filename)
		with self.assertRaises(ValueError):
			observations = {"diagnostic_snapshots": [dict(item) for item in load(RUNTIME_DIRECTORY / "corvette-corv_21-engine-test.json")["runtime"]["observations"]["diagnostic_snapshots"]]}
			observations["diagnostic_snapshots"][1]["pixel_sha256"] = "0" * 64
			evidence_tool._check_pinned_frames("corvette-corv_21-engine-test.json", observations)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, "corv_21")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(mechanics, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_builders_refuse_transitions_in_the_wrong_direction(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY

		def mutated(directory: str, label: str, channel: str, number: int, states: list[int]) -> dict:
			run = json.loads((root / directory / "run.json").read_bytes())
			step = next(item for item in run["steps"] if item["label"] == label)
			for item in step["transitions"][channel]:
				if item["number"] == number:
					item["states"] = states
			return run

		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(mutated("cv-single-lamps", "T.8 Up 1", "lamps", 12, [0]))
		with self.assertRaises(ValueError):
			evidence_tool.build_engine_failed(mutated("cv-engine-test-no-mech", "SELF TEST 6", "solenoids", 51, [1]))
		with self.assertRaises(ValueError):
			evidence_tool.build_zr1_adjust(mutated("cv-zr1-adjust", "Enter (start T.18)", "solenoids", 51, [0]))
		extra = mutated("cv-single-lamps", "T.8 Up 1", "lamps", 12, [1, 0, 1])
		next(item for item in extra["steps"] if item["label"] == "T.8 Up 1")["transitions"]["lamps"].append({"number": 88, "states": [1]})
		with self.assertRaises(ValueError):
			evidence_tool.build_lamps(extra)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_readings_are_checked_against_the_retained_frame_files(self) -> None:
		directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / "cv-zr1-adjust"
		run = evidence_tool._load_run(directory, "cv-zr1-adjust", 7)
		snapshot = next(item for item in run["snapshots"] if item["label"] == "Enter (start T.18)")
		display = next(item for item in snapshot["displays"] if item["index"] == 0)
		self.assertTrue(evidence_tool._frame_matches(run, display))
		display["pixel_sha256"] = "0" * 64
		self.assertFalse(evidence_tool._frame_matches(run, display))
		display["artifact"] = "dmd/missing-frame.pgm"
		with self.assertRaises(OSError):
			evidence_tool._frame_matches(run, display)


if __name__ == "__main__":
	unittest.main()
