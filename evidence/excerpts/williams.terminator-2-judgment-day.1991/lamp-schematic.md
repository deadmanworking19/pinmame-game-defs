# Terminator 2: Judgment Day - lamp matrix schematic connector labels

Source: `Terminator 2 Judgement Day Operations Manual.pdf` (ARC ARC retained source SHA-256 `8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b`), PDF page 100, printed page 2-34, the lamp matrix schematic drawn above the repeated "Lamp Matrix" table. Transcribed manually from the image-only scan and checked against a native-resolution render of the page.

The drawing labels a column connector `J137` and a row connector `J133`, each with pins numbered 1 to 8:

| Drawn connector pin | Printed wire | Printed function |
| --- | --- | --- |
| J137 pin 1 | YEL-BRN | Column 1 |
| J137 pin 2 | YEL-RED | Column 2 |
| J137 pin 3 | YEL-ORN | Column 3 |
| J137 pin 4 | YEL-BLK | Column 4 |
| J137 pin 5 | YEL-GRN | Column 5 |
| J137 pin 6 | YEL-BLU | Column 6 |
| J137 pin 7 | YEL-VIO | Column 7 |
| J137 pin 8 | YEL-GRY | Column 8 |
| J133 pin 1 | RED-BRN | Row 1 |
| J133 pin 2 | RED-BLK | Row 2 |
| J133 pin 3 | RED-ORN | Row 3 |
| J133 pin 4 | RED-YEL | Row 4 |
| J133 pin 5 | RED-GRN | Row 5 |
| J133 pin 6 | RED-BLU | Row 6 |
| J133 pin 7 | RED-VIO | Row 7 |
| J133 pin 8 | RED-GRY | Row 8 |

The grid crossings are numbered 11 to 88, column digit first, and carry no lamp names.

The lamp matrix table on printed page 1-33 (PDF page 53, see [lamp-matrix.md](lamp-matrix.md)) and its copy on PDF page 117 print the same eight column and eight row wire colours and the same addresses, but different connector labels: columns on J138-1 to J138-7 and J138-9, rows on J133-1, J133-2 and J133-4 to J133-9. The copy printed below this drawing on page 2-34 repeats those row labels and wire colours (row 5 reads Red-Green, J133-6, Q86 there too) and columns J138-1 to J138-7; its column 8 pin digit is filled in by the scan, has the same shape as the 9 on page 1-33, and cannot be read with certainty. The drawing's J137 column connector and its consecutive J133 pins 3 to 8 therefore disagree with the table. The lamp-circuit example drawn below the table on printed page 1-33 also routes its column through J137 and its row through J133. Both readings are kept literally here and in the lamp-matrix excerpt. Because both pages put every lamp at the same address with the same wires, the definition treats this as a wiring detail rather than a blocking conflict.
