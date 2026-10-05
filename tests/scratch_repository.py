"""Scratch copies of repository files for tests that must mutate a curator's inputs.

A test that edits a tracked file in place and restores it in ``finally`` leaves the checkout dirty
whenever the restore itself fails, for example when Windows briefly locks the file, and every later
validation and curator test then fails on that leftover. Tests copy what they need here instead and
point the curator at the copy, so no tracked file is ever written.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]


def copy_repository_files(scratch: Path, *paths: Path) -> Path:
	"""Copy repository files, given absolute or ROOT-relative, to the same relative paths under ``scratch``."""
	for path in paths:
		relative = path.relative_to(ROOT) if path.is_absolute() else path
		target = scratch / relative
		target.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(ROOT / relative, target)
	return scratch


def copy_repository_trees(scratch: Path, *directories: str) -> Path:
	"""Copy whole ROOT-relative directories to the same relative paths under ``scratch``."""
	for directory in directories:
		shutil.copytree(ROOT / directory, scratch / directory)
	return scratch


def copy_curator_files(curator: ModuleType, scratch: Path) -> Path:
	"""Copy every existing repository file a curator names in a module-level ``Path`` constant.

	This suits curators whose ``check(root)`` resolves each artifact as ``root / CONSTANT.relative_to(ROOT)``.
	A test should prove the copy complete by running ``check`` on it before mutating anything.
	"""
	files = []
	for value in vars(curator).values():
		if not isinstance(value, Path) or not value.is_absolute():
			continue
		try:
			value.relative_to(ROOT)
		except ValueError:
			continue
		if value.is_file():
			files.append(value)
	if not files:
		raise AssertionError(f"{curator.__name__} names no repository file to copy")
	return copy_repository_files(scratch, *files)
