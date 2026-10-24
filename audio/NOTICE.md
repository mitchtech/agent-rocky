# Audio provenance and rights

This directory holds two kinds of clips.

**Film lines (38 clips).** These are derived from *Project Hail Mary* (2026,
Amazon MGM Studios), based on the novel by Andy Weir. Rocky is voiced by James
Ortiz. The rights holders retain all rights to the film audio, including every
line here. No ownership of these clips is claimed, and no affiliation with or
endorsement by Andy Weir, Amazon MGM Studios, or the film's makers is implied.
The film lines are included for personal, non-commercial use. This notice
records their provenance; it is not a license from the rights holders. They
will be removed on request.

**Eridian chords (6 clips, `eridian-*.wav`).** These are original arrangements
of CC0 (public domain dedication) recordings from Freesound: ocarina,
didgeridoo, whale song, and whippoorwill, pitched and layered into chords. They
follow the film sound designers' public description of how Rocky's voice was
made, but contain no film audio. They are free to reuse. If the film lines are
ever removed, every event still has an Eridian chord or can be pointed at one.

The repository's MIT license covers source code and configuration only. It
does not cover the film recordings or grant any rights to the film's audio.

## Sources and processing

[`sources.json`](sources.json) lists every source URL, its SHA-256, the cut
points and pitch shifts where they apply, and the hash of each committed output.

- **Myinstants** clips are user uploads of film audio. They download with plain
  HTTP, and none carries a license.
- **YouTube** sources are official clips and trailers published by Amazon MGM
  Studios and Prime Video. Video audio cannot be fetched over plain HTTP, so
  rebuilding those clips needs `yt-dlp`; `build-audio.py` prints the exact
  command and cache path for any missing source. A fresh download can differ
  byte for byte from the recorded one, so the committed WAVs are canonical.
- **Freesound** sources are the public HQ previews of CC0 recordings.

Every film clip's words were checked against a speech-to-text transcript before
it was committed.

[`scripts/build-audio.py`](../scripts/build-audio.py) cuts each source, shifts
the pitch of instrument layers and mixes them into chords where a clip asks for
it, trims leading and trailing room tone, applies one linear gain to reach -16
LUFS integrated with a peak limiter, adds 10-20 ms fades, and writes 16-bit mono
PCM WAV at 32 kHz. `--check` verifies the committed files without downloading
anything.

## Film lines

| File | Line | Length | Source |
|---|---|---|---|
| `hello-grace-friend.wav` | Hello, Grace friend. | 0.88 s | Myinstants `hello-grace-friend.mp3` |
| `hello-grace.wav` | Hello, Grace. | 0.82 s | Myinstants `hello-grace.mp3` |
| `hi-grace.wav` | Hi, Grace. | 0.74 s | Myinstants `hi-grace.mp3` |
| `i-am-rocky.wav` | I am Rocky. | 2.70 s | YouTube P0XN3-n-2Lo, Final Trailer (Amazon MGM Studios), 89.3-92 s |
| `can-hear.wav` | Can hear. | 0.84 s | Myinstants `rocky-yes-can-hear.mp3` |
| `yes.wav` | Yes? | 0.55 s | Myinstants `rocky-say-yes.mp3` |
| `rocky-fix.wav` | Rocky fix. | 1.15 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 328.85-330 s |
| `good-plan.wav` | Science! Save Earth! Save Erid! Good plan! | 2.35 s | YouTube yUDp8l7rysU, "Roommates" official clip (Amazon MGM Studios), 17.7-20.05 s |
| `words-of-encouragement.wav` | Words of encouragement. Words of great encouragement. | 3.10 s | Myinstants `rocky-words-of-encouragement.mp3` |
| `thumbs-up-baby.wav` | Thumbs up, baby. | 1.88 s | Myinstants `rocky-thumbs-up-baby.mp3` |
| `this-room-boring.wav` | This room boring. | 1.77 s | Myinstants `this-room-boring-rocky.mp3` |
| `room-for-garbage.wav` | Is this room for garbage? | 1.25 s | Myinstants `this-room-for-garbage.mp3` |
| `hate-mark.wav` | Rocky hate Mark. | 1.33 s | Myinstants `rocky-hate-mark.mp3` |
| `grace-look-disgust.wav` | Grace look disgust when you eat. | 2.50 s | Myinstants `grace-look-disgust.mp3` |
| `what-problem.wav` | What problem, question? | 1.50 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 407.9-409.4 s |
| `sampler-question.wav` | Astrophage sampler in position, question? | 2.55 s | YouTube vppn4gX0eUI, "Having A Moment" official clip (Prime Video), 0.9-3.45 s |
| `down-here-question.wav` | What's this down here, question? | 3.05 s | YouTube yUDp8l7rysU, "Roommates" official clip (Amazon MGM Studios), 19.95-23 s |
| `who-is-grace-talking-to.wav` | Who is Grace talking to, question? | 1.78 s | Myinstants `who-is-grace-talking-to.mp3` |
| `we-die.wav` | We die. We die. We die. | 2.65 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 294.35-297 s |
| `bad-bad-bad.wav` | Bad, bad, bad. | 0.82 s | Myinstants `rocky-bad-bad-bad.mp3` |
| `amaze-amaze-amaze.wav` | Amaze! Amaze! Amaze! | 1.33 s | Myinstants `rocky-amaze-amaze-amaze_mG6l8jR.mp3` |
| `good-good-good.wav` | Good, good, good. | 0.81 s | Myinstants `rocky-good-good-good.mp3` |
| `fist-my-bump.wav` | Fist my bump. | 1.80 s | YouTube 5VYsnngkS_U, Official Trailer 2 (Amazon MGM Studios), 175.5-177.3 s |
| `not-enough.wav` | Not enough. Not enough. | 1.00 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 287-288 s |
| `how-much-astrophage.wav` | How much Astrophage you need, question? | 2.30 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 298.8-301.1 s |
| `too-much.wav` | Too much! Too much! Too much! | 1.00 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 288-289 s |
| `could-not-fix.wav` | Could not fix. | 2.30 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 324-326.3 s |
| `dirty-dirty-dirty.wav` | Dirty, dirty, dirty. | 3.24 s | Myinstants `rocky-dirty-dirty-dirty.mp3` |
| `saves-stars.wav` | Grace Rocky save stars. | 2.70 s | YouTube 5VYsnngkS_U, Official Trailer 2 (Amazon MGM Studios), 93.5-96.2 s |
| `build-workshop.wav` | Rocky will build workshop here. | 2.05 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 189.95-192 s |
| `cant-forget.wav` | Rocky can't forget. | 2.20 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 605-607.2 s |
| `grace-go-home.wav` | Grace go home. | 5.50 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 346.5-352 s |
| `we-go-home.wav` | We go home. | 1.05 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 197.95-199 s |
| `thank-you.wav` | Thank you, thank you, thank you. | 0.95 s | YouTube ayJPcBkR2is, The Best Friendship in Space (Prime Video UK & IE), 583.8-584.75 s |
| `purr.wav` | (Eridian purr) | 2.04 s | Myinstants `rocky-purr.mp3` |
| `singing.wav` | (Rocky sings) | 5.96 s | Myinstants `rocky-phm-singing.mp3` |
| `song.wav` | (Rocky's song) | 5.84 s | Myinstants `rocky-phm-song.mp3` |
| `six-seven.wav` | Six seven. Six seven, question? | 2.61 s | Myinstants `rocky-67.mp3` |

## Eridian chords

Semitone shifts are relative to each recording (`st`).

| File | Sound | Length | Layers |
|---|---|---|---|
| `eridian-question.wav` | (Eridian: a fast rising question) | 0.92 s | Freesound 846436 (Mexican Ocarina Glissando by NikoletB, CC0), +3 st; Freesound 846436 (Mexican Ocarina Glissando by NikoletB, CC0), +10 st |
| `eridian-happy.wav` | (Eridian: a bright major chord) | 1.67 s | Freesound 320849 (Ocarina (C) by alegemaate, CC0), +0 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), +4 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), +7 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), +12 st |
| `eridian-sad.wav` | (Eridian: a low minor chord) | 3.36 s | Freesound 320849 (Ocarina (C) by alegemaate, CC0), -12 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), -9 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), -5 st; Freesound 272165 (Didgeridoo by dethrok, CC0) |
| `eridian-alarm.wav` | (Eridian: agitated high chord) | 1.65 s | Freesound 846437 (Mexican Ocarina Singing by NikoletB, CC0), +5 st; Freesound 846437 (Mexican Ocarina Singing by NikoletB, CC0), +6 st; Freesound 320849 (Ocarina (C) by alegemaate, CC0), +13 st |
| `eridian-hum.wav` | (Eridian: a low whale hum) | 3.69 s | Freesound 171945 (LowWhalesong by RebekahDay, CC0); Freesound 272165 (Didgeridoo by dethrok, CC0), -3 st |
| `eridian-greet.wav` | (Eridian: a slowed birdsong greeting) | 3.30 s | Freesound 176965 (Whippoorwill by kvgarlic, CC0), -7 st; Freesound 826361 (Ocarina Owl Like by Gorkovoy, CC0), +2 st |

## Your own recordings

Replacement recordings you own can be used through `audioDir` in the
configuration; see the README.
