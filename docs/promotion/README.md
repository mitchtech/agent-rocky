# Agent Rocky promotion kit

An owner-run, 30-day organic campaign for successful installs, GitHub
visibility, and recognition of Michael J. Mitchell as the maker. Budget: 3-5
hours per week, no ad spend. "Amaze! Amaze! Amaze!" on every finished turn is
the hook; the event map, the usage alarms, and the Eridian chords are the
substance.

This kit prepares promotion; it does not publish posts, contact people, schedule
messages, or submit the project to directories. Michael reviews and publishes
from his accounts.

## Start here

1. Complete the launch checks below before claiming a live host demonstration.
2. Use the [install walkthrough](install.md) to help early users.
3. Review the [post drafts](posts.md) and [answers to common questions](responses.md).
4. Attach `assets/promotion/sound-preview.mp4` (captioned, with `.srt`), built by
   [build-media.py](build-media.py). Keep its "illustrated preview" label visible.
5. Record publications and voluntary feedback in [campaign.csv](campaign.csv).
   Keep personal feedback details in a private copy, not a public PR.

## Positioning

> Agent Rocky plays Rocky's lines from *Project Hail Mary* when Claude Code,
> Codex, or Gemini CLI does something you should hear: "Amaze! Amaze! Amaze!"
> when a turn finishes, "What problem, question?" when it needs approval,
> "We die. We die. We die." when the approval is for `rm -rf`, and "Not enough.
> Not enough." when Claude Code hits a rate limit. Runs locally, with no
> runtime telemetry.

Primary audience: developers running local Claude Code or Codex sessions who
loved the book or the film. Secondary audiences: users of Agent Navi, Agent
Johnny 5, or Agent Warcraft who want a different voice, and people who want
quiet, non-verbal cues (the Eridian chords).

Use one primary link per post:

- Install: <https://github.com/mitchtech/agent-rocky#install>
- Event map: <https://github.com/mitchtech/agent-rocky#sounds>
- Interactive preview: <https://mitchtech.github.io/agent-rocky/>

Lead with an actual behavior, identify yourself as the maker, state that the
project is free to try, and invite one specific piece of feedback. Do not imply
every host has identical events, that the destructive-command cue is a safety
feature, or that a sound proves the agent completed a task successfully. Do
not use film stills, posters, or trailer footage in posts; the spectrum preview
and the site are the visuals. Do not promise a Codex pet date.

## Launch checks

- Fresh install and an audible cue on macOS from the GitHub marketplace for
  Claude Code and Codex; Gemini from the release ZIP.
- `agent-rocky statusline` inside a real Claude Code status line.
- The Pages site in Day and Night themes on a phone.
- Every film clip previewed once by ear (the transcripts already match).

## Publishing calendar

| Timing | Action | Budget |
|---|---|---|
| Days 1-7 | Capture baseline; run the launch checks; review copy | 4 hours |
| Day 8 | Publish X1 with the sound preview | Included below |
| Day 10 | Share R1 in r/ClaudeCode's current weekly showcase thread | Included below |
| Day 12 | Publish LinkedIn L1 | Days 8-14: 4 hours |
| Day 16 | Publish R2 in r/codex, with the current appropriate showcase flair | Included below |
| Day 18 | Publish X2 about the usage alarms and the Astrophage meter | Included below |
| Day 20 | Share R3 in r/ProjectHailMary if its rules allow fan tools | Days 15-21: 4 hours |
| Day 24 | Publish X3 about the Eridian chords | Included below |
| Days 28-30 | Ask willing early users about continued use; pick the next channel | Days 22-30: 3 hours |

Recheck rules, pinned threads, eligibility, and flair before posting. If a
destination does not permit the post, skip it. Do not work around moderation or
solicit upvotes. On posting days, return for roughly 15 minutes to answer
follow-up questions.

## Measurement

| Outcome | Day-30 target | Measurement |
|---|---|---|
| Successful use | 10 distinct people voluntarily report a successful install | Replies or issue comments; count each person once privately |
| Continued use | 5 report keeping Rocky after at least a week | Follow up only in an existing, willing conversation |
| Visibility | 25 net new GitHub stars | Difference from initial repository count |
| Product learning | 5 actionable observations | Reproducible blockers or specific preferences |

Capture metrics at the beginning and on days 7, 14, 21, and 30:

```bash
python3 docs/promotion/capture-metrics.py
```

The script uses an already authenticated `gh` CLI, reads only GitHub APIs, and
writes a timestamped JSON file under ignored `dist/promotion/metrics`. An
unavailable endpoint is recorded as unavailable, never as zero. GitHub's
traffic window is 14 days; do not sum overlapping windows.

| Observation | Action |
|---|---|
| Two people hit the same install blocker | Fix instructions or behavior before the next promotion |
| Sounds seem too frequent | Point to the attention preset, `mute annoyed`, or the Eridian-only config |
| Someone treats the alarm as a safety guarantee | Correct it plainly: it is a cue, not a guard |
| A rights holder asks for removal | Remove the film clips; the Eridian chords keep every event working |
