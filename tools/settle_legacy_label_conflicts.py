"""Settle import-legacy label conflicts on bulk-imported records from the game's own ROM.

`import-legacy` recorded a conflict wherever a legacy platform file and a legacy game file named one
public address differently. On several WPC records the platform file's `ROM Started` (legacy alias
`c_game_on`) sits on solenoid 19, where no WPC generation has a game-on output, while the game file
names a flasher there. When a hash-pinned harness run of the game's own ROM shows what the address
is, this tool rewrites that one device from the run, drops the conflict, cites the run, and keeps
`coverage.missing` honest.

Every settlement below names its retained evidence. The tool edits only the listed device, conflict,
source list and coverage; everything else in the record is left as `import-legacy` wrote it. Run
with --check to verify that every listed record already matches what the tool would write.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

RUNTIME_PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
ATTRIBUTION = "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external"

SETTLEMENTS: list[dict[str, Any]] = [
	{
		"path": "machines/partial/bally/black-rose-1992.json",
		"machine_id": "bally.black-rose.1992",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"label": "Right Bottom Flasher",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.black-rose.br-l4.flasher-test",
			"uri": "internal:evidence/runtime/wpc-fliptronic/black-rose-br_l4-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of br_l4 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-fliptronic/br-flasher-test.json) that steps T.5 FLASHER TEST through "
				"flashers 17-28 in repeat mode. At step 19 the ROM pulses public solenoid 19 and prints RIGHT BOTTOM "
				"with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Right Bottom Flasher'. The L-4 ROM's own T.5 FLASHER TEST settles it: it pulses "
			"public 19 among flashers 17-28 and prints RIGHT BOTTOM (BLK-ORN RED-WHT). No WPC generation has a "
			"game-on output at 19, so the platform alias is dropped."
		),
	},
]


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def settle(document: dict[str, Any], settlement: dict[str, Any]) -> dict[str, Any]:
	result = json.loads(json.dumps(document))
	if result["machine"]["id"] != settlement["machine_id"]:
		raise RuntimeError(f"{settlement['path']} is not {settlement['machine_id']}")
	matches = [device for device in result["outputs"] + result["inputs"] if device["binding"] == settlement["binding"]]
	if len(matches) != 1:
		raise RuntimeError(f"{settlement['path']}: expected one device at {settlement['binding']}, found {len(matches)}")
	device = matches[0]
	source = settlement["source"]
	device["id"] = f"device.{slug(settlement['label'])}"
	device["label"] = settlement["label"]
	device["kind"] = settlement["kind"]
	device["aliases"] = [alias for alias in device.get("aliases", []) if alias not in settlement["drop_aliases"]]
	refs = [ref for ref in device["provenance"]["source_refs"] if ref != source["id"]] + [source["id"]]
	device["provenance"] = {"source_refs": refs, "status": "observed"}
	device.setdefault("physical", {})["notes"] = settlement["note"]
	identifiers = [item["id"] for item in result["outputs"] + result["inputs"]]
	if identifiers.count(device["id"]) != 1:
		raise RuntimeError(f"{settlement['path']}: {device['id']} would not be unique")
	result["conflicts"] = [conflict for conflict in result["conflicts"] if conflict["id"] != settlement["conflict_id"]]
	result["sources"] = [item for item in result["sources"] if item["id"] != source["id"]] + [{
		"id": source["id"],
		"kind": "runtime_scenario",
		"uri": source["uri"],
		"revision": RUNTIME_PINMAME_REVISION,
		"locator": source["locator"],
		"license": "NOASSERTION",
		"attribution": ATTRIBUTION,
	}]
	unresolved = [conflict for conflict in result["conflicts"] if conflict.get("status", "unresolved") == "unresolved"]
	if not unresolved:
		result["coverage"]["missing"] = [item for item in result["coverage"]["missing"] if item != "unresolved_conflicts"]
	return result


def canonical(document: dict[str, Any]) -> bytes:
	return (json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
	parser.add_argument("--check", action="store_true", help="verify without writing")
	parser.add_argument("--root", type=Path, default=ROOT)
	args = parser.parse_args()
	drift = []
	for settlement in SETTLEMENTS:
		path = args.root / settlement["path"]
		current = json.loads(path.read_text(encoding="utf-8"))
		if any(conflict["id"] == settlement["conflict_id"] for conflict in current["conflicts"]):
			if args.check:
				drift.append(f"{settlement['path']}: {settlement['conflict_id']} is still recorded")
				continue
			path.write_bytes(canonical_bytes(settle(current, settlement)))
			print(f"settled {settlement['conflict_id']} in {settlement['path']}")
			continue
		# Already settled: re-applying must change nothing.
		if canonical_bytes(settle(current, settlement)) != path.read_bytes():
			drift.append(f"{settlement['path']}: record differs from the settlement")
	for line in drift:
		print(line, file=sys.stderr)
	if drift:
		return 1
	print(f"{len(SETTLEMENTS)} legacy label settlement(s) verified" if args.check else "done")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
