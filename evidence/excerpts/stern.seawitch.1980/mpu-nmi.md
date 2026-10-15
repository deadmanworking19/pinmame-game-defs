# Seawitch MPU on-board S33 and service routes

Source: schematics PDF page 1, Stern MPU-200 circuit. S33 is drawn as a normally-open pushbutton to ground on the line to U9 6800 pin 6 (NMI), pulled up through R13 (1.2K) to +5 V. The on-board pushbutton therefore supplies the NMI represented by PinMAME CPU Diagnostic, public -6. The same page separately labels J3-5 EXT. BOOKKEEPING RESET. Cabinet page 7 draws the remote S33 MEMORY CLEAR contact on that pin. The two names do not justify silently joining the two drawn paths into one switch-matrix address.

Manual Figure 1 (PDF page 4) labels S33 MEMORY CLEAR at both the MPU and front door, with SELF TEST separately at the door. The physical remote contact is retained with a profile-local identity and no PinMAME transport; the public NMI route identifies the on-board button. No host-readback or firmware clear-memory outcome is claimed.
