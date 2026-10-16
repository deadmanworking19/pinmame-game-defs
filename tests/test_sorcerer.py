"""Sorcerer's semantic, provenance, runtime and promotion gates."""
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
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine
from pinmame_game_defs.conflicts import unresolved_conflicts
import curate_sorcerer as curator
import sorcerer_data as data
import summarize_sorcerer_runtime as summary

MACHINE_ID = "williams.sorcerer.1985"
DRIVERS = {"sorcr_l1", "sorcr_l2"}
UNUSED_SWITCHES = {41, *range(46, 65)}
UNUSED_SOLENOIDS = {9, 10, 12, 13, 14, 22}


def _roots() -> dict[str, Path] | None:
	names = ("PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_VPX_SOURCES_ROOT")
	if any(not os.environ.get(n) for n in names):
		return None
	return {n: Path(os.environ[n]) for n in names}


class SorcererTests(unittest.TestCase):
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
		self.assertEqual((MACHINE_ID, "Sorcerer", "Williams", 1985, "532", 2242, "G4qxv-MJPyv"),
		                 (m["id"], m["name"], m["manufacturer"], m["year"], m["model_number"], m["ipdb_id"], m["opdb_id"]))
		self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
		by_id = {d["id"]: d for d in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["sorcr_l2"])
		self.assertEqual("sorcr_l2", by_id["sorcr_l1"]["clone_of"])
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in by_id.values()))
		self.assertEqual({"platform": "pinmame.system-11", "hardware_generation": "0x800", "inversion_applied_by_emulator": True}, self.definition["controller"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		self.assertEqual(DRIVERS, {d["id"] for d in catalog["drivers"] if d.get("machine_id") == MACHINE_ID})
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
		expected = {1: "Plumb Bob Tilt", 9: "Left Spinner S", 16: "Right Spinner R", 28: "Outhole", 29: "Ball Ramp 1 (Trough)",
		            30: "Ball Ramp 2 (Trough, Eject Position)", 32: "Left Kicker (Slingshot)", 33: "Right Kicker (Slingshot)",
		            37: "Multi-Ball Lock (Ramp Eject)", 38: "Multi-Ball Ramp Switch", 43: "Lamp Shift Lane", 44: "Lane Change (Right Flipper)", 45: "Playfield Tilt"}
		for address, label in expected.items():
			self.assertEqual(label, self.switches[address]["label"], address)
		self.assertEqual({"drive_connection": "1J8-7", "drive_wire": "GRN-BLU", "return_connection": "1J10-6", "return_wire": "WHT-YEL"},
		                 {k: v for k, v in self.switches[44]["wiring"].items() if k != "board"})
		self.assertEqual("1J10-9", self.switches[1]["wiring"]["return_connection"])
		self.assertEqual("1J10-1", self.switches[8]["wiring"]["return_connection"])
		self.assertIn("drive 82, not 44", self.switches[44]["physical"]["notes"])
		self.assertEqual("playfield", self.switches[44]["physical"]["location"])
		relationships = {(r["source"], r["destination"], r["kind"]) for r in self.definition["relationships"]}
		self.assertIn(("switch.flipper-column-82", self.switches[44]["id"], "direct"), relationships)
		self.assertFalse(any(r["source"] == "switch.flipper-column-84" for r in self.definition["relationships"]))
		self.assertEqual((True, True, False), (self.switches[29]["initial_active"], self.switches[30]["initial_active"], self.switches[28]["initial_active"]))
		self.assertEqual("BLANK FOR DOMESTIC", data.SWITCHES[5][3])
		self.assertNotIn("part_number", self.switches[5]["physical"])

	def test_special_solenoids_follow_their_switches(self):
		relationships = {(r["source"], r["destination"]) for r in self.definition["relationships"] if r["kind"] == "pulse"}
		for switch, coil in {32: 17, 33: 18, 21: 19, 22: 20, 23: 21}.items():
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), relationships)
			self.assertEqual("coil", self.solenoids[coil]["kind"])
		self.assertEqual({"pinmame.core.97aa922bf8e4"} - set(self.solenoids[17]["provenance"]["source_refs"]), set())

	def test_output_identities_and_fitment(self):
		kinds = {a: (o["kind"], o["availability"]) for a, o in self.solenoids.items()}
		for address in (1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 21):
			self.assertEqual(("coil", "used"), kinds[address], address)
		for address in (5, 6, 7):
			self.assertEqual(("flasher", "used"), kinds[address], address)
		self.assertEqual(("relay", "used"), kinds[8])
		self.assertEqual("Flash Eyes Relay", self.solenoids[8]["label"])
		self.assertIn("parts-list error", self.solenoids[8]["physical"]["notes"])
		self.assertEqual(("relay", "used"), kinds[11])
		self.assertIn("turns the GI off", self.solenoids[11]["physical"]["notes"])
		self.assertEqual("cabinet_or_service", self.solenoids[11]["spatial"]["reason"])
		self.assertEqual(("relay", "used"), kinds[23])
		for address in UNUSED_SOLENOIDS:
			self.assertEqual(("coil", "unused"), kinds[address], address)
		self.assertIn("1P12-7 NC", self.solenoids[14]["physical"]["notes"])
		self.assertIn("knocker routine", self.solenoids[14]["physical"]["notes"])
		for address in (45, 46, 47, 48):
			self.assertEqual(("virtual", "used"), kinds[address], address)
		for address in (24, *range(25, 45), 49, 50, *range(51, 65)):
			self.assertEqual(("virtual", "unused"), kinds[address], address)
		backbox = {*range(1, 7), *range(56, 65)}
		for address, lamp in self.lamps.items():
			self.assertEqual("backbox" if address in backbox else "playfield", lamp["physical"]["location"], address)
		self.assertEqual(("Demon", "Bonus Hold Over"), (self.lamps[22]["label"], self.lamps[23]["label"]))
		self.assertIn("printed 22/23 names are swapped", self.lamps[22]["physical"]["notes"])
		self.assertIn("printed 22/23 names are swapped", self.lamps[23]["physical"]["notes"])
		self.assertEqual("1J6-5", self.lamps[4]["wiring"]["return_connection"])
		self.assertEqual("1J7-6", self.lamps[33]["wiring"]["drive_connection"])

	def test_displays_mechanisms_and_no_conflicts(self):
		displays = {d["id"]: (d["controller_index"], d["segment_start"], d["width"]) for d in self.definition["displays"]}
		self.assertEqual((2, 21, 7), displays["display.player-1"])
		self.assertEqual((0, 1, 7), displays["display.player-3"])
		self.assertEqual({0, 1, 2, 3, 4, 5, 6, 7}, {v[0] for v in displays.values()})
		self.assertEqual({"player_1": 2, "player_2": 3, "player_3": 0, "player_4": 1}, {k: v for k, v in {"player_1": displays["display.player-1"][0], "player_2": displays["display.player-2"][0], "player_3": displays["display.player-3"][0], "player_4": displays["display.player-4"][0]}.items()})
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		self.assertEqual({"coil.multi-ball-eject"}, set(mechanisms["mech.multi-ball-lock"]["actuators"]))
		self.assertEqual({self.switches[37]["id"], self.switches[38]["id"]}, set(mechanisms["mech.multi-ball-lock"]["sensors"]))
		self.assertEqual(4, len(mechanisms["mech.outhole-and-ball-ramp"]["sensors"]))
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual([], unresolved_conflicts(self.definition))

	def test_runtime_summary_records_every_claim(self):
		observations = self.runtime["runtime"]["observations"]
		self.assertEqual({str(n): n for n in range(1, 17)}, observations["physical_service_solenoid_to_public"])
		closures = observations["runs"]["switch-test-l2"]["named_action_observations"]
		self.assertEqual(list(range(1, 65)), [c["input_address"] for c in closures])
		for closure in closures:
			shown = "".join(r["interpreted_text"] for r in closure["display_responses"]).strip()
			self.assertEqual(f"{closure['input_address']:02d}" if closure["input_address"] <= 45 else "", shown)
			self.assertEqual([], closure["observed_switch_addresses"])
		self.assertEqual({"demon-lamp": 22, "bonus-hold-over-lamp": 23}, observations["named_output_addresses"])
		award = observations["runs"]["special-award-l2"]["named_action_observations"][0]
		self.assertIn(14, award["transitioned_solenoid_addresses"])
		l1 = load_json(ROOT / curator.RUNTIME_L1)["runtime"]
		self.assertEqual("sorcr_l1", l1["game"])
		self.assertEqual({str(n): n for n in range(1, 17)}, l1["observations"]["physical_service_solenoid_to_public"])
		for source_id, path in ((curator.RUNTIME_SOURCE, curator.RUNTIME), (curator.RUNTIME_L1_SOURCE, curator.RUNTIME_L1)):
			self.assertEqual(curator.sha256(ROOT / path), self.sources[source_id]["sha256"])

	def test_sources_excerpts_and_gate(self):
		self.assertEqual([], validate_machine(self.definition, ROOT))
		manual = self.sources[curator.MANUAL]
		self.assertEqual(data.MANUAL_SHA256, manual["sha256"])
		self.assertEqual(8, len(manual["excerpts"]))
		self.assertTrue(all(e["reviewed"] for s in self.sources.values() for e in s.get("excerpts", [])))
		script = self.sources[curator.SCRIPT]
		self.assertTrue(script["known_working"])
		self.assertEqual(curator.SCRIPT_CORPUS_REVISION, script["revision"])
		coverage = self.definition["coverage"]
		if coverage["status"] == "partial":
			self.assertEqual(["spatial_placement"], coverage["missing"])
		else:
			self.assertEqual([], coverage["missing"])

	def test_spatial_placements_and_callout_check(self):
		report = load_json(ROOT / curator.REPORT)
		check = report["callout_check"]
		self.assertEqual((90, 93), (check["validated"], check["checked"]))
		self.assertEqual({"switch.left-spinner-s.sensor.1", "switch.ball-ramp-1-trough.sensor.1", "switch.lamp-shift-lane.sensor.1"}, set(check["not_validated"]))
		self.assertEqual({"switch.playfield-tilt", "flasher.demon-background"}, {r["id"] for r in report["unplaced"]})
		seed = load_json(ROOT / curator.CALLOUTS)
		self.assertEqual(("23", "22"), (seed["checks"]["lamp.demon.emitter.1"]["label"], seed["checks"]["lamp.bonus-hold-over.emitter.1"]["label"]))
		for address in (6, 7):
			self.assertEqual("observed", self.solenoids[address]["spatial"]["status"])
		for address in range(7, 56):
			self.assertEqual("validated", self.lamps[address]["spatial"]["status"], address)
		self.assertIn("RightFlipper pivot", self.switches[44]["physical"]["notes"])
		geometry = load_json(ROOT / curator.GEOMETRY)
		self.assertEqual({"left": 0.0, "top": 0.0, "right": 952.941, "bottom": 1976.471}, geometry["bounds"])
		self.assertEqual(["li22"], geometry["anchors"]["lamp"]["22"])

	def test_curator_is_deterministic_and_guards_drift(self):
		with mock.patch("builtins.print"):
			curator.check(ROOT)
		with tempfile.TemporaryDirectory() as tmp:
			copy_root = Path(tmp)
			for relative in [curator.EXCERPTS, curator.RUNTIME, curator.RUNTIME_L1, curator.KNOWLEDGE_SEED, Path("schemas"), Path("controllers")]:
				source = ROOT / relative
				target = copy_root / relative
				target.parent.mkdir(parents=True, exist_ok=True)
				(shutil.copytree if source.is_dir() else shutil.copyfile)(source, target)
			if (ROOT / curator.GEOMETRY).exists():
				(copy_root / curator.GEOMETRY).parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(ROOT / curator.GEOMETRY, copy_root / curator.GEOMETRY)
			excerpt = copy_root / curator.EXCERPTS / "switch-matrix.md"
			excerpt.write_bytes(excerpt.read_bytes().replace(b"Lane Change", b"Lane Chance"))
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


@unittest.skipIf(_roots() is None, "external evidence roots not configured")
class SorcererRetainedEvidenceTests(unittest.TestCase):
	def test_retained_evidence_reproduces_and_claims_fail_on_mutation(self):
		with mock.patch("builtins.print"):
			curator.verify_evidence(ROOT)
		runs_root = _roots()["PINMAME_REVIEW_ARTIFACTS_ROOT"] / MACHINE_ID / "harness"
		run = load_json(runs_root / "gameplay-l2" / "run.json")
		broken = copy.deepcopy(run)
		for snapshot in broken["snapshots"]:
			if snapshot["label"] == "right flipper button (flipper column 82) (held)":
				for watched in snapshot["watched_switches"]:
					if watched["number"] == 44:
						watched["state"] = 0
		with self.assertRaisesRegex(RuntimeError, "82 copies into 44"):
			summary.gameplay(broken)
		for mutate, message in (
			(lambda steps: [t for t in steps if t["number"] != 22], "lights lamp 22"),
			(lambda steps: [dict(t, number={22: 23, 23: 22}.get(t["number"], t["number"])) for t in steps], "lights lamp 22"),
		):
			broken = copy.deepcopy(run)
			for step in broken["steps"]:
				step["transitions"]["lamps"] = mutate(step["transitions"]["lamps"])
			with self.assertRaisesRegex(RuntimeError, message):
				summary.demon_lamp_identities(broken)
		broken = copy.deepcopy(run)
		for snapshot in broken["snapshots"]:
			if snapshot["label"] == "ball 2 plunged":
				snapshot["active_lamps"] = [lamp for lamp in snapshot["active_lamps"] if lamp != 23]
		with self.assertRaisesRegex(RuntimeError, "lit into the next ball"):
			summary.demon_lamp_identities(broken)
		award = load_json(runs_root / "special-award-l2" / "run.json")
		broken = copy.deepcopy(award)
		broken["events"] = [e for e in broken["events"] if not (e["event"] == "solenoid" and e["number"] == 14)]
		for step in broken["steps"]:
			step["transitions"]["solenoids"] = [t for t in step["transitions"]["solenoids"] if t["number"] != 14]
		with self.assertRaisesRegex(RuntimeError, "solenoid-14 pulse"):
			summary.special_award(broken)
		pulse_time = next(e["time_s"] for e in award["events"] if e["event"] == "solenoid" and e["number"] == 14 and e["state"] == 1)
		for mutate in (
			lambda events: [e for e in events if not (e["event"] == "solenoid" and e["number"] == 14 and e["state"] == 0)],
			lambda events: [dict(e, time_s=pulse_time + 20.0) if e["event"] == "solenoid" and e["number"] == 14 and e["state"] == 0 else e for e in events],
		):
			broken = copy.deepcopy(award)
			broken["events"] = mutate(broken["events"])
			with self.assertRaisesRegex(RuntimeError, "must release once"):
				summary.special_award(broken)
		switches = load_json(runs_root / "switch-test-l2" / "run.json")
		broken = copy.deepcopy(switches)
		for snapshot in broken["snapshots"]:
			if snapshot["label"].startswith("close public switch 21 alone"):
				snapshot["active_solenoids"] = [s for s in snapshot["active_solenoids"] if s != 19]
		with self.assertRaisesRegex(RuntimeError, "drove specials"):
			summary.switch_test(broken)


if __name__ == "__main__":
	unittest.main()
