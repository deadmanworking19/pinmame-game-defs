"""Decode the switch, lamp, coil, flasher and G.I. name tables from The Flintstones game ROM.

The Flintstones' WPC-Security service text lives in the 512 KiB game ROM as tables of 16-bit pointers.
Each table starts with a count byte and a ``0x02`` entry-width byte, followed by ``count`` big-endian
pointers into the same 16 KiB bank, which the CPU sees at ``0x4000-0x7fff``. Each pointer addresses a
NUL-terminated string. The first pointer is a sentinel: ``INVALID SW. NUMBER`` for the switch table,
``INVALID FL. SW. NUM.`` for the Fliptronic switch table, and ``NULL`` for the others. Six English tables
are read:

* switches: the eight dedicated switches D1-D8, then the 64 matrix switches 11-88 in column order;
* Fliptronic switches F1-F8;
* coils, flashers and G.I. strings, each in the ROM's own test order;
* lamps 11-88 in column order.

The ROM holds every table once per language, and more than one English copy. Each table is located by its
sentinel, its count and English anchor entries, never by a carried-over offset; every English copy found
must decode identically. No ROM bytes are written; only decoded text, offsets and hashes.

    python tools/flintstones_rom_name_tables.py --roms <vpinmame-roms> --json <external.json>
    python tools/flintstones_rom_name_tables.py --roms <vpinmame-roms> --markdown <excerpt.md>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

BANK_BYTES = 0x4000
BANK_WINDOW = 0x4000
ENTRY_WIDTH = 0x02
SETS = ("fs_lx5", "fs_lx4", "fs_lx2", "fs_sp2")
REFERENCE_SET = "fs_lx5"
# (key, title, sentinel text, pointer count including the sentinel, English anchor entries by label)
TABLES = (
	("switch_table", "Switch table", "INVALID SW. NUMBER", 73, {"D1": "LEFT COIN SLOT", "11": "LAUNCH BALL"}),
	("flipper_switch_table", "Fliptronic switch table", "INVALID FL. SW. NUM.", 9, {"F1": "R. FLIPPER E.O.S.", "F2": "R. FLIPPER BUTTON"}),
	("coil_table", "Coil table", "NULL", 20, {"1": "TROUGH", "2": "RIGHT SHOOTER"}),
	("flasher_table", "Flasher table", "NULL", 12, {"1": "LFT. RAMP FLS.", "2": "RGHT. RAMP FLS."}),
	("gi_table", "G.I. table", "NULL", 7, {"1": "ILLUM. STRING 1", "6": "ALL ILLUMINATION"}),
	("lamp_table", "Lamp table", "NULL", 65, {"11": "<D>IG", "21": 'LEFT "/" TGT.'}),
)
EXCERPT_SOURCE_NOTE = (
	"Decoded by `tools/flintstones_rom_name_tables.py` from the user-authorized local ROM archive; no ROM bytes are\n"
	"reproduced. Each table in the 512 KiB game ROM is a count byte and a `0x02` entry-width byte followed by that many\n"
	"big-endian pointers into the same 16 KiB bank (seen by the CPU at `0x4000-0x7fff`), each addressing a NUL-terminated\n"
	"string. The first pointer is a sentinel (`INVALID SW. NUMBER`, `INVALID FL. SW. NUM.` or `NULL`) and is not\n"
	"listed. Offsets are file offsets of the first pointer after the sentinel. The ROM holds each table once per\n"
	"language and more than one English copy; a copy is English when its anchor entries match, every English copy\n"
	"must decode identically, and the offset of each copy is listed. Text is shown exactly as stored, in code spans so\n"
	"that the ROM's `<` and `>` letter markers are not read as markup."
)


def string_at(rom: bytes, bank: int, pointer: int) -> str:
	if not BANK_WINDOW <= pointer < BANK_WINDOW + BANK_BYTES:
		raise ValueError(f"pointer 0x{pointer:04x} is outside the banked window")
	start = bank + pointer - BANK_WINDOW
	end = rom.index(b"\x00", start)
	if end >= bank + BANK_BYTES:
		raise ValueError(f"string at 0x{start:05x} runs past its bank")
	return rom[start:end].decode("ascii")


def pointer_at(rom: bytes, offset: int) -> int:
	return (rom[offset] << 8) | rom[offset + 1]


def candidate_tables(rom: bytes, sentinel: str, count: int) -> list[tuple[int, int]]:
	"""Return (bank, offset of the first entry after the sentinel) for every table with this header."""
	candidates = []
	needle = sentinel.encode("ascii") + b"\x00"
	for bank in range(0, len(rom), BANK_BYTES):
		data = rom[bank:bank + BANK_BYTES]
		position = data.find(needle)
		while position >= 0:
			header = bytes([count, ENTRY_WIDTH]) + (BANK_WINDOW + position).to_bytes(2, "big")
			hit = data.find(header)
			while hit >= 0:
				candidates.append((bank, bank + hit + len(header)))
				hit = data.find(header, hit + 1)
			position = data.find(needle, position + 1)
	return candidates


def labels(key: str, count: int) -> list[str]:
	matrix = [f"{column}{row}" for column in range(1, 9) for row in range(1, 9)]
	if key == "switch_table":
		return [f"D{number}" for number in range(1, 9)] + matrix
	if key == "flipper_switch_table":
		return [f"F{number}" for number in range(1, 9)]
	if key == "lamp_table":
		return matrix
	return [str(number) for number in range(1, count + 1)]


def read_entries(rom: bytes, bank: int, start: int, names: list[str]) -> list[dict[str, str]] | None:
	entries = []
	for index, label in enumerate(names):
		offset = start + 2 * index
		try:
			text = string_at(rom, bank, pointer_at(rom, offset))
		except (ValueError, UnicodeDecodeError):
			return None
		entries.append({"label": label, "offset": f"0x{offset:05x}", "text": text})
	return entries


def decode_table(rom: bytes, key: str, sentinel: str, count: int, anchors: dict[str, str]) -> dict[str, Any]:
	"""Decode the English copy of a table.

	The ROM carries the tables once per language and holds more than one English copy; a copy is English when
	every anchor entry matches, and all English copies must decode identically.
	"""
	names = labels(key, count - 1)
	if len(names) != count - 1:
		raise RuntimeError(f"{key}: {count - 1} entries but {len(names)} labels")
	copies = []
	for bank, start in candidate_tables(rom, sentinel, count):
		entries = read_entries(rom, bank, start, names)
		if entries is None:
			continue
		texts_by_label = {entry["label"]: entry["text"] for entry in entries}
		if all(texts_by_label[label] == text for label, text in anchors.items()):
			copies.append((start, entries))
	if not copies:
		raise RuntimeError(f"{key}: no English copy found")
	reference = [entry["text"] for entry in copies[0][1]]
	for start, entries in copies[1:]:
		if [entry["text"] for entry in entries] != reference:
			raise RuntimeError(f"{key}: English copies at 0x{copies[0][0]:05x} and 0x{start:05x} disagree")
	return {"start": f"0x{copies[0][0]:05x}", "copies": [f"0x{start:05x}" for start, _ in copies], "entries": copies[0][1]}


def program_member(archive: zipfile.ZipFile) -> str:
	candidates = [name for name in archive.namelist() if name.casefold().startswith("flin_")]
	if len(candidates) != 1:
		raise RuntimeError(f"cannot choose the game ROM among {archive.namelist()}")
	return candidates[0]


def decode_set(rom_zip: Path) -> dict[str, Any]:
	with zipfile.ZipFile(rom_zip) as archive:
		member = program_member(archive)
		rom = archive.read(member)
	result: dict[str, Any] = {
		"rom_archive": rom_zip.name,
		"rom_archive_sha256": hashlib.sha256(rom_zip.read_bytes()).hexdigest(),
		"member": member,
		"member_sha256": hashlib.sha256(rom).hexdigest(),
		"member_size": len(rom),
	}
	for key, _title, sentinel, count, anchors in TABLES:
		result[key] = decode_table(rom, key, sentinel, count, anchors)
	return result


def texts(result: dict[str, Any], key: str) -> list[str]:
	return [entry["text"] for entry in result[key]["entries"]]


def _cell(text: str) -> str:
	return f"`{text}`" if text else "(empty string)"


def render_markdown(results: dict[str, dict[str, Any]]) -> str:
	reference = results[REFERENCE_SET]
	lines = ["# The Flintstones — ROM switch, lamp, coil, flasher and G.I. name tables", "", EXCERPT_SOURCE_NOTE, ""]
	lines += [
		"| Driver | ROM archive SHA-256 | Game ROM member | Member SHA-256 | Tables identical to fs_lx5 |",
		"| --- | --- | --- | --- | --- |",
	]
	for name, result in results.items():
		differs = [title for key, title, *_ in TABLES if texts(result, key) != texts(reference, key)]
		if name == REFERENCE_SET:
			verdict = "reference"
		else:
			verdict = "all six" if not differs else "differ: " + ", ".join(differs)
		lines.append(f"| {name} | `{result['rom_archive_sha256']}` | {result['member']} | `{result['member_sha256']}` | {verdict} |")
	lines += ["", "English copies in the reference set:", "", "| Table | Copies (first entry offset) | Entries |", "| --- | --- | ---: |"]
	lines += [f"| {title} | {', '.join(reference[key]['copies'])} | {len(reference[key]['entries'])} |" for key, title, *_ in TABLES]
	headings = {
		"switch_table": ("## Switch table (D1-D8, then matrix switches 11-88 in column order)", "Switch"),
		"flipper_switch_table": ("## Fliptronic switch table (F1-F8)", "Switch"),
		"coil_table": ("## Coil table (ROM coil-test order; entry numbers are table positions, not addresses)", "Entry"),
		"flasher_table": ("## Flasher table (ROM flasher-test order; entry numbers are table positions, not addresses)", "Entry"),
		"gi_table": ("## G.I. table (ROM test order)", "Entry"),
		"lamp_table": ("## Lamp table (lamps 11-88 in column order)", "Lamp"),
	}
	for key, *_ in TABLES:
		heading, column = headings[key]
		lines += ["", heading, "", f"| {column} | ROM text |", "| --- | --- |"]
		lines += [f"| {entry['label']} | {_cell(entry['text'])} |" for entry in reference[key]["entries"]]
	lines += [
		"",
		"The coil, flasher and G.I. tables carry no solenoid or string numbers, so they do not by themselves pair an entry",
		"with a public address; the definition records how each pairing was settled.",
		"",
	]
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
