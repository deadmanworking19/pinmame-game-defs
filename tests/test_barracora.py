from __future__ import annotations

import copy
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_against_schema, validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import barracora_runtime_evidence as runtime_evidence  # noqa: E402
import curate_barracora as curator  # noqa: E402

EXCERPTS = ROOT / "evidence/excerpts" / curator.MACHINE_ID
ROOT_VARIABLES = ["PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT",
	"PINMAME_SOURCE_ROOT", "PINMAME_VPX_SCRIPTS_ROOT", "PINMAME_ROM_LIBRARY_ROOT"]


def tempdir():
	return tempfile.TemporaryDirectory(dir=os.environ.get("PINMAME_TEST_TMP_ROOT"))


def table_after(name: str, heading: str) -> list[list[str]]:
	"""Body rows of the first Markdown table after ``heading`` in an excerpt."""
	lines = (EXCERPTS / name).read_text(encoding="utf-8").splitlines()
	start = lines.index(heading)
	rows: list[list[str]] = []
	for line in lines[start + 1:]:
		if line.startswith("|"):
			cells = [c.strip() for c in line.strip("|").split("|")]
			if not set(cells[0]) <= {"-"}:
				rows.append(cells)
		elif rows:
			break
	return rows[1:]


class BarracoraCurationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.game = curator.build()
		by_group = lambda group, key: {d["binding"]["device"]: d for d in cls.game[key] if d["binding"]["group"] == group}
		cls.switches = by_group("pinmame.input.switch", "inputs")
		cls.dips = by_group("pinmame.input.dip", "inputs")
		cls.coils = by_group("pinmame.output.solenoid", "outputs")
		cls.lamps = by_group("pinmame.output.lamp", "outputs")
		cls.ids = {d["id"] for key in ["inputs", "outputs"] for d in cls.game[key]}

	def test_identity_single_driver_and_catalog_claim(self):
		identity = {k: v for k, v in self.game["machine"].items() if k != "playfield"}
		self.assertEqual(identity, {"id": "williams.barracora.1981", "name": "Barracora", "manufacturer": "Williams", "year": 1981,
			"model_number": "510", "kind": "physical_pinball", "ipdb_id": 177, "opdb_id": "GRo7K-MQ4e3"})
		self.assertEqual([(d["id"], d["physical_compatibility"]) for d in self.game["drivers"]], [("barra_l1", "identical")])
		self.assertEqual(self.game["controller"], {"platform": "pinmame.system-7", "hardware_generation": "0x10000", "inversion_applied_by_emulator": True})
		catalog = load_json(ROOT / "catalog/pinmame.json")
		claims = [m for m in catalog["machines"] if m["id"] == curator.MACHINE_ID]
		self.assertEqual(len(claims), 1)
		self.assertEqual(claims[0]["definition"], curator.DEFINITION.as_posix())
		self.assertEqual(claims[0]["missing"], ["spatial_placement"])
		self.assertEqual(claims[0]["completion_score"], 94)
		self.assertEqual({d["id"] for d in catalog["drivers"] if d["machine_id"] == curator.MACHINE_ID}, {"barra_l1"})
		for directory in ["author-ready", "stubs"]:
			self.assertEqual(list((ROOT / "machines" / directory).glob("**/barracora*")), [])

	def test_every_legal_address_has_a_disposition(self):
		self.assertEqual(set(self.switches), {*range(-7, -2), *range(1, 65), *range(81, 89)})
		self.assertEqual(set(self.dips), {1, 2, *range(9, 25)})
		self.assertEqual(set(self.lamps), set(range(1, 97)))
		self.assertEqual(set(self.coils), {*range(1, 26), *range(45, 49), *range(51, 61)})
		availability = lambda devices, n: (devices[n]["kind"], devices[n]["availability"])
		for n in range(1, 49):
			expected = ("virtual", "used") if n in {34, 35} else ("switch", "used")
			self.assertEqual(availability(self.switches, n), expected, n)
		for n in range(49, 65):
			self.assertEqual(availability(self.switches, n), ("switch", "unused"), n)
			self.assertEqual(self.switches[n]["spatial"]["reason"], "unused")
		for n in range(81, 89):
			self.assertEqual(availability(self.switches, n), ("virtual", "used" if n in {82, 84} else "unused"), n)
		for n in range(-7, -3):
			self.assertEqual(availability(self.switches, n), ("switch", "used"), n)
			self.assertEqual(self.switches[n]["roles"], ["service"])
		self.assertEqual(availability(self.switches, -3), ("virtual", "optional"))
		for n in [1, 2]:
			self.assertEqual(availability(self.dips, n), ("dip_switch", "used"))
		for n in range(9, 25):
			self.assertEqual(availability(self.dips, n), ("virtual", "optional"))
			self.assertIn("DS1,DS2", self.dips[n]["physical"]["notes"])
		for n in range(1, 65):
			self.assertEqual(availability(self.lamps, n), ("lamp", "used"), n)
		for n in range(65, 97):
			self.assertEqual(availability(self.lamps, n), ("lamp", "unused"), n)
		for n in range(1, 23):
			self.assertEqual(availability(self.coils, n), ("coil", "used"), n)
		for n in [23, 24, *range(51, 61)]:
			self.assertEqual(availability(self.coils, n), ("virtual", "unused"), n)
		self.assertEqual(availability(self.coils, 25), ("relay", "used"))
		for n in range(45, 49):
			self.assertEqual(availability(self.coils, n), ("virtual", "used"), n)

	def test_switch_wiring_and_names_follow_the_booklet_tables(self):
		columns = {int(r[0]): r for r in table_after("switch-matrix.md", "## Figure 5 column headers (column number, wire colour, 2J2 pin)")}
		rows = {int(r[0]): r for r in table_after("switch-matrix.md", "## Figure 5 row headers (row number, wire colour, 2J3 pin)")}
		self.assertEqual((len(columns), len(rows)), (8, 8))
		for n in range(1, 65):
			if n in {34, 35}:
				self.assertNotIn("wiring", self.switches[n])
				continue
			col, row = divmod(n - 1, 8)
			wiring = self.switches[n]["wiring"]
			self.assertEqual((wiring["drive_wire"], wiring["drive_connection"]), (columns[col + 1][1], columns[col + 1][2]), n)
			self.assertEqual((wiring["return_wire"], wiring["return_connection"]), (rows[row + 1][1], rows[row + 1][2]), n)
		chart = table_after("switch-matrix.md", "## Figure 3 switch chart (as printed)")
		self.assertEqual(len(chart), 48)
		for number, function in chart:
			expected = re.sub(r" \([0-9,/]+\)$", "", function)
			label = self.switches[int(number.lstrip("*"))]["label"]
			self.assertTrue(label == expected or label.startswith(expected + " ("), (number, label))

	def test_lamp_wiring_and_names_follow_figure_1(self):
		columns = {int(r[0]): r for r in table_after("lamp-matrix.md", "## Column headers (as printed: column number, wire colour, 2J5 pin)")}
		rows = {int(r[0]): r for r in table_after("lamp-matrix.md", "## Row headers (as printed; the wire colour is printed `RED-` / colour on two lines)")}
		for n in range(1, 65):
			col, row = divmod(n - 1, 8)
			wiring = self.lamps[n]["wiring"]
			self.assertEqual((wiring["drive_wire"], wiring["drive_connection"]), (columns[col + 1][1], columns[col + 1][2]), n)
			self.assertEqual((wiring["return_wire"], wiring["return_connection"]), (rows[row + 1][1], rows[row + 1][2]), n)
		self.assertEqual(self.lamps[57]["label"], "Bonus 4")
		self.assertEqual(self.lamps[11]["label"], "BARRACORA RR")
		for n in range(1, 7):
			self.assertEqual((self.lamps[n]["roles"], self.lamps[n]["physical"]["location"]), (["backbox"], "backbox insert board"), n)
			self.assertEqual(self.lamps[n]["physical"]["quantity"], 2 if n == 1 else 1)
			self.assertEqual(self.lamps[n]["spatial"]["reason"], "cabinet_or_service")
		for n in range(7, 65):
			self.assertEqual(self.lamps[n]["physical"]["location"], "playfield", n)
			self.assertNotIn("quantity", self.lamps[n]["physical"])
		self.assertIn("REN-GRN", self.lamps[5]["physical"]["notes"])

	def test_solenoid_wiring_follows_table_4(self):
		printed = {}
		for number, function, wire, connections, transistor, part in table_after("solenoid-connections.md", "## Table 4. Solenoid Connections (all rows, printed order)"):
			if number == "(blank)" or function == "Top Eject Hole":
				continue
			printed[int(number.lstrip("*"))] = (function, wire, connections, transistor, part)
		self.assertEqual(set(printed), set(range(1, 23)))
		for n, (function, wire, connections, transistor, part) in printed.items():
			coil = self.coils[n]
			self.assertTrue(coil["label"] == function or coil["label"].startswith(function + " ("), n)
			self.assertEqual((coil["wiring"]["drive_wire"], coil["wiring"]["driver_transistor"], coil["physical"]["part_number"]), (wire, transistor, part), n)
			self.assertEqual(coil["wiring"]["drive_connection"], "2P11-7, 8P3-3" if n == 3 else connections, n)
		self.assertIn("8P3-3", self.coils[3]["physical"]["notes"])
		self.assertIn("Top Eject Hole", self.coils[1]["physical"]["notes"])
		for n in [15, 16]:
			self.assertEqual((self.coils[n]["roles"], self.coils[n]["spatial"]["reason"]), (["cabinet"], "cabinet_or_service"))
		self.assertEqual((self.coils[25]["roles"], self.coils[25]["spatial"]["reason"]), (["internal"], "internal_nonvisual"))
		self.assertIn("Z1", self.coils[25]["physical"]["notes"])

	def test_service_selectors_pair_every_printed_solenoid_with_its_public_address(self):
		mapping = load_json(ROOT / curator.RUNTIME)["runtime"]["observations"]["physical_service_solenoid_to_public"]
		self.assertEqual({int(k): v for k, v in mapping.items()}, {n: n for n in range(1, 26)})

	def test_polarity_and_switch_types(self):
		for n, d in self.switches.items():
			if "normally_closed" in d:
				self.assertIs(d["normally_closed"], False, n)
		for n in [*range(-7, -3), *(a for a in range(1, 49) if a not in {34, 35})]:
			self.assertIs(self.switches[n]["normally_closed"], False, n)
		types = {n: d["physical"].get("switch_type") for n, d in self.switches.items() if 1 <= n <= 48 and n not in {34, 35}}
		self.assertEqual({n: t for n, t in types.items() if t}, {1: "tilt", 2: "tilt", 3: "button", 7: "tilt", 36: "tilt"})
		self.assertEqual({n: self.switches[n]["physical"]["switch_type"] for n in range(-7, -3)}, {-7: "button", -6: "other", -5: "button", -4: "button"})
		for n in range(41, 49):
			self.assertIn("Closed while the target is down", self.switches[n]["physical"]["notes"])

	def test_specials_relationships_mechanisms_and_displays(self):
		relationships = {(r["source"], r["destination"]) for r in self.game["relationships"]}
		expected = {(self.switches[s]["id"], self.coils[c]["id"]) for s, c in {20: 18, 21: 19, 22: 20, 29: 21, 30: 22}.items()}
		expected |= {(self.switches[82]["id"], self.switches[35]["id"]), (self.switches[84]["id"], self.switches[34]["id"])}
		self.assertEqual(relationships, expected)
		mechanisms = {m["id"]: m for m in self.game["mechanisms"]}
		self.assertEqual(len(mechanisms), 14)
		actuators = [a for m in mechanisms.values() for a in m["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))
		for m in mechanisms.values():
			self.assertTrue(set(m["actuators"]) | set(m["sensors"]) <= self.ids, m["id"])
		self.assertEqual(mechanisms["mech.upper-eject-hole-gate"]["actuators"], [self.coils[17]["id"]])
		self.assertEqual(set(mechanisms["mech.b-a-rr-drop-target-bank"]["actuators"]), {self.coils[n]["id"] for n in (1, 2, 3, 9)})
		self.assertEqual(set(mechanisms["mech.a-c-o-r-a-drop-target-bank"]["actuators"]), {self.coils[n]["id"] for n in (4, 5, 6, 7, 8, 10)})
		self.assertEqual(set(mechanisms["mech.ball-ramp-and-outhole"]["sensors"]), {self.switches[n]["id"] for n in (12, 13, 14, 15, 16)})
		self.assertEqual([(d["controller_index"], d["segment_start"], d["width"]) for d in self.game["displays"]],
			[(2, 1, 7), (3, 9, 7), (0, 21, 7), (1, 29, 7), (4, 0, 1), (5, 8, 1), (6, 20, 1), (7, 28, 1)])
		self.assertEqual(self.game["conflicts"], [])

	def test_sources_excerpts_and_schema(self):
		curator.verify_files()
		self.assertEqual(validate_against_schema(self.game, ROOT / "schemas/machine.schema.json", "game"), [])
		self.assertEqual(validate_machine(self.game, ROOT), [])
		self.assertEqual(validate_against_schema(load_json(ROOT / curator.RUNTIME), ROOT / "schemas/evidence.schema.json", "runtime"), [])
		sources = {s["id"]: s for s in self.game["sources"]}
		for identifier, revision in [(curator.MANUAL, "16P-510-103"), (curator.DRAWINGS, "game 510 drawing set"), (curator.PARTS, "16P-510-110 October 1981")]:
			self.assertEqual((sources[identifier]["kind"], sources[identifier]["revision"]), ("manual", revision))
			self.assertIn("web.archive.org", sources[identifier]["locator"])
		excerpts = [e for s in sources.values() for e in s.get("excerpts", [])]
		self.assertEqual({Path(e["path"]).name for e in excerpts}, set(curator.EXCERPTS))
		for e in excerpts:
			self.assertEqual(e["method"], "manual")
			self.assertTrue(e["transcribed_by"].startswith("curator; "))
			self.assertEqual(e["reviewed"], Path(e["path"]).name not in curator.UNREVIEWED)
		self.assertIs(sources[curator.SCRIPT]["known_working"], True)
		self.assertIs(sources[curator.OLD_SCRIPT]["known_working"], False)
		self.assertIs(sources[curator.EMBEDDED]["known_working"], False)
		for identifier in [curator.SCRIPT, curator.OLD_SCRIPT]:
			self.assertTrue(sources[identifier]["uri"].startswith(f"https://github.com/sverrewl/vpxtable_scripts/blob/{curator.SCRIPT_REVISION}/Barracora%20%28Williams%201981%29"))
		self.assertEqual(sources[curator.RUN]["sha256"], curator.RUNTIME_SHA)
		self.assertEqual([identifier for identifier, source in sources.items() if not source.get("acquired_at")], [])

	def test_partial_gate_names_only_spatial_placement(self):
		self.assertEqual(self.game["coverage"]["status"], "partial")
		self.assertEqual(self.game["coverage"]["missing"], ["spatial_placement"])
		self.assertEqual(self.game["coverage"]["dimensions"]["spatial_placement"], "observed")
		report = curator.spatial.report(self.game, ROOT)
		unplaced = set(report["unplaced_devices"])
		self.assertTrue({self.lamps[n]["id"] for n in range(7, 65)} <= unplaced)
		for group in ["inputs", "outputs"]:
			for d in self.game[group]:
				spatial = d.get("spatial")
				if spatial is None:
					self.assertIn(d["id"], unplaced)
				elif spatial["status"] != "not_applicable":
					self.assertTrue(spatial.get("placements"), d["id"])
					self.assertNotIn(d["id"], unplaced)
		placed = [d for key in ["inputs", "outputs"] for d in self.game[key] if d.get("spatial", {}).get("placements")]
		self.assertEqual(len(placed), 47)
		self.assertTrue(all(p["provenance"]["status"] == "observed" for d in placed for p in d["spatial"]["placements"]))
		promoted = copy.deepcopy(self.game)
		promoted["coverage"]["status"] = "author_ready"
		promoted["coverage"]["missing"] = []
		self.assertTrue(any("spatial" in e for e in validate_machine(promoted, ROOT)))
		self.assertIn("## What would complete this record", curator.KNOWLEDGE_TEXT)

	def _fixture(self, destination: Path) -> None:
		files = [*curator.expected_artifacts(), curator.RUNTIME, curator.READINGS, curator.spatial.SEED]
		files += [Path("evidence/excerpts") / curator.MACHINE_ID / n for n in curator.EXCERPTS]
		files += [Path(r["scenario_path"]) for r in load_json(ROOT / curator.RUNTIME)["runtime"]["raw_runs"]]
		for rel in files:
			(destination / rel).parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(ROOT / rel, destination / rel)

	def test_determinism_and_local_guards(self):
		curator.check()
		self.assertEqual((ROOT / curator.SEED).read_bytes(), (ROOT / curator.DEFINITION).read_bytes())
		with tempdir() as t, patch.dict(os.environ, {}, clear=True):
			root = Path(t)
			self._fixture(root)
			before = curator.expected_artifacts(root)
			curator.regenerate(root)
			curator.regenerate(root)
			curator.check(root)
			self.assertEqual(before, curator.expected_artifacts(root))
			for rel in [curator.DEFINITION, curator.SEED, curator.KNOWLEDGE, curator.REPORT, curator.REPORT_MD]:
				original = (root / rel).read_bytes()
				(root / rel).write_bytes(original + b"drift")
				with self.assertRaisesRegex(RuntimeError, "drift"):
					curator.check(root)
				(root / rel).write_bytes(original)
			guarded = [curator.RUNTIME, curator.READINGS, curator.spatial.SEED]
			guarded += [Path("evidence/excerpts") / curator.MACHINE_ID / n for n in curator.EXCERPTS]
			guarded += [Path(r["scenario_path"]) for r in load_json(ROOT / curator.RUNTIME)["runtime"]["raw_runs"]]
			for rel in guarded:
				original = (root / rel).read_bytes()
				(root / rel).write_bytes(original + b"changed")
				with self.assertRaises(RuntimeError, msg=str(rel)):
					curator.check(root)
				(root / rel).write_bytes(original)
			promoted = copy.deepcopy(self.game)
			promoted["coverage"]["status"] = "author_ready"
			(root / curator.DEFINITION).write_bytes(canonical_bytes(promoted))
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.regenerate(root)
			(root / curator.DEFINITION).write_bytes(canonical_bytes(self.game))
			stale = root / "machines/author-ready/williams/barracora-1981.json"
			stale.parent.mkdir(parents=True)
			stale.write_text("{}")
			with self.assertRaisesRegex(RuntimeError, "author-ready"):
				curator.check(root)

	def test_missing_local_evidence_is_refused(self):
		with tempdir() as t:
			root = Path(t)
			self._fixture(root)
			(root / curator.RUNTIME).unlink()
			with self.assertRaisesRegex(RuntimeError, "runtime evidence absent"):
				curator.check(root)

	def test_configured_but_missing_external_root_fails(self):
		for name in ROOT_VARIABLES:
			with self.subTest(root=name), patch.dict(os.environ, {name: ""}, clear=True):
				with self.assertRaisesRegex(RuntimeError, "configured evidence root unavailable"):
					curator.verify_external()

	def test_unconfigured_external_roots_are_skipped(self):
		with patch.dict(os.environ, {}, clear=True):
			curator.verify_external()

	def test_external_guards_reject_changed_or_missing_files(self):
		for variable, names in [("PINMAME_SOURCE_ROOT", list(curator.SOURCE_FILES)), ("PINMAME_VPX_SCRIPTS_ROOT", [n for n, _ in curator.SCRIPT_FILES.values()])]:
			with self.subTest(variable=variable), tempdir() as t:
				for name in names:
					path = Path(t) / name
					path.parent.mkdir(parents=True, exist_ok=True)
					path.write_bytes(b"wrong artifact")
				with patch.dict(os.environ, {variable: t}, clear=True):
					with self.assertRaisesRegex(RuntimeError, "absent or changed"):
						curator.verify_external()
		for variable, message in [("PINMAME_MANUALS_ROOT", "retained document absent"), ("PINMAME_ROM_LIBRARY_ROOT", "ROM archive absent"),
				("PINMAME_REVIEW_ARTIFACTS_ROOT", "harness directory manifest absent"), ("PINMAME_VPX_SOURCES_ROOT", "spatial VPX absent")]:
			with self.subTest(variable=variable), tempdir() as t, patch.dict(os.environ, {variable: t}, clear=True):
				with self.assertRaisesRegex(RuntimeError, message):
					curator.verify_external()


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime root not configured")
class BarracoraRetainedEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.review = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		cls.runs = {name: load_json(cls.review / runtime_evidence.HARNESS / f"{name}.json") for name in runtime_evidence.SCENARIOS}

	def test_exact_retained_evidence(self):
		curator.verify_external()
		runtime_evidence.check(self.review, ROOT)

	def _loader(self, mutate):
		runs = copy.deepcopy(self.runs)
		mutate(runs)
		return lambda name: runs[name]

	def test_substituted_display_frame_is_refused(self):
		pin = load_json(ROOT / curator.READINGS)["frames"][0]

		def mutate(runs):
			display = next(d for d in runs[pin["run"]]["snapshots"][pin["snapshot"]]["displays"] if d["index"] == pin["display_index"])
			display["segments"] = [v ^ 0x01 for v in display["segments"]]

		with self.assertRaisesRegex(RuntimeError, "raw frame differs"):
			runtime_evidence.build(self.review, ROOT, self._loader(mutate))

	def test_reordered_scenario_step_is_refused(self):
		def mutate(runs):
			runs["play"]["steps"][0]["label"] = "another action"

		with self.assertRaisesRegex(RuntimeError, "differs from its scenario action"):
			runtime_evidence.build(self.review, ROOT, self._loader(mutate))


if __name__ == "__main__":
	unittest.main()
