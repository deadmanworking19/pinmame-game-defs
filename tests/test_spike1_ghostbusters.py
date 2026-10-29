import copy
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / 'tools/seeds/stern/spike1/gbust_117h.json'
sys.path.insert(0, str(ROOT / 'tools'))


class GhostbustersFactsTests(unittest.TestCase):
	def test_own_edition_devices_and_slimer_transport_limits(self):
		d = load_json(SEED)
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
		self.assertTrue(conflicts)
		for conflict in conflicts.values():
			self.assertEqual('ignored', conflict['status'])
			self.assertTrue(conflict.get('rationale', '').strip())
		self.assertNotIn('conflict.ramp43-physical-identity', conflicts)
		self.assertEqual('Right Ramp', inputs[43]['label'])

	def test_distinct_library_and_subway_sensor_construction(self):
		d = load_json(SEED)
		inputs = {i['binding']['device']: i for i in d['inputs'] if i['binding']['group'] == 'pinmame.input.switch'}
		mechanisms = {m['id']: m for m in d['mechanisms']}
		library = mechanisms['mechanism.three-ball-lock']
		subway = mechanisms['mechanism.subway']
		self.assertEqual({inputs[n]['id'] for n in range(28, 34)}, set(library['sensors']))
		self.assertEqual({inputs[n]['id'] for n in range(60, 64)}, set(subway['sensors']))
		self.assertTrue(set(library['sensors']).isdisjoint(subway['sensors']))
		self.assertTrue(all(inputs[n]['physical']['switch_type'] != 'opto' for n in range(28, 34)))
		self.assertTrue(all(inputs[n]['physical']['switch_type'] == 'opto' for n in range(60, 63)))
		self.assertNotEqual('opto', inputs[63]['physical']['switch_type'])
		self.assertIn('manual.ghostbusters-le.completion.2026', library['provenance']['source_refs'])
		self.assertIn('vpx.supplied-pinmame-script.2026-10-25', library['provenance']['source_refs'])

	def test_ramp_release_note_does_not_remove_right_ramp(self):
		d = load_json(SEED)
		inputs = {i['binding']['device']: i for i in d['inputs'] if i['binding']['group'] == 'pinmame.input.switch'}
		self.assertEqual(('used', 'Left Ramp 1'), (inputs[40]['availability'], inputs[40]['label']))
		self.assertEqual(('used', 'Right Ramp'), (inputs[43]['availability'], inputs[43]['label']))
		self.assertEqual('validated', inputs[43]['provenance']['status'])
		self.assertTrue({'factory.ghostbusters-le.readme-117', 'manual.ghostbusters-le.completion.2026',
		                 'rom.ghostbusters-le.gbust-117h', 'vpx.supplied-pinmame-script.2026-10-25'}
		                <= set(inputs[43]['provenance']['source_refs']))
		excerpt = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-factory-readme.json.txt')
		fact = next(s for s in excerpt['facts'] if 'LEFT RAMP ENTER' in s)
		for label in ('LEFT RAMP 2', 'LEFT RAMP 3', 'RIGHT RAMP43', 'LEFT RAMP 1'):
			self.assertIn(label, fact)

	def test_slimer_transport_and_optional_cabinet_scope(self):
		d = load_json(SEED)
		mechanisms = {m['id']: m for m in d['mechanisms']}
		slimer = mechanisms['mechanism.slimer']
		self.assertEqual([], slimer['actuators'])
		self.assertIn('GetMech0', slimer['behavior'])
		self.assertIn('HandleMechanics', slimer['behavior'])
		self.assertTrue({'pinmame.adapter.current', 'runtime.ghostbusters-le.slimer-2026',
		                 'manual.ghostbusters-le.completion.2026', 'vpx.supplied-pinmame-script.2026-10-25'}
		                <= set(slimer['provenance']['source_refs']))
		devices = {item['id']: item for item in d['inputs'] + d['outputs']}
		ticket = mechanisms['mechanism.ticket']
		self.assertEqual(['switch.88-ticket-notch'], ticket['sensors'])
		self.assertEqual(['coil.32-ticket-dispenser'], ticket['actuators'])
		topper = [item for item in d['outputs'] if 'cabinet.topper' in item.get('roles', [])]
		self.assertTrue(topper)
		for item in topper + [devices[x] for x in ticket['sensors'] + ticket['actuators']]:
			self.assertEqual('optional', item['availability'])
			self.assertEqual(('not_applicable', 'cabinet_or_service'),
			                 (item['spatial']['status'], item['spatial']['reason']))




class SuppliedTableEvidenceTests(unittest.TestCase):
	def _artifacts(self):
		definition = load_json(SEED)
		report = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/supplied-spatial-audit.json.txt')
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
			placement = next(p for p in device['spatial']['placements'] if (p['x'], p['y']) == (row['x'], row['y']))
			self.assertEqual((row['x'], row['y']), (placement['x'], placement['y']))
			self.assertEqual(set(row['source_refs']), set(placement['provenance']['source_refs']))
			self.assertTrue(set(row['source_refs']).issubset(sources))
			self.assertNotEqual('Light', row['object']['type'])
			self.assertTrue(row['script_locators'])
		self.assertTrue(report['excluded_or_unresolved'])
		self.assertFalse(sources['vpx.supplied-pinmame-script.2026-10-25']['known_working'])
		for source_id in ('vpx.supplied-pinmame-script.2026-10-25', 'vpx.supplied-pinmame-table.2026-10-25'):
			self.assertIn(report['evidence_excerpt'], sources[source_id]['excerpts'])
			self.assertFalse(sources[source_id]['known_working'])
			self.assertIn('user-identified PinMAME table', sources[source_id]['locator'])
			self.assertIn('No complete VPX launch/playtest has been established', sources[source_id]['locator'])

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


class SpatialReportTests(unittest.TestCase):
	def report(self, definition):
		import curate_spike1
		import curate_ghostbusters_le_2016
		return curate_ghostbusters_le_2016.enrich_spatial_report(
			ROOT, definition, curate_spike1.spatial_report(definition))

	def test_deterministic_inventory_preserves_placement_provenance_and_sources(self):
		import curate_ghostbusters_le_2016
		d = load_json(SEED)
		report = self.report(d)
		self.assertEqual(report, self.report(copy.deepcopy(d)))
		declared = {(r['collection'], r['id'], r['placement']['id']): r for r in report['declared_placements']}
		for collection in ('inputs', 'outputs', 'displays'):
			for device in d[collection]:
				for placement in device.get('spatial', {}).get('placements', []):
					row = declared.pop((collection, device['id'], placement['id']))
					self.assertEqual(placement, row['placement'])
					self.assertEqual(device['spatial']['status'], row['spatial_status'])
		self.assertFalse(declared)
		self.assertTrue(report['projection_classes'])
		self.assertIn('trough_ball_slot', report['projection_classes'])
		self.assertTrue(any(r['spatial_status'] == 'observed' for r in report['declared_placements']))
		self.assertEqual({(s['id'], e['id']) for s in d['sources'] for e in s.get('excerpts', [])
		                  if e['id'].startswith('completion-')},
		                 {(r['source_id'], r['excerpt']['id']) for r in report['completion_source_excerpts']})
		self.assertEqual({s['id'] for s in d['sources']}, {s['id'] for s in report['source_identities']})
		self.assertTrue(report['unresolved_physical_polarity_inputs'])
		self.assertEqual({2, 3, *range(150, 166)},
		                 {r['binding']['device'] for r in report['unresolved_emitter_quantities']})
		self.assertEqual({r['id'] for r in report['unvalidated_spatial_records']},
		                 {r['id'] for r in report['declared_placements'] if r['spatial_status'] != 'validated'})
		self.assertFalse(report['mechanism_candidates'])
		self.assertTrue(any(r['reason'] == 'cabinet_or_service' for r in report['not_applicable_spatial']))
		self.assertTrue(report['absent_spatial'])
		text = curate_ghostbusters_le_2016.report_markdown(report)
		self.assertNotIn('None declared by the schema-valid seed; no class or coordinate was inferred.', text)
		for row in report['completion_source_excerpts']:
			self.assertIn(row['excerpt']['id'], text)

	def test_report_changes_when_seed_loses_placement_quantity_or_source(self):
		d = load_json(SEED)
		device = next(x for x in d['inputs'] if x.get('spatial', {}).get('placements'))
		device['physical']['quantity'] = 2
		baseline = self.report(d)
		without_placement = copy.deepcopy(d)
		next(x for x in without_placement['inputs'] if x['id'] == device['id'])['spatial']['placements'].pop()
		self.assertNotEqual(baseline, self.report(without_placement))
		without_quantity = copy.deepcopy(d)
		del next(x for x in without_quantity['inputs'] if x['id'] == device['id'])['physical']['quantity']
		self.assertNotEqual(baseline, self.report(without_quantity))
		without_source = copy.deepcopy(d)
		without_source['sources'] = [s for s in without_source['sources'] if s['id'] != 'manual.ghostbusters-le.completion.2026']
		self.assertNotEqual(baseline, self.report(without_source))


class CompletionEvidenceTests(unittest.TestCase):
	# Drawing crops use the schema's image/image_sha256 pair beside the
	# factual JSON transcription in path/sha256. Both pairs must fail closed.
	DRAWING_CROPS = {
		'completion-library-contacts': ('manual.ghostbusters-le.completion.2026', 46, 650, 436),
		'completion-light-locations': ('manual.ghostbusters-le.completion.2026', 18, 556, 1240),
		'completion-mechanical-circuit': ('circuit.ghostbusters-le.ordinary-mechanical', 37, 1763, 528),
		'completion-slimer-boom': ('manual.ghostbusters-le.completion.2026', 48, 853, 799),
		'completion-slimer-drive': ('manual.ghostbusters-le.completion.2026', 49, 1083, 1356),
		'completion-subway-lock': ('manual.ghostbusters-le.completion.2026', 39, 723, 594),
		'completion-switch-locations': ('manual.ghostbusters-le.completion.2026', 15, 542, 1238),
		'completion-trough-circuit': ('circuit.ghostbusters-le.trough-receiver', 1, 1700, 1141),
	}

	def test_drawing_crops_pin_original_sources_and_reviewed_render_metadata(self):
		import hashlib
		d = load_json(SEED)
		sources = {s['id']: s for s in d['sources']}
		for name, (source_id, page, width, height) in self.DRAWING_CROPS.items():
			with self.subTest(crop=name):
				path = f'evidence/excerpts/stern.ghostbusters-limited-edition.2016/{name}.webp'
				matches = [(s, e) for s in d['sources'] for e in s.get('excerpts', []) if e.get('image') == path]
				self.assertEqual(1, len(matches))
				source, excerpt = matches[0]
				self.assertEqual(source_id, source['id'])
				self.assertEqual('manual', source['kind'])
				self.assertTrue(source['license'] and source['attribution'])
				self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), excerpt['image_sha256'])
				self.assertTrue(excerpt['reviewed'])
				self.assertIn(excerpt['method'], {'manual', 'mixed'})
				self.assertTrue(excerpt['transcribed_by'] and excerpt['locator'])
				self.assertIn(f'page {page}, crop box ', excerpt['image_derivation'])
				self.assertIn(f'{width}x{height} WebP', excerpt['image_derivation'])
				self.assertEqual(path.removesuffix('.webp') + '.json.txt', excerpt['path'])
		# These are distinct original factory documents, not copied drawings
		# attributed to the title's playfield manual by filename alone.
		self.assertEqual('1616a7a597ff5fbfdd4bfa4d53f7c633a37180ddeae8f125ac09c4c67ae7097d',
		                 sources['manual.ghostbusters-le.completion.2026']['sha256'])
		self.assertEqual('84e82041089a06f681d286d7ffcb795980a9351e666726795804accdbb7c3ec6',
		                 sources['circuit.ghostbusters-le.ordinary-mechanical']['sha256'])
		self.assertEqual('fda8c941757e8bdaf595a568f40f2f257ae8c9003aff99a542aa64117d66e152',
		                 sources['circuit.ghostbusters-le.trough-receiver']['sha256'])

	def test_each_drawing_crop_missing_or_drifted_fails_machine_validation(self):
		from pinmame_game_defs.validation import validate_machine
		d = load_json(SEED)
		self.assertEqual([], validate_machine(d, ROOT))
		for name, (source_id, _, _, _) in self.DRAWING_CROPS.items():
			for defect in ('missing', 'digest'):
				with self.subTest(crop=name, defect=defect):
					changed = copy.deepcopy(d)
					source = next(s for s in changed['sources'] if s['id'] == source_id)
					excerpt = next(e for e in source['excerpts'] if e['id'] == name)
					if defect == 'missing':
						excerpt['image'] += '.missing'
						expected = f"missing excerpt file {excerpt['image']}"
					else:
						excerpt['image_sha256'] = '0' * 64
						expected = f"{excerpt['image']} does not match its recorded digest"
					self.assertTrue(any(expected in error for error in validate_machine(changed, ROOT)))

	def test_assertion_review_keeps_semantics_separate_from_spatial_and_unknown_fields(self):
		d = load_json(SEED)
		outputs = {x['id']: x for x in d['outputs']}
		review = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-assertion-review.json.txt')
		self.assertEqual(set(outputs), {r['id'] for r in review['outputs']})
		self.assertEqual({x['id'] for x in d['inputs']}, {r['id'] for r in review['inputs']})
		self.assertEqual({x['id'] for x in d['mechanisms']}, {r['id'] for r in review['mechanisms']})
		for row in review['outputs']:
			self.assertEqual(row['status'], outputs[row['id']]['provenance']['status'])
			self.assertEqual(bool(row['unresolved_fields']), row['status'] != 'validated')
		self.assertEqual({2, 3, *range(150, 166)},
		                 {x['binding']['device'] for x in d['outputs'] if x['provenance']['status'] != 'validated'})
		self.assertTrue(all(x['provenance']['status'] == 'validated' for x in d['mechanisms']))
		self.assertTrue(all('Quantity must be verified' not in x['behavior'] for x in d['mechanisms']))
		for identifier in ('coil.18-electric-gate', 'lamp.136-ghost'):
			self.assertEqual('validated', outputs[identifier]['provenance']['status'])
			self.assertNotEqual('validated', outputs[identifier].get('spatial', {}).get('status'))
		self.assertEqual({'output_semantics', 'polarity', 'spatial_placement'}, set(d['coverage']['missing']))

	def test_coin_door_count_uses_exact_assembly_and_own_circuit(self):
		d = load_json(SEED)
		lamp = next(x for x in d['outputs'] if x['id'] == 'lamp.116-coin-door-gi')
		self.assertEqual(2, lamp['physical']['quantity'])
		self.assertIn('hardware.ghostbusters-le.coin-door-count', lamp['provenance']['source_refs'])
		excerpt = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-coin-door-count.json.txt')
		self.assertEqual('501-5018-173', excerpt['own_fitment']['part_number'])
		regions = {r['pdf_page']: r for r in excerpt['shared_factory_regions']}
		row = next(r for r in regions[14]['raw_rows'] if r[0] == '83')
		self.assertEqual(('Coin Door GI(x2)', '1', 'CN5', '2', '1', '1-LP-1', '112-5033-08'),
		                 (row[1], row[2], row[4], row[5], row[7], row[12], row[13]))
		self.assertEqual('501-5018-173', next(r for r in regions[37]['rows'] if r[0] == '18')[1])
		self.assertEqual('cabinet_or_service', lamp['spatial']['reason'])

	@unittest.skipUnless(__import__('os').environ.get('PINMAME_VPX_SOURCES_ROOT'), 'Retained VPX root is optional')
	def test_fixed_mechanism_projections_rederive_their_actual_bound_objects(self):
		import os
		from pinmame_game_defs.spatial import extract_spatial_candidates
		d = load_json(SEED)
		retained = Path(os.environ['PINMAME_VPX_SOURCES_ROOT']) / 'stern/ghostbusters-limited-edition-2016/supplied-pinmame-2026-10-25'
		vpx = retained / 'Ghostbusters LE (Stern 2016) v0.041 PinMAME.vpx'
		candidates = extract_spatial_candidates(retained / 'extracted', vpx, 'git:v0.33.3')
		objects = {(o['type'] + '.' + o['name']): o for o in candidates['objects']}
		proof = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-mechanical-projections.json.txt')
		devices = {x['id']: x for x in d['inputs'] + d['outputs']}
		lines = (retained / 'extracted/script.vbs').read_text('utf8').splitlines()
		for identifier, name in [('switch.21-trough-jam', 'Kicker.sw20'),
		                         ('coil.5-left-sling-magnet', 'Trigger.LeftMagnaSling'),
		                         ('coil.6-right-sling-magnet', 'Trigger.RightMagnaSling')]:
			row = next(r for r in proof['placements'] if r['device_id'] == identifier)
			self.assertEqual(name, row['object'])
			self.assertEqual((objects[name]['x'], objects[name]['y']), (row['x'], row['y']))
			self.assertEqual('observed', devices[identifier]['spatial']['status'])
			placement = devices[identifier]['spatial']['placements'][0]
			self.assertEqual((row['x'], row['y']), (placement['x'], placement['y']))
			for locator in row['script_locators']:
				self.assertEqual(locator['text'], lines[locator['line'] - 1].strip())
		self.assertTrue(proof['investigated_but_not_physical_centres'])
		for identifier in ('switch.68-slimer-hit', 'switch.69-slimer-encoder-wheel-3', 'display.ecto-goggles'):
			device = next(x for x in d['inputs'] + d['displays'] if x['id'] == identifier)
			self.assertNotIn('spatial', device, 'Unproved optical image planes or moving mesh origins must not become physical centres')

	def test_circuit_specific_polarity_and_finite_actuator_inventory(self):
		d = load_json(SEED)
		inputs = {x['binding']['device']: x for x in d['inputs'] if x['binding']['group'] == 'pinmame.input.switch'}
		for n in range(15, 22):
			self.assertIs(False, inputs[n]['normally_closed'])
			self.assertIn('circuit.ghostbusters-le.trough-receiver', inputs[n]['provenance']['source_refs'])
		for n in (68, 11, 12):
			self.assertIs(True, inputs[n]['normally_closed'])
		for n in (36, 59, 60, 61, 62):
			self.assertNotIn('normally_closed', inputs[n], 'A generic opto description cannot settle the conditioned6940 receiver')
		for n in (1, 7, 9, 28, 34, 43, 49, 63, 109):
			self.assertIs(False, inputs[n]['normally_closed'])
			self.assertIn('circuit.ghostbusters-le.ordinary-mechanical', inputs[n]['provenance']['source_refs'])
		for n in (65, 66):
			self.assertIs(False, inputs[n]['normally_closed'])
			self.assertIn('circuit.ghostbusters-le.single-drop', inputs[n]['provenance']['source_refs'])
		for n in (69, 71, 72):
			self.assertNotIn('normally_closed', inputs[n], f'{n}: do not infer missing construction from a flag or startup state')
		self.assertIs(False, inputs[88]['normally_closed'])
		self.assertIs(False, inputs[86]['normally_closed'])
		self.assertEqual('516-0007-00', inputs[86]['physical']['part_number'])
		self.assertIn('hardware.ghostbusters-le.cabinet-tilt', inputs[86]['provenance']['source_refs'])
		self.assertIn('factory paper kit', inputs[88]['physical']['part_number'])
		self.assertIn('circuit.ghostbusters-le.factory-ticket', inputs[88]['provenance']['source_refs'])
		self.assertEqual('constant', inputs[116]['kind'])
		self.assertTrue(inputs[116]['constant_active'])
		self.assertNotIn('normally_closed', inputs[116])
		self.assertEqual('constant', inputs[116]['spatial']['reason'])
		physical = {x['id'] for x in d['outputs'] if x['binding']['group'] == 'pinmame.output.solenoid'
		            and x['availability'] in {'used', 'optional'} and x['kind'] != 'virtual'}
		actuators = {a for m in d['mechanisms'] for a in m['actuators']}
		self.assertTrue(physical <= actuators, physical - actuators)
		self.assertNotIn('mechanism_inventory', d['coverage']['missing'])
		self.assertNotIn('mechanism_behavior', d['coverage']['missing'])

	def test_title_power_board_and_cabinet_identity_corrections(self):
		d = load_json(SEED)
		inputs = {x['binding']['device']: x for x in d['inputs'] if x['binding']['group'] == 'pinmame.input.switch'}
		for n, identifier in ((43, 'switch.43-right-ramp'), (80, 'switch.80-sixth-coin-dba'), (89, 'switch.89-slam-tilt')):
			self.assertEqual(identifier, inputs[n]['id'])
			self.assertTrue(any(a['namespace'] == 'legacy.device-id' for a in inputs[n]['aliases']))
		self.assertEqual('CN9-5', inputs[80]['wiring']['control_connection'])
		self.assertEqual('CN5-4', inputs[89]['wiring']['control_connection'])
		self.assertNotIn('normally_closed', inputs[80])
		power = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-power-good.json.txt')
		self.assertEqual('520-5343-01', power['own_34_internal_bom']['rows'][1][1])
		self.assertEqual('520-5343-01', power['own_30']['part_number'])
		self.assertEqual('CN7-4 / nVBBGOOD', inputs[116]['wiring']['control_connection'])
		self.assertNotIn('part_number', inputs[116]['physical'])
		self.assertIn('circuit.ghostbusters-le.power-good', inputs[116]['provenance']['source_refs'])

	@unittest.skipUnless(__import__('os').environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'Retained evidence root is optional')
	def test_completion_sources_and_original_photos_match_retained_bytes(self):
		import hashlib
		import os
		from build_external_evidence_manifest import check_manifest
		working = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']).resolve().parent
		seen = set()
		def verify(value):
			if isinstance(value, dict):
				path = value.get('path', value.get('retained_path', ''))
				if isinstance(path, str) and path.startswith('working-root:') and value.get('sha256'):
					artifact = (working / path.removeprefix('working-root:')).resolve()
					self.assertTrue(artifact.is_relative_to(working), path)
					if 'size' in value:
						self.assertEqual(value['size'], artifact.stat().st_size, path)
					if path not in seen:
						with artifact.open('rb') as stream:
							self.assertEqual(value['sha256'], hashlib.file_digest(stream, 'sha256').hexdigest(), path)
						seen.add(path)
				for child in value.values():
					verify(child)
			elif isinstance(value, list):
				for child in value:
					verify(child)
		for path in (ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016').glob('completion-*.json.txt'):
			verify(load_json(path))
		self.assertGreater(len(seen), 45)
		boards = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-emitter-boards.json.txt')
		self.assertEqual(6, len(boards['photos']))
		for row in boards['photos']:
			self.assertIn(row['retained_path'], seen)
			capture = load_json(working / row['product_capture']['path'].removeprefix('working-root:'))
			self.assertIn(row['product_url'], __import__('json').dumps(capture))
		session = working / 'review-artifacts/ghostbusters-limited-edition-2016/completion-2026-10-29'
		check_manifest(session / 'switch-contact-levels', 'gbust_117h')
		run = load_json(session / 'switch-contact-levels/run.json')
		self.assertIsNone(run['failure'])
		self.assertEqual({'public-' + str(n) + '-one' for n in (65, 66, 76, 80, 81, 82, 83, 84, 85, 86, 88, 89)},
		                 {s['label'] for s in run['snapshots'] if s['label'].endswith('-one')})
		check_manifest(session / 'mechanical-response', 'gbust_117h')
		run = load_json(session / 'mechanical-response/run.json')
		self.assertIsNone(run['failure'])
		proof = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-mechanical-response.json.txt')
		self.assertEqual(10, len(proof['responses']))
		for row in proof['responses']:
			step = next(s for s in run['steps'] if s['step'] == row['step'])
			self.assertEqual(row['input'], step['switch'])
			self.assertEqual(row['label'], step['label'])
			transition = next(t for t in step['transitions']['solenoids'] if t['number'] == row['output'])
			self.assertEqual(row['states'], transition['states'])
			self.assertTrue({0, 1} <= set(transition['states']))

	def test_physical_quantities_and_independent_bulb_reconciliation(self):
		from drawing_callouts import evaluate, apply, fit
		d = load_json(SEED)
		lamps = {x['binding']['device']: x for x in d['outputs'] if x['binding']['group'] == 'pinmame.output.lamp'}
		for n, q in {117: 3, 118: 9, 119: 8, 120: 5, 121: 3, 122: 2, 123: 4, 136: 2, 140: 2, 141: 2}.items():
			self.assertEqual(q, lamps[n]['physical']['quantity'])
			if n not in (122, 136):
				self.assertEqual(q, len(lamps[n]['spatial']['placements']))
		self.assertEqual('observed', lamps[118]['spatial']['status'])
		self.assertEqual(2, sum(p['provenance']['status'] == 'observed' for p in lamps[118]['spatial']['placements']))
		for n in (117, 119, 120, 121, 123):
			self.assertEqual('validated', lamps[n]['spatial']['status'])
		for n in (125, 126):
			self.assertEqual('Rear playfield panel', lamps[n]['physical']['location'])
			self.assertEqual('observed', lamps[n]['spatial']['status'])
			self.assertEqual(1, len(lamps[n]['spatial']['placements']))
			self.assertIn('physical-lens-body', lamps[n]['spatial']['placements'][0]['id'])
		for group in (range(26, 29), range(41, 44), range(45, 48), range(50, 53), range(62, 65),
		              range(80, 83), range(86, 89), range(96, 99), range(107, 110)):
			signatures = set()
			for n in group:
				self.assertEqual(1, lamps[n]['physical']['shared_physical_quantity'])
				self.assertEqual(list(group), lamps[n]['physical']['co_located_addresses'])
				signatures.add(tuple((p['x'], p['y']) for p in lamps[n]['spatial']['placements']))
			self.assertEqual(1, len(signatures))
		bulbs = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-physical-bulbs.json.txt')
		points = {r['placement_id']: (r['x'], r['y']) for r in bulbs['field_bulbs']}
		decisions = evaluate(bulbs['callout_seed'], points)
		self.assertEqual(bulbs['callout_decisions'], decisions)
		self.assertEqual(25, len(points))
		self.assertTrue(all(r['agrees'] for r in decisions['placements'].values()))
		# The independent geometry must matter: moving a bulb outside the source
		# callout neighborhood fails even when every identity and count is intact.
		mutated = dict(points)
		identifier = next(iter(mutated))
		mutated[identifier] = (0.99, 0.99)
		self.assertFalse(evaluate(bulbs['callout_seed'], mutated)['placements'][identifier]['agrees'])
		measure = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-light-measurements.json.txt')
		transform = fit([(tuple(c['pixel']), tuple(c['xy'])) for c in measure['controls']])
		for row in measure['placements']:
			x, y = apply(transform, row['pixel'])
			self.assertEqual((round(x, 3), round(y, 3)), (row['placement']['x'], row['placement']['y']))

	@unittest.skipUnless(__import__('os').environ.get('PINMAME_REVIEW_ARTIFACTS_ROOT'), 'Retained evidence root is optional')
	def test_new_retained_runtime_and_geometry_are_recomputed(self):
		import hashlib
		import os
		from build_external_evidence_manifest import check_manifest
		from curate_twilight_zone import world_mesh_pieces
		working = Path(os.environ['PINMAME_REVIEW_ARTIFACTS_ROOT']).resolve().parent
		session = working / 'review-artifacts/ghostbusters-limited-edition-2016/completion-2026-10-29'
		for name in ('slimer-motion', 'slimer-targets'):
			check_manifest(session / name, 'gbust_117h')
			run = load_json(session / name / 'run.json')
			scenario = load_json(session / f'{name}.json')
			self.assertIsNone(run['failure'])
			self.assertEqual(1, run['handle_mechanics'])
			self.assertEqual('gbust_117h', run['game'])
			self.assertEqual(run['scenario']['sha256'], hashlib.sha256((session / f'{name}.json').read_bytes()).hexdigest())
			self.assertFalse([a for a in scenario['initial_switches'] + scenario['actions'] if a.get('switch') in (68, 69, 71, 72)])
			checkpoint = next(s for s in run['steps'] if s['label'] == 'verified-slimer-test-entry')
			self.assertEqual('SLIMER MOTOR TEST', checkpoint['matched_text'])
			self.assertGreater(len({s['driver_get_mech_0'] for s in run['snapshots']}), 1)
		bulbs = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-physical-bulbs.json.txt')
		obj = working / bulbs['obj']['path'].removeprefix('working-root:')
		with obj.open('rb') as stream:
			self.assertEqual(bulbs['obj']['sha256'], hashlib.file_digest(stream, 'sha256').hexdigest())
		pieces = world_mesh_pieces(obj, 'BM_Bulbs')
		for row in bulbs['field_bulbs'] + bulbs['rear_bulbs']:
			vertices, bounds = pieces[row['piece_index']]
			self.assertEqual(row['piece']['vertices'], vertices)
			self.assertEqual(row['piece']['bounds'], list(bounds))
			self.assertEqual((row['x'], row['y']), (round((bounds[0]+bounds[2])/2/952, 6), round((bounds[1]+bounds[3])/2/2115, 6)))
		flashers = load_json(ROOT / 'evidence/excerpts/stern.ghostbusters-limited-edition.2016/completion-rear-flashers.json.txt')
		parts = world_mesh_pieces(obj, 'BM_Parts')
		self.assertEqual(907, len(parts))
		for row in flashers['fixtures']:
			vertices, bounds = parts[row['piece_index']]
			self.assertEqual(row['vertices'], vertices)
			b = row['bounds']
			self.assertEqual((b[0][0], b[1][0], b[0][1], b[1][1]), bounds)
			self.assertEqual((row['x'], row['y']), (round((bounds[0]+bounds[2])/2/952, 6), round((bounds[1]+bounds[3])/2/2115, 6)))

if __name__ == '__main__':
	unittest.main()
