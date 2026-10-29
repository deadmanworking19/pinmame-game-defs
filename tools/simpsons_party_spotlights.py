"""Replay conditional #555 spotlight filament projections from selected socket vertices.

The selected neck, mouth and socket vertices are retained in compact evidence;
this does not establish that a physical filament was directly observed.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def selection_sha256(selections):
    raw = json.dumps(selections, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def _points(selections, key, expected_count):
    values = selections[key]
    if not isinstance(values, list) or len(values) != expected_count:
        raise ValueError(f'{key}: wrong vertex count')
    result = []
    for entry in values:
        if not isinstance(entry['index'], int) or isinstance(entry['index'], bool) or entry['index'] < 0:
            raise ValueError('invalid vertex index')
        point = entry['xyz']
        if (not isinstance(point, list) or len(point) != 3 or
                any(isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) for n in point)):
            raise ValueError('invalid vertex coordinates')
        result.append(point)
    return result


def project(record, evidence):
    selections = record['selections']
    neck_points = _points(selections, 'neck', 25)
    mouth_points = _points(selections, 'mouth', 48)
    socket_points = _points(selections, 'socket', 56)
    indices = [p['index'] for key in ('neck', 'mouth', 'socket') for p in selections[key]]
    if len(indices) != len(set(indices)) or selection_sha256(selections) != record['selection_sha256']:
        raise ValueError('selected vertex identity differs')
    bounds = evidence['table_bounds']
    if bounds != [952.94, 2117.65] or evidence['units']['vpu_per_ball'] != 50 or evidence['units']['ball_diameter_inches'] != 1.0625:
        raise ValueError('unexpected table bounds or unit definition')
    if evidence['bulb']['light_center_length_mm'] != 16.5 or evidence['scale_allowance_fraction'] != 0.1:
        raise ValueError('unexpected bulb specification or scale allowance')
    mean = lambda points: [sum(point[i] for point in points) / len(points) for i in range(3)]
    neck, mouth = mean(neck_points), mean(mouth_points)
    direction = [b - a for a, b in zip(neck, mouth)]
    length = math.sqrt(sum(v * v for v in direction))
    if length < 1e-9:
        raise ValueError('degenerate socket axis')
    axis = [v / length for v in direction]
    axial = [sum((point[i] - neck[i]) * axis[i] for i in range(3)) for point in socket_points]
    seat = [min(axial), max(axial)]
    if seat[1] - seat[0] < 1e-9:
        raise ValueError('degenerate socket seat range')
    lcl = 16.5 * 50 / (1.0625 * 25.4)
    endpoints = [[neck[i] + (offset + lcl) * axis[i] for i in range(3)] for offset in seat]
    point = [(a + b) / 2 for a, b in zip(*endpoints)]
    xy = [point[i] / bounds[i] for i in (0, 1)]
    halfspan = [abs(axis[i]) * ((seat[1] - seat[0]) / 2 + lcl * 0.1) / bounds[i] for i in (0, 1)]
    if not all(0 <= v <= 1 for v in xy):
        raise ValueError('projected point outside playfield')
    if (math.dist(point, record['conditional_filament_world']) > 1e-6 or
            math.dist(seat, record['socket_axial_span_vpu']) > 1e-6 or
            [round(v, 2) for v in xy] != record['coarse_xy'] or
            math.dist(halfspan, record['seat_and_scale_halfspan_xy']) > 1e-8):
        raise ValueError('projection differs from retained measurement')
    return {'neck': neck, 'axis': axis, 'seat_range': seat, 'world': point,
            'seat_endpoint_world': endpoints, 'normalized_xy': xy,
            'coarse_xy': [round(v, 2) for v in xy], 'seat_and_scale_halfspan_xy': halfspan}


def verify_obj(path, evidence):
    """Verify exact source OBJ and the global zero-based vertex selections."""
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    if digest.hexdigest() != evidence['world_obj']['sha256']:
        raise ValueError('world OBJ SHA-256 differs')
    wanted = {entry['index']: entry['xyz'] for record in evidence['records']
              for values in record['selections'].values() for entry in values}
    found = set()
    index = 0
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            if line.startswith('v '):
                if index in wanted:
                    xyz = [round(float(value), 4) for value in line.split()[1:4]]
                    if xyz != wanted[index]:
                        raise ValueError(f'vertex {index} differs')
                    found.add(index)
                index += 1
    if found != set(wanted):
        raise ValueError('selected vertex missing')
    for record in evidence['records']:
        project(record, evidence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    parser.add_argument('--world-obj', type=Path)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding='utf-8'))
    if args.world_obj:
        verify_obj(args.world_obj, evidence)
    print(json.dumps({r['object']: project(r, evidence) for r in evidence['records']}, indent=2))


if __name__ == '__main__':
    main()
