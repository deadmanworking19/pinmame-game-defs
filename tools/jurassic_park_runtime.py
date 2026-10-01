"""Compact derived runtime evidence for Jurassic Park 5.13, rebuilt from the retained raw runs.

The raw traces, every DMD snapshot and the isolated state directories stay under the working root's
review-artifacts; this module turns them into tools/jurassic_park_runtime.json, which the curator
embeds in an excerpt and the tests re-derive when the evidence root is present. Names read off the
DMD were read visually from the retained PGM frames (an OCR pass over the same frames only
confirmed the wire-colour and number rows); each reading is bound to the frame by its pixel hash.

    python tools/jurassic_park_runtime.py <runtime-dir> --write
    python tools/jurassic_park_runtime.py <runtime-dir> --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "jurassic_park_runtime.json"
SCENARIO_DIR = ROOT / "tools" / "harness-scenarios" / "data-east"
RUNS = ("active-switch-test", "lamp-test", "coil-cycle", "coil-cycle-trex-homed", "laser-kick-test", "trex-test")
LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
ROM_ARCHIVE = "jupk_513.zip"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jurassic_park_data import (  # noqa: E402
    LASER_KICK_PAIRS, ROM_COIL_NAMES, ROM_LAMP_NAMES, ROM_SWITCH_NAMES, SWITCH_COLUMNS, SWITCH_ROWS,
)

# Public coil / flash-lamp / relay number -> pixel hash of the DMD frame that shows its name in the cycle test.
# The names were read visually from the retained coil-cycle frames (ROM_COIL_NAMES); the hash binds each reading to
# its frame, and the frames are deterministic, so a rerun of the scenario reproduces them at shifted snapshot times.
COIL_CYCLE_FRAMES = {
    1: "2c6e45809dc565a949482534b9a38e9ea705dd22b66a4fe4a2a453e82d208a69",
    2: "a430e62710877f60dc540e6c5d285e7fa82ae82b49d07aab296a9121d1c017dd",
    3: "2b5caba87e89d73afc5ef2d93b006563f723d62f7bfa7f4196b70584f95389d4",
    4: "2fb68a1b12246cd331330d213e925ad462d5893154d7bf0f86dcb647a9b3c937",
    5: "723311772754e74fcc16b2c963dfb641c47ddf49b5dcf34cd7e278cefc842e83",
    6: "94bb086ea56e2c2a99ff2dbafcdb33c4d7749b831c23dc1725bbb9a78959a4a7",
    7: "4ee3e56f8e57f90427cb6d7c9998b18b39598fe0106dc1d085d8c9deeb6665bb",
    8: "82ddfbef175a04f3aee536de6b1f0d06b87757bd46de592cc1fdb1a9b6d66a15",
    9: "7a840fde9562d008e44b020ab281b20318223d0e57a26bab05d9fef9eaec8f4a",
    11: "4fbae88ad482e13ce88166684e05af874ce1f005d34fe4ffe3cded6555b879bb",
    12: "660b48bcdd2bab149e253a4166700b18c7096096814429cf40b08eb7d2fbdf2c",
    13: "6ccca9475159623f254e4897629172403472c36502530ef81fa08eb198fb7da3",
    14: "d212a2b420b53160102821cd13800781599ce8d54efc4e0279ba173cae7b64a3",
    15: "1552eafd4d7412ea66a7f194c5c602bb7166cd849b1112288d643073719e83fb",
    16: "3295043acb73030362aede78168f724472ac9373bbf4a3b7a45ad67e00711b43",
    17: "031d244c4b44ef83528fc94453ee7b814ef9e889d6f584a0a09f11967f4b378f",
    18: "079e7d0c4be70d1743cb8441b3cd8e30160247158bf1bc4dd89f900744ce2b36",
    19: "b89202480a7b2b3388fd95c538a4cc31796c6e5b5f28a90c6870e412473b5d31",
    20: "0d667d26f026d7cf7a2fe0ca50bcdfd79b48a2ba7d3b87d238445487925aa489",
    21: "1a963919d3b6b7f58c7888443db6cc145995384c23a7acd03d1a8b5f026bd403",
    22: "fc3039102cf36194e992c94119b6e15c47df992c3bcec09c56e39a29664ca0be",
    25: "a9c460de24b31e851c3d2950dc70ea1df969aa94b9df31341baee1c47fc2fecd",
    26: "357f17df60b2672785cd1babe62f4506d098e8ec0ebfa921648ee8160d03e3ef",
    27: "32417158b41718502f18f96bc3375408269a57c05ff0a174daff9573dc794c80",
    28: "f2715e726ed314bde21ae0e60a875abf9ade244cc0194e4e577c013d4ce59922",
    29: "9d24a6474d4f3622e9f6a628b1638b79e8396c774b7319f171db2b37d3c2fc98",
    30: "3bb9967a9a945486dcc9407e7fe99c5766e0c016ea36d6f7ee78308d623337c5",
    31: "d22bbdf1889ed0860c8e5f4b840bf9ff38616363bfcc3ff78740de1124052424",
    32: "c3fa00fd3b224259d0e2b02bfeaf391a9e553cb5b3f70447abc24057c9e7b2b6",
}
# T-Rex test closures: the label the DMD turns ON for each public address (visual reading).
TREX_ON_LABELS = {57: "TOP SWITCH", 58: "BOTTOM SWITCH", 36: "CENTER SWITCH", 31: "RIGHT SWITCH", 32: "LEFT SWITCH"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frame_record(run_dir: Path, snapshot: dict) -> dict:
    display = snapshot["displays"][0]
    pgm = run_dir / "dmd" / Path(display["artifact"].replace("\\", "/")).name
    return {"snapshot_label": snapshot["label"], "pixel_sha256": display["pixel_sha256"],
            "pgm_file": pgm.name, "pgm_sha256": sha256_file(pgm)}


def run_meta(runtime: Path, name: str) -> tuple[Path, dict, dict]:
    run_dir = runtime / name
    raw = load(run_dir / "run.json")
    if raw.get("failure") or raw.get("game") != "jupk_513" or raw.get("library_sha256") != LIBRARY_SHA256:
        raise ValueError(f"{name}: failed run, wrong game or wrong library")
    scenario = SCENARIO_DIR / f"jupk-513-{name}.json"
    if raw["scenario"]["sha256"] != sha256_file(scenario):
        raise ValueError(f"{name}: retained run did not execute the committed scenario")
    if raw["initial_switches"] != load(scenario).get("initial_switches", []):
        raise ValueError(f"{name}: initial switches differ from the scenario")
    return run_dir, raw, {"raw_sha256": sha256_file(run_dir / "run.json"),
                          "scenario_sha256": raw["scenario"]["sha256"],
                          "scenario": f"tools/harness-scenarios/data-east/jupk-513-{name}.json"}


def solenoids_by_step(raw: dict) -> dict[str, dict[int, list[int]]]:
    return {step["label"]: {s["number"]: s["states"] for s in step.get("transitions", {}).get("solenoids", [])}
            for step in raw["steps"]}


def active_switches(runtime: Path) -> dict:
    run_dir, raw, meta = run_meta(runtime, "active-switch-test")
    snapshots = {s["label"]: s for s in raw["snapshots"]}
    steps = {s["label"]: s for s in raw["steps"]}
    if not any(o.get("number") == 23 and 1 in o.get("states", [])
               for o in steps["Wait for Active Switch Test readiness"]["transitions"]["solenoids"]):
        raise ValueError("output 23 readiness not observed")
    records = []
    for address in range(1, 65):
        label = (f"Active Switch closure {address} (held)" if address < 63 else
                 "Active Switch Left flipper button (held)" if address == 63 else
                 "Active Switch Right flipper button (held)")
        col, row = divmod(address - 1, 8)
        records.append({"address": address, "displayed_name": ROM_SWITCH_NAMES[address - 1],
                        "displayed_wires": f"{SWITCH_COLUMNS[col][0]} {SWITCH_ROWS[row][0]}",
                        "displayed_number": f"#{address:02d}", **frame_record(run_dir, snapshots[label])})
    flipper = {key: {s["number"]: s["states"] for s in steps[f"Active Switch {key} flipper button"]
                     ["transitions"]["solenoids"]} for key in ("Left", "Right")}
    return {**meta, "records": records, "flipper_buttons": flipper}


def lamp_test(runtime: Path) -> dict:
    run_dir, raw, meta = run_meta(runtime, "lamp-test")
    snapshots = {s["label"]: s for s in raw["snapshots"]}
    records = []
    for lamp in range(1, 65):
        settled = snapshots[f"Lamp Test step {lamp + 1:02d}"]
        if settled["active_lamps"] != [lamp]:
            raise ValueError(f"lamp {lamp}: expected only that lamp lit, saw {settled['active_lamps']}")
        # The next press' held frame still shows this lamp's name: bind the reading to both frames.
        held = snapshots[f"Lamp Test step {lamp + 2:02d} (held)"]
        if held["displays"][0]["pixel_sha256"] != settled["displays"][0]["pixel_sha256"]:
            raise ValueError(f"lamp {lamp}: DMD frame changed between the settled and held snapshots")
        records.append({"address": lamp, "displayed_name": ROM_LAMP_NAMES[lamp - 1],
                        "active_lamps": settled["active_lamps"], **frame_record(run_dir, settled)})
    return {**meta, "records": records}


def coil_cycle(runtime: Path) -> dict:
    run_dir, raw, meta = run_meta(runtime, "coil-cycle")
    pulses = [(e["time_s"], e["number"]) for e in raw["events"] if e["event"] == "solenoid" and e["state"] == 1]
    snapshots = raw["snapshots"]
    records = []
    for coil, digest in sorted(COIL_CYCLE_FRAMES.items()):
        index = next(i for i, shot in enumerate(snapshots) if shot["displays"][0]["pixel_sha256"] == digest)
        snapshot = snapshots[index]
        # The ROM paints a name for about as long as one cycle step, from its pulse until the next one:
        # the latest pulse before the snapshot must be the coil, no more than 1.5 s earlier.
        earlier = [(t, n) for t, n in pulses if t <= snapshot["time_s"] and n not in (10, 23)]
        hits = [earlier[-1]] if earlier and snapshot["time_s"] - earlier[-1][0] <= 1.5 else []
        if coil in (14, 15):
            if any(n == coil for t, n in pulses if t >= 40):
                raise ValueError(f"coil {coil} pulsed during the cycle")
            hits = []
        elif [n for _, n in hits] != [coil]:
            raise ValueError(f"snapshot {index}: expected the latest pulse to be {coil}, saw {hits}")
        records.append({"address": coil, "displayed_name": ROM_COIL_NAMES[coil], "snapshot_index": index,
                        "snapshot_time_s": snapshot["time_s"],
                        "pulse_time_s": hits[0][0] if hits else None, **frame_record(run_dir, snapshot)})
    cycle = [n for t, n in pulses if 42 <= t < 80 and n not in (23,)]
    return {**meta, "records": records, "first_cycle_order": cycle}


def boot_homing(runtime: Path) -> dict:
    result = {}
    for name in ("coil-cycle", "coil-cycle-trex-homed"):
        run_dir, raw, meta = run_meta(runtime, name)
        events = [(e["time_s"], e["number"], e["state"]) for e in raw["events"]
                  if e["event"] == "solenoid" and e["number"] in (12, 13, 14, 15) and e["time_s"] < 12]
        result[name] = {**meta, "initial_switches": raw["initial_switches"], "boot_events": events}
    return result


def laser_kick(runtime: Path) -> dict:
    _, raw, meta = run_meta(runtime, "laser-kick-test")
    steps = solenoids_by_step(raw)
    records = []
    for label, solenoids in steps.items():
        if label.startswith("Laser Kick Test closure "):
            address = int(label.rsplit(" ", 1)[1])
            records.append({"address": address, "solenoids": {str(k): v for k, v in solenoids.items()}})
    fired = {r["address"]: sorted(int(k) for k in r["solenoids"]) for r in records}
    for address, coil in LASER_KICK_PAIRS.items():
        if fired.get(address) != [coil]:
            raise ValueError(f"laser kick {address}: expected only coil {coil}, saw {fired.get(address)}")
    if any(coil for address, coil in fired.items() if address not in LASER_KICK_PAIRS and coil):
        raise ValueError("an unexpected closure fired a coil")
    return {**meta, "records": records}


def trex_test(runtime: Path) -> dict:
    run_dir, raw, meta = run_meta(runtime, "trex-test")
    snapshots = {s["label"]: s for s in raw["snapshots"]}
    steps = solenoids_by_step(raw)
    closures = [{"address": a, "on_label": TREX_ON_LABELS[a],
                 **frame_record(run_dir, snapshots[f"T-Rex Test closure {a} (held)"])} for a in TREX_ON_LABELS]
    motors = {label: {str(k): v for k, v in steps[label].items()} for label in (
        "Left flipper with Top closed", "Right flipper with Top closed", "Start with Top closed, Center open",
        "Start with Top and Center closed", "Launch trigger (41) with the T-Rex homed")}
    return {**meta, "closures": closures, "controls": motors}


def build(runtime: Path) -> dict:
    return {
        "format": "jurassic-park-runtime-summary", "version": 1, "game": "jupk_513",
        "pinmame_revision": PINMAME_REVISION, "library_sha256": LIBRARY_SHA256, "rom_archive": ROM_ARCHIVE,
        "active_switch_test": active_switches(runtime), "lamp_test": lamp_test(runtime),
        "coil_cycle": coil_cycle(runtime), "boot_homing": boot_homing(runtime),
        "laser_kick_test": laser_kick(runtime), "trex_test": trex_test(runtime),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    summary = build(args.runtime)
    payload = (json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise SystemExit("runtime summary drift")
        print("runtime summary matches")
    else:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
