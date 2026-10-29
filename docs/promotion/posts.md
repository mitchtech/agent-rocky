# Public post drafts

Owner review required before publishing. These drafts describe documented
behavior, not fabricated user results. Attach `assets/promotion/sound-preview.mp4`
and keep its preview label visible. Recheck community rules and flair on
publication day. Use one primary destination per post.

## R1 - r/ClaudeCode weekly showcase

I built Agent Rocky, a free sound-notification plugin for Claude Code. It plays
Rocky's lines from *Project Hail Mary* on agent events: "Hello, Grace friend."
when a session starts, "What problem, question?" for an approval, and "Amaze!
Amaze! Amaze!" when a turn finishes. When Claude Code stops on a rate limit or
billing error, Rocky says what any engineer on a fuel budget would: "Not
enough. Not enough."

The attached clip is an illustrated sound preview, not a live hook recording.

```bash
claude plugin marketplace add mitchtech/agent-rocky
claude plugin install rocky@agent-rocky
```

It needs Node.js 22+ and local audio. Restart Claude Code after installation.
It runs locally with no runtime telemetry, and the hooks never approve or block
actions. Approvals for `rm -rf` or a force push get "We die. We die. We die."
instead; that is a louder cue, not a safety check. There is also an optional
status-line Astrophage meter that asks "How much Astrophage you need,
question?" once when your 5-hour or weekly limit runs low.

Install details: https://github.com/mitchtech/agent-rocky#install

Which line would you turn off first?

## R2 - r/codex showcase

Title: I built Agent Rocky: Project Hail Mary sound cues for Codex

Agent Rocky is a free plugin that plays Rocky's lines in local Codex sessions.
Prompts get "Rocky fix.", approvals get "What problem, question?", a finished
turn gets "Amaze! Amaze! Amaze!" or "Fist my bump.", and subagents can announce
"Grace Rocky save stars." if you turn that cue on. Approvals whose command
matches a short destructive list get "We die. We die. We die." Only a yes/no
flag leaves the hook; the command is never logged or stored.

The attached video illustrates the sound; it is not a live Codex recording.

```bash
codex plugin marketplace add mitchtech/agent-rocky
codex plugin add rocky@agent-rocky
```

Requirements: Node.js 22+, a local audio player, trusted hooks, and a restart.
Event coverage in Codex: session, prompt, approval, completion, subagent,
compaction, and session end.

https://github.com/mitchtech/agent-rocky#install

## R3 - r/ProjectHailMary (only if fan tools are allowed)

I made a small fan tool: my coding agents now talk like Rocky. "Amaze! Amaze!
Amaze!" when a job finishes, "Not enough. Not enough." when I run out of usage,
and "We die. We die. We die." when the agent wants to `rm -rf` something.

For the quiet version, I built six untranslated Eridian chords from public
domain ocarina, didgeridoo, and whale recordings, following how the film's
sound team described making Rocky's voice. You can hear all of them here:
https://mitchtech.github.io/agent-rocky/

Free and open source. Not affiliated with the book or the film.

## X1 - sound

My coding agent now finishes every turn with "Amaze! Amaze! Amaze!"

Agent Rocky: Project Hail Mary sound cues for Claude Code, Codex, and Gemini
CLI. Local, no telemetry, never approves anything.

https://github.com/mitchtech/agent-rocky

## X2 - usage alarms

Hit a Claude Code rate limit and Rocky tells you: "Not enough. Not enough."

There is a status-line Astrophage meter too: `⬠ 18% astrophage (5h) low`, with
one "How much Astrophage you need, question?" before the tanks run dry.

https://github.com/mitchtech/agent-rocky#astrophage-meter-and-usage-alarms

## X3 - Eridian chords

Rocky talks in chords. So I built six of them from CC0 ocarina, didgeridoo, and
whale recordings, following the film sound team's recipe, and wired them to
agent events. Quiet-office mode for coding agents.

The site labels the notes of every line live: https://mitchtech.github.io/agent-rocky/

## L1 - LinkedIn

I keep building small tools that make coding agents easier to work beside. The
newest is Agent Rocky: sound cues from *Project Hail Mary* for Claude Code,
Codex, and Gemini CLI.

The engineering is the same as its siblings (Agent Navi, Agent Johnny 5, Agent
Warcraft, Agent Star Wars, and Agent StarCraft): one dependency-free Node runtime, native hooks for each host,
fail-open behavior, and no telemetry. Destructive-command detection runs inside
the hook and only a yes/no flag leaves it.

The new part is audio provenance. Every clip is rebuilt from recorded sources
with fixed cut points and loudness normalization, and six of them are original
chords made from public domain recordings, so the plugin keeps working if the
film clips ever have to go.

https://github.com/mitchtech/agent-rocky
