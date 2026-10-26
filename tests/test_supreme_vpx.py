from __future__ import annotations

import copy
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import curate_spike1
import curate_supreme_x_stern_2018 as curator


class SupremeVpxTests(unittest.TestCase):
    def setUp(self):
        self.definition = load_json(ROOT / 'machines/partial/stern/supreme-x-stern-2018.json')

    def test_reproducible_mapping_preserves_shared_positions_and_physical_unknowns(self):
        curator.check(ROOT)
        mapping = load_json(ROOT / curator.MAPPING)
        inputs = {d['id']: d for d in self.definition['inputs']}
        outputs = {d['id']: d for d in self.definition['outputs']}
        self.assertEqual({'vpx-left-slingshot-wall', 'vpx-right-slingshot-wall'},
                         {p['id'] for p in inputs['sw.6']['spatial']['placements']})
        self.assertEqual(2, len(inputs['sw.37']['spatial']['placements']))
        self.assertEqual(2, len(outputs['sol.5']['spatial']['placements']))
        self.assertEqual(2, len(outputs['sol.7']['spatial']['placements']))
        self.assertNotIn('spatial', inputs['sw.22'])
        self.assertNotIn('spatial', outputs['sol.51'])
        for device in outputs.values():
            if device['binding']['group'] == 'pinmame.output.lamp':
                self.assertNotIn('placements', device.get('spatial', {}))
        for _, identifier, _, entry in curator.placements(mapping):
            self.assertTrue(0 <= entry['x'] <= 1 and 0 <= entry['y'] <= 1, identifier)

    def test_curator_refuses_coordinate_source_and_inventory_drift(self):
        report = curate_spike1.spatial_report(self.definition)
        for mutate in ('coordinate', 'source', 'extra'):
            changed = copy.deepcopy(self.definition)
            if mutate == 'source':
                next(s for s in changed['sources'] if s['id'] == 'supreme.vpx.table.008')['sha256'] = '0' * 64
            else:
                shooter = next(d for d in changed['inputs'] if d['id'] == 'sw.1')
                if mutate == 'coordinate':
                    shooter['spatial']['placements'][0]['x'] = 0.5
                else:
                    next(d for d in changed['inputs'] if d['id'] == 'sw.22')['spatial'] = copy.deepcopy(shooter['spatial'])
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                curator.enrich_spatial_report(ROOT, changed, copy.deepcopy(report))

    def test_declared_missing_external_root_fails_instead_of_skipping(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {'PINMAME_VPX_SOURCES_ROOT': folder}):
                with self.assertRaises((OSError, ValueError)):
                    curator.verify_external_evidence(ROOT)

    @unittest.skipUnless(os.environ.get('PINMAME_VPX_SOURCES_ROOT'), 'Retained VPX root is optional')
    def test_all_coordinates_manifest_and_script_contract_match_exact_retained_table(self):
        curator.verify_external_evidence(ROOT)
        path = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / curator.EXTRACTION / 'script.vbs'
        script = path.read_text(encoding='utf-8')
        bindings = {int(n): name for n, name in re.findall(r'^SolCallback\((\d+)\)\s*=\s*"([^"]+)"', script, re.MULTILINE | re.IGNORECASE)}
        self.assertEqual({1: 'SolRelease', 2: 'SolAutoPlungerIM', 3: 'SolLFlipper', 4: 'SolRFlipper',
                          5: 'SolSlings', 7: 'SolPopsLR', 8: 'SolPopBottom', 9: 'SolDTBank123', 10: 'SolControlGate'}, bindings)
        self.assertIn('Const ControlGateCoilCloses = True', script)
        self.assertIn('Flip ControlGateCoilCloses if the ROM', script)


if __name__ == '__main__':
    unittest.main()
