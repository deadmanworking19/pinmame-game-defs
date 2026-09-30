"""Run the standard harness with explicitly synthetic Champion Pub feedback.

The angular windows reproduce the retained mfuegemann 1.2 table script. They
are a host model for probing the ROM, not measurements of the physical cams.
Every feedback write is named separately from emulator output observations.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import run_pinmame_harness as harness


# Exact 5x7 glyphs visually checked in cp_16's MAIN MENU and TEST MENU
# frames. Only service-menu cells are read; unknown glyphs remain unknown.
# Period attributes occupy the padding column and are not part of these
# checkpoint phrases. This is a narrow checkpoint reader, not general OCR.
MENU_GLYPHS = {
	"M": (17, 27, 21, 21, 17, 17, 17), "A": (14, 17, 17, 31, 17, 17, 17),
	"I": (14, 4, 4, 4, 4, 4, 14), "N": (17, 17, 25, 21, 19, 17, 17),
	" ": (0, 0, 0, 0, 0, 0, 0), "E": (31, 16, 16, 30, 16, 16, 31),
	"U": (17, 17, 17, 17, 17, 17, 14), "B": (30, 17, 17, 30, 17, 17, 30),
	"O": (14, 17, 17, 17, 17, 17, 14), "K": (17, 18, 20, 24, 20, 18, 17),
	"P": (30, 17, 17, 30, 16, 16, 16), "G": (14, 17, 16, 16, 19, 17, 15),
	"T": (31, 4, 4, 4, 4, 4, 4), "S": (15, 16, 16, 14, 1, 1, 30),
	"1": (4, 12, 4, 4, 4, 4, 14), "W": (17, 17, 17, 21, 21, 27, 17),
	"C": (15, 16, 16, 16, 16, 16, 15), "H": (17, 17, 17, 31, 17, 17, 17),
	"D": (30, 17, 17, 17, 17, 17, 30),
}


def dmd_checkpoints(pixels: bytes | list[int], width: int, height: int) -> str:
	if (width, height) != (128, 32) or len(pixels) != width * height:
		return ""
	lookup = {pattern: character for character, pattern in MENU_GLYPHS.items()}
	def line(x: int, y: int, pitch: int) -> str:
		characters = []
		for origin in range(x, width - 4, pitch):
			pattern = tuple(sum(1 << (4 - column) for column in range(5)
				if pixels[(y + row) * width + origin + column]) for row in range(7))
			characters.append(lookup.get(pattern, "?"))
		return " ".join("".join(characters).split())
	top = line(1, 1, 8)
	if top in {"MAIN MENU", "TEST MENU"}:
		return f"{top} {line(1, 12, 8)}".strip()
	if line(45, 1, 6) == "SWITCH EDGES":
		return "DIAGNOSTIC SWITCH EDGES"
	return ""


def boxer_switches(angle: float) -> dict[int, int]:
	angle = (angle + 180) % 360 - 180
	return {
		41: int(abs(angle) > 7),
		46: int(abs(angle) <= 173),
		47: int(angle >= -25 or angle <= -30),
		48: int(angle <= 25 or angle >= 30),
	}


def main() -> int:
	parser = harness.build_parser()
	parser.description = __doc__
	parser.add_argument("--boxer-angle", type=float, default=0)
	parser.add_argument("--boxer-speed", type=float, default=66.666667)
	parser.add_argument("--rope-angle", type=float, default=0)
	parser.add_argument("--rope-speed", type=float, default=72)
	parser.add_argument("--disable-feedback", action="store_true")
	parser.add_argument("--feedback-stop-step", type=int, help="Suspend feedback before the first switch action at this scenario step, allowing independent sensor probes after boot.")
	args = parser.parse_args()
	if args.boxer_speed <= 0 or args.rope_speed <= 0:
		parser.error("model speeds must be positive")
	boxer_angle = args.boxer_angle
	rope_angle = args.rope_angle
	last_poll: float | None = None
	last_outputs: tuple[int, int, int] | None = None
	last_feedback: dict[int, int] = {}
	feedback_suspended = False
	checked_event_index = 0
	original_poll = harness._poll_outputs
	original_display_text = harness.Recorder.current_display_text

	def display_text(recorder) -> str:
		with recorder.lock:
			layout = recorder.display_layouts.get(0, {})
			frame = bytes(recorder.display_frames.get(0, []))
		return dmd_checkpoints(frame, layout.get("width", 0), layout.get("height", 0)) or original_display_text(recorder)

	def poll(library, recorder) -> None:
		nonlocal boxer_angle, rope_angle, last_poll, last_outputs, feedback_suspended, checked_event_index
		original_poll(library, recorder)
		with recorder.lock:
			new_events = recorder.events[checked_event_index:]
			checked_event_index = len(recorder.events)
		if args.feedback_stop_step is not None and not feedback_suspended and any(
			event.get("event") == "switch" and event.get("step", 0) >= args.feedback_stop_step
			for event in new_events
		):
			feedback_suspended = True
			recorder.record("host_mech_feedback_suspended", before_step=args.feedback_stop_step)
		now = time.monotonic()
		delta = 0 if last_poll is None else now - last_poll
		last_poll = now
		outputs = tuple(int(bool(library.PinmameGetSolenoid(address))) for address in (27, 26, 25))
		motor, direction, rope_motor = outputs
		# The previous output state acted during the elapsed interval.
		if last_outputs is not None:
			old_motor, old_direction, old_rope_motor = last_outputs
			if old_motor:
				boxer_angle = (boxer_angle + (1 if old_direction else -1) * args.boxer_speed * delta + 180) % 360 - 180
			if old_rope_motor:
				rope_angle = (rope_angle + args.rope_speed * delta) % 360
		if outputs != last_outputs:
			recorder.record("host_mech_output_edge", boxer_angle=round(boxer_angle, 6), rope_angle=round(rope_angle, 6), motor_27=motor, direction_26=direction, rope_motor_25=rope_motor)
			last_outputs = outputs
		feedback = boxer_switches(boxer_angle)
		feedback[64] = int(rope_angle <= 10 or rope_angle >= 350)
		if not args.disable_feedback and not feedback_suspended:
			for address, state in feedback.items():
				library.PinmameSetSwitch(address, state)
				if last_feedback.get(address) != state:
					recorder.record("host_mech_feedback", number=address, state=state, boxer_angle=round(boxer_angle, 6), rope_angle=round(rope_angle, 6))
					last_feedback[address] = state

	harness._poll_outputs = poll
	harness.Recorder.current_display_text = display_text
	try:
		result = harness.run(args)
	finally:
		harness._poll_outputs = original_poll
		harness.Recorder.current_display_text = original_display_text
	result["host_model"] = {
		"implementation": Path(__file__).name,
		"implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		"pattern": "mfuegemann-1.2-script-angular-windows",
		"boxer_initial_angle": args.boxer_angle,
		"boxer_degrees_per_second": args.boxer_speed,
		"rope_initial_angle": args.rope_angle,
		"rope_degrees_per_second": args.rope_speed,
		"feedback_enabled": not args.disable_feedback,
		"feedback_stop_step": args.feedback_stop_step,
		"dmd_checkpoint_reader": "Visually checked cp_16 5x7 glyphs; exact service-menu cells and Switch Edges title only; unknown glyphs fail to match.",
		"scope": "Synthetic host feedback only; no physical cam dimensions or speeds are measured.",
	}
	serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
	if args.output:
		args.output.parent.mkdir(parents=True, exist_ok=True)
		args.output.write_text(serialized, encoding="utf-8")
	else:
		print(serialized, end="")
	return 1 if result["failure"] else 0


if __name__ == "__main__":
	raise SystemExit(main())
