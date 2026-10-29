---
name: rocky-control
disable-model-invocation: false
description: >-
  Inspect and control Agent Rocky (Project Hail Mary) sound notifications without changing pet selection.
  TRIGGER when: the user says "mute Rocky", "unmute Rocky", "Rocky status",
  "Agent Rocky status", "turn off prompt sounds", "stop the Rocky fix",
  "turn off amaze amaze amaze", "stop the good good good", "turn off fist my bump",
  "enable approval sounds", "Rocky attention mode", "turn off easter eggs",
  "stop the purring", "stop the annoyed lines", "stop Rocky hate Mark",
  "enable subagent sounds", "enable tool failure sounds", "enable compaction sounds",
  "turn on session end sounds", "Eridian only", "only the chords", "no English lines",
  "astrophage alarm", "not enough sound", "set a fuel budget", "set an astrophage budget",
  "statusline astrophage meter", "preview a Rocky sound", "play fist my bump",
  "play we die we die we die", or asks to inspect or adjust Agent Rocky notifications.
  DO NOT TRIGGER when: the user wants operating system volume controls, unrelated
  notification settings, Agent Navi controls (use navi-control), Agent Johnny 5
  controls (use johnny5-control), Agent Warcraft controls (use warcraft-control),
  Agent Star Wars controls (use starwars-control), Agent StarCraft controls (use
  starcraft-control), pet artwork, or pet selection through the host picker.
---

# Agent Rocky sound controls

Resolve this installed SKILL.md's directory. The bundled CLI is
`../../scripts/rocky.mjs` relative to it. Run it with Node and a quoted absolute
path, rather than assuming a global `agent-rocky` executable is installed.

- Inspect: `status`, `status --json`, `list`, or `config --effective`.
- Mute/unmute: `mute EVENT|easter-egg|all` or `unmute EVENT|easter-egg|all`.
- Presets: `preset attention` or `preset default`.
- Requested sound preview: `preview CLIP`.

Use `list` to resolve supported event and clip names. Translate a clear request
into the corresponding event:

| Request | Event |
|---|---|
| Session start ("Hello, Grace friend") | `session_started` |
| Prompt sounds ("Rocky fix", "Yes?") | `prompt_submitted` |
| Annoyed lines on rapid prompts ("Rocky hate Mark") | `annoyed` |
| Approval sounds, including the destructive-command alarm ("We die. We die. We die.") | `approval_required` |
| Questions ("Who is Grace talking to, question?") | `input_required` |
| Idle or ready notices ("This room boring") | `ready_for_input` |
| "Amaze! Amaze! Amaze!", "Good, good, good", "Fist my bump" | `turn_completed` |
| Rate limit, billing, or budget exhausted ("Not enough. Not enough.") | `out_of_astrophage` |
| Status-line low-fuel warning ("How much Astrophage you need, question?") | `astrophage_low` |
| Output token limit ("Too much! Too much! Too much!") | `out_of_xenonite` |
| Other API errors ("Bad, bad, bad") | `error` |
| Failed tool calls ("Could not fix") | `tool_failed` |
| Subagents starting ("Grace Rocky save stars") | `subagent_started` |
| Compaction ("Rocky can't forget") | `context_compacting` |
| Session end ("Grace go home") | `session_ended` |
| Rare purring, singing, and "Six seven, question?" | `easter-egg` |

The destructive alarm is part of `approval_required`; it cannot be muted
separately without muting approvals. Ask only when the requested event is unclear.

"Eridian only" or "no English lines" means using only the `eridian-` chord clips.
That is a custom clip list in the config file, not a CLI command. Show the user
the `events` entries to add, using clip names from `list`, and do not edit the
file without being asked.

The Astrophage meter is a status-line command, not a hook. When asked to set it
up or to set a budget, explain the `astrophage.budgetUsd` and
`astrophage.lowPercent` settings in the config file and the `statusline`
command documented in `docs/budget.md`, and show the user the line to add. Do
not edit the host's settings or status line yourself.

Change preferences only when the user requests that change. Inspection and
troubleshooting do not imply muting, unmuting, applying a preset, or playing
audio. Always specify an event or explicit `all`. Global mute/unmute preserves
event preferences. Presets change event enablement and preserve clips and
global mute.

Changes persist outside plugin caches and take effect on the next hook. Report
the resulting status. If `AGENT_ROCKY_MUTE` overrides the saved preference,
explain that the user must change it in the agent's launch environment. Do not
modify shell startup files or host configuration automatically.

Pet installation and selection are independent. These controls never change
pets, register hooks, or approve agent actions.
