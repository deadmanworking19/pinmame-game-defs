import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json


ROOT = Path(__file__).resolve().parents[1]


class GhostbustersFactsTests(unittest.TestCase):
	def test_own_edition_devices_and_slimer_transport_limits(self):
		d = load_json(ROOT / 'machines/partial/stern/ghostbusters-limited-edition-2016.json')
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
		self.assertEqual('ignored', conflicts['conflict.cpu-interlock-endpoints']['status'])
		for cid in ('conflict.cabinet-slam-sixth-coin', 'conflict.ramp43-physical-identity'):
			self.assertEqual('unresolved', conflicts[cid]['status'])
			self.assertIn('Resolution path:', conflicts[cid]['description'])


if __name__ == '__main__':
	unittest.main()
