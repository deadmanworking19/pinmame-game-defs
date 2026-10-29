"""Replay the left mini-flipper socket's conditional playfield-plane anchor."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def point_digest(points):
    return hashlib.sha256(json.dumps(points, separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def circle_fit(points):
    """Fit a circle to the manually read outer-annulus edge points."""
    if not isinstance(points, list) or len(points) != 8:
        raise ValueError('expected eight edge reads')
    if any(not isinstance(p, list) or len(p) != 2 or
           any(type(v) not in (int, float) or not math.isfinite(v) for v in p) for p in points):
        raise ValueError('invalid edge read')
    ox = sum(p[0] for p in points) / len(points)
    oy = sum(p[1] for p in points) / len(points)
    rows = [[2 * (x - ox), 2 * (y - oy), 1] for x, y in points]
    vals = [(x - ox) ** 2 + (y - oy) ** 2 for x, y in points]
    matrix = [[sum(r[i] * r[j] for r in rows) for j in range(3)] +
              [sum(r[i] * v for r, v in zip(rows, vals))] for i in range(3)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda i: abs(matrix[i][col]))
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        div = matrix[col][col]
        if abs(div) < 1e-12:
            raise ValueError('degenerate circle')
        matrix[col] = [v / div for v in matrix[col]]
        for i in range(3):
            if i != col:
                scale = matrix[i][col]
                matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[col])]
    a, b, c = (row[-1] for row in matrix)
    if c + a * a + b * b <= 0:
        raise ValueError('invalid circle radius')
    return [ox + a, oy + b], math.sqrt(c + a * a + b * b)


def gold_component(get_pixel, roi):
    """Recompute the largest four-connected RGB-threshold component."""
    if roi != [309, 763, 376, 833]:
        raise ValueError('unexpected segmentation region')
    x0, y0, x1, y1 = roi
    mask = set()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = get_pixel((x, y))
            if r > 110 and g > 90 and b > 60 and r > g > b and b / r > .45 and g / r > .70:
                mask.add((x, y))
    components = []
    while mask:
        start = mask.pop()
        todo = [start]
        component = [start]
        while todo:
            x, y = todo.pop()
            for pt in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if pt in mask:
                    mask.remove(pt)
                    todo.append(pt)
                    component.append(pt)
        components.append(component)
    if not components:
        raise ValueError('no gold component')
    ring = max(components, key=len)
    bounds = [min(x for x, y in ring), min(y for x, y in ring),
              max(x for x, y in ring), max(y for x, y in ring)]
    return {'pixels': len(ring), 'bbox': bounds,
            'axis_midpoint': [(bounds[0] + bounds[2]) / 2, (bounds[1] + bounds[3]) / 2]}


def replay(evidence):
    """Validate retained reads and return UV, normalized and world positions."""
    if evidence['format'] != 'simpsons-party-left-socket-anchor-v1':
        raise ValueError('unexpected evidence format')
    texture = evidence['source_texture']
    if (texture['size'] != [1844, 4096] or
        texture['sha256'] != '63af7546fa92967fa6e79a345eeffe7e321793dbad21f23e4747ef0d6df66c5c' or
        evidence['table_bounds'] != [952.94, 2117.65]):
        raise ValueError('source pin or dimensions differ')
    points = evidence['edge_points_native_uv']
    if point_digest(points) != evidence['edge_points_sha256']:
        raise ValueError('edge point digest differs')
    center, radius = circle_fit(points)
    if (math.dist(center, evidence['circle_center_native_uv']) > 1e-7 or
        abs(radius - evidence['circle_radius_px']) > 1e-7 or not 28 < radius < 30 or
        math.dist(center, [340.68339710244305, 797.8231108226538]) > 1e-6):
        raise ValueError('circle differs from reference')
    normalized = [center[i] / texture['size'][i] for i in range(2)]
    world = [normalized[i] * evidence['table_bounds'][i] for i in range(2)]
    if (math.dist(normalized, evidence['normalized_xy']) > 1e-10 or
        math.dist(world, evidence['world_xy']) > 1e-7 or
        [round(v, 2) for v in normalized] != evidence['coarse_xy'] or
        math.dist(center, evidence['segmentation']['axis_midpoint']) > 1):
        raise ValueError('anchor differs from reference')
    return {'center_uv': center, 'radius_px': radius, 'normalized_xy': normalized,
            'world_xy': world, 'coarse_xy': [round(v, 2) for v in normalized]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(json.loads(args.evidence.read_text(encoding='utf-8'))), indent=2))


if __name__ == '__main__':
    main()
