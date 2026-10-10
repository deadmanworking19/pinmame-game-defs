from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes, write_json


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_spike1 as curator


GAME = "fixture_1"
MACHINE_ID = "stern.fixture-game.2024"
SLUG_YEAR = "fixture-game-2024"
SOURCE_ID = "manual.fixture"
EXCERPT_PATH = "evidence/excerpts/stern.fixture-game.2024/switches.md"
KNOWLEDGE_PATH = "knowledge/stern/fixture-game-2024.md"


def definition(excerpt_digest: str) -> dict:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {"id": MACHINE_ID, "name": "Fixture Game", "manufacturer": "Stern", "year": 2024, "kind": "physical_pinball"},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "observed",
				"physical_wiring": "observed",
				"mechanisms": "observed",
				"variant_coverage": "validated",
				"recreation_knowledge": "observed",
				"spatial_placement": "unknown",
			},
		},
		"controller": {"platform": "pinmame.spike1", "inversion_applied_by_emulator": True},
		"drivers": [{"id": GAME, "description": "Fixture Game (1.0)", "year": "2024", "manufacturer": "Stern", "flags": 0}],
		"inputs": [{
			"id": "switch.fixture", "label": "Fixture Switch", "kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": 1}, "aliases": [], "availability": "used", "normally_closed": False,
			"provenance": {"status": "observed", "source_refs": [SOURCE_ID]},
		}],
		"outputs": [],
		"displays": [],
		"mechanisms": [],
		"relationships": [],
		"sources": [{
			"id": SOURCE_ID, "kind": "manual", "uri": "https://example.invalid/fixture", "locator": "switch table",
			"license": "Reference only", "attribution": "Fixture manual",
			"excerpts": [{"id": "switches", "locator": "page 1", "path": EXCERPT_PATH, "sha256": excerpt_digest}],
		}],
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "partial"},
	}


def knowledge() -> bytes:
	return b"""# Fixture Game recreation knowledge

Machine ID: `stern.fixture-game.2024`.

## Identity

Fixture Game is the documented Stern machine for this fixture.

## Recreation

Recreate the reviewed partial switch contract without inventing geometry.

## Sources

- `manual.fixture`
"""


class Spike1CuratorTests(unittest.TestCase):
	def make_repository(self) -> Path:
		temporary = tempfile.TemporaryDirectory()
		self.addCleanup(temporary.cleanup)
		root = Path(temporary.name)
		write_bytes(root / "schemas/machine.schema.json", (ROOT / "schemas/machine.schema.json").read_bytes())
		excerpt = b"fixture switch table\n"
		write_bytes(root / EXCERPT_PATH, excerpt)
		write_bytes(root / f"tools/seeds/stern/spike1/{GAME}.md", knowledge())
		write_bytes(root / f"tools/seeds/stern/spike1/{GAME}.json", canonical_bytes(definition(hashlib.sha256(excerpt).hexdigest())))
		return root

	def seed(self, root: Path) -> dict:
		return load_json(root / f"tools/seeds/stern/spike1/{GAME}.json")

	def write_seed(self, root: Path, value: dict) -> None:
		write_json(root / f"tools/seeds/stern/spike1/{GAME}.json", value)

	def test_regenerate_and_check_copy_the_reviewed_inputs_byte_for_byte(self) -> None:
		root = self.make_repository()
		curator.regenerate(GAME, root)
		curator.check(GAME, root)
		self.assertEqual(
			(root / f"tools/seeds/stern/spike1/{GAME}.json").read_bytes(),
			(root / f"machines/partial/stern/{SLUG_YEAR}.json").read_bytes(),
		)
		self.assertEqual(
			(root / f"tools/seeds/stern/spike1/{GAME}.md").read_bytes(),
			(root / KNOWLEDGE_PATH).read_bytes(),
		)
		report = load_json(root / f"reports/spatial/stern/{SLUG_YEAR}.json")
		self.assertEqual("partial", report["decision"]["status"])
		self.assertEqual(["spatial_placement"], report["coverage_missing"])
		self.assertEqual({"group": "pinmame.input.switch", "device": 1}, report["devices"][0]["binding"])
		self.assertNotIn('"x":', canonical_bytes(report).decode("utf-8"))
		self.assertEqual(canonical_bytes(report), (root / f"reports/spatial/stern/{SLUG_YEAR}.json").read_bytes())

	def test_check_detects_real_artifact_drift(self) -> None:
		root = self.make_repository()
		curator.regenerate(GAME, root)
		write_bytes(root / f"machines/partial/stern/{SLUG_YEAR}.json", b"{}\n")
		with self.assertRaisesRegex(curator.CuratorError, "Artifact drift"):
			curator.check(GAME, root)

	def test_schema_wrong_driver_and_partial_guards_fail_before_writes(self) -> None:
		for mutation, expected in (
			(lambda value: value.update({"unexpected": True}), "validation failed"),
			(lambda value: value["drivers"][0].update({"id": "other_driver"}), "does not declare driver"),
			(lambda value: value["coverage"].update({"status": "author_ready", "missing": []}), "must remain partial"),
		):
			with self.subTest(expected=expected):
				root = self.make_repository()
				value = self.seed(root)
				mutation(value)
				self.write_seed(root, value)
				with self.assertRaisesRegex(curator.CuratorError, expected):
					curator.regenerate(GAME, root)
				self.assertFalse((root / f"machines/partial/stern/{SLUG_YEAR}.json").exists())

	def test_author_ready_and_unsafe_knowledge_paths_are_refused(self) -> None:
		root = self.make_repository()
		write_bytes(root / f"machines/author-ready/stern/{SLUG_YEAR}.json", b"{}\n")
		with self.assertRaisesRegex(curator.CuratorError, "author-ready"):
			curator.regenerate(GAME, root)
		with self.assertRaisesRegex(curator.CuratorError, "author-ready"):
			curator.check(GAME, root)
		root = self.make_repository()
		promoted = self.seed(root)
		promoted["coverage"]["status"] = "author_ready"
		partial_target = root / f"machines/partial/stern/{SLUG_YEAR}.json"
		write_json(partial_target, promoted)
		original = partial_target.read_bytes()
		with self.assertRaisesRegex(curator.CuratorError, "author-ready"):
			curator.regenerate(GAME, root)
		self.assertEqual(original, partial_target.read_bytes())
		root = self.make_repository()
		value = self.seed(root)
		value["knowledge"]["path"] = "knowledge/../outside.md"
		self.write_seed(root, value)
		with self.assertRaisesRegex(curator.CuratorError, "Unsafe knowledge.path"):
			curator.regenerate(GAME, root)

	def test_missing_inputs_unknown_games_and_excerpt_hash_claims_fail_closed(self) -> None:
		root = self.make_repository()
		with self.assertRaisesRegex(curator.CuratorError, "Unknown game"):
			curator.check("not_a_driver", root)
		(root / f"tools/seeds/stern/spike1/{GAME}.md").unlink()
		with self.assertRaisesRegex(curator.CuratorError, "knowledge companion"):
			curator.regenerate(GAME, root)
		root = self.make_repository()
		(root / EXCERPT_PATH).unlink()
		with self.assertRaisesRegex(curator.CuratorError, "missing excerpt file"):
			curator.regenerate(GAME, root)
		root = self.make_repository()
		write_bytes(root / EXCERPT_PATH, b"tampered excerpt\n")
		with self.assertRaisesRegex(curator.CuratorError, "does not match its recorded digest"):
			curator.regenerate(GAME, root)

	def test_knowledge_sections_machine_labels_and_source_references_are_required(self) -> None:
		root = self.make_repository()
		write_bytes(root / f"tools/seeds/stern/spike1/{GAME}.md", b"# Fixture Game\n\n## Identity\n\nKnown.\n")
		with self.assertRaisesRegex(curator.CuratorError, "recreation section"):
			curator.regenerate(GAME, root)


if __name__ == "__main__":
	unittest.main()
