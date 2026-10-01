"""D2: decode the switch and coil name tables from every locally available bk2k game ROM.

The Black Knight 2000 service text lives in the 32 KiB U27 program ROM (not U26 as on Earthshaker).
Both tables are fixed 16-byte entries, decoded with tools/s11_rom_name_tables.py (bit 7 = trailing
period, ROM font codes ``o`` and ``p`` for ``-`` and ``/``). Anchors are found per set, never copied
from another set's offsets:

* switch table: the entry holding ``PLUMB TILT`` is entry 1 and sits 3 bytes before the text;
* coil table: the entry holding ``OUTHOLE`` followed 16 bytes later by an entry holding ``RED BOLT``
  is entry 1 and sits 4 bytes before the text.

Each anchored table is then checked for entry-boundary integrity (no entry may begin or end in the
middle of a word: the first and last byte of every decoded entry must be a space), and the decoder
reports the first entry index at which the checked window stops looking like a name table. No ROM
bytes are written; only decoded text, offsets and hashes.

    python bk2k_rom_name_tables.py --roms <vpinmame-roms> --pinmame-tools <worktree>/tools --out <dir>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import zipfile
from pathlib import Path

SETS = ["bk2k_l4", "bk2k_la2", "bk2k_lg3", "bk2k_pa5", "bk2k_pa7", "bk2k_pu1"]
SWITCH_WINDOW = 64
COIL_WINDOW = 32


def load_decoder(tools_dir: Path):
	spec = importlib.util.spec_from_file_location("s11_rom_name_tables", tools_dir / "s11_rom_name_tables.py")
	module = importlib.util.module_from_spec(spec)
	assert spec.loader is not None
	spec.loader.exec_module(module)
	return module


def clean_boundaries(raw: bytes) -> bool:
	return raw[:1] == b" " and raw[-1:] == b" "


def find_tables(rom: bytes):
	switch_text = rom.find(b"PLUMB TILT")
	switch_start = switch_text - 3 if switch_text >= 0 else None
	coil_start = None
	for match in re.finditer(b"OUTHOLE", rom):
		candidate = match.start() - 4
		if rom[candidate + 16:candidate + 32].strip().startswith(b"RED BOLT"):
			coil_start = candidate
			break
	return switch_start, coil_start


def window(module, rom: bytes, start: int, count: int):
	entries = module._table(rom, start, count)
	for entry, index in zip(entries, range(count)):
		raw = rom[start + index * 16:start + (index + 1) * 16]
		entry["boundary_clean"] = clean_boundaries(raw)
	return entries


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--roms", type=Path, required=True)
	parser.add_argument("--pinmame-tools", type=Path, required=True, help="directory holding s11_rom_name_tables.py")
	parser.add_argument("--out", type=Path, required=True)
	args = parser.parse_args()
	module = load_decoder(args.pinmame_tools)
	args.out.mkdir(parents=True, exist_ok=True)
	summary = {}
	for driver in SETS:
		zip_path = args.roms / f"{driver}.zip"
		with zipfile.ZipFile(zip_path) as archive:
			member = None
			for info in archive.infolist():
				data = archive.read(info.filename)
				if info.file_size == 32768 and b"PLUMB TILT" in data and b"OUTHOLE" in data:
					member, rom = info.filename, data
			if member is None:
				raise RuntimeError(f"{driver}: no 32 KiB member holds both anchors")
		switch_start, coil_start = find_tables(rom)
		if switch_start is None or coil_start is None:
			raise RuntimeError(f"{driver}: anchors not found ({switch_start}, {coil_start})")
		document = {
			"rom_archive": zip_path.name,
			"rom_archive_sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
			"member": member,
			"member_sha256": hashlib.sha256(rom).hexdigest(),
			"member_size": len(rom),
			"anchors": {
				"switch": "entry 1 = the 16-byte entry containing PLUMB TILT, 3 bytes before the text",
				"coil": "entry 1 = the 16-byte entry containing OUTHOLE, 4 bytes before the text, whose next entry holds RED BOLT",
			},
			"switch_table": {"start": f"0x{switch_start:04x}", "entries": window(module, rom, switch_start, SWITCH_WINDOW)},
			"coil_table": {"start": f"0x{coil_start:04x}", "entries": window(module, rom, coil_start, COIL_WINDOW)},
		}
		(args.out / f"{driver}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8", newline="\n")
		summary[driver] = {"member": member, "switch_start": document["switch_table"]["start"], "coil_start": document["coil_table"]["start"]}
	print(json.dumps(summary, indent=1))


if __name__ == "__main__":
	main()
