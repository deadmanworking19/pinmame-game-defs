"""Reviewed factory and aftermarket placements for Bally Revenge from Mars (1999).

The factory location drawings are orthographic service diagrams rather than a measured CAD export.
Coordinates are reviewed authoring projections from each callout endpoint into the common
player-view playfield plane: x=0 left, x=1 right, y=0 rear, y=1 apron. Values deliberately retain
three decimal places; extra precision would misrepresent the line-art source. Four optional
myPinballs positions are reviewed projections from the retrofit instructions onto the factory
trough sequence and right-lockup assembly. `validated` means the device identity, side, order,
and usable authoring point reconcile to the retained drawings; it does not claim surveyed CAD.
"""

from __future__ import annotations


SWITCH_POSITIONS = {
	11: (0.900, 0.080), 12: (0.090, 0.055), 15: (0.760, 0.235), 16: (0.115, 0.785),
	17: (0.795, 0.715), 18: (0.955, 0.905), 25: (0.130, 0.305), 26: (0.210, 0.715),
	27: (0.885, 0.785), 28: (0.590, 0.055), 31: (0.655, 0.200), 32: (0.655, 0.200),
	33: (0.635, 0.385), 34: (0.590, 0.410), 35: (0.545, 0.435), 36: (0.500, 0.460),
	37: (0.310, 0.335), 38: (0.390, 0.470), 41: (0.750, 0.900), 42: (0.660, 0.970),
	43: (0.580, 0.970), 44: (0.500, 0.970), 45: (0.420, 0.970), 46: (0.685, 0.285),
	47: (0.255, 0.330), 51: (0.695, 0.205), 52: (0.165, 0.205), 61: (0.220, 0.675),
	62: (0.780, 0.675), 63: (0.140, 0.145), 64: (0.170, 0.240), 65: (0.190, 0.310),
	67: (0.875, 0.310), 68: (0.865, 0.115), 71: (0.080, 0.500), 72: (0.075, 0.560),
	73: (0.070, 0.620), 74: (0.475, 0.055), 75: (0.285, 0.210), 76: (0.385, 0.070),
	77: (0.300, 0.070), 78: (0.085, 0.120), 85: (0.920, 0.620), 86: (0.915, 0.560),
	87: (0.910, 0.500),
}

AFTERMARKET_SWITCH_POSITIONS = {
	53: (0.340, 0.970),
	54: (0.260, 0.970),
	55: (0.695, 0.185),
	56: (0.695, 0.165),
}

# Keys are printed driver numbers, before PinMAME's public 33-48 remap.
SOLENOID_DRIVER_POSITIONS = {
	1: (0.160, 0.480), 2: (0.840, 0.480), 3: (0.200, 0.290), 4: (0.470, 0.035),
	5: (0.100, 0.040), 6: (0.690, 0.220), 7: (0.690, 0.220), 8: (0.690, 0.290),
	9: (0.660, 0.930), 10: (0.200, 0.680), 11: (0.800, 0.680), 12: (0.130, 0.150),
	13: (0.170, 0.230), 14: (0.180, 0.300), 15: (0.950, 0.920), 16: (0.720, 0.180),
	17: (0.500, 0.430), 22: (0.680, 0.280), 23: (0.230, 0.940), 25: (0.770, 0.940),
	26: (0.080, 0.490), 27: (0.920, 0.490), 28: (0.500, 0.500), 33: (0.650, 0.820),
	34: (0.650, 0.820), 35: (0.350, 0.820), 36: (0.350, 0.820), 37: (0.590, 0.120),
	38: (0.590, 0.120), 39: (0.380, 0.380), 40: (0.380, 0.380),
}

# Keys are PinMAME public lamp numbers 1-128: the manual cell's matrix bit index plus one.
LAMP_POSITIONS = {
	5: (0.390, 0.055), 6: (0.300, 0.055), 7: (0.340, 0.300), 8: (0.500, 0.390),
	9: (0.430, 0.700), 10: (0.440, 0.750), 11: (0.470, 0.690), 12: (0.500, 0.750),
	13: (0.550, 0.690), 14: (0.560, 0.750), 15: (0.590, 0.700), 16: (0.220, 0.730),
	21: (0.550, 0.580), 22: (0.450, 0.580), 23: (0.270, 0.690), 24: (0.170, 0.700),
	25: (0.620, 0.690), 26: (0.570, 0.670), 27: (0.574, 0.620), 28: (0.500, 0.620),
	29: (0.440, 0.620), 30: (0.430, 0.670), 31: (0.500, 0.650), 32: (0.780, 0.730),
	37: (0.380, 0.900), 38: (0.620, 0.900), 39: (0.730, 0.690), 40: (0.830, 0.700),
	41: (0.660, 0.700), 42: (0.620, 0.660), 43: (0.680, 0.580), 44: (0.640, 0.580),
	45: (0.600, 0.580), 46: (0.560, 0.580), 47: (0.520, 0.580), 49: (0.690, 0.340),
	50: (0.360, 0.620), 51: (0.460, 0.450), 52: (0.490, 0.410), 53: (0.130, 0.360),
	54: (0.500, 0.490), 55: (0.790, 0.510), 56: (0.800, 0.560), 57: (0.390, 0.690),
	58: (0.340, 0.700), 59: (0.400, 0.660), 60: (0.360, 0.580), 61: (0.400, 0.580),
	62: (0.440, 0.580), 63: (0.480, 0.580), 65: (0.500, 0.320), 66: (0.500, 0.360),
	67: (0.500, 0.400), 68: (0.500, 0.440), 69: (0.500, 0.860), 70: (0.500, 0.050),
	71: (0.910, 0.080), 73: (0.780, 0.420), 74: (0.770, 0.460), 75: (0.700, 0.380),
	76: (0.670, 0.420), 77: (0.240, 0.370), 78: (0.340, 0.360), 79: (0.240, 0.420),
	80: (0.340, 0.420), 81: (0.940, 0.170), 82: (0.870, 0.520), 83: (0.870, 0.450),
	84: (0.900, 0.120), 85: (0.850, 0.860), 86: (0.760, 0.830), 87: (0.240, 0.830),
	88: (0.150, 0.860), 89: (0.880, 0.500), 90: (0.880, 0.560), 91: (0.880, 0.620),
	92: (0.120, 0.500), 93: (0.120, 0.560), 94: (0.120, 0.620), 95: (0.750, 0.690),
	96: (0.250, 0.690), 97: (0.035, 0.650), 98: (0.035, 0.590), 99: (0.035, 0.530),
	100: (0.035, 0.470), 101: (0.130, 0.420), 102: (0.110, 0.360), 103: (0.180, 0.270),
	104: (0.050, 0.070), 105: (0.180, 0.290), 107: (0.140, 0.160), 108: (0.220, 0.060),
	109: (0.350, 0.060), 110: (0.480, 0.060), 111: (0.520, 0.025), 112: (0.910, 0.040),
	113: (0.820, 0.730), 114: (0.780, 0.680), 115: (0.810, 0.650), 116: (0.750, 0.650),
	117: (0.280, 0.650), 118: (0.220, 0.650), 119: (0.220, 0.680), 120: (0.180, 0.730),
	121: (0.940, 0.760), 122: (0.940, 0.700), 123: (0.940, 0.640), 124: (0.940, 0.580),
	125: (0.940, 0.520), 126: (0.940, 0.460), 127: (0.940, 0.400), 128: (0.940, 0.340),
}


def _located(device: dict[str, object], role: str, position: tuple[float, float], source_refs: list[str], status: str = "validated") -> None:
	x, y = position
	device["spatial"] = {
		"status": status,
		"placements": [{
			"id": f"{device['id']}.{role}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": {"status": status, "source_refs": source_refs},
		}],
	}


def apply_spatial(inputs: list[dict[str, object]], outputs: list[dict[str, object]], manual_source: str, aftermarket_source: str) -> None:
	"""Apply a reviewed disposition to every factory and optional RFM device."""
	for device in inputs:
		address = int(device["binding"]["device"])
		if address in SWITCH_POSITIONS:
			_located(device, "sensor", SWITCH_POSITIONS[address], [manual_source])
			if address in {31, 32}:
				physical = device.setdefault("physical", {})
				physical["notes"] = f"{physical.get('notes', '')} The switch-location drawing prints address 31 twice: once as a top callout and again beside 32 at the center-loop assembly. Addresses 31 and 32 use one shared reviewed assembly point because the paired right-margin callout does not provide surveyable separation.".strip()
		elif address in AFTERMARKET_SWITCH_POSITIONS:
			_located(device, "sensor", AFTERMARKET_SWITCH_POSITIONS[address], [manual_source, aftermarket_source])
			if address in {53, 54}:
				physical = device.setdefault("physical", {})
				physical["notes"] = f"{physical.get('notes', '')} Optional myPinballs six-ball trough opto. Position continues the factory trough's evenly spaced Ball 1-4 sequence and is a reviewed authoring projection from the v2.0 installation photograph, not a surveyed coordinate.".strip()
			else:
				physical = device.setdefault("physical", {})
				physical["notes"] = f"{physical.get('notes', '')} Optional myPinballs physical-lock opto installed in the production weldment's omitted mounting position. Position is a reviewed intra-assembly authoring projection from the v2.0 installation photograph, not a surveyed coordinate.".strip()
		elif "spatial" not in device:
			raise ValueError(f"RFM input {address} has no reviewed spatial disposition")

	for device in outputs:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.output.solenoid":
			manual_alias = next(alias["value"] for alias in device["aliases"] if alias["namespace"] == "manual.address")
			driver = int(manual_alias)
			if driver in SOLENOID_DRIVER_POSITIONS:
				role = "emitter" if device["kind"] == "flasher" else "effect"
				_located(device, role, SOLENOID_DRIVER_POSITIONS[driver], [manual_source])
			elif "spatial" not in device:
				raise ValueError(f"RFM solenoid driver {driver} / public {address} has no reviewed spatial disposition")
		elif group == "pinmame.output.lamp":
			if address in LAMP_POSITIONS:
				_located(device, "emitter", LAMP_POSITIONS[address], [manual_source])
				if address in {16, 32}:
					device.setdefault("physical", {})["notes"] += " The semantic label follows the runtime lamp test, while this reviewed coordinate follows the manual drawing's physical address: 18B is drawn at the left slingshot and 28B at the right."
			elif "spatial" not in device:
				raise ValueError(f"RFM lamp {address} has no reviewed spatial disposition")
