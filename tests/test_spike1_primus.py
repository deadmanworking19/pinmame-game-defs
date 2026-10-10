import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class PrimusFactsTests(unittest.TestCase):
	def test_own_title_reels_and_apron_lcd_preserve_internal_transport_limits(self):
		definition = load_json(ROOT / 'machines/partial/stern/primus-2018.json')
		self.assertEqual('GRYX4-MvBpz', definition['machine']['opdb_id'])
		self.assertEqual(6610, definition['machine']['ipdb_id'])
		reels = [m for m in definition['mechanisms'] if m['kind'] == 'reel']
		self.assertEqual(5, len(reels))
		self.assertTrue(all(not m['actuators'] for m in reels))
		self.assertTrue(all(len(m['sensors']) == 1 for m in reels))
		self.assertEqual(1, len(definition['displays']))
		self.assertEqual('playfield', definition['displays'][0]['physical_location'])
		self.assertIn('apron', definition['displays'][0]['id'])
		outputs = {d['binding']['device']: d for d in definition['outputs'] if d['binding']['group'] == 'pinmame.output.solenoid'}
		for address in (51, 52, 53):
			self.assertEqual('control_signal', outputs[address]['kind'])
		self.assertTrue(all(outputs[address]['kind'] == 'virtual' for address in range(17, 32)))
		self.assertIn('polarity', definition['coverage']['missing'])


if __name__ == '__main__':
	unittest.main()
