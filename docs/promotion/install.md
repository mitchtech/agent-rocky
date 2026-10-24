# Install walkthrough

For helping early users. Each host needs Node.js 22+ on the agent's `PATH` and a
local audio player (`afplay` on macOS, `paplay`/`pw-play`/`aplay`/`ffplay` on
Linux, PowerShell on Windows).

## Claude Code

```bash
claude plugin marketplace add mitchtech/agent-rocky
claude plugin install rocky@agent-rocky
```

Restart Claude Code. Send a prompt: "Yes?" or "Rocky fix." should play.

## Codex

```bash
codex plugin marketplace add mitchtech/agent-rocky
codex plugin add rocky@agent-rocky
```

Open Codex's hook settings and trust the plugin's hooks, then restart.

## Gemini CLI

```bash
gemini extensions install https://github.com/mitchtech/agent-rocky
```

Accept the hook consent prompt and restart Gemini.

## When nothing plays

1. Run the doctor from the installed plugin, or install the standalone command:

   ```bash
   npm install -g github:mitchtech/agent-rocky
   agent-rocky doctor
   agent-rocky preview amaze-amaze-amaze
   ```

2. `Player: MISSING` means no audio backend was found on `PATH`.
3. `Muted: true` with `AGENT_ROCKY_MUTE` set means the environment overrides the
   saved preference.
4. Over SSH, in containers, or in WSL, sound plays on the machine running the
   hook, not on your laptop.

## Running more than one Agent plugin

Agent Navi, Agent Johnny 5, Agent Warcraft, and Agent Rocky respond to the same
events. Enable one per host, for example
`claude plugin disable warcraft@agent-warcraft`.

## Quieter setups

- `agent-rocky preset attention` keeps only approvals, questions, idle, and usage alarms.
- `agent-rocky mute annoyed` and `agent-rocky mute easter-egg` remove the jokes.
- The [Eridian-only config](../sounds.md#eridian-only) replaces every English line with chords.
