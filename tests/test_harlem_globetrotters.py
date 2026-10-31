"""Fail-closed tests for the Bally Harlem Globetrotters On Tour (1979) definition.

The printed solenoid numbers are the ROM's test order, the lamp functions come from the board chain
plus this game's own lamp sheets, and the record stays partial because the retained table draws its
playfield inserts without bulbs. Each fact is asserted on its own, against the retained runtime
summary where the ROM decided it, so a regression names the fact that broke. Tests that need the
external evidence roots skip cleanly when those roots are not configured.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_harlem_globetrotters as curator  # noqa: E402
import harlem_globetrotters_runtime_summary as summary_tool  # noqa: E402

MACHINE_ID = "bally.harlem-globetrotters-on-tour.1979"
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "harlem-globetrotters-on-tour-1979.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "harlem-globetrotters-on-tour-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "harlem-globetrotters-on-tour-1979.md"
SUMMARY_PATH = ROOT / "evidence" / "runtime" / "by35" / "harlem-globetrotters-on-tour-1979-harness.json"
SWITCH2_PATH = ROOT / "evidence" / "runtime" / "by35" / "harlem-globetrotters-on-tour-hglbtrtr-switch-2-in-play.json"
SPATIAL_SEED = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-spatial.json"
READINGS_SEED = ROOT / "tools" / "seeds" / "bally" / "harlem-globetrotters-on-tour-1979-frame-readings.json"
REPORT_JSON = ROOT / "reports" / "spatial" / "bally" / "harlem-globetrotters-on-tour-1979.json"
REPORT_MD = ROOT / "reports" / "spatial" / "bally" / "harlem-globetrotters-on-tour-1979.md"

# Printed solenoid self-test number -> (public address, device id), as paired by the ROM's own test.
TEST_TO_PUBLIC = {
	1: (7, "device.outhole-kicker"), 2: (6, "device.knocker"), 3: (13, "device.globe-saucer-kicker"), 4: (14, "device.target-saucer-kicker"),
	5: (12, "device.right-slingshot"), 6: (11, "device.left-slingshot"), 7: (9, "device.left-thumper-bumper"), 8: (8, "device.right-thumper-bumper"),
	9: (10, "device.bottom-thumper-bumper"), 10: (15, "device.drop-target-reset"), 11: (18, "device.coin-lockout-door"),
	12: (19, "device.k1-relay-flipper-enable"), 13: (17, "device.right-gate"),
}
# Playfield switch -> the coil its closure fires in gameplay, and how.
SWITCH_TO_COIL = {37: (11, "direct"), 36: (12, "direct"), 40: (9, "direct"), 39: (8, "direct"), 38: (10, "direct"), 24: (13, "pulse"), 32: (14, "pulse"), 8: (7, "pulse")}
SWITCH_TO_LAMP_ON = {"1": 44, "2": 28, "3": 12, "24": 15, "25": 20, "30": 58, "32": 56, "35": 37}
UNUSED_SWITCHES = {5, 12, 13, 14, 15, 18, 19, 20, 21, *range(41, 49)}
CABINET_SWITCHES = {6, 7, 9, 10, 11, 16}
BACKBOX_LAMPS = {13: "Ball in play", 27: "Match", 29: "High score to date", 45: "Game over", 61: "Tilt"}
# The plug-connector sheet's Table B: the A5 J2 pins routed on to the playfield, and their lamps.
TABLE_B = {"A5J2-1": 63, "A5J2-2": 47, "A5J2-14": 15, "A5J2-15": 31, "A5J2-16": 14, "A5J2-20": 30, "A5J2-6": 46, "A5J2-7": 62}
LAMP_ADDRESSES = [n for n in range(1, 64) if n % 16 != 0]
BULB_LAMPS = {26: ("bumper2l",), 42: ("bumper1l", "bumper3l")}
ROM_ARCHIVES = {
	"hglbtrtr": "e1bf1c869aa00e0cfc2d526eac265aca42cea94726192f974b0bf7b178083fad",
	"hglbtrtb": "a97ca0ec417a0edd442994934f3829638ec0860ca56e16a8ed671de152edaffa",
}
MANUAL_BYTES = 7067665


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def env_root(name: str) -> Path | None:
	value = os.environ.get(name)
	return Path(value) if value else None


class HarlemGlobetrottersDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.summary = load(SUMMARY_PATH)
		cls.seed = load(SPATIAL_SEED)
		cls.inputs = cls.definition["inputs"]
		cls.outputs = cls.definition["outputs"]
		cls.switches = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.switch"}
		cls.dips = {d["binding"]["device"]: d for d in cls.inputs if d["binding"]["group"] == "pinmame.input.dip"}
		cls.solenoids = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {d["binding"]["device"]: d for d in cls.outputs if d["binding"]["group"] == "pinmame.output.lamp"}
		cls.sources = {s["id"]: s for s in cls.definition["sources"]}

	def placement(self, device: dict, index: int = 0) -> tuple[float, float]:
		item = device["spatial"]["placements"][index]
		return item["x"], item["y"]

	# ------------------------------------------------------------- identity --
	def test_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(
			(MACHINE_ID, "Harlem Globetrotters on Tour", "Bally", 1979, 1125, "GRnwQ-M9R5d"),
			(machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"], machine["opdb_id"]),
		)
		self.assertEqual({"width": 952.0, "height": 1974.0}, {k: machine["playfield"][k] for k in ("width", "height")})
		self.assertEqual({"platform": "pinmame.by35", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_drivers_and_the_seven_digit_conversion(self) -> None:
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual({"hglbtrtr", "hglbtrtb"}, set(drivers))
		self.assertEqual("identical", drivers["hglbtrtr"]["physical_compatibility"])
		self.assertNotIn("display_overrides", drivers["hglbtrtr"])
		self.assertEqual("hglbtrtr", drivers["hglbtrtb"]["clone_of"])
		self.assertEqual("compatible", drivers["hglbtrtb"]["physical_compatibility"])
		self.assertEqual([1, 9, 17, 25], [o["segment_start"] for o in drivers["hglbtrtb"]["display_overrides"]])
		self.assertEqual({7}, {o["width"] for o in drivers["hglbtrtb"]["display_overrides"]})
		self.assertIn("090", drivers["hglbtrtb"]["variant_notes"])
		self.assertEqual(sorted(drivers), sorted(self.summary["driver_ids"]))
		catalog = load(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({"hglbtrtr", "hglbtrtb"}, {d["id"] for d in catalog["drivers"] if d["machine_id"] == MACHINE_ID})

	def test_displays(self) -> None:
		layout = {d["id"]: (d["controller_index"], d["segment_start"], d["width"]) for d in self.definition["displays"]}
		self.assertEqual({
			"display.player-1-score": (0, 2, 6), "display.player-2-score": (1, 10, 6), "display.player-3-score": (2, 18, 6),
			"display.player-4-score": (3, 26, 6), "display.credits": (4, 35, 2), "display.ball-in-play-match": (5, 38, 2),
		}, layout)

	def test_no_other_bally_machine_id_or_driver_appears(self) -> None:
		"""The lamp chain is borrowed from the Kiss record by reasoning, never by copying its device data."""
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign_drivers = {d["id"] for d in catalog["drivers"] if d["machine_id"].startswith("bally.") and d["machine_id"] != MACHINE_ID}
		self.assertIn("kiss", foreign_drivers)
		text = json.dumps(self.definition) + KNOWLEDGE_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9_]{3,}", text))
		self.assertEqual(set(), tokens & foreign_drivers)
		foreign_machines = {m["id"] for m in catalog["machines"] if m["id"] != MACHINE_ID}
		self.assertEqual([], [m for m in foreign_machines if m in text])

	# ------------------------------------------------------------- coverage --
	def test_coverage_is_partial_with_only_spatial_placement_missing(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual({"validated"}, {v for k, v in coverage["dimensions"].items() if k != "spatial_placement"})
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		(entry,) = [m for m in catalog["machines"] if m["id"] == MACHINE_ID]
		self.assertEqual(94, entry["completion_score"])
		self.assertIn("**partial**", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_every_source_records_when_it_was_acquired(self) -> None:
		for source in self.definition["sources"]:
			self.assertRegex(source.get("acquired_at", ""), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", source["id"])
			for field in ("license", "attribution"):
				self.assertTrue(source.get(field), (source["id"], field))
		self.assertEqual(
			{"pinmame.catalog.46e1a01a0f73", "pinmame.core.46e1a01a0f73", "controller-profile.pinmame-by35", "ipdb.1125",
			 "manual.bally.harlem-globetrotters-on-tour.1979", "vpinmame-library.bally-vbs", "vpx-script.harlem-globetrotters.1-2-0",
			 "vpx-table.harlem-globetrotters.1-0", "runtime.harlem-globetrotters-on-tour.harness",
			 "runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play"},
			set(self.sources),
		)
		self.assertNotIn("L:", json.dumps(self.definition["sources"]))

	def test_internal_sources_are_attached_to_their_bytes(self) -> None:
		self.assertEqual(file_digest(SUMMARY_PATH), self.sources["runtime.harlem-globetrotters-on-tour.harness"]["sha256"])
		self.assertEqual(file_digest(SWITCH2_PATH), self.sources["runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play"]["sha256"])
		self.assertEqual("8371478a7640f1896dcdf565aed340dc5df989ba", load(SWITCH2_PATH)["source"]["revision"])
		self.assertEqual(self.seed["table_sha256"], self.sources["vpx-table.harlem-globetrotters.1-0"]["sha256"])
		self.assertEqual(MANUAL_BYTES, int(re.search(r"([\d,]+) bytes", self.sources["manual.bally.harlem-globetrotters-on-tour.1979"]["locator"]).group(1).replace(",", "")))

	# ----------------------------------------------------------- solenoids --
	def test_printed_test_numbers_are_paired_by_the_rom(self) -> None:
		observed = self.summary["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({str(t): p for t, (p, _) in TEST_TO_PUBLIC.items()}, observed)
		self.assertEqual([p for _, (p, _) in sorted(TEST_TO_PUBLIC.items())], self.summary["runtime"]["observations"]["runs"]["solenoid-test-hglbtrtr"]["ordered_solenoid_on_sequence"])
		for test, (public, device_id) in TEST_TO_PUBLIC.items():
			device = self.solenoids[public]
			self.assertEqual(device_id, device["id"], public)
			self.assertEqual("used", device["availability"], public)
			self.assertIn({"namespace": "manual.self-test", "value": str(test)}, device["aliases"], public)

	def test_unused_and_missing_solenoid_addresses(self) -> None:
		self.assertEqual({1, 2, 3, 4, 5, 20}, {a for a, d in self.solenoids.items() if d["availability"] == "unused"})
		self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | set(range(45, 49)), set(self.solenoids))
		self.assertIn("power-on pulse", self.solenoids[20]["physical"]["notes"])
		seen = set(self.summary["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertEqual(set(), seen & {1, 2, 3, 4, 5, 16})
		self.assertEqual(set(range(6, 16)) | {17, 18, 19, 20}, seen)

	def test_continuous_outputs(self) -> None:
		self.assertEqual("relay", self.solenoids[19]["kind"])
		self.assertIn("cabinet.relay", self.solenoids[19]["roles"])
		self.assertIn("cabinet.coin-door", self.solenoids[18]["roles"])
		for address, transistor in ((17, "Q17"), (18, "Q19"), (19, "Q15")):
			self.assertEqual(transistor, self.solenoids[address]["wiring"]["driver_transistor"], address)
		self.assertIn("energized means closed", self.solenoids[17]["physical"]["notes"])
		self.assertIn("A tilt closes the FREE BALL GATE", self.solenoids[17]["physical"]["notes"])

	def test_gameplay_closures_fire_their_own_coils(self) -> None:
		relationships = {(r["source"], r["destination"]): r["kind"] for r in self.definition["relationships"]}
		gameplay: dict[int, set[int]] = {}
		for item in self.summary["runtime"]["observations"]["named_action_observations"]:
			if item["label"].startswith("gameplay:"):
				gameplay.setdefault(item["input_address"], set()).update(item["transitioned_solenoid_addresses"])
		for switch, (coil, kind) in SWITCH_TO_COIL.items():
			self.assertEqual(kind, relationships.get((self.switches[switch]["id"], self.solenoids[coil]["id"])), switch)
			self.assertIn(coil, gameplay[switch], switch)
		self.assertEqual("relay_gated", relationships[("switch.left-flipper-button", "device.left-flippers")])
		self.assertEqual("relay_gated", relationships[("switch.right-flipper-button", "device.right-flipper")])
		self.assertEqual(10, len(relationships))

	def test_flippers(self) -> None:
		right, left = self.solenoids[46], self.solenoids[48]
		self.assertEqual(("device.right-flipper", 1, 1), (right["id"], right["physical"]["quantity"], len(right["spatial"]["placements"])))
		self.assertEqual(("device.left-flippers", 2, 2), (left["id"], left["physical"]["quantity"], len(left["spatial"]["placements"])))
		self.assertIn("LEFT FLIPPER E.O.S.", left["physical"]["notes"])
		for address in (45, 47):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("not_applicable", self.solenoids[address]["spatial"]["status"], address)
		self.assertEqual("used", self.switches[82]["availability"])
		self.assertEqual("used", self.switches[84]["availability"])
		# core.h's flipper column: 81/83 are the lower end-of-stroke bits, 85-88 the upper ones; FLIP_SW(FLIP_L) reads only 82 and 84.
		expected = {
			81: ("switch.lower-right-flipper-end-of-stroke-position", "CORE_SWLRFLIPEOSBIT"),
			83: ("switch.lower-left-flipper-end-of-stroke-position", "CORE_SWLLFLIPEOSBIT"),
			85: ("switch.upper-right-flipper-end-of-stroke-position", "CORE_SWURFLIPEOSBIT"),
			86: ("switch.upper-right-flipper-button-position", "CORE_SWURFLIPBUTBIT"),
			87: ("switch.upper-left-flipper-end-of-stroke-position", "CORE_SWULFLIPEOSBIT"),
			88: ("switch.upper-left-flipper-button-position", "CORE_SWULFLIPBUTBIT"),
		}
		for address, (device_id, macro) in expected.items():
			device = self.switches[address]
			self.assertEqual((device_id, "unused"), (device["id"], device["availability"]), address)
			self.assertIn(macro, device["physical"]["notes"], address)
			self.assertIn("FLIP_SW(FLIP_L)", device["physical"]["notes"], address)
			self.assertEqual({"status": "not_applicable", "reason": "unused"}, {k: device["spatial"][k] for k in ("status", "reason")}, address)
			self.assertEqual("validated", device["provenance"]["status"], address)
			for source in ("pinmame.core.46e1a01a0f73", "controller-profile.pinmame-by35"):
				self.assertIn(source, device["provenance"]["source_refs"], address)
		for address in (81, 83):
			self.assertIn("staged", self.switches[address]["physical"]["notes"], address)
			self.assertIn("runtime.harlem-globetrotters-on-tour.harness", self.switches[address]["provenance"]["source_refs"], address)
		for address in (46, 48):
			self.assertNotIn("manual.self-test", {a["namespace"] for a in self.solenoids[address]["aliases"]}, address)

	# ------------------------------------------------------------ switches --
	def test_switch_inventory(self) -> None:
		# Every public switch address the BY35 profile declares has exactly one disposition here.
		profile = load(ROOT / "controllers" / "pinmame" / "by35.json")
		group = next(g for g in profile["groups"] if g["id"] == "pinmame.input.switch")
		declared: set[int] = set()
		for rule in group["address_rules"]:
			declared |= set(rule["values"]) if "values" in rule else set(range(rule["minimum"], rule["maximum"] + 1))
		self.assertEqual(set(range(-7, -4)) | set(range(1, 49)) | set(range(81, 89)), declared)
		self.assertEqual(declared, set(self.switches))
		self.assertEqual(len(self.switches), len([d for d in self.inputs if d["binding"]["group"] == "pinmame.input.switch"]))
		self.assertEqual(UNUSED_SWITCHES | {81, 83, 85, 86, 87, 88}, {a for a, d in self.switches.items() if d["availability"] == "unused"})
		self.assertEqual(set(range(1, 33)), set(self.dips))
		for address, device in self.switches.items():
			if device["availability"] == "used":
				self.assertIs(False, device["normally_closed"], address)
		self.assertEqual(CABINET_SWITCHES, {a for a, d in self.switches.items() if 0 < a < 49 and d["availability"] == "used" and d["spatial"]["status"] == "not_applicable"})
		self.assertEqual({"control_connection": "A4J3-3", "return_connection": "A4J3-16"}, {k: self.switches[16]["wiring"][k] for k in ("control_connection", "return_connection")})
		self.assertEqual({"control_connection": "A4J2-1", "return_connection": "A4J2-14"}, {k: self.switches[7]["wiring"][k] for k in ("control_connection", "return_connection")})

	def test_switch_test_showed_every_wired_address(self) -> None:
		runs = self.summary["runtime"]["observations"]["runs"]
		self.assertIn("public 1 to 40", runs["switch-test-hglbtrtr"]["note"])
		self.assertIn("closing 41 to 48 showed nothing", runs["switch-test-hglbtrtr"]["note"])
		self.assertIn("41 to 48 not", runs["switch-test-hglbtrtb"]["note"])

	def test_parallel_contacts_have_one_placement_each(self) -> None:
		for address, quantity in {7: 3, 16: 2, 34: 2}.items():
			self.assertEqual(quantity, self.switches[address]["physical"]["quantity"], address)
		self.assertEqual(
			[self.placement(self.switches[34], 0), self.placement(self.switches[34], 1)],
			[(self.seed["objects"][name]["x"], self.seed["objects"][name]["y"]) for name in ("Sling1", "Sling2")],
		)

	def test_library_defaults_are_not_taken_as_names(self) -> None:
		self.assertEqual("switch.drop-target-c", self.switches[2]["id"])
		self.assertIn("swBallRollTilt", self.switches[2]["physical"]["notes"])
		self.assertEqual("switch.coin-i-left", self.switches[10]["id"])
		self.assertEqual("switch.coin-ii-middle", self.switches[11]["id"])
		self.assertIn("runtime.harlem-globetrotters-on-tour.hglbtrtr.switch-2-in-play", self.switches[2]["provenance"]["source_refs"])

	def test_option_switches_carry_the_printed_functions(self) -> None:
		self.assertIn("Balls per game (ON 5, OFF 3)", self.dips[31]["physical"]["notes"])
		for number in (21, 22):
			self.assertIn("Score version", self.dips[number]["physical"]["notes"], number)
			self.assertIn("vpx-script.harlem-globetrotters.1-2-0", self.dips[number]["provenance"]["source_refs"], number)

	def test_legacy_compatibility_aliases_are_preserved_by_binding(self) -> None:
		seed = load(curator.LEGACY_ALIAS_SEED_PATH)
		self.assertEqual(MACHINE_ID, seed["machine_id"])
		by_group = {"pinmame.input.switch": self.switches, "pinmame.output.lamp": self.lamps, "pinmame.output.solenoid": self.solenoids}
		self.assertEqual(set(by_group), set(seed["aliases"]))
		for group, entries in seed["aliases"].items():
			for address, aliases in entries.items():
				present = {(a["namespace"], a["value"]) for a in by_group[group][int(address)]["aliases"]}
				self.assertLessEqual({tuple(a) for a in aliases}, present, (group, address))
		self.assertIn(("vpe-legacy.switch", "007"), {(a["namespace"], a["value"]) for a in self.switches[7]["aliases"]})
		self.assertNotIn(("vpe-legacy.switch", "s_ball_roll_tilt"), {(a["namespace"], a["value"]) for a in self.switches[2]["aliases"]})
		# The import's bindings at switch 134 and solenoids 33, 35 and 37 have no public address on BY35.
		self.assertNotIn(134, self.switches)
		self.assertEqual(set(), {33, 35, 37} & set(self.solenoids))
		self.assertIn("134", seed["source"])

	# ---------------------------------------------------------------- lamps --
	def test_sixty_lamps_all_used(self) -> None:
		self.assertEqual(LAMP_ADDRESSES, sorted(self.lamps))
		self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))
		self.assertEqual(LAMP_ADDRESSES, self.summary["runtime"]["observations"]["lamp_addresses_seen"])
		self.assertEqual([16, 32, 48], self.summary["runtime"]["observations"]["lamp_decoder_holes_not_seen"])
		self.assertEqual(SWITCH_TO_LAMP_ON, self.summary["runtime"]["observations"]["switch_to_lamp"])
		for switch, lamp in SWITCH_TO_LAMP_ON.items():
			self.assertIn("runtime.harlem-globetrotters-on-tour.harness", self.lamps[lamp]["provenance"]["source_refs"], lamp)

	def test_backbox_lamps(self) -> None:
		backbox = {a for a, d in self.lamps.items() if (d.get("spatial") or {}).get("status") == "not_applicable"}
		self.assertEqual(set(BACKBOX_LAMPS), backbox)
		for address, label in BACKBOX_LAMPS.items():
			self.assertEqual(label, self.lamps[address]["label"])
			self.assertEqual(["cabinet.backglass"], self.lamps[address]["roles"])

	def test_lamp_43_drives_the_playfield_and_back_box_shoot_again(self) -> None:
		lamp = self.lamps[43]
		self.assertEqual(("Shoot again", "playfield and back box", 2), (lamp["label"], lamp["physical"]["location"], lamp["physical"]["quantity"]))
		addresses = {a["value"] for a in lamp["aliases"] if a["namespace"] == "manual.address"}
		self.assertEqual({"A5J3-22", "A5J2-9"}, addresses)
		self.assertEqual("A5J3-22", lamp["wiring"]["drive_connection"])

	def test_table_b_pins_are_the_j2_playfield_lamps(self) -> None:
		j2 = {d["wiring"]["drive_connection"]: a for a, d in self.lamps.items() if d["wiring"]["drive_connection"].startswith("A5J2-") and a not in BACKBOX_LAMPS}
		self.assertEqual(TABLE_B, j2)

	def test_only_bulb_lights_place_lamps(self) -> None:
		placed = {a for a, d in self.lamps.items() if (d.get("spatial") or {}).get("status") not in (None, "not_applicable")}
		self.assertEqual(set(BULB_LAMPS), placed)
		for address, names in BULB_LAMPS.items():
			self.assertEqual([(self.seed["objects"][n]["x"], self.seed["objects"][n]["y"]) for n in names], [self.placement(self.lamps[address], i) for i in range(len(names))])
			for name in names:
				self.assertTrue(self.seed["objects"][name]["is_bulb_light"] and self.seed["objects"][name]["show_bulb_mesh"], name)
		unplaced = {a for a, d in self.lamps.items() if "spatial" not in d}
		self.assertEqual(set(LAMP_ADDRESSES) - set(BACKBOX_LAMPS) - set(BULB_LAMPS), unplaced)
		self.assertEqual(53, len(unplaced))
		for address in unplaced:
			light = self.seed["objects"][f"l{address}"]
			self.assertFalse(light["is_bulb_light"] or light["show_bulb_mesh"], address)
			self.assertEqual(address, light["timer_interval"], address)

	# --------------------------------------------------------------- spatial --
	def test_placements_match_the_frozen_table_objects(self) -> None:
		objects = self.seed["objects"]
		for address, (_, _, _, _, _, _, names) in curator.SWITCHES.items():
			for index, name in enumerate(names):
				self.assertEqual((objects[name]["x"], objects[name]["y"]), self.placement(self.switches[address], index), address)
		for name, address in (("Bumper1", 9), ("Bumper3", 8), ("Bumper2", 10), ("Drain", 7), ("sw24", 13), ("sw32", 14), ("RightLaneGate", 17), ("RightFlipper", 46)):
			self.assertEqual((objects[name]["x"], objects[name]["y"]), self.placement(self.solenoids[address]), address)
		centre = tuple(round(sum(objects[f"d{i}"][axis] for i in range(1, 5)) / 4 / self.seed["bounds"][edge], 6) for axis, edge in (("raw_x", "right"), ("raw_y", "bottom")))
		self.assertEqual(centre, self.placement(self.solenoids[15]))
		for name, item in objects.items():
			self.assertAlmostEqual(item["raw_x"] / self.seed["bounds"]["right"], item["x"], places=5, msg=name)
			self.assertAlmostEqual(item["raw_y"] / self.seed["bounds"]["bottom"], item["y"], places=5, msg=name)
			self.assertTrue(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1, name)

	def test_no_placement_is_validated_without_a_callout_check(self) -> None:
		statuses = {p["provenance"]["status"] for d in self.inputs + self.outputs for p in (d.get("spatial") or {}).get("placements", [])}
		self.assertEqual({"observed"}, statuses)

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load(REPORT_JSON)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(file_digest(DEFINITION_PATH), report["definition_sha256"])
		ids = {d["id"] for d in self.inputs + self.outputs}
		for disclosure in report["projection_disclosures"]:
			self.assertTrue(set(disclosure["devices"]) <= ids, disclosure["devices"])
		unplaced = sorted(d["id"] for d in self.lamps.values() if "spatial" not in d)
		self.assertEqual(unplaced, sorted(report["unplaced_physical_devices"]))
		self.assertIsNone(report["callout_check"])
		self.assertEqual(file_digest(SPATIAL_SEED), report["source_hashes"]["spatial_seed_sha256"])
		self.assertIn(f"The other {len(unplaced)} used playfield lamps have no position", REPORT_MD.read_text(encoding="utf-8"))

	# ----------------------------------------------------------- determinism --
	def test_curator_reproduces_the_artifacts(self) -> None:
		result = subprocess.run([sys.executable, "-B", str(ROOT / "tools" / "curate_harlem_globetrotters.py"), "--check"], capture_output=True, text=True, encoding="utf-8")
		self.assertEqual(0, result.returncode, result.stderr)

	def test_curator_detects_drift_in_an_isolated_copy(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			copies = {name: base / name for name in ("definition.json", "knowledge.md", "report.json", "report.md")}
			for name, source in zip(copies, (DEFINITION_PATH, KNOWLEDGE_PATH, REPORT_JSON, REPORT_MD)):
				copies[name].write_bytes(source.read_bytes())
			command = [
				sys.executable, "-B", str(ROOT / "tools" / "curate_harlem_globetrotters.py"), "--check",
				"--definition", str(copies["definition.json"]), "--knowledge", str(copies["knowledge.md"]),
				"--report-json", str(copies["report.json"]), "--report-md", str(copies["report.md"]),
			]
			untouched = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertEqual(0, untouched.returncode, untouched.stderr)
			original = copies["definition.json"].read_bytes()
			self.assertIn(b'"Harlem Globetrotters on Tour"', original)
			copies["definition.json"].write_bytes(original.replace(b'"Harlem Globetrotters on Tour"', b'"Harlem Globetrotters on Tours"', 1))
			tampered = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
			self.assertNotEqual(0, tampered.returncode)
			self.assertIn("canonical content mismatch", tampered.stderr)

	def run_curator_in_process(self, *arguments: str) -> tuple[int, str, mock.MagicMock, mock.MagicMock, mock.MagicMock]:
		"""Run curator.main() with every filesystem write, unlink and mkdir replaced by a recording mock."""
		with (
			mock.patch.object(Path, "write_bytes", autospec=True) as write,
			mock.patch.object(Path, "unlink", autospec=True) as unlink,
			mock.patch.object(Path, "mkdir", autospec=True) as mkdir,
			mock.patch.object(sys, "argv", ["curate_harlem_globetrotters.py", *arguments]),
			contextlib.redirect_stdout(io.StringIO()),
			contextlib.redirect_stderr(io.StringIO()) as stderr,
		):
			code = curator.main()
		return code, stderr.getvalue(), write, unlink, mkdir

	def test_a_partial_build_never_touches_an_existing_author_ready_definition(self) -> None:
		self.assertEqual("partial", self.definition["coverage"]["status"])
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			author_dir = base / "author-ready"
			author_path = author_dir / "bally" / "harlem-globetrotters-on-tour-1979.json"
			author_path.parent.mkdir(parents=True)
			author_bytes = b'{"coverage": {"status": "author_ready"}}\n'
			author_path.write_bytes(author_bytes)
			outputs = ("knowledge.md", "report.json", "report.md")
			before = sorted(p.relative_to(base).as_posix() for p in base.rglob("*"))
			with (
				mock.patch.object(curator, "AUTHOR_READY_DIR", author_dir),
				mock.patch.object(curator, "AUTHOR_READY_PATH", author_path),
				mock.patch.object(curator, "PARTIAL_PATH", base / "partial" / "harlem-globetrotters-on-tour-1979.json"),
			):
				for mode in ("--regenerate", "--check"):
					code, stderr, write, unlink, mkdir = self.run_curator_in_process(
						mode, "--knowledge", str(base / outputs[0]), "--report-json", str(base / outputs[1]), "--report-md", str(base / outputs[2]),
					)
					self.assertEqual(2, code, mode)
					self.assertIn("refusing", stderr, mode)
					self.assertIn("author-ready definition exists", stderr, mode)
					write.assert_not_called()
					unlink.assert_not_called()
					mkdir.assert_not_called()
			self.assertEqual(author_bytes, author_path.read_bytes())
			self.assertEqual(before, sorted(p.relative_to(base).as_posix() for p in base.rglob("*")))

	def test_an_explicit_definition_inside_the_author_ready_tree_is_refused(self) -> None:
		self.assertEqual(ROOT / "machines" / "author-ready", curator.AUTHOR_READY_DIR)
		self.assertTrue(curator.AUTHOR_READY_PATH.is_relative_to(curator.AUTHOR_READY_DIR))
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			author_dir = base / "author-ready"
			copy_path = author_dir / "bally" / "copy.json"
			copy_path.parent.mkdir(parents=True)
			copy_path.write_bytes(DEFINITION_PATH.read_bytes())
			before = sorted(p.relative_to(base).as_posix() for p in base.rglob("*"))
			with (
				mock.patch.object(curator, "AUTHOR_READY_DIR", author_dir),
				mock.patch.object(curator, "AUTHOR_READY_PATH", author_dir / "bally" / "harlem-globetrotters-on-tour-1979.json"),
			):
				for mode in ("--regenerate", "--check"):
					for definition in (copy_path, author_dir / "bally" / "absent.json", base / "elsewhere" / ".." / "author-ready" / "nested.json"):
						code, stderr, write, unlink, mkdir = self.run_curator_in_process(
							mode, "--definition", str(definition), "--knowledge", str(base / "k.md"), "--report-json", str(base / "r.json"), "--report-md", str(base / "r.md"),
						)
						self.assertEqual(2, code, (mode, definition))
						self.assertIn("points into", stderr, (mode, definition))
						write.assert_not_called()
						unlink.assert_not_called()
						mkdir.assert_not_called()
			self.assertEqual(DEFINITION_PATH.read_bytes(), copy_path.read_bytes())
			self.assertEqual(before, sorted(p.relative_to(base).as_posix() for p in base.rglob("*")))

	def test_regenerating_into_copies_writes_only_the_copies(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			base = Path(temporary)
			targets = {name: base / name for name in ("definition.json", "knowledge.md", "report.json", "report.md")}
			partial = base / "partial.json"
			partial.write_bytes(b"{}\n")
			with (
				mock.patch.object(curator, "AUTHOR_READY_DIR", base / "author-ready"),
				mock.patch.object(curator, "AUTHOR_READY_PATH", base / "author-ready" / "bally" / "harlem-globetrotters-on-tour-1979.json"),
				mock.patch.object(curator, "PARTIAL_PATH", partial),
				mock.patch.object(Path, "unlink", autospec=True) as unlink,
				mock.patch.object(sys, "argv", [
					"curate_harlem_globetrotters.py", "--regenerate", "--definition", str(targets["definition.json"]), "--knowledge", str(targets["knowledge.md"]),
					"--report-json", str(targets["report.json"]), "--report-md", str(targets["report.md"]),
				]),
				contextlib.redirect_stdout(io.StringIO()),
			):
				self.assertEqual(0, curator.main())
			unlink.assert_not_called()
			self.assertEqual(b"{}\n", partial.read_bytes())
			for name, source in zip(targets, (DEFINITION_PATH, KNOWLEDGE_PATH, REPORT_JSON, REPORT_MD)):
				self.assertEqual(source.read_bytes(), targets[name].read_bytes(), name)
			self.assertEqual(sorted(["definition.json", "knowledge.md", "report.json", "report.md", "partial.json"]), sorted(p.name for p in base.iterdir()))

	def test_excerpts_are_attached_to_their_bytes(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				self.assertEqual(excerpt["sha256"], file_digest(ROOT / excerpt["path"]), excerpt["id"])
				self.assertTrue(excerpt["reviewed"], excerpt["id"])
				self.assertTrue(excerpt["transcribed_by"].startswith("curator"), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], file_digest(ROOT / excerpt["image"]), excerpt["id"])
		self.assertEqual(13, count)
		on_disk = sorted(p.name for p in (ROOT / curator.EXCERPT_DIR).glob("*.md"))
		cited = sorted(Path(e["path"]).name for s in self.definition["sources"] for e in s.get("excerpts", []))
		self.assertEqual(on_disk, cited)

	def test_extraction_modes_require_their_root(self) -> None:
		environment = {k: v for k, v in os.environ.items() if k != "PINMAME_VPX_SOURCES_ROOT"}
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "curate_harlem_globetrotters.py"), "--verify-extraction"],
			capture_output=True, text=True, encoding="utf-8", env=environment,
		)
		self.assertNotEqual(0, result.returncode)
		self.assertIn("PINMAME_VPX_SOURCES_ROOT is required", result.stderr)

	# --------------------------------------------------------- pinned frames --
	def test_a_substituted_frame_is_refused(self) -> None:
		"""A display event at the pinned time and index whose segment words differ is refused, even if it reads the same digits."""
		pins = load(READINGS_SEED)["runs"]
		self.assertEqual("pinmame-segment-readings", load(READINGS_SEED)["format"])
		pinned = pins["solenoid-test-hglbtrtb"]["solenoid test 01"]
		self.assertEqual("01", pinned["reading"])
		# Seven blank-or-digit words reading "01": the comma bit on a blank is masked when decoding, so the digits match.
		event = {"event": "display", "index": pinned["index"], "time_s": pinned["time_s"], "segments": [0x80, 0, 0, 0, 0, 0x3F, 0x06]}
		self.assertEqual("01", summary_tool.reading_of(event)["reading"])
		self.assertNotEqual(pinned["segments_sha256"], summary_tool.segments_sha256(event["segments"]))
		with self.assertRaises(SystemExit):
			summary_tool.verify_cited(pins, "solenoid-test-hglbtrtb", "solenoid test 01", event)
		with self.assertRaises(SystemExit):
			summary_tool.verify_cited(pins, "solenoid-test-hglbtrtb", "solenoid test 99", event)
		self.assertEqual({"solenoid-test-hglbtrtr": 13, "solenoid-test-hglbtrtb": 14, "switch-test-hglbtrtr": 40, "switch-test-hglbtrtb": 40}, {k: len(v) for k, v in pins.items()})
		self.assertEqual("090", pins["solenoid-test-hglbtrtb"]["power-up version"]["reading"])
		self.assertIn(file_digest(READINGS_SEED), self.summary["runtime"]["command_template"])

	# ------------------------------------------------- retained evidence roots --
	def test_runtime_summary_is_reachable_when_configured(self) -> None:
		root = env_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if root is None:
			self.skipTest("evidence roots are not configured")
		runs = root / "harlem-globetrotters-on-tour-1979" / "runs"
		for run in self.summary["runtime"]["raw_runs"]:
			directory, driver = run["retained_from"].split("/runs/")[1].rsplit("/", 1)[0].split("/")
			self.assertEqual(run["sha256"], file_digest(runs / directory / driver / "run.json"), run["name"])
			self.assertEqual(run["scenario_sha256"], file_digest(ROOT / run["scenario_path"]), run["name"])
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "harlem_globetrotters_runtime_summary.py"), "--runs", str(runs), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(self.summary["source"]["sha256"], check_manifest(runs, "hglbtrtr"))
		switch2 = load(SWITCH2_PATH)
		retained = root / "harlem-globetrotters-on-tour-1979" / "harness" / "switch-2-in-play" / "hglbtrtr"
		self.assertEqual(switch2["source"]["sha256"], file_digest(retained / "run.json"))

	def test_a_substituted_frame_in_a_retained_run_is_refused(self) -> None:
		root = env_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if root is None:
			self.skipTest("evidence roots are not configured")
		runs = root / "harlem-globetrotters-on-tour-1979" / "runs"
		pins = load(READINGS_SEED)["runs"]
		pinned = pins["solenoid-test-hglbtrtb"]["solenoid test 01"]
		original_load = summary_tool.load_run
		run = original_load(runs, "solenoid-test-hglbtrtb")
		(event,) = [e for e in summary_tool.display_events(run, pinned["index"]) if e["time_s"] == pinned["time_s"]]
		self.assertEqual("01", summary_tool.verify_cited(pins, "solenoid-test-hglbtrtb", "solenoid test 01", event))

		def substituted(directory: Path, name: str) -> dict:
			loaded = original_load(directory, name)
			if name == "solenoid-test-hglbtrtb":
				loaded = copy.deepcopy(loaded)
				for item in loaded["events"]:
					if item["event"] == "display" and item["index"] == pinned["index"] and item["time_s"] == pinned["time_s"]:
						# Same digits, different words: set the masked comma bit on the leading blank.
						item["segments"] = [item["segments"][0] | 0x80, *item["segments"][1:]]
			return loaded

		with mock.patch.object(summary_tool, "load_run", substituted):
			with self.assertRaises(SystemExit) as refused:
				summary_tool.build(runs)
		self.assertIn("solenoid test 01", str(refused.exception))

	def test_table_geometry_is_reachable_when_configured(self) -> None:
		root = env_root("PINMAME_VPX_SOURCES_ROOT")
		if root is None:
			self.skipTest("evidence roots are not configured")
		base = root / "bally" / "harlem-globetrotters-on-tour-1979"
		vpx = base / "source" / "Harlem Globetrotters On Tour (Bally 1979).vpx"
		self.assertEqual(self.seed["table_sha256"], file_digest(vpx))
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "harlem_globetrotters_spatial_seed.py"), "--extracted", str(base / "extracted-vpxtool"), "--vpx", str(vpx), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		verified = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "curate_harlem_globetrotters.py"), "--verify-extraction"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, verified.returncode, verified.stderr)
		self.assertIn(self.seed["extraction_manifest_sha256"], verified.stdout)
		for name, digest in {"Bally.vbs": curator.BALLY_VBS_SHA, "core.vbs": curator.CORE_VBS_SHA}.items():
			self.assertEqual(digest, file_digest(base / "library" / name), name)
		self.assertEqual(curator.EMBEDDED_SCRIPT_SHA, file_digest(base / "extracted-vpxtool" / "script.vbs"))

	def test_manual_and_ipdb_page_are_reachable_when_configured(self) -> None:
		root = env_root("PINMAME_MANUALS_ROOT")
		if root is None:
			self.skipTest("evidence roots are not configured")
		base = root / "by-machine" / MACHINE_ID
		manual = base / "Bally_1979_Harlem_Globetrotters_On_Tour_Manual.pdf"
		self.assertEqual(MANUAL_BYTES, manual.stat().st_size)
		self.assertEqual(self.sources["manual.bally.harlem-globetrotters-on-tour.1979"]["sha256"], file_digest(manual))
		self.assertEqual(self.sources["ipdb.1125"]["sha256"], file_digest(base / "ipdb1125.html"))

	def test_rom_archives_are_reachable_when_configured(self) -> None:
		root = env_root("PINMAME_ROM_LIBRARY_ROOT")
		if root is None:
			self.skipTest("the ROM library root is not configured")
		for driver, digest in ROM_ARCHIVES.items():
			self.assertEqual(digest, file_digest(root / f"{driver}.zip"), driver)
		self.assertEqual(ROM_ARCHIVES["hglbtrtr"], self.summary["runtime"]["rom_archive_sha256"])
		self.assertIn(ROM_ARCHIVES["hglbtrtb"], self.summary["runtime"]["command_template"])


if __name__ == "__main__":
	unittest.main()
