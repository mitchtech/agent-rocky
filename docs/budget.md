# Budget alarms, the Astrophage meter, and the memory gauge

Agent Rocky has two ways to tell you that usage is running out: hook events
when a turn has already failed, and an optional status-line meter that warns you
before it does.

## Hook events

Claude Code runs `StopFailure` instead of `Stop` when a turn ends on an API
error. Its `error` field names the failure type:

| `error` | Shared event | Lines | Default |
|---|---|---|---|
| `rate_limit`, `billing_error`, `account_on_hold` | `out_of_astrophage` | "Not enough. Not enough." or a low Eridian minor chord | On |
| `max_output_tokens` | `out_of_xenonite` | "Too much! Too much! Too much!" | On |
| Any other type, or none | `error` | "Bad, bad, bad." or a low Eridian minor chord | Off |

Claude Code's usage-limit notifications map as follows:

| `notification_type` | Shared event | Why |
|---|---|---|
| `quota_auto_resume_disabled` | `out_of_astrophage` | The wait for a usage limit ended without continuing your task |
| `quota_auto_resume_stale` | `ready_for_input` | The limit reset while the computer slept; Claude Code is waiting for Enter |
| `quota_auto_resume_fired` | none | The task continued on its own |

Codex and Gemini CLI do not report API failures to hooks. Wrappers around them
can call `agent-rocky play out_of_astrophage` themselves.

## The Astrophage meter

`agent-rocky statusline` reads the JSON that Claude Code sends to a status
line command on stdin. It prints one line and exits.

```text
⬠ 62% astrophage (5h)
⬠ 62% astrophage (5h) · 41% memory
⬠ 90% memory full
⬠ 18% astrophage (7d) low
⬠ $1.25 astrophage low
⬠ 0% astrophage (spend) out
⬠
```

Astrophage is whatever is left of your **tightest** limit, chosen from these sources:

- `rate_limits.five_hour.used_percentage` (5h). Claude.ai Pro and Max plans
  report this after the first response in a session.
- `rate_limits.seven_day.used_percentage` (7d), reported on the same plans.
- `rate_limits.spend_limit.used_percentage` (spend), reported behind a Claude
  apps gateway with a spend limit.
- `cost.total_cost_usd` against `astrophage.budgetUsd`, when you set a budget. This
  is Claude Code's client-side estimate at list price. It resets when `/clear`
  starts a new session, so treat it as a per-session budget.

A bare `⬠` means no limit is reported yet, which is normal for API-key sessions
without a budget. The same bare line appears if the input or configuration
can't be read: the meter never fails the status line.

### Cues

- Crossing `astrophage.lowPercent` used (default 80) plays `astrophage_low`: "How much
  Astrophage you need, question?"
- Reaching 100% plays `out_of_astrophage`.

Each cue plays once per session per rise. When usage falls back, as when a
5-hour window resets, the meter re-arms, and the next crossing plays again.
Mute either with `agent-rocky mute astrophage_low` or `agent-rocky mute out_of_astrophage`.

### Memory gauge

When the status line input includes `context_window`, the meter appends how
much of the context window is in use. It reads `context_window.used_percentage`,
or computes it from `total_input_tokens` and `context_window_size`. Claude Code
counts input tokens only.

Crossing `memory.lowPercent` (default 85) plays `memory_full`: "Rocky can't
forget." It plays once per session per rise and re-arms when use drops, as
after compaction or `/clear`. When both meters rise in the same update, the
Astrophage cue wins and the memory cue waits for the next update. Mute it with
`agent-rocky mute memory_full`.

### Setup

The status line runs outside the plugin, so it needs the standalone command:

```bash
npm install -g github:mitchtech/agent-rocky
```

If you have no status line yet, add this to `~/.claude/settings.json`:

```json
{ "statusLine": { "type": "command", "command": "agent-rocky statusline" } }
```

If you already have a status line script, keep it and append the meter. The
script receives the JSON once on stdin, so save it before using it twice:

```bash
#!/bin/sh
input=$(cat)
mine=$(printf '%s' "$input" | your-existing-statusline)
fuel=$(printf '%s' "$input" | agent-rocky statusline)
printf '%s  %s\n' "$mine" "$fuel"
```

### Settings

```json
{ "astrophage": { "budgetUsd": 20, "lowPercent": 75 }, "memory": { "lowPercent": 90 } }
```

| Setting | Default | Meaning |
|---|---|---|
| `astrophage.budgetUsd` | `null` | Per-session dollar budget, or `null` to use rate limits only |
| `astrophage.lowPercent` | `80` | Percent used at which `astrophage_low` plays; between 0 and 100 |
| `memory.lowPercent` | `85` | Percent of the context window at which `memory_full` plays; between 0 and 100 |

The meter stores one fuel level and one memory level per session under a hashed name in the state
directory. Nothing about your usage or cost is written anywhere else.
