# Changelog

## Unreleased

## 0.2.0 - 2026-10-28

Meet Rocky: an animated Codex pet, plus a memory gauge on the status line.

- Bundle original Rocky v2 pet artwork with nine animations and sixteen look directions, a byte-preserved source PNG, lossless WebP, CC BY 4.0 provenance, and a nine-row web export.
- Replace the site's pet placeholder with animation and look-direction controls, pause/reduced-motion support, and installation links. Add reproducible pet previews and exercise real artwork in installer/package checks.
- Add a memory gauge to `agent-rocky statusline`: it shows context window use beside the Astrophage meter and plays `memory_full` ("Rocky can't forget.") once per rise past `memory.lowPercent` (85% by default). Ported from Agent StarCraft's supply meter.
- Add a 512 px plugin listing icon.
- Link the Agent Star Wars and Agent StarCraft sibling projects in the README, site, control skill, and promotion kit.

## 0.1.0 - 2026-10-24

First release, built on the Agent Warcraft 0.3.0 runtime.

- Play 44 clips on agent events in Claude Code, Codex, and Gemini CLI: 38 of Rocky's lines from *Project Hail Mary* and 6 untranslated Eridian chords built from CC0 ocarina, didgeridoo, whale, and whippoorwill recordings.
- Map Claude Code `StopFailure` errors to usage alarms: rate limits, billing errors, and accounts on hold play `out_of_astrophage` ("Not enough. Not enough."), and the output token limit plays `out_of_xenonite` ("Too much! Too much! Too much!").
- Add `agent-rocky statusline`, an Astrophage meter for Claude Code's status line that shows the tightest remaining limit and cues `astrophage_low` once per session.
- Play an `annoyed` line on the third prompt inside ten seconds, a destructive-command alarm ("We die. We die. We die."), optional tool-failure, subagent, compaction, and session-end cues, and a 2% easter egg.
- Record every clip's source, cut points, and pitch layers in `audio/sources.json`. `build-audio.py` rebuilds them at -16 LUFS, prints the `yt-dlp` command for YouTube sources, and mixes pitched layers into chords.
- Ship the Codex pet installer, validation, and packaging with a manifest-only stub; `pet status` reports `not-bundled` until the art lands.
- Publish a site with an Eridian spectrum analyzer that labels the notes of each line, a twelve-key command card, and Day and Night themes that follow the OS. The README banner switches with GitHub's color scheme.
