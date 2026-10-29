import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from simpsons_party_right_return import boundary_digest, replay


REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / 'tools/seeds/stern/the-simpsons-pinball-party-2003/right-return.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RightReturnEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads(EVIDENCE.read_text(encoding='utf-8'))

    def test_replays_all_thresholds_and_socket_projection(self):
        evidence = self.evidence
        result = replay(evidence)
        self.assertEqual(result['coarse_xy'], [0.80, 0.78])
        self.assertEqual(len(result['circle_centers_uv']), 4)
        for center, measurement in zip(result['circle_centers_uv'], evidence['measurements']):
            self.assertLess(math.dist(center, measurement['ellipse_center']), 0.01)
        self.assertLess(math.dist(result['mean_uv'], [1479.426275253296, 3195.5925006866455]), 0.01)
        self.assertAlmostEqual(result['world_xy'][0], result['normalized_xy'][0] * 952.94)
        self.assertAlmostEqual(result['world_xy'][1], result['normalized_xy'][1] * 2117.65)
        self.assertGreater(math.dist(result['world_xy'], evidence['existing_lower_source_position']['world_xy']), 40)
        self.assertEqual(evidence['normalized_allowance'], [0.02, 0.02])
        check = evidence['photo_homography_crosscheck']
        self.assertLess(check['target_signed_distance_from_control_hull_px'], 0)
        self.assertIn('extrapolated', check['status'])
        self.assertIn('not the original filament', evidence['limitations'])
        self.assertIn('underboard mounting', evidence['limitations'])
        self.assertIn('brass cylindrical shell/collar', evidence['limitations'])

    def test_rejects_changed_contour_digest_dimensions_and_reference(self):
        mutations = []
        e = copy.deepcopy(self.evidence)
        e['measurements'][0]['boundary_pixels'][0][0] += 1
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['measurements'][0]['boundary_pixels'][0][0] += 50
        e['measurements'][0]['boundary_sha256'] = boundary_digest(e['measurements'][0]['boundary_pixels'])
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['measurements'][0]['boundary_sha256'] = '0' * 64
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['source_texture']['sha256'] = '0' * 64
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['source_texture']['size'][0] += 1
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['normalized_xy'][0] += 0.001
        mutations.append(e)
        e = copy.deepcopy(self.evidence)
        e['measurements'][1]['threshold'] = 36
        mutations.append(e)
        for evidence in mutations:
            with self.subTest(evidence=evidence.get('normalized_xy')):
                with self.assertRaises(ValueError):
                    replay(evidence)

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'VPX sources root not configured')
    def test_texture_hash_and_selected_contour_pixels(self):
        from PIL import Image
        record = self.evidence['source_texture']
        texture = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / record['path']
        self.assertEqual(digest(texture), record['sha256'])
        image = Image.open(texture).convert('L')
        self.assertEqual(list(image.size), record['size'])
        for item in self.evidence['measurements']:
            for x, y in item['boundary_pixels']:
                self.assertLess(image.getpixel((x, y)), item['threshold'])
                self.assertTrue(any(image.getpixel((x + dx, y + dy)) >= item['threshold']
                                    for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                    if dx or dy))

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'review artifacts root not configured')
    def test_retained_source_hashes_and_ellipse_measurements(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        owner = self.evidence['physical_owner_source']
        for record in [owner['photo'], owner['manifest'], *self.evidence['retained_analysis']]:
            with self.subTest(path=record['path']):
                self.assertEqual(digest(root / record['path']), record['sha256'])
        raw = json.loads((root / self.evidence['retained_analysis'][0]['path']).read_text(encoding='utf-8'))
        for compact, measured in zip(self.evidence['measurements'], raw['source_annulus_measurements']):
            self.assertEqual(compact['threshold'], measured['threshold'])
            self.assertEqual(compact['ellipse_center'], measured['source_center'])
        manifest = json.loads((root / owner['manifest']['path']).read_text(encoding='utf-8'))
        photo = next(p for p in manifest['photos'] if p['index'] == 14)
        self.assertEqual(photo['sha256'], owner['photo']['sha256'])
        self.assertEqual(photo['url'], owner['photo_url'])


if __name__ == '__main__':
    unittest.main()
