from __future__ import annotations

import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_against_schema, validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import blackout_runtime_evidence as runtime_evidence  # noqa: E402
import curate_blackout as curator  # noqa: E402

EXCERPTS = ROOT / "evidence/excerpts" / curator.MACHINE_ID
ROOT_VARIABLES = ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT",
	"PINMAME_SOURCE_ROOT", "PINMAME_VPX_SCRIPTS_ROOT", "PINMAME_ROM_LIBRARY_ROOT"]


def tempdir():
	return tempfile.TemporaryDirectory(dir=os.environ.get("PINMAME_TEST_TMP_ROOT"))


def table_after(name: str, heading: str) -> list[list[str]]:
	"""Body rows of the first Markdown table after ``heading`` in an excerpt."""
	lines = (EXCERPTS / name).read_text(encoding="utf-8").splitlines()
	start = lines.index(heading)
	rows: list[list[str]] = []
	for line in lines[start + 1:]:
		if line.startswith("|"):
			cells = [c.strip() for c in line.strip("|").split("|")]
			if not set(cells[0]) <= {"-"}:
				rows.append(cells)
		elif rows:
			break
	return rows[1:]


def headers(name: str, prefix: str) -> list[str]:
	"""Wire colours of a `Column headers ...:` or `Row headers ...:` line, in printed order."""
	line = next(l for l in (EXCERPTS / name).read_text(encoding="utf-8").splitlines() if l.startswith(prefix))
	return [item.strip().split(" ", 1)[1] for item in line.split(":", 1)[1].rstrip(".").split(",")]


def matrix_cells(name: str, heading: str) -> dict[int, str]:
	cells = {}
	for row in table_after(name, heading):
		for cell in row[1:]:
			number, label = cell.split(" ", 1)
			cells[int(number)] = label
	return cells


class BlackoutCurationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.game = curator.build()
		by_group = lambda group, key: {d["binding"]["device"]: d for d in cls.game[key] if d["binding"]["group"] == group}
		cls.switches = by_group("pinmame.input.switch", "inputs")
		cls.dips = by_group("pinmame.input.dip", "inputs")
		cls.coils = by_group("pinmame.output.solenoid", "outputs")
		cls.lamps = by_group("pinmame.output.lamp", "outputs")
		cls.ids = {d["id"] for key in ["inputs", "outputs"] for d in cls.game[key]}

	def test_identity_six_drivers_and_catalog_claim(self):
		identity = {k: v for k, v in self.game["machine"].items() if k != "playfield"}
		self.assertEqual(identity, {"id": "williams.blackout.1980", "name": "Blackout", "manufacturer": "Williams", "year": 1980,
			"model_number": "495", "kind": "physical_pinball", "ipdb_id": 317, "opdb_id": "GRwYo-MQoPw"})
		drivers = {d["id"]: d for d in self.game["drivers"]}
		self.assertEqual(set(drivers), {"blkou_l1", "blkou_l1ff", "blkou_f1", "blkou_f1ff", "blkou_t1", "blkou_t1ff"})
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in drivers.values()))
		self.assertNotIn("clone_of", drivers["blkou_l1"])
		self.assertTrue(all(d["clone_of"] == "blkou_l1" for k, d in drivers.items() if k != "blkou_l1"))
		self.assertEqual(self.game["controller"], {"platform": "pinmame.system-6", "hardware_generation": "0x20000", "inversion_applied_by_emulator": True})
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claims = [m for m in catalog["machines"] if m["id"] == curator.MACHINE_ID]
		self.assertEqual(len(claims), 1)
		self.assertEqual(claims[0]["definition"], curator.DEFINITION.as_posix())
		self.assertEqual(claims[0]["missing"], ["spatial_placement"])
		self.assertEqual(claims[0]["completion_score"], 94)
		self.assertEqual({d["id"] for d in catalog["drivers"] if d["machine_id"] == curator.MACHINE_ID}, set(drivers))
		# blkou_hf.zip in a ROM library is a copy of blkou_l1, not a pinned driver.
		self.assertEqual([d for d in catalog["drivers"] if d["id"] == "blkou_hf"], [])
		for directory in ["author-ready", "stubs"]:
			self.assertEqual(list((ROOT / "machines" / directory).glob("**/blackout*")), [])

	def test_every_legal_address_has_a_disposition(self):
		self.assertEqual(set(self.switches), {*range(-7, -2), *range(1, 65), *range(81, 89)})
		self.assertEqual(set(self.dips), {1, 2, *range(9, 25)})
		self.assertEqual(set(self.lamps), set(range(1, 65)))
		self.assertEqual(set(self.coils), {*range(1, 24), *range(45, 49)})
		availability = lambda devices, n: (devices[n]["kind"], devices[n]["availability"])
		for n in range(-7, -2):
			self.assertEqual(availability(self.switches, n), ("switch", "used"), n)
		unused = {16, 17, 24, *range(47, 65)}
		for n in range(1, 65):
			expected = ("virtual", "used") if n == 46 else ("switch", "unused" if n in unused else "used")
			self.assertEqual(availability(self.switches, n), expected, n)
			if n in unused:
				self.assertEqual(self.switches[n]["spatial"]["reason"], "unused")
		for n in range(81, 89):
			self.assertEqual(availability(self.switches, n), ("virtual", "used" if n in {82, 84} else "unused"), n)
		self.assertEqual((self.switches[82]["roles"], self.switches[84]["roles"]), (["flipper.lower.right.button"], ["flipper.lower.left.button"]))
		used_dips = {1, 2, 17, 18, 19}
		for n in self.dips:
			self.assertEqual(availability(self.dips, n), ("dip_switch", "used" if n in used_dips else "unused"), n)
		for n in range(1, 65):
			self.assertEqual(availability(self.lamps, n), ("lamp", "unused" if n == 11 else "used"), n)
		kinds = {n: availability(self.coils, n) for n in self.coils}
		self.assertEqual({n for n, k in kinds.items() if k == ("coil", "unused")}, {2, 3, 7, 8, 22})
		self.assertEqual({n for n, k in kinds.items() if k == ("coil", "used")}, {1, 4, 5, 6, 14, 16, 17, 18, 19, 20, 21})
		self.assertEqual({n for n, k in kinds.items() if k == ("control_signal", "used")}, set(range(9, 14)))
		self.assertEqual({n for n, k in kinds.items() if k == ("relay", "used")}, {15, 23})
		self.assertEqual({n for n, k in kinds.items() if k == ("virtual", "used")}, set(range(45, 49)))

	def test_switch_wiring_and_names_follow_figure_5(self):
		columns = headers("switch-matrix.md", "Column headers")
		rows = headers("switch-matrix.md", "Row headers")
		column_pins = {int(r[3].split()[1]): int(r[1]) for r in table_after("switch-matrix.md", "Columns, 2J2/2P2 to 8P1/8J1:") if r[3].startswith("COLUMN")}
		column_pins[1] = 9  # cabinet sheet: column 1 GRN-BRN from 2J2/2P2-9
		self.assertIn("Column 1: GRN-BRN from 2J2/2P2-9", (EXCERPTS / "switch-matrix.md").read_text(encoding="utf-8"))
		row_pins = {int(r[3].split()[1]): int(r[1]) for r in table_after("switch-matrix.md", "Rows, 2J3/2P3 to 8P1:")}
		self.assertEqual((len(column_pins), len(row_pins)), (6, 8))
		cells = matrix_cells("switch-matrix.md", "## Figure 5. Switch Matrix (booklet, printed page 11)")
		self.assertEqual(len(cells), 64)
		for n in range(1, 65):
			col, row = divmod(n - 1, 8)
			if n == 46:
				self.assertNotIn("wiring", self.switches[n])
				self.assertIn("8SW46", self.switches[n]["physical"]["notes"])
				continue
			wiring = self.switches[n]["wiring"]
			self.assertEqual((wiring["drive_wire"], wiring["return_wire"]), (columns[col], rows[row]), n)
			self.assertEqual(wiring["return_connection"], f"2J3-{row_pins[row + 1]}", n)
			if col + 1 in column_pins:
				self.assertEqual(wiring["drive_connection"], f"2J2-{column_pins[col + 1]}", n)
			printed = cells[n]
			label = self.switches[n]["label"]
			if printed == "NOT USED":
				self.assertEqual(self.switches[n]["availability"], "unused", n)
			elif n == 15:
				self.assertEqual(label, "Green Target #5 (Top)")
				self.assertIn("5 BANK #5 (TOP)", self.switches[n]["physical"]["notes"])
			else:
				self.assertEqual(label.upper().replace(" 10", ""), printed.replace(" 10", ""), n)
		self.assertIn("8SW39", self.switches[39]["physical"]["notes"])

	def test_lamp_wiring_and_names_follow_figure_6(self):
		columns = headers("lamp-matrix.md", "Column headers")
		rows = headers("lamp-matrix.md", "Row headers")
		column_pins = {int(r[3].split()[1]): int(r[1]) for r in table_after("lamp-wiring.md", "Columns, 2J5/2P5 to 8P2/8J2:")}
		row_pins = {int(r[3].split()[1]): int(r[1]) for r in table_after("lamp-wiring.md", "Rows, 2J7/2P7 to 8P2:")}
		self.assertEqual((len(column_pins), len(row_pins)), (7, 8))
		cells = matrix_cells("lamp-matrix.md", "Each cell prints its lamp number and name; all 64 cells, column by column:")
		self.assertEqual(len(cells), 64)
		for n in range(1, 65):
			col, row = divmod(n - 1, 8)
			wiring = self.lamps[n]["wiring"]
			self.assertEqual((wiring["drive_wire"], wiring["return_wire"]), (columns[col], rows[row]), n)
			self.assertEqual(wiring["return_connection"], f"2J7-{row_pins[row + 1]}", n)
			if col < 7:
				self.assertEqual(wiring["drive_connection"], f"2J5-{column_pins[col + 1]}", n)
			else:
				self.assertTrue(wiring["drive_connection"].startswith("9J1-7"), n)
		self.assertEqual(cells[11], "NOT USED")
		self.assertEqual(self.lamps[11]["spatial"]["reason"], "unused")
		self.assertEqual(self.lamps[23]["label"], "Center 3 Bank Arrow (Center)")
		self.assertEqual(self.lamps[24]["label"], "Center 3 Bank Arrow (Right)")
		insert = {(r[1].strip('"'), int(r[3].split(",")[0])) for r in table_after("insert-board.md", "Lamps, each through its own series diode to its row; the column is the vertical bus the lamp's line joins:")}
		self.assertEqual(len(insert), 14)
		for n in curator.BACKBOX_LAMPS:
			lamp = self.lamps[n]
			name, bulbs = curator.INSERT_BOARD[n]
			self.assertIn((name, bulbs), insert, n)
			self.assertEqual((lamp["roles"], lamp["physical"]["location"], lamp["physical"]["quantity"]), (["cabinet.backglass"], "backbox insert board", bulbs), n)
			self.assertEqual(lamp["spatial"]["reason"], "cabinet_or_service")
		self.assertEqual({n for n in curator.BACKBOX_LAMPS if self.lamps[n]["physical"]["quantity"] == 2}, {62, 63, 64})
		for n in [*range(1, 11), *range(12, 50), 56]:
			self.assertEqual((self.lamps[n]["physical"]["location"], self.lamps[n]["physical"]["quantity"]), ("playfield", 1), n)

	def test_solenoid_wiring_follows_table_3(self):
		printed = {}
		for number, function, wire, connections, transistor, part in table_after("solenoid-connections.md", "## Table 3. Solenoid Connections (booklet, printed page 9)"):
			if number == "*":
				continue
			printed[int(number.lstrip("*"))] = (function, wire, connections, transistor, part)
		self.assertEqual(set(printed), set(range(1, 23)))
		for n, (function, wire, connections, transistor, part) in printed.items():
			coil = self.coils[n]
			wiring = coil["wiring"]
			self.assertEqual((wiring["drive_wire"], wiring["drive_connection"], wiring["driver_transistor"]), (wire, connections, transistor), n)
			if function == "Not Used":
				self.assertEqual((coil["id"], coil["availability"]), (f"solenoid.not-used-{n}", "unused"), n)
			elif function == "Sound":
				self.assertEqual(coil["label"], f"Sound Line {n - 8}")
				self.assertNotIn("part_number", coil["physical"])
			else:
				self.assertEqual((coil["label"], coil["physical"]["part_number"]), (function, part), n)
		self.assertEqual((self.coils[14]["roles"], self.coils[16]["roles"], self.coils[15]["roles"]),
			(["cabinet.knocker"], ["cabinet.coin-lockout"], ["cabinet.general-illumination-relay"]))
		self.assertIn("6T1-19", self.coils[15]["physical"]["notes"])
		self.assertEqual((self.coils[23]["roles"], self.coils[23]["spatial"]["reason"]), (["cabinet.flipper-enable-relay"], "internal_nonvisual"))
		for n in range(45, 49):
			self.assertIn("8L25 RIGHT FLIPPER", self.coils[n]["physical"]["notes"])
		notes = (EXCERPTS / "solenoid-connections.md").read_text(encoding="utf-8")
		for n, (wire, pins, _) in curator.SPECIAL_WIRING.items():
			self.assertIn(f"{n} - {wire} - {pins}", notes)
			self.assertIn(f"{wire} {pins}", self.coils[n]["physical"]["notes"])

	def test_sound_dips_follow_the_sound_board_drawing(self):
		# DS1 position 2 reaches IC10 PB5 and position 1 reaches PB6; an ON switch grounds its line; wmssnd.c puts DIP 1/2 uninverted on PB5/PB6.
		text = (EXCERPTS / "sound-board.md").read_text(encoding="utf-8")
		self.assertIn("| 1 | PB5 | 2 | ON: speech enabled | OFF: speech inhibited | 0, speech enabled |", text)
		self.assertIn("| 2 | PB6 | 1 | ON: musical notes | OFF: synthesized sounds | 1, synthesized sounds |", text)
		self.assertIn("s67slocals.sndCmd = (data & 0x1f) | (core_getDip(0)<<5);", text)
		speech, select = self.dips[1], self.dips[2]
		self.assertEqual((speech["id"], speech["label"]), ("dip.sound-board-ds1-switch-2-speech", "Sound Board DS1 Switch 2 - Speech Enable"))
		self.assertEqual((select["id"], select["label"]), ("dip.sound-board-ds1-switch-1-sound-select", "Sound Board DS1 Switch 1 - Sound Select"))
		self.assertIn("PB5", speech["physical"]["notes"])
		self.assertIn("public 0 is ON, speech enabled and public 1 is OFF, speech inhibited", speech["physical"]["notes"])
		self.assertIn("PB6", select["physical"]["notes"])
		self.assertIn("public 0 is ON, musical notes and public 1 is OFF, synthesized sounds", select["physical"]["notes"])
		self.assertNotIn("by number", curator.KNOWLEDGE_TEXT)
		sources = {s["id"]: s for s in self.game["sources"]}
		crop = next(e for e in sources[curator.DRAWINGS]["excerpts"] if e["path"].endswith("/sound-board.md"))
		self.assertEqual(crop["image"], f"evidence/excerpts/{curator.MACHINE_ID}/sound-board-ds1.webp")
		self.assertTrue(crop["image_derivation"].startswith("Williams_1980_Blackout_Manual_with_paginated_schematics.pdf page 13, crop box"))

	def test_service_test_pairs_every_printed_solenoid_with_its_public_address(self):
		mapping = load_json(ROOT / curator.RUNTIME)["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({int(k): v for k, v in mapping.items()}, {n: n for n in range(1, 23)})

	def test_polarity_and_switch_types(self):
		for n, d in self.switches.items():
			if "normally_closed" in d:
				self.assertIs(d["normally_closed"], False, n)
		fitted = [n for n in range(1, 46) if n not in {16, 17, 24}]
		for n in [*range(-7, -2), *fitted]:
			self.assertIs(self.switches[n]["normally_closed"], False, n)
		types = {n: self.switches[n]["physical"].get("switch_type") for n in fitted}
		self.assertEqual({n: t for n, t in types.items() if t}, {1: "tilt", 2: "tilt", 3: "button", 7: "tilt", 8: "button", 32: "tilt"})
		for n in [25, 26, 27, 33, 34, 35]:
			self.assertIn("Closed while the target is down", self.switches[n]["physical"]["notes"])

	def test_specials_relationships_mechanisms_and_displays(self):
		relationships = {(r["source"], r["destination"]) for r in self.game["relationships"]}
		expected = {(self.switches[s]["id"], self.coils[c]["id"]) for c, s in curator.SPECIAL_SWITCHES.items()}
		expected.add((self.switches[82]["id"], self.switches[46]["id"]))
		self.assertEqual(relationships, expected)
		self.assertEqual(curator.SPECIAL_SWITCHES, {17: 22, 18: 21, 19: 23, 20: 44, 21: 43})
		mechanisms = {m["id"]: m for m in self.game["mechanisms"]}
		self.assertEqual(len(mechanisms), 13)
		for m in mechanisms.values():
			self.assertTrue(set(m["actuators"]) | set(m["sensors"]) <= self.ids, m["id"])
		self.assertEqual(mechanisms["mech.center-3-bank"]["actuators"], [self.coils[4]["id"]])
		self.assertEqual(set(mechanisms["mech.center-3-bank"]["sensors"]), {self.switches[n]["id"] for n in (25, 26, 27, 28)})
		self.assertEqual(set(mechanisms["mech.top-3-bank"]["sensors"]), {self.switches[n]["id"] for n in (33, 34, 35, 36)})
		self.assertEqual(mechanisms["mech.blackout-general-illumination"]["actuators"], [self.coils[15]["id"]])
		self.assertEqual([(d["controller_index"], d["segment_start"], d["width"]) for d in self.game["displays"]],
			[(0, 0, 6), (1, 8, 6), (2, 20, 6), (3, 28, 6), (4, 14, 2), (5, 6, 2)])
		self.assertEqual(self.game["conflicts"], [])

	def test_sources_excerpts_and_schema(self):
		curator.verify_files()
		self.assertEqual(validate_against_schema(self.game, ROOT / "schemas/machine.schema.json", "game"), [])
		self.assertEqual(validate_machine(self.game, ROOT), [])
		self.assertEqual(validate_against_schema(load_json(ROOT / curator.RUNTIME), ROOT / "schemas/evidence.schema.json", "runtime"), [])
		sources = {s["id"]: s for s in self.game["sources"]}
		for identifier, revision in [(curator.MANUAL, "16P-495-103"), (curator.DRAWINGS, "16P-495-101")]:
			self.assertEqual((sources[identifier]["kind"], sources[identifier]["revision"]), ("manual", revision))
			self.assertIn("web.archive.org", sources[identifier]["locator"])
		excerpts = [e for s in sources.values() for e in s.get("excerpts", [])]
		self.assertEqual({Path(e["path"]).name for e in excerpts}, set(curator.EXCERPTS))
		for e in excerpts:
			self.assertEqual(e["method"], "manual")
			self.assertTrue(e["transcribed_by"].startswith("curator; "))
			self.assertIn(e["transcribed_by"], {"curator; native page images read visually", "curator; source text and data files read directly"})
			self.assertEqual(e["reviewed"], Path(e["path"]).name not in curator.UNREVIEWED)
		for identifier in [curator.SCRIPT, curator.MOD_SCRIPT]:
			self.assertIs(sources[identifier]["known_working"], True)
			self.assertTrue(sources[identifier]["uri"].startswith(f"https://github.com/sverrewl/vpxtable_scripts/blob/{curator.SCRIPT_REVISION}/Blackout%20%28Williams%201980%29"))
		self.assertIs(sources[curator.EMBEDDED]["known_working"], False)
		self.assertEqual(sources[curator.RUN]["sha256"], curator.RUNTIME_SHA)
		self.assertEqual([identifier for identifier, source in sources.items() if not source.get("acquired_at")], [])
		self.assertEqual(sources[curator.SOURCE]["acquired_at"], curator.REVISION_COMMITTED)
		self.assertEqual(sources[curator.SCRIPT]["acquired_at"], curator.SCRIPT_REVISION_COMMITTED)
		self.assertEqual(sources[curator.EMBEDDED]["acquired_at"], curator.EXTRACTED)
		self.assertEqual(sources[curator.RUN]["acquired_at"], curator.RUN_PERSISTED)

	def test_partial_gate_names_only_spatial_placement(self):
		self.assertEqual(self.game["coverage"]["status"], "partial")
		self.assertEqual(self.game["coverage"]["missing"], ["spatial_placement"])
		self.assertEqual(self.game["coverage"]["dimensions"]["spatial_placement"], "observed")
		report = curator.spatial.report(self.game, ROOT)
		unplaced = set(report["unplaced_devices"])
		self.assertTrue({self.lamps[n]["id"] for n in [*range(1, 11), *range(12, 50), 56]} <= unplaced)
		self.assertTrue({self.switches[n]["id"] for n in (9, 19, 32, 38)} | {self.coils[1]["id"]} <= unplaced)
		for group in ["inputs", "outputs"]:
			for d in self.game[group]:
				spatial = d.get("spatial")
				if spatial is None:
					self.assertIn(d["id"], unplaced)
				elif spatial["status"] != "not_applicable":
					self.assertTrue(spatial.get("placements"), d["id"])
					self.assertNotIn(d["id"], unplaced)
		placed = [d for key in ["inputs", "outputs"] for d in self.game[key] if d.get("spatial", {}).get("placements")]
		self.assertEqual(len(placed), 38)
		self.assertTrue(all(p["provenance"]["status"] == "observed" for d in placed for p in d["spatial"]["placements"]))
		promoted = copy.deepcopy(self.game)
		promoted["coverage"]["status"] = "author_ready"
		promoted["coverage"]["missing"] = []
		self.assertTrue(any("spatial" in e for e in validate_machine(promoted, ROOT)))
		self.assertIn("## What would complete this record", curator.KNOWLEDGE_TEXT)

	def _fixture(self, destination: Path) -> None:
		files = [*curator.expected_artifacts(), curator.RUNTIME, curator.READINGS, curator.spatial.SEED]
		files += [Path("evidence/excerpts") / curator.MACHINE_ID / n for n in [*curator.EXCERPTS, *(i[0] for i in curator.IMAGES.values())]]
		files += [Path(r["scenario_path"]) for r in load_json(ROOT / curator.RUNTIME)["runtime"]["raw_runs"]]
		for rel in files:
			(destination / rel).parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(ROOT / rel, destination / rel)

	def test_determinism_and_local_guards(self):
		curator.check()
		self.assertEqual((ROOT / curator.SEED).read_bytes(), (ROOT / curator.DEFINITION).read_bytes())
		with tempdir() as t, patch.dict(os.environ, {}, clear=True):
			root = Path(t)
			self._fixture(root)
			before = curator.expected_artifacts(root)
			curator.regenerate(root)
			curator.regenerate(root)
			curator.check(root)
			self.assertEqual(before, curator.expected_artifacts(root))
			for rel in [curator.DEFINITION, curator.SEED, curator.KNOWLEDGE, curator.REPORT, curator.REPORT_MD]:
				original = (root / rel).read_bytes()
				(root / rel).write_bytes(original + b"drift")
				with self.assertRaisesRegex(RuntimeError, "drift"):
					curator.check(root)
				(root / rel).write_bytes(original)
			guarded = [curator.RUNTIME, curator.READINGS, curator.spatial.SEED]
			guarded += [Path("evidence/excerpts") / curator.MACHINE_ID / n for n in [*curator.EXCERPTS, *(i[0] for i in curator.IMAGES.values())]]
			guarded += [Path(r["scenario_path"]) for r in load_json(ROOT / curator.RUNTIME)["runtime"]["raw_runs"]]
			for rel in guarded:
				original = (root / rel).read_bytes()
				(root / rel).write_bytes(original + b"changed")
				with self.assertRaises(RuntimeError, msg=str(rel)):
					curator.check(root)
				(root / rel).write_bytes(original)
			promoted = copy.deepcopy(self.game)
			promoted["coverage"]["status"] = "author_ready"
			(root / curator.DEFINITION).write_bytes(canonical_bytes(promoted))
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.regenerate(root)
			(root / curator.DEFINITION).write_bytes(canonical_bytes(self.game))
			stale = root / "machines/author-ready/williams/blackout-1980.json"
			stale.parent.mkdir(parents=True)
			stale.write_text("{}")
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.check(root)

	def test_missing_local_evidence_is_refused(self):
		with tempdir() as t:
			root = Path(t)
			self._fixture(root)
			(root / curator.RUNTIME).unlink()
			with self.assertRaisesRegex(RuntimeError, "runtime evidence absent"):
				curator.check(root)

	def test_configured_but_missing_external_root_fails(self):
		for name in ROOT_VARIABLES:
			with self.subTest(root=name), patch.dict(os.environ, {name: ""}, clear=True):
				with self.assertRaisesRegex(RuntimeError, "configured evidence root unavailable"):
					curator.verify_external()

	def test_unconfigured_external_roots_are_skipped(self):
		with patch.dict(os.environ, {}, clear=True):
			curator.verify_external()

	def test_external_guards_reject_changed_or_missing_files(self):
		for variable, names in [("PINMAME_SOURCE_ROOT", list(curator.SOURCE_FILES)), ("PINMAME_VPX_SCRIPTS_ROOT", [n for n, _ in curator.SCRIPT_FILES.values()])]:
			with self.subTest(variable=variable), tempdir() as t:
				for name in names:
					path = Path(t) / name
					path.parent.mkdir(parents=True, exist_ok=True)
					path.write_bytes(b"wrong artifact")
				with patch.dict(os.environ, {variable: t}, clear=True):
					with self.assertRaisesRegex(RuntimeError, "absent or changed"):
						curator.verify_external()
		for variable, message in [("PINMAME_MANUALS_ROOT", "retained document absent"), ("PINMAME_ROM_LIBRARY_ROOT", "ROM archive absent"),
				("PINMAME_REVIEW_ARTIFACTS_ROOT", "harness directory manifest absent"), ("PINMAME_VPX_SOURCES_ROOT", "spatial VPX absent")]:
			with self.subTest(variable=variable), tempdir() as t, patch.dict(os.environ, {variable: t}, clear=True):
				with self.assertRaisesRegex(RuntimeError, message):
					curator.verify_external()


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime root not configured")
class BlackoutRetainedEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.review = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		cls.runs = {name: load_json(cls.review / runtime_evidence.HARNESS / f"{name}.json") for name in runtime_evidence.SCENARIOS}

	def test_exact_retained_evidence(self):
		curator.verify_external()
		runtime_evidence.check(self.review, ROOT)

	def _loader(self, mutate):
		runs = copy.deepcopy(self.runs)
		mutate(runs)
		return lambda name: runs[name]

	def test_substituted_display_frame_is_refused(self):
		pin = load_json(ROOT / curator.READINGS)["frames"][0]

		def mutate(runs):
			display = next(d for d in runs[pin["run"]]["snapshots"][pin["snapshot"]]["displays"] if d["index"] == pin["display_index"])
			display["segments"] = [v ^ 0x01 for v in display["segments"]]

		with self.assertRaisesRegex(RuntimeError, "raw frame differs"):
			runtime_evidence.build(self.review, ROOT, self._loader(mutate))

	def test_reordered_scenario_step_is_refused(self):
		def mutate(runs):
			runs["play"]["steps"][0]["label"] = "another action"

		with self.assertRaisesRegex(RuntimeError, "differs from its scenario action"):
			runtime_evidence.build(self.review, ROOT, self._loader(mutate))


if __name__ == "__main__":
	unittest.main()
