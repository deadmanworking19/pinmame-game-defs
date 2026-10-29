"""Project the Ghostbusters LE seed into an honest partial spatial audit."""
from __future__ import annotations

from copy import deepcopy


# These names describe only classifications explicitly stated in the device notes.
PROJECTIONS = (
    ("magnetic sling actuator projected", "effect", "magnet_field_trigger"),
    ("trough jam sensor projected", "sensor", "trough_release_slot"),
    ("slingshot contact projected", "sensor", "slingshot_polygon_centroid"),
    ("trough sensor projected", "sensor", "trough_ball_slot"),
    ("standup contact projected", "sensor", "target_collider"),
    ("bumper switch projected", "sensor", "bumper_center"),
    ("bumper coil projected", "effect", "bumper_center"),
    ("auto-launch actuator projected", "effect", "shooter_trigger"),
    ("flipper actuator projected", "effect", "flipper_pivot"),
    ("vuk actuator projected", "effect", "captured_ball_trigger"),
)


def enrich_spatial_report(root, definition, report):
    """Copy declared facts, retaining independent spatial and device provenance."""
    del root  # The seed is the sole input; no external files or invented facts.
    report = deepcopy(report)
    declared = []
    missing = []
    not_applicable = []
    unknown_availability = []
    polarity = []
    emitter_quantities = []
    unvalidated_spatial = []
    projection_classes = set()
    for collection in ("inputs", "outputs", "displays"):
        for device in definition.get(collection, []):
            spatial = device.get("spatial")
            physical = device.get("physical", {})
            notes = physical.get("notes", "")
            identity = {"collection": collection, "id": device["id"],
                        "binding": deepcopy(device.get("binding"))}
            if not isinstance(spatial, dict):
                missing.append({**identity, "physical_location": physical.get("location", device.get("physical_location")),
                                "availability": device.get("availability")})
            elif spatial.get("status") == "not_applicable":
                not_applicable.append({**identity, "reason": spatial.get("reason"),
                                       "provenance": deepcopy(spatial.get("provenance"))})
            else:
                if spatial.get("status") != "validated":
                    unvalidated_spatial.append({**identity, "status": spatial.get("status")})
                for placement in spatial.get("placements", []):
                    classes = [name for phrase, role, name in PROJECTIONS
                               if phrase in notes.lower() and placement.get("role") == role]
                    projection_classes.update(classes)
                    declared.append({**identity, "spatial_status": spatial.get("status"),
                                     "placement": deepcopy(placement),
                                     "quantity": device.get("quantity"),
                                     "physical_quantity": physical.get("quantity"),
                                     "notes": notes, "projection_classes": classes})
            if device.get("availability") == "unknown":
                unknown_availability.append(identity)
            if (collection == "outputs" and device.get("kind") in {"lamp", "rgb_lamp", "flasher", "gi"}
                    and device.get("availability") in {"used", "optional"}
                    and physical.get("quantity") is None):
                emitter_quantities.append({**identity, "availability": device.get("availability"),
                                           "physical_location": physical.get("location")})
            if (collection == "inputs" and device.get("kind") == "switch"
                    and device.get("availability") != "unused"
                    and device.get("normally_closed") is None):
                polarity.append({**identity, "availability": device.get("availability"),
                                 "switch_type": physical.get("switch_type")})
    report["declared_placements"] = declared
    report["projection_classes"] = sorted(projection_classes)
    report["absent_spatial"] = missing
    report["not_applicable_spatial"] = not_applicable
    report["unresolved_physical_polarity_inputs"] = polarity
    report["unresolved_emitter_quantities"] = emitter_quantities
    report["unvalidated_spatial_records"] = unvalidated_spatial
    report["unknown_availability"] = unknown_availability
    report["mechanism_candidates"] = [deepcopy(mechanism) for mechanism in definition.get("mechanisms", [])
                                      if mechanism.get("provenance", {}).get("status") == "candidate"]
    report["completion_source_excerpts"] = [
        {"source_id": source["id"], "source_kind": source.get("kind"),
         "source_sha256": source.get("sha256"), "excerpt": deepcopy(excerpt)}
        for source in definition.get("sources", []) for excerpt in source.get("excerpts", [])
        if (source.get("id", "").startswith("completion-")
            or excerpt.get("id", "").startswith("completion-"))
    ]
    report["completion_source_excerpts"].sort(key=lambda row: (row["source_id"], row["excerpt"]["id"]))
    return report


def report_markdown(report):
    import curate_spike1

    text = curate_spike1.report_markdown(report)
    classes = ", ".join(f"`{name}`" for name in report["projection_classes"])
    text = text.replace("None declared by the schema-valid seed; no class or coordinate was inferred.",
                        classes or "No projection class is explicitly described in the declared placement notes.")
    text += ("\n## Evidence roles and declared placements\n\n"
             "The user identified this exact PinMAME table; a complete VPX launch/playtest has not been established. Its bindings were independently reviewed against factory documents, ROM/source and fresh native-library harness evidence. "
             "Its script supplies runtime bindings; its table supplies observed geometry. The own factory manual supplies physical "
             "construction and fitment, while PinMAME source and ROM routing describe emulator transport. "
             "A projection onto a table object is not a measured physical coil or sensor location. "
             "Placement and device provenance are independent; observed is not validated.\n\n"
             "| Device | Placement | Role | x | y | Spatial / placement status | Sources | Quantity | Projection |\n"
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for row in report["declared_placements"]:
        p = row["placement"]
        provenance = p.get("provenance", {})
        refs = ", ".join(f"`{ref}`" for ref in provenance.get("source_refs", []))
        quantity = row["quantity"] if row["quantity"] is not None else row["physical_quantity"]
        text += (f"| {row['id']} | {p.get('id')} | {p.get('role')} | {p.get('x')} | {p.get('y')} | "
                 f"{row['spatial_status']} / {provenance.get('status')} | {refs} | {quantity if quantity is not None else 'not declared'} | "
                 f"{', '.join(row['projection_classes']) or 'not explicitly classified'} |\n")
    text += ("\n## Remaining evidence gaps\n\n"
             "Absent spatial records are not cabinet/service determinations. Controlled not-applicable records retain their declared "
             "reason, including cabinet/service and other reasons. Missing contact construction is separate from emulator polarity; "
             "unknown availability is separate from an absent placement. Candidate mechanisms are not validated. "
             "See the coverage blockers and the knowledge note for the remaining work.\n\n")
    for title, key in (("Absent spatial", "absent_spatial"), ("Not applicable", "not_applicable_spatial"),
                       ("Unvalidated spatial records", "unvalidated_spatial_records"),
                       ("Unresolved physical polarity", "unresolved_physical_polarity_inputs"),
                       ("Unresolved emitter quantities", "unresolved_emitter_quantities"),
                       ("Unknown availability", "unknown_availability"), ("Mechanism candidates", "mechanism_candidates")):
        text += f"### {title}\n\n"
        for row in report[key]:
            detail = f" — {row['reason']}" if row.get("reason") else ""
            if row.get("physical_location"):
                detail += f" — declared location: {row['physical_location']}"
            if row.get("status"):
                detail += f" — {row['status']}"
            text += f"- `{row['id']}`{detail}\n"
        if not report[key]:
            text += "None declared.\n"
        text += "\n"
    text += "## Completion evidence excerpts\n\n"
    for row in report["completion_source_excerpts"]:
        excerpt = row["excerpt"]
        text += (f"- `{row['source_id']}` ({row['source_kind']}, `{row['source_sha256']}`): "
                 f"`{excerpt['id']}` — `{excerpt['path']}` SHA-256 `{excerpt['sha256']}`.\n")
    return text
