# Build spec: ham exam trainers

Read this whole file before doing any work in a new session. It is the source of truth for how the
trainers look, behave, and are checked. If a decision changes, update this file in the same session.

## What this is

Radio-themed study games for the three US amateur radio license exams, built for Brooke (General
licensee, studying for Extra). One page per exam, used mostly on a phone. Each page is published two ways from the
same template: as a Claude artifact (Brooke's own copy, progress synced to her Claude account) and on the public
website (anyone with the link, installable to the home screen, works offline, progress saved on each device).

| Exam | Element | Pool in force | Exam size | Pass | Status |
|---|---|---|---|---|---|
| Technician | 2 | 2026-2030, Feb 19 2026 revision (July 1 2026 - June 30 2030), 409 questions | 35 | 26 | Live, notes done |
| General | 3 | 2023-2027, 6th errata Feb 4 2026 (through June 30 2027), 423 questions | 35 | 26 | Built, notes done, families in progress |
| Extra | 4 | 2024-2028, 4th errata Feb 4 2026 (through June 30 2028), 599 questions | 50 | 37 | Live, notes done |

Each exam draws exactly one question from every group (35 or 50 groups). Before building or republishing an
exam, search the web for newer NCVEC errata or withdrawn questions and update `sources/` if any exist.

## The study loop (Brooke's method; don't change it without asking)

1. Pick a band (subelement). First run = straight practice test of every question in it, no notes shown.
2. Signal report (debrief) after each run: every miss with the wrong pick, the right answer, and its Elmer's note.
3. Repeat runs: on a miss, a "Why? Show the note" button opens the Elmer's note.
4. Readiness = share of the band's questions answered right the last time they were seen. Cleared at 80%.
5. Mock exam (VE session): one random question per group, no feedback until the end, pass line as above.
6. S-meter on the home screen: needle = projected exam score (sum of per-group readiness); S9 = pass line;
   pass odds = Poisson-binomial over groups.
7. Answer order is shuffled on every showing.

## Elmer's notes

One per question, in `exams/<exam>/notes/*.json` as `{"QID": "note"}`. Rules:
- Say why the correct answer is right in 1-2 short sentences. Add a memory hook only if it truly helps.
- Math questions show the arithmetic with the real numbers from the question.
- Figure questions say how to find the answer on the figure (what the symbol or point looks like).
- Plain text only (no HTML, no double quotes). Pitch: Technician = newcomer; General and Extra = more technical.
- Never state anything the pool's answer key contradicts. Run `tools/pool.py check` after writing.

## Family pages ("Still confused?") — the current project

Some questions form families: several questions test one idea from different angles, and the wrong answers
pull from the neighboring idea (series vs. parallel, capacitor vs. inductor, which propagation when, formulas).
Each family gets an interactive learning page.

**Wiring in the app**
- A question in a family shows a "Still confused?" button under its Elmer's note (in runs and in the debrief).
- The button opens the family page (hash route `#family-<id>`, back returns to where you were).
- The page ends with "Drill these N questions": a run of exactly the family's questions, using the normal loop
  ("Why? Show the note" on misses). Its runs are logged in `P.runs` under the key `family-<id>`.
- The page opens over the current view and back returns to the exact spot (same answered question, same debrief).
- The home screen lists every published family page under "Still confused? pages" (deep links don't reach the page
  inside the Claude artifact frame, so this is the way in outside a run).
- Only finished family pages are published: `tools/site.py build` copies each `families/<exam>/<id>.json` into
  `exams/<exam>/site/families/` and writes a site `_index.json` listing just those. The button appears only for them.
- Each exam has `families/<exam>/_index.json` listing families and their question IDs. A question may belong to
  at most two families. Questions not in any family get no button.

**Scope rule (Brooke's, strict)**: a family page for an exam contains only what that exam's pool tests. No
extra theory, no content from another exam's pool. If a fact isn't needed to answer one of that exam's
questions, it doesn't go on the page.

**Reuse across exams**: a family is one concept with a layer per exam, stored separately:
`families/technician/<id>.json`, `families/general/<id>.json`, `families/extra/<id>.json`. A later exam may
reuse an earlier layer's wording or interactive widget, but its layer is written and checked against its own pool.
Build order: all Technician families first, then the General site and its families, then Extra families.

**What every family page has, in this order**
1. Title and a one-line "the idea" statement.
2. The core rule, formula, or map, shown big.
3. One interactive piece that makes the idea physical (see widget list). This is the heart of the page.
4. Side-by-side comparison of the look-alike terms (when the family has look-alikes).
5. "Traps the exam sets": the specific wrong answers the pool uses, each with one line on why it's wrong.
6. Every question in the family: question, correct answer, and its Elmer's note (collapsed by default).
7. "Drill these N questions" button.

**Family file format** (`families/<exam>/<id>.json`)
```json
{
  "id": "series-vs-parallel",
  "exam": "technician",
  "title": "Series vs. parallel",
  "idea": "Series = one path, same current. Parallel = side by side, same voltage.",
  "core": {"type": "rule-table", "rows": [["", "Series", "Parallel"], ["Same everywhere", "Current", "Voltage"]]},
  "widget": {"type": "circuit-toggle", "config": {}},
  "compare": [{"term": "Voltmeter", "how": "In parallel, across the part"}, {"term": "Ammeter", "how": "In series, in the path"}],
  "traps": [{"q": "T7D03", "wrong": "In parallel", "why": "Current must flow through the meter, so it goes in series."}],
  "questions": ["T5D13", "T5D14", "T7D02", "T7D03", "T0A08", "T6D11"]
}
```
`questions` must match `_index.json`. Every `traps[].wrong` must be an actual wrong answer of that question.
`compare` is optional. `tools/site.py check <exam>` checks ids, `_index.json` agreement, the two-family limit and traps.

**Core types** (`core.type`): `rule-table` (`rows`, first row is the header), `formula` (`text` shown big, optional
`lines` under it), `list` (`items` as `[term, meaning]` pairs). Add new types to `coreHtml` in `app/template.html`.

**Widget types** (build each once as a reusable component; add new types here when needed)
- `formula-triangle`: E/I/R or P/I/E triangle; tap the unknown, enter two values, see the working.
- `calculator`: sliders or inputs with live result and the working shown (wavelength, battery hours, dB).
- `ladder`: an ordered scale to tap through (prefixes, bandwidths, frequency ranges, dB steps).
- `sort-bins`: drag or tap cards into two or three bins (series/parallel, capacitor/inductor, RACES/ARES).
- `match`: connect terms to definitions or symbols to names.
- `scenario`: pick conditions (time of day, season, sunspots, band) and see which propagation or answer applies.
- `band-chart`: interactive band/segment map with privileges, power, and modes.
- `figure-explorer`: tap the numbered parts of a pool figure to reveal each name and its job.
- `circuit-toggle`: small animated circuit that switches between two arrangements.
- `power-wheel`: P, E, I, R wheel; type any two, the formula for each of the others lights up (presets: `vals` with two of P/E/I/R).
- `sine-wave`: a sine wave sized by slider or by typing peak, peak-to-peak, RMS or watts; shows all three voltages and PEP into a load (presets: `kind` pk/pp/rms/w, `v`, optional `ohms`, `carrier`).
- `s-meter`: an S meter with two needles; first reading plus a dB change gives the power ratio (presets: `from` in dB relative to S9, `d`).
- `combiner`: resistors, inductors or capacitors drawn in series or parallel with the total worked out (presets: `kind` R/L/C, `mode`, `parts` as [value, prefix]).
- `transformer`: two windings with turns sliders; voltage, current (wire thickness) and impedance ratios, feed from either side, impedance matching (presets: `np`, `ns`, `vp`, optional `flip`, `zp`/`zs`).
Brooke prefers hands-on widgets (sliders, live graphs, meters, simulators) to match, sort or text quizzes: use those only when nothing in
the idea can be varied, and say why. Widgets must work by tap on a 360px-wide screen, with 44px targets and no hover-only behavior.
Every widget ties in the pool: `config.presets` lists the family's questions the widget can work, shown as "Try a
question from the pool" chips. A chip shows the question and sets the widget up for it: formula and calculator
values, a scenario situation (and its settings), a band and item, a circuit arrangement, a figure part (presets
come from each part's `q`), a sort card dealt next, or one side of a match pair selected (`from: "r"` selects the
answer side, for questions that give the description and ask for the term). Use a question only when the widget
actually works it; `tools/site.py check` checks that every preset is a family question and points at something.
Each widget is a function in the `WIDGETS` registry in `app/template.html`: `WIDGETS[type](el, config, family)` fills
the card `el`. A page whose widget type isn't built yet shows no widget card.

## Look and feel

Radio front panel and logbook. Keep it consistent with the live pages (copy their CSS variables):
- Ground panel grey-green `#e6e9e1` (dark `#111413`); cards `#fcfcf9` (dark `#1a1e1c`); ink `#151918`.
- Signal red `#c4301c` for the needle, pass line, and Elmer's note accents; dial blue `#1d4e8f` for actions;
  green `#257238` only for correct answers and cleared bands.
- Type: Barlow Condensed (500-700) for titles, numbers, and panel legends; Barlow for body. Sentence case.
- Elmer's notes and family "traps" use the note style: red left rule, warm `--face` background.
- One column, max 720px. Must read well in light and dark mode. No emoji.

## Code layout

- `app/template.html` = the one page shared by every exam. Edit this, never a site's `index.html`.
- `exams/<exam>/exam.json` = that exam's settings: `title`, `heading`, `element` line, `source` line, band `letter`,
  exam size `ex`, `pass` line, storage key `ls`, and call sign box `callSize`/`callWidth`.
- `exams/<exam>/site/` = the published files: `index.html` (generated), `pool.json`, `hooks.json` (notes), `fig/*.png`,
  and `families/*.json` (generated). The page fetches its JSON by relative path.
- `tools/site.py build <exam>` writes the site's `index.html` and `families/` from the template, `exam.json` and
  `families/<exam>/`. Run it after any change to those, before testing and publishing.
- `exams/<exam>/raw/` = upstream question JSON (github.com/russolsen/ham_radio_question_pool).
- `exams/<exam>/notes/` = Elmer's note sources, merged into `site/hooks.json` by `tools/pool.py merge`.
- `sources/` = official NCVEC pool PDFs (public domain). The PDF is the authority; the JSON is checked against it.
- `tools/pool.py` = build/verify pool, list questions, merge and check notes.
- `tools/test_app.py` = headless walk-through of an exam site (first run, debrief, repeat run with note, mock exam,
  and the family page flow using a test family). Set `CHROME=` to a Chromium binary if not at /usr/bin/google-chrome.
- Never change a live exam's `ls` key or the db path, or saved progress is lost.
- `tools/web.py build` writes `web/` (the public website) from each exam's built `site/`: a hub page, shared fonts
  (`app/web/fonts/`, self-hosted so nothing loads from Google), and `web/<exam>/` with a manifest, service worker
  (offline copy of every file; its version changes when any file does) and icons. Exams on the website are listed in
  `WEB_EXAMS` in `tools/web.py`; each needs `short` in `exam.json` (the name under the home screen icon). Commit `web/`:
  the host serves it as is, with no build step. Never hand-edit it.
- The template's `<!--fonts-->`, `<!--web-head-->` and `<!--web-body-->` markers are filled only by the web build, which
  also sets `CFG.web` (shows the "Put it on your home screen" card). The artifact build leaves them as comments.
- `tools/test_web.py` = headless check of `web/`: hub, manifest and icons, service worker, fonts, then offline: opens,
  answers, family page with figures, progress kept across a reload. `SITE=web/<exam> tools/test_app.py <exam>` walks the
  web build with the normal test.

## Saved progress

Each artifact declares `db` and `user`. Progress is one document per person at
`data/users/<id>/progress` (private to them), mirrored to localStorage, plus a copy/paste backup code.
Declared rules: root read/write `owner`; `data/users/{self}` read/write `interact`.
On the website there is no account: progress lives only in that browser's localStorage under the exam's `ls` key
(the page asks the browser to keep it, `navigator.storage.persist()`), and the backup code moves it between devices.
On iPhone the home screen app and Safari keep separate storage, so the install card says to install first.

## Checks before publishing (all required)

1. `python3 tools/pool.py build <exam>`: zero mismatches against the PDF.
2. `python3 tools/pool.py merge <exam>` and `check <exam>`: every question has a note; review each flag by hand.
3. For family pages: `python3 tools/site.py check <exam>` passes (every question ID exists; every trap's `wrong` is a real wrong answer for that question);
   every formula result recomputed in code; scope rule re-read against the family's questions.
4. `python3 tools/site.py build <exam>`, then `python3 tools/test_app.py <exam>`: no page errors; look at the screenshots at 390px wide.
5. Publish with `publish_files` (mode `patch`) to the slug in `ARTIFACTS.md`, then update `TRACKER.md`.
6. Website: `python3 tools/web.py build`, then `python3 tools/test_web.py` (all checks pass), and commit `web/`.
   Merging to `main` updates the public site; every PR branch gets its own preview link from Cloudflare Pages.

## Session workflow

1. Read `SPEC.md`, `TRACKER.md`, `ARTIFACTS.md`.
2. Take the next batch (about 5 families, or one setup task) from `TRACKER.md`.
3. Build, run the checks, publish, mark done in `TRACKER.md`, commit and push.
4. End with a short note in `TRACKER.md` under "Log": what was done and anything the next session must know.
