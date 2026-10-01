from __future__ import annotations

import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.priorities import PINSIDE_TOP100_PATH, pinside_rows, refresh_pinside_top100


ROOT = Path(__file__).resolve().parents[1]


class PinsideTop100Tests(unittest.TestCase):
	def setUp(self) -> None:
		self.text = (ROOT / PINSIDE_TOP100_PATH).read_text(encoding="utf-8")
		self.catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.rows = [match for _, match in pinside_rows(self.text)]

	def test_ranks_ascend_and_records_are_unique(self) -> None:
		self.assertTrue(self.rows)
		ranks = [int(row["rank"]) for row in self.rows]
		self.assertEqual(ranks, sorted(ranks))
		machines = [row["machine"] for row in self.rows]
		self.assertEqual(len(machines), len(set(machines)))

	def test_completion_column_matches_catalog(self) -> None:
		self.assertEqual(refresh_pinside_top100(self.text, self.catalog), self.text, "run write_coverage_report to refresh docs/pinside-top100.md")

	def test_indented_stale_row_is_refreshed(self) -> None:
		machine = self.catalog["machines"][0]
		stale = f"  | 1 | Example | `{machine['id']}` | {(machine['completion_score'] + 1) % 101}% |"
		self.assertEqual(refresh_pinside_top100(stale, self.catalog), f"| 1 | Example | `{machine['id']}` | {machine['completion_score']}% |")

	def test_unparsed_ranked_row_fails_closed(self) -> None:
		for row in ("| 1 | Example | no-backticks | 0% |", "| x | Example | `a.b.1990` | 0% |", "| 1 | Example | `a.b.1990` | done |"):
			with self.subTest(row=row), self.assertRaises(ValueError):
				pinside_rows(row)

	def test_unknown_record_fails_closed(self) -> None:
		with self.assertRaises(ValueError):
			refresh_pinside_top100("| 1 | Nothing | `no.such.machine` | 0% |\n", self.catalog)


if __name__ == "__main__":
	unittest.main()
