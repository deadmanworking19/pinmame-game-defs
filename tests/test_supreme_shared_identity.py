from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import supreme_shared_evidence as evidence


class SupremeSharedIdentityTests(unittest.TestCase):
    def test_real_contract_keeps_donor_hardware_qualified_and_driver_mapping_separate(self):
        definition = json.loads((ROOT / "machines/partial/stern/supreme-x-stern-2018.json").read_text(encoding="utf-8"))
        evidence.verify_contract(ROOT, definition)
        self.assertNotIn("driver_mapping", definition["coverage"]["missing"])
        self.assertIn("variant_differences", definition["coverage"]["missing"])
        self.assertEqual("unknown", definition["drivers"][0]["physical_compatibility"])
        switch = next(d for d in definition["inputs"] if d["id"] == "sw.33")
        self.assertIn("type Opto", switch["physical"]["notes"])
        self.assertEqual("unknown", switch["physical"]["switch_type"])
        self.assertNotIn("normally_closed", switch)
        self.assertNotIn("part_number", switch["physical"])
        self.assertNotIn("wiring", switch)
        for mutation in ("driver", "qualification"):
            changed = copy.deepcopy(definition)
            if mutation == "driver":
                changed["drivers"][0]["id"] = "smancp_101"
            else:
                next(d for d in changed["inputs"] if d["id"] == "sw.33")["physical"]["notes"] = "type Opto"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                evidence.verify_contract(ROOT, changed)

    def test_independent_payload_checks_reject_repacked_changes_and_inventory_drift(self):
        for mutation in (None, "payload", "extra", "index"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as folder:
                archive, source, identity, payloads = self.fixture(Path(folder))
                if mutation in ("payload", "extra"):
                    if mutation == "payload":
                        payloads["game"] = b"repacked altered program"
                    else:
                        payloads["extra"] = b"unlisted"
                    with zipfile.ZipFile(archive, "w") as stream:
                        for name, contents in payloads.items():
                            stream.writestr(name, contents)
                    # The outer archive is deliberately repinned: only a full
                    # source/member check can reject these altered payloads.
                    identity["archive"] = {"bytes": archive.stat().st_size, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
                elif mutation == "index":
                    identity["members"][0]["crc32"] = "00000000"
                if mutation is None:
                    evidence.verify_rom_archive(archive, source, identity)
                else:
                    with self.assertRaises(ValueError):
                        evidence.verify_rom_archive(archive, source, identity)

    def test_declared_missing_roots_and_external_path_escape_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": folder}):
                with self.assertRaises((OSError, ValueError)):
                    evidence.verify_external(ROOT)
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": "", "PINMAME_REVIEW_ARTIFACTS_ROOT": str(Path(folder) / "review-artifacts")}):
                with self.assertRaises((OSError, ValueError)):
                    evidence.verify_external(ROOT)
            with self.assertRaises(ValueError):
                evidence._external_uri(Path(folder), "working-root:../../outside")

    @staticmethod
    def fixture(folder):
        payloads = {"game" if i == 0 else f"payload-{i}.bin": f"original payload {i}".encode() for i in range(10)}
        archive, source = folder / "supreme.zip", folder / "spike1.c"
        members, rows = [], []
        with zipfile.ZipFile(archive, "w") as stream:
            for name, contents in payloads.items():
                stream.writestr(name, contents)
                row = {"name": name, "size": len(contents), "crc32": f"{zlib.crc32(contents):08x}", "sha1": hashlib.sha1(contents).hexdigest(), "sha256": hashlib.sha256(contents).hexdigest()}
                members.append(row)
                rows.append(f'ROM_LOAD("{name}", 0x00000000, 0x{row["size"]:08x}, CRC({row["crc32"]}) SHA1({row["sha1"]}))')
        source.write_text("ROM_START(supreme_101)\n" + "\n".join(rows) + "\nROM_END\n", encoding="utf-8")
        identity = {"archive": {"bytes": archive.stat().st_size, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}, "source": {"sha256": hashlib.sha256(source.read_bytes()).hexdigest()}, "members": members}
        return archive, source, identity, payloads


if __name__ == "__main__":
    unittest.main()
