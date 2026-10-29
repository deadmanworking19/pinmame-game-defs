import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import curate_simpsons_party as curator
from simpsons_party_photogrammetry import replay, triangulate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PartyLampTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(curator.PARTY_GI_PATH.read_text(encoding='utf-8'))
        self.measurement = self.data['measurements']['right-return-unhooded']

    def test_own_cap_projection_is_distinct_and_replayed(self):
        result = replay(self.data, 'right-return-unhooded')
        self.assertEqual([.69, .82], result['coarse_xy'])
        self.assertTrue(all(p['residual_px'] < 3 for p in result['reprojections']))
        primary, _ = triangulate(self.measurement['cameras'],
                                 self.measurement['primary_independent_pixels'], self.data['image_size'])
        self.assertEqual([.69, .82], [round(p / size, 2) for p, size in zip(primary, self.data['table_bounds'])])
        gi = curator.gi_outputs()[0]
        placed = next(p for p in gi['spatial']['placements'] if p['id'].endswith('right-return-unhooded'))
        self.assertEqual((.69, .82), (placed['x'], placed['y']))
        self.assertIn(curator.PARTY_GI_SOURCE, placed['provenance']['source_refs'])
        self.assertGreater(math.dist((placed['x'], placed['y']), (.80, .78)), .1)
        self.assertEqual([.03, .02], self.data['physical_review']['uncertainty_normalized_xy'])

    def test_camera_controls_and_hulls_reconcile(self):
        w, h = self.data['table_bounds']
        point_uv = [self.measurement['recorded_svd_world'][0] / w * 1844,
                    self.measurement['recorded_svd_world'][1] / h * 4096]
        for camera in self.measurement['cameras']:
            errors = []
            for pair in camera['control_pairs']:
                xyz = [pair['uv'][0] / 1844 * w, pair['uv'][1] / 4096 * h, 0, 1]
                q = [sum(a * b for a, b in zip(row, xyz)) for row in camera['world_to_image_matrix']]
                errors.append(math.dist([q[0] / q[2], q[1] / q[2]], pair['pixel']))
            self.assertGreaterEqual(len(errors), 40)
            self.assertAlmostEqual(max(errors), camera['maximum_control_reprojection_px'], places=7)
            self.assertLess(max(errors), 7)
        for controls in self.measurement['controls']:
            hull = controls['hull_uv']
            signs = []
            for a, b in zip(hull, hull[1:] + hull[:1]):
                signs.append((b[0]-a[0]) * (point_uv[1]-a[1]) - (b[1]-a[1]) * (point_uv[0]-a[0]))
            self.assertTrue(all(s >= -1e-5 for s in signs) or all(s <= 1e-5 for s in signs))
            self.assertGreater(controls['signed_target_to_hull_distance_uv_pixels'], 24)

    def test_changed_body_reading_is_rejected(self):
        changed = copy.deepcopy(self.data)
        changed['measurements']['right-return-unhooded']['target_pixels'][0]['pixel'][0] += 50
        with self.assertRaises(ValueError):
            replay(changed, 'right-return-unhooded')

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional retained photos not configured')
    def test_exact_photos_and_calibration_artifacts(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        for item in self.data['photo_sources'] + self.data['retained_artifacts']:
            self.assertEqual(item['sha256'], digest(root / item['path']), item['path'])
        retained = json.loads((root / self.data['retained_artifacts'][0]['path']).read_text(encoding='utf-8'))
        self.assertEqual(retained['target']['pixel_readings'], self.measurement['target_pixels'])
        for camera, actual in zip(self.measurement['cameras'], retained['cameras']):
            self.assertEqual(camera['world_to_image_matrix'], actual['world_to_image_matrix'])

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'optional printed-art source not configured')
    def test_exact_source_texture(self):
        source = self.data['source_texture']
        self.assertEqual(source['sha256'], digest(Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / source['path']))
