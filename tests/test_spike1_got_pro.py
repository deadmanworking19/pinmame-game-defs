import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class GameOfThronesProFactsTests(unittest.TestCase):
	def test_own_pro_hardware_and_withheld_factory_specifications(self):
		d = load_json(ROOT / 'machines/partial/stern/game-of-thrones-pro-2015.json')
		self.assertEqual(('G41d5-MKNwX', 6307), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		self.assertEqual(['got_137'], [v['id'] for v in d['drivers']])
		self.assertFalse((ROOT / 'machines/stubs/got_137h.json').exists())
		outputs = {v['binding']['device']: v for v in d['outputs'] if v['binding']['group'] == 'pinmame.output.solenoid'}
		self.assertNotIn('part_number', outputs[14]['physical'])
		self.assertEqual('conflicted', outputs[14]['provenance']['status'])
		self.assertEqual('coil', outputs[18]['kind'])
		self.assertEqual('090-5001-ND', outputs[18]['physical']['part_number'])
		self.assertEqual('virtual', outputs[26]['kind'])
		self.assertEqual('unused', outputs[26]['availability'])
		interlock = next(i for i in d['inputs'] if i['id'] == 'switch.pwr-interlock-sense')
		self.assertEqual({'board': 'SPIKE Node 0', 'control_connection': 'CN7 pin 4'}, interlock['wiring'])
		self.assertNotIn('part_number', interlock['physical'])
		self.assertNotIn('normally_closed', interlock)
		mechanisms = {m['id']: m for m in d['mechanisms']}
		bank = mechanisms['mechanism.three-drop-targets-and-shared-reset']
		self.assertEqual(['coil.3-bank-drop-reset'], bank['actuators'])
		self.assertEqual(3, len(bank['sensors']))


if __name__ == '__main__':
	unittest.main()
