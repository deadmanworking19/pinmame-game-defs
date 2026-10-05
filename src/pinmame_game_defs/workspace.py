from __future__ import annotations

import os
from pathlib import Path

from .errors import DefinitionError


WORKING_ROOT_ENVIRONMENT_VARIABLE = "PINMAME_WORKING_ROOT"
WORKING_ROOT_DIRECTORY_NAME = "pinmame-game-defs-working-dir"


def resolve_working_root(repository_root: Path, *, required: bool = False) -> Path:
	"""Resolve the shared evidence root from a checkout or nested git worktree."""
	override = os.environ.get(WORKING_ROOT_ENVIRONMENT_VARIABLE, "").strip()
	if override:
		working_root = Path(override).expanduser().resolve()
	else:
		repository_root = repository_root.resolve()
		working_root = repository_root.parent / WORKING_ROOT_DIRECTORY_NAME
		for ancestor in (repository_root, *repository_root.parents):
			if ancestor.name == WORKING_ROOT_DIRECTORY_NAME and ancestor.is_dir():
				working_root = ancestor
				break
			candidate = ancestor / WORKING_ROOT_DIRECTORY_NAME
			if candidate.is_dir():
				working_root = candidate
				break
	if required and not working_root.is_dir():
		raise DefinitionError(
			f"Shared working root is missing: {working_root}. "
			f"Set {WORKING_ROOT_ENVIRONMENT_VARIABLE} to its absolute path."
		)
	return working_root


def pinmame_source_at(revision: str, repository_root: Path) -> Path:
	"""Return a PinMAME source tree at exactly ``revision``, read-only for the caller.

	Records and evidence cite the revision they were read at, which can predate the current pin. The managed
	checkout serves when it sits cleanly at that revision; otherwise the revision is exported from the
	checkout's own history (``git archive``) once into ``<working-root>/builds/pinmame-src-<revision>`` and
	reused. The export carries a marker naming its revision, and an interrupted export is refused rather than
	reused.
	"""
	import io
	import subprocess
	import tarfile

	working_root = resolve_working_root(repository_root, required=True)
	checkout = working_root / "source-checkouts" / "pinmame"

	def git(*arguments: str) -> bytes:
		return subprocess.run(["git", "-C", str(checkout), *arguments], check=True, capture_output=True).stdout

	if git("rev-parse", "HEAD").decode("ascii").strip() == revision and not git("status", "--porcelain").strip():
		return checkout
	export = working_root / "builds" / f"pinmame-src-{revision}"
	marker = export / ".pinmame-revision"
	if marker.is_file() and marker.read_bytes().decode("ascii").strip() == revision:
		return export
	if export.exists():
		raise DefinitionError(f"Unexpected PinMAME export without a matching revision marker: {export}")
	staging = export.with_name(export.name + ".incoming")
	if staging.exists():
		raise DefinitionError(f"Refusing to reuse an incomplete PinMAME export: {staging}")
	with tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", revision))) as archive:
		archive.extractall(staging, filter="data")
	(staging / ".pinmame-revision").write_bytes(revision.encode("ascii") + b"\n")
	staging.rename(export)
	return export
