# Champion Pub disables the simulator manual shooter

Literal source regions from pinned PinMAME revision
`8371478a7640f1896dcdf565aed340dc5df989ba`.

`src/wpc/sims/wpc/prelim/cp.c` defines launch as public solenoid 1:

```c
#define sLaunch		1
```

The Shooter state uses that launch coil:

```c
  {"Shooter",		1,swShooter,	 sLaunch,	stBallLane,	0,	0,	0,	SIM_STNOTEXCL|SIM_STSHOOT},
```

The complete game simulator configuration disables manual shooter simulation:

```c
static sim_tSimData cpSimData = {
  2,    				/* 2 game specific input ports */
  cp_stateDef,				/* Definition of all states */
  cp_inportData,			/* Keyboard Entries */
  { stTrough1, stTrough2, stTrough3, stTrough4, stDrain, stDrain, stDrain },	/*Position where balls start.. Max 7 Balls Allowed*/
  NULL, 				/* no init */
  cp_handleBallState,			/*Function to handle ball state changes*/
  cp_drawStatic,			/*Function to handle mechanical state changes*/
  FALSE, 				/* Simulate manual shooter? */
  NULL  				/* Custom key conditions? */
};
```

`src/wpc/sim.c` changes shooter release state only inside the manual-shooter branch:

```c
  if (simData->manShooter) {
    /*--  ball shooter --*/
    if (inports[CORE_SIMINPORT] & SIM_SHOOTERKEY) {
      locals.shooterSpeed += 1;
      if (locals.shooterSpeed > 50)
        locals.shooterSpeed = 50;
    }
    else if (locals.shooterSpeed > 0) {
      /*-- Shooters been released --*/
      if (locals.shooterRel == 1) locals.shooterSpeed = 0;
      if (locals.shooterRel > 0)  locals.shooterRel -= 1;
      else                        locals.shooterRel = SIM_SHOOTRELTIME;
    }
  }
```

Its complete simulated-output reader is:

```c
int sim_getSol(int solNo) {
  if (solNo == sShooterRel)
    return locals.shooterRel > 0;
  return 0;
}
```

`sShooterRel` is the first simulated solenoid, public 49 (the pinned `sim.h`
and `core.h` constants). For Champion Pub's disabled manual shooter, that
release state remains zero. The physical launch is solenoid 1, and public 49
is an unused virtual output rather than another actuator or a used launch state.
