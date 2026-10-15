# Pinned PinMAME Seawitch contract

Revision 97aa922bf8e4b6970126192ec1ac1fb0305a4f62. Emulator facts, not physical fitment. Exact source regions:

## src/wpc/stgames.c:12-23

```c
static core_tLCDLayout dispst7[] = {
  {0, 0, 1,7,CORE_SEG87F},{0,16, 9,7,CORE_SEG87F},
  {2, 0,17,7,CORE_SEG87F},{2,16,25,7,CORE_SEG87F},
  {4, 4,35,2,CORE_SEG7}, {4,10,38,2,CORE_SEG7},{0}
};

BY35_INPUT_PORTS_START(st,1) BY35_INPUT_PORTS_END

#define INITGAME(name, gen, disp, flip, lamps, sb, db) \
static core_tGameData name##GameData = {gen,disp,{flip,0,lamps,0,sb,db}}; \
static void init_##name(void) { core_gameData = &name##GameData; }

```

## src/wpc/stgames.c:703-774

```c
INITGAME(seawitch,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitch,"cpu_u1.716",CRC(c214140b) SHA1(4d68ddd3b0f051c5f601ea5b9d5d5195d6017304),
                            "cpu_u5.716",CRC(ab2eab3a) SHA1(80a8c1ccd554be279720a26466bd6c59e1e56df0),
                            "cpu_u2.716",CRC(b8844174) SHA1(6e01321196fd6fce7b5526efc402044c87fe96a6),
                            "cpu_u6.716",CRC(6c296d8f) SHA1(8cdb77f382ef1214ef45579213cf8f19141366ad))
BY35_ROMEND
#define input_ports_seawitch input_ports_st
CORE_GAMEDEFNV(seawitch,"Seawitch",1980,"Stern",by35_mST200,0)

INITGAME(seawitfp,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitfp,"fpsw_u1.716",CRC(058aa5d4) SHA1(a6aafbcb7c720f1c02ee98a170d2985eda58076c),
                            "fpsw_u5.716",CRC(d3072929) SHA1(6dcc2fdc334d3f3f39355570346406d6eea3ca89),
                            "cpu_u2.716", CRC(b8844174) SHA1(6e01321196fd6fce7b5526efc402044c87fe96a6),
                            "cpu_u6.716", CRC(6c296d8f) SHA1(8cdb77f382ef1214ef45579213cf8f19141366ad))
BY35_ROMEND
#define input_ports_seawitfp input_ports_st
CORE_CLONEDEFNV(seawitfp,seawitch,"Seawitch (Free Play)",1980,"Stern",by35_mST200,0)

INITGAME(seawitcha,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitcha,"seawitch_05-u1.716",CRC(4b4d9927) SHA1(e31f297a83a96af964b713fe944c7c40ef10dcdf),
                             "seawitch_05-u5.716",CRC(afc10bfe) SHA1(a58c8a4e00272d54dfcb9cb815a816b46a16ee25),
                             "seawitch_05-u2.716",CRC(d85701af) SHA1(86314f0c348de7f75802eb844c6cde9aa32c93e6),
                             "seawitch_05-u6.716",CRC(51644c70) SHA1(916dd5df4ba506afd1d0fad9c52345110072633a))
BY35_ROMEND
#define input_ports_seawitcha input_ports_st
CORE_CLONEDEFNV(seawitcha,seawitch,"Seawitch (MOD rev. 5)",2021,"Stern / Idleman",by35_mST200,0)

INITGAME(seawitchb,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitchb,"seawitch_V06-u1.716",CRC(394b14ae) SHA1(754c463922d6b5385397ed54b21730e31d156d9a),
                             "seawitch_V06-u5.716",CRC(9684dcda) SHA1(74ae76101b84e29e4776f398bc70c9d579357932),
                             "seawitch_V06-u2.716",CRC(1cfabb92) SHA1(a5122abec43d3e7df916e516ca26b0fd788d9ba9),
                             "seawitch_V06-u6.716",CRC(9c1bc88d) SHA1(27de8f3c5295a362d544bb5c992d99451b1ef0a4))
BY35_ROMEND
#define input_ports_seawitchb input_ports_st
CORE_CLONEDEFNV(seawitchb,seawitch,"Seawitch (MOD rev. 6)",2021,"Stern / Idleman",by35_mST200,0)

INITGAME(seawitchc,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitchc,"seawitch_V07-u1.716",CRC(0a1c5a87) SHA1(4497beaaeecf9de73c78abce58b5cb5702df208d),
                             "seawitch_V07-u5.716",CRC(16d8f17c) SHA1(6dc677f8db2283f6557539778c0f3c143149734b),
                             "seawitch_V07-u2.716",CRC(c3fd00a0) SHA1(fdf5e2ba040d21793ec2b11f965686441cf998f0),
                             "seawitch_V07-u6.716",CRC(eb1cf81b) SHA1(20114578f4e7fa040d535ccd63f224243495cdfa))
BY35_ROMEND
#define input_ports_seawitchc input_ports_st
CORE_CLONEDEFNV(seawitchc,seawitch,"Seawitch (MOD rev. 7)",2021,"Stern / Idleman",by35_mST200,0)

// New version with spinner counter, standup carryover options, and consecutive loop award option
INITGAME(seawitchd,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitchd,"seawitch_V08-u1.716",CRC(756f8e91) SHA1(3be921799b54525e464a3a92ddef92e116c97038),
                             "seawitch_V08-u5.716",CRC(72ff7b4a) SHA1(34cc77f7971715c0b8ab296d056559fd99150f93),
                             "seawitch_V08-u2.716",CRC(a6dc5885) SHA1(d4866bfdcb87c604c7a47de22745f080ca8fdd63),
                             "seawitch_V08-u6.716",CRC(babb19c4) SHA1(88ed6c2ea0971e73d0f8629653040a0e8e6288a3))
BY35_ROMEND
#define input_ports_seawitchd input_ports_st
CORE_CLONEDEFNV(seawitchd,seawitch,"Seawitch (MOD rev. 8)",2021,"Stern / Idleman",by35_mST200,0)

INITGAME(seawitche,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitche,"seawitch_V09-u1.716",CRC(3f01a1d9) SHA1(12f0f17febe1fad4e570bf82ede821416d79e655),
                             "seawitch_V09-u5.716",CRC(cc4799ee) SHA1(6f4a3929c821d77ebfd706c614669d28728c2746),
                             "seawitch_V09-u2.716",CRC(c300fd13) SHA1(8ca456c0b15a344858afb22af9c9152cc212b3fe),
                             "seawitch_V09-u6.716",CRC(bf9de5c1) SHA1(5d16d4f544d25ffa1b6c20ed0d6acead56301c62))
BY35_ROMEND
#define input_ports_seawitche input_ports_st
CORE_CLONEDEFNV(seawitche,seawitch,"Seawitch (MOD rev. 9)",2023,"Stern / slochar",by35_mST200,0)

INITGAME(seawitchf,GEN_STMPU200,dispst7,FLIP_SW(FLIP_L),0,SNDBRD_ST300,0)
ST200_ROMSTART8888(seawitchf,"seawitch_V093-u1.716",CRC(a47fe686) SHA1(b65a474e6c6679a336bc71db7cb5a69e0cee5a73),
                             "seawitch_V093-u5.716",CRC(c5a04e0a) SHA1(67650e32e2871df87354046e5808874100838db6),
                             "seawitch_V093-u2.716",CRC(9900103e) SHA1(39f35d7bd726a2a90cd75bfa72e14d3eff6ff67f),
                             "seawitch_V093-u6.716",CRC(a73000e6) SHA1(f050f8083e90552424923d9033376cce9f545b8e))
BY35_ROMEND
#define input_ports_seawitchf input_ports_st
CORE_CLONEDEFNV(seawitchf,seawitch,"Seawitch (MOD rev. 9.3)",2024,"Stern / slochar",by35_mST200,0)
```

## src/wpc/by35.c:132-146

```c
static void by35_lampStrobe(int board, int lampadr) {
  if (lampadr != 0x0f) {
    int lampdata = (locals.a0>>4)^0x0f;
#ifdef LISY_SUPPORT
    if ( lampdata ) lisy35_lamp_handler( 0, board, lampadr, lampdata);
#endif
    volatile UINT8 *matrix = &coreGlobals.tmpLampMatrix[(lampadr>>3)+8*board];
    int bit = 1<<(lampadr & 0x07);

    while (lampdata) {
      if (lampdata & 0x01) *matrix |= bit;
      lampdata >>= 1; matrix += 2;
    }
  }
}
```

## src/wpc/by35.c:220-247

```c
static READ_HANDLER(pia0b_r) {
#ifndef LISY_SUPPORT
  if (locals.a0 & 0x20) return core_getDip(0); // DIP#1 1-8
  if (locals.a0 & 0x40) return core_getDip(1); // DIP#2 9-16
  if (locals.a0 & 0x80) return core_getDip(2); // DIP#3 17-24
  if ((locals.hw & BY35HW_DIP4) && locals.cb20) return core_getDip(3); // DIP#4 25-32
#else
  int ret;
  if (locals.a0 & 0x20)
   {  ret = lisy35_get_mpudips(0); if (ret<0) return core_getDip(0); else return ret; } // DIP#1 1-8
  if (locals.a0 & 0x40)
   {  ret = lisy35_get_mpudips(1); if (ret<0) return core_getDip(1); else return ret; } // DIP#1 9-16
  if (locals.a0 & 0x80)
   {  ret = lisy35_get_mpudips(2); if (ret<0) return core_getDip(2); else return ret; } // DIP#1 17-24
  if ((locals.hw & BY35HW_DIP4) && locals.cb20)
   {  ret = lisy35_get_mpudips(3); if (ret<0) return core_getDip(3); else return ret; } // DIP#1 25-32
#endif
  {
    int col = locals.a0 & 0x1f;
    UINT8 sw;
    if (core_gameData->hw.gameSpecific1 & BY35GD_SWVECTOR) col |= (locals.b1 & 0x10)<<1;
    else                                                   col |= (locals.b1 & 0x80)>>2;
    if (!col && (core_gameData->hw.gameSpecific1 & BY35GD_MARAUDER)) {
      sw = coreGlobals.swMatrix[3];
    } else {
      sw = core_getSwCol(col);
    }
    return (locals.hw & BY35HW_REVSW) ? core_revbyte(sw) : sw;
```

## src/wpc/by35.c:319-329

```c
  }
  coreGlobals.pulsedSolState = 0;
  if (!locals.cb21) {
    locals.solenoids |= coreGlobals.pulsedSolState = (1<<(data & 0x0f)) & 0x7fff;
  } else if (core_gameData->hw.gameSpecific1 & BY35GD_MARAUDER) {
    coreGlobals.pulsedSolState = (1<<(data & 0x0f)) & 0x7fff;
  }
  data ^= 0xf0;
  coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0xfff0ffff) | ((data & 0xf0)<<12);
  locals.solenoids |= (data & 0xf0)<<12;
}
```

## src/wpc/by35.c:445-457

```c
  cpu_set_nmi_line(0, core_getSw(BY35_SWCPUDIAG) ? ASSERT_LINE : CLEAR_LINE);
#else
  cpu_set_nmi_line(0, lisy35_get_SW_S33() ? ASSERT_LINE : CLEAR_LINE);
#endif
  sndbrd_0_diag(core_getSw(BY35_SWSOUNDDIAG));
  /*-- coin door switches --*/
#ifndef LISY_SUPPORT
  pia_set_input_ca1(BY35_PIA0, !core_getSw(BY35_SWSELFTEST));
#else
  pia_set_input_ca1(BY35_PIA0, !lisy35_get_SW_Selftest());
#endif
}

```

## src/wpc/core.c:1818-1832

```c
    if (FLIP_SWL(flip)) core_setSw(FLIP_SWL(flip), swFlip & CORE_SWLLFLIPBUTBIT);
    if (FLIP_SWR(flip)) core_setSw(FLIP_SWR(flip), swFlip & CORE_SWLRFLIPBUTBIT);
#ifdef PROC_SUPPORT
  }
#endif

  /*-- fake solenoids if not CPU controlled --*/
  if ((flip & FLIP_SOL(FLIP_L)) == 0) {
    coreGlobals.solenoids2 &= 0xffffff00;
    if (flipEn) {
      if (swFlip & CORE_SWLLFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LLFLIPSOLBITS;
      if (swFlip & CORE_SWLRFLIPBUTBIT) coreGlobals.solenoids2 |= CORE_LRFLIPSOLBITS;
    }
  }

```

## src/wpc/core.h:297-322

```c
/* 11    Tilt (for GI) (fake)            */
#define CORE_FIRSTEXTSOL   37
#define CORE_FIRSTUFLIPSOL 33
#define CORE_FIRSTCUSTSOL  51
#define CORE_FIRSTLFLIPSOL 45
#define CORE_FIRSTSIMSOL   49
#define CORE_MAXSOL        64

#define CORE_SSFLIPENSOL  23
#define CORE_FIRSTSSSOL   17

#define CORE_SOLBIT(x) (1u<<((x)-1))

/*  Flipper Solenoid numbers */
#define sLRFlip     (CORE_FIRSTLFLIPSOL+1)
#define sLRFlipPow  (CORE_FIRSTLFLIPSOL+0)
#define sLLFlip     (CORE_FIRSTLFLIPSOL+3)
#define sLLFlipPow  (CORE_FIRSTLFLIPSOL+2)
#define sURFlip     (CORE_FIRSTUFLIPSOL+1)
#define sURFlipPow  (CORE_FIRSTUFLIPSOL+0)
#define sULFlip     (CORE_FIRSTUFLIPSOL+3)
#define sULFlipPow  (CORE_FIRSTUFLIPSOL+2)

/*-- Flipper solenoid bits --*/
#define CORE_LRFLIPSOLBITS 0x03
#define CORE_LLFLIPSOLBITS 0x0c
```

## src/wpc/stsnd.c:862-864

```c
const struct sndbrdIntf st300Intf = {
	"ST300", sts_init, NULL, st300_switch_w, st300_man_w, st300_data_w,NULL, st300_ctrl_w, NULL, SNDBRD_NODATASYNC|SNDBRD_NOCTRLSYNC
};
```

## src/wpc/sndbrd.c:69-73

```c
void sndbrd_diag(int board, int button) {
  const struct sndbrdIntf *b = intf[board].brdIntf;
  if (b && (coreGlobals.soundEn || (b->flags & SNDBRD_NOTSOUND)) && b->diag)
    b->diag(button);
}
```

Sequential conversion yields matrix 1-40, service -7 through -5 and lower generic flipper buttons 82/84. CPU row-read can select six strobes, not internal flipper column 11; upper 81/83 cannot reach the CPU and FLIP_SW(FLIP_L) declares no independent upper output. Synthetic 45/46 and 47/48 rise together for an enabled lower-button closure. In sndbrdIntf the fourth field is diag: ST300 installs st300_switch_w, which writes voiceSw for the next st300_ctrl_w. Thus -5 is a meaningful virtual route; the NULL third field is exit, not diag. Callback 6 is a DMD-style rendering of segment displays, not a seventh physical display.

## Diagnostic handler field and ST300 voice selection

### sndbrd.h:45-58

```c
struct sndbrdIntf {
  const char* typestr;
  void (*init)(struct sndbrdData *brdData);
  void (*exit)(int boardNo);
  void (*diag)(int buttons);
  WRITE_HANDLER((*manCmd_w));
  WRITE_HANDLER((*data_w));
   READ_HANDLER((*data_r));
  WRITE_HANDLER((*ctrl_w));
   READ_HANDLER((*ctrl_r));
  UINT32 flags;
};

#define SNDBRD_NODATASYNC 0x0001 // Don't use cpu sync'ed data writes
```

### stsnd.c:654-658

```c
static WRITE_HANDLER(st300_ctrl_w) {
	if (!st300loc.voiceSw) {
//	cycles for 4536
//	c0 -> 00 -> 2 clock cycles
//	c0 -> 10 -> 4 clock cycles
```

### stsnd.c:840-864

```c
static void st300_switch_w(int sw) {
	st300loc.voiceSw = sw;
}

static WRITE_HANDLER(st300_man_w) {
	st300loc.voiceSw = 1;
	st300_ctrl_w(0, data);
}

static void sts_init(struct sndbrdData *brdData)
{
	memset(&sts_locals, 0x00, sizeof(sts_locals));
	sts_locals.brdData = *brdData;
}

/*-------------------
/ exported interfaces
/--------------------*/
const struct sndbrdIntf st100Intf = {
	"ST100", sts_init, NULL, NULL, sts_data_w, sts_data_w, NULL, sts_ctrl_w, NULL, SNDBRD_NODATASYNC|SNDBRD_NOCTRLSYNC
};

const struct sndbrdIntf st300Intf = {
	"ST300", sts_init, NULL, st300_switch_w, st300_man_w, st300_data_w,NULL, st300_ctrl_w, NULL, SNDBRD_NODATASYNC|SNDBRD_NOCTRLSYNC
};
```
