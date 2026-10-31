"""Fail-closed tests for the Bally Mousin' Around! (1989) definition.

Each test pins one fact against the evidence that decided it: the ROM's own Coil, Single Lamps,
Switch Levels, C-Side and Motor Bank tests for names, addresses and the relay's behaviour, pinned
PinMAME's mousnGameData for the A/C bank at 12, the switch-2 copy and the flipper copy, the manual
for wiring, parts and fitment, and the retained table for the placements it observes. A regression
names the fact that broke.
"""

from __future__ import annotations

import copy
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

import curate_mousin_around as curator  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "mousin-around-1989.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "mousin-around-1989.md"
SPATIAL_PATH = ROOT / "reports" / "spatial" / "bally" / "mousin-around-1989.json"
RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "mousin-around-l4-service-and-mechanisms.json"
EXCERPTS = ROOT / "evidence" / "excerpts" / "bally.mousin-around.1989"
SCENARIOS = ROOT / "tools" / "harness-scenarios" / "system-11"

DRIVERS = {"mousn_l4": "identical", "mousn_l1": "compatible", "mousn_lu": "compatible", "mousn_l4c": "unknown"}
UNUSED_SWITCHES = {10, 45, 48, 62, 63, 64}
UNUSED_FLIPPER_COLUMN = {81, 83, 85, 86, 87, 88}
UNUSED_SOLENOIDS = {6, 24, *range(33, 45), 49, 50}
# Outputs whose spatial key is omitted, each named by a spatial blocker.
UNPLACED_LAMPS = set(range(1, 57))
UNPLACED_SOLENOIDS = {27, 30, 31, 32}
ROM_ARCHIVES = {
	"mousn_l4": "028dbe18f0183a213a88558cbd9e542283acdcbe0c14958ce50a947784923a74",
	"mousn_l1": "141200ceef7cc2ce7ea664bf0ae07ddc786a71448350e746b86f32241dc22e44",
	"mousn_lu": "64cb997c842cae7e906b69c5e22ab74689fd15f8439585d88355dfdfd92851f7",
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def folded(text: str) -> str:
	return text.replace("0", "O").replace("5", "S")


def shown_switch_names(note: str) -> dict[str, str]:
	shown = {}
	for item in note.split("while held: ", 1)[1].rstrip(".").split("; "):
		address, rest = item.split(" = ", 1)
		shown[address] = rest.rsplit(" / ", 1)[0]
	return shown


def evidence_files() -> list[Path]:
	return [RUNTIME_PATH] + [curator.variant_evidence_path(game) for game in curator.VARIANT_GAMES]


class MousinAroundDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {i["binding"]["device"]: i for i in cls.definition["inputs"] if i["binding"]["group"] == "pinmame.input.switch"}
		cls.solenoids = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {o["binding"]["device"]: o for o in cls.definition["outputs"] if o["binding"]["group"] == "pinmame.output.lamp"}
		cls.sources = {s["id"]: s for s in cls.definition["sources"]}
		cls.runtime = load(RUNTIME_PATH)
		cls.runs = cls.runtime["runtime"]["observations"]["runs"]
		cls.named = cls.runtime["runtime"]["observations"]["named_output_addresses"]

	def test_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_definition_validates_and_keeps_its_two_open_requirements(self) -> None:
		self.assertEqual([], validate_machine(self.definition, ROOT))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("0x100", self.definition["controller"]["hardware_generation"])
		catalog = load(ROOT / "catalog" / "pinmame.json")
		entry = next(m for m in catalog["machines"] if m["id"] == curator.MACHINE_ID)
		self.assertEqual(88, entry["completion_score"])
		self.assertEqual("machines/partial/bally/mousin-around-1989.json", entry["definition"])
		self.assertEqual(hashlib.sha256(DEFINITION_PATH.read_bytes()).hexdigest(), entry["definition_sha256"])
		self.assertFalse(curator.AUTHOR_READY_PATH.exists())

	def test_driver_tree_is_exactly_the_mousn_clone_tree(self) -> None:
		compatibility = {d["id"]: d["physical_compatibility"] for d in self.definition["drivers"]}
		self.assertEqual(DRIVERS, compatibility)
		catalog = load(ROOT / "catalog" / "pinmame.json")
		owners = {d["id"]: d.get("machine_id") for d in catalog["drivers"] if d["id"].startswith("mousn_")}
		self.assertEqual(set(DRIVERS), set(owners))
		self.assertEqual({curator.MACHINE_ID}, set(owners.values()))
		notes = {d["id"]: d["variant_notes"] for d in self.definition["drivers"]}
		self.assertIn("RAMP DRAIN", notes["mousn_l1"])
		self.assertIn("RAMP DRAIN", notes["mousn_lu"])
		self.assertIn("not in the local ROM corpus", notes["mousn_l4c"])

	def test_variant_service_tests_differ_only_at_switch_37(self) -> None:
		reference = shown_switch_names(self.runs["switch-levels"]["note"])
		for game in curator.VARIANT_GAMES:
			evidence = load(curator.variant_evidence_path(game))
			self.assertEqual(game, evidence["runtime"]["game"])
			runs = evidence["runtime"]["observations"]["runs"]
			for name in ("coil-test", "single-lamps"):
				self.assertIn("identical to the mousn_l4 run", runs[name]["note"], (game, name))
			self.assertIn("DIFFERENT from the mousn_l4 run", runs["switch-levels"]["note"], game)
			shown = shown_switch_names(runs["switch-levels"]["note"])
			differing = {address for address in reference if shown[address] != reference[address]}
			self.assertEqual({"37"}, differing, game)
			self.assertEqual("RAMP DRAIN", shown["37"], game)
			self.assertEqual("MADE LEFT RAMP", reference["37"])

	def test_every_controller_address_is_enumerated(self) -> None:
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual(
			[("display.upper-alphanumeric", 0, 0, 16), ("display.lower-alphanumeric", 1, 20, 16)],
			[(d["id"], d["controller_index"], d["segment_start"], d["width"]) for d in self.definition["displays"]],
		)

	def test_coil_names_follow_the_rom_coil_test(self) -> None:
		self.assertEqual(list(curator.COIL_TEST_ORDER), self.runs["coil-test"]["ordered_solenoid_on_sequence"])
		for step, address in enumerate(curator.COIL_TEST_ORDER, start=1):
			key = f"coil-{step:02d}-{slug(folded(curator.ROM_COIL_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)
			self.assertIn(curator.ROM_COIL_NAMES[address], self.solenoids[address]["physical"]["notes"])

	def test_lamp_names_follow_the_single_lamps_test(self) -> None:
		for address in range(1, 65):
			key = f"lamp-{address:02d}-{slug(folded(curator.ROM_LAMP_NAMES[address]))}"
			self.assertEqual(address, self.named[key], key)
		self.assertEqual(curator.FOLDED_LAMP_NAMES, {a for a, name in curator.ROM_LAMP_NAMES.items() if folded(name) != name})

	def test_switch_names_follow_the_switch_levels_test(self) -> None:
		shown = shown_switch_names(self.runs["switch-levels"]["note"])
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertEqual(folded(name), shown[str(address)], address)
		self.assertEqual("RIGHT FLIPPER", shown["82"])
		self.assertEqual("LEFT FLIPPER", shown["84"])
		for address in UNUSED_FLIPPER_COLUMN:
			self.assertEqual("SWITCH LEVELS", shown[str(address)], address)

	def test_ac_bank_is_published_at_25_to_32_and_copied_into_switch_2(self) -> None:
		for pair in range(1, 9):
			a, c = self.solenoids[pair], self.solenoids[pair + 24]
			self.assertEqual(f"{pair:02d}A", [x["value"] for x in a["aliases"] if x["namespace"] == "manual.address"][0])
			self.assertEqual(f"{pair:02d}C", [x["value"] for x in c["aliases"] if x["namespace"] == "manual.address"][0])
		relay = self.solenoids[curator.AC_RELAY]
		self.assertEqual("relay", relay["kind"])
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"]}
		self.assertIn((relay["id"], "switch.matrix-2"), relations)
		switch = self.switches[2]
		self.assertEqual(["internal.ac-relay-feedback"], switch["roles"])
		self.assertIs(False, switch["normally_closed"])
		self.assertIn("S11_MUXSW2", switch["physical"]["notes"])
		self.assertIn("run c-side-test", switch["physical"]["notes"])

	def test_c_side_test_alternates_the_relay_and_reads_switch_2(self) -> None:
		run = self.runs["c-side-test"]
		self.assertIn(12, run["solenoid_addresses_seen"])
		self.assertIn("upper display 'C-SIDE SW. TEST', lower display 'O8'", run["note"])
		self.assertRegex(run["note"], r"energized [5-9] times for 1\.9\d+-1\.9\d+ s")
		self.assertIn("'SELECTED C-SIDE' and the lower 'C-SIDE O8'", run["note"])
		self.assertIn("'SELECTED A-SIDE' and 'O8'", run["note"])

	def test_motor_bank_relay_is_stopped_by_its_limit_switches(self) -> None:
		self.assertEqual("relay", self.solenoids[11]["kind"])
		bank = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.motor-bank")
		self.assertTrue({"switch.matrix-43", "switch.matrix-50"} <= set(bank["sensors"]))
		self.assertIn(self.solenoids[11]["id"], bank["actuators"])
		self.assertIn("'OO ERROR' after the fall", self.runs["motor-bank-no-switch"]["note"])
		self.assertIn("43=1", self.runs["motor-bank-up-down-up"]["note"])

	def test_special_solenoids_have_no_emulated_switch_map(self) -> None:
		self.assertFalse(any(r["id"].startswith("relationship.special-solenoid-") for r in self.definition["relationships"]))
		self.assertTrue({17, 18, 19, 20, 21} <= set(self.runs["gameplay"]["solenoid_addresses_seen"]))
		for switch, solenoid in ((52, 17), (53, 19), (54, 21)):
			self.assertIn(f"switch {switch} fired solenoid {solenoid}", self.runs["gameplay"]["note"])

	def test_flipper_buttons_are_copied_into_the_flipper_switches(self) -> None:
		relations = {(r["source"], r["destination"]) for r in self.definition["relationships"] if "flipper-column" in r["id"]}
		self.assertEqual({("switch.flipper-column-82", "switch.matrix-57"), ("switch.flipper-column-84", "switch.matrix-58")}, relations)
		self.assertEqual((58, 57), curator.FLIP_SWNO)
		for address in (57, 58):
			self.assertIn("cannot drive it directly", self.switches[address]["physical"]["notes"])
		self.assertEqual("Right Flipper", self.switches[57]["label"])
		self.assertEqual("Left Flipper", self.switches[58]["label"])

	def test_every_fitted_switch_is_normally_open(self) -> None:
		self.assertEqual(curator.UNUSED_SWITCHES, UNUSED_SWITCHES)
		for address in list(range(1, 65)) + list(range(81, 89)):
			device = self.switches[address]
			if address in UNUSED_SWITCHES | UNUSED_FLIPPER_COLUMN:
				self.assertEqual("unused", device["availability"], address)
				self.assertNotIn("normally_closed", device, address)
			else:
				self.assertIn(device["availability"], ("used", "optional"), address)
				self.assertIs(False, device["normally_closed"], address)
		self.assertEqual("optional", self.switches[5]["availability"])
		self.assertEqual({5}, {a for a, d in self.switches.items() if d["availability"] == "optional"})

	def test_switch_48_keeps_the_manuals_not_used(self) -> None:
		device = self.switches[48]
		self.assertEqual("Not Used (Matrix Position 48)", device["label"])
		self.assertIn("MADE LEFT RAMP", device["physical"]["notes"])
		self.assertIn("the manual's \"Not Used\" stands", device["physical"]["notes"])
		self.assertIn("Not Used", (EXCERPTS / "switch-matrix.md").read_text(encoding="utf-8"))

	def test_output_availability(self) -> None:
		self.assertEqual(UNUSED_SOLENOIDS, {a for a, d in self.solenoids.items() if d["availability"] == "unused"})
		self.assertEqual({64}, {a for a, d in self.lamps.items() if d["availability"] == "unused"})
		self.assertEqual("NOT USED", curator.ROM_COIL_NAMES[6])
		self.assertEqual("NOT USED", curator.ROM_LAMP_NAMES[64])
		for address in (9, 10):
			self.assertEqual("gi", self.solenoids[address]["kind"])
		self.assertEqual("virtual", self.solenoids[23]["kind"])
		self.assertEqual("used", self.solenoids[23]["availability"])

	def test_unplaced_outputs_are_omitted_and_named_by_a_blocker(self) -> None:
		self.assertEqual(UNPLACED_LAMPS, {a for a, d in self.lamps.items() if "spatial" not in d})
		self.assertEqual(UNPLACED_SOLENOIDS, {a for a, d in self.solenoids.items() if "spatial" not in d})
		report = load(SPATIAL_PATH)
		omitted = {(o["group"], o["address"]) for o in report["omitted_outputs"]}
		expected = {("pinmame.output.lamp", a) for a in UNPLACED_LAMPS} | {("pinmame.output.solenoid", a) for a in UNPLACED_SOLENOIDS}
		self.assertEqual(expected, omitted)
		blockers = " ".join(report["blockers"])
		for phrase in ("Lamps 1-7 and 9-48", "Lamp 8 (Jackpot)", "Lamps 49-56", "Solenoids 27, 30 and 31", "Solenoid 32"):
			self.assertIn(phrase, blockers)
		self.assertEqual({"observed": report["placement_count"]}, report["placement_status_counts"])
		self.assertEqual(36, len(self.solenoids[10]["spatial"]["placements"]))
		self.assertNotIn("quantity", self.solenoids[10]["physical"])

	def test_regeneration_refuses_to_replace_an_author_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			stale = root / curator.STALE_DEFINITION_PATH.relative_to(ROOT)
			stale.parent.mkdir(parents=True)
			stale.write_bytes(b"{}\n")
			with self.assertRaisesRegex(RuntimeError, "refusing to replace the author-ready"):
				curator.generate(root)
			self.assertEqual(b"{}\n", stale.read_bytes())
			self.assertFalse((root / curator.DEFINITION_PATH.relative_to(ROOT)).exists())
			with self.assertRaisesRegex(RuntimeError, "stale artifact exists"):
				curator.check(root)

	def test_check_refuses_drift(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			curator.generate(root)
			curator.check(root)
			definition = root / curator.DEFINITION_PATH.relative_to(ROOT)
			definition.write_bytes(definition.read_bytes().replace(b'"partial"', b'"author_ready"', 1))
			with self.assertRaisesRegex(RuntimeError, "drifted from its deterministic curator"):
				curator.check(root)

	def test_extraction_verifier_refuses_a_refreshed_manifest(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			extraction = root / curator.EXTRACTION_RELATIVE_PATH
			extraction.mkdir(parents=True)
			(extraction / "script.vbs").write_bytes(b"altered\n")
			curator.write_extraction_manifest(root)
			with self.assertRaisesRegex(RuntimeError, "not the pinned one"):
				curator.verify_extraction_manifest(root)

	def test_manual_and_table_sources_carry_acquisition_provenance(self) -> None:
		manual = self.sources[curator.MANUAL_SOURCE]
		self.assertEqual(curator.MANUAL_SHA256, manual["sha256"])
		self.assertEqual("ipdb.1635", manual["source_id"])
		self.assertRegex(manual["acquired_at"], r"^2026-10-31T\d\d:\d\d:\d\dZ$")
		self.assertEqual(curator.RUN_AT["mousn_l4"], self.sources[curator.RUNTIME_SOURCE]["acquired_at"])
		for game in curator.VARIANT_GAMES:
			self.assertEqual(curator.RUN_AT[game], self.sources[curator.variant_source(game)]["acquired_at"])
		self.assertIn("https://www.ipdb.org/machine.cgi?id=1635", manual["locator"])
		self.assertIn("https://www.ipdb.org/files/1635/", manual["locator"])
		self.assertIn(curator.IPDB_PAGE_SHA256, manual["locator"])
		self.assertEqual(curator.EXTRACTION_MANIFEST_SHA256, self.sources[curator.VPX_EXTRACTION_SOURCE]["sha256"])
		self.assertIn('cGameName = "mousn_l4"', self.sources[curator.VPX_SCRIPT_SOURCE]["locator"])
		for key in (curator.MANUAL_SOURCE, curator.VPX_TABLE_SOURCE, curator.VPX_SCRIPT_SOURCE):
			self.assertTrue(self.sources[key]["license"] and self.sources[key]["attribution"], key)

	def test_corpus_scripts_are_pinned_blobs(self) -> None:
		corpus = self.sources[curator.VPX_CORPUS_SOURCE]
		standalone = self.sources[curator.VPX_STANDALONE_SOURCE]
		self.assertEqual("ffec259adb8149d5b4c3424770f04017905c24b069196260da60e975d42a2e72", corpus["sha256"])
		self.assertEqual("c3b3d0bde70f1aa369cee7e6518f4808cc9c76d762177add3168f7b81ea6c7e3", standalone["sha256"])
		self.assertEqual(curator.VPXTABLE_REVISION, corpus["revision"])
		self.assertEqual(curator.STANDALONE_REVISION, standalone["revision"])
		self.assertIn(
			"The retained SHA-256 is the repository checkout's CRLF materialization; the linked Git blob is the identical "
			"LF-normalized text (SHA-256 d9a9ff5f339c7836366501167d7ff33682c2f00ebcaca05a90993ab3b88c2bb2)",
			standalone["locator"],
		)

	def test_excerpt_digests_match_and_were_reviewed(self) -> None:
		cited = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				cited.add(path.name)
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				self.assertNotIn(b"\r", path.read_bytes(), excerpt["path"])
				self.assertIs(True, excerpt["reviewed"], excerpt["path"])
				self.assertTrue(excerpt["transcribed_by"].startswith("curator"), excerpt["path"])
		self.assertEqual({path.name for path in EXCERPTS.glob("*.md")}, cited)

	def test_scenarios_are_lf_and_match_their_recorded_digests(self) -> None:
		referenced = set()
		for path in evidence_files():
			record = load(path)
			for run in record["runtime"]["raw_runs"]:
				scenario = ROOT / run["scenario_path"]
				referenced.add(scenario.name)
				data = scenario.read_bytes()
				self.assertNotIn(b"\r", data, scenario.name)
				self.assertEqual(run["scenario_sha256"], hashlib.sha256(data).hexdigest(), scenario.name)
		self.assertEqual({path.name for path in SCENARIOS.glob("mousn-*.json")}, referenced)

	def test_runtime_sources_pin_the_evidence_files(self) -> None:
		for key, path in ((curator.RUNTIME_SOURCE, RUNTIME_PATH),) + tuple(
			(curator.variant_source(game), curator.variant_evidence_path(game)) for game in curator.VARIANT_GAMES
		):
			self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.sources[key]["sha256"], key)
		for path, game in zip(evidence_files(), ("mousn_l4", *curator.VARIANT_GAMES)):
			self.assertEqual(ROM_ARCHIVES[game], load(path)["runtime"]["rom_archive_sha256"], game)

	def test_no_other_machine_identity_leaks_in(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		foreign = {d["id"] for d in catalog["drivers"] if not d["id"].startswith("mousn_") and len(d["id"]) >= 5 and "_" in d["id"]}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8")]
		texts += [path.read_text(encoding="utf-8") for path in EXCERPTS.glob("*.md")]
		for text in texts:
			words = set(re.findall(r"\b[a-z0-9]+_[a-z0-9_]+\b", text))
			self.assertEqual(set(), words & foreign)


class MousinAroundRetainedEvidenceTests(unittest.TestCase):
	def _review_root(self) -> Path:
		if not os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT not configured")
		import mousin_around_runtime_evidence as builder

		review_root = builder.working_root()
		if not (review_root / builder.RUNTIME_RELATIVE).is_dir():
			self.skipTest("retained Mousin' Around runs are not present under this review-artifacts root")
		return review_root

	def test_runtime_evidence_matches_the_raw_runs(self) -> None:
		review_root = self._review_root()
		import mousin_around_runtime_evidence as builder
		from pinmame_game_defs.jsonio import canonical_bytes

		manifest_bytes, evidence, variants, _ = builder.build(review_root)
		self.assertEqual((review_root / builder.RUNTIME_RELATIVE / "manifest.json").read_bytes(), manifest_bytes)
		self.assertEqual(canonical_bytes(evidence), RUNTIME_PATH.read_bytes())
		for game, record in variants.items():
			self.assertEqual(canonical_bytes(record), curator.variant_evidence_path(game).read_bytes())

	def test_runtime_builder_refuses_substituted_frames_and_drifted_runs(self) -> None:
		review_root = self._review_root()
		import mousin_around_runtime_evidence as builder

		def on_c_side(mutate):
			def changed(runs: Path, game: str, name: str) -> dict:
				run = builder.load_run(runs, game, name)
				if game == builder.GAME and name == "c-side-test":
					run = copy.deepcopy(run)
					mutate(run)
				return run
			return changed

		def substitute_a_side(run: dict) -> None:
			upper = [e for e in run["events"] if e["event"] == "display" and e.get("index") == 0 and isinstance(e.get("segments"), list)]
			reading = lambda event: builder.normalized(builder.decode_alpha(event["segments"]))  # noqa: E731
			a_side = next(e["segments"] for e in upper if reading(e) == "SELECTED A-SIDE")
			for event in upper:
				if reading(event) == "SELECTED C-SIDE":
					event["segments"] = list(a_side)

		def drop_relay(run: dict) -> None:
			run["events"] = [e for e in run["events"] if not (e["event"] == "solenoid" and e.get("number") == 12)]

		with self.assertRaisesRegex(RuntimeError, "carries other segment values than the pinned frame"):
			builder.build(review_root, load=on_c_side(substitute_a_side))
		with self.assertRaisesRegex(RuntimeError, "are not complete alternations"):
			builder.build(review_root, load=on_c_side(drop_relay))

		def drifted(runs: Path, game: str, name: str) -> dict:
			run = json.loads(builder.run_file(runs, game, name).read_text(encoding="utf-8"))
			run["scenario"]["sha256"] = "0" * 64
			with tempfile.TemporaryDirectory() as temporary:
				builder.run_file(Path(temporary), game, name).write_text(json.dumps(run), encoding="utf-8")
				return builder.load_run(Path(temporary), game, name)

		with self.assertRaisesRegex(RuntimeError, "scenario drift"):
			builder.build(review_root, load=drifted)

	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curator.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT not configured")
		if not (root / curator.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("retained Mousin' Around extraction is not present under this root")
		curator.verify_extraction_manifest(root)
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())

	def test_retained_manual_and_ipdb_page_match_their_hashes(self) -> None:
		value = os.environ.get("PINMAME_MANUALS_ROOT")
		if not value:
			self.skipTest("PINMAME_MANUALS_ROOT not configured")
		folder = Path(value) / "by-machine" / curator.MACHINE_ID / "ipdb-1635"
		manual = folder / "Bally_1989_Mousin_Around_Manual.pdf"
		if not manual.is_file():
			self.skipTest("retained Mousin' Around manual is not present under this root")
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256(manual.read_bytes()).hexdigest())
		page = folder / "machine-1635.wayback-20251204104221.html"
		self.assertEqual(curator.IPDB_PAGE_SHA256, hashlib.sha256(page.read_bytes()).hexdigest())

	def test_rom_archives_match_the_runtime_evidence(self) -> None:
		value = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
		if not value:
			self.skipTest("PINMAME_ROM_LIBRARY_ROOT not configured")
		for game, digest in ROM_ARCHIVES.items():
			archive = Path(value) / f"{game}.zip"
			if not archive.is_file():
				self.skipTest(f"{archive.name} is not present under this ROM library")
			self.assertEqual(digest, hashlib.sha256(archive.read_bytes()).hexdigest(), game)


if __name__ == "__main__":
	unittest.main()
