# Sound notes

Why each event plays what it plays, what else would fit, and how to change it.

## Mapping

| Event | Default clips | Why |
|---|---|---|
| `session_started` | `hello-grace-friend`, `hello-grace`, `hi-grace`, `i-am-rocky`, `can-hear` | Rocky's first words to Grace once the translator works. "Can hear." is his reply to a sound check. |
| `prompt_submitted` | `yes`, `rocky-fix`, `good-plan`, `words-of-encouragement`, `thumbs-up-baby` | Acknowledgments. "Rocky fix." is the engineer taking the job. |
| `annoyed` | `room-for-garbage`, `hate-mark`, `grace-look-disgust` | Rocky's complaints, saved for the third prompt in ten seconds. |
| `approval_required` | `what-problem`, `sampler-question`, `eridian-question` | Eridian questions end with "question?", which is exactly what an approval is. |
| Approval for shell or edit | `down-here-question` | "What's this down here, question?" fits a tool reaching into your files. |
| Approval for a destructive command | `we-die`, `bad-bad-bad`, `eridian-alarm` | The loudest, most agitated lines Rocky has. |
| `input_required` | `who-is-grace-talking-to`, `eridian-question` | The agent is asking you directly. |
| `ready_for_input` | `this-room-boring`, `eridian-hum` | An idle Rocky, waiting. |
| `turn_completed` | `amaze-amaze-amaze`, `good-good-good`, `fist-my-bump`, `eridian-happy` | The lines people install this for. |
| `out_of_astrophage` | `not-enough`, `eridian-sad` | Rate limit or budget spent: the fuel is gone. |
| `astrophage_low` | `how-much-astrophage` | The meter warning, asked as a question. |
| `out_of_xenonite` | `too-much` | The reply ran past the output token limit. |
| `error` | `bad-bad-bad`, `eridian-sad` | Off by default. |
| `tool_failed` | `could-not-fix`, `dirty-dirty-dirty` | Off by default; tool failures are frequent. |
| `subagent_started` | `saves-stars`, `build-workshop`, `eridian-greet` | A crew member setting off. Off by default. |
| `context_compacting` | `cant-forget` | Rocky's memory is perfect; the context window's is not. Off by default. |
| `session_ended` | `grace-go-home`, `we-go-home`, `thank-you` | Farewells. Off by default. |
| Easter egg | `purr`, `singing`, `song`, `six-seven` | Rare, and only on non-urgent cues. |

Every clip, its words, and its source are listed in the [audio notice](../audio/NOTICE.md).

## Eridian chords

The six `eridian-` clips contain no film audio. They layer pitched CC0
recordings, following how the film's sound designers described building Rocky's
voice: ocarina for the high notes, didgeridoo and whale song for the low ones,
higher and faster when he is agitated, and a quick rising call for a question.

| Clip | Sound | Used by |
|---|---|---|
| `eridian-question` | Two ocarina glissandi a fifth apart, rising | `approval_required`, `input_required` |
| `eridian-happy` | Ocarina major chord with an octave | `turn_completed` |
| `eridian-sad` | Low ocarina minor chord over didgeridoo | `out_of_astrophage`, `error` |
| `eridian-alarm` | Ocarina melody a semitone apart, with a high clash | Destructive approvals |
| `eridian-hum` | Whale song over a lowered didgeridoo | `ready_for_input` |
| `eridian-greet` | Slowed whippoorwill with an owl-like ocarina call | `subagent_started` |

### Eridian only

For quiet offices, or to avoid the film audio entirely, point every event at the
chords in `~/.config/agent-rocky/config.json`:

```json
{
  "easterEgg": { "chance": 0 },
  "events": {
    "session_started": { "clips": ["eridian-greet"] },
    "prompt_submitted": { "clips": ["eridian-hum"] },
    "annoyed": { "clips": ["eridian-alarm"] },
    "approval_required": { "clips": ["eridian-question"], "changeClips": ["eridian-question"], "dangerClips": ["eridian-alarm"] },
    "input_required": { "clips": ["eridian-question"] },
    "ready_for_input": { "clips": ["eridian-hum"] },
    "turn_completed": { "clips": ["eridian-happy"] },
    "out_of_astrophage": { "clips": ["eridian-sad"] },
    "astrophage_low": { "clips": ["eridian-sad"] },
    "out_of_xenonite": { "clips": ["eridian-alarm"] },
    "error": { "clips": ["eridian-sad"] },
    "tool_failed": { "clips": ["eridian-sad"] },
    "subagent_started": { "clips": ["eridian-greet"] },
    "context_compacting": { "clips": ["eridian-hum"] },
    "session_ended": { "clips": ["eridian-hum"] }
  }
}
```

## Alternatives worth trying

Lines that did not make the defaults but fit well:

- `thank-you` on `turn_completed`, for a politer finish.
- `can-hear` on `ready_for_input`.
- `could-not-fix` on `error`.
- `six-seven` anywhere you want to be asked a number question for no reason.

## Your own clips

To use recordings you own, copy the bundled `audio/` directory somewhere
outside the plugin cache, replace or add WAV files, and set `audioDir`. The
directory must contain a `<clip>.wav` for every name in `agent-rocky list`; use
16-bit PCM WAV so every player can read it.

```json
{ "audioDir": "/Users/you/rocky-audio" }
```

Use an absolute path; `~` is not expanded. Relative paths resolve from the config file's directory. To add a new clip id
to the bundle itself, see [distribution maintenance](distribution.md#audio).
