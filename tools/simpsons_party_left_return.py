"""Replay the fourth left sling/return socket's own flat annulus projection."""
import math

from simpsons_party_right_return import boundary_digest, circle_fit


def boundary(get_gray, roi, threshold):
    """Outer edge of the largest light region enclosed by the black annulus.

    The tan/wood centre is an enclosed hole in the thresholded black ring.
    Its boundary supplies the inner annulus axis, without neighboring artwork.
    Coordinates are native source pixel centres; no source image is rescaled.
    """
    x0, y0, x1, y1 = roi
    pixels = {(x, y) for y in range(y0, y1) for x in range(x0, x1)}
    dark = {p for p in pixels if get_gray(p) < threshold}
    remaining = pixels - dark
    components = []
    offsets = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
    while remaining:
        point = remaining.pop()
        component, todo = {point}, [point]
        while todo:
            x, y = todo.pop()
            for dx, dy in offsets:
                q = x + dx, y + dy
                if q in remaining:
                    remaining.remove(q)
                    component.add(q)
                    todo.append(q)
        if not any(x in (x0, x1 - 1) or y in (y0, y1 - 1) for x, y in component):
            components.append(component)
    if not components:
        raise ValueError('no enclosed annulus region')
    interior = max(components, key=len)
    outside = {p for p in pixels - interior if p[0] in (x0, x1 - 1) or p[1] in (y0, y1 - 1)}
    todo = list(outside)
    while todo:
        x, y = todo.pop()
        for q in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if q in pixels and q not in interior and q not in outside:
                outside.add(q)
                todo.append(q)
    return [list(p) for p in sorted(interior)
            if any((p[0] + dx, p[1] + dy) in outside for dx, dy in offsets)]


def replay(evidence):
    if evidence['source_texture']['sha256'] != '63af7546fa92967fa6e79a345eeffe7e321793dbad21f23e4747ef0d6df66c5c':
        raise ValueError('source texture differs')
    centers = []
    for item in evidence['replayed_boundaries']:
        if boundary_digest(item['pixels']) != item['sha256']:
            raise ValueError('boundary identity differs')
        center, radius = circle_fit(item['pixels'])
        if not 28 < radius < 32:
            raise ValueError('annulus radius differs')
        centers.append(center)
    if len(centers) != 4:
        raise ValueError('expected four threshold fits')
    uv = [sum(c[i] for c in centers) / len(centers) for i in (0, 1)]
    xy = [uv[0] / 1844, uv[1] / 4096]
    if (math.dist(uv, evidence['replayed_center_uv']) > 1e-7 or
            math.dist(uv, evidence['source_center_native_pixels']) > .1 or
            [round(v, 2) for v in xy] != [.11, .78]):
        raise ValueError('socket anchor differs')
    return {'center_uv': uv, 'normalized_xy': xy, 'coarse_xy': [round(v, 2) for v in xy]}
