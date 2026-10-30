"""Deterministic, deliberately partial Firepower II (1983) curation.

Manual = physical construction; pinned source = public transport; retained
ROM runs = observed behavior. Corpus scripts remain candidates until the exact
table is verified. No coordinate or Wild Texas compatibility is inferred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any
from zipfile import ZipFile
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.firepower-ii.1983"
BASE = "8e8b27143a0889c57efaee40df88b03480e61d7f"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SCRIPT_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
MANUAL_SHA = "c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8"
IPDB_SHA = "dd11bcff5b65c77a43594ef941a3214bb58ced2e21a38926cae59454ac886b09"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_SHA = "2f31b97fbaefa7071288850f777ac0f602b3531038293497fcddb8c4843c78e1"
ROM_MEMBERS = {
    "ic14.716": (2048, "83815154bbaf51dd789112664d772a876efee3da"),
    "ic17.532": (4096, "fb0b7f247673dae0744d4188e1a03749a2237165"),
    "ic20.716": (2048, "bcf017b01236f755cee419e398bbd8955ae3576a"),
    "ic26.716": (2048, "f15c3a149bafee6d74e359399de88fd122b93441"),
    "sound3.716": (2048, "521d4cdfb0ed8178b3594cedceae93b772a951a4"),
}
NVRAM_SHA = "3c0377666fb6e5c7d238544e121a930425849448df4bcaba8f65d7fafab82996"
MANUAL_FILE = "Williams_1983_Firepower_II_Operators_Handbook.pdf"
SESSION = Path("williams.firepower-ii.1983/session-20261029")
DEFINITION = Path("machines/partial/williams/firepower-ii-1983.json")
SEED = Path("tools/seeds/williams/firepower-ii-1983.json")
KNOWLEDGE = Path("knowledge/williams/firepower-ii-1983.md")
REPORT = Path("reports/spatial/williams/firepower-ii-1983.json")
REPORT_MD = REPORT.with_suffix(".md")
RUNTIME = Path("evidence/runtime/system-7/firepower-ii-1983.json")
RUNTIME_SHA = "3c1edc9f83e65ac11f8aa7b2a7fa33d834dc56967a484ea9f9cad475651025b2"
TILT = Path("evidence/runtime/system-7/firepower-ii-tilt.json")
RETAINED = Path("evidence/excerpts/williams.firepower-ii.1983/retained-inputs.md")
TILT_SHA = "41fbbffd3929baafd6c7b345a6ec80aa2565a162e59777b9f20e8f188c4ee0dc"
RETAINED_SHA = "9c46e2b6031c7a042f865d5fe6e19c97abb5371679d9e1aaef07e84e9bb98c0f"
VBS_FILES = {"core.vbs": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69",
             "s7.vbs": "88e6f2500f75315b9f5ad01581d9f24a926ad12af43730af01d8bfab8e5cfe03"}
CONVERSION_ID = "unknown-manufacturer.wild-texas"
CONVERSION = Path("machines/partial/unknown-manufacturer/wild-texas-unknown.json")
CONVERSION_SEED = Path("tools/seeds/unknown-manufacturer/wild-texas-unknown.json")
CONVERSION_KNOWLEDGE = Path("knowledge/unknown-manufacturer/wild-texas-unknown.md")
INSERT = "manual.firepower-ii-insert-board"
TILT_RUN = "runtime.firepower-ii-tilt"
MANUAL = "manual.firepower-ii"
SOURCE = "pinmame.firepower-ii"
CORE = "pinmame.system-7-current"
SCRIPT = "vpx.firepower-ii-1-1"
OLD_SCRIPT = "vpx.firepower2v1-1"
RUN = "runtime.firepower-ii"

EXCERPTS = {
    "construction-and-operation.md": "0efb9a032195aac1c542c8189832e61d8e03b6f8e306da77d9b149b9568bdec3",
    "cpu-board.md": "45a0ede82cc09953a37412d639d7033b0595e1538ec7e9d029ac71d1725fb221",
    "gi-relay-wiring.md": "a69337a5fb093980c255e23f0e082ec5f4c79bbf32aa002f4574c248e5b9d594",
    "identity-and-wild-texas.md": "9ff2b2d2922ab28162e1b09f34b686df763ba039b9d3ec88b10845efa16fe389",
    "insert-board.md": "257027bdc1fb3d5c425e19108c79e86c5780fba5f22685d725fd8e9273310a02",
    "lamp-matrix.md": "56947d7dfa43261b5082619a32a673c3785c0bcaf4f81d71de1cc7d4182fbbdd",
    "lamp-wiring.md": "e571ee1f10f4544ad427317082423fb42cfbe71acf5b58225de80f6ca60c8f10",
    "physical-photos.md": "cd4a7e33bd032fc9a1408dc337c735428b4f7e10935b21f55cc7d04328683601",
    "script-bindings.md": "97a55276174339ba23edd23b981b4b70f9f40bff295ddba164c3b2c53bc23701",
    "solenoid-connections.md": "c6628f054ab499010617c5f6e23a43e484b8f7915314a73e0f3618a134e7a183",
    "sound-dips.md": "ddbdfc5aa00ec90b580890652c6235b15093e1af5693bc44396b154467b87c18",
    "special-solenoid-wiring.md": "2a546f0befed8c0f670df346b32ebdc22653e6cdc29d0adc4fafd3525ad7eb8e",
    "switch-matrix.md": "39ebd0cc81571a2aaa6da999f865db65943c7b300aaed69a43d20c45cddd5ff9"
}
IMAGES = {
    "cpu-board.md": ("cpu-led-logic.webp", "e3bd9aa6763ccda9af0bae8466ee0349b32dce8746a6df080d4d66f4e3088124", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 25, crop box 0.37,0.44,0.82,0.71, scanned page rendered at its native resolution (embedded image xref 259, 3400px across 8.50in), rendered at 400 dpi, grayscale, 1530x1166 WebP quality 65"),
    "insert-board.md": ("insert-board.webp", "c48ff582fbd9c51eef0ddc5d6b37aaa3782b780be1b29100f225c08585284be3", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 41, crop box 0.25,0.045,0.61,0.38, scanned page rendered at its native resolution (embedded image xref 181, 3400px across 8.50in), rendered at 400 dpi, grayscale, rotated 270 degrees counter-clockwise, 1387x863 WebP quality 65"),
    "sound-dips.md": ("sound-dips.webp", "f8ef8751f0f9a196fae35c52567781e541b4343bb6b57bfe8dc035a6519d66e4", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 38, crop box 0.17,0.62,0.49,0.68, scanned page rendered at its native resolution (embedded image xref 298, 1680px across 8.39in), rendered at 200 dpi, grayscale, 539x131 WebP quality 80"),
    "lamp-wiring.md": ("lamp-wiring.webp", "9885c52351094e04dd3adea528864c18211a55617754e62c7efa067f7dd93a7c", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 51, crop box 0.215,0.55,0.655,0.825, scanned page rendered at its native resolution (embedded image xref 129, 3400px across 8.50in), rendered at 400 dpi, grayscale, 1496x1188 WebP quality 65"),
    "construction-and-operation.md": ("solenoid-locations.webp", "9732bc60c8d66d48498c271798380d1c7061a0d7e122e24041bda6ec2e294904", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 15, crop box 0.055,0.07,0.452,0.325, scanned page rendered at its native resolution (embedded image xref 70, 3304px across 8.25in), rendered at 400 dpi, grayscale, 1313x1103 WebP quality 65"),
    "special-solenoid-wiring.md": ("special-solenoid-wiring.webp", "b0f708ecda552f561c9d0e418b262445eb700f787001f5c3cf83e4d1c36613a3", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 52, crop box 0.375,0.435,0.91,0.63, scanned page rendered at its native resolution (embedded image xref 124, 3400px across 8.50in), rendered at 400 dpi, grayscale, 1819x843 WebP quality 80"),
    "gi-relay-wiring.md": ("gi-relay-wiring.webp", "fe8a13e5006953e69c1a7464679921cd3e0057d2ad53090603d8577421b45e41", "Williams_1983_Firepower_II_Operators_Handbook.pdf page 35, crop box 0.025,0.443,0.41,0.675, scanned page rendered at its native resolution (embedded image xref 207, 3400px across 8.50in), rendered at 400 dpi, grayscale, 1309x1002 WebP quality 80"),
}
LOCATORS = {
    "cpu-board.md": "PDF 22-25 / printed26-27, complete CPU BOM table and assembly/PA4-7 diagnostic LED topology",
    "insert-board.md": "PDF 41 insert-board branches9B1-9B6 and connector9P1; comparison with PDF 13/14/50/51",
    "sound-dips.md": "PDF 36 sound-board assembly DS1; PDF 38 sound-board logic, two grounded DS1 contacts",
    "lamp-matrix.md": "PDF p13 / printed 17, Figure 1, complete 8x8 matrix and wiring headers",
    "switch-matrix.md": "PDF p18 / printed 22, Figure 3, complete 8x8 matrix and wiring headers",
    "solenoid-connections.md": "PDF p16 / printed 20, Table 4, all columns, footnotes and Switch Test",
    "construction-and-operation.md": "PDF pp7,14,15 / printed 10,18,19, operation and complete lamp/solenoid location legends; drawing crop is rear of Figure 5 on p15",
    "special-solenoid-wiring.md": "PDF pp52-53, solenoid wiring spread; crop from driver/connector block on p52",
    "gi-relay-wiring.md": "PDF p35, Power Wiring Diagram relay K1, plus pp48-50 GI branch topology",
    "script-bindings.md": "corpus script callbacks, ball stacks, lamp bindings and defective handlers",
    "identity-and-wild-texas.md": "IPDB machine pages 857/5500 and Pinside topic 335329, repairer's physical hardware reports",
    "lamp-wiring.md": "PDF pp50-51 / printed 42, complete drawn cell classifications and GI connector branches; crop from p51",
    "physical-photos.md": "IPDB 857 photos 50035,50038,50042,50054,50056; original retained JPEGs, visual inspection",
}
PHOTOS = [
    (50035, "upper-playfield", "image-34.jpg", "7da3dee34eed2b9362a6f1a13267980217365f4b33f2bfb38bde57d4235eeee6", "2026-10-30T00:03:04.098566+00:00"),
    (50038, "lower-playfield", "image-21.jpg", "553907473bc7acf4bccc68b5fc11a4aa6ade65bf35a515d3f89d94f070fb72c9", "2026-10-30T00:03:06.767612+00:00"),
    (50042, "upper-lock", "image-33.jpg", "22907bbcd9e90b4bd82c4001c15c421dc3a35ac0523245c218f3e4f9920d778a", "2026-10-30T00:03:12.520395+00:00"),
    (50056, "inside-backbox", "image-6.jpg", "28adfc5d7fb28b4cce0c4c37fb7d54163877000d11d078ccd29da5dedd69b352", "2026-10-30T07:36:19.702475+00:00"),
    (50054, "behind-backglass", "image-8.jpg", "178910f1297b86fd39f328fcb8ee4a9760fb34088fd919e413fc90aafd9716b7", "2026-10-30T00:03:17.694976+00:00"),
]
SCRIPT_FILES = {
    "FirePower II (Williams 1983) 1.1.vbs": "8a310e2e3773312d2f78c4370a1bd032c2aa194c6d3db175f56e252230c4d4f6",
    "Firepower2v1.1.vbs": "a348a21d346f3f4be38c682a03fe677a8b7b598042dc0a24720c02e6b3765918",
}
SOURCE_FILES = {
    "LICENSE": "21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e",
    "src/wpc/core.c": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
    "src/wpc/core.h": "b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0",
    "src/wpc/s7.h": "00849d86671f0cfc3e2ce3bed12a2e2023c5df0dc81ee50123433514d70379ae",
    "src/wpc/wmssnd.c": "5d9d431416150e22fddf850b59e377d7f923fa7bda067e830729891670eff82f",
    "src/wpc/s7games.c": "cc9cf65dc56416331b537f4595b8f6ce6415e018d2bcf502a74d3b974377e6d7",
    "src/wpc/s7.c": "908c575b40483e47fe0296943b69f74506c10081d3fea8ee361611ef7f6a9f85",
}

SWITCH_LABELS = (
    "Plumb Tilt|Ball Roll Tilt|Credit Button|Right Coin|Center Coin|Left Coin|Slam Tilt|High Score Reset|"
    "Outhole|Right Ball Ramp|Left Ball Ramp|Ball Shooter Trough|Lane Change|Ramp in Roll Under|Ramp out Roll Under|Center Left Standup|"
    "Standup|Spinner|Orbit in Roll Under|Upper Left Standup|Not Used|Upper Right Standup|Eject Hole|Release Target|"
    "F Target|I Target|R Target|E Target (first)|P Target|O Target|W Target|E Target (second)|R Target (last)|"
    "A Rollover|B Rollover|C Rollover|D Rollover|Left Outlane|Right Outlane|Orbit Out Gate|"
    "Lower Left Jet Bumper|Upper Right Jet Bumper|Upper Left Jet Bumper|Lower Right Jet Bumper|"
    "Left Flipper Return Lane|Right Flipper Return Lane|Left Kicker|Right Kicker|Playfield Tilt"
).split("|")
LAMP_LABELS = (
    "Game Over|Match|Tilt|High Score|Shoot Again (backbox)|Shoot Again (playfield)|Double Score|Bonus Holdover (orbit)|"
    "1,000 Bonus|2,000 Bonus|3,000 Bonus|4,000 Bonus|5,000 Bonus|6,000 Bonus|7,000 Bonus|8,000 Bonus|9,000 Bonus|"
    "10,000 Bonus|20,000 Bonus|40,000 Bonus|60,000 Bonus|80,000 Bonus|Bonus Holdover (bonus)|Fire Power Special|"
    "F|I|R (first)|E (first)|P|O|W|E (second)|R (last)|A|B|C|D|Left Drain Special|Right Drain Special|Ball in Play|"
    "Lower Left Jet Bumper|Upper Right Jet Bumper|Upper Left Jet Bumper|Lower Right Jet Bumper|Left Flipper Return Lane|"
    "Right Flipper Return Lane|Mystery|Extra Ball|2x|3x|5x|Eject Hole 10K|Eject Hole 20K|Eject Hole 50K|Eject Hole Lock Arrow|"
    "Release Target 50K|Release Target 100K|Release Target 150K|Release Arrow|Spinner"
).split("|")
# Table 4 literal values, including apparent misprints. No sibling table supplied these.
SOLENOIDS = {
    1: ("Outhole", "coil", "GRY-BRN", "2P11-4, 8P3-1", "Q15", "SG1-23-850-DC"),
    2: ("Ball Ramp Thrower", "coil", "GRY-RED", "2P11-5, 8P3-2", "Q17", "SA3-23-850-DC"),
    3: ("Eject Hole", "coil", "GRY-ORN", "2P11-7, 8P3-3", "Q19", "SG1-23-850-DC"),
    4: ("Orbit Complete Flash Lamps", "flasher", "GRY-YEL", "2P11-8, 8P3-4", "Q21", "Type 83"),
    11: ("General Illumination Relay", "relay", "BRN-ORN", "2P9-1, 3P7-1", "Q35", "5580-09555"),
    15: ("Bell", "coil", "BRN-VIO", "2P9-5, 7P1-17", "Q43", "SM-29-1000-DC"),
    16: ("Coin Lockout", "coil", "BRN-GRY", "2P9-6, 7P1-18, 7P2-4", "Q45", "904218-696"),
    17: ("Left Kicker", "coil", "BLU-BRN", "2P12-7, 8P3-17", "Q2", "SG1-23-850-DC"),
    18: ("Right Kicker", "coil", "BLU-RED", "2P12-4, 8P3-18", "Q4", "SG1-23-850-DC"),
    19: ("Lower Left Jet Bumper", "coil", "BLU-ORN", "2P12-4, 8P3-19", "Q6", "SG1-23-850-DC"),
    20: ("Upper Right Jet Bumper", "coil", "BLU-YEL", "2P12-6, 8P3-20", "Q8", "SG1-23-850-DC"),
    21: ("Upper Left Jet Bumper", "coil", "BLU-GRN", "2P12-8, 8P3-12", "Q10", "SG1-23-850-DC"),
    22: ("Lower Right Jet Bumper", "coil", "BLU-BLK", "2P12-9, 8P3-22", "Q12", "SG1-23-850-DC"),
}
SPECIAL_SWITCHES = {17: 47, 18: 48, 19: 41, 20: 42, 21: 43, 22: 44}
UNUSED_SOLENOIDS = {
    5: ("GRY-GRN", "2P11-9, 8P3-5", "Q23"), 6: ("GRY-BLU", "2P11-3, 8P3-6", "Q25"),
    7: ("GRY-VIO", "2P11-2, 8P3-7", "Q27"), 8: ("GRY-BLK", "2P11-1, 8P3-8", "Q29"),
    9: ("BRN-BLK", "2P9-9, 8P3-9", "Q31"), 10: ("BRN-RED", "2P9-7, 8P3-10", "Q33"),
    12: ("BRN-YEL", "2P9-2, 8P3-12", "Q37"), 13: ("BRN-GRN", "2P9-3, 8P3-13", "Q39"),
    14: ("BRN-BLU", "2P9-4, 8P3-14", "Q41"),
}
MISSING = ["output_enumeration", "output_semantics", "spatial_placement", "unresolved_conflicts"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retained_inputs(root: Path = ROOT) -> dict[str, Any]:
    text = (root / RETAINED).read_text(encoding="utf-8")
    return json.loads(text.split("```json\n", 1)[1].rsplit("\n```", 1)[0])


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def na(reason: str, *refs: str) -> dict[str, Any]:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def base(identifier: str, label: str, kind: str, group: str, address: int,
         *refs: str, availability: str = "used") -> dict[str, Any]:
    namespace = group.replace(".input", "").replace(".output", "")
    values = [str(address)]
    if group == "pinmame.input.switch" and address > 0:
        values = list(dict.fromkeys([str(address), f"{address:02d}", f"{address:03d}"]))
    return {"id": identifier, "label": label, "kind": kind,
            "binding": {"group": group, "device": address}, "availability": availability,
            "aliases": [{"namespace": namespace, "value": value} for value in values],
            "provenance": provenance(*refs)}


def switch_id(address: int) -> str:
    label = SWITCH_LABELS[address - 1] if address <= len(SWITCH_LABELS) else "Not Used"
    return f"switch.{slug(label)}" if label != "Not Used" else f"switch.unused-{address}"


def solenoid_id(address: int) -> str:
    if address == 25:
        return "relay.game-on-flipper-enable"
    if address in SOLENOIDS:
        label, kind, *_ = SOLENOIDS[address]
        return f"{kind}.{slug(label)}"
    return f"virtual.unused-solenoid-{address}"


def matrix_wiring(address: int, lamp: bool = False) -> dict[str, str]:
    col, row = divmod(address - 1, 8)
    if lamp:
        cw = ["BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY"]
        cp = [8, 9, 6, 7, 3, 5, 1, 2]
        rw = ["BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
        rp = [1, 2, 3, 4, 5, 6, 9, 8]
        dc, rc = "2J5", "2J7"
    else:
        cw = ["BRN", "RED", "ORN", "YEL", "BLK", "BLU", "VIO", "GRY"]
        cp = [9, 8, 7, 6, 5, 3, 2, 1]
        rw = ["BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"]
        rp = [9, 8, 7, 6, 5, 4, 3, 1]
        dc, rc = "2J2", "2J3"
    return {"board": "Williams System 7 driver board", "drive_wire": f"{'YEL' if lamp else 'GRN'}-{cw[col]}",
            "drive_connection": f"{dc}-{cp[col]}", "return_wire": f"{'RED' if lamp else 'WHT'}-{rw[row]}",
            "return_connection": f"{rc}-{rp[row]}"}


def inputs() -> list[dict[str, Any]]:
    devices = []
    services = {-7: "Advance", -6: "Auto-Up Manual-Down", -5: "CPU Diagnostic", -4: "Sound Diagnostic", -3: "Master Command Enter"}
    for address, label in services.items():
        d = base(f"switch.{slug(label)}", label, "switch", "pinmame.input.switch", address, CORE, MANUAL)
        d["normally_closed"] = False
        d.update(roles=["service"], spatial=na("cabinet_or_service", CORE),
                 physical={"location": "cabinet or backbox service control", "switch_type": "other" if address == -6 else "button",
                           "notes": "Auto-Up is public -6 = 1; Master Command Enter gates the CPU DIP read. These are not playfield switches."})
        if address == -3:
            d.pop("normally_closed")
            d.update(id="virtual.master-command-enter", kind="virtual", availability="optional", spatial=na("virtual", CORE, MANUAL),
                     physical={"location": "emulator configuration only", "notes": "Generic Master Command Enter gates s7_dips_r. No fitted model 521 Enter button appears in CPU assembly/logic or cabinet wiring; production adjustments use Advance/Auto-Up. It accompanies the optional virtual F/D banks, not a physical playfield or service button."})
        devices.append(d)
    for address in range(1, 65):
        label = SWITCH_LABELS[address - 1] if address <= 49 else "Not Used"
        used = label != "Not Used"
        d = base(switch_id(address), label if used else f"Not Used matrix switch {address}", "switch",
                 "pinmame.input.switch", address, MANUAL, CORE, availability="used" if used else "unused")
        d["wiring"] = matrix_wiring(address)
        d["aliases"].append({"namespace": "manual.address", "value": str(address)})
        if not used:
            d["spatial"] = na("unused", MANUAL)
            d["physical"] = {"notes": "Printed Not Used in the complete matrix. A ROM test scanning an unfitted cell does not fit a contact. Script writes to 57/58 do not change this."}
        elif address == 13:
            d.update(kind="virtual", spatial=na("virtual", SOURCE, CORE),
                     physical={"notes": "Lane Change is the matrix copy of the right cabinet button, not a separately driven playfield input. INITGAMEFULL uses FLIP_SWNO(0,13); core_updateSw overwrites direct writes to 13 from synthetic button 82 on every update. The ROM's Test 03 reports 13 when 82 is held."})
        else:
            cabinet = address <= 8
            d["normally_closed"] = False
            d["physical"] = {"location": "cabinet" if cabinet else "playfield",
                             "switch_type": "tilt" if address in {1, 2, 7, 49} else "button" if cabinet else "leaf",
                             "notes": "Normally open matrix contact: s7.c pia4a_r returns core_getSwCol without inversion, fpwr2 has no inversion mask, and Test 03 recognizes a public closure at 1. Ball occupancy is not contact normal state."}
            if cabinet:
                d.update(roles=["cabinet"], spatial=na("cabinet_or_service", MANUAL))
            if address in {9, 10, 11, 12, 23}:
                d["physical"]["notes"] += " Hold while a ball rests here, release when it leaves; initial occupancy belongs to the table's two-ball model."
            if address in {41, 42, 43, 44, 47, 48}:
                d["physical"]["notes"] += " This scoring contact also supplies PinMAME's special-coil synthesis; the hardware has a separate direct-power contact."
            if address in {1,7,49}:
                d["provenance"] = provenance(MANUAL, CORE, TILT_RUN)
                d["physical"]["notes"] += {1: " Initialized L-2: two GI warnings, third closure tilts.",
                                            7: " Initialized L-2: first closure aborts play into attract. Newer corpus TiltSwitch=7 is a recreation defect: mechanical/plumb tilt must use1, not this slam input.",
                                            49: " Initialized L-2: first closure tilts immediately."}[address]
        devices.append(d)
    for address in range(81, 89):
        used = address in {82, 84}
        side = "right" if address == 82 else "left"
        label = f"{side.title()} Flipper Button" if used else f"Unused flipper-column position {address}"
        d = base(f"switch.{side}-flipper-button" if used else f"virtual.flipper-column-{address}", label,
                 "virtual", "pinmame.input.switch", address, CORE, SOURCE, availability="used" if used else "unused")
        d.update(spatial=na("virtual", CORE), physical={"notes": (
            f"Synthetic cabinet-button input. {'Also copied into matrix 13 for lane change. ' if address == 82 else ''}"
            f"While game-on 25 is set it fabricates outputs {'45/46' if address == 82 else '47/48'}. The physical flipper is cabinet-switched through relay Z1; these outputs measure neither winding current nor EOS timing."
            if used else "The selected driver's read path selects only eight matrix columns; this generic column bit is outside its flipper mask and is never copied into a ROM-readable column.")})
        devices.append(d)
    for address in [1, 2, *range(9, 25)]:
        label = f"Sound DIP {address}" if address <= 2 else f"Master Command {'F' if address <= 16 else 'D'}{address-8 if address <= 16 else address-16}"
        d = base(f"dip.{slug(label)}" if address <= 2 else f"virtual.{slug(label)}", label, "dip_switch" if address <= 2 else "virtual", "pinmame.input.dip", address, CORE, MANUAL,
                 availability="used" if address <= 2 else "optional")
        d.update(spatial=na("dip_switch", CORE), physical={"location": "backbox sound board" if address <= 2 else "backbox CPU board",
                 "switch_type": "dip" if address <= 2 else "other", "notes": (
                     "Fitted sound-board DIP. Public bank0 bits0/1 enter s67s_cmd_w."
                     if address <= 2 else
                     "Generic emulated Master Command data entry, not a fitted model 521 CPU DIP. BOM item 24 and the assembly view are parts of one drawing: the item lists DS1/DS2, but the assembly has no such footprints. Logic PDF 24-25 connects PA4-7 to diagnostic LED decoder IC34. Production photo 50056 independently shows the display and resistor packs without visible DS1/DS2 banks. Full contradictory BOM retained. s7_dips_r returns inverted F/D bank nibbles only while Enter(-3) is held; optional emulator entry is separate from software adjustment numbers.")})
        if address > 2:
            d["physical"]["location"] = "emulator configuration only"
            d["provenance"] = provenance(CORE, MANUAL, "photo.firepower-ii-50056")
        else:
            d["normally_closed"] = False
        devices.append(d)
    return devices


def outputs() -> list[dict[str, Any]]:
    devices = []
    for address in range(1, 97):
        used = address <= 60
        label = LAMP_LABELS[address - 1] if used else f"Not Used lamp {address}"
        d = base(f"lamp.{slug(label)}" if used else f"lamp.unused-{address}", label, "lamp", "pinmame.output.lamp",
                 address, MANUAL if address <= 64 else SOURCE, CORE, availability="used" if used else "unused")
        if address <= 64:
            d["wiring"] = matrix_wiring(address, True)
            d["aliases"].append({"namespace": "manual.address", "value": str(address)})
        if address == 40:
            d.update(roles=["backbox"], availability="unknown", spatial=na("cabinet_or_service", MANUAL, INSERT),
                     provenance=provenance(MANUAL, INSERT, RUN, status="conflicted"),
                     physical={"location": "backbox candidate", "notes": "Meaningful Ball in Play bit observed on Start/tilt. Fitment/routing remains conflicted: PDF 51 says 40 NOT USED, Figure 1/2 call 40 Ball in Play, and insert-board PDF 41 draws 9B6 BALL IN PLAY on column 1/row 6 (public 6). Photo 50054 shows sockets without readable routing; 50030 footer cannot identify the circuit. Runtime transitions cannot prove a bulb absent or fitted. Do not reduce this to a virtual-only lamp."})
        elif not used:
            d["spatial"] = na("unused", MANUAL if address <= 64 else SOURCE)
            d["physical"] = {"notes": "61-64 are printed Not Used. 65-96 are platform auxiliary lamp columns, absent from this game's hw.lampCol=0. A lamp-test sweep does not establish physical fitment."}
        elif address <= 5:
            d.update(roles=["backbox"], spatial=na("cabinet_or_service", MANUAL),
                     physical={"location": "backbox", "notes": "Figure 2 explicitly braces lamps 1-5 as Backbox Lamps."})
        else:
            d["physical"] = {"location": "playfield",
                             "notes": "Named and wired in Figure 1. Bulb count and exact center need geometry/physical-image review; render doubles do not prove additional bulbs."}
            if address in {6, 45, 46, 47, 48}:
                d["physical"]["notes"] += " Wiring template prints BACKBOX here, but game-specific Figure 2 and the retained lower-playfield photograph place this insert on the playfield."
                d["provenance"] = provenance(MANUAL, "photo.firepower-ii-50038")
            if address == 6:
                d["provenance"] = provenance(MANUAL, INSERT, "photo.firepower-ii-50038", status="conflicted")
                d["physical"]["notes"] += " PDF 41 also draws backbox 9B6 BALL IN PLAY on this column 1/row 6 circuit. Playfield Shoot Again fitment is supported by the photo, but its possible shared backbox load is unresolved; see lamp 6/40 conflict."
        devices.append(d)
    for address in [*range(1, 26), *range(45, 49), *range(51, 61)]:
        if address in SOLENOIDS:
            label, kind, wire, connection, transistor, part = SOLENOIDS[address]
            d = base(solenoid_id(address), label, kind, "pinmame.output.solenoid", address, MANUAL, SOURCE, RUN)
            d["wiring"] = {"board": "Williams System 7 driver board", "drive_wire": wire,
                           "drive_connection": connection, "driver_transistor": transistor}
            d["physical"] = {"part_number": part, "location": "cabinet" if address in {11, 15, 16} else "playfield",
                             "notes": "Table 4 literal wiring; printed number equals the public address in the retained Test 02 run."}
            if address in {11, 15, 16}:
                d.update(roles=["cabinet"], spatial=na("cabinet_or_service", MANUAL))
            if address == 4:
                d["physical"]["notes"] += " Flash lamps, not a coil. Type 83 is the bulb type; the plural label and callout do not establish exact socket quantity."
                d["physical"]["notes"] += " PDF 52-53 repeats designation 8L2 for both thrower 2 and flash group 4; pins distinguish them."
            if address == 11:
                d["physical"]["notes"] += " Normally-closed power-board K1 opens the common 6.3 VAC leg for all four fused GI branches when energized. Wire/pin discrepancies in PDF 35/41/48/50 are retained in gi-relay-wiring.md. The controlled sockets are still uncounted. System 7 publishes no separate GI channel."
            if address == 16:
                d["physical"]["notes"] += " Cabinet drawing shows two parallel coin-lockout loads 7L16A/B. De-energized means reject coins (operation page)."
                d["physical"]["quantity"] = 2
            if address in {19, 21, 22}:
                d["physical"]["notes"] += " Wiring drawing disagrees: 19 uses 2P12-3; 21 uses BLU-BLK and 8P3-21; 22 uses BLU-GRN. Table values are retained pending an independent wiring check; device and public identity agree."
            if address in SPECIAL_SWITCHES:
                d["physical"]["notes"] += f" Scoring matrix {SPECIAL_SWITCHES[address]} supplies this slot in PinMAME; the separate direct-power contact is not a public 65-70 input."
        elif address == 25:
            d = base(solenoid_id(address), "Game On / Flipper Enable", "relay", "pinmame.output.solenoid", address, CORE, MANUAL, RUN)
            d.update(roles=["internal"], spatial=na("internal_nonvisual", CORE, MANUAL),
                     physical={"location": "driver board in backbox", "notes": "S7_GAMEONSOL is PIA1 CB2 enable, not solenoid 23. It drives relay Z1 and enables special coils. Test 02 step 25 toggles it; tilt drops it."})
        elif 45 <= address <= 48:
            side = "right" if address <= 46 else "left"
            winding = "power" if address % 2 else "hold"
            d = base(f"virtual.{side}-flipper-{winding}", f"Synthetic {side} flipper {winding} state", "virtual",
                     "pinmame.output.solenoid", address, CORE, SOURCE, RUN)
            d.update(spatial=na("virtual", CORE), physical={"notes": f"Used virtual callback; follows button {82 if side == 'right' else 84} while enabled. Both states of the pair assert together, with no winding or EOS model. Physical {side} coil is SFL-19-400/30-750-DC, cabinet-switched; do not treat these as two physical coils."})
        else:
            d = base(solenoid_id(address), f"Unfitted/reserved solenoid {address}", "virtual", "pinmame.output.solenoid",
                     address, SOURCE, CORE, MANUAL, availability="unused")
            d["spatial"] = na("unused", CORE, MANUAL)
            d["physical"] = {"notes": "Table 4 says Not Used for 5-10/12-14. Test 02 still sweeps them. 23/24 are PIA special slots with no fitted driver in the six-circuit board drawing; the ROM sweeps them too. 51-60 are unavailable because this game declares no custom-solenoid callback. Non-observation is not the basis of these dispositions."}
            if address in UNUSED_SOLENOIDS:
                wire, connection, transistor = UNUSED_SOLENOIDS[address]
                d["wiring"] = {"drive_wire": wire, "drive_connection": connection, "driver_transistor": transistor}
        devices.append(d)
    return devices


def mechanisms() -> list[dict[str, Any]]:
    specs = [
        ("ball-storage-serve", "Two-ball storage, outhole and shooter", "kicker", [solenoid_id(1), solenoid_id(2)], [switch_id(n) for n in [9, 10, 11, 12]],
         "Two balls rest in the ball-ramp storage path on switches 10/11. Drain detection 9 prompts outhole 1 to return the ball; thrower 2 serves toward shooter trough 12, then a manual plunger launches it. The harness starts with 10/11 occupied and observes 2 on Start, and repeated 1 while 9 is held. Host ball moves are separate from coil causality. Exact storage geometry and retry timings remain unmeasured."),
        ("eject-lock", "Eject-hole lock and release", "kicker", [solenoid_id(3)], [switch_id(23), switch_id(24)],
         "Saucer 23 retains the first ball for multiball while thrower 2 supplies the other. Release target 24 commands eject coil 3 and begins two-ball play. During multiball saucer entries score and eject immediately. The retained gameplay trace observes 2 with 23 held and 3 for 24 before host release of 23. A coil does not directly actuate its ball-presence switch; a ball moving after the kick changes it."),
        ("orbit", "Spinner and orbit gates", "gate", [], [switch_id(n) for n in [18, 19, 40]],
         "Passive orbit entry spinner/rollunder and exit gate. Spinner-lane entry followed by exit gate completes orbit and triggers flash output 4. FIREPOWER groups light jets and the timed bonus-holdover opportunity. These are passive gates with no invented gate actuator; script gate animation is visual behavior."),
        ("ramp", "Passive cross-playfield ramp", "other", [], [switch_id(14), switch_id(15)],
         "Rollunder contacts mark ramp entrance and exit. Completed ramp scores its lit value, mystery or extra ball. There is no moving ramp coil in Table 4. Do not confuse this shot ramp with the ball-storage ramp served by output 2."),
        ("targets-and-lanes", "FIREPOWER standup targets and A-B-C-D lanes", "other", [], [switch_id(n) for n in [*range(25, 38), 16, 17, 20, 22]],
         "FIREPOWER uses standup targets, not resettable drop targets. Letter groups and A-B-C-D lane completion control awards. Standalone16/17 score100; upper rebound contacts20/22 score50. No reset coil is fitted. The manual enumerates these contacts; the secondary feature count uses different categories and does not remove documented assemblies."),
        ("orbit-ball-preventer", "Passive orbit ball-preventer wire", "gate", [], [],
         "Retained original-machine photograph 60457 shows the passive wire preventing a ball lodging in the upper orbit area. No actuator or public sensor is assigned; it belongs to physical table geometry."),
        ("gi", "Relay-switched general illumination", "other", [solenoid_id(11)], [],
         "Normally-closed K1 opens the common 6.3 VAC leg feeding four separately fused GI branches: two playfield groups (one also cabinet) and two insert-board groups. Active 11 extinguishes GI. These are real bulbs behind relay contacts, not a GI callback channel. Individual stock sockets and quantities remain unknown; the relay's common contact grouping is established by PDF 35."),
    ]
    for address, sensor in SPECIAL_SWITCHES.items():
        label = SOLENOIDS[address][0]
        specs.append((slug(label), label, "kicker", [solenoid_id(address)], [switch_id(sensor)],
                      f"{label}: scoring matrix contact {sensor} and separate direct-power contact at the same assembly. In PinMAME, enabled closure {sensor} publishes special slot {address}; Test 02 independently pairs printed and public number. Hardware response is direct-power through the game-on enable; pulse length and mechanical tuning remain table-owned."))
    for side, button, pair in [("right", 82, [45, 46]), ("left", 84, [47, 48])]:
        specs.append((f"{side}-flipper", f"{side.title()} flipper", "other", [f"virtual.{side}-flipper-{w}" for w in ["power", "hold"]], [f"switch.{side}-flipper-button"],
                      f"One physical {side} flipper, dual-wound SFL-19-400/30-750-DC with a local EOS contact, cabinet-switched through Z1. Consumer drives synthetic button {button}; outputs {pair} are fabricated together and do not simulate EOS. The right cabinet button also drives lane-change matrix copy13. Travel, EOS opening angle and mechanical tuning belong to the table's geometry."))
    return [{"id": f"mech.{key}", "label": label, "kind": kind, "actuators": actuators,
             "sensors": sensors, "behavior": behavior, "provenance": provenance("photo.firepower-ii-60457") if key == "orbit-ball-preventer" else provenance(MANUAL, CORE, SOURCE, RUN)}
            for key, label, kind, actuators, sensors, behavior in specs]


def excerpt(name: str) -> dict[str, Any]:
    e = {"id": f"excerpt.{slug(name.removesuffix('.md'))}", "locator": LOCATORS[name],
         "path": f"evidence/excerpts/{MACHINE_ID}/{name}", "sha256": EXCERPTS[name],
         "method": "manual", "transcribed_by": "curator; native raster visual check (script excerpt: source-text inspection)",
         "reviewed": name not in {"script-bindings.md", "identity-and-wild-texas.md"}}
    if name in IMAGES:
        image, digest, derivation = IMAGES[name]
        e.update(image=f"evidence/excerpts/{MACHINE_ID}/{image}", image_sha256=digest, image_derivation=derivation)
    return e


def sources(root: Path) -> list[dict[str, Any]]:
    common = {"license": "BSD-3-Clause", "attribution": "PinMAME contributors", "revision": REVISION}
    records = [
        {"id": SOURCE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s7games.c", "sha256": SOURCE_FILES["src/wpc/s7games.c"],
         "locator": "s7_dispS7; INITGAMEFULL macro and fpwr2/wldtexas blocks. Identical routing does not prove Wild Texas physical compatibility.", **common},
        {"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/s7.c", "sha256": SOURCE_FILES["src/wpc/s7.c"],
         "locator": "s7_vblank, setSSSol, pia4a_r/pia4b_w, s7_dips_r, MACHINE_DRIVER_START(s7). Also core.c core_updateSw/core_getSol/core_swSeq2m and core.h FLIP_SWNO/CORE_FLIPPERSWCOL, s7.h S7_COMPORTS and wmssnd.c s67s_cmd_w at the same revision.", **common},
        {"id": MANUAL, "kind": "manual", "uri": "https://www.ipdb.org/files/857/Williams_1983_Firepower_II_Operators_Handbook.pdf", "sha256": MANUAL_SHA,
         "revision": "16-521-101 July 1983", "source_id": "ipdb:857", "original_filename": MANUAL_FILE,
         "locator": f"IPDB machine https://www.ipdb.org/machine.cgi?id=857; retained external:pinmame-manuals/by-machine/{MACHINE_ID}/{MANUAL_FILE}; 56 PDF pages, 6507312 bytes, empty original text layer. Cover visually verified as 16-521-101. Native pages and Windows OCR retained externally.",
         "acquired_at": "2026-10-29T23:57:07Z", "license": "NOASSERTION", "rights": "Copyright Williams Electronics, Inc.; IPDB-hosted scan retained externally for research. No redistribution permission asserted; repository MIT licence does not apply to the source PDF.", "attribution": "Williams Electronics, Inc.; scan hosted by the Internet Pinball Database",
         "excerpts": [excerpt(n) for n in EXCERPTS if n not in {"script-bindings.md", "identity-and-wild-texas.md", "physical-photos.md"}]},
        {"id": "ipdb.firepower-ii", "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=857", "sha256": IPDB_SHA,
         "locator": f"Identity interactively verified by parent orchestrator; retained external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-857.html. Firepower II, August 1983, model 521, System 7, two flippers and four bumpers.",
         "acquired_at": "2026-10-29T23:58:33Z", "license": "NOASSERTION", "attribution": "The Internet Pinball Database; acquisition and identity check by parent orchestrator; acquired_at is retained capture persistence time",
         "excerpts": [excerpt("identity-and-wild-texas.md")]},
        {"id": "ipdb.wild-texas", "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=5500",
         "sha256": "49b41f922729a0dc7b9a12c1359b40207eff24fe3a0b664bc4e3bc2d9f5a9c4f", "acquired_at": "2026-10-30T00:07:40Z",
         "locator": f"Parent interactive capture persisted at acquired_at; external:pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-5500-wild-texas.html. Physical conversion identity and owner-reported Gottlieb parts, not Firepower II fitment evidence.",
         "license": "NOASSERTION", "attribution": "Internet Pinball Database; physical hardware observations attributed to owner of pictured Wild Texas",
         "excerpts": [excerpt("identity-and-wild-texas.md")]},
        {"id": "pinside.wild-texas-repair", "kind": "human_review", "uri": "https://pinside.com/pinball/forum/topic/wild-texas-info-requested",
         "sha256": "7fc10f4c0132436aa942b80304682c0a5b58d4b1d8c1e650c886245186d653a7", "acquired_at": "2026-10-30T00:06:49Z",
         "locator": f"Parent interactive capture persisted at acquired_at; external:pinmame-manuals/by-machine/{MACHINE_ID}/pinside-wild-texas-owner-report.html. Theonlylilo repair report, topic 335329, first and final posts.",
         "license": "NOASSERTION", "attribution": "Pinside contributors; Theonlylilo's firsthand repair report",
         "excerpts": [excerpt("identity-and-wild-texas.md")]},
    ]
    for filename in ["src/wpc/core.c", "src/wpc/core.h", "src/wpc/s7.h", "src/wpc/wmssnd.c"]:
        records.append({"id": "pinmame.dependency." + slug(filename), "kind": "pinmame_core",
                        "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/{filename}", "sha256": SOURCE_FILES[filename],
                        "revision": REVISION, "locator": "Source read-path/flipper/sound dependency cited by pinmame.system-7-current. LICENSE SHA256 " + SOURCE_FILES["LICENSE"],
                        "license": "BSD-3-Clause" if filename.endswith("s7.h") else "LicenseRef-PinMAME-Old-MAME",
                        "attribution": "PinMAME contributors", "rights": "Pinned repository LICENSE distinguishes explicitly marked BSD files from inherited old-MAME files; no blanket BSD assertion for unmarked core/sound dependencies."})
    for number, label, image_file, digest, acquired_at in PHOTOS:
        records.append({"id": f"photo.firepower-ii-{number}", "kind": "human_review", "uri": f"https://www.ipdb.org/images/857/{image_file}",
                        "source_id": "ipdb:857", "sha256": digest, "acquired_at": acquired_at,
                        "locator": f"Machine https://www.ipdb.org/machine.cgi?id=857; photo page https://www.ipdb.org/showpic.pl?id=857&picno={number}; retained external:pinmame-manuals/by-machine/{MACHINE_ID}/photos/ipdb-{number}-{label}.jpg. Parent-acquired original photograph, primary author visual check. No coordinates measured.",
                        "license": "NOASSERTION", "rights": "Photographer retains copyright; original retained externally only, no redistribution permission asserted.",
                        "attribution": "Jonathan Selavka, photograph hosted by the Internet Pinball Database", "excerpts": [excerpt("physical-photos.md")]})
    for identifier, (filename, digest) in zip([SCRIPT, OLD_SCRIPT], SCRIPT_FILES.items()):
        records.append({"id": identifier, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/" + SCRIPT_REVISION + "/" + quote(filename, safe="/"),
                        "revision": SCRIPT_REVISION, "sha256": digest, "locator": f"{filename}; source-text comparison, no exact VPX geometry/launch verification yet",
                        "license": "NOASSERTION", "attribution": "Community table authors credited in the script; Walamab and contributors for FirePower II 1.1; Thalamus and original authors for Firepower2v1.1",
                        "known_working": False, "excerpts": [excerpt("script-bindings.md")]})
    records.append({**next(s for s in records if s["id"] == MANUAL), "id": INSERT,
                    "locator": "PDF 41 insert-board diagram versus PDF 13/14/50/51 reprints of the same manual; not independent corroboration.",
                    "excerpts": [excerpt("insert-board.md")]})
    records.append({"id": "opdb.firepower-ii", "kind": "human_review", "uri": "https://mp-data.sfo3.cdn.digitaloceanspaces.com/latest-opdb.json",
                    "sha256": "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93", "acquired_at": "2026-08-14T17:53:43Z",
                    "locator": "Retained external:pinmame-review-artifacts/opdb-import/latest-opdb.json; machines opdbId GRWYk-Mb5OV, Firepower II, Williams, IPDB 857, manufactureDate1983-01-08. Snapshot has no Wild Texas title entry; do not assign this ID to the conversion.",
                    "license": "NOASSERTION", "attribution": "Open Pinball Database contributors", "rights": "Snapshot retained externally; no original image redistribution permission asserted."})
    records.append({"id": "custody.firepower-ii", "kind": "human_review", "uri": "repo:" + RETAINED.as_posix(),
                    "sha256": RETAINED_SHA, "revision": BASE,
                    "locator": "Deterministic custody metadata for72 retained external source files and all 16 gallery previews. Fenced JSON parsed by the curator; no physical assertions arise from hashes alone.",
                    "license": "NOASSERTION", "attribution": "Source authors/photographers and parent acquisition process, individually recorded in the manifest; source-owned originals remain outside Git.",
                    "excerpts": [{"id": "excerpt.retained-inputs", "path": RETAINED.as_posix(), "sha256": RETAINED_SHA,
                                  "locator": "Complete retained-input custody manifest; filesystem hashes/sizes and acquisition metadata, no physical fitment assertions.",
                                  "method": "mixed", "transcribed_by": "Primary author filesystem hashing; parent acquisition metadata retained verbatim", "reviewed": False}]})
    retained = retained_inputs(root)
    for spec in retained["photo_acquisition"]:
        number = spec["photo_id"]
        if number in {n for n, *_ in PHOTOS}:
            continue
        records.append({"id": f"photo.firepower-ii-{number}", "kind": "human_review", "source_id": "ipdb:857",
                        "uri": spec["resource"]["url"], "sha256": spec["resource"]["sha256"], "acquired_at": spec["acquired_at"],
                        "locator": spec["page"]["url"] + "; retained source/page hashes and paths in repo:" + RETAINED.as_posix() + "; primary author visual check, no coordinates.",
                        "license": "NOASSERTION", "rights": spec["rights"], "attribution": spec["attribution"] + ", hosted by IPDB",
                        "excerpts": [excerpt("physical-photos.md")]})
    for identifier, uri, filename, attribution in [
        ("photo.firepower-ii-50030", "https://www.ipdb.org/images/857/image-16.jpg", "photos/ipdb-50030-illuminated-backglass.jpg", "Jonathan Selavka; IPDB 857 photo50030 https://www.ipdb.org/showpic.pl?id=857&picno=50030"),
        ("photo.wild-texas-42932", "https://www.ipdb.org/images/5500/image-8.jpg", "photos/ipdb-42932-wild-texas-mpu.jpg", "Tony Turner; IPDB 5500 photo42932 https://www.ipdb.org/showpic.pl?id=5500&picno=42932"),
        ("pinside.firepower-ii-gallery", "https://pinside.com/pinball/machine/firepower-ii/gallery", "pinside-firepower-ii-gallery.html", "Pinside and respective photographers;16 retained previews, individual resource URLs/hashes/acquisition times in retained-input manifest"),
        ("pinside.firepower-ii", "https://pinside.com/pinball/machine/firepower-ii", "pinside-firepower-ii.html", "Pinside contributors; June 1983 is a month disagreement with IPDB August 1983, canonical year agrees"),
        ("vpf.firepower-ii-1-1", "https://www.vpforums.org/index.php?showtopic=47652", "vpf-goldchicco-release-47652.html", "Goldchicco, Walamab, Apophis; VPForums release metadata v1.1, download16123; geometry/download unavailable")]:
        spec = next(f for f in retained["files"] if f["path"] == filename)
        records.append({"id": identifier, "kind": "human_review", "uri": uri, "sha256": spec["sha256"],
                        "acquired_at": spec["acquired_at"], "source_id": "ipdb:5500" if "wild-texas" in identifier else "ipdb:857" if "photo." in identifier else identifier,
                        "locator": "Retained external:pinmame-manuals/by-machine/" + MACHINE_ID + "/" + filename + "; page/resource metadata in repo:" + RETAINED.as_posix(),
                        "license": "NOASSERTION", "rights": retained["rights"], "attribution": attribution,
                        "excerpts": [excerpt("identity-and-wild-texas.md" if "wild-texas" in identifier else "physical-photos.md")]})
    records.append({"id": "vbs.installed-tilt-route", "kind": "human_review", "uri": "external:pinmame-review-artifacts/" + SESSION.as_posix() + "/installed-vbs",
                    "sha256": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69",
                    "locator": "Installed core.vbs cvpmNudge.DoMechTilt and s7.vbs vpmKeyDown. Both complete file hashes retained in script-bindings.md; these are inspected installed libraries, not a verified exact VPX bundle.",
                    "license": "NOASSERTION", "attribution": "VPinMAME/Visual Pinball script contributors; installed read-only library copy retained externally", "excerpts": [excerpt("script-bindings.md")]})
    records.append({"id": TILT_RUN, "kind": "runtime_scenario", "uri": "repo:" + TILT.as_posix(), "sha256": sha(root / TILT),
                    "locator": "Three controlled fresh-state L-2 runs on1/7/49; exact raw/scenario/init/binary hashes in compact evidence. Observed behavior does not prove lamp fitment.",
                    "license": "NOASSERTION", "attribution": "pinmame-game-defs curator"})
    runtime = load_json(root / RUNTIME)
    records.append({"id": RUN, "kind": "runtime_scenario", "uri": "repo:" + RUNTIME.as_posix(), "sha256": sha(root / RUNTIME), "revision": REVISION,
                    "locator": "Compact derived evidence with exact raw trace/scenario hashes, explicit CMOS initialization and binary/ROM identity. Raw traces retained under external:pinmame-review-artifacts/" + SESSION.as_posix() + "/harness. " + runtime["recreation_notes"][0]["text"],
                    "acquired_at": "2026-10-30T00:10:24Z", "license": "NOASSERTION", "attribution": "pinmame-game-defs curator; acquired_at is final raw trace persistence time"})
    return records


def build(root: Path = ROOT) -> dict[str, Any]:
    displays = []
    layouts = [("player-1", "Player 1 score", 2, 1, 7), ("player-2", "Player 2 score", 3, 9, 7),
               ("player-3", "Player 3 score", 0, 21, 7), ("player-4", "Player 4 score", 1, 29, 7),
               ("ball-tens", "Ball in Play / Match tens", 4, 0, 1), ("ball-units", "Ball in Play / Match units", 5, 8, 1),
               ("credit-tens", "Credits tens", 6, 20, 1), ("credit-units", "Credits units", 7, 28, 1)]
    for key, label, index, start, width in layouts:
        displays.append({"id": f"display.{key}", "label": label, "kind": "segment", "controller_index": index,
                         "segment_start": start, "width": width, "physical_location": "cabinet_or_service",
                         "spatial": na("cabinet_or_service", MANUAL, SOURCE, "photo.firepower-ii-50054"), "provenance": provenance(SOURCE, MANUAL, RUN, "photo.firepower-ii-50054")})
    relationships = [{"id": f"relationship.special-{sensor}-{address}", "kind": "direct", "source": switch_id(sensor),
                      "destination": solenoid_id(address), "provenance": provenance(CORE, SOURCE, RUN)} for address, sensor in SPECIAL_SWITCHES.items()]
    relationships.append({"id": "relationship.right-button-lane-change", "kind": "direct", "source": "switch.right-flipper-button",
                          "destination": switch_id(13), "provenance": provenance(CORE, SOURCE, RUN)})
    return {"format": "pinmame-machine-definition", "schema_version": 2,
            "machine": {"id": MACHINE_ID, "name": "Firepower II", "manufacturer": "Williams", "year": 1983,
                        "model_number": "521", "kind": "physical_pinball", "ipdb_id": 857, "opdb_id": "GRWYk-Mb5OV"},
            "controller": {"platform": "pinmame.system-7", "hardware_generation": "0x10000", "inversion_applied_by_emulator": True},
            "drivers": [{"id": "fpwr2_l2", "description": "Firepower II (L-2)", "manufacturer": "Williams", "year": "1983", "flags": 0,
                         "physical_compatibility": "identical", "variant_notes": "Production model 521, System 7, L-2; ROM member SHA-1 values verified. Physical CPU-board conversion wldtexas is separately owned by unknown-manufacturer.wild-texas (IPDB 5500); shared init does not merge the hardware."}],
            "inputs": inputs(), "outputs": outputs(), "displays": displays, "mechanisms": mechanisms(), "relationships": relationships,
            "coverage": {"status": "partial", "missing": MISSING, "dimensions": {
                "catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "observed",
                "physical_wiring": "conflicted", "mechanisms": "validated", "variant_coverage": "validated",
                "recreation_knowledge": "observed", "spatial_placement": "unknown"}},
            "conflicts": [{"id": "lamp6-40-insert-routing", "path": "outputs",
                           "description": "PDF 13/14 name 6 playfield Shoot Again and 40 Ball in Play; PDF 51 marks 40 NOT USED, while PDF 41 draws backbox 9B6 BALL IN PLAY on column 1/row 6 (public 6). These are different pages of one manual, not independent corroboration. Photos 50030/50054 do not identify socket wiring, and the meaningful runtime 40 bit establishes no fitment. Resolution path: an owner or technician must trace an original model 521 insert-board Ball in Play socket to 9P1 and matrix columns/rows, including whether 6 has a shared backbox load; this requires physical access unavailable in the retained above-playfield/backglass photographs.",
                           "source_refs": [MANUAL, INSERT, "photo.firepower-ii-50038", "photo.firepower-ii-50054", "photo.firepower-ii-50030", RUN]}],
            "sources": sources(root), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"}}


def spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
    missing = [d["id"] for group in ["inputs", "outputs"] for d in definition[group] if "spatial" not in d]
    na_records = {d["id"]: d["spatial"]["reason"] for group in ["inputs", "outputs", "displays"] for d in definition[group] if "spatial" in d}
    return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
            "decision": "partial", "coordinate_convention": "x 0 left / 1 right; y 0 rear / 1 apron, player view",
            "placements": [], "table_geometry": None, "extraction_manifest": None,
            "manual": {"sha256": MANUAL_SHA, "drawings": [14, 15, 17, 48, 49, 50, 51, 52, 53, 54, 55]},
            "unplaced_devices": missing, "not_applicable": na_records,
            "resolved_dispositions": ["Wild Texas is separately owned by unknown-manufacturer.wild-texas.", "CPU F/D banks are optional emulated Master Command scaffolding, not fitted switches on the drawn CPU assembly.", "Lamp 40 retains cabinet applicability but physical routing is conflicted; runtime activity is not fitment evidence."],
            "transport_holes": {"solenoid": [*range(26, 45), 49, 50], "switch": [*range(-2, 1), *range(65, 81)], "dip": list(range(3, 9))},
            "blockers": ["Exact Firepower II VPX has not been retained/extracted/verified; Firepower 1980 is a different game.",
                         "No manual drawing pixels/frame have been measured or reconciled to exact VPX controls; no coordinates are asserted.",
                         "Count and place Type 83 orbit flash bulbs and every stock GI socket. Continued/grouped schematic symbols and all retained top-view/gallery images do not identify a complete socket inventory.",
                         "Trace original model 521 Ball in Play socket to 9P1/matrix bit: PDF 41 column 1/row 6 disagrees with matrix 6/40 and PDF 51 NOT USED. Photos 50030/50054 and ROM transitions cannot settle physical wiring."]}


def report_markdown(report: dict[str, Any]) -> str:
    return "# Firepower II (1983) spatial blockers\n\nCoverage remains **partial**. No normalized positions have been inferred.\n\n" + "\n".join("- " + s for s in report["blockers"]) + "\n\nThe JSON report enumerates every unplaced device, every controlled not_applicable disposition, and transport holes excluded from legal bindings. Manual drawing crops retain native raster resolution. No VPX extraction or manifest is claimed.\n"


KNOWLEDGE_TEXT = """# Firepower II (Williams, 1983)

Coverage remains **partial**. Public addresses, wiring identities, controller
read paths, displays and causal mechanisms are curated from the original
manual, pinned source, photographs and isolated L-2 ROM runs. Physical lamp
routing, socket inventory and exact spatial geometry remain incomplete.

## Identity

Williams model 521, IPDB 857, OPDB GRWYk-Mb5OV. The visually checked cover is
16-521-101, July 1983. IPDB says August 1983; Pinside says June 1983. These
month differences do not alter canonical year 1983. The old OPDB attachment's
1983-01-08 is retained as an identity link, not evidence of a January release.

Only fpwr2_l2 belongs to this original Williams record. wldtexas belongs to
unknown-manufacturer.wild-texas, a separate physical_conversion, IPDB 5500,
unknown manufacturer and null year. Tony Turner's IPDB hardware account and
Theonlylilo's successful Pinside repair describe changed coils/flippers and
a replacement single-EPROM MPU. The retained MPU photo shows the changed
CPU layout. Shared PinMAME init/routing and clone ancestry do not establish
physical identity. No OPDB identity has been invented for the conversion.

## Controller and complete address dispositions

System 7, GEN0x10000, s7_dispS7. Switches and lamps use column-major
(column-1)*8+row numbering. The complete transcriptions preserve all 64 cells,
wire colours, connector pins, drive transistors and Table 4 footnotes.

Services -7/-6 are Advance/Auto-Up; -5 CPU diagnostic; -4 sound diagnostic.
-3 is generic Master Command Enter scaffolding. The normal production
adjustment interface is the coin-door service pair. Matrix 1-49 is wired
except 21 Not Used. Matrix 50-64 is Not Used. 13 is a virtual lane-change
copy of right button 82: core_updateSw overwrites direct 13 writes every
frame. Button 84 is left. Generic flipper-column 81/83/85-88 is unused.
Transport holes -2..0 and 65..80 are not invented inputs.

DIP 1/2 are fitted sound-board switches entering s67s_cmd_w. DIP 3-8 is
undeclared. The emulator exposes F/D bank bits 9-24 through s7_dips_r:
Enter held selects inverted nibbles on PA4-7. They are optional virtual
configuration inputs, not sixteen fitted CPU switches. The CPU BOM item 24
lists DS1/DS2, 8 STD DIP switches, quantity 2; the assembly view of the same factory drawing has no such footprints. Logic
PDF 24-25 wires those PA pins to the IC34/IC35 diagnostic display. The
independent production photo 50056 shows that display and resistor packs
without visible DS1/DS2 banks, supporting the no-fitted-banks disposition.
DIP resistor packages IC28/29/37 are not switches. These transport bit
names are not factory software adjustment numbers.

Outputs 1-25 include coils 1/2/3, Type 83 flash load 4, power-board GI relay 11,
bell 15, two parallel coin-lockout loads 16, six specials 17-22, and game-on 25.
Table 4 marks 5-10/12-14 Not Used; Test 02 still pulses them. 23/24 are swept
PIA slots without fitted circuits on the six-special-driver board.
25 enables specials and driver-board Z1 flipper returns. K1 and Z1 differ.
45/46 follow right 82 and 47/48 follow left 84 while 25 is enabled. These are
used virtual power/hold callback states that assert together; they model
neither separate physical coils nor EOS timing. Custom 51-60 is unavailable
because this game has no custom callback; 26-44/49-50 are transport holes.
Lamps 61-64 are Not Used; 65-96 is absent auxiliary-column space (lampCol0).
System 7 publishes no separate GI channel. Output transitions do not fit loads.

Four seven-digit player displays map callback 2/3/0/1. Four single-digit
fragments at 4/5 and 6/7 form ball/match and credits. s7_dispS7 offsets are
1/9/21/29 and 0/8/20/28 respectively. Photographs verify physical segmented
displays. Synthetic DMD 8 is an emulator render, not fitted hardware.

## Ball movement and mechanisms

Two stored balls occupy 10/11. Drain 9 prompts outhole 1; thrower 2 feeds
shooter trough 12 and a manual plunger launches the ball. Hold occupancy
contacts while a ball rests there and release when it leaves. The source
script models 9, 11, 10 with two balls. The ROM run observes serve 2 on Start
and repeated outhole 1 while 9 is held. A host ball move is not ROM feedback.

Saucer 23 holds the first ball while 2 serves the second. Release 24 fires 3
before 23 is cleared, starting two-ball play. During multiball, saucer entries
score 5,000 and eject immediately (manual operation). A coil does not directly
close a ball-presence contact. The passive orbit uses spinner 18, entry 19
and exit 40; completion fires flash 4. Passive ramp 14/15 awards its lit value,
mystery or extra ball; there is no ramp actuator. The upper orbit's wire
ball preventer is passive (photo 60457), with no invented output.

FIREPOWER letter targets 25-33 are standups, not a resettable drop bank.
16/17 are separate scoring standups; 20/22 are upper rebound contacts.
The IPDB feature count uses different categories; it is not a reason to
delete documented contacts. A-B-C-D 34-37 advance 2x/3x/5x and right-flipper
lane change. Letter groups light jets and the timed bonus-holdover orbit
award; repeated completions light return lanes, ramp extra ball and specials.
Operation and construction excerpts retain the award progression.

Four jets and two slings have separate scoring and direct-power contacts.
PinMAME synthesizes specials 17-22 from 47/48/41/42/43/44; these are not
public power-switch inputs 65-70. Each relation was exercised in gameplay.
Two flippers use dual-wound SFL-19-400/30-750-DC coils and local EOS contacts,
cabinet-switched through Z1. Physical geometry, tuning and pulse duration
remain consumer/table parameters; they are not invented from callback width.

Ordinary matrix contacts are normally open in the factory schematic;
the uninverted read path and Test 03 closure display agree with that
construction. Ball occupancy is not a normally-closed contact. New controlled
runs show plumb 1 warns twice through GI 11 then tilts on the third closure;
playfield 49 tilts immediately. Slam 7 ends play on its first closure and
resumes the attract sequence. These are exact L-2 observations under the
retained initialized settings, not universal adjustment thresholds.

## Lighting and source contradictions

Backbox 1-5, playfield Shoot Again 6, and separate Bonus Holdover 8/23 are
preserved. PDF 51 BACKBOX labels for 45-48 conflict with the game-specific
location drawing and the independent lower-playfield photo; follow the
physical playfield positions. Reprints within the manual are one source.

Lamp 40 publishes meaningful Ball in Play state, but its physical availability
and routing remain unknown.
Figure 1/Figure 2 call 40 Ball in Play; PDF 51 marks 40 NOT USED; PDF 41 draws
9B6 BALL IN PLAY on COL1/ROW6 (public 6), while 6 is the photographed playfield
Shoot Again. Photo 50054 shows sockets without readable circuit identities;
50030's footer does not trace the wiring. The scripts omit 40. Start/tilt
transitions prove meaningful 40 state, not presence or absence of a bulb.
No virtual-only fitment conclusion is justified. Its cabinet applicability
is recorded; no playfield position or bulb quantity is invented.
Resolution path: an owner/technician must trace the original Ball in Play
socket through 9P1 to its matrix bit and check whether 6 shares a backbox load.

Flash 4 is a real plural Type 83 load. Figure 5 gives a grouped callout and
PDF 52-53 a grouped diode/load, not a socket count. The repeated 8L2
designation also labels thrower 2; connector pins preserve separate circuits.
K1 on the power board opens the common 6.3 VAC GI leg when energized; four
fused branches serve two playfield groups (one also cabinet) and two insert
groups. Each is 5 A slow-blow. Z1 on the driver board gates flipper returns.
The GI excerpt transcribes all four branches. PDF 35/41 swap insert fused
pins; PDF 35/48 versus 50 disagree on playfield colours/pins. These are wiring
details, retained literally without turning public device identity into a
conflict. Table 4 versus solenoid schematics also disagrees on 19/21/22 pins,
colours and an omitted 22 footnote; structured values follow the game table.

Actual GI sockets and orbit-flash sockets cannot be counted from continued
schematic symbols. The retained above-playfield/stripped photos and all 16
Pinside previews lack a complete underside/socket inventory; LED-modified
gallery machines do not establish original fitment. No callback quantity
or geometry estimate substitutes for that missing physical evidence.

## Recreation artifacts and evidence

Two exact pinned corpus scripts remain candidates until the exact table is
retained and launched. Newer 1.1 has ChangedLamps 6-39/41-60, virtual render
doubles and callbacks 1/2/3/4/11/15. It writes unfitted 57/58 for flippers
and clears 57 on left release. S7 library writes 82/84 correctly first.
The older script says unverified and pulses 39 from both outlane handlers;
left outlane is 38. These are script defects, not physical source conflicts.

Newer 1.1 also sets vpmNudge.TiltSwitch=7. The inspected installed s7.vbs
routes the mechanical-tilt key to core.vbs DoMechTilt, which pulses that
configured switch. Controlled L-2 runs distinguish 7 slam from 1 plumb and 49
playfield tilt. Repair the recreation's nudge/plumb route to 1. The separately
retained installed libraries are hash-pinned; no exact table library version
or successful launch is claimed.

The PDF was retained 2026-10-29T23:57:07Z, SHA256
c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8.
Complete table transcriptions and native drawing crops are in the excerpt
folder. Source-owned originals remain external. The retained-input manifest
pins 72 source files, native frames, photo/page metadata and 16 gallery
resources with original attribution/rights. Sources include exact URLs,
acquisition times and hashes; none grants redistribution of originals.

Runtime evidence pins the ROM archive/member identity, 46e1a01a native build,
explicit initialization trace/NVRAM and every scenario/raw run. Each run
uses a fresh directory seeded only with that initialization NVRAM.
Test 02 pairs selectors 1-25 with public outputs; slow Test 03 displays 1-49
and blank 50-64, including scanned but physically unused 21. The initial
450 ms sweep missed multiplexed numerals; its 2200 ms successor is distinct.
A repeated pulse masks lane-change overwrite; the one-shot control and
button 82 display establish the actual copy path. Keyboard/simulator are off.

## Concrete remaining coverage requirements

- output_enumeration: exact stock GI socket inventory per branch and Orbit
  Complete Type 83 quantity. All retained schematics/photos/gallery previews
  were inspected; continued/grouped symbols and top views cannot settle it.
  An original-machine underside/socket inspection is needed.
- output_semantics and unresolved_conflicts: Ball in Play 6/40 routing above.
  The ROM probes and available photographs were exhausted for this question;
  only physical tracing can settle which bulb is wired to which bit.
- spatial_placement: no exact VPX is present in Tables, its Archive or
  Downloads. VPU 7485 and VPF 16123 require signed-in download. Retain the
  Goldchicco/Walamab/Apophis 1.1 table, extract/hash it and verify its script
  before reconciling physical controls and individual emitters. Firepower
  (1980) files, including the misnamed 1983 directb2s, are another game.
  Manual drawings have not been measured into a reproducible coordinate
  frame; no positions or fake spatial credit are asserted.

Driver mapping, input semantics, mechanism inventory/behavior, polarity,
variant separation, recreation notes and provenance have source-backed
dispositions above. Their earlier broad missing flags are closed; the
remaining physical-count/geometry blockers do not erase that evidence.
"""


CONVERSION_TEXT = """# Wild Texas (unknown manufacturer/date)

This focused partial record repairs Firepower II's former clone grouping.
IPDB 5500 explicitly identifies a physical Firepower II conversion. Tony
Turner's report names Gottlieb coils/flipper assemblies and a transformer
marked Tri Zone. Theonlylilo's Pinside posts1/6 describe a different
System 7-compatible single27128 MPU, no CPU diagnostic buttons, and a
six/seven-digit selector; after repair it plays with identification2521 1
and space-themed sounds. The retained Tony Turner MPU photograph confirms
a changed CPU layout with one program EPROM. These are attributed physical
observations, not factory documentation or a guarantee about every specimen.

The pinned s7games.c wldtexas driver uses the fpwr2 init and s7_dispS7
routing but its own16KB program. Keep catalog clone_of=fpwr2_l2 while owning
the driver exactly once here. A CPU-board conversion is a separate physical
record. Manufacturer/year remain unknown; no OPDB identity is claimed.

No Williams coil inventory, cabinet controls, spatial positions or GI counts
have been copied here. The conversion lacks a verified exact table, wiring
manual, ROM/physical cross-check and complete assembly/socket inventory.
Its driver compatibility is unknown pending specimen-to-ROM verification;
the shared emulator init proves routing only. Those concrete acquisition
gaps keep identity, I/O/display/mechanism inventories, polarity, variant
details and recreation knowledge incomplete. Source provenance and the
physical grouping decision are retained; this is not a full Wild Texas
curation.
"""


def conversion(root: Path = ROOT) -> dict[str, Any]:
    refs = {"ipdb.wild-texas", "pinside.wild-texas-repair", "photo.wild-texas-42932", SOURCE}
    return {"format": "pinmame-machine-definition", "schema_version": 2,
            "machine": {"id": CONVERSION_ID, "name": "Wild Texas", "manufacturer": "Unknown Manufacturer",
                        "year": None, "kind": "physical_conversion", "ipdb_id": 5500},
            "controller": {"platform": "pinmame.system-7", "hardware_generation": "0x10000",
                           "inversion_applied_by_emulator": True},
            "drivers": [{"id": "wldtexas", "clone_of": "fpwr2_l2", "description": "Wild Texas",
                         "manufacturer": "Unknown Manufacturer", "year": "????", "flags": 0,
                         "physical_compatibility": "unknown",
                         "variant_notes": "Separate physical CPU-board conversion, IPDB 5500. Owner reports changed coils/flippers and replacement MPU. Exact specimen-to-emulated-ROM compatibility remains unverified; shared init is emulator routing evidence only."}],
            "inputs": [], "outputs": [], "displays": [], "mechanisms": [], "relationships": [], "conflicts": [],
            "coverage": {"status": "partial", "missing": [
                "identity", "input_enumeration", "input_semantics", "output_enumeration", "output_semantics",
                "display_inventory", "mechanism_inventory", "mechanism_behavior", "polarity", "variant_differences",
                "recreation_notes", "spatial_placement"],
                "dimensions": {"catalog_identity": "observed", "address_enumeration": "unknown",
                               "semantic_naming": "unknown", "physical_wiring": "unknown",
                               "mechanisms": "unknown", "variant_coverage": "candidate",
                               "recreation_knowledge": "candidate", "spatial_placement": "unknown"}},
            "sources": [s for s in sources(root) if s["id"] in refs],
            "knowledge": {"path": CONVERSION_KNOWLEDGE.as_posix(), "status": "partial"}}

def verify_files(root: Path = ROOT) -> None:
    for relative, digest in [(TILT, TILT_SHA), (RETAINED, RETAINED_SHA)]:
        if not (root / relative).is_file() or sha(root / relative) != digest:
            raise RuntimeError(f"retained evidence manifest absent or changed: {relative}")
    for name, digest in EXCERPTS.items():
        p = root / "evidence/excerpts" / MACHINE_ID / name
        if not p.is_file() or sha(p) != digest:
            raise RuntimeError(f"excerpt absent or changed: {p}")
    for name, digest, _ in IMAGES.values():
        p = root / "evidence/excerpts" / MACHINE_ID / name
        if not p.is_file() or sha(p) != digest:
            raise RuntimeError(f"drawing crop absent or changed: {p}")
    if not (root / RUNTIME).is_file() or sha(root / RUNTIME) != RUNTIME_SHA:
        raise RuntimeError("compact runtime evidence absent or changed")
    for run in [r for relative in [RUNTIME, TILT] for r in load_json(root / relative)["runtime"]["raw_runs"]]:
        p = root / run["scenario_path"]
        if not p.is_file() or sha(p) != run["scenario_sha256"]:
            raise RuntimeError(f"scenario absent or changed: {p}")


def expected_artifacts(root: Path = ROOT) -> dict[Path, bytes]:
    verify_files(root)
    definition = build(root)
    report = spatial_report(definition)
    return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition),
            CONVERSION: canonical_bytes(conversion(root)), CONVERSION_SEED: canonical_bytes(conversion(root)),
            CONVERSION_KNOWLEDGE: CONVERSION_TEXT.encode("utf-8"),
            KNOWLEDGE: KNOWLEDGE_TEXT.encode("utf-8"), REPORT: canonical_bytes(report),
            REPORT_MD: report_markdown(report).encode("utf-8")}


def guard_destination(root: Path) -> None:
    for relative in [DEFINITION, CONVERSION]:
        tail = relative.relative_to("machines/partial")
        for directory in ["author-ready", "stubs"]:
            p = root / "machines" / directory / tail
            if p.exists():
                raise RuntimeError(f"refusing stale/author-ready destination: {p}")
        p = root / relative
        if p.exists():
            try:
                status = load_json(p)["coverage"]["status"]
            except (ValueError, KeyError, TypeError) as exc:
                raise RuntimeError(f"curator drift: invalid destination {relative}") from exc
            if status == "author_ready":
                raise RuntimeError("refusing to overwrite an existing author-ready artifact")


def regenerate(root: Path = ROOT) -> None:
    guard_destination(root)
    verify_external(root)
    for relative, content in expected_artifacts(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def check(root: Path = ROOT) -> None:
    guard_destination(root)
    for relative, content in expected_artifacts(root).items():
        path = root / relative
        if not path.is_file() or path.read_bytes() != content:
            raise RuntimeError(f"curator drift: {relative}")


def configured_root(variable: str) -> Path | None:
    value = os.environ.get(variable)
    if value is None:
        return None
    path = Path(value)
    if not value.strip() or not path.is_dir():
        raise RuntimeError(f"configured evidence root unavailable: {variable}={value!r}")
    return path


def verify_external(root: Path = ROOT) -> None:
    """Optional roots are skipped when absent and fail closed when configured."""
    verify_files(root)
    manuals = configured_root("PINMAME_MANUALS_ROOT")
    if manuals is not None:
        directory = manuals / "by-machine" / MACHINE_ID
        for spec in retained_inputs(root)["files"]:
            p = directory / spec["path"]
            if not p.is_file() or sha(p) != spec["sha256"] or p.stat().st_size != spec["size"]:
                raise RuntimeError(f"retained manual/capture absent or changed: {p}")
    review = configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review is not None:
        for relative, folder in [(RUNTIME, "harness"), (TILT, "tilt-probes")]:
            directory = review / SESSION / folder
            evidence = load_json(root / relative)
            if check_manifest(directory, "fpwr2_l2") != evidence["source"]["sha256"]:
                raise RuntimeError("raw harness directory manifest identity changed")
            for spec in evidence["runtime"]["raw_runs"]:
                p = directory / (spec["name"] + ".json")
                if sha(p) != spec["sha256"]:
                    raise RuntimeError(f"raw harness run changed: {p}")
                run = load_json(p)
                if (run["failure"] is not None or run["game"] != "fpwr2_l2"
                        or run["library_sha256"] != LIBRARY_SHA or run["handle_mechanics"] != 0):
                    raise RuntimeError(f"raw run is failed or from another game/build/mode: {p}")
                if run["scenario"]["sha256"] != spec["scenario_sha256"] or len(run["steps"]) != spec["action_count"]:
                    raise RuntimeError(f"raw scenario provenance differs: {p}")
        if sha(review / SESSION / "harness/init-state/nvram/fpwr2_l2.nv") != NVRAM_SHA:
            raise RuntimeError("initialization NVRAM changed")
        for name, digest in VBS_FILES.items():
            p = review / SESSION / "installed-vbs" / name
            if not p.is_file() or sha(p) != digest:
                raise RuntimeError(f"installed VBS evidence absent or changed: {p}")
        snapshot = review / "opdb-import/latest-opdb.json"
        if not snapshot.is_file() or sha(snapshot) != "690f784a7968987e39ef20e1aff7bd15ea0d67385bafb5556a027802d2032c93":
            raise RuntimeError("retained OPDB identity-search snapshot absent or changed")
    checkout = configured_root("PINMAME_SOURCE_ROOT")
    if checkout is not None:
        for name, digest in SOURCE_FILES.items():
            p = checkout / name
            if not p.is_file() or sha(p) != digest:
                raise RuntimeError(f"pinned source absent or changed: {p}")
    scripts = configured_root("PINMAME_VPX_SCRIPTS_ROOT")
    if scripts is not None:
        for name, digest in SCRIPT_FILES.items():
            p = scripts / name
            if not p.is_file() or sha(p) != digest:
                raise RuntimeError(f"pinned script absent or changed: {p}")
    roms = configured_root("PINMAME_ROM_LIBRARY_ROOT")
    if roms is not None:
        archive = roms / "fpwr2_l2.zip"
        if not archive.is_file() or sha(archive) != ROM_SHA:
            raise RuntimeError("authorized ROM archive absent or changed")
        with ZipFile(archive) as z:
            members = {m.filename: (m.file_size, hashlib.sha1(z.read(m)).hexdigest()) for m in z.infolist()}
        if members != ROM_MEMBERS:
            raise RuntimeError("ROM members differ from pinned s7games.c declarations")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        verify_external()
        print("Firepower II definition, seed, knowledge, excerpts, scenarios and spatial blockers match.")
    else:
        regenerate()
        print("Regenerated Firepower II partial artifacts.")


if __name__ == "__main__":
    main()
