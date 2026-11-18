# Tracker

Status: `todo`, `doing`, `done`. Update this file at the end of every session, then commit and push.

## Setup tasks

| # | Task | Status |
|---|---|---|
| S1 | Merge the Technician and Extra `index.html` into one template plus per-exam config; keep each live `LS` key and db path; retest both and republish | done |
| S2 | Add family support to the app: `#family-<id>` route, "Still confused?" button, family page renderer, "Drill these N" | done |
| S3 | Build the reusable widgets listed in SPEC.md as they're first needed | doing (built: `formula-triangle`, `ladder`, `calculator` with `db` and `wavelength`, `circuit-toggle`, `sort-bins`, `match`, `figure-explorer`, `scenario`, calc `multipath`, `band-chart`, `power-wheel`, `sine-wave`, `s-meter`, `combiner`, `transformer`, `reactance-graph`, `antenna-ruler`, `fm-spectrum`, `link-budget`, `mixer`, `two-tone`, `sun-timeline`, `sun-indices`, `ionosphere`) |
| S4 | Public website: Technician as an installable offline web app (PWA) on Cloudflare Pages, progress saved on each device; General and Extra added later via `WEB_EXAMS` | doing (built and tested; waiting on Brooke to connect Cloudflare) |

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
| G1 | Check for newer General pool errata; `tools/pool.py build general` (fix the subelement name capitalization, e.g. "rf" to "RF") | done |
| G2 | Write Elmer's notes for all 423 questions; `merge` and `check` | done |
| G3 | Build and publish the General site (35 questions, pass 26); add to ARTIFACTS.md | doing (built and tested; publish the real artifact after the first PR merges) |
| G4 | Map General families into `families/general/_index.json` (reuse Technician family ids where the concept matches) | done |
| G5 | Build General family pages | doing |

### General families (53)

378 of 423 questions are in a family. Question lists, and a one-line plan for each family's interaction, are in `families/general/_index.json`.
Brooke's rule for General: every family gets a hands-on interaction (slider, live graph, meter, simulator). A match, sort or
plain scenario only where nothing can be varied, and the reason is recorded (CW codes, part types, on-air etiquette).

| # | Family | Category | Questions | Interaction | Status |
|---|---|---|---|---|---|
| 1 | Power from any two values (P, E, I, R) (`power-formulas`) | Math and formulas | 4 | Power wheel | done |
| 2 | RMS, peak, peak-to-peak and PEP (`rms-peak-pep`) | Math and formulas | 9 | Live sine wave | done |
| 3 | Decibels and the S meter (`decibels`) | Math and formulas | 6 | Working S meter | done |
| 4 | Resistors, capacitors and inductors in series and parallel (`combining-parts`) | Math and formulas | 10 | Parts bench | done |
| 5 | Transformers and turns ratio (`transformers`) | Math and formulas | 7 | Transformer | done |
| 6 | Reactance, impedance and resonance (`reactance-resonance`) | Math and formulas | 13 | Reactance graph | done |
| 7 | Antenna length (468 / f) (`antenna-length`) | Math and formulas | 5 | Antenna ruler | done |
| 8 | FM deviation and bandwidth (`fm-deviation`) | Math and formulas | 3 | FM spectrum and multiplier chain | done |
| 9 | Link budget and link margin (`link-budget`) | Math and formulas | 3 | Signal path in dB | done |
| 10 | Mixers, IF and image response (`mixers-images`) | Circuits | 7 | Mixer spectrum | done |
| 11 | Intermodulation and the two-tone test (`intermod`) | Circuits | 5 | Two tones on a spectrum | done |
| 12 | Sun to Earth: flares, CMEs and storms (`solar-weather`) | Propagation | 8 | Sun-to-Earth timeline | done |
| 13 | Sunspots, solar flux, K and A (`solar-indices`) | Propagation | 6 | Sunspot slider that opens and closes the high bands, and a K vs. A chart (3-hour bars vs. the daily average) | done |
| 14 | MUF, LUF and the usable window (`muf-luf`) | Propagation | 9 | Ionosphere cross-section | done |
| 15 | D, E and F regions (`ionosphere-regions`) | Propagation | 8 | Same cross-section with a day/night switch | done |
| 16 | Skip zone and scatter (`scatter`) | Propagation | 4 | Cross-section showing the skip zone, then the weak, fluttery scatter that leaks into it | todo |
| 17 | Short path vs. long path (`long-path`) | Propagation | 3 | Beam heading dial on an azimuthal map | todo |
| 18 | Which sideband, and where it sits (`sidebands`) | Operating | 13 | Band-edge tuner | todo |
| 19 | General privileges map (`privileges-map`) | Rules | 12 | Band chart (built for Technician) | todo |
| 20 | Power limits and 60 meters (`power-limits`) | Rules | 8 | Band chart of the HF bands with each band's power limit, the 30-meter 200 W exception and the 60-meter channel rules | todo |
| 21 | Beacons (`beacons`) | Rules | 6 | Band chart with the beacon frequencies and the 28.2 to 28.3 MHz automatic beacon window marked | todo |
| 22 | How wide is each signal (`signal-width`) | Operating | 8 | Spectrum view | todo |
| 23 | Mic gain, ALC and the speech processor (`speech-alc`) | Operating | 7 | Voice envelope on a scope | todo |
| 24 | AM, FM and PM: what changes (`modulation`) | Circuits | 7 | Modulation scope | todo |
| 25 | Receiver tools: notch, blanker, NR, attenuator (`receiver-tools`) | Operating | 6 | Receiver panel with a problem on the band (whistle, ignition pops, a blasting signal); switch on the right control and it clears | todo |
| 26 | The waterfall and FT8 (`waterfall-ft8`) | Digital modes | 8 | Live waterfall | todo |
| 27 | RTTY and FSK (`rtty-fsk`) | Digital modes | 6 | Two-tone FSK display | todo |
| 28 | PSK31, QPSK and Varicode (`psk`) | Digital modes | 4 | Phase wheel | todo |
| 29 | ARQ, NAK and error correction (`arq-fec`) | Digital modes | 6 | Packet exchange | todo |
| 30 | Winlink, gateways and mesh networks (`winlink-mesh`) | Digital modes | 7 | Network map | todo |
| 31 | CW: Q signals and prosigns (`cw-procedures`) | Operating | 12 | Match (pure vocabulary; nothing to calculate or move) | todo |
| 32 | On-air etiquette (`on-air`) | Operating | 9 | Scenario | todo |
| 33 | Rectifiers and power supplies (`rectifiers`) | Circuits | 8 | Rectifier scope | todo |
| 34 | Schematic symbols (Figure G7-1) (`schematic-symbols`) | Circuits | 5 | Figure explorer (built for Technician) on Figure G7-1 | todo |
| 35 | Amplifier classes and efficiency (`amp-classes`) | Circuits | 8 | Conduction viewer | todo |
| 36 | Digital logic: gates, counters, shift registers (`logic`) | Circuits | 5 | Logic bench | todo |
| 37 | Filter words: passband, cutoff, rejection (`filters`) | Circuits | 6 | Filter response curve | todo |
| 38 | SDR, I/Q and DDS (`sdr-iq`) | Circuits | 4 | Rotating I/Q phasor | todo |
| 39 | Diodes, transistors and tubes (`semiconductors`) | Components | 7 | Bias slider | todo |
| 40 | Capacitor, resistor and ferrite types (`parts-types`) | Components | 6 | Sort (these are look-alike part types with one fact each; nothing to slide) | todo |
| 41 | RF connectors (`connectors`) | Components | 4 | Frequency chart | todo |
| 42 | RF in the shack: grounds, bonding and chokes (`rfi-grounds`) | Station | 11 | Ground wire slider | todo |
| 43 | AC wiring, breakers and lightning (`ac-lightning`) | Safety | 9 | Breaker panel | todo |
| 44 | RF exposure (`rf-exposure`) | Safety | 12 | Time-averaging meter | todo |
| 45 | SWR, mismatch and line loss (`swr`) | Antennas and feed lines | 10 | Feed line simulator | todo |
| 46 | Feed line types and loss (`feed-lines`) | Antennas and feed lines | 4 | Line builder | todo |
| 47 | Feed point impedance: height, feed point, radials (`dipole-feed`) | Antennas and feed lines | 6 | Dipole lab | todo |
| 48 | Radiation patterns (`patterns`) | Antennas and feed lines | 8 | Pattern viewer | todo |
| 49 | Yagi design and stacking (`yagi`) | Antennas and feed lines | 8 | Yagi builder | todo |
| 50 | Short and loaded antennas (`short-antennas`) | Antennas and feed lines | 7 | Mobile whip | todo |
| 51 | Mobile, battery and solar power (`station-power`) | Station | 9 | Solar builder | todo |
| 52 | Exams, VEs and upgrades (`ve-licensing`) | Rules | 10 | Upgrade timeline | todo |
| 53 | Remote operation, third party and ITU regions (`remote-third-party`) | Rules | 10 | Scenario | todo |

## Extra

| # | Task | Status |
|---|---|---|
| X1 | Map Extra families into `families/extra/_index.json` | todo |
| X2 | Build Extra family pages | todo |

## Log

- 2026-11-18 (General batch 3, PR general-batch3): Intermodulation and the two-tone test, Sun to Earth, sunspots/flux/K/A, MUF/LUF, D/E/F regions. New widgets: `two-tone` (two audio tones into SSB with a drive slider; odd-order products grow beside them), `sun-timeline` (flare, CME, coronal hole or rotation on a log time slider, with band-condition tiles at Earth), `sun-indices` (sunspot slider sets solar flux and opens/closes bands 160-10 m; tappable 3-hour K bars give the A index), `ionosphere` (cross-section with frequency, takeoff angle and day/night/flare; simplified model: foF2 8 MHz day / 4 night, foE 3.5, secant law capped at 3.5, D absorption by day, hop distances from spherical geometry; used by both muf-luf and ionosphere-regions). After PR #12 merged: General v2, Technician v11, Extra v6 republished from main. Next batch: families 16-20 (scatter, long path, sidebands, privileges map, power limits).
- 2026-11-18 (PR #11 merged): General Class Trainer published from main as a new artifact (https://claude.ai/artifact/6ybQ4odexMzPKbgtAhoHux, v1, batch 1 families, `db` + `user`). Technician and Extra are republished once #12 merges (the template changes in #11 and #12 add only General widgets).
- 2026-11-18 (General batch 2, PR general-batch2, based on general-start): Reactance and resonance, antenna length, FM deviation, link budget, mixers and images. New widgets: `reactance-graph` (log-log XL/XC lines with frequency, L and C sliders, series or parallel net impedance, real-coil self-resonance), `antenna-ruler` (dipole, quarter-wave vertical or Yagi drawn to scale with a 6 ft person; 468/f, 234/f, reflector +5%, director -5%), `fm-spectrum` (Bessel sidebands with Carson's box, plus an oscillator → multiplier → transmitter chain), `link-budget` (dBm staircase with sensitivity line and margin; receiver sensitivity from front-end gain, noise figure and bandwidth via Friis), `mixer` (receiver mixer with IF filter and image, balanced modulator with sideband filter, product detector with BFO error). Shared helpers in the template: `LOGS`/`LOGI` (log sliders), `segOn`, `spectrum`, `besselJ`. Every preset clicked headless; each result matches the pool answer. Next batch: families 11-15 (intermod, solar weather, solar indices, MUF/LUF, ionosphere regions).
- 2026-11-18 (General start, PR general-start): G1, G2, G4 done and G3 built. Pool verified 423/423 against the Feb 4, 2026 errata PDF (no newer errata); `pool.py` now upper-cases RF in subelement names. Notes for all 423 questions (`check` flags none). `exams/general/exam.json` added (`ls` = `general-trainer-v1`, 35 questions, pass 26); figure G7-1 copied to `site/fig/`. Family map: 53 families covering 378 questions, each with an interaction plan (readable copy for Brooke: Claude Doc "General trainer: family map"). Batch 1: power formulas, RMS/peak/PEP, decibels and the S meter, series/parallel parts, transformers. New widgets: `power-wheel`, `sine-wave`, `s-meter`, `combiner`, `transformer`, plus `fmtSI` (metric-prefix formatting) in the template; `site.py check` validates their presets. Every preset was clicked headless and its result matched the pool answer. The preview artifact now shows General (Technician files removed from it). The template changed, so after merge: republish Technician and Extra, and publish the real General artifact (new, with `db` + `user`, then add it to ARTIFACTS.md). Next batch: families 6-10 (reactance and resonance, antenna length, FM deviation, link budget, mixers).
- 2026-11-18 (S4, public website): `tools/web.py build` writes `web/` (hub + `web/technician/` with manifest, service worker, icons, self-hosted fonts). Progress on the website is localStorage only, under the same `ls` key; the backup code moves it. Template gained the `<!--fonts-->`, `<!--web-head-->`, `<!--web-body-->` markers and an install card shown only when `CFG.web`; the artifact pages are unchanged apart from that inert code, so republish both artifacts after this merges. Hosting: Cloudflare Pages, no build step, output dir `web`. Also on record: Technician v10 and Extra v5 were published after PR #9. To put General or Extra on the website: add to `WEB_EXAMS`, add `short` to its exam.json (Extra has it), build, test, commit `web/`.
- 2026-11-18 (Technician families 31-34, pool questions in every widget): Coax and connectors, antenna length, grounding and lightning, RF exposure. All 34 Technician families are now written. Brooke noticed only the first pages had "Try a question from the pool" chips, so every widget type now takes `presets` (see SPEC.md), every family has them, and `match` can be started from either side. Questions left out of a widget are ones it doesn't work (for example a definition question whose answer is the term itself, or instrument questions on the units page). Families 26-30 were republished to Technician on 2026-11-18 (v9). The template changed, so republish Extra too after this merges. Next: X1, map the Extra families.
- 2026-11-18 (Technician families 26-30): Repeater alphabet soup, internet linking, "you sound bad" fixes, SWR, interference: whose fix is it? No new widgets: `match` (repeater terms, bad-audio reports), `scenario` (internet linking, SWR) and `sort-bins` (where the interference fix goes). Families 21-25 were republished to Technician on 2026-11-18 (v8). Next batch: families 31-34 (coax and connectors, antenna length, grounding and lightning, RF exposure).
- 2026-11-18 (Technician families 21-25): Who's responsible, control types, only-when exceptions, RACES vs. ARES, bandwidth ladder. `match` now accepts repeated answers (matches by text); `band-chart` items take `show` (list text) and bands take `title`. Control types: the pool never asks about local control, so the page covers remote, automatic, control point and auxiliary only (scope rule). Families 16-20 were republished to Technician on 2026-11-18 (v7). Next batch: families 26-30 (repeater alphabet soup, internet linking, you sound bad, SWR, interference).
- 2026-11-18 (Technician families 16-20): Polarization, weather and terrain, HF vs. VHF vs. UHF, privileges map, the numbers. New widget: `band-chart` (bands drawn to scale, linear or log, with segments and marked frequencies; details on tap). Only edges and spots the pool tests are drawn. Families 11-15 were republished to Technician on 2026-11-18 (v6). Next batch: families 21-25 (who's responsible, control types, only-when exceptions, RACES vs. ARES, bandwidth ladder).
- 2026-11-18 (Technician families 11-15): Lead names, schematic symbols, radio building blocks, which propagation when, multipath and fading. New widgets: `figure-explorer` (numbered buttons under a pool figure, a ring marks the part; ring positions are percent of the 1800x1200 figure), `scenario` (situations, optional dims with first-match rules), calc `multipath` (illustration only, no real distances). Families 6-10 were republished to Technician on 2026-11-18 (v5). Next batch: families 16-20 (polarization, weather and terrain, HF vs. VHF vs. UHF, privileges map needs `band-chart`, the numbers).
- 2026-11-18 (Technician families 6-10): Series vs. parallel, units, capacitor vs. inductor, resistance vs. impedance, what each component does. New widgets: `circuit-toggle` (series/parallel with ammeter or voltmeter; text from config), `sort-bins` (one card at a time, tap the bin), `match` (tap a term, then its partner). Families 1-5 were republished to Technician on 2026-11-18 (v4), and PR #2 was closed. Flow now: build, publish a preview copy (Technician Trainer Preview, https://claude.ai/artifact/JVa74CyW5j9ktfCoZp2u1o, no db), Brooke tries it, merges, then republish the real one. Next batch: families 11-15 (lead names, schematic symbols need `figure-explorer`, radio building blocks, which propagation needs `scenario`, multipath).
- 2026-11-17 (Technician families 1-5): Ohm's law, power and batteries, metric prefixes, decibels, wavelength and frequency pages written. New widgets in `app/template.html`: `formula-triangle` (tap the unknown, fill two values, see the working), `ladder` (prefix converter; every rung shows the same amount), `calculator` (named calcs in `CALCS`: `db`, `wavelength`). Widgets take `presets` of pool questions as chips. Every preset result was checked against the pool's correct answer headless. `tools/test_app.py` now also opens every published family page and clicks each preset chip. Republish Technician after the PR merges. Next batch: families 6-10 (series vs. parallel needs `circuit-toggle`, units needs `match` or `sort-bins`).
- 2026-11-17 (S1, S2): Both exam pages now come from `app/template.html` plus `exams/<exam>/exam.json`; run `tools/site.py build <exam>` after any change and never hand-edit a site's `index.html`. Storage keys and db path unchanged. Family support is in: "Still confused?" button under notes (runs and debriefs), family page over the current view with back returning to the same spot, deep links `#family-<id>`, "Drill these N". Pages are published only once `families/<exam>/<id>.json` exists; `tools/site.py check <exam>` validates them. No widgets exist yet (S3): the first family session builds its widget into the `WIDGETS` registry. Both sites tested headless with no page errors. Both artifacts republished after the merge (Technician v3, Extra v4); capabilities and saved progress carried over.
- 2026-11-17: Repo created from the first session. Technician and Extra sites live with notes for every question. All three pools verified word for word against the NCVEC PDFs. Technician family list drafted and approved by Brooke (34 families).
