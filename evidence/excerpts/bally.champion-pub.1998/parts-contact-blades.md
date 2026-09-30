# Factory contact-blade construction

Literal complete assembly subtrees from the retained factory hierarchical parts
list, IPDB 4358. Columns are item, hierarchy level, part number, description and
quantity. The indentation preserves parent-child ownership; quantities belong to
the listed assembly and are not copied to each controller input. This source is
plain text, so no visual PDF review is claimed for these rows.

The Switch Locations tables map lower EOS F1/F3 to SW-1A-194, slingshots 51/52 to
A-17801 with A-17800 (KICK) and A-17794 (SCORE), three-bank targets 25/53/54 to
A-22253-6, and entry contacts 74/78 to A-16443. The subtrees below establish paired
contact blades and insulating or spacer stacks for those exact assemblies.
These component hierarchies support leaf construction; an assembly name alone
would not. The flipper drawing and its longer/shorter blade adjustment instruction
provide independent visual confirmation for SW-1A-194.

## Item 437 complete subtree

```text
437     ..3      SW-1A-194         switch assy-make                                  1
438     ...4     06-1-20           blade-contact                                     1
439     ...4     06-2V-14          blade-contact                                     1
440     ...4     03-7007-4A        tubing-switch                                     2
441     ...4     01-916-L          "spacer-loose 1/16"""                             2
442     ...4     01-916-S          "spacer-tight 1/16"""                             2
443     ...4     5860-09374-00     cp prec met 7309fs                                1
444     ...4     5860-06244-00     cp prec met 7207FSn                               1
```

## Item 484 complete subtree

```text
484     ..3      SW-1A-194         switch assy-make                                  1
485     ...4     06-1-20           blade-contact                                     1
486     ...4     06-2V-14          blade-contact                                     1
487     ...4     03-7007-4A        tubing-switch                                     2
488     ...4     01-916-L          "spacer-loose 1/16"""                             2
489     ...4     01-916-S          "spacer-tight 1/16"""                             2
490     ...4     5860-09374-00     cp prec met 7309fs                                1
491     ...4     5860-06244-00     cp prec met 7207FSn                               1
```

## Item 543 complete subtree

```text
543     .2       A-17801           kicker count sw assy                              2
544     ..3      A-17800           stand up sw assy                                  2
545     ...4     SW-1A-114         switch-kicker                                     2
546     ....5    A-8394            blade & contact assy                              2
547     .....6   06-36-10          blade-contact                                     2
548     .....6   5860-09374-00     cp prec met 7309fs                                2
549     ....5    A-8395            blade & contact assy                              2
550     .....6   06-35-8           blade-contact                                     2
551     .....6   5860-09374-00     cp prec met 7309fs                                2
552     ....5    01-916-H          "spacer- 3/32"""                                  2
553     ....5    01-916-L          "spacer-loose 1/16"""                             4
554     ....5    01-916-T          "spacer- 1/32"""                                  2
555     ....5    01-916-S          "spacer-tight 1/16"""                             4
556     ....5    03-7007-6A        "tubing-13/32"""                                  4
557     ....5    06-20-20          blade-back up                                     2
558     ...4     01-3670           plate-switch curved                               2
559     ...4     01-12345          brkt switch                                       2
560     ...4     07-6688-27        rivet 9/16X1/8                                    4
561     ..3      A-17794           kicker sw sub assy                                2
562     ...4     A-17793           stand up sw assy                                  2
563     ....5    SW-1A-120         switch-score                                      2
564     .....6   A-8394            blade & contact assy                              2
565     ......7  06-36-10          blade-contact                                     2
566     ......7  5860-09374-00     cp prec met 7309fs                                2
567     .....6   A-8395            blade & contact assy                              2
568     ......7  06-35-8           blade-contact                                     2
569     ......7  5860-09374-00     cp prec met 7309fs                                2
570     .....6   01-916-L          "spacer-loose 1/16"""                             2
571     .....6   01-916-Q          "spacer- 1/64"""                                  2
572     .....6   01-916-S          "spacer-tight 1/16"""                             4
573     .....6   01-916-T          "spacer- 1/32"""                                  4
574     .....6   01-916-H          "spacer- 3/32"""                                  2
575     .....6   03-7007-6A        "tubing-13/32"""                                  4
576     .....6   06-17             blade-side lug                                    2
577     .....6   06-20-20          blade-back up                                     2
578     ....5    01-12345          brkt switch                                       2
579     ....5    01-3670           plate-switch curved                               2
580     ....5    07-6688-26        rivet 1/2X1/8                                     4
581     ...4     5070-09054-00     diode-1N4004 1.0a                                 2
582     ..3      CW-30022-5        wire 22awg green                                 10
583     ..3      CW-30022-9        wire 22awg white                                 10
```

## Item 1373 complete subtree

```text
1373    ..3      A-16443           jet bumper switch & diode assy                    2
1374    ...4     SW-11A-37         switch-jet bumper                                 2
1375    ....5    A-8198            blade & contact assy                              2
1376    .....6   06-1-14           blade-contact                                     2
1377    .....6   5860-09374-00     cp prec met 7309fs                                2
1378    ....5    A-8199            blade & contact assy                              2
1379    .....6   06-68D-8          blade-contact                                     2
1380    .....6   5860-09374-00     cp prec met 7309fs                                2
1381    ....5    01-916-Q          "spacer- 1/64"""                                  2
1382    ....5    01-916-H          "spacer- 3/32"""                                  6
1383    ....5    01-916-S          "spacer-tight 1/16"""                             4
1384    ....5    03-7007-7A        "tubing 15/32"" LONG"                             4
1385    ....5    06-17             blade-side lug                                    2
1386    ....5    06-21B-12         blade-contact                                     2
1387    ...4     5070-09054-00     diode-1N4004 1.0a                                 2
```

## Item 1499 complete subtree

```text
1499    ..3      A-22253-6         3 bank standup tgt assy                           1
1500    ...4     01-14805          brkt-3 bank standup tgt                           1
1501    ...4     A-11175           bld & contact assy                                3
1502    ....5    06-1-14           blade-contact                                     3
1503    ....5    5860-09374-00     cp prec met 7309fs                                3
1504    ...4     A-8378            blade & contact assy                              3
1505    ....5    06-13G-14         blade-contact                                     3
1506    ....5    5860-09374-00     cp prec met 7309fs                                3
1507    ...4     01-8657-1         stop-switch limit                                 3
1508    ...4     01-916-H          "spacer- 3/32"""                                  3
1509    ...4     01-916-S          "spacer-tight 1/16"""                             6
1510    ...4     01-916-T          "spacer- 1/32"""                                  3
1511    ...4     01-3670           plate-switch curved                               3
1512    ...4     03-7007-6         "tubing-3/8"""                                    6
1513    ...4     03-8304-6         tgt sq skirt stat-op yellow                       3
1514    ...4     06-20-20          blade-back up                                     6
1515    ...4     06-73-2           blade-insulator                                   3
1516    ...4     07-6688-27        rivet 9/16X1/8                                    6
1517    ...4     07-6697-4         rivet .125X.187x.218 zinc                         3
1518    ...4     4700-00003-00     fw .125X.281X.032                                 3
1519    ...4     5070-09054-00     diode-1N4004 1.0a                                 3
1520    ...4     06-1F-14          blade-contact                                     6
```

The Half Guy rows 55/56 identify A-17795-6 with a dashed switch-part cell.
The game-specific parts list has no exact A-17795-6 subtree. Its blade switch
construction and exact SW-1A-178-6 cross-reference are established separately
by the manufacturer Green Parts Catalog table retained in
green-catalog-target-blades.md. No equivalence to A-18530-6 is assumed.
Switch 77 is NOT USED with dashed assembly and switch cells; no construction
is inferred for that channel.
