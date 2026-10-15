"""Determinism and fail-closed contracts for the Swords of Fury seed materializer."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_swords_of_fury as curator
from build_external_evidence_manifest import check_manifest, write_manifest
from pinmame_game_defs.jsonio import canonical_bytes
from pinmame_game_defs.schema_validation import validate_against_schema


SEED_PATH = ROOT / curator.SEED_RELATIVE_PATH
KNOWLEDGE_SEED_PATH = ROOT / curator.KNOWLEDGE_SEED_RELATIVE_PATH
EVIDENCE_BINDING_PATH = ROOT / curator.EVIDENCE_BINDING_RELATIVE_PATH
KNOWLEDGE_PATH = ROOT / curator.KNOWLEDGE_RELATIVE_PATH
PARTIAL_PATH = ROOT / curator.PARTIAL_RELATIVE_PATH
AUTHOR_READY_PATH = ROOT / curator.AUTHOR_READY_RELATIVE_PATH
SPATIAL_REPORT_PATH = ROOT / curator.SPATIAL_REPORT_RELATIVE_PATH
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / curator.SPATIAL_REPORT_MARKDOWN_RELATIVE_PATH


def _digest(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: dict) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_bytes(canonical_bytes(value))


def _load_json(path: Path) -> dict:
	return json.loads(path.read_bytes())


def _bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def _copy_seed_inputs() -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
	"""Copy only authored seed inputs and their referenced repository excerpts into a temp root."""
	temporary = tempfile.TemporaryDirectory()
	root = Path(temporary.name)
	for relative in (curator.SEED_RELATIVE_PATH, curator.KNOWLEDGE_SEED_RELATIVE_PATH, curator.EVIDENCE_BINDING_RELATIVE_PATH):
		destination = root / relative
		destination.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(ROOT / relative, destination)
	definition = _load_json(root / curator.SEED_RELATIVE_PATH)
	first_excerpt: Path | None = None
	for source in definition["sources"]:
		uri = source.get("uri", "")
		if uri.startswith(("evidence/", "tools/seeds/")):
			destination = root / uri
			destination.parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(ROOT / uri, destination)
		for excerpt in source.get("excerpts", []):
			for field in ("path", "image"):
				relative = excerpt.get(field)
				if relative is None:
					continue
				parts = PurePosixPath(relative).parts
				destination = root.joinpath(*parts)
				destination.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(ROOT.joinpath(*parts), destination)
				if field == "path" and first_excerpt is None:
					first_excerpt = destination
	if first_excerpt is None:
		raise AssertionError("Swords of Fury seed must declare an excerpt before mutation tests can run")
	return temporary, root, first_excerpt


def _external_register(vpx_root: Path, *, file_count_offset: int = 0) -> dict:
	table = vpx_root / "source-table.vpx"
	table.write_bytes(b"fixture table")
	extraction = vpx_root / "extracted"
	extraction.mkdir(exist_ok=True)
	(extraction / "script.vbs").write_bytes(b"fixture extraction")
	write_manifest(extraction, curator.EXTRACTION_GAME)
	manifest_path = extraction / "manifest.json"
	manifest = _load_json(manifest_path)
	return {
		"files": [{
			"root": "vpx",
			"path": "source-table.vpx",
			"size": table.stat().st_size,
			"sha256": _digest(table),
		}],
		"extraction": {
			"root": "vpx",
			"path": "extracted/manifest.json",
			"game": curator.EXTRACTION_GAME,
			"sha256": _digest(manifest_path),
			"file_count": len(manifest["files"]) + file_count_offset,
			"total_bytes": sum(entry["size"] for entry in manifest["files"]),
		},
	}


class SwordsOfFuryStaticContractTests(unittest.TestCase):
	def test_settled_controller_constants_do_not_depend_on_seed_availability(self) -> None:
		self.assertEqual("williams.swords-of-fury.1988", curator.MACHINE_ID)
		self.assertEqual(
			{"swrds_l1", "swrds_l2", "swrds_lg2", "swrds_rr1", "swrds_rr1b"},
			curator.DRIVER_IDS,
		)
		self.assertEqual(set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)), curator.EXPECTED_SWITCH_BINDINGS)
		self.assertEqual(set(range(1, 65)), curator.EXPECTED_SOLENOID_BINDINGS)
		self.assertEqual(set(range(1, 65)), curator.EXPECTED_LAMP_BINDINGS)
		self.assertEqual("swrds_l2", curator.EXTRACTION_GAME)


class SwordsOfFuryExternalRegisterGuardTests(unittest.TestCase):
	def test_external_manifest_is_recomputed_over_every_retained_file(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			vpx_root = root / "vpx"
			vpx_root.mkdir()
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, _external_register(vpx_root))
			curator.verify_retained(vpx_root, None, None, root=root)
			(vpx_root / "extracted" / "script.vbs").write_bytes(b"drifted extraction")
			with self.assertRaisesRegex(RuntimeError, "extraction content drifted"):
				curator.verify_retained(vpx_root, None, None, root=root)

	def test_external_register_rejects_a_pinned_source_digest_mismatch(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			vpx_root = root / "vpx"
			vpx_root.mkdir()
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, _external_register(vpx_root))
			curator.verify_retained(vpx_root, None, None, root=root)
			(vpx_root / "source-table.vpx").write_bytes(b"changed table")
			with self.assertRaisesRegex(RuntimeError, "retained vpx evidence SHA-256 drifted"):
				curator.verify_retained(vpx_root, None, None, root=root)

	def test_external_register_rejects_traversal_drive_paths_and_manifest_count_drift(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			vpx_root = root / "vpx"
			vpx_root.mkdir()
			register = _external_register(vpx_root)
			register["files"][0]["path"] = "../outside.vpx"
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, register)
			with self.assertRaisesRegex(RuntimeError, "safe relative POSIX"):
				curator.verify_retained(vpx_root, None, None, root=root)
			register["files"][0]["path"] = "C:/outside.vpx"
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, register)
			with self.assertRaisesRegex(RuntimeError, "safe relative POSIX"):
				curator.verify_retained(vpx_root, None, None, root=root)
			_write_json(root / curator.EVIDENCE_BINDING_RELATIVE_PATH, _external_register(vpx_root, file_count_offset=1))
			with self.assertRaisesRegex(RuntimeError, "file count drifted"):
				curator.verify_retained(vpx_root, None, None, root=root)


@unittest.skipUnless(
	SEED_PATH.is_file() and KNOWLEDGE_SEED_PATH.is_file() and EVIDENCE_BINDING_PATH.is_file(),
	"Swords of Fury authored seed inputs are not present yet",
)
class SwordsOfFuryMaterializerMutationTests(unittest.TestCase):
	def test_repository_runtime_evidence_drift_fails_closed(self) -> None:
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			path = root / "tools/seeds/williams/swords-of-fury-runtime.json"
			path.write_bytes(path.read_bytes() + b"\n")
			with self.assertRaisesRegex(RuntimeError, "repository derived evidence SHA-256 drifted"):
				curator.generate(root)

	def test_regeneration_is_byte_deterministic_and_never_rewrites_the_seed(self) -> None:
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			seed_before = (root / curator.SEED_RELATIVE_PATH).read_bytes()
			first = curator.generate(root)
			first_definition = first.read_bytes()
			first_report = (root / curator.SPATIAL_REPORT_RELATIVE_PATH).read_bytes()
			curator.check(root)
			curator.generate(root)
			self.assertEqual(seed_before, (root / curator.SEED_RELATIVE_PATH).read_bytes())
			self.assertEqual(first_definition, first.read_bytes())
			self.assertEqual(first_report, (root / curator.SPATIAL_REPORT_RELATIVE_PATH).read_bytes())
			self.assertEqual(seed_before, first_definition)
			self.assertEqual(
				(root / curator.KNOWLEDGE_SEED_RELATIVE_PATH).read_bytes(),
				(root / curator.KNOWLEDGE_RELATIVE_PATH).read_bytes(),
			)

	def test_missing_or_drifting_seed_and_knowledge_fail_closed(self) -> None:
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			(root / curator.SEED_RELATIVE_PATH).unlink()
			with self.assertRaisesRegex(RuntimeError, "machine seed is missing"):
				curator.check(root)
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			(root / curator.KNOWLEDGE_SEED_RELATIVE_PATH).unlink()
			with self.assertRaisesRegex(RuntimeError, "knowledge seed is missing"):
				curator.generate(root)
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			curator.generate(root)
			definition = _load_json(root / curator.SEED_RELATIVE_PATH)
			definition["machine"]["name"] += " drift"
			_write_json(root / curator.SEED_RELATIVE_PATH, definition)
			with self.assertRaisesRegex(RuntimeError, "generated definition drifted"):
				curator.check(root)
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			curator.generate(root)
			knowledge_seed = root / curator.KNOWLEDGE_SEED_RELATIVE_PATH
			knowledge_seed.write_bytes(knowledge_seed.read_bytes() + b"\nseed drift\n")
			with self.assertRaisesRegex(RuntimeError, "knowledge note drifted"):
				curator.check(root)

	def test_missing_or_drifting_excerpt_fails_closed(self) -> None:
		temporary, root, excerpt = _copy_seed_inputs()
		with temporary:
			curator.generate(root)
			excerpt.unlink()
			with self.assertRaisesRegex(RuntimeError, "missing excerpt file|repository excerpt is missing"):
				curator.check(root)
		temporary, root, excerpt = _copy_seed_inputs()
		with temporary:
			curator.generate(root)
			excerpt.write_bytes(excerpt.read_bytes() + b"\nexcerpt drift\n")
			with self.assertRaisesRegex(RuntimeError, "excerpt.*SHA-256|excerpt.*sha256|excerpt.*hash|repository excerpt SHA-256 drifted"):
				curator.check(root)

	def test_partial_seed_cannot_overwrite_an_author_ready_record(self) -> None:
		temporary, root, _excerpt = _copy_seed_inputs()
		with temporary:
			definition = curator.build(root)
			self.assertEqual("partial", definition["coverage"]["status"])
			author_ready = root / curator.AUTHOR_READY_RELATIVE_PATH
			author_ready.parent.mkdir(parents=True, exist_ok=True)
			author_ready.write_bytes(b"author-ready sentinel\n")
			with self.assertRaisesRegex(RuntimeError, "author-ready Swords of Fury artifact"):
				curator.generate(root)
			self.assertEqual(b"author-ready sentinel\n", author_ready.read_bytes())


@unittest.skipUnless(
	SEED_PATH.is_file() and KNOWLEDGE_SEED_PATH.is_file() and EVIDENCE_BINDING_PATH.is_file(),
	"Swords of Fury authored seed inputs are not present yet",
)
class SwordsOfFurySeededDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = curator.build(ROOT)
		cls.switches = _bindings(cls.definition, "inputs", curator.SWITCH_GROUP)
		cls.dips = _bindings(cls.definition, "inputs", curator.DIP_GROUP)
		cls.solenoids = _bindings(cls.definition, "outputs", curator.SOLENOID_GROUP)
		cls.lamps = _bindings(cls.definition, "outputs", curator.LAMP_GROUP)

	def test_seeded_machine_matches_the_settled_identity_and_exact_address_contract(self) -> None:
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			{"id": curator.MACHINE_ID, "manufacturer": "Williams", "year": 1988},
			{key: self.definition["machine"][key] for key in ("id", "manufacturer", "year")},
		)
		self.assertEqual(curator.DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertEqual("pinmame.system-11", self.definition["controller"]["platform"])
		self.assertEqual("0x100", self.definition["controller"]["hardware_generation"])
		self.assertEqual(curator.EXPECTED_SWITCH_BINDINGS, set(self.switches))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual("dip_switch", self.dips[0]["kind"])
		self.assertEqual(len(curator.EXPECTED_SWITCH_BINDINGS) + 1, len(self.definition["inputs"]))
		self.assertEqual(curator.EXPECTED_SOLENOID_BINDINGS, set(self.solenoids))
		self.assertEqual(curator.EXPECTED_LAMP_BINDINGS, set(self.lamps))
		self.assertEqual(128, len(self.definition["outputs"]))
		self.assertNotIn(curator.GI_GROUP, {item["binding"]["group"] for item in self.definition["outputs"]})
		self.assertTrue(any(
			source.get("kind") in {"pinmame_catalog", "pinmame_core"} and source.get("revision") == curator.PINMAME_REVISION
			for source in self.definition["sources"]
		))

	def test_flipper_copies_and_synthetic_outputs_follow_their_bindings_not_device_ids(self) -> None:
		pairs = {
			(item["source"], item["destination"])
			for item in self.definition["relationships"]
			if item["kind"] == "direct"
		}
		for source_address, matrix_address in ((84, 58), (82, 60)):
			with self.subTest(source_address=source_address):
				self.assertEqual("used", self.switches[source_address]["availability"])
				self.assertIn((self.switches[source_address]["id"], self.switches[matrix_address]["id"]), pairs)
		for address in (46, 47):
			self.assertEqual("virtual", self.solenoids[address]["kind"])
			self.assertNotEqual("flasher", self.solenoids[address]["kind"])

	def test_factory_lamp_and_gi_semantics_are_preserved_by_binding(self) -> None:
		gi_relay = self.solenoids[10]
		self.assertEqual("relay", gi_relay["kind"])
		gi_notes = gi_relay["physical"]["notes"].casefold()
		self.assertEqual(2, gi_relay["physical"]["quantity"])
		self.assertNotIn("spatial", gi_relay, "render GI lights must not become physical bulb positions")
		self.assertEqual(2, self.solenoids[9]["physical"]["quantity"])
		self.assertIn("playfield", self.solenoids[9]["physical"]["location"])
		self.assertNotEqual("not_applicable", self.solenoids[9].get("spatial", {}).get("status"))
		for lamp in self.lamps.values():
			if lamp.get("spatial", {}).get("placements"):
				self.assertEqual("candidate", lamp["spatial"]["status"])
		self.assertIn("playfield", gi_notes)
		self.assertIn("backbox", gi_notes)
		for address in curator.MIXED_LOCATION_LAMPS:
			with self.subTest(address=address):
				self.assertEqual(2, self.lamps[address]["physical"]["quantity"])
		for address in curator.BACKBOX_ONLY_LAMPS:
			with self.subTest(address=address):
				self.assertEqual(("not_applicable", "cabinet_or_service"), (self.lamps[address]["spatial"]["status"], self.lamps[address]["spatial"]["reason"]))
		for address in curator.PRINTED_BLANK_LAMPS:
			with self.subTest(address=address):
				lamp = self.lamps[address]
				self.assertEqual("unused", lamp["availability"])
				text = " ".join((lamp["label"], lamp.get("physical", {}).get("notes", ""))).casefold()
				self.assertIn("blank", text)

	def test_source_excerpt_hashes_and_optional_images_are_exact(self) -> None:
		checked = 0
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				checked += 1
				path = ROOT.joinpath(*PurePosixPath(excerpt["path"]).parts)
				self.assertEqual(excerpt["sha256"], _digest(path), excerpt["id"])
				if "image" in excerpt:
					image = ROOT.joinpath(*PurePosixPath(excerpt["image"]).parts)
					self.assertEqual(excerpt["image_sha256"], _digest(image), excerpt["id"])
		self.assertGreater(checked, 0)

	def test_generated_definition_and_spatial_reports_are_exact_seed_projections(self) -> None:
		self.assertTrue(PARTIAL_PATH.is_file(), "Swords of Fury is required to remain partial")
		self.assertFalse(AUTHOR_READY_PATH.exists(), "a partial Swords of Fury record must not retain an author-ready twin")
		self.assertEqual(SEED_PATH.read_bytes(), PARTIAL_PATH.read_bytes())
		self.assertEqual(KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		curator.check(ROOT)
		report = curator.build_spatial_report(self.definition)
		self.assertEqual([], validate_against_schema(report, ROOT / "schemas/spatial-report.schema.json", "Swords of Fury report"))
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())
		self.assertEqual(curator.render_spatial_report(report).encode("utf-8"), SPATIAL_REPORT_MARKDOWN_PATH.read_bytes())
		self.assertEqual(hashlib.sha256(SEED_PATH.read_bytes()).hexdigest(), report["definition_sha256"])
		self.assertEqual(_load_json(EVIDENCE_BINDING_PATH), report["external_evidence"])
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertIn("Partial", report["promotion_decision"]["decision"])

	def test_spatial_report_preserves_all_seeded_placements_including_displays(self) -> None:
		report = curator.build_spatial_report(self.definition)
		expected = {
			(collection, device["id"], placement["id"])
			for collection in ("inputs", "outputs", "displays")
			for device in self.definition[collection]
			for placement in device.get("spatial", {}).get("placements", [])
		}
		actual = {
			(device["collection"], device["id"], placement["id"])
			for device in report["located_devices"]
			for placement in device["spatial"]["placements"]
		}
		self.assertEqual(expected, actual)
		expected_missing = {
			(collection, device["id"])
			for collection in ("inputs", "outputs", "displays")
			for device in self.definition[collection]
			if not isinstance(device.get("spatial"), dict)
		}
		self.assertEqual(expected_missing, {(device["collection"], device["id"]) for device in report["missing_spatial_records"]})
		expected_unknown = {
			(collection, device["id"], tuple(curator._unknown_reasons(device)))
			for collection in ("inputs", "outputs", "displays")
			for device in self.definition[collection]
			if curator._unknown_reasons(device)
		}
		self.assertEqual(expected_unknown, {
			(device["collection"], device["id"], tuple(device["unknown_fields"])) for device in report["unknown_records"]
		})
		self.assertEqual("left=0, right=1 in player view", report["coordinate_convention"]["x"])
		self.assertEqual("rear=0, front=1 in player view", report["coordinate_convention"]["y"])


@unittest.skipUnless(
	EVIDENCE_BINDING_PATH.is_file()
	and os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	and os.environ.get("PINMAME_MANUALS_ROOT")
	and os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"),
	"Swords of Fury external evidence register or roots are not configured",
)
class SwordsOfFuryRetainedEvidenceTests(unittest.TestCase):
	def test_external_evidence_register_recomputes_source_hashes_and_manifest_metadata(self) -> None:
		roots = {
			"vpx": Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]),
			"manuals": Path(os.environ["PINMAME_MANUALS_ROOT"]),
			"review": Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]),
		}
		curator.verify_retained(roots["vpx"], roots["manuals"], roots["review"])
		register = _load_json(EVIDENCE_BINDING_PATH)
		for entry in register["files"]:
			path = curator._external_file(roots[entry["root"]], entry["path"], "test retained evidence")
			self.assertEqual(entry["size"], path.stat().st_size)
			self.assertEqual(entry["sha256"], _digest(path))
		extraction = register["extraction"]
		manifest_path = curator._external_file(roots[extraction["root"]], extraction["path"], "test extraction manifest")
		self.assertEqual(extraction["sha256"], _digest(manifest_path))
		self.assertEqual(extraction["sha256"], check_manifest(manifest_path.parent, curator.EXTRACTION_GAME))
		manifest = _load_json(manifest_path)
		self.assertEqual(extraction["file_count"], len(manifest["files"]))
		self.assertEqual(extraction["total_bytes"], sum(item["size"] for item in manifest["files"]))


if __name__ == "__main__":
	unittest.main()
