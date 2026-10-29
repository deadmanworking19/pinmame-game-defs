import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import simpsons_party_completion_report as audit


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def placement(identifier, x, y, sources):
    return {'status': 'validated', 'placements': [{'id': identifier, 'role': 'emitter', 'space': 'playfield',
                                                    'x': x, 'y': y, 'provenance': {'source_refs': sources}}]}


class CompletionReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legacy = read(ROOT / 'tools/seeds/stern/the-simpsons-pinball-party-2003-spatial-sources.json')
        cls.vpw = read(EVIDENCE / 'vpx-components.json')
        cls.measurements = read(EVIDENCE / 'completion-measurements.json')
        cls.upper = read(EVIDENCE / 'upper-gi.json')
        cls.photo = read(EVIDENCE / 'photogrammetry.json')

    def setUp(self):
        self.definition = {
            'machine': {'id': 'fixture'}, 'coverage': {'status': 'author_ready', 'missing': []},
            'inputs': [{'id': 'switch', 'label': 'Input', 'kind': 'switch', 'availability': 'used',
                        'binding': {'group': 'switch', 'device': 1},
                        'spatial': placement('switch.point', 0.1, 0.2, ['manual'])}],
            'outputs': [{'id': 'gi', 'label': 'GI', 'kind': 'gi', 'availability': 'used',
                         'binding': {'group': 'pinmame.output.gi', 'device': 0},
                         'physical': {'quantity': 1, 'notes': 'F24 F25 F26 F27'},
                         'spatial': placement('gi.point', 0.3, 0.4, ['fixture'])},
                        {'id': 'virtual', 'kind': 'virtual', 'availability': 'unused',
                         'binding': {'group': 'lamp', 'device': 81},
                         'spatial': {'status': 'not_applicable', 'reason': 'virtual',
                                     'provenance': {'source_refs': ['manual']}}}],
            'displays': [{'id': 'screen', 'label': 'Screen', 'kind': 'video', 'controller_index': 3,
                          'spatial': placement('screen.point', 0.5, 0.6, ['mesh'])}],
            'conflicts': [],
        }

    def build(self, definition=None):
        return audit.build_report(definition or self.definition, legacy_report=self.legacy, vpw_components=self.vpw,
                                  measurements=self.measurements, upper_gi=self.upper, photogrammetry=self.photo)

    def test_reports_every_disposition_and_placement_including_display(self):
        report = self.build()
        self.assertEqual('author_ready', report['status'])
        self.assertEqual([], report['blockers'])
        self.assertEqual(3, report['placement_count'])
        self.assertEqual(['screen'], report['resolved_displays'])
        self.assertEqual(['screen.point'], [p['id'] for p in report['dispositions']['displays'][0]['placements']])
        self.assertEqual(['mesh'], report['dispositions']['displays'][0]['placements'][0]['source_refs'])
        self.assertEqual([{'group': 'lamp', 'address': 81}], report['not_applicable_outputs']['virtual'])
        self.assertEqual(1, report['gi']['quantity'])
        self.assertEqual('F24 F25 F26 F27', report['gi']['notes'])
        self.assertEqual(self.legacy['projections'], report['projections'][:len(self.legacy['projections'])])
        self.assertEqual({('pinmame.output.lamp', 16), ('pinmame.output.solenoid', 27), ('pinmame.output.gi', 0)},
                         {(p['group'], p['address']) for p in report['projections'][len(self.legacy['projections']):]})
        self.assertEqual(3, len(report['additional_tables_checked']))
        self.assertEqual(self.vpw['source']['world_manifest_sha256'], report['additional_tables_checked'][2]['world_manifest_sha256'])
        self.assertFalse(any('see blockers' in value for value in report['excluded_object_classes']))

    def test_unknown_omitted_unvalidated_and_missing_are_blockers(self):
        d = copy.deepcopy(self.definition)
        d['coverage']['status'] = 'partial'
        d['coverage']['missing'] = ['spatial_placement']
        d['outputs'][1]['availability'] = 'unknown'
        del d['displays'][0]['spatial']
        d['inputs'][0]['spatial']['status'] = 'candidate'
        d['conflicts'] = [{'id': 'conflict.fixture'}]
        report = self.build(d)
        self.assertEqual('partial', report['status'])
        self.assertEqual('pinmame-spatial-blockers', report['format'])
        self.assertEqual(['screen'], report['omitted_displays'])
        self.assertEqual(2, report['placement_count'])
        self.assertTrue(any('spatial_placement' in item for item in report['blockers']))
        self.assertTrue(any('virtual: availability unknown' in item for item in report['unresolved']))
        self.assertTrue(any('screen: spatial disposition omitted' in item for item in report['blockers']))
        self.assertTrue(any('switch: spatial status candidate' in item for item in report['blockers']))
        self.assertTrue(any('conflict.fixture' in item for item in report['blockers']))

    def test_renderer_is_deterministic_and_contains_auditable_evidence(self):
        report = self.build()
        self.assertEqual(report, self.build())
        rendered = audit.render_report(report)
        self.assertEqual(rendered, audit.render_report(report))
        for phrase in ('fixture', 'Placements: 3', 'screen.point', '0.5, 0.6', 'mesh',
                       self.vpw['source']['table_sha256'], 'shared ancestry', 'original incandescent'):
            self.assertIn(phrase, rendered)
        self.assertNotIn('every retained table models one', rendered)


if __name__ == '__main__':
    unittest.main()
