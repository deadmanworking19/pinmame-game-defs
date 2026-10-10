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


if __name__ == '__main__':
	unittest.main()
