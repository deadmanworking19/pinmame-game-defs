import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class KissLEFactsTests(unittest.TestCase):
	def test_motor_lamp_transport_blank_cells_and_recorded_wiring_discrepancies(self):
		d = load_json(ROOT / 'machines/partial/stern/kiss-limited-edition-2015.json')
		self.assertEqual(('G4qX5-Ml9jb', 6267), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		lamps = {v['binding']['device']: v for v in d['outputs'] if v['binding']['group'] == 'pinmame.output.lamp'}
		for n in range(165, 169):
			self.assertEqual('gi', lamps[n]['kind'])
		self.assertEqual(2, lamps[165]['physical']['quantity'])
		for n in range(169, 173):
			self.assertEqual('motor', lamps[n]['kind'])
			self.assertEqual('Playfield', lamps[n]['physical']['location'])
			self.assertNotIn('spatial', lamps[n])
		for n in (170, 172):
			self.assertNotIn('part_number', lamps[n]['physical'])
		self.assertTrue(all(c['status'] == 'ignored' for c in d['conflicts']))
		self.assertNotIn('unresolved_conflicts', d['coverage']['missing'])
		inputs = {v['binding']['device']: v for v in d['inputs'] if v['binding']['group'] == 'pinmame.input.switch'}
		for n in (65, 66):
			self.assertTrue(inputs[n]['normally_closed'])
			self.assertEqual('180-5149-00', inputs[n]['physical']['part_number'])
			self.assertIn('synthesized', inputs[n]['physical']['notes'])


if __name__ == '__main__':
	unittest.main()
