"""Decode the lamp, switch and coil name tables from the Cyclone game ROMs.

Cyclone's System 11B service text lives in the 32 KiB U27 program ROM, which the CPU maps at 0x8000. Each name
is a 14-byte record: seven characters for the player 1 display followed by seven for the player 2 display, which
is how the Single Lamps, Switch Levels and Coil tests print them. A byte with bit 7 set is the character in its
low seven bits followed by the display's period segment. Unlike Space Station's ROM, the tests do not index the
records directly; they go through big-endian pointer tables:

* the switch table is 64 records in public switch order, the first of which is `` PLUMB  TILT  ``;
* the coil pointer table follows the switch table directly: 44 pointers, two per coil-test step 01-22, the
  first naming the A-side (or only) load and the second the C-side load of an A/C-multiplexed drive;
* the lamp pointer table is 64 pointers, one per public lamp, and ends where the first lamp-only record begins;
  lamps that share a switch's name point into the switch table.

Each table is located from its anchor and checked, never by a carried-over offset. No ROM bytes are written;
only decoded text, offsets, pointers and hashes.

    python tools/cyclone_rom_name_tables.py --roms <vpinmame-roms> --json <external.json>
    python tools/cyclone_rom_name_tables.py --roms <vpinmame-roms> --markdown <excerpt.md>
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
BASE = 0x8000
SETS = ("cycln_l5", "cycln_l4", "cycln_l1")
SWITCH_ANCHOR = b" PLUMB  TILT  "
LAMP_COUNT = 64
SWITCH_COUNT = 64
COIL_STEPS = 22
EXCERPT_SOURCE_NOTE = (
	"Decoded by `tools/cyclone_rom_name_tables.py` from the user-authorized local ROM archives; no ROM bytes are\n"
	"reproduced. Every name is a fixed 14-byte record in the 32 KiB **U27** program ROM (mapped at 0x8000): seven\n"
	"characters for the player 1 display followed by seven for the player 2 display, which is how the Single Lamps,\n"
	"Switch Levels and Coil tests print them. A byte with bit 7 set is the character in its low seven bits followed by\n"
	"the display's period segment (shown as `.`). The switch records are read in place; the coil and lamp names are\n"
	"read through the ROM's own big-endian pointer tables, so a lamp that shares a switch's name points into the\n"
	"switch table. Entries show the two halves joined by one space with padding trimmed. The three game ROMs decode\n"
	"to identical text at identical offsets."
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


def record(rom: bytes, offset: int) -> dict[str, str]:
	if not 0 <= offset <= len(rom) - ENTRY_BYTES:
		raise RuntimeError(f"name record 0x{offset:04x} lies outside the ROM")
	return decode_entry(rom[offset:offset + ENTRY_BYTES])


def pointer(rom: bytes, offset: int) -> int:
	return int.from_bytes(rom[offset:offset + 2], "big") - BASE


def program_member(archive: zipfile.ZipFile) -> str:
	candidates = [name for name in archive.namelist() if "u27" in name.casefold()]
	if len(candidates) != 1:
		raise RuntimeError(f"cannot choose the U27 program ROM among {archive.namelist()}")
	return candidates[0]


def decode_set(rom_zip: Path) -> dict[str, Any]:
	with zipfile.ZipFile(rom_zip) as archive:
		member = program_member(archive)
		rom = archive.read(member)
	if len(rom) != 0x8000:
		raise RuntimeError(f"{rom_zip.name}: U27 is not 32 KiB")
	switch_start = rom.find(SWITCH_ANCHOR)
	if switch_start < 0 or rom.find(SWITCH_ANCHOR, switch_start + 1) >= 0:
		raise RuntimeError(f"{rom_zip.name}: switch table anchor missing or ambiguous")
	switches = []
	for index in range(SWITCH_COUNT):
		offset = switch_start + index * ENTRY_BYTES
		switches.append({"index": index + 1, "offset": f"0x{offset:04x}", **record(rom, offset)})
	if switches[-1]["text"] != "RIGHT KICKER" or switches[9]["text"] != "OUTHOLE":
		raise RuntimeError(f"{rom_zip.name}: switch table does not run from PLUMB TILT to RIGHT KICKER")

	coil_pointers = switch_start + SWITCH_COUNT * ENTRY_BYTES
	coils = []
	for step in range(1, COIL_STEPS + 1):
		names = []
		for side in (0, 1):
			slot = coil_pointers + 2 * (2 * (step - 1) + side)
			target = pointer(rom, slot)
			names.append({"pointer_offset": f"0x{slot:04x}", "record": f"0x{target:04x}", **record(rom, target)})
		coils.append({"step": step, "first": names[0], "second": names[1]})
	if coils[0]["first"]["text"] != "OUTHOLE" or coils[-1]["first"]["text"] != "NOT USED":
		raise RuntimeError(f"{rom_zip.name}: coil pointer table does not follow the switch table")
	coil_records_start = coil_pointers + 4 * COIL_STEPS
	if int(coils[0]["second"]["record"], 16) != coil_records_start:
		raise RuntimeError(f"{rom_zip.name}: the first C-side name does not start right after the coil pointers")

	candidates = [c for c in range(0, switch_start - 2 * LAMP_COUNT) if pointer(rom, c) == c + 2 * LAMP_COUNT]
	candidates = [c for c in candidates if record(rom, c + 2 * LAMP_COUNT)["text"] == "HOLD"]
	if len(candidates) != 1:
		raise RuntimeError(f"{rom_zip.name}: lamp pointer table not found exactly once")
	lamp_pointers = candidates[0]
	lamps = []
	for index in range(LAMP_COUNT):
		slot = lamp_pointers + 2 * index
		target = pointer(rom, slot)
		in_switch_table = switch_start <= target < coil_pointers
		if in_switch_table and (target - switch_start) % ENTRY_BYTES:
			raise RuntimeError(f"{rom_zip.name}: lamp {index + 1} points between switch records")
		lamps.append({"index": index + 1, "pointer_offset": f"0x{slot:04x}", "record": f"0x{target:04x}",
		              "shared_switch": (target - switch_start) // ENTRY_BYTES + 1 if in_switch_table else None, **record(rom, target)})
	return {
		"rom_archive": rom_zip.name,
		"rom_archive_sha256": hashlib.sha256(rom_zip.read_bytes()).hexdigest(),
		"member": member,
		"member_sha256": hashlib.sha256(rom).hexdigest(),
		"member_size": len(rom),
		"lamp_pointer_table": f"0x{lamp_pointers:04x}",
		"switch_table": f"0x{switch_start:04x}",
		"coil_pointer_table": f"0x{coil_pointers:04x}",
		"lamps": lamps,
		"switches": switches,
		"coils": coils,
	}


def text_only(result: dict[str, Any]) -> tuple:
	return (result["lamp_pointer_table"], result["switch_table"], result["coil_pointer_table"],
	        [(e["record"], e["text"]) for e in result["lamps"]], [e["text"] for e in result["switches"]],
	        [(c["first"]["text"], c["second"]["text"]) for c in result["coils"]])


def _cell(text: str) -> str:
	return text if text else "(blank)"


def render_markdown(results: dict[str, dict[str, Any]]) -> str:
	reference = results[SETS[0]]
	for name, result in results.items():
		if text_only(result) != text_only(reference):
			raise RuntimeError(f"{name} name tables differ from {SETS[0]}")
	lines = ["# Cyclone - ROM lamp, switch and coil name tables", "", EXCERPT_SOURCE_NOTE, ""]
	lines += ["| Driver | ROM archive SHA-256 | ROM member | Member SHA-256 | Lamp pointers | Switch table | Coil pointers |", "| --- | --- | --- | --- | --- | --- | --- |"]
	for name, result in results.items():
		lines.append(f"| {name} | `{result['rom_archive_sha256']}` | {result['member']} | `{result['member_sha256']}` | "
		             f"{result['lamp_pointer_table']} | {result['switch_table']} | {result['coil_pointer_table']} |")
	lines += ["", "## Lamp names (public lamp address = pointer number)", "", "| Lamp | Record | ROM text |", "| --- | --- | --- |"]
	for entry in reference["lamps"]:
		where = entry["record"] + (f" (switch {entry['shared_switch']}'s record)" if entry["shared_switch"] else "")
		lines.append(f"| {entry['index']} | {where} | {_cell(entry['text'])} |")
	lines += ["", "## Switch names (public switch address = record number)", "", "| Switch | ROM text |", "| --- | --- |"]
	lines += [f"| {entry['index']} | {_cell(entry['text'])} |" for entry in reference["switches"]]
	lines += ["", "## Coil-test names (two pointers per step)", "",
	          "Steps 01-08 name the A-side load first and the C-side load second; from step 09 the second pointer is the",
	          "blank record. The ROM's Coil Test pairs each displayed step with the public solenoid it pulses; that",
	          "pairing is in the runtime evidence, not in this table.", "",
	          "| Step | First name | Second name |", "| --- | --- | --- |"]
	lines += [f"| {c['step']:02d} | {_cell(c['first']['text'])} | {_cell(c['second']['text'])} |" for c in reference["coils"]]
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
		args.markdown.parent.mkdir(parents=True, exist_ok=True)
		args.markdown.write_bytes(render_markdown(results).encode("utf-8"))
	if not args.json and not args.markdown:
		print(json.dumps(results, indent=1))


if __name__ == "__main__":
	main()
