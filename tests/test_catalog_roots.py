from __future__ import annotations

import json
import unittest
from pathlib import Path

from pinmame_game_defs.catalog import NOT_A_DRIVER, Driver, resolve_root_driver


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _driver(driver_id: str, clone_of: str | None = None, flags: int = 0) -> Driver:
	return Driver(id=driver_id, clone_of=clone_of, description=driver_id, year="1978", manufacturer="Recel", flags=flags)


class CatalogRootTests(unittest.TestCase):
	def test_a_reported_not_a_driver_parent_does_not_group_its_games(self) -> None:
		drivers = {
			"recel": _driver("recel", flags=NOT_A_DRIVER),
			"r_torneo": _driver("r_torneo", "recel"),
			"r_torneoa": _driver("r_torneoa", "recel"),
			"r_mrevil": _driver("r_mrevil", "recel"),
		}
		self.assertEqual("recel", resolve_root_driver("recel", drivers))
		self.assertEqual("r_torneo", resolve_root_driver("r_torneo", drivers))
		self.assertEqual("r_mrevil", resolve_root_driver("r_mrevil", drivers))

	def test_ordinary_clones_still_resolve_to_their_parent(self) -> None:
		drivers = {"fh_l9": _driver("fh_l9"), "fh_905hbs": _driver("fh_905hbs", "fh_l9")}
		self.assertEqual("fh_l9", resolve_root_driver("fh_905hbs", drivers))

	def test_unreported_bios_parents_still_end_resolution(self) -> None:
		drivers = {"amh": _driver("amh", "pinheck"), "dominos": _driver("dominos", "pinheck")}
		self.assertEqual("amh", resolve_root_driver("amh", drivers))
		self.assertEqual("dominos", resolve_root_driver("dominos", drivers))

	def test_catalog_keeps_recel_system_iii_apart_from_its_games(self) -> None:
		catalog = json.loads((REPOSITORY_ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
		records = {record["id"]: record for record in catalog["drivers"]}
		self.assertEqual("recel", records["recel"]["root_driver"])
		self.assertEqual("recel.system-iii.1978", records["recel"]["machine_id"])
		for driver_id, record in records.items():
			if record.get("clone_of") == "recel":
				self.assertEqual(driver_id, record["root_driver"])
				self.assertNotEqual("recel.system-iii.1978", record["machine_id"])


if __name__ == "__main__":
	unittest.main()
