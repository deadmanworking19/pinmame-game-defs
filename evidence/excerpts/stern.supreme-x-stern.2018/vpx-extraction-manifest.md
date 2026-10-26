# Retained `supreme_008.vpx` extraction identity

Method: manual inspection of the user-supplied retained VPX and the adjacent
`vpxtool git:v0.33.3` extraction. This is a compact factual excerpt; the
source-owned VPX, extraction, and complete manifest remain external.

- Original: `vpx-sources/stern/supreme-x-stern-2018/supreme_008.vpx`
  (`64,925,696` bytes; SHA-256
  `444c21186425f23c173dece87fe9f683e2ee5c101e76271bf1d2339d1920edd9`).
- Extraction: `vpx-sources/stern/supreme-x-stern-2018/supreme_008/`.
  Its `script.vbs` is `114,094` bytes (SHA-256
  `f2bb8a48bd0aa49310d7e7e8bc165757d59d168110815ac1712dcc971e7a34ca`).
- `tools/build_external_evidence_manifest.py --game supreme_101` created
  `manifest.json` and `manifest.sha256` beside the extraction. Its canonical
  UTF-8 JSON algorithm sorts relative POSIX paths case-sensitively and records
  every included file's `path`, byte `size`, and SHA-256; the manifest excludes
  only those two generated manifest files. The complete manifest has 565 files,
  64,800,271 bytes, and SHA-256
  `9f4af73ce3091bde3c61ff734feb92a3ec48f113d57327bc8142e2b6905b41bb`.
- `gamedata.json` SHA-256
  `683dfdc918c64af0243df227d230d962bd30df5b2064a2920697a1ae616b395a`
  declares exact VPX bounds `left=0`, `top=0`, `right=952.9`,
  `bottom=2117.6`. Normalization is `(x-left)/(right-left)` and
  `(y-top)/(bottom-top)`, rounded by the shared spatial helper to six decimals.
- `info.json` has no `author_name`; it identifies itself as a Basic VPW Example
  Table and describes a generic starter table. It therefore does not establish
  a Supreme table author, provenance, known-working status, or physical-machine
  construction. The table image and `cGameName` binding are implementation
  evidence only.

The retained filesystem creation time for the supplied VPX is
`2026-10-26T13:52:48Z`; original download/acquisition history is not recorded.
No redistribution license was supplied with this community table.
