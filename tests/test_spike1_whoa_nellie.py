import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class WhoaNellieFactsTests(unittest.TestCase):
	def test_own_identity_reels_and_unresolved_cabinet_semantics(self):
		d = load_json(ROOT / 'machines/partial/stern/whoa-nellie-big-juicy-melons-2015.json')
		self.assertEqual(('GRYX4-MLqqx', 6252), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		reels = [m for m in d['mechanisms'] if m['kind'] == 'reel']
		self.assertEqual(5, len(reels))
		self.assertTrue(all(not m['actuators'] and len(m['sensors']) == 1 for m in reels))
		self.assertNotIn('physical_location', d['displays'][0])
		self.assertEqual('video', d['displays'][0]['kind'])
		inputs = {i['binding']['device']: i for i in d['inputs'] if i['binding']['group'] == 'pinmame.input.switch'}
		for n in (60, 61):
			self.assertEqual('unknown', inputs[n]['availability'])
			self.assertEqual('conflicted', inputs[n]['provenance']['status'])
			self.assertNotIn('wiring', inputs[n])
		outputs = {v['binding']['device']: v for v in d['outputs'] if v['binding']['group'] == 'pinmame.output.solenoid'}
		for n in (51, 52, 53):
			self.assertEqual('control_signal', outputs[n]['kind'])
		self.assertTrue(all(outputs[n]['kind'] == 'virtual' for n in range(17, 32)))
		self.assertTrue(any(c['id'] == 'conflict.slam-sixth-coin' and c['status'] == 'unresolved' for c in d['conflicts']))




class SuppliedTableEvidenceTests(unittest.TestCase):
	def _artifacts(self):
		definition = load_json(ROOT / 'machines/partial/stern/whoa-nellie-big-juicy-melons-2015.json')
		report = load_json(ROOT / 'evidence/spatial/stern/whoa-nellie-big-juicy-melons-2015-supplied-vpx.json')
		excerpt = load_json(ROOT / report['evidence_excerpt']['path'])
		return definition, report, excerpt

	def test_exact_table_identity_observed_projection_and_partial_limits(self):
		import hashlib
		definition, report, excerpt = self._artifacts()
		self.assertEqual('wnbjm_155', excerpt['bound_driver'])
		self.assertEqual('277fff2d00c349ef1c15b4ff4a97df05d38b7b0bc892949ea180305cd8ccc753', excerpt['source_vpx']['sha256'])
		self.assertEqual('partial', definition['coverage']['status'])
		self.assertIn('spatial_placement', definition['coverage']['missing'])
		self.assertEqual(report['placements'], excerpt['placements'])
		self.assertEqual(27, sum(row['collection'] == 'inputs' for row in report['placements']))
		self.assertEqual(7, sum(row['collection'] == 'outputs' for row in report['placements']))
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
		retained = vpx_root / 'stern/whoa-nellie-big-juicy-melons-2015/supplied-pinmame-2026-10-25'
		working_root = vpx_root.parent
		def resolve(record):
			path = (working_root / record['path'].removeprefix('working-root:')).resolve()
			self.assertTrue(path.is_relative_to(retained), record['path'])
			self.assertEqual(record['size'], path.stat().st_size)
			self.assertEqual(record['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
			return path
		self.assertEqual(excerpt['extraction_manifest']['sha256'], check_manifest(retained, 'wnbjm_155'))
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
