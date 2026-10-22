"""Unit tests for the factory location-drawing callout check."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import drawing_callouts as dc


def pixel(x: float, y: float) -> list[float]:
	# A drawing 800 px wide with a slight shear, so the fit has to recover a real affine.
	return [round(100 + 800 * x + 20 * y, 1), round(50 + 30 * x + 1600 * y, 1)]


def seed() -> dict:
	controls = [("upper-left jet bumper centre", 0.36, 0.17), ("upper-right jet bumper centre", 0.66, 0.18),
	            ("lower jet bumper centre", 0.51, 0.23), ("left flipper pivot", 0.37, 0.87),
	            ("right flipper pivot", 0.67, 0.87)]
	placements = {f"p{n}": (0.1 + 0.08 * n, 0.1 + 0.08 * (3 * n % 10)) for n in range(1, 11)}
	return {
		"format": dc.FORMAT,
		"pages": {"page": {
			"controls": [{"feature": f, "object": f, "pixel": pixel(x, y), "xy": [x, y]} for f, x, y in controls],
			"reads": [{"label": f"{n:02d}", "pixel": pixel(x + 0.01, y - 0.01), "point": "leader_end"}
			          for n, (x, y) in ((int(k[1:]), v) for k, v in placements.items())],
		}},
		"checks": {k: {"page": "page", "label": k[1:]} for k in placements},
	}, placements


class DrawingCalloutTests(unittest.TestCase):
	def test_labels_normalize_leading_zeros_and_shared_circles(self):
		self.assertEqual(["7"], dc.labels("07"))
		self.assertEqual(["5", "16"], dc.labels("05/16"))
		self.assertEqual(["1R"], dc.labels("1r"))
		self.assertEqual(["29", "30"], dc.labels("29&30"))

	def test_fit_recovers_an_exact_affine(self):
		pairs = [(pixel(x, y), (x, y)) for x, y in ((0.1, 0.1), (0.9, 0.2), (0.5, 0.9), (0.3, 0.6))]
		transform = dc.fit(pairs)
		for p, xy in pairs:
			self.assertLess(dc.distance(dc.apply(transform, p), xy), 1e-9)

	def test_agreeing_callouts_validate(self):
		s, placements = seed()
		result = dc.evaluate(s, placements)
		self.assertTrue(all(d["agrees"] for d in result["placements"].values()))
		self.assertLess(result["pages"]["page"]["control_rms"], 0.001)

	def test_a_transposed_callout_stays_observed_and_does_not_skew_the_fit(self):
		s, placements = seed()
		reads = s["pages"]["page"]["reads"]
		reads[0]["label"], reads[9]["label"] = reads[9]["label"], reads[0]["label"]
		result = dc.evaluate(s, placements)
		self.assertFalse(result["placements"]["p1"]["agrees"])
		self.assertFalse(result["placements"]["p10"]["agrees"])
		self.assertTrue(all(result["placements"][f"p{n}"]["agrees"] for n in range(2, 10)))
		self.assertEqual(8, result["pages"]["page"]["callout_fit_pairs"])

	def test_both_fits_must_agree(self):
		s, placements = seed()
		# Shift every control: the callouts still agree with each other but not with the table.
		for control in s["pages"]["page"]["controls"]:
			control["pixel"][0] += 200
		result = dc.evaluate(s, placements)
		self.assertFalse(any(d["agrees"] for d in result["placements"].values()))

	def test_missing_callout_and_unknown_placement(self):
		s, placements = seed()
		s["checks"]["p11"] = {"page": "page", "label": "11"}
		placements["p11"] = (0.5, 0.5)
		result = dc.evaluate(s, placements)
		self.assertFalse(result["placements"]["p11"]["agrees"])
		self.assertIsNone(result["placements"]["p11"]["read"])
		bad = copy.deepcopy(s)
		bad["checks"]["ghost"] = {"page": "page", "label": "3"}
		with self.assertRaises(ValueError):
			dc.evaluate(bad, placements)

	def test_one_callout_confirms_only_the_nearest_of_several_placements(self):
		s, placements = seed()
		# A second bulb of device 4 sits 0.03 away; the drawing draws only one callout 4.
		placements["p4b"] = (placements["p4"][0] + 0.03, placements["p4"][1])
		s["checks"]["p4b"] = {"page": "page", "label": "4"}
		result = dc.evaluate(s, placements)
		self.assertTrue(result["placements"]["p4"]["agrees"])
		self.assertFalse(result["placements"]["p4b"]["agrees"])
		self.assertEqual("every callout of this label marks a nearer placement", result["placements"]["p4b"]["reason"])

	def test_controls_must_be_redundant_and_span_the_playfield(self):
		s, placements = seed()
		s["pages"]["page"]["controls"] = s["pages"]["page"]["controls"][:3]
		with self.assertRaisesRegex(ValueError, "at least 4 controls"):
			dc.evaluate(s, placements)
		s, placements = seed()
		s["pages"]["page"]["controls"] = s["pages"]["page"]["controls"][:3] + [dict(s["pages"]["page"]["controls"][0], xy=[0.4, 0.2])]
		with self.assertRaisesRegex(ValueError, "spanning"):
			dc.evaluate(s, placements)

	def test_a_page_that_checks_nothing_keeps_only_its_control_fit(self):
		# A page read only for drawing measurements has no callouts to fit; it must not demand them.
		s, placements = seed()
		s["pages"]["measured"] = {"controls": copy.deepcopy(s["pages"]["page"]["controls"]), "reads": []}
		result = dc.evaluate(s, placements)
		self.assertEqual(0, result["pages"]["measured"]["callout_pairs"])
		self.assertEqual(5, result["pages"]["measured"]["controls"])
		self.assertTrue(all(d["agrees"] for d in result["placements"].values()))

	def elevation_seed(self):
		# A panel drawn obliquely: along the panel is (-50, 75) px, across it (1, -0.05); x = 0.9 - 0.1 * s.
		axis, cross = (-50.0, 75.0), (1.0, -0.05)
		def px(s, t):
			return [round(600 + s * axis[0] + t * cross[0], 3), round(500 + s * axis[1] + t * cross[1], 3)]
		page = {"axis": list(axis), "cross_axis": list(cross), "plane_y": 0.041,
		        "controls": [{"placement": f"lamp{i}", "pixel": px(s, t), "x": round(0.9 - 0.1 * s, 6)}
		                     for i, (s, t) in enumerate(((2.0, 60), (2.6, 40), (3.1, 30), (3.7, 40), (4.2, 60)))],
		        "reads": [{"label": "GI", "pixel": px(s, 0), "point": "symbol_centre"} for s in range(8)]}
		placements = {f"gi{s}": (round(0.9 - 0.1 * s, 6), 0.041) for s in range(8)}
		seed = {"elevations": {"elev": page}, "elevation_checks": {pid: {"page": "elev", "label": "GI"} for pid in placements}}
		return seed, placements, px

	def test_elevation_coordinate_ignores_the_cross_axis(self):
		seed, _placements, px = self.elevation_seed()
		page = seed["elevations"]["elev"]
		base = dc.elevation_coordinate(page, px(3.0, 0))
		self.assertAlmostEqual(base, dc.elevation_coordinate(page, px(3.0, 80)), places=6)
		self.assertAlmostEqual(1.0, dc.elevation_coordinate(page, px(4.0, 0)) - base, places=6)

	def test_elevation_checks_agree_along_the_panel_and_extrapolate(self):
		seed, placements, _px = self.elevation_seed()
		result = dc.evaluate_elevations(seed, placements)
		self.assertEqual(8, len(result["placements"]))
		self.assertTrue(all(d["agrees"] for d in result["placements"].values()))
		placements["gi7"] = (placements["gi7"][0] + 0.09, 0.041)
		self.assertFalse(dc.evaluate_elevations(seed, placements)["placements"]["gi7"]["agrees"])

	def test_elevation_measurement_reproduces_and_is_never_checked_on_its_own_page(self):
		seed, placements, px = self.elevation_seed()
		seed["elevation_measurements"] = {"gi3": {"page": "elev", "pixel": px(3.0, 0), "normalized": [0.6, 0.041]}}
		self.assertEqual((0.6, 0.041), dc.elevation_measured(seed, "gi3"))
		seed["elevation_measurements"]["gi3"]["normalized"] = [0.61, 0.041]
		with self.assertRaisesRegex(ValueError, "does not reproduce"):
			dc.elevation_measured(seed, "gi3")
		with self.assertRaisesRegex(ValueError, "measured on"):
			dc.evaluate_elevations(seed, placements)

	def test_inset_reads_are_not_used(self):
		s, placements = seed()
		s["pages"]["page"]["reads"][2]["region"] = "inset"
		result = dc.evaluate(s, placements)
		self.assertIsNone(result["placements"]["p3"]["read"])

	def test_promote_validates_only_agreeing_table_placements(self):
		definition = {"inputs": [
			{"id": "a", "spatial": {"status": "observed", "placements": [
				{"id": "p1", "provenance": {"status": "observed"}}, {"id": "p2", "provenance": {"status": "observed"}}]}},
			{"id": "b", "spatial": {"status": "candidate", "placements": [{"id": "p3", "provenance": {"status": "candidate"}}]}},
			{"id": "c", "spatial": {"status": "not_applicable"}},
		]}
		decisions = {"placements": {"p1": {"agrees": True}, "p2": {"agrees": False}, "p3": {"agrees": True}}}
		self.assertEqual(["p1", "p3"], dc.promote(definition, decisions))
		self.assertEqual("observed", definition["inputs"][0]["spatial"]["status"])
		self.assertEqual("validated", definition["inputs"][1]["spatial"]["status"])


if __name__ == "__main__":
	unittest.main()
