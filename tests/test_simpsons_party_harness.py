import base64
import hashlib
import json
import ntpath
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import simpsons_party_harness as adapter


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003/lamp-service.json'
RETAINED = Path('the-simpsons-pinball-party-2003/completion-20261029')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derive_observations(trace):
    if trace['format'] != 'pinmame-harness-run' or trace['game'] != 'simpprty' or trace['failure'] is not None:
        raise ValueError('not a successful simpprty run')
    selected = [s for s in trace['steps'] if s['label'].startswith('single lamp forward step ')]
    all_lamps = [s for s in trace['steps'] if s['label'] == 'all-lamp cycle observation']
    if len(selected) != 82 or len(all_lamps) != 1:
        raise ValueError('incomplete service walk')
    def states(steps, state):
        return sorted({v['number'] for s in steps for v in s['transitions']['lamps'] if state in v['states']})
    checkpoints = []
    for s in trace['steps']:
        if s['type'] != 'pulse_until_display':
            continue
        title = s['matched_text']
        snapshot = next(x for x in trace['snapshots'] if x['label'] == s['label'])
        display = snapshot['displays'][0]
        checkpoints.append({'step': s['step'], 'title': title, 'pulses': s['pulses'],
                            'frame': ntpath.basename(display['artifact']), 'pixel_sha256': display['pixel_sha256']})
    return {'single_walk_steps': len(selected), 'single_active': states(selected, 1),
            'single_inactive': states(selected, 0), 'all_active': states(all_lamps, 1),
            'all_inactive': states(all_lamps, 0), 'checkpoints': checkpoints}


class HarnessEvidenceTests(unittest.TestCase):
    def test_compact_evidence_and_repo_pins(self):
        e = json.loads(EVIDENCE.read_text(encoding='utf-8'))
        expected = list(range(1, 81))
        for field in ('single_active', 'single_inactive', 'all_active', 'all_inactive'):
            self.assertEqual(e['observations'][field], expected)
        self.assertEqual(e['observations']['single_walk_steps'], 82)
        self.assertEqual([c['title'] for c in e['observations']['checkpoints']], list(adapter.TEMPLATES))
        for pin in e['repo_inputs']:
            self.assertEqual(sha(ROOT / pin['path']), pin['sha256'])

    def test_adapter_rejects_corruption_and_unknown_screens(self):
        for title, template in adapter.TEMPLATES.items():
            frame = bytearray(128 * 32)
            mask = base64.b64decode(template['mask'])
            n = 0
            for y in range(template['rows'][0], template['rows'][1] + 1):
                for x in range(template['cols'][0], template['cols'][1] + 1):
                    frame[y * 128 + x] = mask[n] * 255
                    n += 1
            self.assertIn(title, adapter.match_titles(frame, 128, 32))
            frame[template['rows'][0] * 128 + template['cols'][0]] ^= 255
            self.assertNotIn(title, adapter.match_titles(frame, 128, 32))
        self.assertEqual(adapter.match_titles(bytes(4096), 128, 32), [])
        self.assertEqual(adapter.match_titles(bytes(4095), 128, 32), [])
        self.assertEqual(adapter.match_titles(bytes(4096), 64, 64), [])

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'optional retained trace not configured')
    def test_retained_trace_and_frames(self):
        e = json.loads(EVIDENCE.read_text(encoding='utf-8'))
        retained = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']) / RETAINED
        trace_path = retained / 'lamp-service-1.json'
        self.assertEqual(sha(trace_path), e['trace']['sha256'])
        trace = json.loads(trace_path.read_text(encoding='utf-8'))
        self.assertEqual(trace['handle_mechanics'], 0)
        self.assertEqual(trace['switch_converter'], 'sequential')
        self.assertEqual(trace['initial_switches'], [
            {'switch': n, 'state': 1 if n < 15 else 0} for n in range(10, 16)])
        observed = e['observations'].copy()
        observed['checkpoints'] = [{k: v for k, v in c.items() if k != 'pgm_sha256'}
                                   for c in observed['checkpoints']]
        self.assertEqual(derive_observations(trace), observed)
        self.assertEqual(trace['library_sha256'], e['library']['sha256'])
        self.assertEqual(trace['scenario']['sha256'], e['repo_inputs'][0]['sha256'])
        working_root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']).parent
        self.assertEqual(sha(working_root / e['library']['locator']), e['library']['sha256'])
        if os.environ.get('PINMAME_ROM_LIBRARY_ROOT'):
            self.assertEqual(sha(Path(os.environ['PINMAME_ROM_LIBRARY_ROOT']) / e['rom']['archive']),
                             e['rom']['archive_sha256'])
        for checkpoint in e['observations']['checkpoints']:
            frame_path = retained / 'lamp-service-dmd-1' / checkpoint['frame']
            raw = frame_path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), checkpoint['pgm_sha256'])
            header = b'P5\n128 32\n255\n'
            self.assertTrue(raw.startswith(header))
            self.assertEqual(adapter.match_titles(raw[len(header):], 128, 32), [checkpoint['title']])


if __name__ == '__main__':
    unittest.main()
