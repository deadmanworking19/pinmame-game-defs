import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class HeavyMetalFactsTests(unittest.TestCase):
	def test_shared_devices_digital_signals_and_literal_factory_conflicts(self):
		definition = load_json(ROOT / 'machines/partial/stern/heavy-metal-2020.json')
		self.assertEqual('GoEej-Mo1q0', definition['machine']['opdb_id'])
		self.assertEqual(6733, definition['machine']['ipdb_id'])
		outputs = {(d['binding']['group'], d['binding']['device']): d for d in definition['outputs']}
		for address in (51, 52, 53):
			self.assertEqual('control_signal', outputs['pinmame.output.solenoid', address]['kind'])
		self.assertEqual(2, outputs['pinmame.output.solenoid', 5]['physical']['quantity'])
		self.assertEqual(2, outputs['pinmame.output.solenoid', 7]['physical']['quantity'])
		self.assertNotIn('quantity', outputs['pinmame.output.solenoid', 10]['physical'])
		for address, quantity in [(85, 10), (86, 12), (87, 17)]:
			self.assertEqual('gi', outputs['pinmame.output.lamp', address]['kind'])
			self.assertEqual(quantity, outputs['pinmame.output.lamp', address]['physical']['quantity'])
		self.assertGreaterEqual(len([c for c in definition['conflicts'] if c['status'] == 'unresolved']), 2)
		for device in definition['inputs']:
			if 'normally_closed' in device:
				self.assertTrue(device['normally_closed'])
				self.assertEqual('virtual', device['kind'])
				self.assertIn('eos', device['id'])


if __name__ == '__main__':
	unittest.main()
