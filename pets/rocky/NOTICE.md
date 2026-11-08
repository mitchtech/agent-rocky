# Rocky pet artwork

This original artwork depicts Rocky, the Eridian engineer from Project Hail
Mary. Michael J. Mitchell requested it on October 23, 2026, and created it
with Codex using built-in image generation. A canonical character image
grounded each animation and look-direction strip. Deterministic processing
extracted, registered, assembled, cleaned, and validated the generated pixels.
No frames, stills, sprites, or models were extracted from the film.

Rocky and Project Hail Mary belong to Andy Weir and their respective rights
holders. This project is not affiliated with or endorsed by them or by
Amazon MGM Studios. Film audio has a separate [rights notice](../../audio/NOTICE.md).

The contributor's rights in this artwork are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as described in
[LICENSE.txt](LICENSE.txt). Suggested credit: "Rocky pet artwork by Michael
J. Mitchell / mitchtech, CC BY 4.0, https://github.com/mitchtech/agent-rocky."

## Format and validation

- ID: `rocky`; display name: `Rocky`; sprite version: `2`.
- Transparent RGBA WebP, 1536 x 2288 pixels, with 192 x 208 cells.
- Nine animation rows: idle, moving right, moving left, waving, jumping,
  failure, waiting, working, and review.
- Two look rows: sixteen clockwise directions, beginning at up.
- 73 occupied cells and 15 fully transparent unused cells.

The source PNG passed structural, chroma, jump, registration, and visual
direction checks. Three isolated reviewers confirmed all gaze axes. An
exterior-background connectivity audit distinguished open limb gaps from
interior holes flagged by the scanline heuristic. The exact final PNG passed
the Pets service preflight. Native local-host rendering remains unverified.

## Source and active files

The exact original PNG and local host manifest are preserved in
`assets/original/rocky`. Account-pet IDs and temporary upload links are
excluded from distribution. `assets/pet-revision.json` records source,
active, and web-export hashes.

| File | SHA-256 |
|---|---|
| Original PNG | `0b7c5b299da30317494b9ef8135a3a692a33d06149e1ca2a355f054892518dd5` |
| Active WebP | `0332a9b2cc8b5c35f4ed78daecd7004791a376aca9cb5d68f929d56e2b95a25d` |

The WebP was encoded with Pillow using `lossless=True`, `quality=100`,
`method=6`, and `exact=True`. Decoded RGBA pixels are identical to the source,
including RGB under transparent pixels. The separate web export contains
exactly the first nine animation rows.
