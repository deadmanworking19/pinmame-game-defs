"""Decode the lamp, switch and coil name tables from the Space Station game ROM.

Space Station's System 11B service text lives in the 32 KiB U27 program ROM as fixed 14-byte entries:
seven characters for the player 1 display followed by seven for the player 2 display, which is how the
Single Lamps, Switch Levels and Coil tests print them. A byte with bit 7 set is the character in its low
seven bits followed by the display's period segment. Three tables are read:

* the lamp table, 64 entries in public lamp order, ending where the switch table begins;
* the switch table, 64 entries in public switch order, whose first entry is `` PLUMB  TILT  ``;
* the coil table, which on this ROM does not follow the switch table directly: a block of non-text bytes
  sits between them, and the table starts at ``OUTHOLE`` followed by ``RELNCH FLASHER``. It runs in the
  ROM's own coil-test order (28 names, none for the unused drives 5 and 14) and ends with a ``NOT USED``
  entry and a blank one, after which the audit-name table begins.

Each table is located by its anchor text, never by a carried-over offset, and each anchor is checked. No
ROM bytes are written; only decoded text, offsets and hashes.

    python tools/space_station_rom_name_tables.py --roms <vpinmame-roms> --json <external.json>
    python tools/space_station_rom_name_tables.py --roms <vpinmame-roms> --markdown <excerpt.md>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

ENTRY_BYTES = 14
HALF = 7
SETS = ("spstn_l5",)
LAMP_COUNT = 64
SWITCH_COUNT = 64
COIL_ANCHOR = b"OUTHOLE       RELNCH FLASHER"
COIL_COUNT = 30
EXCERPT_SOURCE_NOTE = (
	"Decoded by `tools/space_station_rom_name_tables.py` from the user-authorized local ROM archive; no ROM bytes are\n"
	"reproduced. Each table is a run of fixed 14-byte entries in the 32 KiB **U27** program ROM: seven characters for the\n"
	"player 1 display followed by seven for the player 2 display, which is how the Single Lamps, Switch Levels and Coil\n"
	"tests print them. A byte with bit 7 set is the character in its low seven bits followed by the display's period\n"
	"segment. Entries are shown with the two halves joined by one space and padding trimmed. The lamp table ends where\n"
	"the switch table begins; the coil table starts at its own anchor further on, after a block of non-text bytes."
)


def decode_text(raw: bytes) -> str:
	text = []
	for value in raw:
		if value >= 0x80:
			text.append(chr(value & 0x7F) + ".")
		elif 32 <= value < 127:
			text.append(chr(value))
		else:
			text.append(f"<{value:02x}>")
	return "".join(text)


def decode_entry(raw: bytes) -> dict[str, str]:
	top, bottom = decode_text(raw[:HALF]), decode_text(raw[HALF:])
	return {"player_1": top, "player_2": bottom, "text": " ".join(part for part in (top.strip(), bottom.strip()) if part)}


def table(rom: bytes, start: int, count: int) -> list[dict[str, Any]]:
	entries = []
	for index in range(count):
		offset = start + index * ENTRY_BYTES
		entry = decode_entry(rom[offset:offset + ENTRY_BYTES])
		entries.append({"index": index + 1, "offset": f"0x{offset:04x}", **entry})
	return entries


def program_member(archive: zipfile.ZipFile) -> str:
	candidates = [name for name in archive.namelist() if "u27" in name.casefold()]
	if len(candidates) != 1:
		raise RuntimeError(f"cannot choose the U27 program ROM among {archive.namelist()}")
	return candidates[0]


def decode_set(rom_zip: Path) -> dict[str, Any]:
	with zipfile.ZipFile(rom_zip) as archive:
		member = program_member(archive)
		rom = archive.read(member)
	switch_start = rom.find(b" PLUMB  TILT  ")
	if switch_start < 0 or rom.find(b" PLUMB  TILT  ", switch_start + 1) >= 0:
		raise RuntimeError(f"{rom_zip.name}: switch table anchor missing or ambiguous")
	lamp_start = switch_start - LAMP_COUNT * ENTRY_BYTES
	if decode_entry(rom[lamp_start:lamp_start + ENTRY_BYTES])["text"] != "BON BAL PLYR 1":
		raise RuntimeError(f"{rom_zip.name}: lamp table does not end at the switch table")
	coil_start = rom.find(COIL_ANCHOR)
	if coil_start < 0 or rom.find(COIL_ANCHOR, coil_start + 1) >= 0:
		raise RuntimeError(f"{rom_zip.name}: coil table anchor missing or ambiguous")
	coils = table(rom, coil_start, COIL_COUNT)
	if coils[-2]["text"] != "NOT USED" or coils[-1]["text"] != "":
		raise RuntimeError(f"{rom_zip.name}: coil table does not end with NOT USED and a blank entry")
	return {
		"rom_archive": rom_zip.name,
		"rom_archive_sha256": hashlib.sha256(rom_zip.read_bytes()).hexdigest(),
		"member": member,
		"member_sha256": hashlib.sha256(rom).hexdigest(),
		"member_size": len(rom),
		"lamp_table": {"start": f"0x{lamp_start:04x}", "entries": table(rom, lamp_start, LAMP_COUNT)},
		"switch_table": {"start": f"0x{switch_start:04x}", "entries": table(rom, switch_start, SWITCH_COUNT)},
		"coil_table": {"start": f"0x{coil_start:04x}", "entries": coils},
	}


def _cell(text: str) -> str:
	return text if text else "(blank)"


def render_markdown(results: dict[str, dict[str, Any]]) -> str:
	lines = ["# Space Station — ROM lamp, switch and coil name tables", "", EXCERPT_SOURCE_NOTE, ""]
	lines += ["| Driver | ROM archive SHA-256 | ROM member | Member SHA-256 | Lamp table | Switch table | Coil table |", "| --- | --- | --- | --- | --- | --- | --- |"]
	for name, result in results.items():
		lines.append(
			f"| {name} | `{result['rom_archive_sha256']}` | {result['member']} | `{result['member_sha256']}` | "
			f"{result['lamp_table']['start']} | {result['switch_table']['start']} | {result['coil_table']['start']} |"
		)
	reference = results[SETS[0]]
	lines += ["", "## Lamp table (public lamp address = entry number)", "", "| Lamp | ROM text |", "| --- | --- |"]
	lines += [f"| {entry['index']} | {_cell(entry['text'])} |" for entry in reference["lamp_table"]["entries"]]
	lines += ["", "## Switch table (public switch address = entry number)", "", "| Switch | ROM text |", "| --- | --- |"]
	lines += [f"| {entry['index']} | {_cell(entry['text'])} |" for entry in reference["switch_table"]["entries"]]
	lines += [
		"", "## Coil table (ROM coil-test order; entry numbers are table positions, not addresses)", "",
		"The ROM's Coil Test pairs each displayed entry with the public solenoid it pulses; that pairing is in the",
		"runtime evidence, not in this table. The audit-name table (`LEFT COINS`, ...) follows the blank entry.", "",
		"| Entry | ROM text |", "| --- | --- |",
	]
	lines += [f"| {entry['index']} | {_cell(entry['text'])} |" for entry in reference["coil_table"]["entries"]]
	lines += ["", "Normalization: each seven-character half is trimmed and the halves are joined with one space; spaces inside a half are kept.", ""]
	return "\n".join(lines)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--roms", type=Path, required=True, help="read-only ROM archive directory")
	parser.add_argument("--json", type=Path, help="external output file for the full decode")
	parser.add_argument("--markdown", type=Path, help="excerpt file to write")
	args = parser.parse_args()
	results = {name: decode_set(args.roms / f"{name}.zip") for name in SETS}
	if args.json:
		args.json.parent.mkdir(parents=True, exist_ok=True)
		args.json.write_bytes((json.dumps(results, indent=1) + "\n").encode("utf-8"))
	if args.markdown:
		args.markdown.write_bytes(render_markdown(results).encode("utf-8"))
	if not args.json and not args.markdown:
		print(json.dumps(results, indent=1))


if __name__ == "__main__":
	main()
