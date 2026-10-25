from __future__ import annotations

import json
import copy
import unittest
from pathlib import Path

from pinmame_game_defs.validation import validate_against_schema, validate_controller_profile


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "spike1.json"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"


def addresses(group: dict) -> set[int]:
	result = set()
	for rule in group["address_rules"]:
		result.update(rule.get("values", []))
		if "minimum" in rule:
			result.update(range(rule["minimum"], rule["maximum"] + 1))
	return result


class Spike1ControllerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def test_profile_passes_schema_and_semantic_validation(self) -> None:
		self.assertEqual([], validate_against_schema(self.profile, ROOT / "schemas" / "controller.schema.json", PROFILE_PATH.name))
		self.assertEqual([], validate_controller_profile(self.profile))

	def test_plugin_routes_are_from_the_current_pinned_contract(self) -> None:
		self.assertEqual("pinmame.spike1", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp"},
			set(self.groups),
		)
		# PinMAMEPlugin.h:56-66 replaces the older switch 1 / lamp 0x200 IDs.
		for group_id, plugin_id in (
			("pinmame.input.switch", 5),
			("pinmame.input.dip", 6),
			("pinmame.output.solenoid", 1),
			("pinmame.output.lamp", 3),
		):
			with self.subTest(group=group_id):
				self.assertEqual(
					{"group_id": plugin_id, "contract_revision": PINMAME_REVISION},
					self.groups[group_id]["transports"]["controller_plugin"],
				)
		self.assertEqual({PINMAME_REVISION}, {source["revision"] for source in self.profile["sources"]})

	def test_switch_conversion_has_128_distinct_public_positions(self) -> None:
		# spike1_sw2m / spike1_m2sw admit padding; other numbers alias 132.
		self.assertEqual(
			set(range(0, 96)) | set(range(101, 133)),
			addresses(self.groups["pinmame.input.switch"]),
		)

	def test_unknown_revision_cannot_reuse_the_current_plugin_ids(self) -> None:
		profile = copy.deepcopy(self.profile)
		for group in profile['groups']:
			group['transports']['controller_plugin']['contract_revision'] = 'f' * 40
		self.assertTrue(validate_controller_profile(profile))

	def test_solenoid_rules_exclude_unrouted_holes(self) -> None:
		# Driver references, GAME ON, four binary lower-flipper copies and custom coils.
		self.assertEqual(
			set(range(1, 34)) | set(range(45, 49)) | set(range(51, 73)),
			addresses(self.groups["pinmame.output.solenoid"]),
		)

	def test_dip_ordinals_use_the_corrected_plugin_route(self) -> None:
		group = self.groups["pinmame.input.dip"]
		self.assertEqual(set(range(1, 9)), addresses(group))
		self.assertEqual(
			{"libpinmame": {"channel": "dip"}, "controller_plugin": {"group_id": 6, "contract_revision": PINMAME_REVISION}},
			group["transports"],
		)
		# libpinmame.cpp:2624 passes zero-based i separately from public i+1.
		self.assertIn("bank 0", group["notes"])
		self.assertIn("zero-based source bit i", group["notes"])

	def test_virtual_game_on_and_current_polling_are_explicit(self) -> None:
		notes = self.groups["pinmame.output.solenoid"]["notes"]
		self.assertIn("Public 33 is the virtual GAME ON state", notes)
		self.assertIn("nSolenoids is at least 48", notes)
		self.assertIn("1 kHz", notes)
		self.assertNotIn("nSolenoids is 32", notes)

	def test_lamp_namespace_keeps_gi_and_rgb_in_the_lamp_channel(self) -> None:
		group = self.groups["pinmame.output.lamp"]
		self.assertEqual(set(range(1, 273)), addresses(group))
		self.assertEqual({"channel": "lamp"}, group["transports"]["libpinmame"])
		self.assertNotIn("pinmame.output.gi", self.groups)
		self.assertIn("motor-drive bit 0x08", group["notes"])
		self.assertIn("RGB emitters use three ordinary channels", group["notes"])

	def test_notes_preserve_rom_and_physical_evidence_limits(self) -> None:
		self.assertIn("exact ROM must prove a custom binding", self.groups["pinmame.output.solenoid"]["notes"])
		self.assertIn("cannot represent custom outputs 65-72", self.groups["pinmame.output.solenoid"]["notes"])
		self.assertIn("does not establish physical normally_closed construction", self.groups["pinmame.input.switch"]["notes"])
		self.assertIn("overwrites direct EOS writes", self.groups["pinmame.input.switch"]["notes"])
		self.assertIn("only during initial mapping", self.groups["pinmame.input.switch"]["notes"])


if __name__ == "__main__":
	unittest.main()
