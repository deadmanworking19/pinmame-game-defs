from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "the-flintstones-1994.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "the-flintstones-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "the-flintstones-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "the-flintstones-1994.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "the-flintstones-1994.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "williams.the-flintstones.1994"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
MACHINE_ID = "williams.the-flintstones.1994"

COMPATIBILITY = {
	"fs_lx5": "identical", "fs_lx4": "identical", "fs_lx3": "identical", "fs_lx2": "identical", "fs_la5": "compatible",
	"fs_sp2": "compatible", "fs_dx5": "compatible", "fs_dx4": "compatible", "fs_dx2": "compatible", "fs_sp2d": "compatible",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# fsGameData's inverted-switch mask as printed in src/wpc/sims/wpc/prelim/fs.c.
INVERTED_MASK = (0x00, 0x00, 0x00, 0x3F, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
OPTOS = {31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 46, 47}
PLAYFIELD_FLASHERS = {17, 18, 19, 20, 21, 22, 24, 25, 28}
TWIN_BULB_LAMPS = {41, 52, 63, 64, 72, 86}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_xy(device: dict) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


def mask_addresses(mask: tuple[int, ...]) -> set[int]:
	return {column * 10 + bit + 1 for column, value in enumerate(mask) for bit in range(8) if value >> bit & 1}


def rom_table(heading: str) -> dict[str, str]:
	"""Rows of one decoded ROM table in the excerpt, keyed by the table's own label."""
	text = (EXCERPTS / "rom-name-tables.md").read_text(encoding="utf-8")
	section = text.split(f"## {heading}", 1)[1].split("\n## ", 1)[0]
	rows = {}
	for label, cell in re.findall(r"(?m)^\| (\S+) \| (`[^`]*`|\(empty string\)) \|$", section):
		rows[label] = "" if cell == "(empty string)" else cell[1:-1]
	return rows


def pinned_pinmame_checkout() -> Path | None:
	import curate_the_flintstones as curator
	from pinmame_game_defs.workspace import resolve_working_root

	configured = os.environ.get("PINMAME_SOURCE_ROOT")
	candidates = [Path(configured)] if configured else []
	working_root = resolve_working_root(ROOT)
	if working_root is not None:
		candidates.append(working_root / "source-checkouts" / f"pinmame-{curator.PINMAME_REVISION[:8]}")
	for path in candidates:
		if not (path / "src/wpc/sims/wpc/prelim/fs.c").is_file():
			continue
		head = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, encoding="utf-8")
		if head.returncode == 0 and head.stdout.strip() == curator.PINMAME_REVISION:
			return path
	return None


class TheFlintstonesTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = by_address(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = by_address(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_address(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gis = by_address(cls.definition, "outputs", "pinmame.output.gi")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}
		cls.mechanisms = {mechanism["id"]: mechanism for mechanism in cls.definition["mechanisms"]}

	def test_identity_and_honest_partial_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "The Flintstones", "Williams", 1994), (machine["id"], machine["name"], machine["manufacturer"], machine["year"]))
		self.assertEqual((888, "GRK95-MQ674", "50029", "physical_pinball"), (machine["ipdb_id"], machine["opdb_id"], machine["model_number"], machine["kind"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual({"validated"}, {value for key, value in coverage["dimensions"].items() if key != "spatial_placement"})
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual([], self.definition["relationships"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertEqual({"path": "knowledge/williams/the-flintstones-1994.md", "status": "complete"}, self.definition["knowledge"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_catalog_maps_exactly_the_ten_drivers_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(set(COMPATIBILITY), mapped)
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(COMPATIBILITY, {identifier: driver["physical_compatibility"] for identifier, driver in drivers.items()})
		self.assertNotIn("clone_of", drivers["fs_lx5"])
		self.assertEqual({"fs_lx5"}, {driver["clone_of"] for identifier, driver in drivers.items() if identifier != "fs_lx5"})
		for identifier in ("fs_dx5", "fs_dx4", "fs_dx2", "fs_sp2d"):
			self.assertIn("LED Ghost Fix", drivers[identifier]["description"])
			self.assertIn("not a Williams release", drivers[identifier]["variant_notes"])

	def test_the_full_input_space_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119))
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		unused = {address for address, device in self.switches.items() if device["availability"] == "unused"}
		self.assertEqual({57, 58, 117, 118} | set(range(81, 89)), unused)
		optional = {address for address, device in self.switches.items() if device["availability"] == "optional"}
		self.assertEqual({4, 12}, optional)

	def test_opto_polarity_matches_the_re_derived_pinmame_mask(self) -> None:
		normalized = mask_addresses(INVERTED_MASK)
		self.assertEqual(OPTOS, normalized)
		closed = {address for address, device in self.switches.items() if device.get("normally_closed")}
		self.assertEqual(normalized, closed)
		optos = {address for address, device in self.switches.items() if device.get("physical", {}).get("switch_type") == "opto" and address < 100}
		self.assertEqual(normalized | {12}, optos)
		self.assertFalse(self.switches[12]["normally_closed"])
		for address in normalized:
			self.assertIn("must not be inverted again", self.switches[address]["physical"]["notes"])

	def test_labels_follow_the_rom_where_the_printed_tables_differ(self) -> None:
		self.assertEqual("Trough Jam", self.switches[31]["label"])
		self.assertEqual(["Trough 1", "Trough 2", "Trough 3", "Trough 4"], [self.switches[address]["label"] for address in (32, 33, 34, 35)])
		self.assertIn("Upper", self.switches[51]["label"])
		self.assertIn("Lower", self.switches[53]["label"])
		for address in (51, 52, 53):
			self.assertEqual(2, len(self.switches[address]["spatial"]["placements"]))
		for address in (31, 32, 33, 34, 35, 51, 53):
			self.assertIn("which is recorded", self.switches[address]["physical"]["notes"])

	def test_curator_rom_texts_equal_the_decoded_excerpt(self) -> None:
		import curate_the_flintstones as curator

		switches = rom_table("Switch table")
		self.assertEqual({str(address): text for address, text in curator.ROM_SWITCH_TEXT.items()}, {label: text for label, text in switches.items() if label.isdigit() and switches[label] != "NOT USED"})
		self.assertEqual({str(address) for address in curator.UNUSED_MATRIX_ADDRESSES}, {label for label, text in switches.items() if text == "NOT USED"})
		self.assertEqual({str(address): text for address, text in curator.ROM_LAMP_TEXT.items()}, rom_table("Lamp table"))
		coils = rom_table("Coil table")
		self.assertEqual({str(entry): curator.ROM_COIL_TEXT[address] for address, entry in curator.ROM_COIL_ENTRY.items()}, coils)
		flashers = rom_table("Flasher table")
		self.assertEqual({str(entry): curator.ROM_COIL_TEXT[address] for address, entry in curator.ROM_FLASHER_ENTRY.items()}, flashers)
		flipper = rom_table("Fliptronic switch table")
		self.assertEqual({f"F{address - 110}": entry[7] for address, entry in curator.FLIPPER_SWITCHES.items()}, {label: text for label, text in flipper.items() if text})
		self.assertEqual({"F7", "F8"}, {label for label, text in flipper.items() if not text})
		self.assertEqual(["ILLUM. STRING 1", "ILLUM. STRING 2", "ILLUM. STRING 3", "ILLUM. STRING 4", "ILLUM. STRING 5", "ALL ILLUMINATION"], list(rom_table("G.I. table").values()))
		for address, device in self.switches.items():
			if address in curator.ROM_SWITCH_TEXT:
				self.assertIn(f"'{curator.ROM_SWITCH_TEXT[address]}'", device["physical"]["notes"], address)

	def test_fliptronic_column(self) -> None:
		for address in (112, 114, 116):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		for address in (111, 113, 115):
			self.assertEqual("leaf", self.switches[address]["physical"]["switch_type"])
			self.assertIn("must not drive it", self.switches[address]["physical"]["notes"])
		for address in (112, 116):
			self.assertIn("a host drives 112 and 116 together", self.switches[address]["physical"]["notes"])
		mechanism = self.mechanisms["mechanism.flippers"]
		self.assertEqual({f"switch.generic-{address}" for address in range(111, 117)}, set(mechanism["sensors"]))

	def test_always_closed_switch(self) -> None:
		device = self.switches[24]
		self.assertEqual("constant", device["kind"])
		self.assertTrue(device["constant_active"])

	def test_the_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gis))
		kinds = {address: device["kind"] for address, device in self.solenoids.items()}
		self.assertEqual(PLAYFIELD_FLASHERS | {26, 27}, {address for address, kind in kinds.items() if kind == "flasher"})
		self.assertEqual({23}, {address for address, kind in kinds.items() if kind == "motor"})
		self.assertEqual(set(range(29, 33)) | set(range(37, 45)) | {49, 50}, {address for address, kind in kinds.items() if kind == "virtual"})
		self.assertEqual({32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {address for address, device in self.solenoids.items() if device["availability"] == "unused"})
		self.assertEqual(set(), {address for address, device in self.lamps.items() if device["availability"] != "used"})
		for address in range(37, 45):
			self.assertIn(f"'{address}* Not Used'", self.solenoids[address]["physical"]["notes"])
		self.assertEqual({26, 27}, {address for address, device in self.solenoids.items() if "cabinet.backbox-flasher" in device.get("roles", [])})

	def test_flasher_quantities_count_every_printed_bulb(self) -> None:
		# The PDF 109 table prints playfield and backbox flashlamp counts in parentheses; quantity is their sum.
		text = (EXCERPTS / "solenoid-flasher-table.md").read_text(encoding="utf-8")
		section = text.split("### Solenoid rows", 1)[1].split("### General Illumination block", 1)[0]
		printed = {}
		for line in section.splitlines():
			match = re.match(r"\| (\d\d) \|", line)
			if match and int(match.group(1)) in PLAYFIELD_FLASHERS | {26, 27}:
				cells = [cell.strip() for cell in line.strip("|").split("|")]
				printed[int(match.group(1))] = sum(int(count) for cell in cells[-2:] for count in re.findall(r"\((\d+)\)", cell))
		self.assertEqual(PLAYFIELD_FLASHERS | {26, 27}, set(printed))
		self.assertEqual({17: 3, 18: 3, 19: 3, 20: 4, 21: 3}, {address: printed[address] for address in range(17, 22)})
		self.assertEqual(printed, {address: self.solenoids[address]["physical"]["quantity"] for address in printed})

	def test_flipper_circuits_and_up_down_gates(self) -> None:
		printed = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
		for address, number in printed.items():
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(number, aliases["manual.address"], address)
		self.assertEqual(("Upper Right Flipper Power", "Upper Right Flipper Hold"), (self.solenoids[33]["label"], self.solenoids[34]["label"]))
		self.assertEqual(("Right Up/Down Gate", "Left Up/Down Gate"), (self.solenoids[35]["label"], self.solenoids[36]["label"]))
		for address, transistor in ((35, "Q1"), (36, "Q5")):
			wiring = self.solenoids[address]["wiring"]
			self.assertEqual((transistor, "J907-8 (Red-Gry)"), (wiring["driver_transistor"], wiring["power_connection"]))
			self.assertIn("upper-left circuit", self.solenoids[address]["physical"]["notes"])

	def test_gi_strings_follow_the_settled_readings(self) -> None:
		self.assertEqual(
			["Machine Lighting", "Flintstones Logo", "Upper Playfield & Insert Panel", "Middle Playfield & Insert Panel", "Lower Playfield & Insert Panel"],
			[self.gis[address]["label"] for address in range(5)],
		)
		feeds = [self.gis[address]["wiring"]["power_connection"] for address in range(5)]
		returns = [self.gis[address]["wiring"]["control_connection"] for address in range(5)]
		self.assertEqual("J121-7 (Playfield)", feeds[0])
		self.assertEqual("J121-1 (Playfield)", returns[0])
		self.assertEqual("J121-11 (Playfield) / J119-1 (Cabinet)", feeds[4])
		self.assertEqual("J121-6 (Playfield) / J119-3 (Cabinet)", returns[4])
		self.assertEqual(["Q18", "Q10", "Q14", "Q16", "Q12"], [self.gis[address]["wiring"]["driver_transistor"] for address in range(5)])
		self.assertIn("J120-1/J120-7", self.gis[0]["physical"]["notes"])
		self.assertIn("J120-11/J120-6", self.gis[4]["physical"]["notes"])

	def test_lamp_bulbs_and_twin_sockets(self) -> None:
		for address in MATRIX_ADDRESSES - {87, 88}:
			physical = self.lamps[address]["physical"]
			expected = 2 if address in TWIN_BULB_LAMPS else 1
			self.assertEqual(expected, physical["quantity"], address)
			# No table object marks a lamp socket, so no lamp is placed.
			self.assertNotIn("spatial", self.lamps[address], address)
			self.assertRegex(physical["notes"], r"marks? no socket", address)
		for address in (87, 88):
			self.assertNotIn("quantity", self.lamps[address]["physical"])
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])
		self.assertIn("#86 (24-8829)", self.lamps[67]["physical"]["notes"])
		self.assertIn("#44 (24-6549)", self.lamps[66]["physical"]["notes"])
		self.assertIn("J137-5", self.lamps[41]["physical"]["notes"])

	def test_geometric_ordering(self) -> None:
		switch = {address: first_xy(device) for address, device in self.switches.items() if device["spatial"]["status"] != "not_applicable"}
		# D-I-G rollovers run left to right along the top.
		self.assertLess(switch[66][0], switch[67][0])
		self.assertLess(switch[67][0], switch[68][0])
		# B-E-D: B at the rear, D at the front. R-O-C-K: R at the rear left, K at the front right.
		self.assertLess(switch[47][1], switch[46][1])
		self.assertLess(switch[46][1], switch[45][1])
		self.assertLess(switch[41][0], switch[44][0])
		self.assertLess(switch[41][1], switch[44][1])
		# Side 3-bank targets: 51 upper, 53 lower, on both sides.
		for side in (0, 1):
			ys = [self.switches[address]["spatial"]["placements"][side]["y"] for address in (51, 52, 53)]
			self.assertEqual(sorted(ys), ys)
		self.assertLess(switch[63][0], switch[64][0])
		self.assertGreater(switch[65][1], switch[63][1])
		self.assertLess(switch[71][0], switch[72][0])
		self.assertLess(switch[73][0], switch[74][0])
		self.assertLess(first_xy(self.solenoids[47])[0], first_xy(self.solenoids[45])[0])
		self.assertLess(first_xy(self.solenoids[45])[0], first_xy(self.solenoids[33])[0])
		self.assertLess(first_xy(self.solenoids[33])[1], first_xy(self.solenoids[45])[1])

	def test_observed_and_unplaced_records_are_exactly_the_disclosed_ones(self) -> None:
		statuses = set()
		unplaced = set()
		ids = []
		for device in self.definition["inputs"] + self.definition["outputs"]:
			key = (device["binding"]["group"], device["binding"]["device"])
			spatial = device.get("spatial")
			if spatial is None:
				unplaced.add(key)
				continue
			if spatial["status"] == "not_applicable":
				continue
			statuses.add(spatial["status"])
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				self.assertEqual(round(placement["x"], 6), placement["x"])
				self.assertEqual(round(placement["y"], 6), placement["y"])
				self.assertEqual(spatial["status"], placement["provenance"]["status"])
		self.assertEqual({"observed"}, statuses)
		self.assertEqual(len(ids), len(set(ids)))
		expected = {("pinmame.output.solenoid", address) for address in PLAYFIELD_FLASHERS | {36}}
		expected |= {("pinmame.output.gi", address) for address in range(5)}
		expected |= {("pinmame.output.lamp", address) for address in MATRIX_ADDRESSES - {87, 88}}
		self.assertEqual(expected, unplaced)
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(sorted(({"group": group, "address": address} for group, address in expected), key=lambda item: (item["group"], item["address"])), report["unplaced_output_bindings"])
		self.assertEqual([], report["resolved_input_addresses"])
		self.assertEqual([], report["resolved_output_bindings"])
		self.assertEqual(len(ids), report["placement_count"])

	def test_projections_are_disclosed(self) -> None:
		trough = first_xy(self.solenoids[1])
		for address in (31, 32, 33, 34, 35):
			self.assertEqual(trough, first_xy(self.switches[address]))
			self.assertIn("Projected onto the trough exit kicker BallRelease", self.switches[address]["physical"]["notes"])
		for address, bank in ((5, (45, 46, 47)), (6, (41, 42, 43, 44))):
			xs = [first_xy(self.switches[number])[0] for number in bank]
			ys = [first_xy(self.switches[number])[1] for number in bank]
			mean = (sum(xs) / len(xs), sum(ys) / len(ys))
			x, y = first_xy(self.solenoids[address])
			self.assertAlmostEqual(mean[0], x, places=5)
			self.assertAlmostEqual(mean[1], y, places=5)
			self.assertIn("Projected to the mean", self.solenoids[address]["physical"]["notes"])

	def test_every_used_actuator_belongs_to_a_mechanism(self) -> None:
		actuators = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		driven = {device["id"] for device in self.solenoids.values() if device["kind"] in {"coil", "motor"} and device["availability"] == "used"}
		self.assertEqual(set(), driven - actuators)
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertEqual(set(), set(mechanism["actuators"] + mechanism["sensors"]) - ids, mechanism["id"])
		machine = self.mechanisms["mechanism.boulder-machine"]
		self.assertEqual((["device.boulder-machine-motor"], ["switch.matrix-76", "switch.matrix-25"]), (machine["actuators"], machine["sensors"]))

	def test_sources_carry_hashed_excerpts_without_local_paths(self) -> None:
		text = json.dumps(self.definition)
		self.assertNotIn("E:/", text)
		self.assertNotIn("C:\\", text)
		excerpt_paths = set()
		for source in self.sources.values():
			for excerpt in source.get("excerpts", []):
				excerpt_paths.add(excerpt["path"])
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["id"])
				if "image" in excerpt:
					excerpt_paths.add(excerpt["image"])
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["id"])
				self.assertTrue(excerpt["reviewed"])
		on_disk = {f"evidence/excerpts/{MACHINE_ID}/{path.name}" for path in EXCERPTS.iterdir()}
		self.assertEqual(on_disk, excerpt_paths)
		for source_id in ("manual.williams.the-flintstones.1994.operations-manual", "service-bulletin.williams.the-flintstones.16-9872", "service-bulletin.williams.the-flintstones.16-9876"):
			self.assertTrue(self.sources[source_id]["uri"].startswith("https://web.archive.org/web/"), source_id)

	def test_no_catalog_or_other_machine_identifier_leaks_into_the_artifacts(self) -> None:
		# The curator was modelled on another WPC-Security curator; forbid every other machine's
		# driver ids so inherited prose cannot survive unnoticed.
		catalog = load_json(CATALOG_PATH)
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID}
		artifacts = DEFINITION_PATH.read_text(encoding="utf-8") + KNOWLEDGE_PATH.read_text(encoding="utf-8") + SPATIAL_REPORT_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9]+_[a-z0-9]+", artifacts))
		self.assertEqual(set(), tokens & foreign)
		for word in ("Johnny", "Mnemonic", "Data Glove", "Cyber", "jm.c", "jmGameData"):
			self.assertNotIn(word, artifacts)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_the_flintstones as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curator.build())
		self.assertEqual(expected, canonical_bytes(curator.build()))
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())
		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_refuses_drift(self) -> None:
		import shutil
		import tempfile

		import curate_the_flintstones as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			drifted = root / DEFINITION_PATH.relative_to(ROOT)
			drifted.write_bytes(drifted.read_bytes().replace(b"Boulder Machine Motor", b"Boulder Machine Mot0r", 1))
			with self.assertRaises(RuntimeError):
				curator.check(root)
			shutil.copyfile(DEFINITION_PATH, drifted)
			stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(DEFINITION_PATH, stale)
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_pinned_pinmame_declares_the_mask_flippers_and_clones(self) -> None:
		checkout = pinned_pinmame_checkout()
		if checkout is None:
			self.skipTest("pinned PinMAME checkout is not available")
		text = (checkout / "src/wpc/sims/wpc/prelim/fs.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("{ 0x00, 0x00, 0x00, 0x3f, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}, /* inverted switches */", text)
		self.assertIn("FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR)", text)
		self.assertIn("GEN_WPCSECURITY, wpc_dispDMD,", text)
		self.assertNotIn("wpc_set_fastflip_addr", text)
		self.assertNotIn("handleMech", text)
		self.assertIn('CORE_GAMEDEF(fs,lx5,"Flintstones, The (LX-5)",1994,"Williams",wpc_mSecurityS,0)', text)
		clones = set(re.findall(r"(?m)^CORE_CLONEDEF\(fs,(\w+),lx5,\"[^\"]*\",1994,\"Williams\",wpc_mSecurityS,0\)", text))
		self.assertEqual({identifier[3:] for identifier in COMPATIBILITY} - {"lx5"}, clones)
		self.assertIn("// Prototype Sound ??", text)
		for define in ("#define swTroughJam\t31", "#define swTrough1\t32", "#define swLeftJet\t63", "#define swRightJet\t64", "#define swBottomJet\t65", "#define sLeftJet\t11", "#define sBottomJet\t12", "#define sRightJet\t13"):
			self.assertIn(define, text)
		wpc = (checkout / "src/wpc/wpc.c").read_text(encoding="utf-8", errors="replace")
		self.assertIn("core_set_pwm_output_type(CORE_MODOUT_SOL0 + 17 - 1, 6, CORE_MODOUT_BULB_89_20V_DC_WPC);", wpc)
		self.assertIn("core_set_pwm_output_type(CORE_MODOUT_SOL0 + 24 - 1, 5, CORE_MODOUT_BULB_89_20V_DC_WPC);", wpc)
		self.assertIn("coreGlobals.swMatrix[2] |= 0x08; /* Always closed switch */", wpc)


class TheFlintstonesRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_the_flintstones as curator

		curator.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_lamp_lights_draw_no_bulb_so_no_lamp_is_placed(self) -> None:
		import curate_the_flintstones as curator

		extraction = self._root("PINMAME_VPX_SOURCES_ROOT") / "williams" / "the-flintstones-1994" / "extracted-vpxtool"
		lamps_collection = next(item["items"] for item in load_json(extraction / "collections.json") if item["name"] == "Lamps")
		definition = load_json(DEFINITION_PATH)
		lamps = by_address(definition, "outputs", "pinmame.output.lamp")
		unplaced = {address: device for address, device in lamps.items() if address not in {87, 88}}
		for address, device in sorted(unplaced.items()):
			self.assertNotIn("spatial", device, address)
			for name in curator.lamp_bulb_objects(address):
				light = load_json(extraction / "gameitems" / f"Light.{name}.json")["Light"]
				# The light the script binds is a bulb-mode light that shows no bulb mesh, so it marks no socket.
				self.assertTrue(light["is_bulb_light"], name)
				self.assertFalse(light["show_bulb_mesh"], name)
				self.assertEqual("", light["image"], name)
				self.assertIn(name, lamps_collection)
				self.assertEqual(address, int(name[2:4]))
				self.assertIn(name, device["physical"]["notes"])
		# The overlay each single-bulb lamp is bound beside is a classic light that draws the insert image.
		self.assertFalse(load_json(extraction / "gameitems" / "Light.LT11.json")["Light"]["is_bulb_light"])

	def test_retained_table_and_script_hashes_and_claims(self) -> None:
		import curate_the_flintstones as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "williams" / "the-flintstones-1994"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "source" / "The Flintstones (Williams 1994) v1.25.7.vpx").read_bytes()).hexdigest())
		script = (root / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script).hexdigest())
		text = script.decode("latin-1")
		# Claims the definition makes about the script, checked against the script itself.
		for claim in (
			'Const cGameName = "fs_lx5"',
			"Const UseSolenoids=2",
			"Const UseLamps=0,UseGI=1,",
			"Const UseVPMModSol=1",
			'LoadVPM "01560000", "WPC.VBS", 3.26',
			".Switch(22) = 1",
			".Switch(24) = 1",
			"vpmNudge.TiltSwitch = 14",
			".InitSwitches Array(32, 33, 34, 35)",
			"Set bsKicker36 = New cvpmSaucer",
			".InitTurnTable ttMachineTrigger, 32",
			".SpinCW = True",
			"vpmTimer.PulseSw 31",
			'SolCallback(1) = "SolRelease"',
			'SolCallback(3) = "SolTopDiverter"',
			'SolCallback(4) = "bsKicker36.SolOut"',
			'SolCallback(8) = "SolBrontoDiverter"',
			'SolCallback(14) = "SetLamp 114,"',
			'SolCallback(16) = "SolRightApronDiverter"',
			'SolModCallback(17) = "FadeLights.LampMod 117,"',
			'SolCallback(23) = "SolMachine"',
			'SolModCallback(24) = "FadeLights.LampMod 124,"',
			'SolCallback(26) = ""',
			'SolCallback(27) = ""',
			'SolCallback(35) = "SolGateRGate"',
			'SolCallback(36) = "SolGateLGate"',
			'SolCallback(sLRFlipper) = "SolRFlipper"',
			"id = cInt(mid(lightobj.Name,3, 2))",
			"If keycode = PlungerKey Then Controller.Switch(11) = 1",
			"If keycode = keyFront Then Controller.Switch(23) = 1",
		):
			self.assertIn(claim, text)
		self.assertNotRegex(text, r"(?m)^\s*SolCallback\((11|12|13)\)")

	def test_retained_manual_and_bulletin_hashes(self) -> None:
		import curate_the_flintstones as curator

		root = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / MACHINE_ID / "ipdb-888"
		for name, digest in (
			(curator.MANUAL_NAME, curator.MANUAL_SHA256),
			("Williams_1994_The_Flintstones_Ball_Hang_up_Correction_Instructions_August_4_1994.pdf", curator.HANGUP_SHA256),
			("Williams_1994_The_Flintstones_Manual_Amendment_Page_2_24_Correction_August_10_1994.pdf", curator.AMENDMENT_SHA256),
		):
			self.assertEqual(digest, hashlib.sha256((root / name).read_bytes()).hexdigest(), name)

	def test_retained_rom_decode_matches_the_excerpt_identity(self) -> None:
		import curate_the_flintstones as curator

		decoded = load_json(self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "the-flintstones-1994" / "rom-name-tables.json")
		self.assertEqual(["fs_lx5", "fs_lx4", "fs_lx2", "fs_sp2"], list(decoded))
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, decoded["fs_lx5"]["rom_archive_sha256"])
		import flintstones_rom_name_tables

		self.assertEqual(flintstones_rom_name_tables.render_markdown(decoded), (EXCERPTS / "rom-name-tables.md").read_text(encoding="utf-8"))

	def test_rom_name_table_excerpt_matches_the_rom(self) -> None:
		import curate_the_flintstones as curator
		import flintstones_rom_name_tables

		roms = self._root("PINMAME_ROM_LIBRARY_ROOT")
		archives = {name: roms / f"{name}.zip" for name in flintstones_rom_name_tables.SETS}
		if not all(path.is_file() for path in archives.values()):
			self.skipTest("the Flintstones ROM sets are not all in this ROM library")
		results = {name: flintstones_rom_name_tables.decode_set(path) for name, path in archives.items()}
		self.assertEqual(curator.ROM_ARCHIVE_SHA256, results["fs_lx5"]["rom_archive_sha256"])
		self.assertEqual(flintstones_rom_name_tables.render_markdown(results), (EXCERPTS / "rom-name-tables.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
	unittest.main()
