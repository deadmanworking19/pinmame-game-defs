from __future__ import annotations

import hashlib
import os
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]
REVISION = '46e1a01a0f73dc5ce163d98db1ae435883ecc450'
DRIVERS = {
	'avscp_103', 'gbust_117h', 'got_137', 'got_137h', 'heavym20_102',
	'kiss15_141h', 'pabst_101', 'primus_103', 'smancp_101',
	'supreme_101', 'tfcp_1018', 'wnbjm_155', 'wwe_135h',
}


class Spike1SourceRefreshTests(unittest.TestCase):
	def test_current_api_rows_have_unique_curated_owners(self):
		catalog = load_json(ROOT / 'catalog/pinmame.json')
		excerpt = load_json(ROOT / 'evidence/excerpts/pinmame.spike1/current-catalog.json.txt')
		self.assertEqual(REVISION, catalog['source']['pinmame_revision'])
		self.assertEqual(REVISION, excerpt['revision'])
		self.assertEqual(DRIVERS, {row['id'] for row in excerpt['drivers']})
		for row in excerpt['drivers']:
			with self.subTest(driver=row['id']):
				owners = [driver for driver in catalog['drivers'] if driver['id'] == row['id']]
				self.assertEqual(1, len(owners))
				self.assertTrue(owners[0]['definition'].startswith('machines/partial/stern/'))
				for field in ('description', 'manufacturer', 'year', 'flags'):
					self.assertEqual(row[field], owners[0][field])
				definition = load_json(ROOT / owners[0]['definition'])
				game_on = [device for device in definition['outputs'] if device['binding'] == {'group': 'pinmame.output.solenoid', 'device': 33}]
				self.assertEqual(1, len(game_on))
				self.assertEqual('virtual', game_on[0]['kind'])
				self.assertEqual('not_applicable', game_on[0]['spatial']['status'])

	@unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'Retained pinned source is optional')
	def test_every_retained_code_region_matches_its_numbered_source(self):
		working = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']).resolve().parent
		source = working / 'source-checkouts/pinmame-46e1a01a'
		excerpt = load_json(ROOT / 'evidence/excerpts/pinmame.spike1/current-adapter.json.txt')
		self.assertEqual(REVISION, excerpt['revision'])
		for record in excerpt['source_files']:
			with self.subTest(file=record['path']):
				data = (source / record['path']).read_bytes()
				self.assertEqual(record['byte_size'], len(data))
				self.assertEqual(record['sha256'], hashlib.sha256(data).hexdigest())
		for region in excerpt['code_excerpts']:
			with self.subTest(region=region['id']):
				lines = (source / region['path']).read_text(encoding='utf-8').splitlines()
				self.assertEqual(region['code'], '\n'.join(lines[region['line_start'] - 1:region['line_end']]) + '\n')


if __name__ == '__main__':
	unittest.main()
