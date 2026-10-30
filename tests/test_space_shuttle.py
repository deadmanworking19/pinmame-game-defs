"""Space Shuttle's semantic, provenance, runtime and promotion gates."""
from __future__ import annotations

import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine
from pinmame_game_defs.conflicts import unresolved_conflicts
import curate_space_shuttle as curator
import space_shuttle_data as data
import summarize_space_shuttle_runtime as summary

MACHINE_ID = "williams.space-shuttle.1984"
DRIVERS = {"sshtl_l7", "sshtl_l3"}
UNUSED_SWITCHES = set(range(50, 65))
UNUSED_SOLENOIDS = {12, 22}


def _roots() -> dict[str, Path] | None:
	names = ("PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_VPX_SOURCES_ROOT")
	if any(not os.environ.get(n) for n in names):
		return None
	return {n: Path(os.environ[n]) for n in names}


class SpaceShuttleTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		path = curator.AUTHOR_READY if (ROOT / curator.AUTHOR_READY).exists() else curator.DEFINITION
		cls.definition = load_json(ROOT / path)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.dip"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.sources = {s["id"]: s for s in cls.definition["sources"]}
		cls.runtime = load_json(ROOT / curator.RUNTIME)

	def test_identity_drivers_catalog_and_no_stale_stub(self):
		m = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "Space Shuttle", "Williams", 1984, "535", 2260, "G4q3L-MKN50"),
		                 (m["id"], m["name"], m["manufacturer"], m["year"], m["model_number"], m["ipdb_id"], m["opdb_id"]))
		self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
		by_id = {d["id"]: d for d in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["sshtl_l7"])
		self.assertEqual("sshtl_l7", by_id["sshtl_l3"]["clone_of"])
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in by_id.values()))
		self.assertEqual({"platform": "pinmame.system-11", "hardware_generation": "0x800", "inversion_applied_by_emulator": True}, self.definition["controller"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVERS, {d["id"] for d in catalog["drivers"] if d.get("machine_id") == MACHINE_ID})
		self.assertFalse(any("sshtlzac" in d["id"] for d in self.definition["drivers"]))
		for path in (ROOT / "machines/stubs").rglob("*.json"):
			self.assertFalse(DRIVERS & {d["id"] for d in load_json(path)["drivers"]}, path)

	def test_full_address_enumeration(self):
		self.assertEqual({-7, -6, -5, -4, *range(1, 65), *range(81, 89)}, set(self.switches))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual(set(range(1, 65)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual(UNUSED_SWITCHES, {a for a in range(1, 65) if self.switches[a]["availability"] == "unused"})
		self.assertEqual({5}, {a for a in range(1, 65) if self.switches[a]["availability"] == "optional"})
		self.assertEqual({81, 83, 85, 86, 87, 88}, {a for a in range(81, 89) if self.switches[a]["availability"] == "unused"})
		for address in set(range(1, 65)) - UNUSED_SWITCHES:
			self.assertIs(False, self.switches[address]["normally_closed"], address)
		self.assertTrue(all(lamp["availability"] == "used" for lamp in self.lamps.values()))

	def test_switch_names_wiring_and_flipper_copy(self):
		expected = {1: "Plumb Bob Tilt", 9: "Outhole", 10: "Ball Ramp Top (Trough)", 12: "Ball Ramp Lower (Trough, Release Position)",
		            20: "SHUTTLE T Drop Target", 25: "Left Jet Bumper", 26: "Right Jet Bumper", 27: "Lower Jet Bumper",
		            32: "Long Ramp Upper Switch", 39: "Left Kicker (Slingshot)", 41: "Lane Change (Right Flipper)", 49: "Playfield Tilt"}
		for address, label in expected.items():
			self.assertEqual(label, self.switches[address]["label"], address)
		# Column 6 is on 1J8-7 (1J8-6 is the key); row 8 returns on 1J10-1 per the schematic, not the table's 1J10-9.
		self.assertEqual({"drive_connection": "1J8-7", "drive_wire": "GRN-BLU", "return_connection": "1J10-1", "return_wire": "WHT-GRY"},
		                 {k: v for k, v in self.switches[48]["wiring"].items() if k != "board"})
		self.assertEqual("1J10-9", self.switches[1]["wiring"]["return_connection"])
		self.assertIn("prints this row's return on 1J10-1", self.switches[1]["physical"]["notes"])
		self.assertIn("drive 82, not 41", self.switches[41]["physical"]["notes"])
		relationships = {(r["source"], r["destination"], r["kind"]) for r in self.definition["relationships"]}
		self.assertIn(("switch.flipper-column-82", self.switches[41]["id"], "direct"), relationships)
		self.assertFalse(any(r["source"] == "switch.flipper-column-84" for r in self.definition["relationships"]))
		self.assertEqual((True, True, True, False), tuple(self.switches[a]["initial_active"] for a in (10, 11, 12, 9)))
		self.assertNotIn("part_number", self.switches[5]["physical"])
		self.assertEqual("cabinet_or_service", self.switches[1]["spatial"]["reason"])

	def test_special_solenoids_and_the_rotated_jet_table(self):
		self.assertEqual({39: 17, 40: 18, 27: 19, 26: 20, 25: 21}, data.PINMAME_SPECIAL_SWITCH_SOLENOIDS)
		self.assertEqual({17: 39, 18: 40, 19: 25, 20: 27, 21: 26}, data.PHYSICAL_SPECIAL_SWITCH)
		pulses = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "pulse"}
		for switch, coil in ((39, 17), (40, 18)):
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), pulses)
		# PinMAME's rotated jet pairing is not physical causality, and no relationship asserts it.
		for switch in (25, 26, 27):
			self.assertFalse(any(s == self.switches[switch]["id"] for s, _d in pulses), switch)
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		for coil, switch, mech in ((19, 25, "mech.left-jet-bumper"), (20, 27, "mech.lower-jet-bumper"), (21, 26, "mech.right-jet-bumper")):
			self.assertEqual([self.solenoids[coil]["id"]], mechanisms[mech]["actuators"])
			self.assertEqual([self.switches[switch]["id"]], mechanisms[mech]["sensors"])
			self.assertIn("rotated against the machine", self.solenoids[coil]["physical"]["notes"])
			self.assertIn("rotated against the machine", self.switches[switch]["physical"]["notes"])
		self.assertEqual("8P3-21", self.solenoids[21]["wiring"]["drive_connection"].split("; ")[1])
		self.assertEqual("Q48", self.solenoids[2]["wiring"]["driver_transistor"])
		self.assertIn("Q46", self.solenoids[2]["physical"]["notes"])

	def test_output_identities_and_fitment(self):
		kinds = {a: (o["kind"], o["availability"]) for a, o in self.solenoids.items()}
		for address in (1, 2, 3, 4, 5, 6, 7, 8, 13, 15, 16, 17, 18, 19, 20, 21):
			self.assertEqual(("coil", "used"), kinds[address], address)
		for address in (9, 10, 14):
			self.assertEqual(("flasher", "used"), kinds[address], address)
		self.assertEqual(("relay", "used"), kinds[11])
		self.assertIn("turns the GI off", self.solenoids[11]["physical"]["notes"])
		self.assertEqual(("relay", "used"), kinds[23])
		for address in UNUSED_SOLENOIDS:
			self.assertEqual(("coil", "unused"), kinds[address], address)
		self.assertIn("8L12 NOT USED", self.solenoids[12]["physical"]["notes"])
		for address in (45, 46, 47, 48):
			self.assertEqual(("virtual", "used"), kinds[address], address)
		for address in (24, *range(25, 45), 49, 50, *range(51, 65)):
			self.assertEqual(("virtual", "unused"), kinds[address], address)
		backbox = {*range(1, 7), 38, 39, 40}
		for address, lamp in self.lamps.items():
			self.assertEqual("backbox" if address in backbox else "playfield", lamp["physical"]["location"], address)
		self.assertEqual({5, 7, 15, 38, 40, 41, 49}, {a for a, lamp in self.lamps.items() if lamp["physical"].get("quantity") == 2})
		self.assertEqual(2, len(self.lamps[15]["spatial"]["placements"]))
		self.assertEqual(2, len(self.lamps[41]["spatial"]["placements"]))
		self.assertEqual("1J6-5", self.lamps[4]["wiring"]["return_connection"])
		self.assertEqual("1J7-4", self.lamps[25]["wiring"]["drive_connection"])
		self.assertEqual("1J7-6", self.lamps[33]["wiring"]["drive_connection"])

	def test_insert_flash_lamps_conflict_blocks(self):
		conflicts = self.definition["conflicts"]
		self.assertEqual(["conflict.insert-flash-lamps-location"], [c["id"] for c in conflicts])
		self.assertEqual(conflicts, unresolved_conflicts(self.definition))
		self.assertIn("Resolution path:", conflicts[0]["description"])
		self.assertEqual({curator.MANUAL, curator.SCRIPT}, set(conflicts[0]["source_refs"]))
		flasher = self.solenoids[14]
		self.assertEqual("conflicted", flasher["provenance"]["status"])
		self.assertNotIn("spatial", flasher)
		self.assertIn("unresolved", flasher["physical"]["location"])

	def test_displays_and_mechanisms(self):
		displays = {d["id"]: (d["controller_index"], d["segment_start"], d["width"]) for d in self.definition["displays"]}
		self.assertEqual((0, 21, 7), displays["display.player-1"])
		self.assertEqual((1, 29, 7), displays["display.player-2"])
		self.assertEqual((2, 1, 7), displays["display.player-3"])
		self.assertEqual((3, 9, 7), displays["display.player-4"])
		self.assertEqual({0, 1, 2, 3, 4, 5, 6, 7}, {v[0] for v in displays.values()})
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		self.assertEqual({"coil.left-eject-hole", "coil.right-eject-hole"}, set(mechanisms["mech.eject-hole-locks-and-multiball"]["actuators"]))
		self.assertEqual({"coil.up-post", "coil.down-post"}, set(mechanisms["mech.heat-shield-post"]["actuators"]))
		self.assertEqual(["coil.outlane-gate"], mechanisms["mech.right-outlane-gate"]["actuators"])
		self.assertEqual(5, len(mechanisms["mech.outhole-and-ball-ramp"]["sensors"]))
		self.assertEqual({self.switches[a]["id"] for a in (33, 34, 35)}, set(mechanisms["mech.three-bank-drop-targets"]["sensors"]))

	def test_runtime_summary_records_every_claim(self):
		observations = self.runtime["runtime"]["observations"]
		self.assertEqual({str(n): n for n in range(1, 17)}, observations["physical_service_solenoid_to_public"])
		self.assertFalse(set(observations["solenoid_addresses_seen"]) & {22})
		closures = observations["runs"]["switch-test-l7"]["named_action_observations"]
		self.assertEqual(list(range(1, 65)), [c["input_address"] for c in closures])
		for closure in closures:
			shown = "".join(r["interpreted_text"] for r in closure["display_responses"]).strip()
			self.assertEqual(f"{closure['input_address']:02d}" if closure["input_address"] <= 49 else "", shown)
		l3 = load_json(ROOT / curator.RUNTIME_L3)["runtime"]
		self.assertEqual("sshtl_l3", l3["game"])
		self.assertEqual({str(n): n for n in range(1, 17)}, l3["observations"]["physical_service_solenoid_to_public"])
		for source_id, path in ((curator.RUNTIME_SOURCE, curator.RUNTIME), (curator.RUNTIME_L3_SOURCE, curator.RUNTIME_L3)):
			self.assertEqual(curator.sha256(ROOT / path), self.sources[source_id]["sha256"])

	def test_sources_excerpts_and_gate(self):
		self.assertEqual([], validate_machine(self.definition, ROOT))
		manual = self.sources[curator.MANUAL]
		self.assertEqual(data.MANUAL_SHA256, manual["sha256"])
		self.assertEqual(7, len(manual["excerpts"]))
		self.assertTrue(all(e["reviewed"] for s in self.sources.values() for e in s.get("excerpts", [])))
		script = self.sources[curator.SCRIPT]
		self.assertTrue(script["known_working"])
		self.assertEqual((curator.SCRIPT_CORPUS_REVISION, curator.SCRIPT_SHA256), (script["revision"], script["sha256"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], coverage["missing"])
		self.assertFalse((ROOT / curator.AUTHOR_READY).exists())

	def test_spatial_placements(self):
		report = load_json(ROOT / curator.REPORT)
		self.assertEqual({"switch.playfield-tilt", "flasher.insert-flash-lamps"}, {r["id"] for r in report["unplaced"]})
		self.assertIsNone(report["callout_check"])
		for record in report["located"]:
			for placement in record["placements"]:
				self.assertEqual("observed", placement["provenance"]["status"], placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
		ids = [p["id"] for r in report["located"] for p in r["placements"]]
		self.assertEqual(len(ids), len(set(ids)))
		geometry = load_json(ROOT / curator.GEOMETRY)
		self.assertEqual({"left": 0, "top": 0, "right": 952.9412, "bottom": 1976.471}, geometry["bounds"])
		self.assertEqual(["sw25"], geometry["anchors"]["solenoid"]["19"])
		self.assertEqual(["sw27"], geometry["anchors"]["solenoid"]["20"])
		self.assertEqual(["sw26"], geometry["anchors"]["solenoid"]["21"])
		post, collide = geometry["objects"]["centerpost"], geometry["objects"]["centerpostcollide"]
		self.assertLess(abs(post["x"] - collide["x"]) + abs(post["y"] - collide["y"]), 2.0)
		# The left bumper sits left of the right bumper, and the lower bumper below both.
		left, right, lower = (geometry["objects"][n] for n in ("sw25", "sw26", "sw27"))
		self.assertLess(left["x"], right["x"])
		self.assertGreater(lower["y"], max(left["y"], right["y"]))

	def test_curator_is_deterministic_and_guards_drift(self):
		with mock.patch("builtins.print"):
			curator.check(ROOT)
		with tempfile.TemporaryDirectory() as tmp:
			copy_root = Path(tmp)
			for relative in [curator.EXCERPTS, curator.RUNTIME, curator.RUNTIME_L3, curator.KNOWLEDGE_SEED, curator.GEOMETRY, Path("schemas"), Path("controllers")]:
				source = ROOT / relative
				target = copy_root / relative
				target.parent.mkdir(parents=True, exist_ok=True)
				(shutil.copytree if source.is_dir() else shutil.copyfile)(source, target)
			excerpt = copy_root / curator.EXCERPTS / "switch-matrix.md"
			excerpt.write_bytes(excerpt.read_bytes().replace(b"Lane Chg", b"Lane Chng"))
			with self.assertRaisesRegex(RuntimeError, "excerpt missing or changed"):
				curator.products(copy_root)

	def test_data_tables_are_complete(self):
		self.assertEqual(set(range(1, 65)), set(data.SWITCHES) | data.UNUSED_SWITCHES)
		self.assertEqual(set(range(1, 23)), set(data.SOLENOIDS))
		self.assertEqual(UNUSED_SOLENOIDS, set(data.UNUSED_SOLENOIDS))
		self.assertTrue(all(row[0] == "Not Used" for a, row in data.SOLENOIDS.items() if a in UNUSED_SOLENOIDS))
		matrix = (ROOT / curator.EXCERPTS / "switch-matrix.md").read_text(encoding="utf-8")
		for address, row in data.SWITCHES.items():
			self.assertIn(f"{row[1]} — {address} ", matrix + " ", address)
		lamps = (ROOT / curator.EXCERPTS / "lamp-matrix.md").read_text(encoding="utf-8")
		for address, row in data.LAMPS.items():
			self.assertIn(f"{row[1]} — {address} ", lamps + " ", address)
		table = (ROOT / curator.EXCERPTS / "solenoid-table.md").read_text(encoding="utf-8")
		for address, (function, wire, cpu, field, transistor, _part) in data.SOLENOIDS.items():
			self.assertIn(f"| {address:02d} | {function} | {wire} | {cpu} | {field} | {transistor} |", table.replace("| *", "| "), address)


@unittest.skipIf(_roots() is None, "external evidence roots not configured")
class SpaceShuttleRetainedEvidenceTests(unittest.TestCase):
	def test_retained_evidence_reproduces_and_claims_fail_on_mutation(self):
		with mock.patch("builtins.print"):
			curator.verify_evidence(ROOT)
		runs_root = _roots()["PINMAME_REVIEW_ARTIFACTS_ROOT"] / curator.REVIEW_FOLDER / "harness"
		run = load_json(runs_root / "gameplay-l7" / "run.json")
		broken = copy.deepcopy(run)
		for snapshot in broken["snapshots"]:
			if snapshot["label"] == "right flipper button (flipper column 82) (held)":
				for watched in snapshot["watched_switches"]:
					if watched["number"] == 41:
						watched["state"] = 0
		with self.assertRaisesRegex(RuntimeError, "82 copies into 41"):
			summary.gameplay(broken)
		broken = copy.deepcopy(run)
		for snapshot in broken["snapshots"]:
			if snapshot["label"] == "playfield tilt closure 2":
				snapshot["active_solenoids"] = [s for s in snapshot["active_solenoids"] if s != 23]
		with self.assertRaisesRegex(RuntimeError, "does not yet tilt"):
			summary.gameplay(broken)
		switches = load_json(runs_root / "switch-test-l7" / "run.json")
		broken = copy.deepcopy(switches)
		for snapshot in broken["snapshots"]:
			if snapshot["label"].startswith("close public switch 25 alone"):
				snapshot["active_solenoids"] = [19 if s == 21 else s for s in snapshot["active_solenoids"]]
		with self.assertRaisesRegex(RuntimeError, "Switch 25 drove specials"):
			summary.switch_test(broken)
		award = load_json(runs_root / "credit-award-l7" / "run.json")
		broken = copy.deepcopy(award)
		for step in broken["steps"]:
			step["transitions"]["solenoids"] = [t for t in step["transitions"]["solenoids"] if t["number"] != 15]
		with self.assertRaisesRegex(RuntimeError, "bell did not ring"):
			summary.credit_award(broken)


if __name__ == "__main__":
	unittest.main()
