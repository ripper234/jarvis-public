# Song-Aware Running Coach

*A running app that feels like Spotify plus a coach.*

## What it is

This is a running app that knows the current song and uses natural transition moments, especially when a song begins or ends, to deliver cues like pace up, recover, form check, or motivation.

The key idea is that coaching should not constantly interrupt the music. The soundtrack and the coaching should feel designed together. Songs become workout blocks, not just background audio.

## Why it could be interesting

Most running apps make a tradeoff:
- music players feel good but do not coach well
- coaching apps talk a lot but disrupt the music

This concept tries to combine both. The coaching layer would be aware of track structure and use the music itself as part of the workout design.

## Product shape

Possible moments for intervention:
- song starts
- song endings
- transitions between songs
- interval boundaries
- recovery windows
- effort ramps

Possible coaching types:
- pace up
- settle down
- posture / form reminders
- cadence prompts
- motivation

## Closest prior work

Aaptiv and Nike Run Club combine coaching with music.
RockMyRun and Weav Run adapt music to pace.

Weav is probably the closest match because it also added adaptive voice coaching, but the gap still seems to be truly song-aware coaching timed to track structure.

## Open questions

- How much music-platform integration is needed for an MVP?
- Does this start as a full consumer app or as a feature layer on top of existing music + running workflows?
- Is the right initial wedge serious runners, casual runners, or guided interval training?
- Could this also work for walking, cycling, or workouts beyond running?

## Notes

Prior-work summary lives in `docs/running-music-coach-prior-work-2026-04-17.md` in the workspace.
