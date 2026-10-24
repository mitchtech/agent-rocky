# Rocky pet

The sound plugin and the Codex pet are independent. Sounds support Claude Code,
Codex, Gemini CLI, and a generic event interface. The pet will be a local v2
Codex bundle whose animations are controlled by the host, without additional
hooks or a daemon.

## Status: not bundled yet

`pets/rocky/` holds the manifest only. The installer, validation, and release
packaging are complete, so adding art needs no runtime code changes:

```bash
agent-rocky pet status        # Pet: Rocky, not-bundled (...)
agent-rocky pet install       # explains that the art is not bundled; changes nothing
agent-rocky doctor --pet      # exits 1 until a pet is installed
```

Until the art ships, Codex's native pet feature can create a companion.
[Official pet documentation](https://learn.chatgpt.com/docs/pets)

## Adding the art

1. Place `spritesheet.webp` in `pets/rocky/`: a transparent 1536 x 2288 RGBA
   WebP, 8 columns by 11 rows of 192 x 208 cells, in Codex sprite version 2 row
   order (idle 6, moving-right 8, moving-left 8, waving 4, jumping 5, failure 8,
   waiting 6, working 6, review 6, then two 8-frame look-direction rows).
2. Add `LICENSE.txt` for the artwork and update `NOTICE.md` with its provenance.
   The art must be original, not frames or stills from the film.
3. Port `scripts/export-pet-web.py` from Agent Warcraft to write the nine-row web
   atlas to `assets/exports/agent-rocky-pet-web.webp` and record its hash in
   `assets/pet-revision.json`.
4. Run `python3 scripts/check-pet.py`; it validates the atlas and web export once
   the sheet exists.
5. `scripts/package-pet.py` then builds `agent-rocky-pet.zip`, the release
   workflow attaches it, `npm run site` copies the pet into the site, and
   `agent-rocky pet install` copies it into `~/.codex/pets/rocky/`.

The site's spectrum hero and "Coming soon" pet section were written for the
stub. Replace the pet section with a pet stage, as Agent Warcraft does, when the
art lands.

## Installer behavior

Once art ships, the CLI copies the four bundle files and a local ownership
record into `$CODEX_HOME/pets/rocky` (default `~/.codex/pets/rocky`). It
leaves avatar selection, agent settings, hooks, and audio configuration
unchanged. An identical install is a no-op.

Different files require `agent-rocky pet install --replace`. The previous entire
directory is renamed to `rocky.backup-<unique-suffix>` next to the new
installation. Files and symbolic links at the target directory path are never
replaced.

Status reports `not-bundled`, `not-installed`, `matching`, `modified`, or
`conflict`. Uninstall removes only an unchanged CLI-owned installation, even
when the current package has no art. It refuses edited files, unknown additional
files, symbolic links, and unmanaged installations.

## Validation limits

Installer tests run against a one-pixel fixture bundle. Native desktop and
terminal rendering will need a separate check once real art exists.
