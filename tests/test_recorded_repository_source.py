import hashlib
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from recorded_repository_source import verify_recorded_source


class RecordedRepositorySourceTests(unittest.TestCase):
    def test_recorded_bytes_and_failure_boundaries(self):
        path = "tools/run_pinmame_harness.py"
        try:
            current = subprocess.run(
                ["git", "show", f"HEAD:{path}"], cwd=ROOT,
                capture_output=True, timeout=10, check=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("Git repository history is unavailable")
        expected = hashlib.sha256(current).hexdigest()
        verify_recorded_source(ROOT, "HEAD", path, expected)
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            verify_recorded_source(ROOT, "HEAD", path, "0" * 64)
        with self.assertRaisesRegex(ValueError, "historical commit"):
            verify_recorded_source(ROOT, "0" * 40, path, expected)


if __name__ == "__main__":
    unittest.main()
