"""Check table placements against the callouts of factory location drawings.

A callout seed (``tools/seeds/<manufacturer>/<machine>-callouts.json``) records, for each factory
location drawing, the render it was read on with its SHA-256 and pixel size, the mechanism centres
read as controls, and every callout read on the drawing: the label as printed and the drawing pixel
where its leader ends at the part, or the centre of the part a label is printed on. Its ``checks``
map names, for each placement it checks, the page and label of the callout that names it.

``evaluate`` decides every checked placement from the seed alone, so a test can recompute it
without the renders:

- A page's control fit maps drawing pixels to normalized playfield coordinates by least squares
  over its controls: jet bumper caps and flipper pivots, whose table objects are unambiguous (or,
  where balloons hide the pivots, other crisp mechanism features). It needs at least four controls
  spanning half the playfield height, so it has leave-one-out redundancy and does not extrapolate
  from one cluster.
- A page's callout fit does the same over each checked placement and the nearest read of its own
  label, measured leave-one-out: a read is transformed by the fit on every other pair. The pair
  furthest beyond the limit is dropped and the fit repeated until every remaining pair is within
  it, so a transposed or misread callout cannot pull the fit towards itself. Because the callouts
  cover the whole page, this fit interpolates where the controls do not, and each leave-one-out
  offset is that placement's own prediction error, edges included.
- Each read confirms at most one placement: placements and reads of one label are paired nearest
  first, so a device with two bulbs and one drawn callout validates only the bulb the callout marks.
- A placement agrees with the drawing when its paired read lands within the limit under both fits. The limit is 0.07 normalized, the bar the Indianapolis 500 and Twilight
  Zone records use: a leader ends on the part it names, not at the object's centre.

A curator promotes an agreeing placement to ``validated`` and keeps every other one at the status
the table evidence gave it. Placements measured on the drawing itself are never checked against it.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

FORMAT = "pinmame-drawing-callouts"
LIMIT = 0.07
# A page's control fit must have leave-one-out redundancy and reach from the jet bumpers towards the
# flippers, so it interpolates over most of the playfield instead of extrapolating from one cluster.
MIN_CONTROLS = 4
MIN_CONTROL_SPAN = 0.5


def labels(printed: str) -> list[str]:
	"""Normalize a printed callout: ``"07"`` is ``"7"``, ``"05/16"`` names both 5 and 16."""
	result = []
	for part in re.split(r"[/&,]", printed):
		part = part.strip().upper().replace(" ", "")
		match = re.fullmatch(r"0*(\d+)([A-Z]?)", part)
		if part:
			result.append(str(int(match.group(1))) + match.group(2) if match else part)
	return result


def _solve(rows: list[tuple[float, float, float]], values: list[float]) -> list[float]:
	m = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
	t = [sum(r[i] * value for r, value in zip(rows, values)) for i in range(3)]
	for col in range(3):
		pivot = max(range(col, 3), key=lambda row: abs(m[row][col]))
		m[col], m[pivot] = m[pivot], m[col]
		t[col], t[pivot] = t[pivot], t[col]
		if abs(m[col][col]) < 1e-12:
			raise ValueError("degenerate drawing fit: controls are collinear")
		for row in range(3):
			if row != col:
				factor = m[row][col] / m[col][col]
				m[row] = [a - factor * b for a, b in zip(m[row], m[col])]
				t[row] -= factor * t[col]
	return [t[i] / m[i][i] for i in range(3)]


def fit(pairs: Iterable[tuple[tuple[float, float], tuple[float, float]]]) -> tuple[list[float], list[float]]:
	"""Least-squares affine x = a*u + b*v + c, y = d*u + e*v + f from (pixel, (x, y)) pairs."""
	pairs = list(pairs)
	if len(pairs) < 3:
		raise ValueError("a drawing fit needs at least three pairs")
	rows = [(float(u), float(v), 1.0) for (u, v), _ in pairs]
	return _solve(rows, [xy[0] for _, xy in pairs]), _solve(rows, [xy[1] for _, xy in pairs])


def apply(transform: tuple[list[float], list[float]], pixel: Iterable[float]) -> tuple[float, float]:
	(a, b, c), (d, e, f) = transform
	u, v = pixel
	return a * u + b * v + c, d * u + e * v + f


def distance(p: Iterable[float], q: Iterable[float]) -> float:
	(px, py), (qx, qy) = p, q
	return math.hypot(px - qx, py - qy)


def leave_one_out(pairs: list[tuple[tuple[float, float], tuple[float, float]]]) -> list[float]:
	"""Each pair's offset from the fit on all the other pairs (needs four or more pairs)."""
	return [distance(apply(fit(pairs[:i] + pairs[i + 1:]), pixel), xy) for i, (pixel, xy) in enumerate(pairs)]


def _read_point(read: dict[str, Any]) -> tuple[float, float]:
	return tuple(read["pixel"])


def evaluate(seed: dict[str, Any], placements: dict[str, tuple[float, float]], limit: float = LIMIT) -> dict[str, Any]:
	"""Decide every placement the seed checks.

	``placements`` maps placement IDs to their normalized ``(x, y)``. Returns ``{"pages": ...,
	"placements": ...}``: per page its two fits' summaries, per placement the page, label, chosen read,
	both offsets and whether it agrees.
	"""
	if seed.get("format") != FORMAT:
		raise ValueError("not a drawing callout seed")
	missing = sorted(set(seed["checks"]) - set(placements))
	if missing:
		raise ValueError(f"callout checks name placements the definition lacks: {missing}")
	result: dict[str, Any] = {"limit": limit, "pages": {}, "placements": {}}
	for key, page in sorted(seed["pages"].items()):
		controls = [(tuple(c["pixel"]), tuple(c["xy"])) for c in page["controls"]]
		span = max(xy[1] for _, xy in controls) - min(xy[1] for _, xy in controls) if controls else 0.0
		if len(controls) < MIN_CONTROLS or span < MIN_CONTROL_SPAN:
			raise ValueError(f"{key}: the control fit needs at least {MIN_CONTROLS} controls spanning {MIN_CONTROL_SPAN} of the playfield height")
		control_fit = fit(controls)
		control_loo = leave_one_out(controls) if len(controls) >= 4 else []
		reads = [r for r in page["reads"] if r.get("region", "playfield") == "playfield"]
		by_label: dict[str, list[int]] = {}
		for index, read in enumerate(reads):
			for label in labels(read["label"]):
				by_label.setdefault(label, []).append(index)
		# Pair placements with reads of their own label one-to-one, nearest first, so a single
		# callout never confirms two placements of a multi-bulb or multi-contact device.
		chosen: dict[str, int | None] = {}
		groups: dict[str, list[str]] = {}
		for pid, check in sorted(seed["checks"].items()):
			if check["page"] == key:
				groups.setdefault(labels(check["label"])[0], []).append(pid)
		for label, pids in sorted(groups.items()):
			options = sorted((distance(apply(control_fit, _read_point(reads[i])), placements[pid]), pid, i)
			                 for pid in pids for i in by_label.get(label, []))
			used: set[int] = set()
			for _, pid, i in options:
				if pid not in chosen and i not in used:
					chosen[pid] = i
					used.add(i)
			for pid in pids:
				chosen.setdefault(pid, None)
		paired = sorted(pid for pid, index in chosen.items() if index is not None)
		kept = list(paired)
		while len(kept) >= 4:
			pairs = [(_read_point(reads[chosen[pid]]), tuple(placements[pid])) for pid in kept]
			offsets = leave_one_out(pairs)
			worst = max(range(len(kept)), key=lambda i: (offsets[i], kept[i]))
			if offsets[worst] <= limit:
				break
			kept.pop(worst)
		if len(kept) < 4:
			raise ValueError(f"{key}: fewer than four callouts agree with their placements; the page cannot be fitted")
		kept_pairs = [(_read_point(reads[chosen[pid]]), tuple(placements[pid])) for pid in kept]
		callout_fit = fit(kept_pairs)
		kept_offsets = dict(zip(kept, leave_one_out(kept_pairs)))
		result["pages"][key] = {
			"controls": len(controls),
			"control_rms": round(math.sqrt(sum(distance(apply(control_fit, p), xy) ** 2 for p, xy in controls) / len(controls)), 4),
			"control_loo_max": round(max(control_loo), 4) if control_loo else None,
			"callout_pairs": len(paired),
			"callout_fit_pairs": len(kept),
			"callout_loo_max": round(max(kept_offsets.values()), 4),
			"control_fit": [[round(v, 9) for v in row] for row in control_fit],
			"callout_fit": [[round(v, 9) for v in row] for row in callout_fit],
		}
		for pid, index in sorted(chosen.items()):
			check = seed["checks"][pid]
			entry: dict[str, Any] = {"page": key, "label": check["label"]}
			if index is None:
				spent = bool(by_label.get(labels(check["label"])[0]))
				entry.update(read=None, agrees=False,
				             reason="every callout of this label marks a nearer placement" if spent else "no callout of this label on the drawing")
			else:
				pixel = _read_point(reads[index])
				by_controls = distance(apply(control_fit, pixel), placements[pid])
				by_callouts = kept_offsets.get(pid, distance(apply(callout_fit, pixel), placements[pid]))
				entry.update(read=index, point=reads[index].get("point"), pixel=list(pixel), control_offset=round(by_controls, 4),
				             callout_offset=round(by_callouts, 4),
				             agrees=by_controls <= limit and by_callouts <= limit)
			result["placements"][pid] = entry
	return result


RULE = (
	"A placement is validated when its own callout on the factory location drawing (each callout paired with "
	"at most one placement of its label, nearest first) lands within 0.07 normalized of it under two "
	"least-squares fits of that page: one on independently read controls (jet-bumper caps and flipper "
	"pivots, or another crisp mechanism feature where balloons hide a pivot), and one, measured "
	"leave-one-out, on the page's other callout reads, from which any read beyond the limit is dropped. Placements without such a read keep their table status. Placements "
	"measured on a drawing are never checked against it."
)


def placements_of(definition: dict[str, Any]) -> dict[str, tuple[float, float]]:
	return {placement["id"]: (placement["x"], placement["y"])
	        for collection in ("inputs", "outputs", "displays") for device in definition.get(collection) or []
	        for placement in (device.get("spatial") or {}).get("placements") or []}


def measured(seed: dict[str, Any], placement_id: str) -> tuple[float, float]:
	"""A placement measured on a drawing: its read pixel through that page's control fit.

	Rounded to three decimals, the precision these scans support; the stored value must match.
	"""
	item = seed["measurements"][placement_id]
	page = seed["pages"][item["page"]]
	x, y = apply(fit([(tuple(c["pixel"]), tuple(c["xy"])) for c in page["controls"]]), item["pixel"])
	value = (round(x, 3), round(y, 3))
	if list(value) != item["normalized"]:
		raise ValueError(f"drawing measurement {placement_id} does not reproduce: {value} != {item['normalized']}")
	return value


def apply_to_definition(definition: dict[str, Any], seed: dict[str, Any], source_id: str) -> dict[str, Any]:
	"""Evaluate the seed against a built definition, promote agreeing placements and note the rest.

	A promoted placement also cites ``source_id``, the definition's source record for the seed. Each
	device with a checked placement that does not agree gets one sentence saying why, so a reader of
	the device sees what the drawing showed without opening the seed.
	"""
	if seed.get("machine_id") != definition["machine"]["id"]:
		raise ValueError("drawing callout seed belongs to another machine")
	if source_id not in {source["id"] for source in definition.get("sources", [])}:
		raise ValueError(f"the definition has no source record {source_id} for its drawing callout seed")
	decisions = evaluate(seed, placements_of(definition), seed.get("limit", LIMIT))
	promoted = set(promote(definition, decisions))
	for collection in ("inputs", "outputs", "displays"):
		for device in definition.get(collection) or []:
			for placement in (device.get("spatial") or {}).get("placements") or []:
				refs = placement["provenance"]["source_refs"]
				if placement["id"] in promoted and source_id not in refs:
					refs.append(source_id)
	for collection in ("inputs", "outputs", "displays"):
		for device in definition.get(collection) or []:
			placements = (device.get("spatial") or {}).get("placements") or []
			reasons = []
			for placement in placements:
				decision = decisions["placements"].get(placement["id"])
				if not decision or decision["agrees"]:
					continue
				page = seed["pages"][decision["page"]]["locator"].split(":")[0]
				label = decision["label"]
				if decision["read"] is None and decision["reason"].startswith("every"):
					why = f"draws callout {label} only once, at a nearer placement of this device"
				elif decision["read"] is None:
					why = f"draws no callout {label}"
				else:
					worst = f"{max(decision['control_offset'], decision['callout_offset']):.3f} normalized from it, beyond the {LIMIT} limit"
					why = {
						"symbol_centre": f"draws part {label} {worst}",
						"label_beside": f"draws callout {label} without a leader, its label {worst}",
						"label_beside_part": f"draws callout {label} without a leader beside a part {worst}",
					}.get(decision["point"], f"ends callout {label}'s leader {worst}")
				target = "this placement" if len(placements) == 1 else f"placement {placement['id']}"
				reasons.append(f"The factory drawing ({page}) {why}, so {target} stays {placement['provenance']['status']}.")
			if reasons:
				physical = device.setdefault("physical", {})
				physical["notes"] = (physical.get("notes", "") + " " + " ".join(reasons)).strip()
	return decisions


def summary(seed: dict[str, Any], decisions: dict[str, Any], seed_path: str, seed_sha256: str) -> dict[str, Any]:
	"""Report-ready record of the check: rule, pages, fits and every placement left unvalidated."""
	agreeing = sorted(pid for pid, d in decisions["placements"].items() if d["agrees"])
	return {
		"seed": seed_path, "seed_sha256": seed_sha256, "rule": RULE, "limit": decisions["limit"],
		"read_by": seed.get("read_by"), "retained_artifacts": seed.get("retained_artifacts"),
		"pages": {key: {"locator": seed["pages"][key]["locator"], "image": seed["pages"][key]["image"],
		                **{k: v for k, v in page.items() if not k.endswith("_fit")}}
		          for key, page in decisions["pages"].items()},
		"checked": len(decisions["placements"]), "validated": len(agreeing),
		"not_validated": {pid: {k: d[k] for k in ("page", "label", "control_offset", "callout_offset") if k in d}
		                  | ({} if d["read"] is not None else {"reason": d["reason"]})
		                  for pid, d in sorted(decisions["placements"].items()) if not d["agrees"]},
	}


def verify_retained(seed: dict[str, Any], repository: Path, manuals: Path | None, review_artifacts: Path | None) -> int:
	"""Re-hash every page render and the retained reading artifacts that are reachable.

	Renders live in the repository (committed excerpts), the manuals root or the review-artifacts
	root; a root that is not supplied is skipped. Returns the number of files checked and raises on
	any missing or changed file.
	"""
	roots = {"repository": repository, "manuals": manuals, "review_artifacts": review_artifacts}
	checked = 0
	for key, page in sorted(seed["pages"].items()):
		image = page["image"]
		root = roots[image["root"]]
		if root is None:
			continue
		path = root / image["path"]
		if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != image["sha256"]:
			raise ValueError(f"drawing callout render missing or changed: {key} {path}")
		checked += 1
	retained = seed.get("retained_artifacts")
	if retained and review_artifacts is not None:
		directory = review_artifacts / retained["directory"]
		manifest = directory / "manifest.json"
		if not manifest.is_file() or hashlib.sha256(manifest.read_bytes()).hexdigest() != retained["manifest_sha256"]:
			raise ValueError(f"drawing callout artifacts manifest missing or changed: {manifest}")
		for entry in json.loads(manifest.read_text(encoding="utf-8"))["files"]:
			target = directory / entry["path"]
			if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != entry["sha256"]:
				raise ValueError(f"drawing callout artifact missing or changed: {target}")
			checked += 1
	return checked


def promote(definition: dict[str, Any], decisions: dict[str, Any]) -> list[str]:
	"""Set each agreeing placement to ``validated`` and recompute its device's spatial status.

	A device's spatial status becomes the weakest status among its placements. Returns the IDs of
	the promoted placements.
	"""
	rank = {"candidate": 0, "observed": 1, "validated": 2}
	promoted = []
	for collection in ("inputs", "outputs", "displays"):
		for device in definition.get(collection) or []:
			spatial = device.get("spatial") or {}
			if spatial.get("status") in (None, "not_applicable"):
				continue
			for placement in spatial["placements"]:
				decision = decisions["placements"].get(placement["id"])
				if decision and decision["agrees"] and placement["provenance"]["status"] in ("candidate", "observed"):
					placement["provenance"]["status"] = "validated"
					promoted.append(placement["id"])
			spatial["status"] = min((p["provenance"]["status"] for p in spatial["placements"]), key=rank.__getitem__)
	return promoted
