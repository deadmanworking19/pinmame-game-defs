"""Regression tests for the Bally Centaur definition and the Bally MPU-35 profile.

The solenoid numbering here is the expensive fact: the manual's printed Self Test
number and PinMAME's public solenoid address are two different numberings, and
neither retained community script matches the manual. The mapping asserted below
was read off the ROM's own solenoid self test, which pulses each coil while
displaying that coil's identification number. Anything that quietly "tidies" it
back into an identity mapping is a regression.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "bally" / "centaur-1981.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "by35" / "centaur-solenoid-self-test.json"
AUX_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "by35" / "centaur-aux-lamps-in-play.json"
PINSIDE_PHOTOS = {
	"65f35c74d10ac19414aedc4fa70f52e5a89dd4b3.jpg": "6ddd40f46dc512fc0415cc1455589b0d35efae5bc482ab6c628e5e8bb07ecb00",
	"826977b13515798c9ccd366cda9be25b8c63d669.jpg": "629c564dd444053caf579c0d0e3813fea5f3084453069e9720d425596270ad5e",
}

MANUAL_SHA256 = "9893d29ee871fd8c0a2afea35e931f107fb97a8156739035e005b15fd879e7ea"
TRANSCRIPTION_SHA256 = "b2c47f5ddb5f7f22ffa680e01f8fcf84512f6afabfdc1d408b1fe45a89189c05"
TRACE_SHA256 = "e5ea81fea6bea18964708637a3486637d5d2e9045841ea2994f604863940327a"

# printed Self Test number -> (public PinMAME solenoid address, semantic device id)
#
# Asserting the device id as well as the address is the point: comparing only alias values lets a
# swap of two labels - exactly the off-by-one the legacy import already contained on the right
# four-bank - pass silently.
SELF_TEST_TO_PUBLIC_SOLENOID = {
	1: (7, "device.outhole-kicker"),
	2: (6, "device.knocker"),
	3: (8, "device.inline-drop-target-reset"),
	4: (9, "device.right-4-drop-target-reset"),
	5: (10, "device.left-thumper-bumper"),
	6: (11, "device.right-thumper-bumper"),
	7: (12, "device.left-slingshot"),
	8: (13, "device.right-slingshot"),
	9: (1, "device.orbs-target-reset"),
	10: (2, "device.right-4-drop-target-1-top"),
	11: (3, "device.right-4-drop-target-2"),
	12: (4, "device.right-4-drop-target-3"),
	13: (5, "device.right-4-drop-target-4-bottom"),
	14: (15, "device.ball-release"),
	15: (14, "device.ball-kick-to-playfield"),
	16: (18, "device.coin-lockout-door"),
	17: (19, "device.k1-relay-flipper-enable"),
	18: (20, "device.magnet"),
}

UNUSED_SWITCH_ADDRESSES = (7, 13, 14, 23, 35, 36)

# addresses the manual prints with a parenthesised physical quantity
SHARED_SWITCH_QUANTITIES = {12: 4, 15: 3, 16: 2, 18: 2, 21: 2, 34: 5}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class CentaurDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.inputs = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		cls.dips = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		}
		cls.solenoids = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.centaur.1981", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1981, machine["year"])
		self.assertEqual(476, machine["ipdb_id"])

	def test_controller_platform_is_the_bally_mpu_35_profile(self) -> None:
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertEqual("pinmame.by35", self.profile["id"])
		self.assertEqual("Bally MPU AS-2518-35", self.profile["hardware_family"])

	def test_driver_variants_are_the_same_physical_machine(self) -> None:
		drivers = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual({"centaur", "centaura", "centaurb"}, drivers)
		# The Inder game of the same name is a different physical machine and must not be grouped.
		self.assertNotIn("centauri", drivers)
		self.assertNotIn("centaurj", drivers)

	def test_solenoid_self_test_numbers_map_to_the_observed_public_addresses(self) -> None:
		for self_test, (public, device_id) in SELF_TEST_TO_PUBLIC_SOLENOID.items():
			device = self.solenoids.get(public)
			self.assertIsNotNone(device, f"public solenoid {public} is missing")
			aliases = {
				alias["value"]
				for alias in device["aliases"]
				if alias["namespace"] == "manual.self-test"
			}
			self.assertEqual({f"{self_test:02d}"}, aliases, f"public solenoid {public}")
			self.assertEqual(device_id, device["id"], f"public solenoid {public}")

	def test_committed_runtime_evidence_carries_the_same_mapping(self) -> None:
		"""The definition and the evidence artifact must not be able to drift apart."""
		evidence = load_json(EVIDENCE_PATH)
		observed = evidence["runtime"]["observations"]["physical_service_solenoid_to_public"]
		expected = {
			str(self_test): public
			for self_test, (public, _) in SELF_TEST_TO_PUBLIC_SOLENOID.items()
		}
		self.assertEqual(expected, observed)
		self.assertEqual(["centaur"], evidence["driver_ids"])
		self.assertEqual(["bally.centaur.1981"], evidence["machine_ids"])

	def test_every_observed_lamp_address_is_declared(self) -> None:
		"""Observing an address and not declaring it is silent under-reporting."""
		evidence = load_json(EVIDENCE_PATH)
		observed = set(evidence["runtime"]["observations"]["lamp_addresses_seen"])
		declared = {
			item["binding"]["device"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual(set(), observed - declared, "observed lamp addresses are undeclared")

	def test_solenoid_alias_namespace_is_consistent(self) -> None:
		"""A consumer enumerating one namespace must not silently drop devices."""
		namespaces = {
			alias["namespace"]
			for device in self.solenoids.values()
			for alias in device["aliases"]
			if alias["namespace"].startswith("pinmame.")
		}
		self.assertEqual({"pinmame.coil"}, namespaces)

	def test_printed_fourteen_and_fifteen_are_transposed(self) -> None:
		"""The single easiest thing to get wrong: the numbers collide but the devices swap."""
		self.assertEqual("device.ball-kick-to-playfield", self.solenoids[14]["id"])
		self.assertEqual("device.ball-release", self.solenoids[15]["id"])

	def test_public_seven_is_the_outhole_kicker_not_a_ball_release(self) -> None:
		"""Both retained community scripts label public 7 a release to the shooter lane."""
		self.assertEqual("device.outhole-kicker", self.solenoids[7]["id"])

	def test_magnet_and_flipper_relay_are_present_on_the_continuous_outputs(self) -> None:
		self.assertEqual("device.magnet", self.solenoids[20]["id"])
		self.assertEqual("magnet", self.solenoids[20]["kind"])
		self.assertEqual("device.k1-relay-flipper-enable", self.solenoids[19]["id"])
		self.assertEqual("relay", self.solenoids[19]["kind"])

	def test_continuous_output_one_is_the_sixth_switch_column_strobe(self) -> None:
		"""Public 17 is a strobe, not a coil, which is why it never pulses and never releases.

		A continuous output that is held never appears as a pulse, so the absence of a pulse in the
		self-test trace was never evidence that the address is unused - an inference an earlier pass
		got wrong. It reads as permanently asserted because by35.c OR-accumulates solenoid state
		within each VBLANK window, so a line toggling faster than VBLANK looks continuously on.
		"""
		device = self.solenoids[17]
		self.assertEqual("used", device["availability"])
		self.assertEqual("control_signal", device["kind"])
		self.assertEqual("validated", device["provenance"]["status"])
		self.assertIn("strobe", device["label"].lower())
		self.assertNotIn("coil.driver-17", [conflict["path"] for conflict in self.definition["conflicts"]])

	def test_every_mpu_option_switch_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 33)), set(self.dips))
		# All 32 now carry a function: 28 from the printed manual, and 17-20 as the centre coin
		# chute selector, which the manual omits but the community option-switch documentation
		# carried by all four retained tables supplies.
		self.assertEqual(set(), {n for n, i in self.dips.items() if i["availability"] != "used"})

	def test_mechanisms_are_documented_and_own_their_hardware_once(self) -> None:
		mechanisms = self.definition["mechanisms"]
		self.assertGreaterEqual(len(mechanisms), 10)
		owned: dict[str, str] = {}
		for mechanism in mechanisms:
			self.assertTrue(mechanism["behavior"].strip())
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owned, f"{actuator} claimed twice")
				owned[actuator] = mechanism["id"]
		names = {mechanism["id"] for mechanism in mechanisms}
		self.assertIn("mech.captive-orb-store", names)
		self.assertIn("mech.inline-drop-target-bank", names)
		# The orb store is game state, not hardware: the trough owns the coils.
		orb = next(m for m in mechanisms if m["id"] == "mech.captive-orb-store")
		self.assertEqual([], orb["actuators"])

	def test_switch_polarity_is_declared(self) -> None:
		for address, item in self.inputs.items():
			if item["availability"] in {"used", "optional"}:
				self.assertIsInstance(item.get("normally_closed"), bool, f"switch {address}")

	def test_every_declared_solenoid_is_legal_for_the_profile(self) -> None:
		group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.solenoid")
		allowed = set()
		for rule in group["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		for address in self.solenoids:
			self.assertIn(address, allowed, f"solenoid {address} is outside the profile")

	def test_switch_matrix_covers_the_printed_forty_eight_addresses(self) -> None:
		matrix = {address for address in self.inputs if 1 <= address <= 48}
		self.assertEqual(set(range(1, 49)), matrix)

	def test_blank_switch_positions_are_declared_unused(self) -> None:
		for address in UNUSED_SWITCH_ADDRESSES:
			device = self.inputs[address]
			self.assertEqual("unused", device["availability"], f"switch {address}")

	def test_shared_switch_addresses_record_their_physical_quantity(self) -> None:
		for address, quantity in SHARED_SWITCH_QUANTITIES.items():
			device = self.inputs[address]
			self.assertEqual(
				quantity,
				device.get("physical", {}).get("quantity"),
				f"switch {address} should record {quantity} physical contacts",
			)

	def test_legacy_switch_label_conflicts_are_resolved_from_the_manual(self) -> None:
		"""All seven inherited conflicts; the platform source was right in every case."""
		self.assertEqual("switch.5th-ball-trough", self.inputs[2]["id"])
		self.assertEqual("switch.credit-button", self.inputs[6]["id"])
		self.assertEqual("switch.coin-3-right", self.inputs[9]["id"])
		self.assertEqual("switch.coin-1-left", self.inputs[10]["id"])
		self.assertEqual("switch.coin-2-middle", self.inputs[11]["id"])
		self.assertEqual("switch.slam", self.inputs[16]["id"])
		# Neither legacy source was right about 7: the manual prints no description there.
		self.assertEqual("unused", self.inputs[7]["availability"])
		# All seven legacy label conflicts are gone; the only conflict left is a new, honest one.
		switch_conflicts = [
			conflict for conflict in self.definition["conflicts"]
			if conflict["path"].startswith("binding:pinmame.input.switch")
		]
		self.assertEqual([], switch_conflicts)

	def test_display_inventory_matches_dispby7(self) -> None:
		displays = {item["controller_index"]: item for item in self.definition["displays"]}
		self.assertEqual(set(range(6)), set(displays))
		for index in range(4):
			self.assertIn("Player", displays[index]["label"])
			self.assertIn("seven digits", displays[index]["label"])
		self.assertIn("two digits", displays[4]["label"])
		self.assertIn("two digits", displays[5]["label"])
		for display in displays.values():
			self.assertEqual("segment", display["kind"])
			# Backbox devices never carry playfield coordinates.
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_definition_cites_the_manual_and_the_runtime_scenario(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("manual.bally.centaur.1981", sources)
		self.assertIn("runtime.centaur.solenoid-self-test", sources)
		self.assertEqual("runtime_scenario", sources["runtime.centaur.solenoid-self-test"]["kind"])
		manual = sources["manual.bally.centaur.1981"]
		# The hash belongs in the typed field, not smuggled into free-text prose.
		self.assertEqual(MANUAL_SHA256, manual["sha256"])
		self.assertTrue(manual["uri"].startswith("external:pinmame-manuals/"))
		for field in ("license", "attribution", "original_filename", "rights", "acquired_at"):
			self.assertIn(field, manual)
		self.assertEqual(3, len(manual["excerpts"]))
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), path)
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])
			self.assertTrue((ROOT / excerpt["image"]).is_file(), excerpt["id"])
			self.assertTrue(excerpt["reviewed"])
		runtime = sources["runtime.centaur.solenoid-self-test"]
		self.assertEqual(
			"internal:evidence/runtime/by35/centaur-solenoid-self-test.json", runtime["uri"]
		)
		self.assertEqual("NOASSERTION", runtime["license"])
		self.assertIn("manual-support.bally.centaur.1981", sources)
		self.assertEqual(TRANSCRIPTION_SHA256, sources["manual-support.bally.centaur.1981"]["sha256"])

	def test_retained_evidence_hashes_match_when_the_roots_are_available(self) -> None:
		"""With the evidence roots set, prove the asserted hashes against the real files."""
		import hashlib
		import os

		manuals_root = os.environ.get("PINMAME_MANUALS_ROOT")
		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not manuals_root or not artifacts_root:
			self.skipTest("evidence roots are not configured")
		pdf = (
			Path(manuals_root)
			/ "by-machine"
			/ "bally.centaur.1981"
			/ "archive-bally-1981-english-manual"
			/ "Bally 1981 English Manual.pdf"
		)
		transcription = Path(artifacts_root) / "centaur-1981" / "manual-transcription.md"
		for path, expected in ((pdf, MANUAL_SHA256), (transcription, TRANSCRIPTION_SHA256)):
			self.assertTrue(path.is_file(), f"missing retained evidence: {path}")
			digest = hashlib.sha256()
			with open(path, "rb") as handle:
				for chunk in iter(lambda: handle.read(1 << 20), b""):
					digest.update(chunk)
			self.assertEqual(expected, digest.hexdigest(), str(path))

	def test_synthetic_flipper_coils_are_declared(self) -> None:
		"""The flippers are real coils; PinMAME just addresses them synthetically."""
		self.assertEqual("device.flipper-lower-right", self.solenoids[46]["id"])
		self.assertEqual("device.flipper-lower-left", self.solenoids[48]["id"])
		for address in (46, 48):
			self.assertEqual("coil", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])

	def test_unenumerated_dips_are_admitted_rather_than_implied_complete(self) -> None:
		"""The MPU has 32 physical option switches and this record enumerates none."""
		dips = [
			item for item in self.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		]
		if not dips:
			self.assertIn("input_enumeration", self.definition["coverage"]["missing"])
			self.assertIn("input_semantics", self.definition["coverage"]["missing"])

	def test_coverage_does_not_claim_more_than_the_devices_support(self) -> None:
		"""Naming cannot be validated while the largest device class is legacy carry-over."""
		lamps = [
			item for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		]
		statuses = {item["provenance"]["status"] for item in lamps}
		if statuses - {"validated"}:
			self.assertNotEqual("validated", self.definition["coverage"]["dimensions"]["semantic_naming"])
			self.assertIn("output_semantics", self.definition["coverage"]["missing"])

	def test_mapping_is_rederived_from_the_raw_trace_when_it_is_available(self) -> None:
		"""Re-derive the mapping from the ROM's own output, not from a second copied table.

		The naive version of this test built a dict and let later observations overwrite earlier
		ones, which hid a genuine contradiction: an early boot-time pairing yields 11 -> 19 before
		the steady-state cycle yields 11 -> 3. Overwriting made the assertion pass for the wrong
		reason. This version instead splits the trace into complete ordered 01..18 cycles and
		requires every complete cycle to equal the expected mapping independently, so a
		contradictory or partial observation fails rather than being silently replaced.
		"""
		import hashlib
		import json
		import os

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("evidence roots are not configured")
		trace = Path(artifacts_root) / "centaur-1981" / "harness" / "soltest3.json"
		self.assertTrue(trace.is_file(), f"missing retained trace: {trace}")

		# Decode only a trace whose bytes are the ones the definition cites.
		digest = hashlib.sha256()
		with open(trace, "rb") as handle:
			for chunk in iter(lambda: handle.read(1 << 20), b""):
				digest.update(chunk)
		self.assertEqual(TRACE_SHA256, digest.hexdigest(), str(trace))

		seg7 = {
			0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4",
			0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9",
		}
		# Ordered (self_test, public) observations, in trace order, with no overwriting.
		pairs: list[tuple[int, int]] = []
		pending: int | None = None
		for event in json.loads(trace.read_text(encoding="utf-8"))["events"]:
			if event["event"] == "solenoid" and event["state"] == 1:
				pending = event["number"]
			elif event["event"] == "display" and event.get("segments") and event["index"] == 0:
				if pending is None:
					continue
				digits = "".join(seg7.get(value & 0x7F, "") for value in event["segments"])
				if len(digits) == 2 and digits.isdigit() and 1 <= int(digits) <= 18:
					pairs.append((int(digits), pending))
					pending = None

		expected = {
			self_test: public
			for self_test, (public, _) in SELF_TEST_TO_PUBLIC_SOLENOID.items()
		}
		# Split into complete ordered cycles: a cycle runs 01..18 ascending, and a number that
		# does not continue the current cycle starts a new one.
		cycles: list[dict[int, int]] = []
		current: dict[int, int] = {}
		last = 0
		for self_test, public in pairs:
			if self_test <= last:
				cycles.append(current)
				current = {}
			current[self_test] = public
			last = self_test
		cycles.append(current)

		complete = [cycle for cycle in cycles if set(cycle) == set(expected)]
		self.assertGreaterEqual(
			len(complete), 2, f"expected at least two complete self-test cycles, saw {len(cycles)}"
		)
		for index, cycle in enumerate(complete):
			self.assertEqual(expected, cycle, f"complete cycle {index} disagrees with the definition")

	def test_evidence_manifest_hashes_reproduce(self) -> None:
		"""Every hash the evidence artifact pins must be reproducible from the real files."""
		import hashlib
		import os

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("evidence roots are not configured")
		evidence = load_json(EVIDENCE_PATH)
		harness = Path(artifacts_root) / "centaur-1981" / "harness"

		def sha256_of(path: Path) -> str:
			digest = hashlib.sha256()
			with open(path, "rb") as handle:
				for chunk in iter(lambda: handle.read(1 << 20), b""):
					digest.update(chunk)
			return digest.hexdigest()

		# Each recorded run must exist under the harness directory with the recorded hash.
		recorded = {run["sha256"] for run in evidence["runtime"]["raw_runs"]}
		actual = {sha256_of(path) for path in harness.glob("*.json")}
		self.assertTrue(
			recorded <= actual,
			f"recorded run hashes not found in {harness}: {sorted(recorded - actual)}",
		)

		# The directory manifest digest must be reproducible by the documented algorithm.
		import json as _json

		self.assertIn("manifest_algorithm", evidence["source"])
		entries = [
			{
				"path": item.relative_to(harness).as_posix(),
				"size": item.stat().st_size,
				"sha256": sha256_of(item),
			}
			for item in sorted(harness.rglob("*"))
			if item.is_file()
		]
		canonical = _json.dumps(
			entries, indent=None, separators=(",", ":"), sort_keys=True, ensure_ascii=False
		).encode("utf-8")
		self.assertEqual(evidence["source"]["sha256"], hashlib.sha256(canonical).hexdigest())

	def test_schematic_lamp_names_match_the_script_bound_addresses(self) -> None:
		"""The seven lamps the retained script binds by name are the only independent check.

		Everything else in the lamp table is derived: public = 16*d + lampadr + 1 puts an address
		on an MC14514 output, the schematic gives that output's SCR and connector pin, and the pin
		carries a printed function. If the derivation were wrong these seven would disagree.
		"""
		expected = {
			11: "Shoot Again",
			13: "Ball in Play",
			27: "Match",
			29: "High Score to Date",
			43: "Tilt Warning",
			45: "Game Over",
			61: "Tilt",
		}
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address, label in expected.items():
			self.assertEqual(label, lamps[address]["label"], f"lamp {address}")
			self.assertEqual("validated", lamps[address]["provenance"]["status"], f"lamp {address}")

	def test_lamp_classes_are_consistent_across_decoders(self) -> None:
		"""Each MC14514 output drives the same class of lamp on all four decoders.

		That structure is what makes the derivation trustworthy, so it is worth pinning: if a
		future edit puts a chamber lamp where a bonus lamp belongs, the class breaks.
		"""
		lamps = {
			item["binding"]["device"]: item["label"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		classes = {
			1: "Bonus", 2: "Bonus", 4: "Bonus", 5: "Rollover",
			6: "Drop Target", 7: "Drop Target Arrow", 8: "Chamber", 11: "Captive Orbs",
		}
		for output, token in classes.items():
			members = [
				lamps[16 * d + output + 1]
				for d in range(4)
				if (16 * d + output + 1) in lamps
			]
			self.assertEqual(4, len(members), f"decoder output {output}")
			for label in members:
				self.assertIn(token.split()[-1], label, f"output {output}: {label}")

	def test_public_lamp_one_is_not_a_lamp(self) -> None:
		"""It feeds the G.I. flasher module, which is why the legacy corpus never bound it."""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual("control_signal", lamps[1]["kind"])

	def test_coverage_is_author_ready_with_nothing_open(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("author_ready", coverage["status"])
		self.assertEqual([], coverage["missing"])
		self.assertTrue(all(value == "validated" for value in coverage["dimensions"].values()))
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse((ROOT / "machines" / "partial" / "bally" / "centaur-1981.json").exists())

	def test_lamp_113_is_an_unwired_circuit(self) -> None:
		"""The board drives A9J2-11, but the harness has no wire there and nothing names a function.

		What PinMAME publishes at 113 is the carry bit of the four-bit top-lane register, which the
		auxiliary-lamp gameplay run pins: it changes only with 65 at a lane-change wrap and in the
		power-up and game-start flashes. A bulb bound to it would invent a lamp.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		device = lamps[113]
		self.assertEqual("unused", device["availability"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("unused", device["spatial"]["reason"])
		self.assertIn("human-review.centaur.pinside-a9-photos", device["provenance"]["source_refs"])
		self.assertIn("runtime.centaur.aux-lamps-in-play", device["provenance"]["source_refs"])
		note = (ROOT / "evidence" / "excerpts" / "bally.centaur.1981" / "a9-harness-j2-list.md").read_text(encoding="utf-8")
		self.assertIn("| 11 | no | | |", note)
		evidence = load_json(AUX_EVIDENCE_PATH)
		run_note = evidence["runtime"]["observations"]["runs"]["centaur-aux-lamps-in-play"]["note"]
		self.assertIn("3 times with 65 at a lane rotation, and never otherwise", run_note)


	def test_centre_coin_chute_selector_is_enumerated(self) -> None:
		"""The printed credits-per-coin tables cover chutes 1 and 3 only; 17-20 are the centre."""
		for address in (17, 18, 19, 20):
			device = self.dips[address]
			self.assertEqual("used", device["availability"])
			self.assertIn("centre", device["label"])

	def test_every_device_carries_a_validated_spatial_record(self) -> None:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			self.assertIsNotNone(spatial, item["id"])
			self.assertIn(spatial["status"], {"validated", "not_applicable"}, item["id"])
		for display in self.definition["displays"]:
			self.assertIn("spatial", display, display["id"])


	def test_bare_auxiliary_matrix_positions_have_no_lamp(self) -> None:
		"""The A9 has twelve SCRs for sixteen matrix positions; four positions carry no bulb.

		Its MC14555B decoders are binary one-of-four, so the board reaches lamp addresses 0-3 on
		each of four data lines. The fitted circuits are 65-67, 81-83, 97-99 and 113-115; decoder
		position 3 has no SCR. PinMAME reports matrix bits rather than bulbs, so these still show
		activity during the self-test lamp sequence - that is not evidence of a lamp.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (68, 84, 100, 116):
			device = lamps[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			# The validator requires reason "unused" for an unused device; that there is no SCR
			# fitted at all is the sharper fact and lives in the device note.
			self.assertEqual("unused", device["spatial"]["reason"], address)
			self.assertIn("N/U", device["physical"]["notes"], address)


	def test_outer_top_lane_lamps_follow_the_rom_pairing(self) -> None:
		"""The ROM lights 97 for the left rollover (switch 5) and 65 for the right (switch 3).

		The A9 sheet prints TOP LEFT LANE against A9J2-7 (public 65) and TOP RIGHT LANE against
		A9J2-18 (public 97). An earlier pass followed that and called the retained table wrong, but a
		lit top lane is a made lane and the ROM's own pairing, read from a gameplay run, puts 97 with
		the left rollover. Each lane lamp must sit in its own rollover's column, and left must sit
		left of right.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		self.assertEqual(("lamp.rollover-1-left", "Top Left Lane"), (lamps[97]["id"], lamps[97]["label"]))
		self.assertEqual(("lamp.rollover-2", "Top Middle Lane"), (lamps[81]["id"], lamps[81]["label"]))
		self.assertEqual(("lamp.rollover-3-right", "Top Right Lane"), (lamps[65]["id"], lamps[65]["label"]))
		evidence = load_json(AUX_EVIDENCE_PATH)
		pairing = evidence["runtime"]["observations"]["switch_to_lamp"]
		self.assertEqual({"5": 97, "4": 81, "3": 65}, {key: pairing[key] for key in ("5", "4", "3")})
		for switch, lamp in ((5, 97), (4, 81), (3, 65)):
			lamp_x = lamps[lamp]["spatial"]["placements"][0]["x"]
			switch_x = self.inputs[switch]["spatial"]["placements"][0]["x"]
			self.assertLess(abs(lamp_x - switch_x), 0.02, f"lamp {lamp} is not above rollover {switch}")
		xs = [lamps[address]["spatial"]["placements"][0]["x"] for address in (97, 81, 65)]
		self.assertEqual(sorted(xs), xs, "top lanes must run left to right across the playfield")

	def test_struck_slingshots_and_bumpers_flick_the_lamps_the_sheet_prints(self) -> None:
		"""The ROM-side check of the rest of the A9 decoding: each struck device flicks its own row."""
		evidence = load_json(AUX_EVIDENCE_PATH)
		pairing = evidence["runtime"]["observations"]["switch_to_lamp"]
		self.assertEqual({"37": 66, "38": 82, "39": 98, "40": 114}, {key: pairing[key] for key in ("37", "38", "39", "40")})
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for switch, lamp in ((37, 66), (38, 82), (39, 98), (40, 114)):
			side = "Right" if switch in (37, 39) else "Left"
			self.assertTrue(lamps[lamp]["label"].startswith(side), lamp)
			self.assertTrue(self.inputs[switch]["label"].startswith(side), switch)

	def test_ball_kick_records_the_solenoid_expander_relay(self) -> None:
		device = self.solenoids[14]
		self.assertIn("Solenoid Expander A15", device["physical"]["notes"])
		self.assertIn("schematics.centaur-ii-reprint.bally.centaur.1981", device["provenance"]["source_refs"])

	def test_rebound_switch_places_all_five_contacts(self) -> None:
		device = self.inputs[34]
		self.assertEqual(5, device["physical"]["quantity"])
		placements = device["spatial"]["placements"]
		self.assertEqual(5, len(placements))
		left = sorted(p["y"] for p in placements if p["x"] < 0.2)
		right = sorted(p["y"] for p in placements if p["x"] > 0.7 and p["y"] > 0.5)
		upper = [p for p in placements if p["x"] > 0.7 and p["y"] < 0.3]
		self.assertEqual((2, 2, 1), (len(left), len(right), len(upper)))

	def test_auxiliary_board_is_sourced_from_the_centaur_manual(self) -> None:
		"""The A9 sheet is printed in Centaur's own manual, not borrowed from another game.

		An earlier pass concluded no Centaur manual carried it and fell back on the Kings of Steel
		schematics. The boards are identical, but only the Centaur print annotates the per-pin lamp
		functions, and those are what identify the twelve circuits.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (65, 66, 67, 68, 81, 82, 83, 84, 97, 98, 99, 100, 113, 114, 115, 116):
			self.assertIn(
				"manual-schematics.bally.centaur.1981",
				lamps[address]["provenance"]["source_refs"],
				address,
			)

	def test_placement_count_matches_declared_quantity(self) -> None:
		"""A render primitive is not a physical contact, and a lamp pair is not one bulb.

		The retained table models a single physical target as a trigger plus a hit target plus
		several render primitives stacked at one point. An earlier pass promoted each object as its
		own sensor, which invented contacts: switch 12 carried ten placements for four physical
		targets. Every located device must place exactly the quantity it declares.
		"""
		for item in self.definition["inputs"] + self.definition["outputs"]:
			placements = (item.get("spatial") or {}).get("placements")
			quantity = (item.get("physical") or {}).get("quantity")
			if placements and quantity is not None:
				self.assertEqual(quantity, len(placements), item["id"])

	def test_stacked_render_objects_are_not_separate_contacts(self) -> None:
		"""No two placements on one device may describe the same point."""
		for item in self.definition["inputs"] + self.definition["outputs"]:
			placements = (item.get("spatial") or {}).get("placements") or []
			for index, one in enumerate(placements):
				for other in placements[index + 1:]:
					self.assertFalse(
						abs(one["x"] - other["x"]) <= 0.01 and abs(one["y"] - other["y"]) <= 0.01,
						f"{item['id']}: {one['id']} and {other['id']} are the same location",
					)

	def test_only_the_chamber_circuits_drive_a_pair_of_lamps(self) -> None:
		"""The A9 sheet prints (2) against the four chamber circuits and against nothing else.

		An earlier pass read the board as twelve sets of two, which no source says; it left eight
		single-bulb circuits claiming a second bulb with no coordinate.
		"""
		lamps = {
			item["binding"]["device"]: item
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}
		for address in (67, 83, 99, 115):
			self.assertEqual(2, lamps[address]["physical"]["quantity"], address)
			placements = lamps[address]["spatial"]["placements"]
			self.assertEqual(2, len(placements), address)
			# one bulb either side of the Queen's Chamber lane
			self.assertLess(placements[0]["x"], 0.06, address)
			self.assertGreater(placements[1]["x"], 0.15, address)
		for address in (65, 66, 81, 82, 97, 98, 114):
			self.assertNotIn("quantity", lamps[address]["physical"], address)
			self.assertEqual(1, len(lamps[address]["spatial"]["placements"]), address)

	def test_aux_lamp_runtime_summary_reproduces_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		run_dir = Path(root) / "centaur-1981" / "harness-aux-lamps" / "centaur"
		evidence = load_json(AUX_EVIDENCE_PATH)
		(raw,) = evidence["runtime"]["raw_runs"]
		self.assertEqual(raw["sha256"], hashlib.sha256((run_dir / "run.json").read_bytes()).hexdigest())
		self.assertEqual(raw["scenario_sha256"], hashlib.sha256((ROOT / raw["scenario_path"]).read_bytes()).hexdigest())
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "centaur_aux_lamp_runtime_summary.py"), "--run-dir", str(run_dir), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr)
		sys.path.insert(0, str(ROOT / "tools"))
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(evidence["source"]["sha256"], check_manifest(run_dir, "centaur"))

	def test_pinside_photographs_are_retained_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		for name, digest in PINSIDE_PHOTOS.items():
			path = Path(root) / "centaur-1981" / "pinside-303903" / name
			self.assertTrue(path.is_file(), str(path))
			self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest(), name)

	def test_spatial_report_matches_the_definition(self) -> None:
		result = subprocess.run(
			[sys.executable, "-B", str(ROOT / "tools" / "centaur_spatial_report.py"), "--check"],
			capture_output=True, text=True, encoding="utf-8",
		)
		self.assertEqual(0, result.returncode, result.stderr + result.stdout)
		report = load_json(ROOT / "reports" / "spatial" / "bally" / "centaur-1981.json")
		self.assertEqual("pinmame-spatial-audit", report["format"])
		self.assertEqual([], report["unresolved"])
		self.assertIn("pinmame.output.lamp:113", report["not_applicable_outputs"]["unused"])


def _summary_tool():
	sys.path.insert(0, str(ROOT / "tools"))
	import centaur_aux_lamp_runtime_summary as summary

	return summary


def _switch(number: int, state: int, time: float) -> dict:
	return {"event": "switch", "number": number, "state": state, "time_s": time}


def _lamp(number: int, state: int, time: float) -> dict:
	return {"event": "lamp", "number": number, "state": state, "time_s": time}


def _lamp_113_trace() -> dict:
	"""A minimal trace with one data-line flash before the serve and one lane wrap after it."""
	events = [_switch(8, 0, 10.0), _switch(21, 1, 20.0)]
	for time, state in ((1.0, 1), (1.12, 0)):
		events += [_lamp(number, state, time) for number in (49, 50, 113, 114, 115)]
	events += [_lamp(65, 1, 20.05), _lamp(113, 1, 20.05), _lamp(97, 0, 20.08)]
	return {"events": events}


def _strike_trace() -> dict:
	events = []
	for offset, (switch, (lamp, solenoid)) in enumerate(_summary_tool().STRIKES.items()):
		start = 10.0 * (offset + 1)
		events += [
			_switch(switch, 1, start),
			{"event": "solenoid", "number": solenoid, "state": 1, "time_s": start + 0.01},
			_lamp(lamp, 0, start + 0.03),
			_lamp(lamp, 1, start + 0.17),
		]
	return {"events": events}


class CentaurRuntimeVerifierTests(unittest.TestCase):
	"""The runtime-summary checks must refuse traces that do not show what the summary claims."""

	def test_lamp_113_classifier_accepts_a_flash_and_a_lane_wrap(self) -> None:
		summary = _summary_tool()
		trace = _lamp_113_trace()
		counts = summary.classify_113(trace, summary.lamp_events(trace))
		self.assertEqual({"whole_row_flash": 2, "lane_rotation_with_65": 1}, counts)

	def test_lamp_113_classifier_refuses_unexplained_activity(self) -> None:
		summary = _summary_tool()
		mutations = {
			# an extra 113 pulse beside two lamps changing the other way
			"opposite direction": [_lamp(113, 1, 5.0), _lamp(49, 0, 5.0), _lamp(50, 0, 5.0), _lamp(113, 0, 5.1), _lamp(49, 1, 5.1), _lamp(50, 1, 5.1)],
			# a flash that mixes in a lamp from neither flash group
			"foreign lamp": [_lamp(113, 1, 6.0), _lamp(114, 1, 6.0), _lamp(115, 1, 6.0), _lamp(66, 1, 6.0), _lamp(113, 0, 6.1), _lamp(114, 0, 6.1), _lamp(115, 0, 6.1), _lamp(66, 0, 6.1)],
			# a flash that lights 113 and never puts it out
			"no off phase": [_lamp(113, 1, 7.0), _lamp(114, 1, 7.0), _lamp(115, 1, 7.0), _lamp(49, 1, 7.0)],
			# 113 changing on its own in play
			"alone in play": [_lamp(113, 1, 30.0), _lamp(113, 0, 30.5)],
		}
		for name, extra in mutations.items():
			trace = _lamp_113_trace()
			trace["events"] = sorted(trace["events"] + extra, key=lambda event: event["time_s"])
			with self.assertRaises(SystemExit, msg=name):
				summary.classify_113(trace, summary.lamp_events(trace))
		trace = _lamp_113_trace()
		trace["events"] = [dict(event, state=0) if event["event"] == "lamp" and event["number"] == 65 else event for event in trace["events"]]
		with self.assertRaises(SystemExit, msg="65 moving the other way at the wrap"):
			summary.classify_113(trace, summary.lamp_events(trace))

	def test_strike_verifier_requires_the_lamp_to_come_back_on(self) -> None:
		summary = _summary_tool()
		trace = _strike_trace()
		self.assertEqual({"37": 66, "38": 82, "39": 98, "40": 114}, summary.verify_strikes(trace, summary.lamp_events(trace)))
		trace["events"] = [event for event in trace["events"] if not (event["event"] == "lamp" and event["state"] == 1 and event["number"] == 98)]
		with self.assertRaises(SystemExit):
			summary.verify_strikes(trace, summary.lamp_events(trace))

	def test_retained_run_mutations_are_refused_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		summary = _summary_tool()
		run = load_json(Path(root) / "centaur-1981" / "harness-aux-lamps" / "centaur" / "run.json")
		summary.verify(run)
		pulsed = dict(run, events=sorted(
			run["events"] + [_lamp(113, 1, 20.0), _lamp(1, 0, 20.0), _lamp(17, 0, 20.0), _lamp(113, 0, 20.1), _lamp(1, 1, 20.1), _lamp(17, 1, 20.1)],
			key=lambda event: event["time_s"],
		))
		with self.assertRaises(SystemExit):
			summary.verify(pulsed)
		strikes = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") in (37, 38, 39, 40) and event["state"] == 1]
		dark = dict(run, events=[
			event for event in run["events"]
			if not (event["event"] == "lamp" and event["state"] == 1 and event["number"] in (66, 82, 98, 114) and min(strikes) < event["time_s"])
		])
		with self.assertRaises(SystemExit):
			summary.verify(dark)

	def test_spatial_geometry_check_refuses_displaced_placements_when_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		sys.path.insert(0, str(ROOT / "tools"))
		import copy

		import centaur_spatial_report as report

		gameitems = Path(root) / report.EXTRACTION / "gameitems"
		definition = load_json(DEFINITION_PATH)
		report.verify_geometry(definition, gameitems)
		for collection, group, address in (("inputs", "pinmame.input.switch", 34), ("outputs", "pinmame.output.lamp", 66), ("outputs", "pinmame.output.lamp", 99)):
			mutated = copy.deepcopy(definition)
			item = next(i for i in mutated[collection] if i["binding"] == {"device": address, "group": group})
			item["spatial"]["placements"][-1]["x"] = round(item["spatial"]["placements"][-1]["x"] + 0.05, 6)
			with self.assertRaises(SystemExit, msg=f"{group}:{address}"):
				report.verify_geometry(mutated, gameitems)


class By35ProfileTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(PROFILE_PATH)
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def _allowed(self, group_id: str) -> set[int]:
		allowed: set[int] = set()
		for rule in self.groups[group_id]["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		return allowed

	def test_momentary_solenoids_stop_at_fifteen(self) -> None:
		"""Selector 15 is the idle state, so there is no public address 16."""
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual(set(range(1, 16)), allowed)
		self.assertNotIn(16, allowed)

	def test_four_continuous_outputs_are_published_at_seventeen_through_twenty(self) -> None:
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual({17, 18, 19, 20}, allowed)

	def test_lamp_decoder_slots_are_not_addressable(self) -> None:
		allowed = self._allowed("pinmame.output.lamp")
		for slot in (16, 32, 48, 64, 80, 96, 112, 128):
			self.assertNotIn(slot, allowed, f"lamp {slot} is a skipped decoder slot")
		self.assertEqual(120, len(allowed))

	def test_switch_matrix_is_six_columns_of_eight_plus_diagnostics(self) -> None:
		allowed = self._allowed("pinmame.input.switch")
		self.assertLessEqual(set(range(1, 49)), allowed)
		self.assertLessEqual({-7, -6, -5}, allowed)
		self.assertNotIn(49, allowed)

	def test_emulator_normalization_is_declared_and_not_reapplied(self) -> None:
		self.assertTrue(self.profile["inversion_applied_by_emulator"])

	def test_profile_pins_its_pinmame_revision(self) -> None:
		revisions = {source["revision"] for source in self.profile["sources"]}
		self.assertIn("4ec52ff0ac133ac251681518aed2249e19fe26eb", revisions)


if __name__ == "__main__":
	unittest.main()
