import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from simpsons_party_left_socket import gold_component, point_digest, replay


REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / 'tools/seeds/stern/the-simpsons-pinball-party-2003/left-socket.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LeftSocketEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_circle_and_projection(self):
        e = self.evidence
        result = replay(e)
        self.assertLess(math.dist(result['center_uv'], [340.68339710244305, 797.8231108226538]), 1e-6)
        self.assertEqual(result['coarse_xy'], [0.18, 0.19])
        self.assertAlmostEqual(result['world_xy'][0], result['normalized_xy'][0] * 952.94)
        self.assertAlmostEqual(result['world_xy'][1], result['normalized_xy'][1] * 2117.65)
        self.assertLess(math.dist(result['center_uv'], e['segmentation']['axis_midpoint']), 0.38)
        self.assertEqual(e['normalized_uncertainty_bound'], [0.02, 0.02])
        self.assertTrue(any('not the original filament' in limit for limit in e['limits']))
        self.assertIn('does not establish exact factory bulb number', e['photo']['note'])

    def test_rejects_mutated_point_digest_source_and_coordinate(self):
        variants = []
        e = copy.deepcopy(self.evidence)
        e['edge_points_native_uv'][0][0] += 1
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['edge_points_native_uv'][0][0] += 1
        e['edge_points_sha256'] = point_digest(e['edge_points_native_uv'])
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['edge_points_sha256'] = '0' * 64
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['source_texture']['sha256'] = '0' * 64
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['source_texture']['size'][0] += 1
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['normalized_xy'][0] += .001
        variants.append(e)
        e = copy.deepcopy(self.evidence)
        e['circle_center_native_uv'][0] += 1
        variants.append(e)
        for index, variant in enumerate(variants):
            with self.subTest(index=index), self.assertRaises(ValueError):
                replay(variant)

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'VPX sources root not configured')
    def test_source_texture_and_gold_component(self):
        from PIL import Image
        texture = self.evidence['source_texture']
        path = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / texture['path']
        self.assertEqual(digest(path), texture['sha256'])
        image = Image.open(path).convert('RGB')
        self.assertEqual(list(image.size), texture['size'])
        component = gold_component(image.getpixel, self.evidence['segmentation']['roi'])
        self.assertEqual(component['pixels'], self.evidence['segmentation']['pixels'])
        self.assertEqual(component['bbox'], self.evidence['segmentation']['bbox'])
        self.assertEqual(component['axis_midpoint'], self.evidence['segmentation']['axis_midpoint'])

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'review artifacts root not configured')
    def test_retained_photo_and_analysis_pins(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        photo = self.evidence['photo']
        for record in [photo['source'], photo['index'], *self.evidence['retained_analysis']]:
            with self.subTest(path=record['path']):
                self.assertEqual(digest(root / record['path']), record['sha256'])
        index = json.loads((root / photo['index']['path']).read_text(encoding='utf-8'))
        self.assertEqual(index[28]['full'], photo['url'])
        raw = json.loads((root / self.evidence['retained_analysis'][0]['path']).read_text(encoding='utf-8'))
        self.assertEqual(raw['edge_points_native_uv'], self.evidence['edge_points_native_uv'])
        self.assertEqual(raw['segmentation'], self.evidence['segmentation'])


if __name__ == '__main__':
    unittest.main()
