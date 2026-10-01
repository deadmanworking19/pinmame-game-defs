"""Settle import-legacy label conflicts on bulk-imported records from the game's own ROM.

`import-legacy` recorded a conflict wherever a legacy platform file and a legacy game file named one
public address differently. On several WPC records the platform file's `ROM Started` (legacy alias
`c_game_on`) sits on solenoid 19, where no WPC generation has a game-on output, while the game file
names a flasher there; on others the game file puts playfield sensors on the coin-door switches the
platform file places at 1-4, or, on System 11, calls the game-on line at 23 a tilt output. When a
hash-pinned harness run of the game's own ROM shows what the address is, this tool rewrites that one
device from the run, drops the conflict, cites the run, and keeps `coverage.missing` honest.

Every settlement below names its retained evidence. Several settlements may cite one run; a device
keeps its id unless the settlement gives a new one. A settlement names the id and label
`import-legacy` gave the device, and the tool refuses a device that carries neither those nor the
settled ones, or whose public-number aliases name another address. The tool edits only the listed
device, conflict, source list and coverage; everything else in the record is left as
`import-legacy` wrote it, and a record whose `coverage.missing` omits `unresolved_conflicts` while
one remains is refused. Run with --check to verify that every listed record already matches what
the tool would write.
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

NBA_FASTBREAK_SWITCH_EDGES = {
	"id": "runtime.nba-fastbreak.nbaf-31.switch-edges",
	"uri": "internal:evidence/runtime/wpc-95/nba-fastbreak-nbaf_31-switch-edges.json",
	"locator": (
		"One hash-pinned LibPinMAME harness run of nbaf_31 from empty NVRAM (scenario "
		"tools/harness-scenarios/wpc-95/nbaf-switch-edges-1-4-12.json) that holds public 12, 1, 2, 3, 4 and 12 again "
		"at each level for 2 s inside T.1 SWITCH EDGES. At level 1 the ROM's top line names public 1-3 LEFT, CENTER "
		"and RIGHT COIN SLOT, public 4 4TH COIN OPTION, and public 12 BACKBOX BASKET; it reports 1-4 as LAST SW D1-D4, "
		"the coin-door switches."
	),
}
NBA_FASTBREAK_COIN_NOTE = (
	"Legacy import set the WPC platform map's 'Coin Button {n}' against the game file's 'Backbox Basket Score {n}'. "
	"In T.1 SWITCH EDGES the 3.1 ROM names public {n} {name} and reports it as LAST SW D{n}, a coin-door switch "
	"({wires}); it names public 12 BACKBOX BASKET, the one backbox basket switch nbaf.c defines (swBackboxBasket). "
	"Public {n} is the coin slot WPC_COMPORTS places there; the game file's 'Backbox Basket Score' labels at 1-3 do "
	"not match what the ROM reads at those matrix positions."
)

SETTLEMENTS: list[dict[str, Any]] = [
	{
		"path": "machines/partial/bally/black-rose-1992.json",
		"machine_id": "bally.black-rose.1992",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
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
	{
		"path": "machines/partial/williams/no-fear-dangerous-sports-1995.json",
		"machine_id": "williams.no-fear-dangerous-sports.1995",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flasher: No Fear",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.no-fear.nf-23x.flasher-test",
			"uri": "internal:evidence/runtime/wpc-security/no-fear-nf_23x-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of nf_23x from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-security/nf-flasher-test.json) that steps T.5 FLASHER TEST through "
				"flashers 17-28 in repeat mode. At step 19 the ROM pulses public solenoid 19 and prints FLS. NO FEAR "
				"with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Flasher: No Fear (x2)'. The 2.3 X ROM's own T.5 FLASHER TEST settles it: it "
			"pulses public 19 among flashers 17-28 and prints FLS. NO FEAR (BLK-ORN RED-WHT). No WPC generation has a "
			"game-on output at 19, so the platform alias is dropped. The ROM names one output, not a bulb count: the "
			"game file's '(x2)' quantity is not confirmed by the run."
		),
	},
	{
		"path": "machines/partial/bally/doctor-who-1992.json",
		"machine_id": "bally.doctor-who.1992",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flasher F19 (5x3 Right/Right)",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.doctor-who.dw-l2.flasher-test",
			"uri": "internal:evidence/runtime/wpc-fliptronic/doctor-who-dw_l2-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of dw_l2 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-fliptronic/dw-flasher-test.json) that steps T.5 FLASHER TEST through the "
				"flashers 6, 8, 14 and 17-24 in repeat mode. At step 19 the ROM pulses public solenoid 19 and prints "
				"5x3 Right/Right with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Flasher F19'. The L-2 ROM's own T.5 FLASHER TEST settles it: it pulses public 19 "
			"among the flashers 6, 8, 14 and 17-24 and prints 5x3 Right/Right (BLK-ORN RED-WHT). No WPC generation has "
			"a game-on output at 19, so the platform alias is dropped."
		),
	},
	{
		"path": "machines/partial/williams/red-and-ted-s-road-show-1994.json",
		"machine_id": "williams.red-and-ted-s-road-show.1994",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Ted Motor Direction",
		"kind": "coil",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.red-and-ted-s-road-show.rs-l6.ted-test",
			"uri": "internal:evidence/runtime/wpc-security/red-and-ted-s-road-show-rs_l6-ted-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of rs_l6 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-security/rs-ted-test.json) that starts T.17 \"TED\" TEST and lets it run two "
				"cycles. As the display reaches 06 MOUTH OPEN the ROM raises public 19 together with 20, drops 20 about "
				"0.33 s and 19 about 0.39 s later, and in 07 MOUTH CLOSED drives 20 alone; 19 never rises without 20."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Ted Motor Direction'. Pinned rs.c names 19 sTedMotorDrv, and the L-6 ROM's own "
			"T.17 \"TED\" TEST settles it: in step 06 MOUTH OPEN it raises public 19 together with 20 (Ted Mouth Motor) "
			"and releases 19 just after 20, and in step 07 MOUTH CLOSED it drives 20 alone. So 19 sets the direction of "
			"Ted's mouth motor and is set for opening, which is also how rs.c's simulation reads it. No WPC generation "
			"has a game-on output at 19, so the platform alias is dropped."
		),
	},
	{
		"path": "machines/partial/williams/diner-1990.json",
		"machine_id": "williams.diner.1990",
		"conflict_id": "conflict.pinmame-output-solenoid-23-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 23},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Game-On / Special-Solenoid Enable",
		"kind": "virtual",
		"drop_aliases": [],
		"source": {
			"id": "runtime.diner.diner-l4.game-on-23",
			"uri": "internal:evidence/runtime/system-11/diner-diner_l4-game-on-23.json",
			"locator": (
				"Two hash-pinned LibPinMAME harness runs of diner_l4: a factory-settings initialization from empty NVRAM "
				"(tools/harness-scenarios/system-11/diner-nvram-init.json), then a three-ball game from a fresh state "
				"holding only its .nv file (tools/harness-scenarios/system-11/diner-game-on-23.json). Public 23 is 0 in "
				"attract mode, rises during the start press, drops at the third plumb-bob tilt, rises again for ball 2, "
				"stays 1 through balls 2 and 3, and drops when ball 3 ends the game."
			),
		},
		"note": (
			"Legacy import set the legacy platform map's 'ROM Started' (alias c_game_on) against the game file's "
			"'Tilt'. Pinned s11.c publishes public 23 as S11_GAMEONSOL from PIA0 CB2, the flipper and special-solenoid "
			"enable, and a diner_l4 gameplay run settles it: 23 is 0 in attract mode, rises during the start press, "
			"drops at the third plumb-bob tilt, rises again for ball 2 and drops when ball 3 ends the game. It is the "
			"game-on enable, so the c_game_on alias stays; 'Tilt' names an event that drops it. As the System 11 "
			"controller profile records, it has no driver-board device of its own."
		),
	},
	*[
		{
			"path": "machines/partial/bally/nba-fastbreak-1997.json",
			"machine_id": "bally.nba-fastbreak.1997",
			"conflict_id": f"conflict.pinmame-input-switch-{number}-none",
			"binding": {"group": "pinmame.input.switch", "device": number},
			"from": {"id": f"switch.coin-{number}", "label": f"Coin Button {number}"},
			"id": f"switch.coin-{number}",
			"label": name.title(),
			"kind": "switch",
			"drop_aliases": [],
			"source": NBA_FASTBREAK_SWITCH_EDGES,
			"note": NBA_FASTBREAK_COIN_NOTE.format(n=number, name=name, wires=wires),
		}
		for number, name, wires in (
			(1, "LEFT COIN SLOT", "ORN-BRN BLACK"),
			(2, "CENTER COIN SLOT", "ORN-RED BLACK"),
			(3, "RIGHT COIN SLOT", "ORN-BLK BLACK"),
		)
	],
	{
		"path": "machines/partial/bally/nba-fastbreak-1997.json",
		"machine_id": "bally.nba-fastbreak.1997",
		"conflict_id": "conflict.pinmame-output-solenoid-19-none",
		"binding": {"group": "pinmame.output.solenoid", "device": 19},
		"from": {"id": "device.game-on", "label": "ROM Started"},
		"label": "Flasher — Upper Left",
		"kind": "flasher",
		"drop_aliases": [{"namespace": "vpe-legacy.coil", "value": "c_game_on"}],
		"source": {
			"id": "runtime.nba-fastbreak.nbaf-31.flasher-test",
			"uri": "internal:evidence/runtime/wpc-95/nba-fastbreak-nbaf_31-flasher-test.json",
			"locator": (
				"One hash-pinned LibPinMAME harness run of nbaf_31 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-95/nbaf-flasher-test.json) that steps T.5 FLASHER TEST through the "
				"flashers 17, 18, 19, 20, 22 and 24 in repeat mode. At step 19 the ROM pulses public solenoid 19 and "
				"prints UPPER LEFT with the wires BLK-ORN RED-WHT."
			),
		},
		"note": (
			"Legacy import labelled this address 'ROM Started' (alias c_game_on) from the legacy WPC platform map, "
			"against the game file's 'Flasher — Upper Left / BG Left'. The 3.1 ROM's own T.5 FLASHER TEST settles "
			"it: it pulses public 19 among flashers 17, 18, 19, 20, 22 and 24 and prints UPPER LEFT (BLK-ORN RED-WHT). "
			"No WPC generation has a game-on output at 19, so the platform alias is dropped. The ROM names one "
			"output, so the game file's '/ BG Left' is not confirmed by the run."
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
	group, number = settlement["binding"]["group"], settlement["binding"]["device"]
	target_id = settlement.get("id", f"device.{slug(settlement['label'])}")
	pending = [conflict for conflict in result["conflicts"] if conflict["id"] == settlement["conflict_id"]]
	if pending:
		# Unsettled: the conflict must sit on this binding and the device must still be the imported one.
		if [conflict["path"] for conflict in pending] != [f"binding:{group}/{number}/None"]:
			raise RuntimeError(f"{settlement['path']}: {settlement['conflict_id']} is not on {group}/{number}")
		expected = (settlement["from"]["id"], settlement["from"]["label"])
	else:
		expected = (target_id, settlement["label"])
	if (device["id"], device["label"]) != expected:
		raise RuntimeError(f"{settlement['path']}: the device at {group}/{number} is {device['id']} ({device['label']!r}), expected {expected}")
	namespace = "pinmame.coil" if group == "pinmame.output.solenoid" else "pinmame.switch"
	numbers = {alias["value"] for alias in device.get("aliases", []) if alias["namespace"] == namespace}
	if numbers != {str(number)}:
		raise RuntimeError(f"{settlement['path']}: the device at {group}/{number} carries {namespace} aliases {sorted(numbers)}")
	device["id"] = target_id
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
	record = {
		"id": source["id"],
		"kind": "runtime_scenario",
		"uri": source["uri"],
		"revision": RUNTIME_PINMAME_REVISION,
		"locator": source["locator"],
		"license": "NOASSERTION",
		"attribution": ATTRIBUTION,
	}
	# Replace in place, so that settlements sharing one run leave the source list stable on re-application.
	positions = [index for index, item in enumerate(result["sources"]) if item["id"] == source["id"]]
	if positions:
		result["sources"][positions[0]] = record
	else:
		result["sources"].append(record)
	unresolved = [conflict for conflict in result["conflicts"] if conflict.get("status", "unresolved") == "unresolved"]
	if not unresolved:
		result["coverage"]["missing"] = [item for item in result["coverage"]["missing"] if item != "unresolved_conflicts"]
	elif "unresolved_conflicts" not in result["coverage"]["missing"]:
		raise RuntimeError(f"{settlement['path']}: {len(unresolved)} unresolved conflict(s) remain but coverage.missing omits unresolved_conflicts")
	return result


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
