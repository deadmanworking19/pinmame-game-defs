import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class GameOfThronesLEFactsTests(unittest.TestCase):
	def test_edition_split_conflicted_coil_and_unbound_factory_light(self):
		d = load_json(ROOT / 'machines/partial/stern/game-of-thrones-limited-edition-2015.json')
		self.assertEqual(('G41d5-M9REd', 6309), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		catalog = load_json(ROOT / 'catalog/pinmame.json')
		owners = {v['id']: v['definition'] for v in catalog['drivers']}
		self.assertNotEqual(owners['got_137h'], owners['got_137'])
		inputs = {v['binding']['device']: v for v in d['inputs'] if v['binding']['group'] == 'pinmame.input.switch'}
		self.assertEqual('unknown', inputs[75]['availability'])
		self.assertNotIn('wiring', inputs[75])
		outputs = {(v['binding']['group'], v['binding']['device']): v for v in d['outputs']}
		self.assertNotIn('part_number', outputs['pinmame.output.solenoid', 14].get('physical', {}))
		self.assertEqual('virtual', outputs['pinmame.output.lamp', 245]['kind'])
		for n in range(225, 229):
			self.assertEqual('gi', outputs['pinmame.output.lamp', n]['kind'])
		mechanisms = {m['id']: m for m in d['mechanisms']}
		self.assertEqual(['solenoid.014'], mechanisms['mechanism.three-bank-drop-reset']['actuators'])
		self.assertEqual(['switch.007', 'switch.008', 'switch.009'], mechanisms['mechanism.three-bank-drop-reset']['sensors'])
		self.assertEqual(['switch.012'], mechanisms['mechanism.upper-right-flipper']['sensors'])
		self.assertEqual(['switch.013'], mechanisms['mechanism.upper-left-flipper']['sensors'])
		self.assertTrue(any(e['path'].endswith('/unbound-physical.json.txt') for s in d['sources'] for e in s.get('excerpts', [])))


if __name__ == '__main__':
	unittest.main()
