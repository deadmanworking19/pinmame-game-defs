"""Replay retained fixed-camera socket measurements without OpenCV or ROM data.

The original calibrated camera matrices come from the retained OpenCV analysis;
this checks the subsequent triangulation, not the calibration or source identity.
"""
import argparse
import json
import math
from pathlib import Path


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('expected a finite number')
    return float(value)


def _vector(value, length):
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f'expected a {length}-element vector')
    return [_number(v) for v in value]


def _solve(matrix, values):
    augmented = [list(row) + [value] for row, value in zip(matrix, values)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda i: abs(augmented[i][col]))
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        if abs(divisor) < 1e-12:
            raise ValueError('singular camera geometry')
        augmented[col] = [v / divisor for v in augmented[col]]
        for row in range(3):
            if row != col:
                factor = augmented[row][col]
                augmented[row] = [v - factor * w for v, w in zip(augmented[row], augmented[col])]
    return [r[-1] for r in augmented]


def triangulate(cameras, readings, image_size):
    """Inhomogeneous least squares from two or more fixed 3x4 cameras."""
    width, height = _vector(image_size, 2)
    if width <= 0 or height <= 0 or len(readings) < 2:
        raise ValueError('need a positive image size and at least two readings')
    by_photo = {}
    for item in cameras:
        photo = item['photo']
        if photo in by_photo:
            raise ValueError('duplicate camera')
        matrix = item['world_to_image_matrix']
        if not isinstance(matrix, list) or len(matrix) != 3:
            raise ValueError('camera must be 3x4')
        by_photo[photo] = [_vector(row, 4) for row in matrix]
    rows, targets, seen = [], [], set()
    for reading in readings:
        photo = reading['photo']
        if photo in seen or photo not in by_photo:
            raise ValueError('duplicate reading or camera missing')
        seen.add(photo)
        u, v = _vector(reading['pixel'], 2)
        if not (0 <= u < width and 0 <= v < height):
            raise ValueError('pixel outside image')
        camera = by_photo[photo]
        for axis, coordinate in ((0, u), (1, v)):
            line = [coordinate * camera[2][i] - camera[axis][i] for i in range(4)]
            rows.append(line[:3])
            targets.append(-line[3])
    normal = [[sum(r[i] * r[j] for r in rows) for j in range(3)] for i in range(3)]
    right = [sum(r[i] * v for r, v in zip(rows, targets)) for i in range(3)]
    point = _solve(normal, right)
    if not all(math.isfinite(v) for v in point):
        raise ValueError('nonfinite point')
    errors = []
    for reading in readings:
        q = [sum(v * w for v, w in zip(row, point + [1.0])) for row in by_photo[reading['photo']]]
        if q[2] <= 1e-12:
            raise ValueError('point behind camera or on image plane')
        pixel = [q[0] / q[2], q[1] / q[2]]
        errors.append({'photo': reading['photo'], 'pixel': pixel,
                       'residual_px': math.dist(pixel, reading['pixel'])})
    return point, errors


def replay(document, name, readings_key='target_pixels'):
    if document.get('format') != 'simpsons-party-photogrammetry-v1':
        raise ValueError('unexpected evidence format')
    width, height = _vector(document['table_bounds'], 2)
    if width <= 0 or height <= 0:
        raise ValueError('table bounds must be positive')
    measurement = document['measurements'][name]
    point, errors = triangulate(measurement['cameras'], measurement[readings_key], document['image_size'])
    xy = [point[0] / width, point[1] / height]
    if not all(0 <= n <= 1 for n in xy):
        raise ValueError('projection outside playfield')
    reference = _vector(measurement['recorded_svd_world'], 3)
    recorded_xy = _vector(measurement['recorded_svd_normalized_xy'], 2)
    if (math.dist(point, reference) > 0.05 or
            math.dist(recorded_xy, [reference[0] / width, reference[1] / height]) > 1e-9 or
            [round(n, 2) for n in xy] != measurement['coarse_xy']):
        raise ValueError('fixed-camera replay differs from recorded SVD measurement')
    return {'world': point, 'normalized_xy': xy, 'coarse_xy': [round(n, 2) for n in xy],
            'reprojections': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path)
    args = parser.parse_args()
    document = json.loads(args.evidence.read_text(encoding='utf-8'))
    print(json.dumps({name: replay(document, name) for name in document['measurements']}, indent=2))


if __name__ == '__main__':
    main()
