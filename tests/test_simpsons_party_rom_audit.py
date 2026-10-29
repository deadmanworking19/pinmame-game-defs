import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from unittest import mock
import zipfile

import simpsons_party_rom_audit as audit


# Factual instruction excerpt, CPU AB63..AB96 in the 5.00 image: increment
# and bound the counter, then select the table and store the strobe word.
COUNTER_AND_WRITER = bytes.fromhex('''
96 17 4c 81 0a 25 1d 4f 7c 02 3d d6 18 c1 02 25 03 5f 20 01
5c d7 18 be 02 40 27 08 be 15 02 30 01 bf 15 02 97 17 dc ac
b7 20 0a 8e b2 1a ec 85 fd 20 08 39
''')


class AuditTests(unittest.TestCase):
    def test_documented_instruction_sequence_and_mutated_counter_bound(self):
        signature = audit.SCANNER
        self.assertTrue(signature.endswith(COUNTER_AND_WRITER))
        self.assertEqual(audit.validate_scanner(signature, 0xb21a), 0xac)
        changed = signature.replace(bytes.fromhex('81 0a 25 1d'), bytes.fromhex('81 0b 25 1d'))
        with self.assertRaisesRegex(ValueError, 'counter bound'):
            audit.validate_scanner(changed, 0xb21a)
        with self.assertRaises(ValueError):
            audit.validate_scanner(signature, 0xb207)

    def test_strobes_and_mutations(self):
        self.assertEqual(audit.validate_table(bytes.fromhex(
            '01 00 02 00 04 00 08 00 10 00 20 00 40 00 80 00 00 01 00 02')),
            (256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 1, 2))
        for bad in (audit.TABLE[:-1], audit.TABLE[:-2] + b'\x00\x04', audit.TABLE + b'\x00'):
            with self.assertRaises(ValueError):
                audit.validate_table(bad)

    def test_scan_bounds_and_word_straddle(self):
        data = bytes.fromhex('00 fd 34 05 b7 34 07 7c 34 06 fd 34 07')
        ops = {0xfd: (2, 'STD'), 0xb7: (1, 'STA'), 0x7c: (1, 'INC')}
        hits = audit.scan_operands(data, {0x3406, 0x3407}, ops)
        self.assertEqual([h['offset'] for h in hits], [1, 4, 7, 10])
        self.assertEqual([h['offset'] for h in audit.scan_operands(data, {0x3406, 0x3407}, ops, 1, 10)], [1, 4, 7])
        with self.assertRaises(ValueError):
            audit.scan_operands(data, {0x3406}, ops, 0, len(data) + 1)
        with self.assertRaises(ValueError):
            audit.scan_operands(data, {0x3406}, ops, 4, 3)

    def test_member_hash_guard(self):
        data = bytes(131072)
        expected = hashlib.sha1(data).hexdigest()
        self.assertEqual(audit.verify_member(data, expected)['size'], 131072)
        with self.assertRaises(ValueError):
            audit.verify_member(data[:-1] + b'\x01', expected)
        with self.assertRaises(ValueError):
            audit.verify_member(data[:-1], expected)

    def test_clone_fallback_and_bad_own_member(self):
        cpu = bytes(131072)
        expected = {'member': 'spp-cpu.500', 'sha1': hashlib.sha1(cpu).hexdigest(), 'source_line': 1}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with zipfile.ZipFile(root / 'simpprty.zip', 'w') as archive:
                archive.writestr('spp-cpu.500', cpu)
            with zipfile.ZipFile(root / 'simpprtg.zip', 'w') as archive:
                archive.writestr('spp-cpu.400', b'other revision')
            info, resolved = audit.resolve_driver(root, 'simpprtg', expected)
            self.assertTrue(info['parent_fallback'])
            self.assertEqual(info['own_archive']['cpu_members'], ['spp-cpu.400'])
            self.assertEqual(resolved, cpu)
            with zipfile.ZipFile(root / 'simpprtg.zip', 'w') as archive:
                archive.writestr('spp-cpu.500', cpu[:-1] + b'\x01')
            with self.assertRaisesRegex(ValueError, 'SHA-1 mismatch'):
                audit.resolve_driver(root, 'simpprtg', expected)

    def test_pinned_source_guard_and_entry_hash(self):
        source = '\n'.join(
            f'SE128_ROMSTART({name}, "spp-cpu.{rev}", CRC(12345678) SHA1({rev[0] * 40}))'
            for rev, names in audit.DRIVERS.items() for name in names).encode()
        with mock.patch.object(audit, 'SOURCE_SHA256', hashlib.sha256(source).hexdigest()):
            entries = audit.source_entries(source)
            self.assertEqual(entries['simp400g']['sha1'], '4' * 40)
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                audit.source_entries(source + b' ')

    def test_source_clone_disagreement_rejected(self):
        lines = [f'SE128_ROMSTART({name}, "spp-cpu.{rev}", CRC(12345678) SHA1({rev[0] * 40}))'
                 for rev, names in audit.DRIVERS.items() for name in names]
        lines[1] = lines[1].replace('5' * 40, 'a' * 40)
        source = '\n'.join(lines).encode()
        with mock.patch.object(audit, 'SOURCE_SHA256', hashlib.sha256(source).hexdigest()):
            with self.assertRaisesRegex(ValueError, 'hashes disagree'):
                audit.source_entries(source)

    @unittest.skipUnless(os.environ.get('PINMAME_ROM_LIBRARY_ROOT') and os.environ.get('PINMAME_SOURCE_ROOT'),
                         'optional ROM library and source root not configured')
    def test_real_rom_library(self):
        source = Path(os.environ['PINMAME_SOURCE_ROOT']) / audit.SOURCE_PATH
        report = audit.build_report(Path(os.environ['PINMAME_ROM_LIBRARY_ROOT']), source.read_bytes())
        evidence = Path(__file__).resolve().parents[1] / 'tools/seeds/stern/the-simpsons-pinball-party-2003/lamp-scan.json'
        self.assertEqual(report, json.loads(evidence.read_text(encoding='utf-8')))
        self.assertEqual(len(report['drivers']), 18)
        self.assertEqual({key: value['table_offset'] for key, value in report['revisions'].items()},
                         {'500': 0x1b21a, '400': 0x1b207, '300': 0x1b1e4, '204': 0x1b16e})
        for revision in report['revisions'].values():
            self.assertEqual(len(revision['std_2008_candidates']), 3)
            self.assertEqual(len(revision['sta_200a_candidates']), 2)
            self.assertEqual(revision['extended_3406_3407_candidates'], [])


if __name__ == '__main__':
    unittest.main()
