#!/usr/bin/env python3
"""Headless walk-through of an exam site: first run of the first band (4 misses, no note button allowed),
debrief, a repeat run with all misses (opens a note), then a full mock exam.
Then the family pages ("Still confused?"), using a test family served in place of families/*.json:
the button in the debrief and in a run, back returning to the same spot, a deep link, and "Drill these N".
Usage: python3 tools/test_app.py <exam>    Screenshots go to shots/<exam>-*.png
Set SITE=web/<exam> to walk the web build instead. Needs: playwright for Python and a Chrome/Chromium binary (set CHROME=/path if not /usr/bin/google-chrome)."""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exam = sys.argv[1]; site = os.environ.get("SITE") or os.path.join(ROOT, "exams", exam, "site"); out = os.path.join(ROOT, "shots"); os.makedirs(out, exist_ok=True)
EX = {"technician": 35, "general": 35, "extra": 50}[exam]
async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8790"], cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
            pg = await b.new_page(viewport={"width": 390, "height": 844}, service_workers="block"); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            BY = {q["id"]: q for q in json.load(open(os.path.join(site, "pool.json")))["qs"]}
            # test family: every question of the first band, so each miss in the runs below has a button
            band1 = sorted({k[:2] for k in BY})[0]
            fq = sorted(k for k in BY if k.startswith(band1))
            t0 = BY[fq[0]]; wrong0 = t0["a"][(t0["c"] + 1) % 4]
            fam = {"id": "test-family", "exam": exam, "title": "Test family", "idea": "One idea, tested from several angles.",
                   "core": {"type": "rule-table", "rows": [["", "A", "B"], ["Same everywhere", "Current", "Voltage"]]},
                   "widget": {"type": "none-yet", "config": {}},
                   "compare": [{"term": "Voltmeter", "how": "In parallel"}, {"term": "Ammeter", "how": "In series"}],
                   "traps": [{"q": fq[0], "wrong": wrong0, "why": "Test trap."}], "questions": fq}
            async def serve(route, body): await route.fulfill(status=200, content_type="application/json", body=json.dumps(body))
            await pg.route("**/families/_index.json", lambda r: serve(r, {"exam": exam, "families": [{"id": fam["id"], "title": fam["title"], "questions": fq}]}))
            await pg.route("**/families/test-family.json", lambda r: serve(r, fam))
            await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
            await pg.screenshot(path=f"{out}/{exam}-home.png", full_page=True)
            first = await pg.get_attribute(".band", "data-b"); await pg.click(f'.band[data-b="{first}"]'); await pg.click("#full")
            n = sum(1 for k in BY if k.startswith(first))
            for i in range(n):
                q = BY[(await pg.text_content(".card .cond")).strip()]
                for o in await pg.query_selector_all(".opt"):
                    if (int(await o.get_attribute("data-k")) == q["c"]) == (i >= 4): await o.click(); break
                assert await pg.query_selector("#hk") is None, "note button shown on a first run"
                await pg.click("#next")
            await pg.wait_for_selector(".miss"); await pg.screenshot(path=f"{out}/{exam}-debrief.png", full_page=True)
            assert first == band1
            # "Still confused?" from the debrief, then back to the same debrief
            assert await pg.locator("#app .fambtn").count() == 4, "each miss should have a Still confused button"
            await pg.locator("#app .fambtn").nth(1).click(); await pg.wait_for_selector("#fdrill")
            assert await pg.is_hidden("#app") and "#family-test-family" in pg.url
            assert await pg.locator(".fq").count() == len(fq) and await pg.locator(".trap").count() == 1
            assert await pg.text_content("#fdrill") == f"Drill these {len(fq)} questions"
            await pg.screenshot(path=f"{out}/{exam}-family.png", full_page=True)
            await pg.click("#fback"); await pg.wait_for_selector("#app .miss")
            assert await pg.is_hidden("#fam") and await pg.locator("#app .fambtn").count() == 4, "back should return to the debrief"
            await pg.click("#again")
            for i in range(n):
                q = BY[(await pg.text_content(".card .cond")).strip()]
                for o in await pg.query_selector_all(".opt"):
                    if int(await o.get_attribute("data-k")) != q["c"]: await o.click(); break
                if i == 0:
                    await pg.click("#hk"); await pg.screenshot(path=f"{out}/{exam}-note.png", full_page=True)
                    # "Still confused?" in a run: open it, come back to the same answered question
                    qid = (await pg.text_content(".card .cond")).strip()
                    await pg.click("#app .fambtn"); await pg.wait_for_selector("#fdrill"); await pg.go_back()
                    await pg.wait_for_selector("#app .opt.wrong")
                    assert (await pg.text_content(".card .cond")).strip() == qid and await pg.is_visible("#next"), "back should return to the run"
                await pg.click("#next")
            await pg.click("#done"); await pg.click("#back"); await pg.click("#exam")
            for i in range(EX): await pg.click(".opt >> nth=0")
            await pg.wait_for_selector(".big"); await pg.screenshot(path=f"{out}/{exam}-exam.png", full_page=True)
            # deep link to a family page, then "Drill these N" runs exactly the family's questions
            await pg.goto("http://localhost:8790/index.html#family-test-family"); await pg.wait_for_selector("#fdrill")
            await pg.click("#fdrill"); seen = set()
            for i in range(len(fq)):
                assert (await pg.text_content(".qhead span")).endswith(f"of {len(fq)}")
                seen.add((await pg.text_content(".card .cond")).strip()); await pg.click(".opt >> nth=0"); await pg.click("#next")
            assert seen == set(fq), "the drill should be exactly the family's questions"
            await pg.wait_for_selector("#done"); assert await pg.text_content("#done") == "Family page"
            await pg.click("#done"); await pg.wait_for_selector("#fdrill"); await pg.click("#fback"); await pg.wait_for_selector("#again")
            # a page with no families published shows no button
            await pg.unroute("**/families/_index.json"); await pg.unroute("**/families/test-family.json")
            await pg.goto("about:blank"); await pg.goto("http://localhost:8790/index.html#family-test-family"); await pg.wait_for_selector(".band")
            assert await pg.locator(".fambtn").count() == 0 and await pg.is_hidden("#fam")
            # the home screen lists every published family page, and tapping one opens it
            fams = json.load(open(os.path.join(site, "families", "_index.json")))["families"]
            if fams:
                await pg.goto("about:blank"); await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
                assert await pg.locator('#app button[data-fam]').count() == len(fams), "home should list every family page"
                await pg.locator('#app button[data-fam]').first.click(); await pg.wait_for_selector("#fdrill")
                await pg.click("#fback"); await pg.wait_for_selector("#app .band")
            # reference pages: listed on the home screen, each opens with every entry, back returns home, deep link works
            rp = os.path.join(site, "references", "_index.json")
            refs = json.load(open(rp))["references"] if os.path.exists(rp) else []
            await pg.goto("about:blank"); await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
            assert await pg.locator('#app button[data-ref]').count() == len(refs), "home should list every reference page"
            for i, r in enumerate(refs):
                doc = json.load(open(os.path.join(site, "references", r["id"] + ".json")))
                await pg.locator('#app button[data-ref]').nth(i).click(); await pg.wait_for_selector("#fback2")
                assert "#ref-" + r["id"] in pg.url and await pg.is_hidden("#app")
                if doc["kind"] == "glossary":
                    n = sum(len(g["items"]) for g in doc["groups"])
                    assert await pg.locator("#fam .gl").count() == n, "the glossary should show every entry"
                    assert await pg.locator("#fam .fambtn, #fam #fdrill").count() == 0, "a reference page has no question links"
                    # band buttons on each group: counts recomputed here the way site.py's check reads the pool, most first
                    import re
                    def words(q):
                        w = set()
                        for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9.\-/]*", " ".join([q["q"]] + q["a"])):
                            t = re.sub(r"^[\d.]+(?=[A-Za-z])", "", t.rstrip(".,")); w.add(t); w |= {x for x in re.split(r"[-/]", t) if x}
                        return w
                    W = {qi: words(q) for qi, q in BY.items()}
                    for gi, g in enumerate(doc["groups"]):
                        terms = [v.rstrip(".") for it in g["items"] for v in it[0].split(", ")]
                        n = {}
                        for qi in BY:
                            if any(t in W[qi] for t in terms): n[qi[:2]] = n.get(qi[:2], 0) + 1
                        got = await pg.locator("#fam .card").nth(gi + 1).locator("[data-gb]").all_text_contents()
                        got = [x.replace(" ", "") for x in got]; cnt = [int(x[2:]) for x in got]
                        assert sorted(got) == sorted(f"{b_}{c}" for b_, c in n.items()) and cnt == sorted(cnt, reverse=True), (g["title"], got, n)
                    # tapping a band button opens that band
                    first = pg.locator("#fam [data-gb]").first; fb = await first.get_attribute("data-gb")
                    await first.click(); await pg.wait_for_selector("#back")
                    assert "#band-" + fb in pg.url and await pg.is_hidden("#fam")
                    await pg.goto("about:blank"); await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
                    await pg.locator('#app button[data-ref]').nth(i).click(); await pg.wait_for_selector("#fback2")
                await pg.screenshot(path=f"{out}/{exam}-ref-{r['id']}.png", full_page=True)
                await pg.click("#fback2"); await pg.wait_for_selector("#app .band")
                assert await pg.is_hidden("#fam") and "#ref-" not in pg.url
                await pg.goto("about:blank"); await pg.goto(f"http://localhost:8790/index.html#ref-{r['id']}"); await pg.wait_for_selector("#fam .gl, #fback2")
                await pg.click("#fback"); await pg.wait_for_selector("#app .band")
                await pg.goto("about:blank"); await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
            # every real family page: loads, its widget card renders (not dropped by an error), every preset chip works
            for f in json.load(open(os.path.join(site, "families", "_index.json")))["families"]:
                doc = json.load(open(os.path.join(site, "families", f["id"] + ".json")))
                await pg.goto("about:blank"); await pg.goto(f"http://localhost:8790/index.html#family-{f['id']}"); await pg.wait_for_selector("#fdrill")
                wt = doc["widget"]["type"]
                if wt in ("formula-triangle", "ladder", "calculator", "circuit-toggle", "sort-bins", "match", "figure-explorer", "scenario", "band-chart"):
                    assert await pg.locator("#widget").count() == 1, f"{f['id']}: widget card missing"
                    # "Try a question from the pool": every chip shows its question and sets the widget up for it
                    pres = doc["widget"]["config"].get("presets", [])
                    for i in range(await pg.locator("#widget .chip").count()):
                        await pg.locator("#widget .chip").nth(i).click(); assert await pg.is_visible("#widget .wq"), f"{f['id']}: chip {i} shows no question"
                        if wt == "match": assert await pg.locator("#widget .mt .sel").count() == 1, f"{f['id']}: chip {i} selects nothing"
                        elif wt == "sort-bins": assert (await pg.text_content("#widget .sbcard")).strip() == doc["widget"]["config"]["cards"][pres[i]["t"]]["t"], f"{f['id']}: chip {i} deals the wrong card"
                        else: assert await pg.is_visible("#widget .wres .eq"), f"{f['id']}: chip {i} gives no result"
                    if wt not in ("formula-triangle", "ladder", "calculator"):
                        assert await pg.locator("#widget .chip").count() > 0, f"{f['id']}: no pool questions in the widget"
                    await pg.goto("about:blank"); await pg.goto(f"http://localhost:8790/index.html#family-{f['id']}"); await pg.wait_for_selector("#widget")
                    if wt == "circuit-toggle":
                        for m in ("parallel", "series"):
                            await pg.click(f'#widget .seg [data-m="{m}"]'); assert await pg.locator("#widget .circ .mtr").count() == 1
                    if wt == "sort-bins":  # sort every card into its right bin; expect a full score
                        cards = {k["t"]: k["bin"] for k in doc["widget"]["config"]["cards"]}
                        for _ in cards:
                            await pg.click(f'#widget .bins button[data-b="{cards[(await pg.text_content("#widget .sbcard")).strip()]}"]'); await pg.click("#sbnext")
                        assert (await pg.text_content("#widget .wres .eq")).startswith(f"{len(cards)} of {len(cards)}")
                    if wt == "figure-explorer":  # every figure, every part number shows a name and the ring
                        for fi, F in enumerate(doc["widget"]["config"]["figs"]):
                            if len(doc["widget"]["config"]["figs"]) > 1: await pg.click(f'#widget [data-f="{fi}"]')
                            for pi, part in enumerate(F["parts"]):
                                await pg.click(f'#widget .nums [data-p="{pi}"]')
                                assert part["name"] in await pg.text_content("#widget .wres .eq") and await pg.is_visible("#widget .ring")
                    if wt == "scenario":  # every situation shows a result; every option of every dim too
                        for si, S in enumerate(doc["widget"]["config"]["situations"]):
                            await pg.click(f'#widget [data-s="{si}"]'); assert await pg.is_visible("#widget .wres .eq")
                            for d in S.get("dims", []):
                                for o in d["options"]:
                                    await pg.click(f'#widget [data-d="{d["id"]}"][data-o="{o}"]'); assert (await pg.text_content("#widget .wres .eq")).strip()
                    if wt == "band-chart":  # every band draws; every segment and mark opens its details
                        for bi, B in enumerate(doc["widget"]["config"]["bands"]):
                            if len(doc["widget"]["config"]["bands"]) > 1: await pg.click(f'#widget [data-b="{bi}"]')
                            items = B.get("segs", []) + B.get("marks", [])
                            assert await pg.locator("#widget .bclist button").count() == len(items)
                            for ii, it in enumerate(items):
                                await pg.click(f'#widget .bclist [data-i="{ii}"]'); assert it["label"] in await pg.text_content("#widget .wres .eq")
                    if wt == "match":  # one wrong tap, then every right pair; expect all matched
                        pairs = doc["widget"]["config"]["pairs"]
                        await pg.locator("#widget .l").first.click()
                        li = await pg.locator("#widget .l").first.get_attribute("data-i")
                        wrong = next(i for i, p in enumerate(pairs) if p[1] != pairs[int(li)][1])
                        await pg.click(f'#widget .r[data-i="{wrong}"]'); assert await pg.locator("#widget .r.ok").count() == 0
                        for i in range(len(pairs)):
                            await pg.click(f'#widget .l[data-i="{i}"]'); await pg.click(f'#widget .r[data-i="{i}"]')
                        assert await pg.locator("#widget .r.ok").count() == len(pairs) and await pg.is_visible("#mtagain")
                assert await pg.locator(".fq").count() == len(f["questions"])
                await pg.screenshot(path=f"{out}/{exam}-family-{f['id']}.png", full_page=True)
            print("page errors:", errs or "none"); await b.close()
    finally:
        srv.terminate()
asyncio.run(main())
