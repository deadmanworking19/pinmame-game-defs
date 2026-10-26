from __future__ import annotations

import copy
import hashlib
import os
from pathlib import Path
import unittest

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / 'machines/partial/stern/supreme-x-stern-2018.json'
EXTERNAL_FILES = {
    'supreme.factory-model-photo': ('ipdb-image-14.png', 'd8035e505e0cb938c2866146d4f70bc1f8c969f378367c39e6b34c81ab847133'),
    'supreme.backbox-photo': ('ipdb-image-5.png', '05eaeba2bfbf312f999397168f2801d9e79e6c4b98ad32dd4c4ad3a5297ac662'),
    'supreme.factory-rule-card': ('pinside-2021-2639645.jpeg', 'fd6f0408c7c6baf8ece115b19ce2cc021fbc5b5e4dbf6c386ffc5a491a57ba4c'),
    'supreme.programmer-tutorial-lead': ('programmer-segments.json', 'cc22d8ff5ff2b720fb375edb6345911a33569b0f1cc75256c12cc305c3144798'),
}


class SupremeWebEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.definition = load_json(MACHINE)
        self.sources = {s['id']: s for s in self.definition['sources']}

    def test_primary_backbox_evidence_resolves_display_without_promoting_machine(self):
        self.assertEqual('PINBALL I-00PL * SUPREME 1', self.definition['machine']['model_number'])
        display, = self.definition['displays']
        self.assertEqual((0, 128, 32), (display['controller_index'], display['width'], display['height']))
        self.assertEqual('cabinet_or_service', display['physical_location'])
        self.assertEqual('validated', display['provenance']['status'])
        self.assertIn('supreme.backbox-photo', display['provenance']['source_refs'])
        self.assertIn('pinmame.adapter.current', display['provenance']['source_refs'])
        self.assertEqual('not_applicable', display['spatial']['status'])
        self.assertEqual('cabinet_or_service', display['spatial']['reason'])
        self.assertNotIn('display_inventory', self.definition['coverage']['missing'])
        self.assertEqual('partial', self.definition['coverage']['status'])
        self.assertTrue({'polarity', 'output_semantics', 'mechanism_behavior', 'spatial_placement'} <= set(self.definition['coverage']['missing']))
        self.assertEqual([], validate_machine(self.definition, ROOT))

    def test_complete_rule_card_facts_and_unverified_transcript_are_distinguished(self):
        for ident, (_, digest) in EXTERNAL_FILES.items():
            source = self.sources[ident]
            self.assertEqual(digest, source['sha256'])
            self.assertTrue(source['license'])
            self.assertTrue(source['attribution'])
            excerpt, = source['excerpts']
            self.assertEqual(ident != 'supreme.programmer-tutorial-lead', excerpt['reviewed'])
            self.assertEqual(excerpt['sha256'], hashlib.sha256((ROOT / excerpt['path']).read_bytes()).hexdigest())
        mechanisms = {m['id']: m for m in self.definition['mechanisms']}
        self.assertIn('supreme.factory-rule-card', mechanisms['mech.captive']['provenance']['source_refs'])
        self.assertIn('Galaxy multiball', mechanisms['mech.captive']['behavior'])
        self.assertIn('Meteor Shower', mechanisms['mech.spinner']['behavior'])
        self.assertNotEqual('validated', mechanisms['mech.gate']['provenance']['status'])

    def test_photo_excerpt_digest_and_promotion_guards_fail_closed(self):
        damaged = copy.deepcopy(self.definition)
        source = next(s for s in damaged['sources'] if s['id'] == 'supreme.backbox-photo')
        source['excerpts'][0]['sha256'] = '0' * 64
        self.assertTrue(any('SHA-256' in error or 'sha256' in error for error in validate_machine(damaged, ROOT)))
        promoted = copy.deepcopy(self.definition)
        promoted['coverage']['status'] = 'author_ready'
        promoted['coverage']['missing'] = []
        promoted['coverage']['dimensions'] = {key: 'validated' for key in promoted['coverage']['dimensions']}
        errors = validate_machine(promoted, ROOT)
        self.assertTrue(any('physical contact polarity' in error for error in errors))
        self.assertTrue(any('availability' in error for error in errors))

    @unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'Retained web evidence root is optional')
    def test_retained_original_web_artifacts_match_pinned_bytes(self):
        folder = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']) / 'stern.supreme-x-stern.2018/session-20261026'
        for ident, (filename, digest) in EXTERNAL_FILES.items():
            with self.subTest(source=ident):
                self.assertEqual(digest, hashlib.sha256((folder / filename).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
