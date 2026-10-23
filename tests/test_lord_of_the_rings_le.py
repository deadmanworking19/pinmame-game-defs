"""Fail-closed tests for the Lord of the Rings Limited Edition (Stern, 2009).

The edition is derived from the 2003 machine's record, so most of what is tested here is the
derivation itself: that it carries exactly the 2003 inventory and placements, that it changes only
the three drivers the edition's evidence moves, that its wiring is the edition's own chart, and that
the chart and runtime evidence it rests on still reproduce from their retained originals.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes, load_json  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "stern" / "lord-of-the-rings-limited-edition-2009.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "stern" / "lord-of-the-rings-limited-edition-2009.json"
BASE_PATH = ROOT / "machines" / "author-ready" / "stern" / "lord-of-the-rings-2003.json"
CHART_PATH = ROOT / "tools" / "seeds" / "stern" / "lord-of-the-rings-limited-edition-2009-chart.json"
GAMEPLAY_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "lord-of-the-rings-limited-edition-gameplay.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
LE_DOCUMENTS = "by-machine/stern.lord-of-the-rings-limited-edition.2009"
CHANGED_SOLENOIDS = {12, 14, 28}


def _by_binding(definition: dict, collection: str) -> dict[tuple[str, int], dict]:
	return {(d["binding"]["group"], d["binding"]["device"]): d for d in definition[collection]}


def _placements(definition: dict) -> dict[str, tuple[float, float, str]]:
	return {
		p["id"]: (p["x"], p["y"], p["role"])
		for c in ("inputs", "outputs") for d in definition[c] for p in d.get("spatial", {}).get("placements", [])
	}


def _root(variable: str) -> Path | None:
	value = os.environ.get(variable)
	return Path(value) if value and Path(value).is_dir() else None


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


class LordOfTheRingsLimitedEditionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.base = load_json(BASE_PATH)
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}
		cls.outputs = _by_binding(cls.definition, "outputs")
		cls.solenoids = {address: d for (group, address), d in cls.outputs.items() if group == "pinmame.output.solenoid"}
		cls.chart = load_json(CHART_PATH)

	def test_curator_rebuilds_every_artifact(self) -> None:
		import curate_lord_of_the_rings_le as curator

		self.assertEqual(canonical_bytes(self.definition), canonical_bytes(curator.build()))
		curator._check(ROOT)

	def test_the_partial_record_is_retired(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())

	def test_identity_and_driver(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("stern.lord-of-the-rings-limited-edition.2009", 5558, "GrqZX-MDEPd", "I-00B4", 2009),
		                 (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["model_number"], machine["year"]))
		self.assertEqual(["lotr_le"], [driver["id"] for driver in self.definition["drivers"]])
		driver = self.definition["drivers"][0]
		self.assertEqual(("lotr", "identical"), (driver["clone_of"], driver["physical_compatibility"]))
		self.assertIn("lotrcpua.a02", driver["variant_notes"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_catalog_maps_the_firmware_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		relative = DEFINITION_PATH.relative_to(ROOT).as_posix()
		self.assertEqual({"lotr_le"}, {d["id"] for d in catalog["drivers"] if d.get("definition") == relative})
		machine = next(m for m in catalog["machines"] if m["id"] == self.definition["machine"]["id"])
		self.assertEqual(("author_ready", 100, relative), (machine["coverage_status"], machine["completion_score"], machine["definition"]))

	def test_inventory_is_the_2003_machine_except_three_drivers(self) -> None:
		for collection in ("inputs", "outputs"):
			le, base = _by_binding(self.definition, collection), _by_binding(self.base, collection)
			self.assertEqual(set(base), set(le), collection)
			for key, device in le.items():
				if collection == "outputs" and key[0] == "pinmame.output.solenoid" and key[1] in CHANGED_SOLENOIDS:
					continue
				original = base[key]
				for field in ("id", "kind", "label", "availability", "normally_closed", "roles", "aliases"):
					self.assertEqual(original.get(field), device.get(field), f"{key} {field}")
		self.assertEqual([m["id"] for m in self.base["mechanisms"]], [m["id"] for m in self.definition["mechanisms"]])
		for le, base in zip(self.definition["mechanisms"], self.base["mechanisms"]):
			self.assertEqual({k: v for k, v in base.items() if k not in ("provenance", "behavior")}, {k: v for k, v in le.items() if k not in ("provenance", "behavior")})
			self.assertTrue(le["behavior"].startswith(base["behavior"]), le["id"])
			if le["id"] == "mechanism.ring-magnet":
				self.assertIn("F7, 4A", le["behavior"][len(base["behavior"]):])
			else:
				self.assertEqual(base["behavior"], le["behavior"])
		self.assertEqual(self.base["relationships"], self.definition["relationships"])
		self.assertEqual([{k: v for k, v in d.items() if k != "provenance"} for d in self.base["displays"]],
		                 [{k: v for k, v in d.items() if k != "provenance"} for d in self.definition["displays"]])

	def test_every_placement_is_the_2003_placement(self) -> None:
		le, base = _placements(self.definition), _placements(self.base)
		self.assertEqual(216, len(le))
		self.assertEqual(base, le)
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				for placement in device.get("spatial", {}).get("placements", []):
					self.assertEqual("validated", placement["provenance"]["status"], placement["id"])
					self.assertIn("human-review.lotr-le.owner-tech-chart", placement["provenance"]["source_refs"], placement["id"])

	def test_the_right_helms_deep_flasher_moves_to_28(self) -> None:
		flasher = self.solenoids[28]
		self.assertEqual(("device.helms-deep-right-flasher", "flasher", "used"), (flasher["id"], flasher["kind"], flasher["availability"]))
		self.assertEqual({"control_connection": "J6-P4", "control_wire": "BLU-BLK", "driver_transistor": "Q28", "power_connection": "J6-P10", "power_wire": "YEL-ORG", "nominal_voltage_v": 20.0},
		                 {k: flasher["wiring"][k] for k in ("control_connection", "control_wire", "driver_transistor", "power_connection", "power_wire", "nominal_voltage_v")})
		original = _by_binding(self.base, "outputs")[("pinmame.output.solenoid", 14)]
		self.assertEqual("device.helms-deep-right-flasher", original["id"])
		self.assertEqual([(p["id"], p["x"], p["y"]) for p in original["spatial"]["placements"]],
		                 [(p["id"], p["x"], p["y"]) for p in flasher["spatial"]["placements"]])
		for ref in ("runtime.lord-of-the-rings-limited-edition.flash-test", "runtime.lord-of-the-rings-limited-edition.gameplay", "human-review.lotr-le.owner-tech-chart"):
			self.assertIn(ref, flasher["provenance"]["source_refs"])

	def test_solenoid_14_is_unconnected_and_explained(self) -> None:
		unused = self.solenoids[14]
		self.assertEqual(("device.solenoid-14-unused", "unused", "unused"), (unused["id"], unused["availability"], unused["spatial"]["reason"]))
		self.assertNotIn("control_wire", unused["wiring"], "nothing is connected at J9-P7")
		self.assertEqual("J9-P7", unused["wiring"]["control_connection"])
		self.assertIn("mirror", unused["physical"]["notes"])
		self.assertIn("runtime.lord-of-the-rings-limited-edition.gameplay", unused["provenance"]["source_refs"])

	def test_solenoid_12_is_the_optional_shaker(self) -> None:
		shaker = self.solenoids[12]
		self.assertEqual(("device.shaker-motor", "motor", "optional", ["cabinet.shaker"]), (shaker["id"], shaker["kind"], shaker["availability"], shaker["roles"]))
		self.assertEqual(("cabinet_or_service", "J9-P5", "BLU-YEL", "Q12"),
		                 (shaker["spatial"]["reason"], shaker["wiring"]["control_connection"], shaker["wiring"]["control_wire"], shaker["wiring"]["driver_transistor"]))
		self.assertIn("ipdb.5558", shaker["provenance"]["source_refs"])

	def test_the_balrog_flasher_carries_the_led_module(self) -> None:
		balrog = self.solenoids[32]
		self.assertIn("112-5023-02", balrog["physical"]["notes"])
		self.assertIn("service-bulletin.stern.148", balrog["provenance"]["source_refs"])

	def test_wiring_is_the_chart(self) -> None:
		chart = self.chart
		lamp_rows = {r["row"]: r for r in chart["lamp_matrix"]["rows"]}
		lamp_columns = {c["column"]: c for c in chart["lamp_matrix"]["columns"]}
		for address in range(1, 81):
			wiring = self.outputs[("pinmame.output.lamp", address)]["wiring"]
			row, column = lamp_rows[(address - 1) // 8 + 1], lamp_columns[(address - 1) % 8 + 1]
			self.assertEqual((row["wire"], row["connector"], row["drive"], column["wire"], column["connector"], column["ic"]),
			                 (wiring["drive_wire"], wiring["drive_connection"], wiring["driver_transistor"], wiring["return_wire"], wiring["return_connection"], wiring["return_component"]), address)
		coils = {c["address"]: c for c in chart["coil_table"]["coils"]}
		for address, device in self.solenoids.items():
			transistor = device.get("wiring", {}).get("driver_transistor", "")
			if device["kind"] == "virtual" or not transistor or address in (33, 34, 35):
				continue
			record = coils[int(transistor[1:])]
			self.assertEqual(record["control_connection"], device["wiring"]["control_connection"], address)
			if "control_wire" in device["wiring"]:
				self.assertEqual(record["control_wire"], device["wiring"]["control_wire"], address)
			if "power_wire" in record:
				self.assertEqual((record["power_wire"], record["power_connection"]), (device["wiring"]["power_wire"], device["wiring"]["power_connection"]), address)
		switches = _by_binding(self.definition, "inputs")
		base_switches = _by_binding(self.base, "inputs")
		for address in range(1, 65):
			key = ("pinmame.input.switch", address)
			self.assertEqual(base_switches[key]["wiring"], switches[key]["wiring"], "the chart prints the 2003 switch wiring")

	def test_the_chart_prints_the_2003_tables(self) -> None:
		import curate_lord_of_the_rings as base

		words = lambda text: " ".join(text.replace("( ", "(").replace(" )", ")").split()).upper()  # noqa: E731
		for switch in self.chart["switch_matrix"]["switches"]:
			original = base.SW[switch["address"]]
			self.assertEqual(words(original.get("name") or "NOT USED"), words(switch["name"]), switch["address"])
			self.assertEqual(original.get("location"), switch.get("location"), switch["address"])
		for lamp in self.chart["lamp_matrix"]["lamps"]:
			original = base.LAMPS[lamp["address"]]
			self.assertEqual(words(original["name"]), words(lamp["name"]).replace("LEGOLAS", "LEGOLES"), lamp["address"])
		coils = {c["address"]: c for c in self.chart["coil_table"]["coils"]}
		for address, original in base.COILS.items():
			if address in CHANGED_SOLENOIDS:
				continue
			self.assertEqual(original["control_connector"], coils[address]["control_connection"], address)
			self.assertEqual(original["transistor"], coils[address]["transistor"], address)
		self.assertEqual("OPTIONAL SHAKER MOTOR", coils[12]["name"])
		self.assertEqual("NOT USED NC J9-P7", coils[14]["name"])
		self.assertEqual("FLASH: HELMS DEEP RT", coils[28]["name"])

	def test_device_notes_carry_the_owner_overlay_readings(self) -> None:
		switches = _by_binding(self.definition, "inputs")
		self.assertIn("PINK-GRY", switches[("pinmame.input.switch", 1)]["physical"]["notes"])
		self.assertIn("PINK-VIO", switches[("pinmame.input.switch", 36)]["physical"]["notes"])
		self.assertNotIn("annotated", switches[("pinmame.input.switch", 33)]["physical"]["notes"])
		self.assertIn("ORG-YEL", self.solenoids[5]["physical"]["notes"])
		self.assertIn("J10-P4/5", self.solenoids[46]["physical"]["notes"])

	def test_gameplay_evidence_shows_the_mirror(self) -> None:
		evidence = load_json(GAMEPLAY_PATH)
		runs = evidence["runtime"]["observations"]["runs"]
		le = runs["lotr-le-gameplay"]["ordered_solenoid_on_sequence"]
		self.assertEqual(le.count(14), le.count(28))
		self.assertGreater(le.count(14), 0)
		self.assertNotIn(28, runs["lotr-gameplay"]["ordered_solenoid_on_sequence"])
		self.assertIn(14, runs["lotr-gameplay"]["ordered_solenoid_on_sequence"])
		for raw in evidence["runtime"]["raw_runs"]:
			self.assertEqual(raw["scenario_sha256"], _sha256(ROOT / raw["scenario_path"]))

	def test_gameplay_evidence_matches_the_retained_runs(self) -> None:
		artifacts = _root("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if artifacts is None:
			self.skipTest("retained review artifacts are not available")
		import lotr_le_gameplay_evidence

		self.assertEqual(load_json(GAMEPLAY_PATH), lotr_le_gameplay_evidence.build(artifacts))

	def test_chart_seed_matches_the_retained_chart(self) -> None:
		manuals = _root("PINMAME_MANUALS_ROOT")
		if manuals is None:
			self.skipTest("retained manuals are not available")
		import lotr_le_chart_transcription

		pdf = manuals / LE_DOCUMENTS / "firepowerpinball" / "LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf"
		self.assertEqual(self.chart, lotr_le_chart_transcription.transcribe(pdf))

	def test_io_board_parts_seed_matches_the_retained_schematic(self) -> None:
		parts = load_json(ROOT / "tools" / "seeds" / "stern" / "lord-of-the-rings-limited-edition-2009-io-board-parts.json")
		self.assertEqual(["—", *(str(n) for n in range(1, 68))], [item["item"] for item in parts["items"]])
		designators = {item["item"]: item["ref"] for item in parts["items"]}
		self.assertEqual(", ".join(f"Q{n}" for n in range(33, 43)), designators["31"])
		self.assertEqual(", ".join(f"U{n}" for n in range(10, 18)), designators["33"])
		manuals = _root("PINMAME_MANUALS_ROOT")
		if manuals is None:
			self.skipTest("retained manuals are not available")
		import lotr_le_io_board_parts

		pdf = manuals / LE_DOCUMENTS / "firepowerpinball" / "Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf"
		self.assertEqual(parts, lotr_le_io_board_parts.transcribe(pdf))

	def test_the_curator_refuses_a_coil_row_the_2003_table_does_not_print(self) -> None:
		import curate_lord_of_the_rings_le as curator

		row = curator.COILS[19]
		original = row["coil"]
		try:
			row["coil"] = "26-1200 / 090-5020-00B"
			with self.assertRaises(SystemExit):
				curator._check_coil_row(19)
		finally:
			row["coil"] = original
		curator._check_coil_row(19)

	def test_retained_le_documents_match_their_sources(self) -> None:
		manuals = _root("PINMAME_MANUALS_ROOT")
		artifacts = _root("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if manuals is None or artifacts is None:
			self.skipTest("retained manuals and review artifacts are not available")
		retained = {
			"human-review.lotr-le.owner-tech-chart": manuals / LE_DOCUMENTS / "firepowerpinball" / "LOTR-LE-ONLY-Cabinet-Matrix-11x17.pdf",
			"human-review.lotr-le.owner-annotated-manual-pages": manuals / LE_DOCUMENTS / "firepowerpinball" / "Stern-2009-LOTR-LE-Missing-Pages-100-to-106.pdf",
			"human-review.lotr-le.owner-documentation-page": manuals / LE_DOCUMENTS / "firepowerpinball" / "14-lotr.html",
			"human-review.lotr-le.owner-knocker-page": manuals / LE_DOCUMENTS / "firepowerpinball" / "15-lotr-knocker.html",
			"human-review.lotr-le.owner-shaker-post": manuals / LE_DOCUMENTS / "lotrpinball-blog" / "lotr-le-shaker-motor.html",
			"schematic.stern.io-power-driver-520-5249-00": manuals / LE_DOCUMENTS / "firepowerpinball" / "Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf",
			"service-bulletin.stern.148": artifacts / "lord-of-the-rings-2003" / "completion-2026-10-21" / "SB148-Balrog.pdf",
			"human-review.lotr-le.owner-report-2010": artifacts / "lord-of-the-rings-2003" / "completion-2026-10-21" / "richard-le-wiring-2010.html",
			"ipdb.5558": artifacts / "lord-of-the-rings-2003" / "completion-2026-10-21" / "edition-research" / "ipdb-5558.txt",
		}
		for source_id, path in retained.items():
			self.assertTrue(path.is_file(), path)
			self.assertEqual(self.sources[source_id]["sha256"], _sha256(path), source_id)

	def test_excerpts_are_present_and_reviewed(self) -> None:
		seen = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], _sha256(path), excerpt["id"])
				self.assertTrue(excerpt["reviewed"], excerpt["id"])
				self.assertTrue(excerpt["transcribed_by"].strip(), excerpt["id"])
				seen += 1
		self.assertGreaterEqual(seen, 7 + 11)

	def test_spatial_report_describes_the_derivation(self) -> None:
		report = load_json(ROOT / "reports" / "spatial" / "stern" / "lord-of-the-rings-limited-edition-2009.json")
		self.assertEqual(("pinmame-spatial-audit", self.definition["machine"]["id"], 216),
		                 (report["format"], report["machine_id"], report["placement_count"]))
		self.assertEqual("stern.lord-of-the-rings.2003", report["edition_derivation"]["from_machine"])
		self.assertEqual(28, report["edition_derivation"]["moved"][0]["to_public_solenoid"])


if __name__ == "__main__":
	unittest.main()
