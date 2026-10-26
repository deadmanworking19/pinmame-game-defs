from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from supreme_shared_playfield import build_crosswalk


EXCERPTS = ROOT / "evidence" / "excerpts"


class SupremeSharedPlayfieldTests(unittest.TestCase):
    def test_complete_real_excerpt_crosswalk_preserves_comparison_facts(self) -> None:
        crosswalk = build_crosswalk(ROOT)
        self.assertEqual(crosswalk, build_crosswalk(ROOT))
        json.dumps(crosswalk, sort_keys=True)

        self.assertEqual(crosswalk["coordinate_convention"], "x=0 left, x=1 right, y=0 rear/backglass end, y=1 apron/front")
        self.assertEqual(
            crosswalk["authority_limit"],
            "Matches prove routing only; the sibling manual proves sibling hardware; "
            "Supreme physical fitment/harness, polarity, parts and emitter counts remain unconfirmed.",
        )
        self.assertEqual(
            crosswalk["sections"]["switches"]["counts"],
            {"shared": 56, "supreme_only": 10, "spiderman_only": 2, "manual_matched": 51},
        )
        self.assertEqual(
            crosswalk["sections"]["coils"]["counts"],
            {"shared": 12, "supreme_only": 0, "spiderman_only": 0, "manual_matched": 9},
        )
        self.assertEqual(
            crosswalk["sections"]["leds"]["counts"],
            {"shared": 65, "supreme_only": 0, "spiderman_only": 0, "manual_matched": 61},
        )

        switches = crosswalk["sections"]["switches"]
        cpu = next(row for row in switches["shared"] if (row["node"], row["position"]) == (0, 0))
        self.assertEqual(101, cpu["public_address"])
        self.assertEqual("C1", cpu["manual_row"]["ID"])
        moved = {(row["node"], row["position"], row["public_address"]): row for row in switches["spiderman_only"]}
        self.assertEqual(set(moved), {(8, 26, 15), (8, 27, 14)})
        self.assertEqual(moved[(8, 26, 15)]["spiderman_name"], "LAUNCH BUTTON")
        self.assertEqual(moved[(8, 27, 14)]["spiderman_name"], "TILT PENDULUM")
        self.assertTrue(all("manual_row" not in row for row in switches["spiderman_only"]))
        self.assertTrue(
            all(
                not (
                    row["public_address"] in {14, 15} and "manual_row" in row
                )
                for row in switches["shared"]
            )
        )

        supreme_only = {(row["node"], row["position"], row["public_address"]): row for row in switches["supreme_only"]}
        self.assertEqual(
            set(supreme_only),
            {
                (1, 8, 83),
                (1, 12, 74),
                (1, 14, 14),
                (1, 15, 15),
                (1, 16, 76),
                (1, 17, 78),
                (1, 18, 77),
                (1, 19, 79),
                (1, 20, 80),
                (1, 22, 84),
            },
        )
        self.assertEqual(supreme_only[(1, 14, 14)]["supreme_name"], "TILT PENDULUM")
        self.assertEqual(supreme_only[(1, 15, 15)]["supreme_name"], "LAUNCH BUTTON")
        self.assertNotIn("manual_row", supreme_only[(1, 14, 14)])
        self.assertNotIn("manual_row", supreme_only[(1, 15, 15)])

        coils = crosswalk["sections"]["coils"]["shared"]
        self.assertEqual(sum(row["node"] == 1 for row in coils), 3)
        self.assertTrue(all("manual_row" not in row for row in coils if row["node"] == 1))

        leds = crosswalk["sections"]["leds"]["shared"]
        self.assertEqual(sum(row["node"] == 1 for row in leds), 4)
        self.assertTrue(all("manual_row" not in row for row in leds if row["node"] == 1))
        lamp = next(row for row in leds if (row["node"], row["position"]) == (8, 29))
        self.assertEqual(lamp["supreme_name"], "LEFT ORBIT ARROW")
        self.assertEqual(lamp["spiderman_name"], "L SANDMAN ARROW")
        self.assertEqual(lamp["supreme_class_bits"], 1)
        self.assertEqual(lamp["spiderman_class_bits"], 1)
        self.assertEqual(lamp["manual_row"]["Part Number"], "520-7011-00")
        self.assertEqual(lamp["manual_row"]["Address"], "8-LP-29")

        manual_switches = [
            {"manual_page": row["manual_page"], "manual_row": row["manual_row"]}
            for row in switches["shared"] if "manual_row" in row
        ] + switches["unmatched_manual_rows"]
        self.assertIn(
            {
                "manual_page": "evidence/excerpts/stern.spider-man-the-pin.2016/manual-switches-page15.md",
                "manual_row": {
                    "ID": "16",
                    "Name": "Trough 6",
                    "Node": "8",
                    "Node Ext": "8b",
                    "Conn.": "CN2",
                    "Input Pin": "-",
                    "Input Wire": "BLANK",
                    "GND Pin": "-",
                    "Ground Wire": "BLANK",
                    "Location": "Playfield",
                    "Type": "Opto",
                    "Address": "8-SW-40",
                    "Part Number": "520-5344-00 tx 520-7001-00 rx",
                },
            },
            manual_switches,
        )
        self.assertEqual(
            {
                (row["manual_row"]["ID"], row["manual_row"]["Address"])
                for row in manual_switches
                if row["manual_row"]["ID"] in {"14", "15"}
            },
            {("14", "8-SW-27"), ("15", "8-SW-26")},
        )
        self.assertNotIn("manual_page", next(row for row in coils if row["node"] == 1))

    def test_sources_hash_exact_bytes_and_change_with_fixture_source(self) -> None:
        crosswalk = build_crosswalk(ROOT)
        expected_sources = [
            "stern.supreme-x-stern.2018/rom-routing.json.txt",
            "stern.spider-man-the-pin.2016/rom-routing.json.txt",
            "stern.spider-man-the-pin.2016/manual-drivers.md",
            "stern.spider-man-the-pin.2016/manual-switches-page15.md",
            "stern.spider-man-the-pin.2016/manual-switches-page17.md",
            "stern.spider-man-the-pin.2016/manual-lamps-page18.md",
            "stern.spider-man-the-pin.2016/manual-lamps-page20.md",
        ]
        actual = {source["path"]: source["sha256"] for source in crosswalk["sources"]}
        self.assertEqual(set(actual), {f"evidence/excerpts/{path}" for path in expected_sources})
        for relative_path in expected_sources:
            path = EXCERPTS / relative_path
            self.assertEqual(actual[f"evidence/excerpts/{relative_path}"], hashlib.sha256(path.read_bytes()).hexdigest())

        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            self._write_fixture(fixture_root)
            before = build_crosswalk(fixture_root)
            routing_path = fixture_root / "evidence/excerpts/stern.supreme-x-stern.2018/rom-routing.json.txt"
            routing_path.write_bytes(routing_path.read_bytes() + b"\n")
            after = build_crosswalk(fixture_root)
            source_path = "evidence/excerpts/stern.supreme-x-stern.2018/rom-routing.json.txt"
            self.assertNotEqual(
                self._source_hash(before, source_path),
                self._source_hash(after, source_path),
            )

    def test_manual_and_routing_guards_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            self._write_fixture(fixture_root, duplicate_manual=True)
            with self.assertRaisesRegex(ValueError, "ambiguous manual match in coils"):
                build_crosswalk(fixture_root)

        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            self._write_fixture(fixture_root, duplicate_routing=True)
            with self.assertRaisesRegex(ValueError, "duplicate node-position row"):
                build_crosswalk(fixture_root)

        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            self._write_fixture(fixture_root, spiderman_public=99)
            with self.assertRaisesRegex(ValueError, "public-address disagreement in switches"):
                build_crosswalk(fixture_root)

        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            self._write_fixture(fixture_root, spiderman_public=None)
            with self.assertRaisesRegex(ValueError, "invalid public address"):
                build_crosswalk(fixture_root)

    @staticmethod
    def _source_hash(crosswalk: dict, path: str) -> str:
        return next(source["sha256"] for source in crosswalk["sources"] if source["path"] == path)

    @staticmethod
    def _write_fixture(
        root: Path,
        *,
        duplicate_manual: bool = False,
        duplicate_routing: bool = False,
        spiderman_public: int | None = 1,
    ) -> None:
        excerpts = root / "evidence/excerpts"
        supreme_path = excerpts / "stern.supreme-x-stern.2018/rom-routing.json.txt"
        spiderman_path = excerpts / "stern.spider-man-the-pin.2016/rom-routing.json.txt"
        supreme_path.parent.mkdir(parents=True, exist_ok=True)
        spiderman_path.parent.mkdir(parents=True, exist_ok=True)
        columns = ["name", "position", "public_address", "node"]
        supreme = {section: {"columns": columns, "rows": [["Supreme Route", 2, 1, 8]]} for section in ("switches", "coils", "leds")}
        if duplicate_routing:
            for table in supreme.values():
                table["rows"].append(["Duplicate Route", 2, 1, 8])
        spiderman = {
            section: {"columns": ["public_address", "node", "name", "position"], "rows": [[spiderman_public, 8, "Spider-Man Route", 2]]}
            for section in ("switches", "coils", "leds")
        }
        supreme_path.write_text(json.dumps(supreme), encoding="utf-8")
        spiderman_path.write_text(json.dumps(spiderman), encoding="utf-8")

        manual_root = excerpts / "stern.spider-man-the-pin.2016"
        tables = {
            "manual-drivers.md": ("DR", "1"),
            "manual-switches-page15.md": ("SW", "1"),
            "manual-switches-page17.md": ("SW", "2"),
            "manual-lamps-page18.md": ("LP", "1"),
            "manual-lamps-page20.md": ("LP", "2"),
        }
        for filename, (kind, identifier) in tables.items():
            rows = [f"| {identifier} | Fixture | 8-{kind}-2 |"]
            if duplicate_manual and filename == "manual-drivers.md":
                rows.append("| 1 | Duplicate Fixture | 8-DR-2 |")
            manual_root.joinpath(filename).write_text(
                "\n".join(
                    [
                        "| ID | Name | Address |",
                        "| --- | --- | --- |",
                        *rows,
                        "",
                    ]
                ),
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main()
