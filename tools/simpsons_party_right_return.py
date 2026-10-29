"""Recompute the right-return socket's conditional playfield-plane anchor."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def boundary_digest(points):
    return hashlib.sha256(json.dumps(points, separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def _solve(matrix, target):
    rows = [list(row) + [value] for row, value in zip(matrix, target)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda i: abs(rows[i][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        if abs(divisor) < 1e-12:
            raise ValueError('degenerate circle boundary')
        rows[col] = [v / divisor for v in rows[col]]
        for i in range(3):
            if i != col:
                scale = rows[i][col]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def circle_fit(points):
    """Algebraic least-squares circle; coordinates are centred for stability."""
    if not isinstance(points, list) or len(points) < 20:
        raise ValueError('too few boundary points')
    if any(not isinstance(p, list) or len(p) != 2 or any(type(v) is not int for v in p) for p in points):
        raise ValueError('invalid boundary point')
    ox = sum(p[0] for p in points) / len(points)
    oy = sum(p[1] for p in points) / len(points)
    rows = [[2 * (x - ox), 2 * (y - oy), 1] for x, y in points]
    values = [(x - ox) ** 2 + (y - oy) ** 2 for x, y in points]
    normal = [[sum(row[i] * row[j] for row in rows) for j in range(3)] for i in range(3)]
    rhs = [sum(row[i] * value for row, value in zip(rows, values)) for i in range(3)]
    a, b, c = _solve(normal, rhs)
    radius_squared = c + a * a + b * b
    if radius_squared <= 0:
        raise ValueError('invalid fitted radius')
    return [ox + a, oy + b], math.sqrt(radius_squared)


def replay(evidence):
    """Check pinned contour identities and return UV, normalized and world positions."""
    if evidence['format'] != 'simpsons-party-right-return-anchor-v1':
        raise ValueError('unexpected evidence format')
    if (evidence['source_texture']['size'] != [1844, 4096] or
            evidence['source_texture']['sha256'] != '63af7546fa92967fa6e79a345eeffe7e321793dbad21f23e4747ef0d6df66c5c' or
            evidence['table_bounds'] != [952.94, 2117.65]):
        raise ValueError('source dimensions or table bounds differ')
    measurements = evidence['measurements']
    if [m['threshold'] for m in measurements] != [25, 35, 45, 55]:
        raise ValueError('thresholds differ')
    x0, y0, x1, y1 = evidence['roi']
    if [x0, y0, x1, y1] != [1420, 3120, 1545, 3265]:
        raise ValueError('ROI differs')
    centers = []
    for item in measurements:
        points = item['boundary_pixels']
        if boundary_digest(points) != item['boundary_sha256']:
            raise ValueError('boundary digest differs')
        center, radius = circle_fit(points)
        if any(not (x0 <= p[0] < x1 and y0 <= p[1] < y1) for p in points):
            raise ValueError('boundary point outside ROI')
        if not 33 <= radius <= 36 or math.dist(center, item['ellipse_center']) > 0.01:
            raise ValueError('circle and retained ellipse do not agree')
        centers.append(center)
    uv = [sum(p[i] for p in centers) / len(centers) for i in (0, 1)]
    normalized = [uv[i] / evidence['source_texture']['size'][i] for i in (0, 1)]
    world = [normalized[i] * evidence['table_bounds'][i] for i in (0, 1)]
    if (math.dist(evidence['normalized_xy'], [0.8022919063195748, 0.7801739503629506]) > 1e-12 or
            math.dist(uv, evidence['ellipse_mean_uv']) > 0.01 or
            math.dist(normalized, evidence['normalized_xy']) > 0.00001 or
            [round(v, 2) for v in normalized] != evidence['coarse_xy'] or
            math.dist(world, evidence['world_xy']) > 0.01):
        raise ValueError('replayed anchor differs from reference')
    return {'circle_centers_uv': centers, 'mean_uv': uv, 'normalized_xy': normalized,
            'world_xy': world, 'coarse_xy': [round(v, 2) for v in normalized]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    print(json.dumps(replay(json.loads(args.evidence.read_text(encoding='utf-8'))), indent=2))


if __name__ == '__main__':
    main()
