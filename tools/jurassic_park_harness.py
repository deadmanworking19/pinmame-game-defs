"""Exact 128x32 DMD title checkpoints for the Jurassic Park 5.13 ROM.

The Data East service menus are painted on the DMD, so the harness has no segment text to wait on.
This bounded adapter fingerprints one text line of a frame: the first group of non-empty rows (or, for
the T-Rex test, the first group inside a named region) is cropped to its own bounding box and hashed
as a bitmap. That ignores the row a title is drawn on and everything below it, so a title still
matches while its detail lines change. The templates were taken from the retained exploratory run
``explore2`` (fresh state, trough 9-14 and T-Rex 36/57 closed) and then visually read; an unknown
frame returns empty text and the ordinary harness times out.
"""
from __future__ import annotations

import hashlib
import sys

import run_pinmame_harness as harness

WIDTH, HEIGHT = 128, 32
# title -> (region x0, y0, x1, y1 or None for the whole frame, SHA-256 of the cropped bitmap)
TEMPLATES = {
    'DIAGNOSTICS': (None, "cf1205c880ccda02ed8960307dd8378d0d8595dae49b39396bf4acd76ec7b6ea"),
    'SERVICE CALL': (None, "21514a2ec37b24b85c093ed652f7d0c84a48554343cdb1dc4da3bc804845eda2"),
    'SERVICE CREDITS': (None, "49105f4ad8c9ba619e3f6557f6ef869127e44df3d0c4d792459978b8da6fc2f1"),
    'PLAYFIELD STATUS': (None, "10f5a62b6b39f004b436cd0e2a01aeebb209bfb6c3bf1cac2c7463514064e685"),
    'EASY TROUGH CLEAR': (None, "a346bc1dbbbd5726ab8da8b50600d329a3af8ebdb0347bbe2c00c9aa2360059f"),
    'BURN IN TIME': (None, "c9b070b143ec6181dd606958d618900c8a5741ddca8fb7ea261593b66e4b986c"),
    'SPEAKER TEST': (None, "e845b3e6337dce1a318534452580512808c78869faf1e97b44f1328d149162fb"),
    'T-REX TEST': ((76, 0, 128, 16), "4c316a8e28f13acca7e4edfdb34412fb33f36af5b12d9db05def841648552bac"),
    'LASER KICK TEST': (None, "8fdc9018e4f1e4ee4dcbd4e34c5ef9253c7ebf3bf44ca8d2ef2a0413116266c4"),
    'SWITCH TEST': (None, "0322e1e6b48615e6e3399dcec1a1289e36dedb3f1feafab531b487d66658583f"),
    'ACTIVE SWITCH TEST': (None, "3d0ead1e667f6078bde8bf405d0686bc0855f2548a443e1df7c7be90cfefe94d"),
    'ALL LAMPS ON': (None, "33481f4fe9a13af101747f97ee7a4cab214ab078eeb72568da82e254e447e2c6"),
    'ROW LAMPS ON': (None, "3c8a3558b0ef1bcbd47702272abcb7a90c000666f5e952060deeed914050d001"),
    'COLUMN LAMPS ON': (None, "71975dd6b68a182c57b6bab7304551239ec981e20b7d5a982709987d5ea0d7ec"),
    'LAMP TEST': (None, "66078d5772d87e9b4fe3ce10085d2ea9c26e0e4b511603ab35dee45b23364564"),
    'CYCLING FLASHERS': (None, "b1b05c8385d3002404ce5ef0f540d21bf447b4844c247447d3e9ab7f52ec5196"),
    'CYCLING COILS': (None, "bfb5450570882084b4622b7a87d782329cf345ac9168054049959244ad31a3d8"),
    'COIL TEST': (None, "fd4de7d82f387cbf1345223e209b3d5f45a9864925ba46907006bb168a10449b"),
    'DISPLAY VERSION': (None, "6ecbbfcd06381a0baf2449845e237e4f2117e9bc62e6a0e9dbaca2c4ef9128fb"),
}


def line_signature(frame: bytes | list[int], region: tuple[int, int, int, int] | None = None) -> str:
    x0, y0, x1, y1 = region or (0, 0, WIDTH, HEIGHT)
    rows = [any(frame[y * WIDTH + x] for x in range(x0, x1)) for y in range(y0, y1)]
    first = next((y for y, lit in enumerate(rows) if lit), None)
    if first is None:
        return ""
    last = first
    while last + 1 < len(rows) and rows[last + 1]:
        last += 1
    ys = range(y0 + first, y0 + last + 1)
    columns = [x for x in range(x0, x1) if any(frame[y * WIDTH + x] for y in ys)]
    left, right = columns[0], columns[-1]
    bits = "".join("1" if frame[y * WIDTH + x] else "0" for y in ys for x in range(left, right + 1))
    return hashlib.sha256(f"{right - left + 1}x{len(ys)}:{bits}".encode()).hexdigest()


def match_title(frame: bytes | list[int], width: int, height: int) -> str:
    if (width, height) != (WIDTH, HEIGHT) or len(frame) != WIDTH * HEIGHT:
        return ""
    return next((title for title, (region, digest) in TEMPLATES.items()
                 if line_signature(frame, region) == digest), "")


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        matches = [
            match_title(frame, layout.get("width", 0), layout.get("height", 0))
            for index, frame in recorder.display_frames.items()
            if ((layout := recorder.display_layouts.get(index, {})).get("type", -1) & 31) == 14
        ]
    return " ".join(title for title in matches if title)


def main() -> int:
    args = harness.build_parser().parse_args()
    if args.game != "jupk_513":
        raise ValueError("Title templates are only verified for jupk_513")
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    sys.exit(main())
