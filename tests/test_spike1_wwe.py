import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class WrestlemaniaLEFactsTests(unittest.TestCase):
	def test_shared_motor_lamp_names_upper_flipper_and_two_displays(self):
		d = load_json(ROOT / 'machines/partial/stern/wwe-wrestlemania-limited-edition-2015.json')
		self.assertEqual(('GR6Or-MKNYR', 6216), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		lamps = {v['binding']['device']: v for v in d['outputs'] if v['binding']['group'] == 'pinmame.output.lamp'}
		for n, names in [(5, {'MOTOR 2', '200 THOUSAND'}), (22, {'MOTOR 1', 'SPECIAL WHEN RED(RIGHT)'})]:
			self.assertEqual(names, {a['value'] for a in lamps[n]['aliases'] if a['namespace'] == 'rom.name'})
			self.assertEqual('candidate', lamps[n]['provenance']['status'])
			self.assertIn('no independent state is available', lamps[n]['physical']['notes'])
			self.assertIn('Binary value ORs', lamps[n]['physical']['notes'])
			self.assertIn('overwritten by later LED-table traversal', lamps[n]['physical']['notes'])
		conflicts = {c['id']: c for c in d['conflicts']}
		self.assertEqual('ignored', conflicts['wwe.led-aliases']['status'])
		self.assertIn('transport limitation', conflicts['wwe.led-aliases']['rationale'])
		self.assertNotIn('shared node/position', conflicts['wwe.led-aliases']['description'])
		for conflict_id in ('wwe.extension-lp-addresses', 'wwe.ring-assembly-caption'):
			self.assertEqual('unresolved', conflicts[conflict_id]['status'])
		for gap in ('output_semantics', 'mechanism_behavior'):
			self.assertIn(gap, d['coverage']['missing'])
		for n in range(83, 88):
			self.assertEqual('gi', lamps[n]['kind'])
		for n, quantity in [(83, 2), (86, 3), (87, 3)]:
			self.assertEqual(quantity, lamps[n]['physical']['quantity'])
		mechanisms = {m['id']: m for m in d['mechanisms']}
		self.assertEqual(['solenoid.022'], mechanisms['mechanism.upper-flipper']['actuators'])
		self.assertEqual({'switch.074', 'switch.075', 'switch.078'}, set(mechanisms['mechanism.upper-flipper']['sensors']))
		self.assertNotIn('solenoid.022', mechanisms['mechanism.ring-disc']['actuators'])
		upper_eos = next(i for i in d['inputs'] if i['id'] == 'switch.078')
		self.assertTrue(upper_eos['normally_closed'])
		self.assertEqual('180-5149-00', upper_eos['physical']['part_number'])
		displays = {v['controller_index']: v for v in d['displays']}
		self.assertEqual((128, 32), (displays[0]['width'], displays[0]['height']))
		self.assertEqual((320, 240), (displays[1]['width'], displays[1]['height']))
		self.assertTrue(any(c['id'] == 'wwe.extension-lp-addresses' and c['status'] == 'unresolved' for c in d['conflicts']))


if __name__ == '__main__':
	unittest.main()
