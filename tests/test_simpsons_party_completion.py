import hashlib
import json
import math
import os
from pathlib import Path
import sys
import re
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from unittest import mock

import curate_simpsons_party as curator
import drawing_callouts
import simpsons_party_photogrammetry as photo
from pinmame_game_defs.jsonio import canonical_bytes


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_least_squares(rows, values):
    """Solve the small normal equations independently of the curator."""
    matrix = [[sum(row[i] * row[j] for row in rows) for j in range(3)] +
              [sum(row[i] * value for row, value in zip(rows, values))] for i in range(3)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(matrix[r][col]))
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        if abs(matrix[col][col]) < 1e-12:
            raise ValueError('degenerate fit')
        divisor = matrix[col][col]
        matrix[col] = [v / divisor for v in matrix[col]]
        for row in range(3):
            if row != col:
                factor = matrix[row][col]
                matrix[row] = [v - factor * p for v, p in zip(matrix[row], matrix[col])]
    return [row[3] for row in matrix]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    points = sorted(set(map(tuple, points)))
    def half(sequence):
        result = []
        for p in sequence:
            while len(result) >= 2 and cross(result[-2], result[-1], p) <= 0:
                result.pop()
            result.append(p)
        return result
    return half(points)[:-1] + half(reversed(points))[:-1]


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(curator.MEASUREMENTS_PATH.read_text(encoding='utf-8'))

    def test_lamp16_calibration_and_interpolation(self):
        d = self.data['lamp16']
        self.assertEqual(d['points'], [[189, 608], [243, 609]])
        self.assertIn('leader endpoints', d['point_kind'])
        self.assertEqual(d['uncertainty_normalized'], 0.02)
        w, h = d['table_bounds']
        controls = [(tuple(c['pixel']), (c['vpx_center'][0] / w, c['vpx_center'][1] / h))
                    for c in d['controls']]
        self.assertGreaterEqual(len(controls), 4)
        ys = [xy[1] for _, xy in controls]
        self.assertGreaterEqual(max(ys) - min(ys), 0.5)
        self.assertLess(max(drawing_callouts.leave_one_out(controls)), 0.023)
        hull = convex_hull([point for point, _ in controls])
        self.assertGreaterEqual(len(hull), 3)
        for point in d['points']:
            self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], point) >= 0
                                for i in range(len(hull))))
        positions = curator.lamp16_measurement()
        self.assertEqual(positions, [(0.123, 0.506), (0.236, 0.507)])
        self.assertEqual(len(set(positions)), 2)

    def test_backpanel_projective_fit(self):
        d = self.data['backpanel']
        self.assertEqual(d['physical_count'], 10)
        points = d['pixel_centres']
        matches = d['second_elevation_pixel_x']
        self.assertEqual(len(matches), 8)
        left, right = d['panel_extent_on_second_elevation']
        rows, targets = [], []
        for index, v in matches.items():
            x = (v - left) / (right - left)
            u = points[int(index)][0]
            rows.append([u, 1, -u * x])
            targets.append(x)
        a, b, c = solve_least_squares(rows, targets)
        for actual, expected in zip((a, b, c), d['coefficients']):
            self.assertAlmostEqual(actual, expected, places=11)
        project = lambda u: (a * u + b) / (c * u + 1)
        self.assertLess(max(abs(project(row[0]) - x) for row, x in zip(rows, targets)), 0.003)
        us = [row[0] for row in rows]
        self.assertTrue(all(min(us) <= p[0] <= max(us) for p in points))
        positions = [(round(project(u), 2), 0) for u, _ in points]
        self.assertEqual(curator.backpanel_measurement(), positions)
        self.assertEqual(len(set(positions)), 10)
        self.assertEqual(d['round_decimals'], 2)
        self.assertEqual(d['plane_y'], 0)
        self.assertIn('y=-4.0773', d['plane_basis'])
        self.assertIn('Clamp', d['plane_basis'])

    def test_upper_gi_fit_and_six_modelled_socket_controls(self):
        root = curator.ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003'
        d = json.loads((root / 'upper-gi.json').read_text(encoding='utf-8'))
        components = json.loads((root / 'vpx-components.json').read_text(encoding='utf-8'))
        w, h = d['table_bounds']
        self.assertEqual([w, h], [952.94, 2117.65])
        self.assertEqual(len(d['controls']), 12)
        controls = [(tuple(c['pixel']), (c['world'][0] / w, c['world'][1] / h)) for c in d['controls']]
        transform = drawing_callouts.fit(controls)
        self.assertLess(max(drawing_callouts.leave_one_out(controls)), 0.01)
        for row, coeffs in enumerate(transform):
            for actual, original in zip(coeffs, d['affine_pixel_to_world'][row]):
                self.assertAlmostEqual(actual, original / (w if row == 0 else h), places=11)
        missing = next(g for g in d['gi'] if g['nearest_model_gi'] is None)
        hull = convex_hull([point for point, _ in controls])
        self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], missing['pixel']) >= 0
                            for i in range(len(hull))))
        self.assertEqual(tuple(round(v, 2) for v in drawing_callouts.apply(transform, missing['pixel'])), (0.25, 0.01))
        self.assertEqual(curator.upper_gi_measurement(), (0.25, 0.01))
        by_name = {c['object']: c for c in components['gi_emitters']}
        matched = [g for g in d['gi'] if g['nearest_model_gi'] is not None]
        self.assertEqual(len(matched), 6)
        self.assertEqual(len({g['nearest_model_gi'] for g in matched}), 6)
        for g in matched:
            center = by_name[g['nearest_model_gi']]['center']
            model = (center['x'] / w, center['y'] / h)
            manual = drawing_callouts.apply(transform, g['pixel'])
            self.assertLess(math.dist(model, manual), 0.02, g['description'])
        self.assertIn('keep their VPW geometry', d['coordinate_rule'])

    def test_mode_front_window_triangulation_and_comparison(self):
        root = curator.ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003'
        d = json.loads((root / 'mode-sign.json').read_text(encoding='utf-8'))
        calibrated = json.loads((root / 'photogrammetry.json').read_text(encoding='utf-8'))
        self.assertEqual(d['cameras'], calibrated['measurements']['gi5']['cameras'])
        self.assertAlmostEqual(d['calibration_rms_px'], 1.2513070149511378)
        self.assertIn('not the unseen circuit board/base', d['method'])
        self.assertIn('Do not silently treat front-window centers as base/PCB centers', d['limits'])
        results = {}
        for record in d['records']:
            point, reprojections = photo.triangulate(d['cameras'], record['target_pixels'], d['image_size'])
            xy = [point[i] / d['table_bounds'][i] for i in (0, 1)]
            self.assertLess(math.dist(xy, record['normalized_xy']), 0.0005)
            for actual, expected in zip(reprojections, record['reprojections']):
                self.assertLess(abs(actual['residual_px'] - expected['residual_px']), 0.05)
                self.assertTrue(4.0 < actual['residual_px'] < 6.5)
            results[record['side']] = xy
        self.assertEqual(set(results), {'left', 'right'})
        self.assertLess(math.dist(results['left'], (0.583, 0.071)), 0.001)
        self.assertLess(math.dist(results['right'], (0.645, 0.070)), 0.001)
        for side in ('left', 'right'):
            new = d['comparison']['new_vpw_' + side]
            self.assertLess(abs(results[side][1] - new[1]), abs(results[side][1] - d['comparison']['old_vpw_y']))
            self.assertGreater(abs(results[side][1] - new[1]), 0.005)
        self.assertLess(math.dist(results['left'], d['comparison']['new_vpw_left']),
                        math.dist(results['left'], (0.5763, d['comparison']['old_vpw_y'])))

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional review artifacts not configured')
    def test_mode_front_sources_and_original_measurement_hashes(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        path = curator.ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003/mode-sign.json'
        d = json.loads(path.read_text(encoding='utf-8'))
        for item in d['input_fits'] + d['target_read_grids'] + d['retained_analysis'] + d['photo_sources']:
            self.assertEqual(sha(root / item['path']), item['sha256'], item['path'])
        source = json.loads((root / d['retained_analysis'][0]['path']).read_text(encoding='utf-8'))
        self.assertEqual(d['records'], source['records'])
        self.assertEqual(d['cameras'], source['cameras'])

    def test_vpw_manifest_rejects_changed_content_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / curator.VPW_RELATIVE_PATH
            for folder in ('extracted', 'world-obj', 'source'):
                (base / folder).mkdir(parents=True)
            table = base / 'source/Simpsons Pinball Party, The (Stern 2003) VPW 2.0.vpx'
            script = base / 'extracted/script.vbs'
            obj = base / 'world-obj/Simpsons Pinball Party, The (Stern 2003) VPW 2.0.obj'
            for path, content in ((table, b'table'), (script, b'script'), (obj, b'object')):
                path.write_bytes(content)
            hashes = {}
            for folder in ('extracted', 'world-obj'):
                raw = canonical_bytes(curator.build_extraction_manifest(base / folder))
                (base / f'{folder}.manifest.json').write_bytes(raw)
                hashes[folder] = hashlib.sha256(raw).hexdigest()
            pins = {'VPW_MANIFEST_SHA256': hashes['extracted'], 'VPW_WORLD_MANIFEST_SHA256': hashes['world-obj'],
                    'VPW_TABLE_SHA256': sha(table), 'VPW_SCRIPT_SHA256': sha(script), 'VPW_OBJ_SHA256': sha(obj)}
            with mock.patch.multiple(curator, **pins):
                curator.verify_vpw(root)
                script.write_bytes(b'changed')
                with self.assertRaisesRegex(RuntimeError, 'extraction identity differs'):
                    curator.verify_vpw(root)
                script.write_bytes(b'script')
                with mock.patch.object(curator, 'VPW_MANIFEST_SHA256', '0' * 64):
                    with self.assertRaisesRegex(RuntimeError, 'extraction identity differs'):
                        curator.verify_vpw(root)

    def test_gi_inventory_keeps_physical_sockets_and_excludes_shafts(self):
        gi = curator.gi_outputs()[0]
        points = gi['spatial']['placements']
        self.assertEqual(51, gi['physical']['quantity'])
        self.assertEqual(49, len(points))
        self.assertEqual(49, len({p['id'] for p in points}))
        self.assertEqual(49, len({(p['x'], p['y']) for p in points}))
        self.assertNotIn('GI_030', curator.GI_BULB_OBJECTS)
        self.assertNotIn('GI_053', curator.GI_BULB_OBJECTS)
        self.assertNotIn('GI_032', curator.GI_BULB_OBJECTS)
        self.assertNotIn('GI_31', curator.GI_BULB_OBJECTS)
        self.assertIn('GI_040', curator.GI_BULB_OBJECTS)
        self.assertNotIn('GI_043', curator.GI_BULB_OBJECTS)
        for xy in ((.18, .19), (.25, .01), (.34, .26), (.80, .77), (.80, .78), (.11, .78), (.17, .32), (.69, .82)):
            self.assertIn(xy, {(p['x'], p['y']) for p in points})
        self.assertEqual(10, sum(p['y'] == 0 for p in points))
        self.assertEqual(2, sum(curator.EXPOSED_SOCKETS_SOURCE in p['provenance']['source_refs'] for p in points))
        for phrase in ('European one-bulb', '40 GI #44', '41 GI bayonets', 'total 43', 'not a universal'):
            self.assertIn(phrase, gi['physical']['notes'])

    def test_exposed_socket_registration_is_interpolated_identity_evidence(self):
        d = json.loads(curator.EXPOSED_SOCKETS_PATH.read_text(encoding='utf-8'))
        self.assertEqual('hawkeyexx', d['photo']['author'])
        self.assertEqual(7481, d['photo']['post_number'])
        self.assertEqual(162, len(d['inliers']))
        h = d['homography_source_uv_to_photo']
        def project(point):
            vector = [*point, 1]
            xyz = [sum(a * b for a, b in zip(row, vector)) for row in h]
            return [xyz[0] / xyz[2], xyz[1] / xyz[2]]
        residuals = sorted(math.dist(project(p['source_uv']), p['photo_xy']) for p in d['inliers'])
        self.assertLess(residuals[len(residuals) // 2], .7)
        self.assertLess(max(residuals), 4)
        hull = convex_hull([p['source_uv'] for p in d['inliers']])
        for point in d['targets']:
            uv = point['source_uv']
            self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], uv) >= 0 for i in range(len(hull))))
            self.assertLess(math.dist(project(uv), point['projected_photo_pixels']), .001)
        self.assertIn('not independent accuracy controls', d['interpretation'])
        self.assertIn('not an invariant factory quantity', d['physical_review']['limits'])

    def test_shaft_identity_crosschecks_replay_with_extrapolation_disclosed(self):
        d = json.loads(curator.GI_HARDWARE_PATH.read_text(encoding='utf-8'))
        shafts = d['shaft_checks']
        h = shafts['world_to_photo']
        self.assertEqual({'GI_030', 'GI_053'}, {p['model_light'] for p in shafts['observations']})
        for point in shafts['observations']:
            vector = [*point['model_light_world'], 1]
            xyz = [sum(a * b for a, b in zip(row, vector)) for row in h]
            xy = [xyz[0] / xyz[2], xyz[1] / xyz[2]]
            self.assertLess(math.dist(xy, point['model_ground_projection']), .0001)
            residual = math.dist(xy, point['observed_wood_plane_contact_native_pixel'])
            self.assertAlmostEqual(residual, point['projection_pixel_residual'], places=5)
            self.assertLess(residual, point['pixel_read_uncertainty'])
        self.assertTrue(any('extrapolated' in item for item in shafts['limits']))
        other = d['independent_owner_gi007']
        self.assertEqual('Sandman454', other['author'])
        self.assertIn('514', other['limitations'])
        self.assertIn('not a validated coordinate', other['limitations'])

    def test_cbg_gi_factory_symbol_is_calibrated_inside_control_hull(self):
        d = json.loads(curator.GI_CBG_SYMBOL_PATH.read_text(encoding='utf-8'))
        self.assertEqual('GI circuit bulb symbol centre', d['point_kind'])
        self.assertEqual(16, len(d['controls']))
        rows = [[*c['world'], 1] for c in d['controls']]
        fit = [solve_least_squares(rows, [c['pixel'][i] for c in d['controls']]) for i in (0, 1)]
        for expected, actual in zip(d['world_to_source_crop_affine'], fit):
            for a, b in zip(expected, actual):
                self.assertAlmostEqual(a, b, places=8)
        world = d['world_xy']
        point = d['symbol_center_source_crop']
        predicted = [sum(a * b for a, b in zip(row, [*world, 1])) for row in fit]
        self.assertLess(math.dist(point, predicted), .00001)
        hull = convex_hull([c['world'] for c in d['controls']])
        self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], world) >= 0 for i in range(len(hull))))
        ys = [c['world'][1] for c in d['controls']]
        self.assertGreater((max(ys) - min(ys)) / d['texture']['world_bounds'][1], .5)
        self.assertEqual((.17, .32), curator.gi_cbg_measurement())
        self.assertEqual([.05, .05], d['uncertainty']['coarse_factory_projection_bound_proposed'])
        self.assertIn('no native raster DPI', d['source']['reference_render_note'])

    def test_cbg_flasher_plan_reconciliation_preserves_factory_construction(self):
        d = json.loads(curator.CBG_FLASHER_PATH.read_text(encoding='utf-8'))
        self.assertEqual(10, len(d['controls']))
        self.assertGreater(d['normalized_control_span'][1], .5)
        fit = drawing_callouts.fit([(c['world_xy'], c['native_pixel']) for c in d['controls']])
        for expected, actual in zip(d['affine_world_to_native'], fit):
            for a, b in zip(expected, actual):
                self.assertAlmostEqual(a, b, places=9)
        target = d['target_cover29_native_pixel']
        hull = convex_hull([c['native_pixel'] for c in d['controls']])
        self.assertTrue(all(cross(hull[i], hull[(i + 1) % len(hull)], target) >= 0 for i in range(len(hull))))
        xy = [d['old_f29a_world_xy'][i] / d['old_source_bounds'][i] for i in (0, 1)]
        self.assertEqual([round(v, 6) for v in xy], list(curator.SOLENOID_POSITIONS[29][0]))
        modeled = [xy[i] * [952.94, 2117.65][i] for i in (0, 1)]
        projected = drawing_callouts.apply(fit, modeled)
        self.assertLess(math.dist(projected, d['old_bulb_native_projected']), .0001)
        for observed, expected in zip([target[i] - projected[i] for i in (0, 1)], d['target_minus_model_native_px']):
            self.assertAlmostEqual(observed, expected, places=7)
        self.assertLess(max(map(abs, d['inverse_minus_modeled_normalized'])), .01)
        self.assertIn('below playfield', d['construction_correction'])

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional review artifacts not configured')
    def test_exposed_socket_photo_and_registration_sources(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        d = json.loads(curator.EXPOSED_SOCKETS_PATH.read_text(encoding='utf-8'))
        for source in (d['photo'], d['retained_analysis']):
            self.assertEqual(source['sha256'], sha(root / source['path']))
        original = json.loads((root / d['retained_analysis']['path']).read_text(encoding='utf-8'))
        for key in ('inliers', 'targets', 'homography_source_uv_to_photo'):
            self.assertEqual(original[key], d[key])
        hardware = json.loads(curator.GI_HARDWARE_PATH.read_text(encoding='utf-8'))
        for source in (hardware['shaft_checks']['source_photo'], hardware['shaft_checks']['homography_input']):
            self.assertEqual(source['sha256'], sha(root / source['path']))
        other = hardware['independent_owner_gi007']
        self.assertEqual(other['photo_sha256'], sha(root / 'the-simpsons-pinball-party-2003/completion-20261029/club-gallery' / other['photo_file']))
        wire_passages = hardware['wire_passages']
        for source in (wire_passages['GI_032']['source_photo'], wire_passages['GI_032']['identity_registration'],
                       wire_passages['GI_032']['retained_measurement'], wire_passages['GI_31']['primary_photo'],
                       wire_passages['GI_31']['second_photo'], wire_passages['GI_31']['retained_measurement']):
            self.assertEqual(source['sha256'], sha(root / source['path']))

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional review artifacts not configured')
    def test_all_review_artifact_hashes(self):
        root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT'])
        for artifact in self.data['artifacts']:
            self.assertEqual(artifact['root'], 'review')
            self.assertEqual(sha(root / artifact['path']), artifact['sha256'], artifact['path'])
        cbg = json.loads(curator.CBG_FLASHER_PATH.read_text(encoding='utf-8'))
        for artifact in (cbg['source_render'], cbg['retained_measurement']):
            self.assertEqual(sha(root / artifact['path']), artifact['sha256'])
        gi = json.loads(curator.GI_CBG_SYMBOL_PATH.read_text(encoding='utf-8'))
        self.assertEqual(sha(root / gi['retained_measurement']['path']), gi['retained_measurement']['sha256'])
        base = root / 'the-simpsons-pinball-party-2003/completion-20261029'
        for path, digest in ((gi['source']['rendered_crop'], gi['source']['rendered_crop_sha256']),
                             (gi['source']['reference_render_150dpi'], gi['source']['reference_render_sha256'])):
            self.assertEqual(sha(base / path), digest)

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'optional VPX sources not configured')
    def test_retained_vpw_manifests_world_geometry_and_bindings(self):
        root = Path(os.environ['PINMAME_VPX_SOURCES_ROOT'])
        curator.verify_vpw(root)
        base = root / curator.VPW_RELATIVE_PATH
        table = json.loads((base / 'extracted/gamedata.json').read_text(encoding='utf-8'))
        self.assertEqual([table[k] for k in ('left', 'top', 'right', 'bottom')], [0, 0, 952.94, 2117.65])
        components = json.loads(curator.VPW_COMPONENTS_PATH.read_text(encoding='utf-8'))
        gi = json.loads(curator.GI_CBG_SYMBOL_PATH.read_text(encoding='utf-8'))
        for control in gi['controls']:
            if 'source_uv' in control:
                for value, pixel, size, bound in zip(control['world'], control['source_uv'], gi['texture']['size'], gi['texture']['world_bounds']):
                    self.assertAlmostEqual(value, pixel / size * bound, places=8)
            else:
                kind = 'Bumper' if control['name'].startswith('Bumper') else 'Light'
                path = base / 'extracted/gameitems' / f"{kind}.{control['name']}.json"
                item = json.loads(path.read_text(encoding='utf-8'))[kind]
                self.assertEqual(control['world'], [item['center']['x'], item['center']['y']])
                if 'world_source_sha256' in control:
                    self.assertEqual(control['world_source_sha256'], sha(path))
        for item in components['gi_emitters']:
            path = base / 'extracted/gameitems' / f"Light.{item['object']}.json"
            self.assertEqual(item['object_sha256'], sha(path))
            light = json.loads(path.read_text(encoding='utf-8'))['Light']
            self.assertTrue(light['show_bulb_mesh'])
            self.assertEqual(item['center'], light['center'])
            self.assertEqual(item['surface'], light['surface'])
        for fixture in components['flashers']:
            path = base / 'extracted/gameitems' / f"Primitive.{fixture['object']}.json"
            self.assertEqual(fixture['object_sha256'], sha(path))
        names = {f'l{n}' for n in range(73, 81)} | {'l80b', 'LEDOff', 'backwall_gion'}
        obj = base / 'world-obj/Simpsons Pinball Party, The (Stern 2003) VPW 2.0.obj'
        bounds = curator.world_bounds(obj, names)
        def centre(name):
            lo, hi = bounds[name]
            return tuple((lo[i] + hi[i]) / 2 for i in range(3))
        for n in range(73, 81):
            sources = [f'l{n}'] + (['l80b'] if n == 80 else [])
            xy = [(round(centre(name)[0] / table['right'], 6),
                   round(centre(name)[1] / table['bottom'], 6)) for name in sources]
            self.assertEqual(xy, curator.MODE_SIGN_LAMP_POSITIONS[n])
        self.assertAlmostEqual(centre('LEDOff')[0], 412.249985, places=5)
        self.assertAlmostEqual(centre('LEDOff')[1], 172.5, places=5)
        self.assertAlmostEqual(centre('backwall_gion')[1], -4.0773, delta=0.0001)
        script = (base / 'extracted/script.vbs').read_text(encoding='utf-8')
        callbacks = re.findall(r'^\s*Lampz\.Callback\(80\)\s*=\s*"DisableLighting\s+(l80b?),\s*5,"',
                               script, re.IGNORECASE | re.MULTILINE)
        self.assertEqual([name.lower() for name in callbacks], ['l80', 'l80b'])
        setter = re.search(r'^\s*Public Property Let Callback\(idx, String\)(.*?)End Property',
                           script, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(setter)
        self.assertRegex(setter.group(1), r'(?im)^\s*cCallback\(idx\)\s*=\s*cCallback\(idx\)\s*&\s*"___"\s*&\s*String')


if __name__ == '__main__':
    unittest.main()
