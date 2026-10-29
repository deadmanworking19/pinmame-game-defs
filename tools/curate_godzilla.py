"""Deterministically curate the partial Sega Godzilla machine from pinned evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json
try:
    from drawing_callouts import fit, apply, leave_one_out
    from build_external_evidence_manifest import check_manifest
except ModuleNotFoundError:
    from tools.drawing_callouts import fit, apply, leave_one_out
    from tools.build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/data/godzilla/definition.json"
SPATIAL_SEED = ROOT / "tools/data/godzilla/spatial.json"
PARTIAL = ROOT / "machines/partial/sega/godzilla-1998.json"
AUTHOR_READY = ROOT / "machines/author-ready/sega/godzilla-1998.json"
TEXT_ARTIFACTS = {
    ROOT / "knowledge/sega/godzilla-1998.md": ROOT / "tools/data/godzilla/knowledge.md",
    ROOT / "reports/spatial/sega/godzilla-1998.md": ROOT / "tools/data/godzilla/spatial-report.md",
}
MANUAL_SHA256 = "fc71e6584b2a8ad715100f94b5d4d690b0cd3864cd9abd6746c2441ad4d6c1c5"
SCRIPT_SHA256 = "95d77a6678cc735792091e582abd66983a709b28e9bde307679d10029598949b"
SPATIAL_SHA256 = "48c11b3c041840ecebaecd7c11792ee6a0b7c1e74c71b72b8578d50103fd306a"
TABLE_SHA256 = "9b5d3a0fce830ec18d8423e42cddfc763646aa1f712bed954de0cc10175ca37d"
EXTRACTION_MANIFEST_SHA256 = "6afdd84196c67308837e5311cea0f274f3f540c21b5eabdc1114412aa729913f"
MANUAL = "manual.sega.godzilla.1998.gameex"
CORE = "pinmame.core.46e1a01a0f73"
SCRIPT = "vpx-script.godzilla-vpw-1"
TABLE = "vpx-table.godzilla-vpw-1"
IDENTITY = "human-review.godzilla.ipdb-4443"
LIBRARY = "vpx-script.vpinmame-sega-361"
CORE_LIBRARY = "vpx-script.vpinmame-core-361"
RUNTIME_EVIDENCE = {
    "godzilla": ("runtime.godzilla-205-gameplay", "e7d380dc9d0b3777ab1575539cc114d61b01d8cf40be6b885ef5edb1ff8198c1"),
    "godz_100": ("runtime.godzilla-100-gameplay", "e3fc31dbed9fa8a3e2e0713165949199e6ac8908f843f23460e44b527f9160be"),
    "godz_090": ("runtime.godzilla-090-gameplay", "278f619ec00ae6fdb6b9cbf0a3d61c2f7ca10ade11f99036b216ad7383bbfd70"),
}


def runtime_path(driver: str) -> Path:
    return ROOT / f"evidence/runtime/whitestar/godzilla-{driver.replace('_', '-')}-gameplay.json"


def runtime_sources() -> list[dict]:
    records = []
    for driver, (identifier, digest) in RUNTIME_EVIDENCE.items():
        path = runtime_path(driver)
        if sha256(path) != digest:
            raise ValueError(f"Changed compact runtime evidence: {path}")
        records.append({
            "id": identifier, "kind": "runtime_scenario", "sha256": digest,
            "uri": path.relative_to(ROOT).as_posix(),
            "revision": "46e1a01a0f73dc5ce163d98db1ae435883ecc450",
            "acquired_at": {"godzilla": "2026-10-29T18:13:49.1696064Z", "godz_100": "2026-10-29T18:19:55.0705974Z", "godz_090": "2026-10-29T18:19:55.0886595Z"}[driver],
            "locator": f"{driver}: fresh-state serve/launch, individual bumper, sling and flipper inputs; per-run ROM/binary/scenario/raw-trace hashes in the evidence file",
            "license": "NOASSERTION; no ROM bytes redistributed",
            "attribution": "PinMAME contributors; pinmame-game-defs harness; user-authorized ROM library",
        })
    return records
EXCERPT_DIR = ROOT / "evidence/excerpts/sega.godzilla.1998"
EXCERPT_HASHES = {
    "coils-front.md": "67d763209f013f0c359627ae9fc11df96c16cc6eef8289940fa90eefb1010b0a",
    "controller-and-script.md": "7cf9846d1c99fffecdea7dc47b62fc6b7567979721bca630fc843b2e370de285",
    "dip-settings-front.md": "39fdd4814c36f0cdfe998e68b23fac48c6f15e37a03ed2190536063f28253283",
    "gi-wiring.md": "8d6e1b5c109cf363caa468646c2c5429c56a1706a9b0828e20f47c2d14c9c477",
    "identity.md": "27734ed7c652c966b288048236ad041bfec47fc3ea9fe3cc7b37f27dd10a235f",
    "lamp-matrix-front.md": "3f636e6e98fea7a72844e6966928acfa9c1a61c28b2afe34d25cc2ad03a9bbde",
    "mechanism-facts.md": "9bb081434c8b21d8087f9dd2eb69d43b44ad8aff88c5a58be930625f8e075e44",
    "switch-matrix-front.md": "0d99c6cdfe253d82b1ce4d991644fed1fae041f6987ea05327639772608755dc",
    "trough-parts.md": "083d32baee1306f59db45bc5f3dd87c0334d04eb6c81a166d3ab504f2d260a4a",
    "vpinmame-libraries.md": "9943ca7a3c6973b6251ffa846c5c8f9ba32ab68c1b86fc175ab4633da22e7bec",
    "flipper-wiring.md": "5850df21d0947cdab98c17c95512d0395cdf435be8af0064d0169d04fac40621",
    "factory-location-drawings.md": "fc932c7bcd72069307ccf3630f6f55b62ff520887a127031e76a32e30803c96e",
}
SWITCH_WIRES = [("GRN-BRN","CN5-P1"),("GRN-RED","CN5-P3"),("GRN-ORG","CN5-P4"),
                ("GRN-YEL","CN5-P5"),None,("GRN-BLU","CN5-P7"),("GRN-VIO","CN5-P8"),("GRN-GRY","CN5-P9")]
ROW_WIRES = [("WHT-BRN","CN7-P9"),("WHT-RED","CN7-P8"),("WHT-ORG","CN7-P7"),
             ("WHT-YEL","CN7-P6"),("WHT-GRN","CN7-P5"),("WHT-BLU","CN7-P3"),
             ("WHT-VIO","CN7-P2"),("WHT-GRY","CN7-P1")]
LAMP_COLUMNS = [("U17","YEL-BRN","J13-P9"),("U16","YEL-RED","J13-P8"),("U15","YEL-ORG","J13-P7"),
                ("U14","YEL-BLK","J13-P6"),("U13","YEL-GRN","J13-P5"),("U12","YEL-BLU","J13-P4"),
                ("U11","YEL-VIO","J13-P3"),("U10","YEL-GRY","J13-P1")]
LAMP_ROWS = [("Q33","RED-BRN","J12-P1"),("Q34","RED-BLK","J12-P2"),("Q35","RED-ORG","J12-P3"),
             ("Q36","RED-YEL","J12-P4"),("Q37","RED-GRN","J12-P5"),("Q38","RED-BLU","J12-P6"),("Q39","RED-VIO","J12-P8")]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while data := stream.read(1024 * 1024):
            h.update(data)
    return h.hexdigest()


def verify_configured_evidence(spatial: dict) -> None:
    for variable, relative, digest in (
        ("PINMAME_MANUALS_ROOT", "by-machine/sega.godzilla.1998/godzilla-gameex-manual.pdf", MANUAL_SHA256),
        ("PINMAME_VPX_SOURCES_ROOT", "sega/godzilla-1998/extracted/script.vbs", SCRIPT_SHA256),
        ("PINMAME_VPX_SOURCES_ROOT", "sega/godzilla-1998/Godzilla (Sega 1998) VPW v1.0.vpx", TABLE_SHA256),
        ("PINMAME_VPX_SOURCES_ROOT", "libraries/vpinmame-3.61/sega.vbs", "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"),
        ("PINMAME_VPX_SOURCES_ROOT", "libraries/vpinmame-3.61/core.vbs", "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"),
    ):
        value = os.environ.get(variable)
        if value:
            path = Path(value) / relative
            if not path.is_file() or sha256(path) != digest:
                raise ValueError(f"{variable} does not contain the pinned evidence: {path}")
    if value := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        extraction = Path(value) / "sega/godzilla-1998/extracted"
        if check_manifest(extraction, "godzilla") != EXTRACTION_MANIFEST_SHA256:
            raise ValueError("Changed complete Godzilla extraction manifest")
        root = Path(value) / "sega/godzilla-1998/extracted/gameitems"
        for item in spatial["switches"] + spatial["actuators_and_effects"]:
            path = root / item["raw_object"]
            if not path.is_file() or sha256(path) != item["sha256"]:
                raise ValueError(f"Changed retained VPX object: {path}")
    if value := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        root = Path(value) / "sega.godzilla.1998"
        for page in spatial["pages"].values():
            path = root / page["render_path"]
            if not path.is_file() or sha256(path) != page["render_sha256"]:
                raise ValueError(f"Changed retained factory render: {path}")
        path = root / "ipdb-machine-4443.json"
        if not path.is_file() or sha256(path) != "e9fb0debf6cd6e461d66da56bba9f41a9179cb76bde8bcee78fdeb8c88fdcf7a":
            raise ValueError(f"Changed retained identity capture: {path}")
        harness = root / "harness"
        expected = "46e9b7f0a91f8e3da47d1c2cde741850661495a07957e2caf802d212889e3519"
        if check_manifest(harness, "godzilla") != expected:
            raise ValueError("Changed complete Godzilla runtime manifest")


def provenance(*refs: str, status: str = "observed") -> dict:
    return {"source_refs": list(refs), "status": status}


def unavailable(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def located(identifier: str, role: str, coords: list[tuple[float, float]], *refs: str) -> dict:
    return {"status": "observed", "placements": [
        {"id": f"{identifier}.{role}.{i}", "role": role, "space": "playfield",
         "x": round(x, 6), "y": round(y, 6), "provenance": provenance(*refs)}
        for i, (x, y) in enumerate(coords, 1)]}


def read_grid(filename: str, expected: int) -> dict[int, str]:
    result = {}
    for line in (EXCERPT_DIR / filename).read_text(encoding="utf-8").splitlines():
        cells = [s.strip() for s in line.strip().strip("|").split("|")]
        if len(cells) != 9 or not cells[0].isdigit():
            continue
        for cell in cells[1:]:
            match = re.fullmatch(r"(\d+)\s+(.+)", cell)
            if match:
                number = int(match.group(1))
                if number in result:
                    raise ValueError(f"Duplicate chart cell {number} in {filename}")
                result[number] = match.group(2)
    if set(result) != set(range(1, expected + 1)):
        raise ValueError(f"Incomplete literal matrix: {filename}")
    return result


def read_coils() -> dict[int, list[str]]:
    rows = {}
    for line in (EXCERPT_DIR / "coils-front.md").read_text(encoding="utf-8").splitlines():
        cells = [s.strip() for s in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        m = re.match(r"#(F?)(\d+)\s+(.+)", cells[0])
        if m:
            number = int(m.group(2)) + (24 if m.group(1) else 0)
            rows[number] = [m.group(3), *cells[1:]]
    if set(rows) != set(range(1,33)):
        raise ValueError("Incomplete detailed coil chart")
    return rows


def aliases(namespace: str, number: int, previous: dict | None = None, manual: str | None = None) -> list[dict]:
    result = [{"namespace": namespace, "value": str(number)}]
    if previous:
        result.extend(previous.get("aliases", []))
    if manual:
        result.append({"namespace": "manual.address", "value": manual})
    seen = set()
    return [a for a in result if (a["namespace"], a["value"]) not in seen and not seen.add((a["namespace"], a["value"]))]


def device(identifier: str, label: str, kind: str, group: str, number: int, availability: str, refs: tuple[str,...], **kw) -> dict:
    return {"id":identifier,"label":label,"kind":kind,"binding":{"group":group,"device":number},
            "availability":availability,"provenance":provenance(*refs),**kw}


def source_records(base: dict) -> list[dict]:
    manual = next(s for s in base["sources"] if s["id"] == MANUAL)
    manual["acquired_at"] = "2026-10-29T18:06:21Z"
    manual["excerpts"] = []
    for name, locator, reviewed in (
        ("dip-settings-front.md","PDF 5, DR. 3, country DIP settings",True),
        ("switch-matrix-front.md","PDF 6, DR. 4, switch and dedicated matrix",False),
        ("lamp-matrix-front.md","PDF 6, DR. 4, lamp matrix",False),
        ("coils-front.md","PDF 8, DR. 6, detailed coil chart",False),
        ("gi-wiring.md","PDF 89, printed 83, GI wiring",False),
        ("trough-parts.md","PDF 77, printed 71, trough parts",True),
        ("mechanism-facts.md","PDF 22–23, 77, 81, 95–96, mechanisms and opto theory",True),
        ("flipper-wiring.md","PDF 92, printed 86, flipper circuit and technical overview",True),
    ):
        manual["excerpts"].append({"id":"excerpt.godzilla."+name[:-3], "locator":locator,
            "path":"evidence/excerpts/sega.godzilla.1998/"+name,"sha256":EXCERPT_HASHES[name],
            "method":"mixed","transcribed_by":"curator; read from native-resolution render","reviewed":reviewed})
    for n, digest, xref in ((7,"e673220f4755e6852683ff663ace1cf4f480b779f5a50bafcc5a25c218a2597a",37),
                            (9,"d4467a30db93b0e71371144e41dc4c24c16f092a8c33975a1af8cd555c81af60",47)):
        image = EXCERPT_DIR / f"factory-{n}.webp"
        if sha256(image) != digest:
            raise ValueError(f"Changed factory crop: {image}")
        manual["excerpts"].append({"id":f"excerpt.godzilla.factory-{n}","locator":f"PDF {n}, factory location drawing",
          "path":"evidence/excerpts/sega.godzilla.1998/factory-location-drawings.md","sha256":EXCERPT_HASHES["factory-location-drawings.md"],
          "image":f"evidence/excerpts/sega.godzilla.1998/factory-{n}.webp","image_sha256":digest,
          "image_derivation":f"godzilla-gameex-manual.pdf page {n}, crop box 0.52,0.07,0.9,0.79, scanned page rendered at its native resolution (embedded image xref {xref}, 1280px across 8.53in), rendered at 150 dpi, grayscale, 485x1189 WebP quality 5",
          "method":"manual","transcribed_by":"curator","reviewed":True})
    excerpt = {"id":"excerpt.godzilla.controller-script","locator":"segames.c, se.c and VPW script.vbs relevant read paths and callbacks",
      "path":"evidence/excerpts/sega.godzilla.1998/controller-and-script.md","sha256":EXCERPT_HASHES["controller-and-script.md"],
      "method":"manual","transcribed_by":"curator","reviewed":True}
    identity_excerpt = {"id":"excerpt.godzilla.identity","locator":"retained IPDB machine 4443 capture",
      "path":"evidence/excerpts/sega.godzilla.1998/identity.md","sha256":EXCERPT_HASHES["identity.md"],
      "method":"manual","transcribed_by":"curator","reviewed":True}
    library_excerpt = {"id":"excerpt.godzilla.vpinmame-libraries","locator":"sega.vbs key handlers and core.vbs flipper constants and lamp mapping",
      "path":"evidence/excerpts/sega.godzilla.1998/vpinmame-libraries.md","sha256":EXCERPT_HASHES["vpinmame-libraries.md"],
      "method":"manual","transcribed_by":"curator","reviewed":True}
    return [manual,
      {"id":CORE,"kind":"pinmame_core","uri":"https://github.com/vpinball/pinmame",
       "revision":"46e1a01a0f73dc5ce163d98db1ae435883ecc450",
       "locator":"src/wpc/segames.c INITGAME Godzilla; src/wpc/se.h SE_SWMEMORYPROTECT=-3; src/wpc/se.c coin-door memoryProtectSw, read paths, nLamps, nSolenoids, fastflip, giaux_w and se_solenoid_w; src/wpc/core.c core_m2swSeq and core_updateSw",
       "license":"BSD-3-Clause","attribution":"PinMAME contributors","excerpts":[excerpt]},
      {"id":SCRIPT,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/sega/godzilla-1998/extracted/script.vbs",
       "sha256":SCRIPT_SHA256,"acquired_at":"2026-10-29T18:03:39Z","locator":"retained VPW v1.0 script, switch events, callbacks and lamp mapping",
       "license":"NOASSERTION","attribution":"VPW team","known_working":True,"excerpts":[excerpt]},
      {"id":TABLE,"kind":"vpx_table","uri":"external:pinmame-vpx-sources/sega/godzilla-1998/Godzilla (Sega 1998) VPW v1.0.vpx",
       "sha256":TABLE_SHA256,"acquired_at":"2026-10-29T18:03:36Z","locator":"retained VPW v1.0 table and extracted gameitems; bounds 0,0–952,2206.5",
       "license":"NOASSERTION","attribution":"VPW team"},
      {"id":LIBRARY,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/libraries/vpinmame-3.61/sega.vbs",
       "sha256":"d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924","acquired_at":"2026-10-29T18:21:55Z",
       "locator":"retained sega.vbs flipper and service switch constants and handlers","license":"NOASSERTION","attribution":"VPinMAME contributors","excerpts":[library_excerpt]},
      {"id":CORE_LIBRARY,"kind":"vpx_script","uri":"external:pinmame-vpx-sources/libraries/vpinmame-3.61/core.vbs",
       "sha256":"a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69","acquired_at":"2026-10-29T18:21:55Z",
       "locator":"retained core.vbs flipper output constants and vpmMapLights","license":"NOASSERTION","attribution":"VPinMAME contributors","excerpts":[library_excerpt]},
      {"id":IDENTITY,"kind":"human_review","uri":"https://www.ipdb.org/machine.cgi?id=4443",
       "sha256":"e9fb0debf6cd6e461d66da56bba9f41a9179cb76bde8bcee78fdeb8c88fdcf7a",
       "acquired_at":"2026-10-29T18:09:44Z","locator":"retained browser capture review-artifacts/sega.godzilla.1998/ipdb-machine-4443.json; machine 4443, model 40",
       "license":"NOASSERTION","attribution":"Internet Pinball Database","excerpts":[identity_excerpt]},
      *runtime_sources(),
      *[s for s in base["sources"] if s["id"] == "legacy.game.godzilla"]]


def matrix_inputs(base: dict, spatial: dict) -> list[dict]:
    old = {d["binding"]["device"]:d for d in base["inputs"] if d["binding"]["group"] == "pinmame.input.switch"}
    chart = read_grid("switch-matrix-front.md",64)
    points = {p["address"]:p for p in spatial["switches"]}
    items = []
    dedicated = {-3:("Memory Protect","service.memory-protect"),-2:("Volume / Left","service.button"),
                 -1:("Service Credit / Right","service.button"),0:("Begin Test / Enter","service.test")}
    for n,(label,role) in dedicated.items():
        refs = (CORE,) if n == -3 else (CORE,MANUAL)
        d=device("switch.dedicated-"+str(n).replace("-","minus-"),label,"switch","pinmame.input.switch",n,"used",refs,
                 aliases=aliases("pinmame.switch",n,old.get(n)), roles=[role],
                 physical={"location":"coin door","switch_type":"button"},spatial=unavailable("cabinet_or_service",*refs))
        if n in {-2,-1,0}:
            wire, pin, printed = {-2:("GRY-BLU","CN6-P8","DS-6"),-1:("GRY-VIO","CN6-P9","DS-7"),0:("GRY-BLK","CN6-P10","DS-8")}[n]
            d["wiring"]={"board":"CPU/Sound Board","drive_wire":wire,"drive_connection":pin,"return_component":"U206"}
            d["aliases"].append({"namespace":"manual.address","value":printed})
        items.append(d)
    for n,label in sorted(chart.items()):
        unused = label == "NOT USED"
        optional = n in {1,8}
        identifier = old[n]["id"] if n in old else f"switch.matrix-{n}"
        if n in {14,15}:
            identifier = "switch.trough-vuk-opto" if n == 14 else "switch.trough-stacking-opto"
        if n == 50:
            identifier = "switch.right-turbo-bumper"
        entry=device(identifier,label.title(),"switch","pinmame.input.switch",n,
                     "unused" if unused else "optional" if optional else "used",(MANUAL,CORE,SCRIPT),
                     aliases=aliases("pinmame.switch",n,old.get(n),str(n)),
                     physical={"notes":f"Factory matrix cell {n}: {label}."})
        col,row=divmod(n-1,8)
        if SWITCH_WIRES[col]:
            wire,conn=SWITCH_WIRES[col]; ret,rconn=ROW_WIRES[row]
            entry["wiring"]={"board":"CPU/Sound Board","driver_transistor":f"Q{col+1}",
              "drive_wire":wire,"drive_connection":conn,"return_wire":ret,"return_connection":rconn}
        if n in {11,12,13}:
            entry["physical"].update({"switch_type":"microswitch","part_number":"180-5119-00"})
            entry["normally_closed"]=False
        if n in points and n not in {14,15}:
            entry["normally_closed"]=False
        if n in {14,15}:
            entry["physical"].update({"switch_type":"opto","assembly_part_number":"500-6318-24",
              "notes":f"Factory cell {n}: {label}. Dual receiver acts open with light and closed with beam blocked; PDF 95–96."})
            entry["normally_closed"]=False
        if n in {11,12,13,14,15}:
            entry["initial_active"]=n != 15
        if n in {11,12,13,14,15}:
            entry["roles"]=["internal.trough"]
        if unused:
            entry["spatial"]=unavailable("unused",MANUAL)
        elif n in {2,3,4,5,6,7,53,54,55,56}:
            entry["physical"]["location"]="cabinet"
            entry["spatial"]=unavailable("cabinet_or_service",MANUAL)
        elif n in points and n not in {14}:
            p=points[n]
            entry["spatial"]=located(identifier,"sensor",[tuple(p["xy"])],TABLE,SCRIPT)
            entry["physical"]["notes"] += f" Observed script-bound {p['type']} {p['object']} ({p['binding']}); a simulation object may approximate the physical contact."
        if n == 14 and n in points:
            p=points[n]; entry["spatial"]=located(identifier,"sensor",[tuple(p["xy"])],TABLE,SCRIPT)
            entry["physical"]["notes"] += " sw14 is the script's release kicker and is a projection of the VUK opto, not modeled opto geometry."
            entry["spatial"]["placements"][0]["provenance"]["source_refs"].append(MANUAL)
        if n == 15 and 14 in points:
            p=points[14]; entry["spatial"]=located(identifier,"sensor",[tuple(p["xy"])],TABLE,SCRIPT,MANUAL)
            entry["physical"]["notes"] += " Upper beam projected onto the VUK anchor on the same dual opto board; exact upper-beam geometry is not modeled."
        items.append(entry)
    names={81:("Synthetic Right Flipper EOS","DS-4"),82:("Right Flipper Button","DS-3"),
           83:("Synthetic Left Flipper EOS","DS-2"),84:("Left Flipper Button","DS-1"),
           85:("Unused Flipper Column 85",None),86:("Unused Flipper Column 86",None),
           87:("Unused Flipper Column 87",None),88:("Unused Dedicated Input DS-5","DS-5")}
    for n,(label,printed) in names.items():
        active=n in {81,82,83,84}
        kind="virtual" if n in {81,83,85,86,87,88} else "switch"
        note=("core_updateSw synthesizes the EOS bit from flipper state." if n in {81,83}
              else "dedswitch_r reads this cabinet flipper button." if n in {82,84}
              else "dedswitch_r selects only the low four flipper bits and bit 7; DS-5 is printed NOT USED.")
        items.append(device(f"switch.flipper-column-{n}",label,kind,"pinmame.input.switch",n,
          "used" if active else "unused",(CORE,MANUAL),aliases=aliases("pinmame.switch",n,old.get(n),printed),
          physical={"notes":note},spatial=unavailable("cabinet_or_service" if n in {82,84} else "virtual",CORE)))
        if n in {82,84}:
            items[-1]["normally_closed"]=False
            items[-1]["provenance"]["source_refs"].append(LIBRARY)
            items[-1]["roles"]=["flipper.lower."+("right" if n==82 else "left")+".button"]
        elif n in {81,83}:
            items[-1]["roles"]=["internal.synthetic-flipper"]
            items[-1]["physical"]["notes"] += " The factory's separate physical EOS contact is normally closed (PDF 92); this public bit is synthesized, so that construction is not assigned to the virtual input."
        if n in {81,82,83,84}:
            wire,pin={81:("GRY-YEL","CN6-P6"),82:("GRY-ORG","CN6-P4"),83:("GRY-RED","CN6-P3"),84:("GRY-BRN","CN6-P2")}[n]
            items[-1]["wiring"]={"board":"CPU/Sound Board","drive_wire":wire,"drive_connection":pin,"return_component":"U206"}
    for n in range(1,9):
        items.append(device(f"dip.sw300-{n}",f"SW300 Position {n}","dip_switch","pinmame.input.dip",n,
          "used" if n <= 4 else "unknown",(CORE,MANUAL),aliases=aliases("pinmame.dip",n),
          physical={"location":"CPU/Sound Board","switch_type":"dip","notes":"Country setting SW300. No listed country turns positions 5–8 on; ROM behavior for other settings is not established."},
          spatial=unavailable("dip_switch",MANUAL)))
    return items


def outputs(base: dict, spatial: dict) -> list[dict]:
    old = {(d["binding"]["group"],d["binding"]["device"]):d for d in base["outputs"]}
    coil = read_coils()
    lamps = read_grid("lamp-matrix-front.md",80)
    effects = {}
    for p in spatial["actuators_and_effects"]:
        effects.setdefault(p["address"],[]).append(p)
    items=[]
    flashers={7,18,19,20,*range(25,33)}
    optional={8,21,22,23,24}
    page=spatial["pages"]["flashers"]
    fit_flash=fit([(c["pixel"],c["xy"]) for c in page["controls"]])
    for n in range(1,51):
        prev=old.get(("pinmame.output.solenoid",n))
        if n <= 32 and n not in {15,16}:
            label,trans,wire,conn,power,pconn,voltage,part=coil[n]
            kind="flasher" if n in flashers else "motor" if n==6 else "magnet" if n in {3,4,5,14} else "coil"
            identifier=prev["id"] if prev else f"device.output-{n}"
            entry=device(identifier,label.title(),kind,"pinmame.output.solenoid",n,
              "optional" if n in optional else "used",(MANUAL,CORE,SCRIPT),
              aliases=aliases("pinmame.solenoid",n,prev,f"#{n}" if n<=24 else f"F{n-24}"),
              physical={"notes":f"Factory chart #{n}: {label}; {part}. {voltage}."},
              wiring={"board":"I/O Power Driver Board","driver_transistor":trans,"control_wire":wire,
                      "control_connection":conn,"power_wire":power,"power_connection":pconn})
            if n == 1:
                entry["physical"].update({"part_number":"26-1200 090-5044-00T","assembly_part_number":"500-6318-24"})
            if n == 6 or n in {8,24}:
                entry["physical"]["location"]="cabinet"
                entry["spatial"]=unavailable("cabinet_or_service",MANUAL)
            elif n in flashers:
                measures=page["measurements"].get(str(n),[])
                entry["physical"]["quantity"]=len(measures)
                entry["spatial"]=located(identifier,"emitter",[apply(fit_flash,m["pixel"]) for m in measures],MANUAL,TABLE,SCRIPT)
                entry["physical"]["notes"]+=" Factory drawing part centers; observed, some extrapolated from controls."
            elif n in effects:
                p=effects[n][0]
                entry["spatial"]=located(identifier,"effect",[tuple(p["xy"])],TABLE,SCRIPT)
                entry["physical"]["notes"]+=f" Projection onto script object {p['object']}, not a measured coil."
            elif n in {9,10,11,12,13}:
                contact={9:49,10:50,11:51,12:59,13:62}[n]
                p=next((point for point in spatial["switches"] if point["address"]==contact),None)
                if p:
                    entry["spatial"]=located(identifier,"effect",[tuple(p["xy"])],TABLE,SCRIPT,MANUAL)
                    entry["physical"]["notes"]+=f" Projection onto the factory-matched bumper or slingshot contact object {p['object']}; coil center is not measured."
            items.append(entry)
        else:
            if n == 15: label,availability="Fast-flip signal (root 2.05 only)","used"
            elif n in {45,47}: label,availability=("Right" if n==45 else "Left")+" Flipper Power Mirror","used"
            elif n in {46,48}: label,availability=("Right" if n==46 else "Left")+" Flipper","used"
            else: label,availability=f"Reserved Output {n}","unused"
            kind="coil" if n in {46,48} else "virtual"
            identifier=prev["id"] if prev and n in {46,48} else f"device.output-{n}"
            notes=("Root godzilla fastflipaddr is configured by se.c; clone names godz_100 and godz_090 do not match, so they lack this signal." if n==15
                   else "se_solenoid_w moves physical Q16/Q15 to 45/47 and core supplies the companion 46/48 callback. The two public addresses are views of one physical flipper."
                   if n in {45,46,47,48} else "Godzilla INITGAME hardware selector is 0; no aux board handler is selected and this reserved output has no game-specific producer.")
            entry=device(identifier,label,kind,"pinmame.output.solenoid",n,availability,(CORE,MANUAL),
              aliases=aliases("pinmame.solenoid",n,prev),physical={"notes":notes},
              spatial=unavailable("virtual",CORE) if kind=="virtual" else None)
            if kind=="coil":
                entry.pop("spatial")
                entry["provenance"]["source_refs"].append(CORE_LIBRARY)
                entry["roles"]=["flipper.lower."+("right" if n==46 else "left")]
                p=effects.get("sLRFlipper" if n==46 else "sLLFlipper",[])
                if p: entry["spatial"]=located(identifier,"effect",[tuple(p[0]["xy"])],TABLE,SCRIPT)
                row=coil[16 if n==46 else 15]
                entry["wiring"]={"board":"I/O Power Driver Board","driver_transistor":row[1],"control_wire":row[2],
                   "control_connection":row[3],"power_wire":row[4],"power_connection":row[5]}
                entry["physical"]["part_number"]=row[7]
            items.append(entry)
    page=spatial["pages"]["lamps"]
    transform=fit([(c["pixel"],c["xy"]) for c in page["controls"]])
    for n,label in lamps.items():
        prev=old.get(("pinmame.output.lamp",n))
        unused=label=="NOT USED"
        identifier=prev["id"] if prev else f"lamp.matrix-{n}"
        entry=device(identifier,label.title(),"lamp","pinmame.output.lamp",n,
          "unused" if unused else "optional" if n==40 else "used",(MANUAL,CORE,SCRIPT),
          aliases=aliases("pinmame.lamp",n,prev,str(n)),
          physical={"notes":f"Factory lamp cell {n}: {label}." +
                    (" No load is fitted at this printed unused position." if unused else
                     f" {'#44' if n in {28,32} else '#555'} bulb; factory drawing coordinates are calibrated by retained-table mechanism controls.")})
        row,col=divmod(n-1,8)
        if row<7:
            drv,wire,conn=LAMP_COLUMNS[col]; transistor,rwire,rconn=LAMP_ROWS[row]
            entry["wiring"]={"board":"I/O Power Driver Board","driver_transistor":drv+" / "+transistor,
                "drive_wire":wire,"drive_connection":conn,"return_wire":rwire,"return_connection":rconn}
        measures=page["measurements"].get(str(n),[])
        if measures:
            entry["physical"]["quantity"]=len(measures)
            entry["spatial"]=located(identifier,"emitter",[apply(transform,m["pixel"]) for m in measures],MANUAL,TABLE,SCRIPT)
        elif n==8:
            entry["physical"].update({"quantity":1,"location":"cabinet launch button"})
            entry["spatial"]=unavailable("cabinet_or_service",MANUAL)
        elif unused:
            entry["spatial"]=unavailable("unused",MANUAL)
        items.append(entry)
    giold=old.get(("pinmame.output.gi",0))
    items.append(device("gi.relay","General Illumination Relay","gi","pinmame.output.gi",0,"used",(MANUAL,CORE),
       aliases=aliases("pinmame.gi",0,giold),physical={"quantity":38,"notes":"Four fused circuits behind one GI relay: nominal 36 playfield bulbs and two coin-door bulbs; the manual notes production quantities can vary. Socket positions remain unknown."}))
    return items


def mechanisms(inputs: list[dict], outputs_: list[dict]) -> list[dict]:
    ins={d["binding"]["device"]:d["id"] for d in inputs if d["binding"]["group"]=="pinmame.input.switch"}
    outs={d["binding"]["device"]:d["id"] for d in outputs_ if d["binding"]["group"]=="pinmame.output.solenoid"}
    def mech(identifier,label,kind,acts,sensors,behavior,part=None):
        d={"id":"mechanism."+identifier,"label":label,"kind":kind,"actuators":[outs[n] for n in acts],
           "sensors":[ins[n] for n in sensors],"behavior":behavior,"provenance":provenance(MANUAL,SCRIPT)}
        if part: d["assembly_part_number"]=part
        return d
    result=[
      mech("trough","Four-ball trough and serve","kicker",[1],[11,12,13,14,15,16],
           "Three roller contacts plus lower VUK and upper stacking optos. Initial ball occupancy holds 11–14 active and 15 clear. Output 1 kicks the VUK ball to the shooter lane; contacts follow ball motion, not a direct coil-to-switch wire.","500-6318-24"),
      mech("auto-launch","Shooter lane auto launch","kicker",[2],[16,53],"The shooter lane switch senses the ball; the launch button requests output 2 to launch it."),
      mech("ramp-diverter","Godzilla ramp diverter","diverter",[17],[],
           "The script alternates Diverter1 and Diverter2 collision walls when output 17 changes. The manual states a hard Godzilla ramp shot goes left return with diverter UP and out the mouth when DOWN; the wall flag is not an independently proven physical UP mapping."),
      mech("captive-balls","Three captive balls","other",[],[41,42,43,44],
           "Three captive balls occupy separate lanes. A hit to either outer captive ball knocks the top center captive ball between its posts."),
      mech("shaker","Cabinet shaker","motorized",[6],[],"The cabinet-bottom shaker motor is driven by output 6. The VPW callback produces shaker sound; its timing is table tuning, not a motor measurement.")]
    result.append(mech("uk-posts","Optional UK post-save devices","other",[21,22,23],[1,8],
        "The factory chart lists left and right outlane save devices and an up/down post for UK only. Adjustment 51 requires the UK EPROM. Physical home state, device causality and timing are not established."))
    result.append(mech("token-dispenser","Optional European token dispenser","other",[8],[],
        "The factory chart reserves output 8 for the optional European token dispenser and lists its part as Various (Call). Attachment topology, feedback and payout timing are not established; no absent attachment is simulated by assumption."))
    for n,name in ((3,"top-orbit"),(4,"middle-playfield"),(5,"bottom-playfield"),(14,"left-lane")):
        result.append(mech("magnet-"+name,name.replace("-"," ").title()+" Magnet","other",[n],[],
            "A 22-650 magnet coil uses a threaded bushing core; the retained table binds a separate magnet object to this output. No dedicated feedback sensor is established.","515-6142-01"))
    return result


def build() -> bytes:
    if AUTHOR_READY.exists():
        raise ValueError(f"Refusing to overwrite an author-ready definition: {AUTHOR_READY}")
    base=load_json(SEED)
    if SEED.read_bytes()!=canonical_bytes(base):
        raise ValueError(f"Seed is not in canonical byte format: {SEED}")
    if base["machine"]["id"]!="sega.godzilla.1998" or base["coverage"]["status"]!="partial":
        raise ValueError("Godzilla seed must identify the partial machine")
    for name,digest in EXCERPT_HASHES.items():
        if sha256(EXCERPT_DIR/name)!=digest:
            raise ValueError(f"Changed excerpt: {name}")
    spatial=load_json(SPATIAL_SEED)
    if sha256(SPATIAL_SEED) != SPATIAL_SHA256 or SPATIAL_SEED.read_bytes() != canonical_bytes(spatial):
        raise ValueError("Spatial seed has changed or is not canonical")
    for page in spatial["pages"].values():
        pairs=[(c["pixel"],c["xy"]) for c in page["controls"]]
        affine=fit(pairs)
        if any(abs(a-b)>1e-9 for row1,row2 in zip(affine,page["affine"]) for a,b in zip(row1,row2)):
            raise ValueError("Factory control fit differs from recorded affine")
        if any(abs(a-b)>1e-9 for a,b in zip(leave_one_out(pairs),page["control_leave_one_out"])):
            raise ValueError("Factory control leave-one-out values differ")
    verify_configured_evidence(spatial)
    base["sources"]=source_records(base)
    base["schema_version"]=2
    base["machine"]["model_number"]="40"
    base["machine"]["playfield"]={"width":952,"height":2206.5,"units":"vpx","provenance":provenance(TABLE)}
    base["controller"]["platform"]="pinmame.whitestar"
    for driver in base["drivers"]:
        driver["physical_compatibility"]="unknown" if driver["id"]=="godz_090" else "identical"
        driver["variant_notes"]=("Shared GEN_WS driver initialization proves routing; prototype physical compatibility remains unknown." if driver["id"]=="godz_090" else
          "Production hardware; shared GEN_WS initialization. "+("Root 2.05 exposes fast-flip 15." if driver["id"]=="godzilla" else "Clone name does not receive se.c root fast-flip address 15; flipper callbacks remain available."))
    base["inputs"]=matrix_inputs(base,spatial)
    base["outputs"]=outputs(base,spatial)
    # These runs corroborate controller responses. They do not establish optional
    # load fitment or independently validate a physical device's coordinates.
    runtime_refs = [record[0] for record in RUNTIME_EVIDENCE.values()]
    for entry in base["outputs"]:
        if entry["binding"]["group"] == "pinmame.output.solenoid" and entry["binding"]["device"] in {1,2,9,10,11,12,13,15,24,45,46,47,48}:
            entry["provenance"]["source_refs"].extend(runtime_refs)
    base["displays"]=[{"id":"display.dmd","label":"128x32 dot-matrix display","kind":"dmd","controller_index":0,
      "width":128,"height":32,"provenance":provenance(CORE,MANUAL),"spatial":unavailable("cabinet_or_service",MANUAL)}]
    base["mechanisms"]=mechanisms(base["inputs"],base["outputs"])
    base["coverage"]["missing"]=["input_semantics","output_semantics","mechanism_behavior","polarity","variant_differences","recreation_notes","provenance","spatial_placement"]
    base["coverage"]["dimensions"].update({"catalog_identity":"validated","address_enumeration":"observed","physical_wiring":"observed",
      "semantic_naming":"observed","mechanisms":"observed","spatial_placement":"observed"})
    return canonical_bytes(base)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--regenerate",action="store_true")
    args=parser.parse_args()
    if args.check == args.regenerate:
        parser.error("choose exactly one of --check or --regenerate")
    try:
        payload=build()
        if args.check:
            if not PARTIAL.is_file() or PARTIAL.read_bytes()!=payload:
                raise ValueError(f"Partial definition differs from curator: {PARTIAL}")
            for destination, seed in TEXT_ARTIFACTS.items():
                if not destination.is_file() or destination.read_bytes() != seed.read_bytes():
                    raise ValueError(f"Text artifact differs from curator seed: {destination}")
            print("Godzilla partial definition matches curator")
        else:
            PARTIAL.write_bytes(payload)
            for destination, seed in TEXT_ARTIFACTS.items():
                destination.write_bytes(seed.read_bytes())
            print(f"Wrote {PARTIAL}")
    except (OSError,ValueError,KeyError,StopIteration) as exc:
        parser.exit(1,f"{exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
