# Play Clipper — Product & Roadmap

## Product
Watch any game play by play without scrubbing a 3.5-hr video — with insights the stat line never shows.
- **Users:** super fans + amateur social analysts.
- **Unique:** drive-by-drive layout; instant search to any play; software-charted insights (no fan charting).
- **Vantage point:** pick team + unit (e.g. Miami Defense) → every play shows only the insights relevant to that view.
- **Platform:** web + mobile web. Native later.
- **Video:** YouTube (built-in search + downloader) and ESPN login. No user uploads. All-22 as a second angle when available. Licensing needed before paid launch.
- **Business:** freemium. Free = all games, play browser, ESPN tags, search, clips (ads). Team pass ~$5–8/mo = AI insights, swing plays, clean sharing, discussion, no ads. All-access ~$12–15/mo = every P4 team. Betting angle TBD.

## Phase 0 — Clipping near flawless (Miami)
### New clip flow (replaces motion-first matcher + 16 patch rules)
1. Read the scoreboard every second, whole game: quarter, clock, down & distance, flag.
2. Find each ESPN play there: the moment the scoreboard shows its quarter + clock + down & distance.
3. Snap = the moment the clock starts or the down changes; back up to the last wide field shot before it.
4. Confirm the ball was actually snapped (on video). Not snapped (false start, delay) or snapped with a flag (scoreboard shows FLAG) → keep recording until the play is over.
5. Special cases only: kicks, touchdowns (ESPN clock = after the play), penalties.
6. Answer key per game (each play's real snap, confirmed once) → every change scored as % correct per game.

- Flag-this-clip button → fix each wrong clip
- Resolve flagged: Q2 0:18, Q2 0:00, Q4 14:52; Clemson clips moved by snap check
- Accuracy target: every play correct, snap within ~0.5s
- Answer key + per-game score: correct snap per play for all games; every rule change reports % correct per game. Re-check only affected plays (now 5–6 min per full run).
- Pitt: 24 flagged — 8 kicks not found, 8 plays not found, 6 D&D mismatches, 2 stacked (Q2 1:48/1:40, Q3 13:00 TD on next play)
- Done: thumbnails no longer show wrong frames on reload; screenshot download (paused + spotlight); zoom pan locked while paused + spotlit

### Accuracy log (per game, first scan → are rules converging?)
Flagged = self-check flags / clips. Wrong = clips user found wrong (flagged or not). New rules = rules added because of this game.
| Game | Clips | Flagged | Wrong | New rules |
|---|---|---|---|---|
| FSU | 176 | — (not logged) | 9 | 1–3, 5–11 |
| Clemson | — | — | — | — |
| Pitt | 177 | 34 (19%) → 43 after wiped fixes → 24 (14%) | 5 of first 7 + Q3/Q4 drift (scoreboard check: 103/139 ok before fix) | 6 (codes 2–6 letters), 12 (scoreboard D&D) |

Why clips failed. Cause = root category; repeat counts show what to generalize.
| Game | Play | What was wrong | Cause | Rule |
|---|---|---|---|---|
| FSU | 3 | Started after the handoff | Lead-in: camera cut too close to snap | 1 |
| FSU | 6 | Opened on QB close-up | Lead-in: non-field shot | 7 |
| FSU | 15 | Sat on extra point | Clock: frozen, not a live play | 2 |
| FSU | 16 | Replay of previous play | Replay mistaken for play | 3 |
| FSU | 20 | Sat on frozen 0:44 | Clock: already running pre-snap | 2 |
| FSU | 25 | False start showed +3 | ESPN text: team code | 6 |
| FSU | 29/30 | Same clip twice | Overlap: snap before previous | 8 |
| FSU | 56 | Not found | Clock: back-solve from running clock | 10 |
| FSU | 73 | Opened on kicker graphic | Broadcast hid snap (unfixable) | 7, 11 |
| Pitt | 1 | False start showed +5 | ESPN text: team code (CANES, PIT) | 6 |
| Pitt | 4 | Punt clip before the snap | Clock: frozen, not a live play | 12 |
| Pitt | 6–9+ | Each clip showed the next play | Missed snap after false start → whole drive shifted | 12 |
| Pitt | Q3/Q4 | Clips 30–130s off ESPN clock | Matcher drift; no scoreboard cross-check | 12 |
| Pitt | Off 56 | Clip ended before the snap | Clock: restarted on ready after false start; D&D matched so check passed | 12 |
| Pitt | — | Scoreboard reads from wrong moment | Bug: two checks seeking one video at once | code fix |
| Pitt | — | Fixes ran on no motion data | Bug: empty cached sample list treated as loaded | code fix |

Cause totals: Clock 4 · Shift/drift 2 · Lead-in 2 · ESPN text 2 · Replay 1 · Overlap 1 · Broadcast 1

## Phase 1 — UX right with Miami
Constraint: on a laptop, everything (header, video, timeline) fits in one view with no scrolling.
- Header redesign: there's no header now (old scoreboard header hidden); needs game identity + score
- Game switching: faster UX than the current "Choose a game" list
- Game picker + Offense/Defense/Special teams switch: both look awkward and sit in odd places — redesign their look and placement to follow established UX patterns (study how good sports/video apps handle game + view switching)
- Above/below the video: shrink the bars, ideally to one line each, to free up vertical space
- Timeline: fix it + make sure it has everything (drive time, results, key plays…); possibly shorter vertically to fit
- Insights panel: overarching game stats (see backlog in CLAUDE.md for the first stats)
- Team/unit tabs (wireframe 2a): All | Offense | Defense | Special teams
- Search: find plays and pull clips from this game or any other game. Plain-language queries, e.g. "all clips where Malachi Toney catches a pass", "every false start on S.Alofaituli"
- Tag filters (wire up existing tags)
- Game loading UX: users never upload games (games get pulled in automatically later), so upload is internal/admin only. Design what a game looks like while it is being loaded/scanned.
- Swing plays (ESPN win probability)
- Mobile web layout
- YouTube search + downloader; ESPN source

## Phase 2 — Insights
- PFF import: pressures, PBUs, missed tackles, blocks, grades
- AI video reads, checked against PFF
- Penalty detail beyond ESPN category (ref audio / flag banner OCR)
- Player tracking (SAM 2) + jersey OCR

## Phase 3 — Social
- Share card (auto overlay, user-editable)
- Discussion pinned to play + frame. Open question: probably a slide-out panel, but it would cover the video and timeline. Decide where it lives (overlay vs push layout vs docked) without breaking the one-screen laptop layout.

## Phase 4 — Scale + money
- More teams → all P4
- Accounts, team pass / all-access, ads
- Licensing; All-22; native app

## Insight catalog (E = ESPN has it)
- **Big plays:** sacks E, INTs E, forced fumbles E, recoveries E, PBUs (partial E), tipped balls, blocked kicks E, safeties E, defensive TDs E
- **QB:** runs E, scrambles vs designed, time to throw, holding ball too long, throws into coverage, throwaways, off-target, RPO read, hot reads
- **Receivers:** drops, contested catches, YAC, separation, route, target depth
- **Blocking:** missed blocks, key blocks, pressures allowed, scheme (zone/gap), pancakes, stunts, blitz pickup
- **Defense:** pressures, missed tackles, bad angles, TFLs (partial E), run fits, yards after contact, coverage busts
- **Scheme:** coverage (Cover 1…), man/zone, blitz, sim pressure, box count, personnel, formation, motion/shifts, WR stack, jumbo, pitch sweep, play-action, screens, trick plays
- **Special teams:** return yds E, coverage tackles, fair catches E, hang time, kick location
- **Situational:** 4th-down calls E, red zone, explosives E, win-prob swing E
