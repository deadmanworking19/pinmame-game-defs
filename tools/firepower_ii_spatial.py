"""Pinned spatial continuation; physical facts and public bindings stay in the curator."""
from __future__ import annotations

import copy
import hashlib
import math
from collections import Counter
from pathlib import Path
from typing import Any

import drawing_callouts as drawing
from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.spatial import _round_point

SEED = Path("tools/seeds/williams/firepower-ii-1983-spatial.json")
SEED_SHA = "c69ff28e00f35760f1a0f4e50087f0d7fe91b9323ce21efd137a3db324a22206"
EXCERPT = Path("evidence/excerpts/williams.firepower-ii.1983/spatial-method.md")
EXCERPT_SHA = "681c2491037ebd2fb70a300a5715920797b344bc42e6df81515dc65543355c34"
RETENTION_SHA = "9c3eba2a39e77ff90a6cc62c341ad330f44be59c1a9fea9d9b2179dd1338af17"
SESSION = Path("williams.firepower-ii.1983/session-20261030-spatial")
TABLE = "geometry.firepower-ii-1-1"
SCRIPT = "script.firepower-ii-embedded-1-1"
MANUAL = "manual.firepower-ii-spatial"
MACHINE_ID = "williams.firepower-ii.1983"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_seed(root: Path) -> dict[str, Any]:
    for path, digest in [(SEED, SEED_SHA), (EXCERPT, EXCERPT_SHA)]:
        if not (root / path).is_file() or sha(root / path) != digest:
            raise RuntimeError(f"spatial evidence absent or changed: {path}")
    return load_json(root / SEED)


def normalized(seed: dict[str, Any], raw: tuple[float, float]) -> tuple[float, float]:
    b = seed["table"]["bounds"]
    point = ((raw[0] - b["left"]) / (b["right"] - b["left"]),
             (raw[1] - b["top"]) / (b["bottom"] - b["top"]))
    if not all(0 <= v <= 1 for v in point):
        raise ValueError(f"out-of-range source point: {raw}")
    return tuple(_round_point(v) for v in point)


def object_point(seed: dict[str, Any], name: str, method: str = "center") -> tuple[float, float]:
    if method == "world_bounds":
        bounds = seed["world_obj"]["bounds"][name]
        return tuple((a + b) / 2 for a, b in zip(bounds["minimum"][:2], bounds["maximum"][:2]))
    fields = seed["objects"][name]["fields"]
    if method == "drag_point_centroid":
        pts = fields["drag_points"]
        return tuple(sum(p[a] for p in pts) / len(pts) for a in ["x", "y"])
    if method == "slingshot_edge_midpoint":
        pts = fields["drag_points"]
        edges = [(p, pts[(i + 1) % len(pts)]) for i, p in enumerate(pts) if p["is_slingshot"]]
        if len(edges) != 1:
            raise ValueError(f"expected one active sling edge: {name}")
        return tuple((edges[0][0][a] + edges[0][1][a]) / 2 for a in ["x", "y"])
    if seed["objects"][name]["type"] == "Primitive":
        raise ValueError(f"primitive needs world bounds: {name}")
    point = fields.get("center", fields.get("position"))
    return tuple(point[a] for a in ["x", "y"])


def callout_seed(seed: dict[str, Any]) -> tuple[dict[str, Any], dict[str, tuple[float, float]]]:
    """Reconcile table candidates, never a measurement against its own drawing."""
    pages = copy.deepcopy(seed["pages"])
    checks, candidates = {}, {}
    for key, page in pages.items():
        excluded = {label for printed in page.get("excluded", {}) for label in drawing.labels(printed)}
        for read in page.get("excluded_reads", []):
            if not set(drawing.labels(read["label"])) <= excluded:
                raise ValueError(f"{key}: excluded raw observation lacks an explicit exclusion")
        if any(excluded.intersection(drawing.labels(r["label"])) for r in page["reads"]):
            raise ValueError(f"{key}: excluded/regional read cannot enter a precise callout fit")
        for c in page["controls"]:
            c["xy"] = list(normalized(seed, object_point(seed, c["object"])))
        for r in page["reads"]:
            r["point"] = "symbol_centre" if key == "pdf-14" else "label_beside_part"
    for spec in seed["specs"]:
        group, n = spec["group"], spec["address"]
        page = {"lamp": "pdf-14", "switch": "pdf-17", "solenoid": "pdf-15"}[group]
        if str(n) not in {r["label"] for r in pages[page]["reads"]}:
            continue
        pid = f"reconcile.{group}-{n}"
        # Fifty lamp coordinates are drawing measurements. These extra IDs check
        # their table proxies only and can never promote those measured placements.
        method = "center" if spec["method"] == "drawing_symbol" else spec["method"]
        candidates[pid] = normalized(seed, object_point(seed, spec["object"], method))
        checks[pid] = {"page": page, "label": str(n)}
    return {"format": drawing.FORMAT, "machine_id": MACHINE_ID, "pages": pages, "checks": checks}, candidates


def outside_controls(page: dict[str, Any], point: tuple[float, float]) -> bool:
    """Convex hull, not bounding box; source points beyond it stay observed."""
    points = sorted(set(tuple(c["xy"]) for c in page["controls"]))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    return any(cross(a, b, point) < -1e-9 for a, b in zip(hull, hull[1:] + hull[:1]))


def geometry(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    seed = read_seed(root)
    calls, candidates = callout_seed(seed)
    decisions = drawing.evaluate(calls, candidates)
    rows = []
    for spec in seed["specs"]:
        page_key = {"lamp": "pdf-14", "switch": "pdf-17", "solenoid": "pdf-15"}[spec["group"]]
        page = calls["pages"][page_key]
        measured = spec["method"] == "drawing_symbol"
        if measured:
            pixel = next(r["pixel"] for r in page["reads"] if r["label"] == str(spec["address"]))
            transform = drawing.fit([(tuple(c["pixel"]), tuple(c["xy"])) for c in page["controls"]])
            xy = tuple(round(v, 3) for v in drawing.apply(transform, pixel))
        else:
            xy = normalized(seed, object_point(seed, spec["object"], spec["method"]))
            pixel = None
        extrapolated = outside_controls(page, xy)
        decision = decisions["placements"].get(f"reconcile.{spec['group']}-{spec['address']}")
        # Assembly projections and measurements without a second independent
        # drawing remain observed even when the neighboring proxy agrees.
        direct = spec["classification"] in {"direct_sensor", "bulb_mesh"}
        status = "validated" if direct and not extrapolated and decision and decision["agrees"] else "observed"
        rows.append({**spec, "placement_id": f"placement.{spec['group']}-{spec['address']}",
                     "x": xy[0], "y": xy[1], "page": page_key, "pixel": pixel,
                     "extrapolated": extrapolated, "status": status,
                     "coordinate_source": "factory lamp-location symbol" if measured else "world-space OBJ bounds" if spec["method"] == "world_bounds" else "retained table geometry",
                     "reconciliation_excluded_reason": page.get("excluded", {}).get(str(spec["address"])),
                     "reconciliation": decision})
    return seed, decisions, rows


def export_controls(seed: dict[str, Any]) -> list[dict[str, Any]]:
    controls = []
    for name in ["Bumper1", "Bumper2", "Bumper3", "Bumper4"]:
        raw = object_point(seed, name)
        mesh = object_point(seed, name + "Base", "world_bounds")
        offset = math.dist(normalized(seed, raw), normalized(seed, mesh))
        if offset > 0.001:
            raise RuntimeError(f"world export axes/scale fail geometry control: {name}")
        controls.append({"object": name, "table_center": list(raw), "exported_base_bounds_center": list(mesh), "normalized_offset": round(offset, 6)})
    return controls


def source_records(root: Path, manual: dict[str, Any], seed: dict[str, Any]) -> list[dict[str, Any]]:
    t = seed["table"]
    excerpt = {"id": "excerpt.firepower-ii-spatial", "path": EXCERPT.as_posix(), "sha256": EXCERPT_SHA,
               "locator": "PDF14 Figure2; PDF15 Figure5; PDF17 Figure4; exact retained table and embedded script",
               "method": "manual", "transcribed_by": "Primary curator; independent native drawing reads and source inspection", "reviewed": True}
    common = {"license": "NOASSERTION", "attribution": "Goldchicco and Apophis, based on Walamab; geometry measured by primary curator",
              "rights": "Source-owned community table retained externally; no redistribution permission asserted.",
              "acquired_at": t["acquired_at"], "revision": "Goldchicco/Apophis 1.1, September 2021; vpxtool git:v0.33.3",
              "excerpts": [excerpt], "known_working": False}
    return [
        {**common, "id": TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/" + t["path"] + "/" + t["filename"],
         "sha256": t["sha256"], "original_filename": t["filename"],
         "locator": "User supplied read-only table; exact acquisition URL unknown. Bounds (0,0)-(1000,2000); extraction manifest " + t["manifest_sha256"] + "; raw selected fields/native reads in repo:" + SEED.as_posix() + "; exported world OBJ " + seed["world_obj"]["sha256"]},
        {**common, "id": SCRIPT, "kind": "vpx_script", "sha256": t["script_sha256"],
         "uri": "external:pinmame-vpx-sources/" + t["path"] + "/extracted/script.vbs",
         "locator": "Windows-1252 embedded script: cGameName fpwr2_l2; callbacks45-53, GI149-157, flasher168-174, ballstack210-218, switches287-355/394-419, lamps475-533; dampener1602 differs from corpus1603/1605. Successful launch not claimed."},
        {**manual, "id": MANUAL, "locator": "PDF14/15/17 native renders: independently read controls, lamp symbols and switch/coil part callouts. Tight native crops retained outside Git; hashes, crop boxes and all pixel readings in repo:" + SEED.as_posix(), "excerpts": [excerpt]},
    ]


def apply(definition: dict[str, Any], root: Path) -> dict[str, Any]:
    seed, _, rows = geometry(root)
    groups = {"switch": "pinmame.input.switch", "lamp": "pinmame.output.lamp", "solenoid": "pinmame.output.solenoid"}
    devices = {(d["binding"]["group"], d["binding"]["device"]): d for k in ["inputs", "outputs"] for d in definition[k]}
    for row in rows:
        d = devices[groups[row["group"]], row["address"]]
        refs = [TABLE, SCRIPT, MANUAL]
        if (row["group"] in {"lamp", "switch"} and row["address"] in {41,42,43,44}) or (row["group"] == "solenoid" and row["address"] in {19,20,21,22}):
            refs.append("photo.firepower-ii-50035")
        if (row["group"] == "lamp" and row["address"] in {52,53,54,55}) or (row["group"] == "switch" and row["address"] == 23) or (row["group"] == "solenoid" and row["address"] == 3):
            refs.append("photo.firepower-ii-50042")
        if row["group"] == "lamp" and row["address"] == 6:
            refs.extend(["photo.firepower-ii-50038", "manual.firepower-ii-insert-board"])
        p = {"id": row["placement_id"], "role": "sensor" if row["group"] == "switch" else "emitter" if row["group"] == "lamp" else "effect",
             "space": "playfield", "x": row["x"], "y": row["y"], "provenance": {"status": row["status"], "source_refs": refs}}
        d["spatial"] = {"status": row["status"], "placements": [p]}
        physical = d.setdefault("physical", {})
        if row["group"] == "lamp":
            # Only the playfield member is placed. A possible parallel backbox
            # load prevents quantity=1 on public 6.
            if row["address"] != 6:
                physical["quantity"] = 1
            physical["notes"] = physical["notes"].replace("Bulb count and exact center need geometry/physical-image review; render doubles do not prove additional bulbs.",
                "Figure 2 has one located lamp symbol; the placement is its playfield-plane projection. Render doubles do not add physical bulbs.")
        note = f" Spatial: {row['classification'].replace('_', ' ')} from {row['coordinate_source']}; object {row['object']}, {row['method']}; see the spatial report."
        if row["extrapolated"]:
            note += " Outside the mechanical controls' convex hull; remains observed."
        if row["group"] == "switch" and row["address"] == 40:
            note += " OrbitGate uses its baked world mesh bounds, not its stored origin or the script's broad Trigger1 helper. This is an assembly projection, not a measured contact."
        physical["notes"] += note
    for d in devices.values():
        if d["id"] in seed["unplaced"]:
            d.setdefault("physical", {})["notes"] += " Spatial unresolved: " + seed["unplaced"][d["id"]]
    definition["machine"]["playfield"] = {"width": 1000, "height": 2000, "units": "vpx",
        "provenance": {"status": "validated", "source_refs": [TABLE]}}
    definition["coverage"]["dimensions"]["spatial_placement"] = "observed"
    definition["sources"].extend(source_records(root, next(s for s in definition["sources"] if s["id"] == "manual.firepower-ii"), seed))
    return definition


def report(definition: dict[str, Any], root: Path) -> dict[str, Any]:
    seed, decisions, rows = geometry(root)
    by_binding = {(d["binding"]["group"].rsplit(".", 1)[-1], d["binding"]["device"]): d["id"] for k in ["inputs", "outputs"] for d in definition[k]}
    for row in rows:
        row["device_id"] = by_binding[row["group"], row["address"]]
    counts = Counter(row["group"] for row in rows)
    missing = sorted(d["id"] for k in ["inputs", "outputs"] for d in definition[k] if "spatial" not in d)
    if set(missing) != set(seed["unplaced"]):
        raise RuntimeError("spatial unresolved-device accounting differs from the definition")
    unbound = copy.deepcopy(seed["unbound_gi"])
    unbound["render_light_geometry"] = [{"object": name,
        "raw_center": list(object_point(seed, name)), "normalized_center": list(normalized(seed, object_point(seed, name))),
        "show_bulb_mesh": seed["objects"][name]["fields"]["show_bulb_mesh"],
        "role": "unbound rendering geometry; no stock socket or branch assertion"} for name in unbound["lights"]]
    unbound["model_bulb_geometry"] = [{"object": name,
        "world_bounds_center": list(object_point(seed, name, "world_bounds")),
        "normalized_center": list(normalized(seed, object_point(seed, name, "world_bounds"))),
        "role": "visible model bulb; public binding and stock wiring unverified"} for name in unbound["model_bulb_primitives"]]
    return {"format": "pinmame-spatial-blockers", "version": 2, "machine_id": MACHINE_ID, "decision": "partial",
            "coordinate_convention": "x 0 left / 1 right; y 0 rear / 1 apron, player view; VPX normalized with shared six-decimal rounding; manual readings three decimals",
            "table_geometry": {**seed["table"], "retention_sha256": RETENTION_SHA}, "world_obj": seed["world_obj"],
            "extraction_manifest": {"algorithm": "tools/build_external_evidence_manifest.py canonical sorted POSIX path/size/SHA256 entries, compact sorted-key JSON plus LF; exclude only manifest.json/manifest.sha256", "sha256": seed["table"]["manifest_sha256"], "file_count": seed["table"]["file_count"], "byte_count": seed["table"]["byte_count"]},
            "drawing_seed": {"path": SEED.as_posix(), "sha256": SEED_SHA}, "manual": {"sha256": "c601834cd57c8cf01423355304d487f3143d92ef1374187344d264eab7e6e6d8", "pages": seed["pages"], "read_corrections": seed["read_corrections"], "correction_crops": seed["correction_crops"], "correction_review": seed["correction_review"]},
            "reconciliation_rule": "Independent native pixel reads; one-to-one labels and two affine fits using drawing_callouts at 0.07 normalized. Table proxy checks never validate manual measurements on the same page. Assembly projections and convex-hull extrapolations remain observed.",
            "layout_photo_refs": ["photo.firepower-ii-50035", "photo.firepower-ii-50038", "photo.firepower-ii-50042"],
            "reconciliation": decisions, "export_geometry_controls": export_controls(seed), "counts": dict(sorted(counts.items())), "placements": rows,
            "unplaced_devices": missing, "unplaced_reasons": seed["unplaced"],
            "not_applicable": {d["id"]: d["spatial"]["reason"] for k in ["inputs", "outputs", "displays"] for d in definition[k] if d.get("spatial", {}).get("status") == "not_applicable"},
            "unbound_gi_geometry": unbound,
            "rejected_geometry": {"Light62": seed["unplaced"]["flasher.orbit-complete-flash-lamps"], "Trigger1": "Broad routing helper; switch40 is only an observed projection onto the actual animated OrbitGate world mesh.", "L41-L44": "Render doubles; use each corresponding a-member showing its own bulb mesh.", "L6-L39/L45-L60": "No own bulb mesh; table insert overlays are reconciliation candidates, not socket coordinate sources.", "OrbitGate.position": "Stored origin differs from baked world bounds; never used as a coordinate."},
            "transport_holes": {"solenoid": [*range(26, 45), 49, 50], "switch": [*range(-2, 1), *range(65, 81)], "dip": list(range(3, 9))},
            "blockers": ["Stock GI sockets per branch and individual Type 83 orbit-flash bulbs remain unidentified/unplaced; table GI grouping is not a factory inventory and System 7 supplies no separate GI callback.", "Ball-ramp sensors10/11 and playfield tilt49 lack defensible individual contact geometry; exact reasons are enumerated.", "Ball in Play public6/40 physical routing remains conflicted, including a possible parallel backbox load on6; table omission of40 and runtime transitions settle no socket wiring.", "Drawing measurements, assembly projections, extrapolations and failed drawing checks remain observed. The supplied table has no confirmed successful launch/play report."]}


def report_markdown(report: dict[str, Any]) -> str:
    counts = report["counts"]
    return ("# Firepower II (1983) spatial continuation\n\nCoverage remains **partial**. "
            f"Located {counts['switch']} switch sensors/projections, {counts['solenoid']} controlled-device effects and {counts['lamp']} playfield emitters. "
            "The detailed JSON records each coordinate source, projection, extrapolation, drawing check and unresolved device.\n\n"
            + "\n".join("- " + s for s in report["blockers"]) + "\n\n"
            + "Native drawing crops, grid inspections and the world-space OBJ remain in the external spatial session; the original table and full extraction are immutable. "
            + "The measurement seed pins every source/transform. Fifty lamp-symbol projections are measured on Figure 2; four bumper emitters use their own bulb meshes. "
            + "Table insert centers are checked for reconciliation only; measured lamps are not validated against their own drawing. "
            + "The corrected native flipper-pivot control reads and all old/new pixel corrections are retained in the seed/report. PDF15 regional sling17/18 and PDF17 storage/shooter9/12 observations are explicitly excluded from precise fits; their observed table placements remain. "
            + "No public GI bindings or stock socket counts are invented.\n")


def verify_external(root: Path, configured_root) -> None:
    seed = read_seed(root)
    t = seed["table"]
    vpx = configured_root("PINMAME_VPX_SOURCES_ROOT")
    if vpx is not None:
        directory = vpx / t["path"]
        source = directory / t["filename"]
        if not source.is_file() or sha(source) != t["sha256"] or source.stat().st_size != t["size"]:
            raise RuntimeError("retained spatial VPX absent or changed")
        if not (directory / "retention.json").is_file() or sha(directory / "retention.json") != RETENTION_SHA:
            raise RuntimeError("spatial retention metadata absent or changed")
        extracted = directory / "extracted"
        if check_manifest(extracted, "fpwr2_l2") != t["manifest_sha256"]:
            raise RuntimeError("spatial extraction manifest changed")
        manifest = load_json(extracted / "manifest.json")
        if len(manifest["files"]) != t["file_count"] or sum(f["size"] for f in manifest["files"]) != t["byte_count"]:
            raise RuntimeError("spatial extraction totals changed")
        for rel, digest in t["inputs"].items():
            if sha(extracted / rel) != digest:
                raise RuntimeError(f"spatial source changed: {rel}")
        data = load_json(extracted / "gamedata.json")
        if {k: data[k] for k in t["bounds"]} != t["bounds"]:
            raise RuntimeError("spatial normalization bounds changed")
        for name, o in seed["objects"].items():
            if sha(extracted / o["path"]) != o["sha256"]:
                raise RuntimeError(f"spatial object changed: {name}")
            typ, value = next(iter(load_json(extracted / o["path"]).items()))
            fields = {k: value[k] for k in o["fields"] if k != "drag_points"}
            if "drag_points" in o["fields"]:
                fields["drag_points"] = [{k: p[k] for k in ["x", "y", "is_slingshot"]} for p in value["drag_points"]]
            if typ != o["type"] or fields != o["fields"]:
                raise RuntimeError(f"spatial derived fields differ: {name}")
        gi = next(c for c in load_json(extracted / "collections.json") if c["name"] == "GI")
        if gi["items"] != seed["unbound_gi"]["lights"]:
            raise RuntimeError("GI grouping changed")
    manuals = configured_root("PINMAME_MANUALS_ROOT")
    if manuals is not None:
        for page in seed["pages"].values():
            path = manuals / "by-machine" / MACHINE_ID / page["render"]
            if not path.is_file() or sha(path) != page["sha256"]:
                raise RuntimeError("spatial native drawing absent or changed")
    review = configured_root("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review is not None:
        for spec in [seed["world_obj"], *(p["external_crop"] for p in seed["pages"].values()), *seed["correction_crops"]]:
            path = review / SESSION / spec["path"]
            if not path.is_file() or sha(path) != spec["sha256"]:
                raise RuntimeError("spatial derived artifact absent or changed")
        actual = mesh_bounds(review / SESSION / seed["world_obj"]["path"], set(seed["world_obj"]["bounds"]))
        if actual != seed["world_obj"]["bounds"]:
            raise RuntimeError("spatial world mesh bounds differ")


def mesh_bounds(path: Path, names: set[str]) -> dict[str, Any]:
    result, name = {}, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("o "):
            name = line[2:].strip()
        elif line.startswith("v ") and name in names:
            xyz = [float(v) for v in line.split()[1:4]]
            if name not in result:
                result[name] = {"vertices": 0, "minimum": xyz[:], "maximum": xyz[:]}
            b = result[name]
            b["vertices"] += 1
            b["minimum"] = [min(a, v) for a, v in zip(b["minimum"], xyz)]
            b["maximum"] = [max(a, v) for a, v in zip(b["maximum"], xyz)]
    return result
