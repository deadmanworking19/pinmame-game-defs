import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import simpsons_party_spotlights as spotlight


EVIDENCE = Path(__file__).resolve().parents[1] / 'tools/seeds/stern/the-simpsons-pinball-party-2003/spotlights.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SpotlightTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_conditional_axes_full_seat_range_and_scale_allowance(self):
        e = self.evidence
        self.assertEqual(e['format'], 'simpsons-party-spotlight-axis-v1')
        self.assertEqual(e['uncertainty_normalized'], 0.02)
        self.assertAlmostEqual(1.0625 * 25.4 / 50, e['units']['millimeters_per_vpu'])
        expected = {'Primitive24': [0.80, 0.77], 'Primitive98': [0.92, 0.33],
                    'Primitive108': [0.37, 0.27], 'Primitive116': [0.26, 0.27]}
        self.assertEqual(set(expected), {r['object'] for r in e['records']})
        for r in e['records']:
            with self.subTest(object=r['object']):
                result = spotlight.project(r, e)
                self.assertEqual(result['coarse_xy'], expected[r['object']])
                self.assertEqual([len(r['selections'][s]) for s in ('neck', 'mouth', 'socket')], [25, 48, 56])
                self.assertLess(math.dist(result['seat_range'], r['socket_axial_span_vpu']), 1e-6)
                for actual, reference in zip(result['seat_endpoint_world'], r['conditional_seat_endpoint_world']):
                    self.assertLess(math.dist(actual, reference), 1e-6)
                self.assertTrue(all(0 < span < e['uncertainty_normalized'] for span in result['seat_and_scale_halfspan_xy']))
        self.assertTrue(any('not a separate observed filament' in item for item in e['limitations']))
        self.assertTrue(any('10percent' in item for item in e['limitations']))

    def test_changed_vertices_indices_digest_and_ranges_fail_closed(self):
        for case in ('vertex', 'redigested_vertex', 'index', 'digest', 'seat_range', 'table_bounds', 'lcl', 'missing_vertex'):
            with self.subTest(case=case):
                e = copy.deepcopy(self.evidence)
                r = e['records'][0]
                if case in ('vertex', 'redigested_vertex'):
                    r['selections']['neck'][0]['xyz'][0] += 1
                    if case == 'redigested_vertex':
                        r['selection_sha256'] = spotlight.selection_sha256(r['selections'])
                elif case == 'index':
                    r['selections']['neck'][0]['index'] = r['selections']['mouth'][0]['index']
                    r['selection_sha256'] = spotlight.selection_sha256(r['selections'])
                elif case == 'digest':
                    r['selection_sha256'] = '0' * 64
                elif case == 'seat_range':
                    r['socket_axial_span_vpu'][0] += 1
                elif case == 'table_bounds':
                    e['table_bounds'][0] += 1
                elif case == 'lcl':
                    e['bulb']['light_center_length_mm'] += 1
                else:
                    r['selections']['socket'].pop()
                with self.assertRaises(ValueError):
                    spotlight.project(r, e)

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional retained source documents not configured')
    def test_retained_documents_and_analysis_hashes(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        for item in (self.evidence['units'], self.evidence['bulb']):
            self.assertEqual(sha(root / item['retained_path']), item['sha256'])
        for item in self.evidence['retained_analysis']:
            self.assertEqual(sha(root / item['path']), item['sha256'])

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'optional VPW source not configured')
    def test_full_obj_and_selected_vertices(self):
        root = Path(os.environ['PINMAME_VPX_SOURCES_ROOT'])
        obj = root / self.evidence['world_obj']['path']
        spotlight.verify_obj(obj, self.evidence)
        altered = copy.deepcopy(self.evidence)
        altered['world_obj']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'OBJ SHA-256'):
            spotlight.verify_obj(obj, altered)
        base = root / 'stern/the-simpsons-pinball-party-2003/vpw-2.0/extracted/gameitems'
        for r in self.evidence['records']:
            self.assertEqual(sha(base / f"Primitive.{r['object']}.json"), r['primitive_json_sha256'])
            self.assertEqual(sha(base / f"Primitive.{r['object']}.obj"), r['primitive_local_obj_sha256'])


if __name__ == '__main__':
    unittest.main()
