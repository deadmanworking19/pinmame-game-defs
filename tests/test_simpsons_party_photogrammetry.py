import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import simpsons_party_photogrammetry as photo


EVIDENCE = Path(__file__).resolve().parents[1] / 'tools/seeds/stern/the-simpsons-pinball-party-2003/photogrammetry.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PhotogrammetryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_fixed_camera_replay_and_sensitivity(self):
        for name, expected, maximum_residual in [('homer', [0.73, 0.13], 7.6), ('gi5', [0.34, 0.26], 1.0)]:
            with self.subTest(name=name):
                result = photo.replay(self.data, name)
                measurement = self.data['measurements'][name]
                self.assertEqual(result['coarse_xy'], expected)
                self.assertLess(math.dist(result['world'], measurement['recorded_svd_world']), 0.05)
                self.assertLess(max(p['residual_px'] for p in result['reprojections']), maximum_residual)
                self.assertEqual(measurement['bootstrap']['succeeded'], 200)
                self.assertEqual(measurement['bootstrap']['requested'], 200)
                self.assertGreaterEqual(len(measurement['calibration_sensitivity']), 4)
                self.assertTrue(all(max(abs(p['normalized_xy'][i] - result['normalized_xy'][i])
                                        for i in (0, 1)) < 0.002
                                    for p in measurement['calibration_sensitivity']))
        self.assertIn('original incandescent', self.data['measurements']['gi5']['limits'])
        self.assertIn('socket', self.data['measurements']['homer']['limits'])
        self.assertIn('not reproduced', self.data['calibration_recipe']['triangulation'])

    def test_gi_replacement_body_crosscheck(self):
        m = self.data['measurements']['gi5']
        cross = m['body_crosscheck']
        point, errors = photo.triangulate(m['cameras'], cross['target_pixels'], self.data['image_size'])
        self.assertLess(math.dist(point, cross['recorded_svd_world']), 0.05)
        self.assertEqual([round(point[i] / self.data['table_bounds'][i], 2) for i in (0, 1)], [0.34, 0.26])
        self.assertNotEqual(cross['target_pixels'], m['target_pixels'])
        self.assertTrue(all(math.isfinite(e['residual_px']) for e in errors))
        self.assertIn('original incandescent', cross['description'])

    def test_malformed_and_mutated_inputs_rejected(self):
        for mutation in ('missing_camera', 'duplicate_camera', 'duplicate_reading', 'bad_matrix',
                         'nonfinite', 'outside_image', 'singular', 'changed_reference', 'changed_pixel'):
            with self.subTest(mutation=mutation):
                d = copy.deepcopy(self.data)
                m = d['measurements']['gi5']
                if mutation == 'missing_camera':
                    m['cameras'] = [c for c in m['cameras'] if c['photo'] != 5]
                elif mutation == 'duplicate_camera':
                    m['cameras'].append(copy.deepcopy(m['cameras'][0]))
                elif mutation == 'duplicate_reading':
                    m['target_pixels'][1]['photo'] = m['target_pixels'][0]['photo']
                elif mutation == 'bad_matrix':
                    m['cameras'][0]['world_to_image_matrix'][0].pop()
                elif mutation == 'nonfinite':
                    m['target_pixels'][0]['pixel'][0] = float('nan')
                elif mutation == 'outside_image':
                    m['target_pixels'][0]['pixel'][0] = 1536
                elif mutation == 'singular':
                    m['cameras'][2]['world_to_image_matrix'] = copy.deepcopy(m['cameras'][0]['world_to_image_matrix'])
                elif mutation == 'changed_reference':
                    m['recorded_svd_world'][0] += 1
                else:
                    m['target_pixels'][0]['pixel'][0] += 10
                with self.assertRaises((ValueError, KeyError)):
                    photo.replay(d, 'gi5')

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional retained evidence not configured')
    def test_retained_photos_fits_and_analysis_hashes(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        for record in self.data['photo_sources'] + self.data['retained_fits'] + self.data['retained_analysis']:
            self.assertEqual(sha(root / record['path']), record['sha256'], record['path'])

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'optional texture source not configured')
    def test_retained_vpw_texture_hash(self):
        texture = self.data['texture']
        self.assertEqual(sha(Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / texture['path']), texture['sha256'])


if __name__ == '__main__':
    unittest.main()
