---
name: making-actaone-feature-trailers
description: Use when the user wants a feature trailer, promo, teaser, release video or LinkedIn clip for an actaOne feature, or wants to re-cut, re-render, extend or fix the existing actaOne trailers (trailer workspace with Blender, staging screen captures, synthesized music).
---

# actaOne Feature-Trailer

## Overview
Real staging UI, captured as screenshots and frame bursts, is turned into textures, flown through a dark 3D space in **Blender 5.2 headless**, cut hard on a 120 BPM beat to self-synthesized music, and encoded with ffmpeg. Everything lives in the **trailer workspace** (below: `<trailer>`; all paths in this skill are relative to it). Read `storyboard.md` for the look, `scripts/trailers/_template.py` for the shot skeleton. Blender MCP is **not** needed.

## Before the first step
The workspace is a local working folder, not a published repository, and this skill does not contain it. Origin, licensing and the check below: [references/sources.md](references/sources.md).

1. Locate `<trailer>`: ask the user, or confirm a known location contains `storyboard.md`, `scripts/trailer.sh` and `scripts/trailers/_template.py`. Without it, stop and report; do not rebuild the toolchain from this description.
2. Check the runtime the scripts assume, and report what is missing instead of installing it unasked:
   - Windows with Microsoft Edge at its default path and an SSO session for staging (`staging_window.py`).
   - cua-driver at `%LOCALAPPDATA%\Programs\Cua\cua-driver\bin\cua-driver.exe` (hard-coded in `cua.py` and `staging_window.py`).
   - Blender 5.2: `trailer.sh` uses `$BLENDER`, defaulting to the standard Windows install path. Set `BLENDER` for any other location.
   - `ffmpeg`, Python and Bash on `PATH`.
3. Capture opens windows on the user's desktop and drives staging with the user's SSO account; agree the capture session together with the story in step 1.

## Workflow
1. **Agree the story** with the user: hook (0–89), three feature beats, recap (690–749), outro (750–899). 30 s, 16:9 by default; 4:5 only on request. Write it into `storyboard.md`.
2. **Demo data:** fictional content only (pattern: `scripts/make_demo_docs.py`, Gemeinde *Musterstadt*). Existing staging demo area: Wissensbereich „Bauamt Musterstadt“.
3. **Capture** (`assets/footage/<name>/`):
   - `eval "$(python scripts/staging_window.py [url] | tail -1)"` opens a NEW Edge app window with the SSO session and exports `PID`/`WID` (all capture scripts need them). Never click in the user's own Edge windows. If a link opens a tab in the user's main window, close exactly that tab afterwards.
   - Stills and bursts: `python scripts/grab.py $WID out.png` / `… outdir --burst 600 --interval 0.12`. Start bursts `run_in_background`, then act.
   - Chat messages: `python scripts/chat_take.py "<text>" <name>/<take> --seconds 40 [--new-chat]` records a burst while it sets the text via accessibility and invokes „Nachricht senden“. It runs purely in the background. Typing is faked later in prep.
   - Other input: `python scripts/cua.py state [filter]`, then `python scripts/cua.py click '{"idx":N}'`, which is background and preferred. Use `"delivery_mode":"foreground"` only where Chromium ignores background input: drawing, some dialogs. **Foreground typing leaks keystrokes into whatever window the user focuses and drops characters**, so avoid it. Re-run `state` before every idx because indices go stale. Escape closes whole dialogs.
   - Pixel clicks use cua coordinates: `x_cua = x_grab·0.98`, `y_cua = (y_grab+30)·0.98`.
   - Heavy pages, such as the Design Studio, make `state` time out. `cua.py` retries with `max_elements`. If it still fails, click by pixel off `grab.py` screenshots. For native file dialogs, find the `#32770` window, then use `set_value` on `Dateiname:` and `click` on `Öffnen`. For inputs, paste via `clipboard_write` plus ctrl+a/ctrl+v, and tell the user that the clipboard was overwritten.
   - The local dev build (`localhost:3091` chat, `localhost:3000` admin) works too. Remove the devtools badges in prep with a `clean(im)` patch (see `prep_control.py`, `prep_studio.py`).
   - Hygiene: close the sidebar, since it shows the user's chat titles. Replace the greeting name with `greeting_patcher` (in `prep_lib`). Check live web or third-party content in the frame for foreign brands and personal data. Reopen the sidebar when done.
4. **Prep:** `scripts/prep_<name>.py` built on `prep_lib` (`still`, `seq`, `retime`, `first_change`, `first_match`, `typing_frames`, `ring`). Synthetic typing beats real typing. Sequences must be aligned to scene frames.
5. **Shots:** copy `_template.py` to `scripts/trailers/<name>.py`.
6. **QA loop:** `bash scripts/trailer.sh stills <name> 50,200,…`, look at `renders/final/stills_<name>_16x9.png`, then `trailer.sh preview <name>` (~25 min), show the user, then `trailer.sh final <name>` (~50 min, 3.3 s/frame). Music is regenerated from the shot list automatically.

## Rules that bite
| Rule | Why |
|---|---|
| Cuts and headline starts on multiples of 15 frames | music is 120 BPM, whooshes and hits land on cuts |
| Visible width ≥ 2.2 m on 4 m window panels | screenshots are 1598 px, closer framings go soft |
| Panel pixel y = screenshot y + 46 | browser bar added by `window()` |
| Headline continuing into the next shot: pass `f_in` before that shot's start | HUD objects render only during their own shot |
| Headline over white UI or paper → reframe or rely on backing | white on white disappears |
| Only one Blender render at a time | iGPU, parallel renders slow both |
| Chat endpoints only via the real browser, never by script | staging bans the account for 2 h (`NON_BROWSER_VIOLATION_SCORE`) |
| Knowledge-base questions say „nach unserer …“ | otherwise Luna does a web search |
| Sketchpad styles: open the editor on the base image, then `python scripts/style_loop.py <Stil> …` | the script applies every style to „Version 1“ and moves each download to `assets/images/style_<stil>.png` |

## Quick reference
```
eval "$(python scripts/staging_window.py | tail -1)"   # new capture window -> PID/WID
python scripts/prep_<name>.py                    # textures
bash scripts/trailer.sh stills|preview|final <name> [16x9|4x5]
bash scripts/trailer.sh music <name>
bash scripts/trailer.sh stills _selftest 5,120,300,500,820   # toolchain smoke test after changes
```
Outputs: `renders/final/actaone_<NAME>_<fmt>.mp4`. Existing trailers: `kb`, `sketch`, `control`, `studio`, `release`.

**Compilations (release trailer):** `scripts/trailers/release.py` sets `FRAME_END`, `DROP`, `RENDER_RANGES` (only the title and chapter cards are rendered) and `CLIPS` (source trailer, from, to, target). `scripts/assemble_release.py` copies the clip frames in after the card render, `trailer.sh final release` runs it automatically. It needs the finished PNG frames of the source trailers in `renders/<src>_16x9/`, so don't delete them. Keep clip offsets at multiples of 15. Report staging leftovers (demo areas, chats) and product bugs you notice while filming.
