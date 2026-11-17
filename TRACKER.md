# Tracker

Status: `todo`, `doing`, `done`. Update this file at the end of every session, then commit and push.

## Setup tasks

| # | Task | Status |
|---|---|---|
| S1 | Merge the Technician and Extra `index.html` into one template plus per-exam config; keep each live `LS` key and db path; retest both and republish | todo |
| S2 | Add family support to the app: `#family-<id>` route, "Still confused?" button, family page renderer, "Drill these N" | todo |
| S3 | Build the reusable widgets listed in SPEC.md as they're first needed | todo |

## Technician families (34)

257 of 409 questions are in a family. Question lists are in `families/technician/_index.json`.

| # | Family | Category | Questions | Status |
|---|---|---|---|---|
| 1 | Ohm's law (E = I x R) (`ohms-law`) | Math and formulas | 12 | todo |
| 2 | Power and batteries (P = I x E) (`power-and-batteries`) | Math and formulas | 6 | todo |
| 3 | Metric prefixes and unit abbreviations (`metric-prefixes`) | Math and formulas | 12 | todo |
| 4 | Decibels (`decibels`) | Math and formulas | 3 | todo |
| 5 | Wavelength and frequency (`wavelength-frequency`) | Math and formulas | 8 | todo |
| 6 | Series vs. parallel (`series-vs-parallel`) | Commonly confused terms | 6 | todo |
| 7 | Units and what they measure (`units`) | Commonly confused terms | 12 | todo |
| 8 | Capacitor vs. inductor (`capacitor-vs-inductor`) | Commonly confused terms | 7 | todo |
| 9 | Resistance vs. impedance (`resistance-vs-impedance`) | Commonly confused terms | 3 | todo |
| 10 | What each component does (`component-jobs`) | Commonly confused terms | 8 | todo |
| 11 | Transistor and diode lead names (`lead-names`) | Commonly confused terms | 5 | todo |
| 12 | Schematic symbols (Figures T-1, T-2, T-3) (`schematic-symbols`) | Commonly confused terms | 12 | todo |
| 13 | Radio building blocks (`radio-building-blocks`) | Commonly confused terms | 7 | todo |
| 14 | Which propagation, when (`which-propagation`) | Propagation | 8 | todo |
| 15 | Multipath and fading (`multipath-fading`) | Propagation | 4 | todo |
| 16 | Polarization (`polarization`) | Propagation | 7 | todo |
| 17 | What weather and terrain do (`weather-terrain`) | Propagation | 3 | todo |
| 18 | HF vs. VHF vs. UHF (`hf-vhf-uhf`) | Propagation | 7 | todo |
| 19 | Technician privileges map (`privileges-map`) | Rules and numbers to memorize | 12 | todo |
| 20 | The numbers to memorize (`the-numbers`) | Rules and numbers to memorize | 9 | todo |
| 21 | Who's responsible (`whos-responsible`) | Rules and numbers to memorize | 12 | todo |
| 22 | Local vs. remote vs. automatic control (`control-types`) | Rules and numbers to memorize | 5 | todo |
| 23 | "Only when..." exceptions (`only-when-exceptions`) | Rules and numbers to memorize | 8 | todo |
| 24 | RACES vs. ARES (`races-vs-ares`) | Rules and numbers to memorize | 5 | todo |
| 25 | Bandwidth ladder (`bandwidth-ladder`) | Operating and equipment | 7 | todo |
| 26 | Repeater alphabet soup (`repeater-alphabet-soup`) | Operating and equipment | 10 | todo |
| 27 | Internet linking (`internet-linking`) | Operating and equipment | 7 | todo |
| 28 | "You sound bad" fixes (`you-sound-bad`) | Operating and equipment | 6 | todo |
| 29 | SWR family (`swr`) | Operating and equipment | 8 | todo |
| 30 | Interference: whose fix is it? (`interference-whose-fix`) | Operating and equipment | 7 | todo |
| 31 | Coax and connectors (`coax-connectors`) | Operating and equipment | 10 | todo |
| 32 | Antenna length rules (`antenna-length`) | Operating and equipment | 5 | todo |
| 33 | Grounding and lightning (`grounding-lightning`) | Safety | 8 | todo |
| 34 | RF exposure (`rf-exposure`) | Safety | 13 | todo |

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

- 2026-11-17: Repo created from the first session. Technician and Extra sites live with notes for every question. All three pools verified word for word against the NCVEC PDFs. Technician family list drafted and approved by Brooke (34 families).
