# Tracker

Status: `todo`, `doing`, `done`. Update this file at the end of every session, then commit and push.

## Setup tasks

| # | Task | Status |
|---|---|---|
| S1 | Merge the Technician and Extra `index.html` into one template plus per-exam config; keep each live `LS` key and db path; retest both and republish | done |
| S2 | Add family support to the app: `#family-<id>` route, "Still confused?" button, family page renderer, "Drill these N" | done |
| S3 | Build the reusable widgets listed in SPEC.md as they're first needed | doing (built: `formula-triangle`, `ladder`, `calculator` with `db` and `wavelength`, `circuit-toggle`, `sort-bins`, `match`, `figure-explorer`, `scenario`, calc `multipath`, `band-chart`) |

## Technician families (34)

257 of 409 questions are in a family. Question lists are in `families/technician/_index.json`.

| # | Family | Category | Questions | Status |
|---|---|---|---|---|
| 1 | Ohm's law (E = I x R) (`ohms-law`) | Math and formulas | 12 | done |
| 2 | Power and batteries (P = I x E) (`power-and-batteries`) | Math and formulas | 6 | done |
| 3 | Metric prefixes and unit abbreviations (`metric-prefixes`) | Math and formulas | 12 | done |
| 4 | Decibels (`decibels`) | Math and formulas | 3 | done |
| 5 | Wavelength and frequency (`wavelength-frequency`) | Math and formulas | 8 | done |
| 6 | Series vs. parallel (`series-vs-parallel`) | Commonly confused terms | 6 | done |
| 7 | Units and what they measure (`units`) | Commonly confused terms | 12 | done |
| 8 | Capacitor vs. inductor (`capacitor-vs-inductor`) | Commonly confused terms | 7 | done |
| 9 | Resistance vs. impedance (`resistance-vs-impedance`) | Commonly confused terms | 3 | done |
| 10 | What each component does (`component-jobs`) | Commonly confused terms | 8 | done |
| 11 | Transistor and diode lead names (`lead-names`) | Commonly confused terms | 5 | done |
| 12 | Schematic symbols (Figures T-1, T-2, T-3) (`schematic-symbols`) | Commonly confused terms | 12 | done |
| 13 | Radio building blocks (`radio-building-blocks`) | Commonly confused terms | 7 | done |
| 14 | Which propagation, when (`which-propagation`) | Propagation | 8 | done |
| 15 | Multipath and fading (`multipath-fading`) | Propagation | 4 | done |
| 16 | Polarization (`polarization`) | Propagation | 7 | done |
| 17 | What weather and terrain do (`weather-terrain`) | Propagation | 3 | done |
| 18 | HF vs. VHF vs. UHF (`hf-vhf-uhf`) | Propagation | 7 | done |
| 19 | Technician privileges map (`privileges-map`) | Rules and numbers to memorize | 12 | done |
| 20 | The numbers to memorize (`the-numbers`) | Rules and numbers to memorize | 9 | done |
| 21 | Who's responsible (`whos-responsible`) | Rules and numbers to memorize | 12 | done |
| 22 | Local vs. remote vs. automatic control (`control-types`) | Rules and numbers to memorize | 5 | done |
| 23 | "Only when..." exceptions (`only-when-exceptions`) | Rules and numbers to memorize | 8 | done |
| 24 | RACES vs. ARES (`races-vs-ares`) | Rules and numbers to memorize | 5 | done |
| 25 | Bandwidth ladder (`bandwidth-ladder`) | Operating and equipment | 7 | done |
| 26 | Repeater alphabet soup (`repeater-alphabet-soup`) | Operating and equipment | 10 | done |
| 27 | Internet linking (`internet-linking`) | Operating and equipment | 7 | done |
| 28 | "You sound bad" fixes (`you-sound-bad`) | Operating and equipment | 6 | done |
| 29 | SWR family (`swr`) | Operating and equipment | 8 | done |
| 30 | Interference: whose fix is it? (`interference-whose-fix`) | Operating and equipment | 7 | done |
| 31 | Coax and connectors (`coax-connectors`) | Operating and equipment | 10 | done |
| 32 | Antenna length rules (`antenna-length`) | Operating and equipment | 5 | done |
| 33 | Grounding and lightning (`grounding-lightning`) | Safety | 8 | done |
| 34 | RF exposure (`rf-exposure`) | Safety | 13 | done |

## General

| # | Task | Status |
|---|---|---|
| G1 | Check for newer General pool errata; `tools/pool.py build general` (fix the subelement name capitalization, e.g. "rf" to "RF") | todo |
| G2 | Write Elmer's notes for all 423 questions; `merge` and `check` | todo |
| G3 | Build and publish the General site (35 questions, pass 26); add to ARTIFACTS.md | todo |
| G4 | Map General families into `families/general/_index.json` (reuse Technician family ids where the concept matches) | todo |
| G5 | Build General family pages | todo |

## Extra

| # | Task | Status |
|---|---|---|
| X1 | Map Extra families into `families/extra/_index.json` | todo |
| X2 | Build Extra family pages | todo |

## Log

- 2026-11-18 (Technician families 31-34, pool questions in every widget): Coax and connectors, antenna length, grounding and lightning, RF exposure. All 34 Technician families are now written. Brooke noticed only the first pages had "Try a question from the pool" chips, so every widget type now takes `presets` (see SPEC.md), every family has them, and `match` can be started from either side. Questions left out of a widget are ones it doesn't work (for example a definition question whose answer is the term itself, or instrument questions on the units page). Families 26-30 were republished to Technician on 2026-11-18 (v9). The template changed, so republish Extra too after this merges. Next: X1, map the Extra families.
- 2026-11-18 (Technician families 26-30): Repeater alphabet soup, internet linking, "you sound bad" fixes, SWR, interference: whose fix is it? No new widgets: `match` (repeater terms, bad-audio reports), `scenario` (internet linking, SWR) and `sort-bins` (where the interference fix goes). Families 21-25 were republished to Technician on 2026-11-18 (v8). Next batch: families 31-34 (coax and connectors, antenna length, grounding and lightning, RF exposure).
- 2026-11-18 (Technician families 21-25): Who's responsible, control types, only-when exceptions, RACES vs. ARES, bandwidth ladder. `match` now accepts repeated answers (matches by text); `band-chart` items take `show` (list text) and bands take `title`. Control types: the pool never asks about local control, so the page covers remote, automatic, control point and auxiliary only (scope rule). Families 16-20 were republished to Technician on 2026-11-18 (v7). Next batch: families 26-30 (repeater alphabet soup, internet linking, you sound bad, SWR, interference).
- 2026-11-18 (Technician families 16-20): Polarization, weather and terrain, HF vs. VHF vs. UHF, privileges map, the numbers. New widget: `band-chart` (bands drawn to scale, linear or log, with segments and marked frequencies; details on tap). Only edges and spots the pool tests are drawn. Families 11-15 were republished to Technician on 2026-11-18 (v6). Next batch: families 21-25 (who's responsible, control types, only-when exceptions, RACES vs. ARES, bandwidth ladder).
- 2026-11-18 (Technician families 11-15): Lead names, schematic symbols, radio building blocks, which propagation when, multipath and fading. New widgets: `figure-explorer` (numbered buttons under a pool figure, a ring marks the part; ring positions are percent of the 1800x1200 figure), `scenario` (situations, optional dims with first-match rules), calc `multipath` (illustration only, no real distances). Families 6-10 were republished to Technician on 2026-11-18 (v5). Next batch: families 16-20 (polarization, weather and terrain, HF vs. VHF vs. UHF, privileges map needs `band-chart`, the numbers).
- 2026-11-18 (Technician families 6-10): Series vs. parallel, units, capacitor vs. inductor, resistance vs. impedance, what each component does. New widgets: `circuit-toggle` (series/parallel with ammeter or voltmeter; text from config), `sort-bins` (one card at a time, tap the bin), `match` (tap a term, then its partner). Families 1-5 were republished to Technician on 2026-11-18 (v4), and PR #2 was closed. Flow now: build, publish a preview copy (Technician Trainer Preview, https://claude.ai/artifact/JVa74CyW5j9ktfCoZp2u1o, no db), Brooke tries it, merges, then republish the real one. Next batch: families 11-15 (lead names, schematic symbols need `figure-explorer`, radio building blocks, which propagation needs `scenario`, multipath).
- 2026-11-17 (Technician families 1-5): Ohm's law, power and batteries, metric prefixes, decibels, wavelength and frequency pages written. New widgets in `app/template.html`: `formula-triangle` (tap the unknown, fill two values, see the working), `ladder` (prefix converter; every rung shows the same amount), `calculator` (named calcs in `CALCS`: `db`, `wavelength`). Widgets take `presets` of pool questions as chips. Every preset result was checked against the pool's correct answer headless. `tools/test_app.py` now also opens every published family page and clicks each preset chip. Republish Technician after the PR merges. Next batch: families 6-10 (series vs. parallel needs `circuit-toggle`, units needs `match` or `sort-bins`).
- 2026-11-17 (S1, S2): Both exam pages now come from `app/template.html` plus `exams/<exam>/exam.json`; run `tools/site.py build <exam>` after any change and never hand-edit a site's `index.html`. Storage keys and db path unchanged. Family support is in: "Still confused?" button under notes (runs and debriefs), family page over the current view with back returning to the same spot, deep links `#family-<id>`, "Drill these N". Pages are published only once `families/<exam>/<id>.json` exists; `tools/site.py check <exam>` validates them. No widgets exist yet (S3): the first family session builds its widget into the `WIDGETS` registry. Both sites tested headless with no page errors. Both artifacts republished after the merge (Technician v3, Extra v4); capabilities and saved progress carried over.
- 2026-11-17: Repo created from the first session. Technician and Extra sites live with notes for every question. All three pools verified word for word against the NCVEC PDFs. Technician family list drafted and approved by Brooke (34 families).
