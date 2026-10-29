# Answers to common questions

Short, accurate replies. Adapt the tone to the thread.

**Is this official?**
No. It is a fan project, not affiliated with Andy Weir, Amazon MGM Studios, or
the film's makers. The film lines are credited in the audio notice and will be
removed on request.

**Where do the sounds come from?**
38 lines are clips of the film: Myinstants uploads and official clips and
trailers. 6 are Eridian chords I built from CC0 recordings of ocarina,
didgeridoo, and whale song, following how the film's sound designers described
Rocky's voice. Every source and cut point is in `audio/sources.json`.

**Will it approve or block anything?**
No. Hooks fail open and never return a decision. The destructive-command line
("We die. We die. We die.") is a louder cue, not a guard; only a yes/no flag
leaves the hook, and the command is never logged or stored.

**Does a finished-turn sound mean the task worked?**
No. `Stop` means the agent finished responding. Check the work.

**It's too much.**
`agent-rocky preset attention` keeps approvals, questions, idle, and usage
alarms. `agent-rocky mute annoyed` removes the jokes. The Eridian-only config in
`docs/sounds.md` drops the English entirely.

**Where's the Codex pet?**
The original Rocky artwork is bundled. Run `agent-rocky pet install`, then
select Rocky in a compatible Codex host. Sounds and pet installation are independent.

**Why not Grace's lines too?**
Rocky is the character people want to hear. Grace's voice would also make cues
harder to tell apart from real speech around you.

**Does it work with Navi, Johnny 5, Warcraft, Star Wars, or StarCraft installed?**
Yes, but they all respond to the same events. Enable one per host.

**Does it send telemetry?**
No. It plays local files and stores hashed session ids with timestamps.
