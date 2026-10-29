import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import curate_simpsons_party as curator
import simpsons_party_left_return as anchor
from test_simpsons_party_completion import convex_hull, cross


class LeftReturnTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(curator.LEFT_RETURN_PATH.read_text(encoding='utf-8'))

    def test_own_annulus_and_interpolated_photo_identity(self):
        d = self.data
        result = anchor.replay(d)
        self.assertEqual([.11, .78], result['coarse_xy'])
        self.assertLess(math.dist(result['center_uv'], [199.36, 3201.45]), .05)
        fit = d['photo_registration']
        h = fit['texture_to_photo']
        def project(point):
            q = [sum(a * b for a, b in zip(row, [*point, 1])) for row in h]
            return [q[0] / q[2], q[1] / q[2]]
        residuals = [math.dist(project(p['texture']), p['photo']) for p in fit['inlier_pairs']]
        self.assertEqual(160, len(residuals))
        self.assertLess(max(residuals), 2.75)
        self.assertAlmostEqual(math.sqrt(sum(r * r for r in residuals) / len(residuals)), fit['residual_px']['rms'], places=7)
        hull = convex_hull([p['texture'] for p in fit['inlier_pairs']])
        point = result['center_uv']
        self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], point) >= 0 for i in range(len(hull))))
        self.assertIn('separate physical emitter', d['physical_identity'])

    def test_changed_boundary_is_rejected(self):
        d = copy.deepcopy(self.data)
        d['replayed_boundaries'][0]['pixels'][0][0] += 1
        with self.assertRaisesRegex(ValueError, 'boundary identity'):
            anchor.replay(d)

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'optional VPX source not configured')
    def test_source_pixels_reproduce_every_annulus_boundary(self):
        from PIL import Image
        path = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / self.data['source_texture']['path']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.data['source_texture']['sha256'])
        with Image.open(path) as source:
            gray = source.convert('L')
            for item in self.data['replayed_boundaries']:
                self.assertEqual(item['pixels'], anchor.boundary(gray.getpixel, self.data['source_annulus_roi_native_pixels'], item['threshold']))

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional review root not configured')
    def test_physical_photo_and_retained_analysis_hashes(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        for source in (self.data['physical_owner_photo'], self.data['retained_measurement']):
            self.assertEqual(hashlib.sha256((root / source['path']).read_bytes()).hexdigest(), source['sha256'])


if __name__ == '__main__':
    unittest.main()
