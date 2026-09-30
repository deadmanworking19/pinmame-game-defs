from __future__ import annotations

import copy
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_champion_pub as curator


def group(definition: dict, collection: str, name: str) -> dict:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == name}


class ChampionPubTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = curator.build()
		cls.facts = curator.facts()
		cls.switches = group(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = group(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = group(cls.definition, "outputs", "pinmame.output.lamp")

	def test_exact_physical_identity_and_software_variant_contract(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.champion-pub.1998", 4358, "50063", 1998), (machine["id"], machine["ipdb_id"], machine["model_number"], machine["year"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual({"cp_15", "cp_16", "cp_16pfx"}, set(drivers))
		self.assertEqual("compatible", drivers["cp_16pfx"]["physical_compatibility"])
		self.assertIn("board/address contract", drivers["cp_16pfx"]["variant_notes"])
		self.assertIn("Program differences are uncharacterized", drivers["cp_16pfx"]["variant_notes"])
		self.assertNotIn("variant_differences", self.definition["coverage"]["missing"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claims = [row for row in catalog["drivers"] if row["id"] in drivers]
		self.assertEqual(3, len(claims))
		self.assertTrue(all(row["machine_id"] == machine["id"] for row in claims))

	def test_complete_public_inventory_without_helper_address_100(self) -> None:
		matrix = set(curator.MATRIX_ADDRESSES)
		self.assertEqual(matrix | set(range(1, 9)) | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(group(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(matrix | set(curator.EXTRA_LAMP_ADDRESSES), set(self.lamps))
		self.assertNotIn(100, self.lamps)
		self.assertEqual(set(range(5)), set(group(self.definition, "outputs", "pinmame.output.gi")))
		self.assertEqual((88, 151, 1), tuple(len(self.definition[key]) for key in ("inputs", "outputs", "displays")))
		self.assertEqual("cabinet_or_service", self.definition["displays"][0]["spatial"]["reason"])

	def test_nonflipper_circuits_lpdc_and_mirrors(self) -> None:
		self.assertEqual(["coil"] * 4, [self.solenoids[n]["kind"] for n in range(33, 37)])
		self.assertIn("Rope", self.solenoids[33]["label"])
		self.assertIn("Ramp", self.solenoids[34]["label"])
		for n in range(37, 41):
			self.assertEqual("control_signal", self.solenoids[n]["kind"])
			self.assertEqual("internal_nonvisual", self.solenoids[n]["spatial"]["reason"])
		for n in range(41, 45):
			self.assertEqual("virtual", self.solenoids[n]["kind"])
		for n in range(45, 49):
			self.assertEqual("coil", self.solenoids[n]["kind"])
		self.assertEqual("unused", self.solenoids[32]["availability"])
		self.assertEqual("unused", self.solenoids[50]["availability"])
		for n in (29, 30, 31):
			self.assertEqual(["internal.wpc-state"], self.solenoids[n]["roles"])
		for n in (32, 50):
			self.assertEqual(["internal.unused.wpc-output"], self.solenoids[n]["roles"])
			self.assertEqual("virtual", self.solenoids[n]["spatial"]["reason"])
		self.assertIn("constant zero", self.solenoids[32]["physical"]["notes"])

	def test_rom_contract_and_unfitted_upper_button_states(self) -> None:
		self.assertTrue(self.switches[38]["normally_closed"])
		self.assertFalse(self.switches[64]["normally_closed"])
		for n in (38, 64, 61, 62):
			self.assertTrue(any(ref.startswith("runtime.champion-pub") for ref in self.switches[n]["provenance"]["source_refs"]))
		for n in (116, 118):
			self.assertEqual(("virtual", "used"), (self.switches[n]["kind"], self.switches[n]["availability"]))
			self.assertEqual("virtual", self.switches[n]["spatial"]["reason"])
			self.assertNotIn("normally_closed", self.switches[n])
		for n in (111, 113):
			self.assertEqual("sensor", self.switches[n]["spatial"]["placements"][0]["role"])
			self.assertEqual("observed", self.switches[n]["spatial"]["status"])

	def test_full_mechanism_ownership_and_causal_not_proximity_relationships(self) -> None:
		self.assertEqual(17, len(self.definition["mechanisms"]))
		actuators = [actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))
		self.assertEqual({("coil.solenoid-2", "switch.matrix-31"), ("coil.solenoid-9", "switch.matrix-61"), ("coil.solenoid-10", "switch.matrix-62"), ("coil.solenoid-12", "switch.matrix-75")}, {(row["source"], row["destination"]) for row in self.definition["relationships"]})
		boxer = next(row for row in self.definition["mechanisms"] if row["id"] == "mechanism.boxer")
		self.assertEqual({"switch.matrix-41", "switch.matrix-46", "switch.matrix-47", "switch.matrix-48"}, {sensor for position in boxer["positions"] for sensor in position["sensors"]})

	def test_lamp_helpers_and_series_pair_are_not_extra_bulbs(self) -> None:
		for n in (51, 53, 54, 55):
			self.assertEqual(1, self.lamps[n]["physical"]["quantity"])
		self.assertEqual("LED91", self.facts["positions"]["pinmame.output.lamp:95"]["points"][0]["object"])
		self.assertEqual("LED108", self.facts["positions"]["pinmame.output.lamp:124"]["points"][0]["object"])
		for n in (91, 104, 111, 124):
			self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
			self.assertEqual("observed", self.lamps[n]["spatial"]["status"])
			self.assertEqual(1, len(self.lamps[n]["spatial"]["placements"]))
		for n in (105, 108, 125, 128):
			self.assertEqual("unknown", self.lamps[n]["availability"])
			self.assertNotIn("spatial", self.lamps[n])
		self.assertEqual("A-17835", self.lamps[83]["physical"]["assembly_part_number"])
		self.assertIn(curator.COMPANION, self.lamps[95]["provenance"]["source_refs"])

	def test_physical_switch_construction_and_service_revision(self) -> None:
		for n in (11, 15, 16, 17, 18, 26, 27, 57, 58, 61, 62, 63, 72, 76):
			self.assertEqual("microswitch", self.switches[n]["physical"]["switch_type"])
		self.assertEqual("leaf", self.switches[65]["physical"]["switch_type"])
		self.assertEqual("unknown", self.switches[71]["physical"]["switch_type"])
		self.assertIn("SB 107", self.facts["knowledge"])
		self.assertIn("31-3065.1", self.facts["knowledge"])
		self.assertIn("31-3066.1", self.facts["knowledge"])
		self.assertNotIn("\ufffd", self.facts["knowledge"])

	def test_source_hashes_and_exact_normalization(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest())
				if "image" in excerpt:
					payload = (ROOT / excerpt["image"]).read_bytes()
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256(payload).hexdigest())
					self.assertLess(len(payload), 100_000)
		for item in self.definition["inputs"] + self.definition["outputs"]:
			key = f"{item['binding']['group']}:{item['binding']['device']}"
			if key not in self.facts["positions"]:
				continue
			for raw, point in zip(self.facts["positions"][key]["points"], item["spatial"]["placements"], strict=True):
				self.assertEqual(curator._round_point(raw["x"] / 970), point["x"])
				self.assertEqual(curator._round_point(raw["y"] / 2100), point["y"])
				if raw.get("path", "").startswith("gameitems/Primitive."):
					self.fail("Stored primitive offset used instead of world mesh")

	def test_partial_gate_and_schema(self) -> None:
		self.assertEqual([], validate_against_schema(self.definition, ROOT / "schemas/machine.schema.json", "Champion Pub"))
		self.assertEqual([], validate_machine(self.definition, ROOT))
		promoted = copy.deepcopy(self.definition)
		promoted["coverage"]["status"] = "author_ready"
		promoted["coverage"]["missing"] = []
		promoted["coverage"]["dimensions"] = {key: "validated" for key in promoted["coverage"]["dimensions"]}
		self.assertTrue(validate_machine(promoted, ROOT), "Incomplete geometry and serial-output routing must reject promotion")
		self.assertEqual("pinmame-spatial-blockers", load_json(ROOT / curator.REPORT_PATH)["format"])

	def test_deterministic_artifacts_and_refusal_to_overwrite_promotion(self) -> None:
		for _ in range(2):
			curator.check()
		for path, payload in curator.artifacts().items():
			self.assertEqual(payload, (ROOT / path).read_bytes())
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			(root / curator.AUTHOR_READY_PATH).parent.mkdir(parents=True)
			(root / curator.AUTHOR_READY_PATH).write_text("{}")
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.generate(root)
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.check(root)

	def test_facts_refuse_incomplete_input_or_promotion(self) -> None:
		broken = copy.deepcopy(self.facts)
		del broken["extra_lamps"]["128"]
		with patch.object(curator, "load_json", return_value=broken):
			with self.assertRaisesRegex(RuntimeError, "Incomplete extra_lamps"):
				curator.facts()
		broken = copy.deepcopy(self.facts)
		broken["coverage"]["status"] = "author_ready"
		with patch.object(curator, "load_json", return_value=broken):
			with self.assertRaisesRegex(RuntimeError, "promotion"):
				curator.facts()

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT") and os.environ.get("PINMAME_MANUALS_ROOT"), "Optional retained evidence roots are not configured")
	def test_retained_full_artifacts_manifest_and_clean_source_checkout(self) -> None:
		curator.verify_evidence()


if __name__ == "__main__":
	unittest.main()
