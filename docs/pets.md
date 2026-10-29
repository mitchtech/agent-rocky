# Rocky pet

The sound plugin and Codex pet install independently. The original Rocky
artwork is a local v2 Codex bundle with nine animations and sixteen clockwise
look directions. The host controls its activity without extra hooks or a daemon.

## Install

With the Agent Rocky CLI installed:

```bash
agent-rocky pet install
agent-rocky pet status
agent-rocky doctor --pet
```

Then select Rocky in the desktop pet picker, or enter `/pets Rocky` in a
supported Codex CLI terminal. Installation never changes pet selection,
agent settings, sound hooks, or audio configuration.

For a standalone install, download `agent-rocky-pet.zip` from the
[releases](https://github.com/mitchtech/agent-rocky/releases), then extract its
`rocky` directory into `~/.codex/pets/` (or `$CODEX_HOME/pets/`). Preserve any
existing directory first. Manual installs are unmanaged by the CLI.

## Artwork and source

`pets/rocky/` contains `pet.json`, `spritesheet.webp`, `LICENSE.txt`, and
`NOTICE.md`. The transparent 1536 x 2288 atlas has eight columns and eleven
rows of 192 x 208 cells, with 73 occupied cells and 15 transparent unused cells:

| Row | Animation | Frames |
|---|---|---:|
| 0 | Idle | 6 |
| 1 | Moving right | 8 |
| 2 | Moving left | 8 |
| 3 | Waving | 4 |
| 4 | Jumping | 5 |
| 5 | Failure | 8 |
| 6 | Waiting | 6 |
| 7 | Working | 6 |
| 8 | Review | 6 |
| 9-10 | Clockwise look directions, beginning at up | 16 |

The exact source PNG and local manifest are archived in `assets/original/rocky`.
The active WebP preserves every decoded RGBA pixel. Source and active hashes
are recorded in `assets/pet-revision.json`; no account-pet IDs or temporary
upload URLs are distributed. See the [artwork notice](../pets/rocky/NOTICE.md).

Contributor rights in the original artwork are licensed under
[CC BY 4.0](../pets/rocky/LICENSE.txt). Suggested credit: "Rocky pet artwork by
Michael J. Mitchell / mitchtech, CC BY 4.0, https://github.com/mitchtech/agent-rocky."
Character IP and trademarks remain with their respective holders. No film
frames, stills, or models were used as sprite assets.

## Web upload

`assets/exports/agent-rocky-pet-web.webp` contains exactly the first nine
animation rows, without the local v2 look rows. It is a transparent
1536 x 1872 lossless WebP with 57 occupied cells and 15 unused cells. It is
an account-upload artifact; the local v2 bundle stays unchanged.

Download the web atlas from the site or a release and use it in your account's
custom pet creation flow. Keep the same credit when sharing the artwork.
Local installation and account pet creation are separate operations.

Regenerate and check the export:

```bash
python3 scripts/export-pet-web.py
python3 scripts/check-pet.py
```

## Installer behavior

The CLI copies the four bundle files and a local ownership record into
`$CODEX_HOME/pets/rocky` (default `~/.codex/pets/rocky`). An identical install
is a no-op.

Different files require `agent-rocky pet install --replace`. The previous
entire directory is renamed to `rocky.backup-<unique-suffix>` next to the new
installation. Files and symbolic links at the target path are never replaced.

Status reports `not-bundled`, `not-installed`, `matching`, `modified`, or
`conflict`. Uninstall removes only an unchanged CLI-owned installation,
even when the current package has no art. It refuses edited files, unknown
additional files, symbolic links, and unmanaged installations. Older or
manifest-only packages still report `not-bundled` without changing files.

## Builds and validation

`scripts/check-pet.py` checks the real atlas and exact web-export pixels.
`scripts/package-pet.py` builds reproducible versioned pet ZIPs, and
`scripts/package-release.py` adds the stable ZIP and web atlas to releases.
`npm run site` copies the active bundle and web export into the built site.
`scripts/build-assets.py` renders pet GIF previews from the active atlas.

Installer tests cover the real artwork and fixture-isolated conflict and
missing-art cases. Package checks install the actual tarball and generated
Gemini bundle into isolated temporary directories. These checks do not prove
native desktop or terminal rendering on every OS.
