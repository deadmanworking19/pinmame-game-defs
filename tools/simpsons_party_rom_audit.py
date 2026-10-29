"""Bounded, reproducible static evidence from the four Simpsons Party CPU ROMs.

This is an operand-byte scan, not a disassembler or a proof about indexed writes.
ROM inputs remain external; only short instruction excerpts are emitted.
"""

import argparse
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path


SOURCE_PATH = Path('src/wpc/segames.c')
SOURCE_REVISION = '46e1a01a0f73dc5ce163d98db1ae435883ecc450'
SOURCE_URI = f'https://github.com/vpinball/pinmame/blob/{SOURCE_REVISION}/src/wpc/segames.c'
SOURCE_SHA256 = '205dca0bd34d32c711aa99ac9c40dc02e91a0caaf3d3ccb1108f98aee03d69d4'
DRIVERS = {
    '500': ('simpprty', 'simpprtg', 'simpprtl', 'simpprtf', 'simpprti'),
    '400': ('simp400', 'simp400g', 'simp400l', 'simp400f', 'simp400i'),
    '300': ('simp300', 'simp300l', 'simp300f', 'simp300i'),
    '204': ('simp204', 'simp204l', 'simp204f', 'simp204i'),
}
WORDS = (0x0100, 0x0200, 0x0400, 0x0800, 0x1000, 0x2000, 0x4000, 0x8000, 0x0001, 0x0002)
TABLE = bytes.fromhex('0100 0200 0400 0800 1000 2000 4000 8000 0001 0002')

# Literal 6809 instruction signature from the fixed-bank writer. AC is its
# scratch direct-page operand (A8 in 2.04); the LDX operand is the located table.
SCANNER = bytes.fromhex('''
4f d6 17 1f 01 96 18 81 02 25 24 a6 88 5f a4 88 69 97 ac
a6 88 5f 43 a4 88 37 a4 88 4b 9a ac 97 ac a6 88 5f aa 88 37
43 a4 88 19 9a ac 20 22 a6 88 5f a4 88 69 97 ac a6 88 5f
43 a4 88 37 a4 88 41 9a ac 97 ac a6 88 5f aa 88 37 43 a4
88 19 9a ac 58 dd ac 96 17 4c 81 0a 25 1d 4f 7c 02 3d d6 18
c1 02 25 03 5f 20 01 5c d7 18 be 02 40 27 08 be 15 02 30 01
bf 15 02 97 17 dc ac b7 20 0a 8e b2 1a ec 85 fd 20 08 39
''')
BOUND = bytes.fromhex('96 17 4c 81 0a 25 1d 4f')
RESET = bytes.fromhex('cc 00 00 b7 20 0a fd 20 08')
BOOT = bytes.fromhex('4f 5f fd 20 08')


def digest(data, algorithm):
    return hashlib.new(algorithm, data).hexdigest()


def unique(data, pattern, label):
    hits = [i for i in range(len(data) - len(pattern) + 1) if data[i:i + len(pattern)] == pattern]
    if len(hits) != 1:
        raise ValueError(f'{label}: expected one match, found {len(hits)}')
    return hits[0]


def validate_table(data):
    if len(data) != 20:
        raise ValueError('strobe table must contain exactly ten words')
    words = tuple(int.from_bytes(data[i:i + 2], 'big') for i in range(0, len(data), 2))
    if words != WORDS:
        raise ValueError('unexpected strobe words')
    return words


def scanner_signature(scratch, table_address):
    if scratch not in (0xac, 0xa8) or not 0x8000 <= table_address <= 0xffff:
        raise ValueError('unexpected scanner operands')
    code = SCANNER.replace(b'\xac', bytes([scratch]))
    marker = bytes.fromhex('8e b2 1a ec 85 fd 20 08 39')
    replacement = b'\x8e' + table_address.to_bytes(2, 'big') + bytes.fromhex('ec 85 fd 20 08 39')
    return code.replace(marker, replacement)


def validate_scanner(code, table_address):
    matches = [s for s in (0xac, 0xa8) if code == scanner_signature(s, table_address)]
    if len(matches) != 1:
        raise ValueError('unexpected scanner instruction signature or counter bound')
    return matches[0]


def scan_operands(data, targets, opcodes, start=0, end=None):
    """Find opcode/extended-operand byte sequences in [start,end); include data hits."""
    if end is None:
        end = len(data)
    if not 0 <= start <= end <= len(data):
        raise ValueError('invalid scan bounds')
    found = []
    for i in range(start, max(start, end - 2)):
        op = data[i]
        if op not in opcodes:
            continue
        address = int.from_bytes(data[i + 1:i + 3], 'big')
        width, mnemonic = opcodes[op]
        if not any(address <= target < address + width for target in targets):
            continue
        found.append({'offset': i, 'opcode': f'{op:02x}', 'mnemonic': mnemonic,
                      'operand': f'{address:04x}', 'width': width,
                      'context_offset': max(start, i - 8),
                      'context_hex': data[max(start, i - 8):min(end, i + 11)].hex(' ')})
    return found


def source_entries(source):
    if digest(source, 'sha256') != SOURCE_SHA256:
        raise ValueError('pinned segames.c SHA-256 differs')
    text = source.decode('utf-8')
    entries = {}
    for revision, names in DRIVERS.items():
        for driver in names:
            pattern = (r'SE128_ROMSTART\(\s*' + re.escape(driver) +
                       r'\s*,\s*"(spp-cpu\.' + revision + r')"\s*,\s*CRC\([0-9a-f]+\)\s*SHA1\(([0-9a-f]{40})\)\)')
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if len(matches) != 1:
                raise ValueError(f'{driver}: expected exactly one source entry')
            match = matches[0]
            entries[driver] = {'member': match.group(1), 'sha1': match.group(2).lower(),
                               'source_line': text.count('\n', 0, match.start()) + 1}
        if len({entries[n]['sha1'] for n in names}) != 1:
            raise ValueError(f'{revision}: driver CPU hashes disagree')
    return entries


def verify_member(data, expected_sha1):
    if len(data) != 131072 or digest(data, 'sha1') != expected_sha1:
        raise ValueError('CPU member size or source SHA-1 mismatch')
    return {'size': len(data), 'sha1': digest(data, 'sha1'), 'sha256': digest(data, 'sha256')}


def read_archive(root, name, member):
    path = root / (name + '.zip')
    if not path.is_file():
        return None
    raw = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names.count(member) > 1:
            raise ValueError(f'{path}: duplicate expected member')
        data = archive.read(member) if member in names else None
        cpu_members = sorted(n for n in names if n.lower().startswith('spp-cpu.'))
    return {'archive': path.name, 'archive_sha256': digest(raw, 'sha256'),
            'archive_sha1': digest(raw, 'sha1'), 'cpu_members': cpu_members}, data


def resolve_driver(root, driver, expected):
    own = read_archive(root, driver, expected['member'])
    parent = None if driver == 'simpprty' else read_archive(root, 'simpprty', expected['member'])
    for candidate in (own, parent):
        if candidate is not None and candidate[1] is not None:
            info, data = candidate
            hashes = verify_member(data, expected['sha1'])
            return {'driver': driver, 'expected_member': expected['member'],
                    'source_sha1': expected['sha1'], 'source_line': expected['source_line'],
                    'own_archive': own[0] if own else None,
                    'resolved_archive': info, 'parent_fallback': candidate is parent,
                    'member_hashes': hashes}, data
    raise ValueError(f'{driver}: expected member absent from own and parent archives')


def audit_cpu(data):
    if len(data) != 131072:
        raise ValueError('CPU image must be 131072 bytes')
    table_offset = unique(data, TABLE, 'strobe table')
    validate_table(data[table_offset:table_offset + 20])
    if not 0x18000 <= table_offset <= 0x1ffec:
        raise ValueError('strobe table outside fixed CPU bank')
    address = table_offset - 0x10000
    candidates = []
    for scratch in (0xac, 0xa8):
        signature = scanner_signature(scratch, address)
        pos = data.find(signature)
        while pos >= 0:
            candidates.append((pos, signature))
            pos = data.find(signature, pos + 1)
    if len(candidates) != 1:
        raise ValueError(f'scanner: expected one exact signature, found {len(candidates)}')
    offset, signature = candidates[0]
    validate_scanner(signature, address)
    if not (0x18000 <= offset and offset + len(signature) <= 0x20000):
        raise ValueError('scanner outside fixed CPU bank')
    bound = unique(signature, BOUND, 'counter bound')
    reset, boot = unique(data, RESET, 'reset sequence'), unique(data, BOOT, 'boot clear')
    stores = [hit for hit in scan_operands(data, {0x2008}, {0xfd: (2, 'STD extended')})
              if hit['operand'] == '2008']
    strobes = scan_operands(data, {0x200a}, {0xb7: (1, 'STA extended')})
    if [hit['offset'] for hit in stores] != sorted([boot + 2, reset + 6, offset + len(signature) - 4]):
        raise ValueError('unexpected STD 2008 byte-pattern locations')
    if [hit['offset'] for hit in strobes] != sorted([reset + 3, offset + len(signature) - 12]):
        raise ValueError('unexpected STA 200a byte-pattern locations')
    # Conservative raw scan: BF/FF also include possible prefixed STY/STS.
    ops = {0xb7: (1, 'STA'), 0xf7: (1, 'STB'), 0xfd: (2, 'STD'),
           0xbf: (2, 'STX / prefixed STY'), 0xff: (2, 'STU / prefixed STS')}
    ops.update({op: (1, name) for op, name in ((0x70, 'NEG'), (0x73, 'COM'), (0x74, 'LSR'),
               (0x76, 'ROR'), (0x77, 'ASR'), (0x78, 'ASL'), (0x79, 'ROL'),
               (0x7a, 'DEC'), (0x7c, 'INC'), (0x7f, 'CLR'))})
    return {'image_scan_bounds': [0, len(data)], 'table_offset': table_offset,
            'table_cpu_address': f'{address:04x}', 'strobe_words': [f'{w:04x}' for w in WORDS],
            'scanner': {'offset_start': offset, 'offset_end_exclusive': offset + len(signature),
                        'cpu_start': f'{offset - 0x10000:04x}',
                        'cpu_end_inclusive': f'{offset + len(signature) - 1 - 0x10000:04x}',
                        'writer_tail_hex': signature[-12:].hex(' '), 'counter_bound_offset': offset + bound,
                        'counter_bound_hex': BOUND.hex(' '),
                        'meaning': 'RAM 0017 counter increments, compares with 0a and resets at 10; doubled old index selects ten big-endian words; A writes 2008 and B writes 2009, so B is 00, 01 or 02.'},
            'reset_offset': reset, 'reset_hex': RESET.hex(' '),
            'reset_disassembly': 'LDD #0000; STA 200A; STD 2008',
            'boot_offset': boot, 'boot_hex': BOOT.hex(' '),
            'boot_disassembly': 'CLRA; CLRB; STD 2008',
            'std_2008_candidates': stores, 'sta_200a_candidates': strobes,
            'extended_3406_3407_candidates': scan_operands(data, {0x3406, 0x3407}, ops),
            'limitations': 'Full image byte-operand scan includes possible data or unaligned false positives. It covers listed extended stores and read-modify-write opcodes, including word stores starting at 3405. It does not prove absence of arbitrary indexed or indirect writes, or physical lamps.'}


def build_report(root, source):
    entries = source_entries(source)
    drivers, revisions = [], {}
    for revision, names in DRIVERS.items():
        images = []
        for driver in names:
            info, data = resolve_driver(root, driver, entries[driver])
            drivers.append(info)
            images.append(data)
        if any(image != images[0] for image in images[1:]):
            raise ValueError(f'{revision}: resolved clone CPU images differ')
        revisions[revision] = audit_cpu(images[0])
    return {'format': 'simpsons-party-rom-audit-v1',
            'source': {'uri': SOURCE_URI, 'sha256': digest(source, 'sha256'), 'revision': SOURCE_REVISION},
            'authority': 'Static ROM audit describes writer padding, not physical presence. Manual controls physical circuits; working script controls runtime; pinned source controls emulator metadata.',
            'coordinate_convention': 'x left to right; y rear to apron',
            'drivers': drivers, 'revisions': revisions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom-root', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, default=os.environ.get('PINMAME_SOURCE_ROOT'),
                        help='pinned PinMAME checkout (or PINMAME_SOURCE_ROOT)')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.source_root:
        parser.error('--source-root or PINMAME_SOURCE_ROOT is required')
    if args.output:
        output = args.output.resolve()
        worktree = Path(__file__).resolve().parent.parent
        if output.is_relative_to(worktree) or output.is_relative_to(args.rom_root.resolve()):
            parser.error('--output must be outside the worktree and ROM library')
    report = build_report(args.rom_root, (Path(args.source_root) / SOURCE_PATH).read_bytes())
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8', newline='\n')
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
