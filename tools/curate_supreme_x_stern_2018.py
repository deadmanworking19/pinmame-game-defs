"""Verify Supreme's reviewed VPX mapping and reproduce its partial artifacts."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.jsonio import file_sha256, load_json
from pinmame_game_defs.spatial import extract_spatial_candidates
from supreme_shared_evidence import verify_contract

GAME = "supreme_101"
ROOT = Path(__file__).resolve().parents[1]
MAPPING = "tools/seeds/stern/supreme-x-stern-2018-vpx-008.json"
VPX = "stern/supreme-x-stern-2018/supreme_008.vpx"
EXTRACTION = "stern/supreme-x-stern-2018/supreme_008"
VPX_SHA256 = "444c21186425f23c173dece87fe9f683e2ee5c101e76271bf1d2339d1920edd9"
SCRIPT_SHA256 = "f2bb8a48bd0aa49310d7e7e8bc165757d59d168110815ac1712dcc971e7a34ca"
MANIFEST_SHA256 = "9f4af73ce3091bde3c61ff734feb92a3ec48f113d57327bc8142e2b6905b41bb"


def placements(mapping):
    for collection, key, role in (("inputs", "input_placements", "sensor"), ("outputs", "output_placements", "effect")):
        for identifier, entries in mapping[key].items():
            for entry in entries:
                yield collection, identifier, role, entry


def verify_external_evidence(root=ROOT):
    """An absent optional root skips; a declared root must prove the exact inputs."""
    raw = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if not raw:
        return
    source_root = Path(raw)
    extraction = source_root / EXTRACTION
    vpx = source_root / VPX
    if file_sha256(vpx) != VPX_SHA256 or file_sha256(extraction / "script.vbs") != SCRIPT_SHA256:
        raise ValueError("Supreme retained VPX/script hash mismatch")
    if check_manifest(extraction, GAME) != MANIFEST_SHA256:
        raise ValueError("Supreme extraction manifest differs from reviewed evidence")
    manifest = load_json(extraction / "manifest.json")
    if len(manifest["files"]) != 565 or sum(row["size"] for row in manifest["files"]) != 64800271:
        raise ValueError("Supreme extraction inventory changed")
    candidates = extract_spatial_candidates(extraction, vpx, "git:v0.33.3")
    if candidates["bounds"] != {"left": 0, "top": 0, "right": 952.9, "bottom": 2117.6}:
        raise ValueError("Supreme VPX bounds changed")
    objects = {f"{row['type']}.{row['name']}": row for row in candidates["objects"]}
    mapping = load_json(root / MAPPING)
    for _, identifier, _, entry in placements(mapping):
        components = [objects[name] for name in entry["object"].split("+")]
        actual = {axis: round(sum(p[axis] for p in components) / len(components), 6) for axis in ("x", "y")}
        if actual != {axis: entry[axis] for axis in ("x", "y")}:
            raise ValueError(f"{identifier}/{entry['object']}: retained coordinate differs: {actual}")
    lights = list((extraction / "gameitems").glob("Light.*.json"))
    if not lights or any(load_json(path)["Light"].get("show_bulb_mesh") is not False for path in lights):
        raise ValueError("Supreme lamp evidence needs renewed bulb/socket review")


def enrich_spatial_report(root, definition, report):
    """Add the title's explicit object/projection audit to the common inventory."""
    shared = verify_contract(root, definition)
    mapping = load_json(root / MAPPING)
    verify_external_evidence(root)
    sources = {source["id"]: source for source in definition["sources"]}
    for source in mapping["sources"]:
        if sources.get(source["id"]) != source:
            raise ValueError(f"{source['id']}: reviewed source metadata drift")
    devices = {(collection, d["id"]): d for collection in ("inputs", "outputs") for d in definition[collection]}
    located = {key for key, device in devices.items() if device.get("spatial", {}).get("placements")}
    expected_located = {(collection, identifier) for collection, identifier, _, _ in placements(mapping)}
    if located != expected_located:
        raise ValueError("Supreme located-device inventory differs from reviewed mapping")
    mechanisms = {mechanism["id"]: mechanism for mechanism in definition["mechanisms"]}
    for identifier, addendum in mapping["mechanism_behavior_addenda"].items():
        if addendum not in mechanisms[identifier]["behavior"]:
            raise ValueError(f"{identifier}: reviewed VPX behavior addendum missing")
    observed = []
    for collection, identifier, role, entry in placements(mapping):
        spatial = devices[collection, identifier].get("spatial", {})
        expected = {"id": entry["id"], "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
                    "provenance": {"status": "observed", "source_refs": ["supreme.vpx.table.008", "supreme.vpx.script.008"]}}
        if spatial.get("status") != "observed" or expected not in spatial.get("placements", []):
            raise ValueError(f"{identifier}: canonical placement drift")
        observed.append({"collection": collection, "device_id": identifier, **entry, "role": role})
    for collection, key in (("inputs", "input_placements"), ("outputs", "output_placements")):
        for identifier, entries in mapping[key].items():
            if len(devices[collection, identifier]["spatial"]["placements"]) != len(entries):
                raise ValueError(f"{identifier}: unexpected extra placement")
    report["decision"]["reason"] = "Observed VPX sensor/effect proxies and verified backbox display; physical wiring, gate action, lighting sockets and cabinet fitment remain incomplete."
    report["observed_placements"] = observed
    report["projection_classes"] = sorted({row.get("projection", "bound_object_center") for row in observed})
    report["shared_design"] = {
        "authority_limit": shared["authority_limit"],
        "counts": {key: value["counts"] for key, value in shared["sections"].items()},
        "supreme_only_switch_routes": shared["sections"]["switches"]["supreme_only"],
        "donor_only_switch_routes": shared["sections"]["switches"]["spiderman_only"],
    }
    report["retained_vpx"] = {"path": VPX, "sha256": VPX_SHA256, "script_sha256": SCRIPT_SHA256,
                              "manifest_sha256": MANIFEST_SHA256, "file_count": 565, "total_bytes": 64800271,
                              "bounds": {"left": 0, "top": 0, "right": 952.9, "bottom": 2117.6}}
    return report


def report_markdown(report):
    import curate_spike1
    text = curate_spike1.report_markdown(report)
    text = text.replace("None declared by the schema-valid seed; no class or coordinate was inferred.",
                        ", ".join(f"`{name}`" for name in report["projection_classes"]))
    text += "\n## Retained geometry and projection audit\n\n"
    retained = report["retained_vpx"]
    text += (f"VPX SHA-256 `{retained['sha256']}`; script `{retained['script_sha256']}`; "
             f"complete extraction manifest `{retained['manifest_sha256']}` ({retained['file_count']} files, {retained['total_bytes']} bytes). "
             "Bounds: left=0, top=0, right=952.9, bottom=2117.6. Coordinates use (x-left)/(right-left), (y-top)/(bottom-top), six decimals.\n\n")
    text += "| Device | Bound object | x | y | Coordinate role |\n| --- | --- | --- | --- | --- |\n"
    for row in report["observed_placements"]:
        text += f"| {row['device_id']} | {row['object']} | {row['x']} | {row['y']} | {row.get('projection', 'bound_object_center')} |\n"
    text += ("\nAll listed points are observed recreation proxies. Slings use wall drag-point centroids; "
             "the reset output uses the mean of the three drop-wall centroids; flipper effects use pivots. "
             "Bumper output positions project onto the corresponding bumper centers. These do not measure under-playfield coils. "
             "The guessed control-gate coil-on direction remains unresolved. No trough, cabinet or service location is invented. "
             "Insert/lightmap and GI render helpers do not establish emitter sockets, quantities or string membership, so lamp placements remain absent. "
             "The independently photographed backbox display uses cabinet_or_service. See the knowledge note and physical-web-research excerpt for primary rule-card and photo evidence.\n")
    text += "\n## Shared-design comparison and completed driver mapping\n\n"
    text += report["shared_design"]["authority_limit"] + "\n\n"
    text += "| Routing table | Shared routes | Supreme only | Donor only | Reconciled donor manual rows |\n| --- | --- | --- | --- | --- |\n"
    for name, counts in report["shared_design"]["counts"].items():
        text += f"| {name} | {counts['shared']} | {counts['supreme_only']} | {counts['spiderman_only']} | {counts['manual_matched']} |\n"
    text += ("\nSwitch rows include nine CPU C-namespace references. Donor tilt 14 at node 8/27 and launch 15 at node 8/26 "
             "move to Supreme node 1/14 and node 1/15, so public-number agreement does not justify copying their wiring. "
             "Eight other Supreme cabinet switch routes have no donor route. Three node 1 coil routes and four node 1 LED routes "
             "remain physically unconfirmed, including the cabinet/playfield collisions at lamp 1/2/3. "
             "Full literal donor rows and all route exceptions are retained in shared-design-crosswalk.json.txt. "
             "The donor assembly lists are candidate references, not Supreme part-number or quantity assignments.\n\n"
             "The sole supported Supreme driver is mapped to its physical record and all ten ROM payloads independently match "
             "the pinned current source manifest. This resolves driver_mapping; physical compatibility, variant differences, "
             "contact polarity, wiring, cabinet fitment and complete placement remain unresolved. See driver-map-identity.json.txt "
             "and current-driver-identity.md for the exact archive/source proof.\n")
    return text


def check(root=ROOT):
    import curate_spike1
    curate_spike1.check(GAME, root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    import curate_spike1
    curate_spike1.run(GAME, args.regenerate, ROOT)


if __name__ == "__main__":
    main()
