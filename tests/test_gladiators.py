"""Fail-closed tests for the Gottlieb Gladiators (1993) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Lamp Matrix, Relay & Solenoid and Switch
Matrix tests for names and addresses, pinned PinMAME's gts3.c and gts3games.c for the numbering and the flipper copy,
and the known-working script for bindings. A regression names the fact that broke.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_gladiators  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "gottlieb" / "gladiators-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "gottlieb" / "gladiators-1993.md"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "gts3.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "gottlieb.gladiators.1993"
MATRIX = {column * 10 + row for column in range(12) for row in range(8)}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def note_pairs(note: str, marker: str = "Address = name: ") -> dict[str, str]:
	"""Parse the "a = b; c = d." list a run note ends with."""
	body = note.split(marker, 1)[1].split(". No SWITCH line", 1)[0].rstrip(".")
	pairs = {}
	for item in body.split("; "):
		key, _, value = item.partition(" = ")
		pairs[key] = value
	return pairs


def allowed(rules: list[dict]) -> set[int]:
	values: set[int] = set()
	for rule in rules:
		values |= set(rule["values"]) if "values" in rule else set(range(rule["minimum"], rule["maximum"] + 1))
	return values


class GladiatorsDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"]}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.runtime = load(curate_gladiators.RUNTIME_EVIDENCE_PATH)
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]
		cls.profile = load(PROFILE_PATH)

	def test_curator_reproduces_every_artifact(self) -> None:
		curate_gladiators.check(ROOT)

	def test_definition_validates_and_keeps_only_spatial_open(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual({"platform": "pinmame.gts3", "hardware_generation": "0x20000000000", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertEqual((1011, "737", "G4P9q-MLnOY"), (self.definition["machine"]["ipdb_id"], self.definition["machine"]["model_number"], self.definition["machine"]["opdb_id"]))

	def test_single_driver_is_claimed_and_identical(self) -> None:
		self.assertEqual(["gladiatr"], [d["id"] for d in self.definition["drivers"]])
		self.assertEqual("identical", self.definition["drivers"][0]["physical_compatibility"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		claimed = {d["id"] for d in catalog["drivers"] if d.get("machine_id") == curate_gladiators.MACHINE_ID}
		self.assertEqual({"gladiatr"}, claimed)
		self.assertIn("Game #737", self.runs["nvram-init"]["note"])

	def test_every_profile_address_is_enumerated_once_and_there_is_no_aux_board(self) -> None:
		groups = {group["id"]: allowed(group["address_rules"]) for group in self.profile["groups"]}
		self.assertEqual(groups["pinmame.input.switch"], set(self.switches))
		self.assertEqual(groups["pinmame.output.solenoid"], set(self.solenoids))
		# hw.lampCol = 4: the profile's auxiliary lamps 120-127 do not exist on this machine.
		self.assertEqual(groups["pinmame.output.lamp"] - set(range(120, 128)), set(self.lamps))
		self.assertEqual(MATRIX, set(self.lamps))
		self.assertEqual(set(range(1, 33)) | set(range(45, 49)), set(self.solenoids))

	def test_coil_names_follow_the_rom_relay_and_solenoid_test(self) -> None:
		seen = 0
		for key, address in self.named.items():
			match = re.fullmatch(r"solenoid-(\d+)-(.+)", key)
			if not match:
				continue
			seen += 1
			driver, name = int(match.group(1)), match.group(2)
			self.assertEqual(driver + 1, address)
			self.assertEqual(curate_gladiators.slug(curate_gladiators.ROM_COIL_NAMES[address]), name)
			self.assertIn(f"\"{curate_gladiators.ROM_COIL_NAMES[address]}\"", self.solenoids[address]["physical"]["notes"])
		self.assertEqual(32, seen)
		# The walk fires drivers 0-31 and then wraps back to driver 0; no driver is NOT USED.
		self.assertEqual(list(range(1, 33)) + [1], self.runs["solenoids"]["ordered_solenoid_on_sequence"])
		self.assertEqual({27}, {a for a, o in self.solenoids.items() if o["availability"] != "used"})

	def test_lamp_names_follow_the_lamp_matrix_test(self) -> None:
		pairs = note_pairs(self.runs["lamp-matrix"]["note"])
		self.assertEqual({str(address) for address in MATRIX}, set(pairs))
		for address in MATRIX:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "(NOT USED)":
					self.assertEqual("unused", self.lamps[address]["availability"])
				else:
					self.assertEqual(curate_gladiators.ROM_LAMP_NAMES[address], name)
					self.assertEqual("used", self.lamps[address]["availability"])
		self.assertEqual({80, 90, 110, 111}, {a for a, o in self.lamps.items() if o["availability"] == "unused"})

	def test_switch_names_follow_the_switch_matrix_test(self) -> None:
		pairs = note_pairs(self.runs["switch-matrix"]["note"])
		expected = MATRIX - {4}
		self.assertEqual({str(address) for address in expected}, set(pairs))
		for address in expected:
			name = pairs[str(address)]
			with self.subTest(address=address):
				if name == "(NOT USED)":
					self.assertEqual("unused", self.switches[address]["availability"])
				else:
					self.assertEqual(curate_gladiators.ROM_SWITCH_NAMES[address], name)
					self.assertEqual("used", self.switches[address]["availability"])
		self.assertIn("ALL SWITCHES OPEN", self.runs["switch-matrix"]["note"])

	def test_every_fitted_physical_switch_is_normally_open(self) -> None:
		for address, device in self.switches.items():
			if device["kind"] == "switch" and device["availability"] in ("used", "optional"):
				with self.subTest(address=address):
					self.assertIs(False, device.get("normally_closed"))

	def test_flipper_buttons_are_copied_into_82_and_83(self) -> None:
		relationships = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		self.assertEqual({("switch.flipper-column-141", "switch.matrix-83"), ("switch.flipper-column-143", "switch.matrix-82")}, relationships)
		for address in (82, 83):
			self.assertIn("cannot be driven directly", self.switches[address]["physical"]["notes"])
		self.assertEqual({141, 143}, {a for a in range(140, 148) if self.switches[a]["availability"] == "used"})
		self.assertEqual((82, 83), curate_gladiators.FLIP_SWNO)
		# Only the right button was pressed while the Relay & Solenoid Test held 32 on.
		seen = set(self.runtime["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertEqual({45, 46}, seen & {45, 46, 47, 48})

	def test_relays_flashers_and_led_lamps_follow_pinmame(self) -> None:
		self.assertEqual({23, 26, 31, 32}, {a for a, o in self.solenoids.items() if o["kind"] == "relay"})
		self.assertEqual("motor", self.solenoids[25]["kind"])
		self.assertEqual(set(curate_gladiators.FLASHER_SOLENOIDS), {a for a, o in self.solenoids.items() if o["kind"] == "flasher"})
		self.assertEqual({8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24}, set(curate_gladiators.FLASHER_SOLENOIDS))
		self.assertEqual(set(range(2, 8)) | set(range(12, 18)) | set(range(94, 98)), set(curate_gladiators.LED_LAMPS))
		for address in curate_gladiators.LED_LAMPS:
			self.assertIn("strobed LED", self.lamps[address]["physical"]["notes"])

	def test_placements_are_observed_in_range_and_only_backbox_flashers_are_omitted(self) -> None:
		placements = [
			placement for collection in ("inputs", "outputs") for device in self.definition[collection]
			for placement in (device.get("spatial") or {}).get("placements", [])
		]
		self.assertEqual(153, len(placements))
		self.assertEqual(len(placements), len({placement["id"] for placement in placements}))
		for placement in placements:
			with self.subTest(placement=placement["id"]):
				self.assertEqual("observed", placement["provenance"]["status"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1)
		omitted = sorted(
			device["binding"]["device"] for device in self.definition["inputs"] + self.definition["outputs"] if "spatial" not in device
		)
		self.assertEqual([8, 9, 19, 20, 21, 22, 24], omitted)
		self.assertEqual("not_applicable", self.lamps[112]["spatial"]["status"])
		self.assertEqual(19, len(self.solenoids[31]["spatial"]["placements"]))
		self.assertNotIn("quantity", self.solenoids[31])

	def test_placements_follow_the_bound_objects(self) -> None:
		def xy(device):
			(placement,) = device["spatial"]["placements"]
			return (placement["x"], placement["y"])

		self.assertEqual((0.902311, 0.077706), xy(self.switches[100]))  # trigger sw100 at the top of the shooter lane
		self.assertEqual((0.941176, 0.862627), xy(self.switches[24]))
		self.assertEqual(xy(self.switches[31]), xy(self.solenoids[6]))
		self.assertEqual(xy(self.switches[30]), xy(self.solenoids[23]))
		self.assertEqual(curate_gladiators.norm(*curate_gladiators.MESH_POINTS["LEDR84"]), xy(self.lamps[84]))
		self.assertEqual(curate_gladiators.norm(78.5, 1886.0), xy(self.lamps[2]))
		self.assertEqual("emitter", self.solenoids[14]["spatial"]["placements"][0]["role"])
		self.assertEqual("effect", self.solenoids[13]["spatial"]["placements"][0]["role"])

	def test_table_defects_are_recorded_on_devices_not_as_conflicts(self) -> None:
		self.assertIn("TiltSwitch = 151", self.switches[-7]["physical"]["notes"])
		excerpt = (EXCERPTS / "kiwi-script-bindings.md").read_text(encoding="utf-8")
		self.assertIn("`vpmNudge.TiltSwitch = 151`", excerpt)
		self.assertIn("`.AddSw 30, 0, 0`", excerpt)

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curate_gladiators.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curate_gladiators.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())

	def test_excerpt_digests_match(self) -> None:
		count = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				count += 1
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
		self.assertEqual(4, count)

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if d["id"] != "gladiatr" and re.search(r"\d|_", d["id"]) and len(d["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class GladiatorsRetainedEvidenceTests(unittest.TestCase):
	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import gladiators_runtime_evidence
		from pinmame_game_defs.jsonio import canonical_bytes

		review_root = gladiators_runtime_evidence.working_root()
		if not (review_root / gladiators_runtime_evidence.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Gladiators runs are not present under this review-artifacts root")
		self.assertEqual(canonical_bytes(gladiators_runtime_evidence.build(review_root)), curate_gladiators.RUNTIME_EVIDENCE_PATH.read_bytes())

	def test_placements_match_the_retained_table(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		root = Path(value).expanduser().resolve()
		if not (root / curate_gladiators.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Gladiators table is not present under this root")
		curate_gladiators.verify_retained_table(root)

	def test_retained_table_verifier_refuses_a_moved_point(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value or not (Path(value) / curate_gladiators.TABLE_RELATIVE_PATH).is_file():
			self.skipTest("retained Gladiators table is not present")
		kind, x, y = curate_gladiators.TABLE_POINTS["sw24"]
		original = dict(curate_gladiators.TABLE_POINTS)
		curate_gladiators.TABLE_POINTS["sw24"] = (kind, x + 1.0, y)
		try:
			with self.assertRaisesRegex(RuntimeError, "sw24"):
				curate_gladiators.verify_retained_table(Path(value).expanduser().resolve())
		finally:
			curate_gladiators.TABLE_POINTS.clear()
			curate_gladiators.TABLE_POINTS.update(original)


if __name__ == "__main__":
	unittest.main()
