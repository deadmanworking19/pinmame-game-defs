import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class GhostbustersFactsTests(unittest.TestCase):
	def test_own_edition_devices_and_slimer_transport_limits(self):
		d = load_json(ROOT / 'machines/partial/stern/ghostbusters-limited-edition-2016.json')
		self.assertEqual('GR9Nr-MVKol', d['machine']['opdb_id'])
		self.assertEqual(6334, d['machine']['ipdb_id'])
		inputs = {i['binding']['device']: i for i in d['inputs'] if i['binding']['group'] == 'pinmame.input.switch'}
		for number in (11, 12):
			self.assertTrue(inputs[number]['normally_closed'])
			self.assertEqual('virtual', inputs[number]['kind'])
		mechanisms = {m['id']: m for m in d['mechanisms']}
		self.assertEqual(['switch.22-shooter-lane'], mechanisms['mechanism.shooter']['sensors'])
		self.assertEqual([], mechanisms['mechanism.slimer']['actuators'])
		self.assertEqual({inputs[n]['id'] for n in (68, 69, 71, 72)}, set(mechanisms['mechanism.slimer']['sensors']))
		self.assertEqual({inputs[n]['id'] for n in (60, 61, 62, 63)}, set(mechanisms['mechanism.subway']['sensors']))
		displays = {v['controller_index']: v for v in d['displays']}
		self.assertEqual((128, 32), (displays[0]['width'], displays[0]['height']))
		self.assertEqual((160, 128), (displays[1]['width'], displays[1]['height']))
		self.assertEqual('playfield', displays[1]['physical_location'])
		conflicts = {c['id']: c for c in d['conflicts']}
		self.assertEqual('ignored', conflicts['conflict.cpu-interlock-endpoints']['status'])
		for cid in ('conflict.cabinet-slam-sixth-coin', 'conflict.ramp43-physical-identity'):
			self.assertEqual('unresolved', conflicts[cid]['status'])
			self.assertIn('Resolution path:', conflicts[cid]['description'])




class SuppliedTableEvidenceTests(unittest.TestCase):
	def _artifacts(self):
		definition = load_json(ROOT / 'machines/partial/stern/ghostbusters-limited-edition-2016.json')
		report = load_json(ROOT / 'evidence/spatial/stern/ghostbusters-limited-edition-2016-supplied-vpx.json')
		excerpt = load_json(ROOT / report['evidence_excerpt']['path'])
		return definition, report, excerpt

	def test_exact_table_identity_observed_projection_and_partial_limits(self):
		import hashlib
		definition, report, excerpt = self._artifacts()
		self.assertEqual('gbust_117h', excerpt['bound_driver'])
		self.assertEqual('717cba9783713791b457a110e8a68dc2328934b9f4a9b0a151ccaa3f98dc5d52', excerpt['source_vpx']['sha256'])
		self.assertEqual('partial', definition['coverage']['status'])
		self.assertIn('spatial_placement', definition['coverage']['missing'])
		self.assertEqual(report['placements'], excerpt['placements'])
		self.assertEqual(48, sum(row['collection'] == 'inputs' for row in report['placements']))
		self.assertEqual(8, sum(row['collection'] == 'outputs' for row in report['placements']))
		self.assertEqual(report['evidence_excerpt']['sha256'], hashlib.sha256((ROOT / report['evidence_excerpt']['path']).read_bytes()).hexdigest())
		devices = {device['id']: device for device in definition['inputs'] + definition['outputs']}
		sources = {source['id']: source for source in definition['sources']}
		for row in report['placements']:
			device = devices[row['device_id']]
			self.assertEqual('observed', device['spatial']['status'])
			placement, = device['spatial']['placements']
			self.assertEqual((row['x'], row['y']), (placement['x'], placement['y']))
			self.assertEqual(set(row['source_refs']), set(placement['provenance']['source_refs']))
			self.assertTrue(set(row['source_refs']).issubset(sources))
			self.assertNotEqual('Light', row['object']['type'])
			self.assertTrue(row['script_locators'])
		self.assertTrue(report['excluded_or_unresolved'])
		self.assertFalse(sources['vpx.supplied-pinmame-script.2026-10-25']['known_working'])
		for source_id in ('vpx.supplied-pinmame-script.2026-10-25', 'vpx.supplied-pinmame-table.2026-10-25'):
			self.assertEqual(report['evidence_excerpt'], sources[source_id]['excerpts'][0])

	def test_retained_manifest_source_lines_and_repository_normalization(self):
		import hashlib
		import os
		import sys
		if not os.environ.get('PINMAME_VPX_SOURCES_ROOT'):
			self.skipTest('Retained VPX root is optional')
		from pinmame_game_defs.spatial import extract_spatial_candidates
		sys.path.insert(0, str(ROOT / 'tools'))
		from build_external_evidence_manifest import check_manifest
		definition, report, excerpt = self._artifacts()
		vpx_root = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']).resolve()
		retained = vpx_root / 'stern/ghostbusters-limited-edition-2016/supplied-pinmame-2026-10-25'
		working_root = vpx_root.parent
		def resolve(record):
			path = (working_root / record['path'].removeprefix('working-root:')).resolve()
			self.assertTrue(path.is_relative_to(retained), record['path'])
			self.assertEqual(record['size'], path.stat().st_size)
			self.assertEqual(record['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
			return path
		self.assertEqual(excerpt['extraction_manifest']['sha256'], check_manifest(retained, 'gbust_117h'))
		manifest = load_json(resolve(excerpt['extraction_manifest']))
		self.assertEqual(excerpt['extraction_manifest']['file_count'], len(manifest['files']))
		self.assertEqual(excerpt['extraction_manifest']['byte_count'], sum(row['size'] for row in manifest['files']))
		vpx = resolve(excerpt['source_vpx'])
		script_lines = resolve(excerpt['script']).read_text(encoding='utf8').splitlines()
		candidates = extract_spatial_candidates(retained / 'extracted', vpx, 'git:v0.33.3')
		self.assertEqual(excerpt['bounds'], candidates['bounds'])
		objects = {(row['type'].casefold(), row['name'].casefold()): row for row in candidates['objects']}
		for row in report['placements']:
			resolve(row['object']['artifact'])
			obj = objects[row['object']['type'].casefold(), row['object']['name'].casefold()]
			self.assertEqual((row['x'], row['y']), (obj['x'], obj['y']))
			for locator in row['script_locators']:
				self.assertEqual(locator['text'], script_lines[locator['line'] - 1].strip())
		for locator in excerpt['script_runtime_lines'] + excerpt['script_light_lines']:
			self.assertEqual(locator['text'], script_lines[locator['line'] - 1].strip())
if __name__ == '__main__':
	unittest.main()
