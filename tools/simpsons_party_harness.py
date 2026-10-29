"""Run Simpsons Pinball Party lamp diagnostics with exact DMD title checkpoints.

The templates contain only visually read title bands from retained exploratory
frames. Unknown screens return no text and make navigation fail closed.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads(Path(__file__).with_name("simpsons_party_header_templates.json").read_text(encoding="utf-8"))


def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
    if (width, height) != (128, 32) or len(frame) != width * height:
        return []
    matches = []
    for title, template in TEMPLATES.items():
        first, last = template["rows"]
        left, right = template["cols"]
        band = bytes(bool(frame[y * width + x]) for y in range(first, last + 1) for x in range(left, right + 1))
        if band == base64.b64decode(template["mask"]):
            matches.append(title)
    return matches


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        return " ".join(
            title
            for index, frame in recorder.display_frames.items()
            if ((layout := recorder.display_layouts.get(index, {})).get("type", -1) & 31) == 14
            for title in match_titles(frame, layout.get("width", 0), layout.get("height", 0))
        )


def main() -> int:
    args = harness.build_parser().parse_args()
    if args.game != "simpprty":
        raise ValueError("DMD checkpoints are verified only for simpprty 5.00 English")
    if args.scenario:
        scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
        for action in scenario["actions"]:
            if action["type"] == "pulse_until_display":
                for target in action["texts"]:
                    if target not in TEMPLATES or any(target in other for other in TEMPLATES if other != target):
                        raise ValueError(f"unverified or ambiguous DMD target: {target}")
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    sys.exit(main())
