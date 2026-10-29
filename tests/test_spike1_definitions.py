from __future__ import annotations

import hashlib
import os
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import curate_spike1


def definitions():
	return [(path.stem, load_json(path)) for path in sorted((ROOT / 'tools/seeds/stern/spike1').glob('*.json'))]


def sha256(path):
	digest = hashlib.sha256()
	with path.open('rb') as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b''):
			digest.update(block)
	return digest.hexdigest()


def external_records(value):
	if isinstance(value, dict):
		if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
			yield value
		for child in value.values():
			yield from external_records(child)
	elif isinstance(value, list):
		for child in value:
			yield from external_records(child)


class Spike1DefinitionTests(unittest.TestCase):
	def test_complete_revision_specific_address_sets_and_partial_gate(self):
		for game, definition in definitions():
			with self.subTest(game=game):
				self.assertEqual('partial', definition['coverage']['status'])
				self.assertIn('spatial_placement', definition['coverage']['missing'])
				if game == 'gbust_117h':
					self.assertNotIn('mechanism_behavior', definition['coverage']['missing'])
					self.assertTrue(all(m['provenance']['status'] == 'validated' for m in definition['mechanisms']))
				else:
					self.assertIn('mechanism_behavior', definition['coverage']['missing'])
				self.assertEqual('pinmame.spike1', definition['controller']['platform'])
				self.assertEqual([], validate_machine(definition, ROOT))
				groups = {}
				for device in definition['inputs'] + definition['outputs']:
					groups.setdefault(device['binding']['group'], []).append(device['binding']['device'])
				for addresses in groups.values():
					self.assertEqual(len(addresses), len(set(addresses)))
				self.assertEqual(set(range(96)) | set(range(101, 133)), set(groups['pinmame.input.switch']))
				self.assertEqual(set(range(1, 9)), set(groups['pinmame.input.dip']))
				self.assertEqual(set(range(1, 34)) | set(range(45, 49)) | set(range(51, 73)), set(groups['pinmame.output.solenoid']))
				rom_path = ROOT / 'evidence/excerpts' / definition['machine']['id'] / 'rom-routing.json.txt'
				if any(source['kind'] == 'rom_static_analysis' for source in definition['sources']):
					self.assertTrue(rom_path.is_file())
					rom = load_json(rom_path)
					self.assertEqual(set(range(1, rom['controller']['padded_lamp_limit'] + 1)), set(groups['pinmame.output.lamp']))

	def test_every_exported_firmware_row_preserves_its_name_and_binding(self):
		for game, definition in definitions():
			with self.subTest(game=game):
				rom_sources = [source for source in definition['sources'] if source['kind'] == 'rom_static_analysis']
				if not rom_sources:
					continue
				rom = load_json(ROOT / 'evidence/excerpts' / definition['machine']['id'] / 'rom-routing.json.txt')
				devices = {(d['binding']['group'], d['binding']['device']): d for d in definition['inputs'] + definition['outputs']}
				for section, group in [('switches', 'pinmame.input.switch'), ('coils', 'pinmame.output.solenoid'), ('leds', 'pinmame.output.lamp')]:
					columns = rom[section]['columns']
					for values in rom[section]['rows']:
						row = dict(zip(columns, values))
						address = row['public_address']
						if address is None:
							continue
						device = devices[group, address]
						aliases = device['aliases']
						if 'name_origin' in row:
							self.assertIn(row['name_origin'], {'firmware_string', 'pinmame_source_synthesized'})
							namespace = 'pinmame.label' if row['name_origin'] == 'pinmame_source_synthesized' else 'rom.label'
							aliases = [alias for alias in aliases if alias['namespace'] == namespace]
						self.assertIn(row['name'], [alias['value'] for alias in aliases], (game, section, address, row['name']))

	def test_reproduction_catalog_ownership_and_all_excerpt_digests(self):
		catalog = load_json(ROOT / 'catalog/pinmame.json')
		for game, definition in definitions():
			with self.subTest(game=game):
				curate_spike1.check(game, ROOT)
				paths = [d['definition'] for d in catalog['drivers'] if d['id'] == game]
				self.assertEqual(1, len(paths))
				self.assertTrue(paths[0].startswith('machines/partial/stern/'))
				self.assertEqual(canonical_bytes(definition), (ROOT / paths[0]).read_bytes())
				for source in definition['sources']:
					for excerpt in source.get('excerpts', []):
						self.assertEqual(excerpt['sha256'], sha256(ROOT / excerpt['path']))

	@unittest.skipUnless(os.environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'Retained evidence root is optional')
	def test_exact_retained_facts_and_source_artifacts(self):
		working_root = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']).resolve().parent
		checked = {}
		for game, definition in definitions():
			with self.subTest(game=game):
				for source in definition['sources']:
					if source['uri'].startswith('working-root:'):
						path = (working_root / source['uri'].removeprefix('working-root:')).resolve()
						self.assertTrue(path.is_relative_to(working_root), source['uri'])
						self.assertTrue(path.is_file(), source['uri'])
						if path not in checked:
							checked[path] = sha256(path)
						self.assertEqual(source['sha256'], checked[path], source['uri'])
					for excerpt in source.get('excerpts', []):
						if not excerpt['path'].endswith('.json.txt'):
							continue
						for record in external_records(load_json(ROOT / excerpt['path'])):
							locator = record['path']
							if locator.startswith('working-root:'):
								locator = locator.removeprefix('working-root:')
							elif not locator.startswith(('review-artifacts/', 'manuals/', 'roms/', 'builds/', 'source-checkouts/')):
								continue
							path = (working_root / locator).resolve()
							self.assertTrue(path.is_relative_to(working_root), locator)
							self.assertTrue(path.is_file(), locator)
							if path not in checked:
								checked[path] = sha256(path)
							self.assertEqual(record['sha256'], checked[path], locator)

	def test_supreme_aliases_keep_all_colliding_firmware_rows_without_fitment_claims(self):
		definition = load_json(ROOT / 'machines/partial/stern/supreme-x-stern-2018.json')
		self.assertEqual('G3EnZ-MePOV', definition['machine']['opdb_id'])
		self.assertEqual(6609, definition['machine']['ipdb_id'])
		self.assertEqual('Supreme x Stern', definition['machine']['name'])
		lamps = {d['binding']['device']: d for d in definition['outputs'] if d['binding']['group'] == 'pinmame.output.lamp'}
		for number in (1, 2, 3):
			self.assertEqual('unknown', lamps[number]['availability'])
			self.assertEqual(2, len([a for a in lamps[number]['aliases'] if a['namespace'] == 'rom.label']))
		for device in definition['inputs'] + definition['outputs']:
			self.assertNotIn('normally_closed', device)
			self.assertNotIn('quantity', device.get('physical', {}))
			for placement in device.get('spatial', {}).get('placements', []):
				self.assertEqual('observed', placement['provenance']['status'])
				self.assertIn('supreme.vpx.table.008', placement['provenance']['source_refs'])
				self.assertIn('supreme.vpx.script.008', placement['provenance']['source_refs'])


if __name__ == '__main__':
	unittest.main()
