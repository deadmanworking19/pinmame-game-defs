import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class PabstFactsTests(unittest.TestCase):
	def test_reels_driven_bumpers_and_unproven_lcd_mounting(self):
		d = load_json(ROOT / 'machines/partial/stern/pabst-can-crusher-2016.json')
		self.assertEqual(('GRYX4-MRjVP', 6335), (d['machine']['opdb_id'], d['machine']['ipdb_id']))
		reels = [m for m in d['mechanisms'] if m['kind'] == 'reel']
		self.assertEqual(5, len(reels))
		self.assertTrue(all(not m['actuators'] and len(m['sensors']) == 1 for m in reels))
		outputs = {v['binding']['device']: v for v in d['outputs'] if v['binding']['group'] == 'pinmame.output.solenoid'}
		for n in range(9, 13):
			self.assertEqual('coil', outputs[n]['kind'])
			self.assertEqual('used', outputs[n]['availability'])
		for n in (51, 52, 53):
			self.assertEqual('control_signal', outputs[n]['kind'])
		self.assertTrue(all(outputs[n]['kind'] == 'virtual' for n in range(17, 32)))
		self.assertEqual('video', d['displays'][0]['kind'])
		self.assertNotIn('physical_location', d['displays'][0])
		self.assertEqual((128, 32), (d['displays'][0]['width'], d['displays'][0]['height']))
		note = (ROOT / d['knowledge']['path']).read_text(encoding='utf-8')
		self.assertNotIn('passive bumpers', note.lower())


if __name__ == '__main__':
	unittest.main()
