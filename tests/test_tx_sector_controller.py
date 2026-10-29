from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from pinmame_game_defs.validation import (
	_validate_machine_controller_bindings,
	validate_against_schema,
	validate_controller_profile,
)


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "controllers/pinmame/gts80b.json"
EXCERPT_PATH = ROOT / "evidence/excerpts/gottlieb.tx-sector.1988/pinmame-controller.txt"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"


def addresses(group: dict) -> set[int]:
	result: set[int] = set()
	for rule in group["address_rules"]:
		result.update(rule.get("values", []))
		if "minimum" in rule:
			result.update(range(rule["minimum"], rule["maximum"] + 1))
	return result


class TxSectorControllerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def test_profile_schema_and_routes(self) -> None:
		self.assertEqual([], validate_against_schema(self.profile, ROOT / "schemas/controller.schema.json", str(PROFILE_PATH)))
		self.assertEqual([], validate_controller_profile(self.profile))
		self.assertEqual("pinmame.gts80b", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])
		for group_id, channel in (
			("pinmame.input.switch", "switch"),
			("pinmame.input.dip", "dip"),
			("pinmame.output.solenoid", "solenoid"),
			("pinmame.output.lamp", "lamp"),
			("pinmame.output.gi", "gi"),
		):
			with self.subTest(group=group_id):
				self.assertEqual({"libpinmame": {"channel": channel}}, self.groups[group_id]["transports"])
		self.assertEqual(5, len(self.groups))

	def test_public_envelopes_exclude_aliases_and_solenoid_holes(self) -> None:
		matrix = {10 * strobe + ret for strobe in range(8) for ret in range(8)}
		self.assertEqual(set(range(-8, 0)) | matrix | set(range(111, 119)), addresses(self.groups["pinmame.input.switch"]))
		self.assertEqual(set(range(1, 43)), addresses(self.groups["pinmame.input.dip"]))
		self.assertEqual(set(range(1, 12)) | set(range(45, 49)), addresses(self.groups["pinmame.output.solenoid"]))
		self.assertEqual(set(range(64)), addresses(self.groups["pinmame.output.lamp"]))
		self.assertEqual({0}, addresses(self.groups["pinmame.output.gi"]))
		for alias in (8, 9, 78, 79, 80, 101, 109, 110, 119, 120):
			with self.subTest(alias=alias):
				self.assertNotIn(alias, addresses(self.groups["pinmame.input.switch"]))

	def test_invalid_ranges_and_author_ready_binding_fail_closed(self) -> None:
		bad_profile = copy.deepcopy(self.profile)
		bad_profile["groups"][0]["address_rules"][0] = {"minimum": -1, "maximum": -8}
		self.assertTrue(validate_controller_profile(bad_profile))
		bad_profile["groups"][0]["address_rules"][0] = {"minimum": 0}
		self.assertTrue(validate_against_schema(bad_profile, ROOT / "schemas/controller.schema.json", "malformed"))

		definition = {
			"controller": {"platform": self.profile["id"]},
			"coverage": {"status": "author_ready"},
			"inputs": [{"binding": {"group": "pinmame.input.switch", "device": 8}}],
			"outputs": [],
		}
		errors: list[str] = []
		_validate_machine_controller_bindings(definition, "candidate", {self.profile["id"]: self.profile}, errors)
		self.assertTrue(any("outside controller group" in error for error in errors))
		definition["inputs"][0]["binding"]["device"] = 112
		errors.clear()
		_validate_machine_controller_bindings(definition, "candidate", {self.profile["id"]: self.profile}, errors)
		self.assertEqual([], errors)

	def test_generic_button_copy_and_output_mode_contract_is_explicit(self) -> None:
		switch = self.groups["pinmame.input.switch"]["notes"]
		for statement in ("copies these button states to that game's declared matrix positions", "overwriting direct host writes", "Copy destinations and FLIP_SOL/EOS flags", "per-game inversion mask"):
			self.assertIn(statement, switch)
		for group in self.groups.values():
			self.assertNotIn("tx-sector", group["notes"].lower())
			self.assertNotIn("FLIP_SWNO(6,16)", group["notes"])
			self.assertNotIn("lampCol=0", group["notes"].replace(" ", ""))
		sol = self.groups["pinmame.output.solenoid"]["notes"]
		for statement in ("10 is the game-on state from lamp 0 even when lamp 1 is set", "45/46 from right button 112", "47/48 from left button 114", "driver writes 1-9, game-on 10 and tilt 11"):
			self.assertIn(statement, sol)
		lamp = self.groups["pinmame.output.lamp"]["notes"]
		for statement in ("Selector nibbles 13, 14 and 15", "48-51, 52-55 and 56-59", "52-55 mirror solenoids 1-4", "60 mirrors 9"):
			self.assertIn(statement, lamp)
		self.assertIn("lamp 1's tilt-relay bit", self.groups["pinmame.output.gi"]["notes"])
		self.assertIn("bit 6 is the inverse of bank 4 bit 0 (33)", self.groups["pinmame.input.dip"]["notes"])
		self.assertIn("When the selected sound module is gts80bs2", self.groups["pinmame.input.dip"]["notes"])
		self.assertIn("nLamps = 64 + hw.lampCol * 8", lamp)

	def test_pinned_portable_source_excerpt_is_present(self) -> None:
		self.assertTrue(EXCERPT_PATH.is_file(), f"Required source excerpt is missing: {EXCERPT_PATH}")
		excerpt = EXCERPT_PATH.read_text(encoding="utf-8-sig")
		for anchor in ("GTS80_sw2m", "riot6532_2b_w", "core_updateSw", "s80bs1_sound_input_r", "vp_getLamp"):
			with self.subTest(anchor=anchor):
				self.assertIn(anchor, excerpt)
		self.assertTrue(any(source["revision"] == REVISION and EXCERPT_PATH.relative_to(ROOT).as_posix() in source["locator"] for source in self.profile["sources"]))


if __name__ == "__main__":
	unittest.main()
