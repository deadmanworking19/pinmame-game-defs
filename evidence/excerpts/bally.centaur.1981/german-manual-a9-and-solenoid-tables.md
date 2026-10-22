# Centaur — German manual: A9 troubleshooting table, solenoid table and module list

Transcribed from `Bally_1981_Centaur_German_Manual.pdf`, the German edition published by the
distributor Wulff-Automaten GmbH, Hannover (`Nachdruck verboten`). PDF page 42 (printed 42) carries
the two tables below; PDF page 39 carries the module list. The pages are typed tables, not Bally
drawings, so they are transcribed without a crop.

## FEHLERSUCHTABELLE AUXILIARY LAMP DRIVER MODUL A9 (page 42)

| Thyristor Nr. | Stecker Nr./Kontakt Nr. | Dazugehörige Lampe |
| --- | --- | --- |
| Q1 | J2-1 | Obere mittlere Kugelbahn |
| Q2 | J2-2 | Linker Slingshot |
| Q4 | J2-5 | 1. Lampe Chamberbeleuchtung |
| Q3 | J2-3 | 2. Lampe Chamberbeleuchtung |
| Q10 | J2-20 | 3. Lampe Chamberbeleuchtung |
| Q9 | J2-17 | 4. Lampe Chamberbeleuchtung |
| Q5 | J2-6 | Rechter Slingshot |
| Q6 | J2-7 | Obere mittlere Kugelbahn |
| Q12 | J2-18 | Obere rechte Kugelbahn |
| Q11 | J2-19 | Rechter Schlagturm |
| Q8 | J2-12 | Linker Schlagturm |

Eleven rows. There is no row for `Q7` or `J2-11`. The `Q6 J2-7` row repeats "Obere mittlere
Kugelbahn" (upper middle lane) where the English sheet prints TOP LEFT LANE, so this table is a
retyped copy with its own errors, not an independent check of the lane labels.

## SPULENIDENTIFIZIERUNGSTABELLE (page 42)

| Selbsttest Nr. | Kontaktbezeichnung | Transistor Nr. | Stecker Nr./Kontakt Nr. |
| --- | --- | --- | --- |
| 01 | Startloch | Q4 | J3-4 |
| 02 | Klopfspule | Q3 | J2-5 |
| 03 | Linke Target-Rücksetzspule | Q8 | J5-10 |
| 04 | Rechte Target-Rücksetzspule | Q13 | J5-12 |
| 05 | Linker Schlagturm | Q14 | J5-11 |
| 06 | Rechter Schlagturm | Q9 | J5-9 |
| 07 | Linker Slingshot | Q10 | J5-15 |
| 08 | Rechter Slingshot | Q12 | J5-13 |
| 09 | ORBS Target Rücksetzspule | Q2 | J2-4 |
| 10 | Rechtes A-Target-Rücksetz-spule | Q1 | J2-9 |
| 11 | Rechtes B-Target-Rücksetz-spule | Q5 | J2-10 |
| 12 | Rechtes C-Target-Rücksetz-spule | Q6 | J2-11 |
| 13 | Rechtes D-Target-Rücksetz-spule | Q7 | J2-12 |
| 14 | Kugelfreigabe | Q16 | J5-8 |
| 15 | Autom. Kugelauswurf | Q11 | J5-14 |
| 16 | Münzsperrspule | Q19 | J2-8 |
| 17 | K1 Relais | Q15 | - |
| 18 | Magnet unter dem Spielfeld | Q18 | J5-3 |

Rows 10 to 13 break their description over two lines at the printed hyphen (`Rücksetz-` / `spule`);
the hyphen is kept. Row 17 prints `-` in the connector column. The English table prints names only;
this table's row 15 is what pairs the ball kick with driver Q11 and connector J5-14.

## Module (page 39)

| module | assembly |
| --- | --- |
| Lamp Driver A5 | AS-2518-23 |
| Display Driver A1 (1) | AS-2518-21 |
| Display Driver A1 (4) | AS-2518-58 |
| Solenoid Driver /Voltage Regulator A3 | AS-2962-29 |
| MPU A4 | AS-2962-29 |
| Transformer & Rectifier A2 | AS-2877-6 |
| Rectifier Board (Part of A2) | AS-2518-54 |
| Squawk & Talk | AS-3107-6 |
| Auxiliary Lamp Driver A9 | AS-2518-52 |
| Aux. Driver (G.I. Flasher) | AS-2518-68 |
| Solenoid Expander | AS-2518-66 |

The list names the AS-2518-52 for A9 where the English parts list names the AS-2518-43, and it gives
the MPU the solenoid driver's assembly number, so its part numbers are not reliable on their own.
