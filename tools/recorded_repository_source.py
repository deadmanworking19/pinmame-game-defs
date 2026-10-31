"""Verify the repository source bytes recorded by historical evidence."""

import hashlib
import subprocess


def verify_recorded_source(root, revision, path, expected_sha256):
    """Reject missing history or a digest mismatch instead of using today's file."""
    try:
        result = subprocess.run(
            ["git", "show", f"{revision}:{path}"], cwd=root,
            capture_output=True, timeout=10, check=True,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        raise ValueError(
            f"Cannot read recorded repository source {revision}:{path}; "
            "ensure Git and the historical commit are available"
        ) from error
    actual = hashlib.sha256(result.stdout).hexdigest()
    if actual != expected_sha256:
        raise ValueError(
            f"Recorded repository source hash mismatch for {revision}:{path}: "
            f"expected {expected_sha256}, got {actual}"
        )
