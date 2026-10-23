"""Transcribe the parts list of Stern's 520-5249-00 I/O power driver board from its PDF text layer.

The LE owner published Stern's manual chapter for the S.A.M. I/O Power Driver PCB 520-5249-00, the
board he reports in his Limited Edition, as ``Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf``. Its
page 129 is the board's complete parts list, items 1-67 under the assembly line. The page is vector,
so this reads every row from the text layer, assigning characters to the printed columns by position
and joining characters whose gap exceeds ``GAP`` points with a space, and writes the seed
``tools/seeds/stern/lord-of-the-rings-limited-edition-2009-io-board-parts.json``.

Four cells do not survive that reading and are given as the page renders them at 220 dpi, in
``RENDERED``: the page overprints two words of items 33 and 39 on each other, drops item 55's ohm
sign from its text layer, and lets item 62's manufacturer number run into the next column. The
assembly line's description runs across the reference column and is joined. The rotated
``Sec. 5: PCBs`` tab along the right edge is not part of the table and is left out.

    python -B tools/lotr_le_io_board_parts.py --write <schematics.pdf>
    python -B tools/lotr_le_io_board_parts.py --check <schematics.pdf>
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import load_json, write_json  # noqa: E402

SEED_PATH = ROOT / "tools/seeds/stern/lord-of-the-rings-limited-edition-2009-io-board-parts.json"
PDF_SHA256 = "ab5c8226945de803b1236db9d06d69043e9a744e7f46fbe140a787a660d15492"
PAGE_INDEX = 5
COLUMNS = (("item", 60, 105), ("qty", 105, 140), ("part", 140, 215), ("mfg", 215, 270), ("ref", 270, 433), ("description", 433, 590))
GAP = 0.9
# Cells read from the page rendered at 220 dpi, with what the text layer gives for each.
RENDERED = {
	("33", "description"): ("Fet Tht. PENTAWAT VN0N2NFet HighSide 26V 6A", "Fet Tht. PENTAWAT VN02N NFet HighSide 26V 6A (VN02N and NFet overprint each other)"),
	("39", "description"): ("I.C. SM SO 74LS138D Hex Inverte3r;-8 DC/DMX", "I.C. SM SO 74LS138D Hex Inverter; 3-8 DC/DMX (Inverter and 3-8 overprint each other)"),
	("55", "description"): ("Potiento THT 50 Single Top Adjust. Trimr.", "Potiento THT 50Ω Single Top Adjust. Trimr."),
	("62", "mfg"): ("(579103B00000G", "(579103B00000G)"),
	("62", "ref"): (") for U1 on TO-3 LM338 5A Adj. Volt. Reg.", "for U1 on TO-3 LM338 5A Adj. Volt. Reg."),
}


def _rows(page) -> list[tuple[float, list[dict]]]:
	rows: list[list] = []
	for block in page.get_text("rawdict")["blocks"]:
		for line in block.get("lines", []):
			if abs(line["dir"][0]) < 0.5:
				continue  # the rotated Sec. 5: PCBs tab
			for span in line["spans"]:
				for char in span["chars"]:
					y = char["bbox"][1]
					for row in rows:
						if abs(row[0] - y) < 1.5:
							row[1].append(char)
							break
					else:
						rows.append([y, [char]])
	return sorted(((y, chars) for y, chars in rows), key=lambda row: row[0])


def _text(chars: list[dict]) -> str:
	out, last = "", None
	for char in sorted(chars, key=lambda c: c["bbox"][0]):
		if char["c"] == " ":
			out, last = out + " ", char["bbox"][2]
			continue
		if last is not None and char["bbox"][0] - last > GAP:
			out += " "
		out, last = out + char["c"], char["bbox"][2]
	return " ".join(out.split())


def transcribe(pdf: Path) -> dict:
	import pymupdf

	data = pdf.read_bytes()
	digest = hashlib.sha256(data).hexdigest()
	if digest != PDF_SHA256:
		raise SystemExit(f"{pdf} is not the retained 520-5249-00 schematic (sha256 {digest})")
	page = pymupdf.open(stream=data, filetype="pdf")[PAGE_INDEX]
	rows = _rows(page)
	title = _text(next(chars for y, chars in rows if y < 25))
	header = _text(next(chars for y, chars in rows if 25 < y < 40))
	entries: list[dict] = []
	for y, chars in rows:
		if not 40 < y < 650:
			continue
		cells = {name: _text([c for c in chars if x0 <= c["bbox"][0] < x1]) for name, x0, x1 in COLUMNS}
		if cells["item"]:
			entries.append(cells)
		else:
			for name, value in cells.items():
				if value:
					entries[-1][name] = f"{entries[-1][name]} {value}".strip()
	# The assembly line prints one description across the reference and description columns.
	assembly = entries[0]
	assembly["description"], assembly["ref"] = f"{assembly['ref']}{assembly['description']}", ""
	for (item, field), (layer, rendered) in RENDERED.items():
		entry = next(e for e in entries if e["item"] == item)
		if entry[field] != layer:
			raise SystemExit(f"item {item} {field}: the text layer gives {entry[field]!r}, not {layer!r}")
		entry[field] = rendered
	if [e["item"] for e in entries] != ["—", *(str(n) for n in range(1, 68))]:
		raise SystemExit("the parts list is not the assembly line followed by items 1-67")
	return {
		"format": "lotr-le-io-board-parts-transcription",
		"header": header,
		"items": entries,
		"source": {
			"document": "Sec 5 Chp 4-3 IO-520-5249-schematics-11x17.pdf",
			"method": f"read from the PDF text layer of page {PAGE_INDEX + 1} by column with tools/lotr_le_io_board_parts.py; the cells in RENDERED from the page rendered at 220 dpi",
			"sha256": digest,
		},
		"title": title,
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", type=Path, metavar="SCHEMATICS_PDF")
	mode.add_argument("--check", type=Path, metavar="SCHEMATICS_PDF")
	args = parser.parse_args()
	if args.write:
		write_json(SEED_PATH, transcribe(args.write))
		print(f"Wrote {SEED_PATH.relative_to(ROOT)}")
		return
	if load_json(SEED_PATH) != transcribe(args.check):
		raise SystemExit(f"{SEED_PATH.relative_to(ROOT)} does not match the schematic's parts list")
	print("520-5249-00 parts list transcription matches the retained schematic.")


if __name__ == "__main__":
	main()
