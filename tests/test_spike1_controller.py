from __future__ import annotations

import json
import unittest
from pathlib import Path

from pinmame_game_defs.validation import validate_against_schema, validate_controller_profile


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "spike1.json"
PINMAME_REVISION = "8e0f721e3df7a2b4e8a9d2f4454ac7a9aa1ced53"


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

	def test_plugin_routes_are_from_the_exact_pr_contract(self) -> None:
		self.assertEqual("pinmame.spike1", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp"},
			set(self.groups),
		)
		# PinMAMEPlugin.h:56-66 replaces the older switch 1 / lamp 0x200 IDs.
		for group_id, plugin_id in (
			("pinmame.input.switch", 5),
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

	def test_solenoid_rules_exclude_unrouted_holes(self) -> None:
		# Driver references, four binary lower-flipper copies and custom coils.
		self.assertEqual(
			set(range(1, 33)) | set(range(45, 49)) | set(range(51, 73)),
			addresses(self.groups["pinmame.output.solenoid"]),
		)

	def test_dip_ordinals_do_not_claim_the_shifted_plugin_route(self) -> None:
		group = self.groups["pinmame.input.dip"]
		self.assertEqual(set(range(1, 9)), addresses(group))
		self.assertEqual({"libpinmame": {"channel": "dip"}}, group["transports"])
		# libpinmame.cpp:2074-2091 uses srcId without subtracting one.
		self.assertIn("bank 0", group["notes"])
		self.assertIn("bank 1 bit 0", group["notes"])

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
