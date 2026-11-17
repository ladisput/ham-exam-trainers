#!/usr/bin/env python3
"""Headless walk-through of an exam site: first run of the first band (4 misses, no note button allowed),
debrief, a repeat run with all misses (opens a note), then a full mock exam.
Usage: python3 tools/test_app.py <exam>    Screenshots go to shots/<exam>-*.png
Needs: playwright for Python and a Chrome/Chromium binary (set CHROME=/path if not /usr/bin/google-chrome)."""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exam = sys.argv[1]; site = os.path.join(ROOT, "exams", exam, "site"); out = os.path.join(ROOT, "shots"); os.makedirs(out, exist_ok=True)
EX = {"technician": 35, "general": 35, "extra": 50}[exam]
async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8790"], cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
            pg = await b.new_page(viewport={"width": 390, "height": 844}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8790/index.html"); await pg.wait_for_selector(".band")
            await pg.screenshot(path=f"{out}/{exam}-home.png", full_page=True)
            BY = {q["id"]: q for q in json.load(open(os.path.join(site, "pool.json")))["qs"]}
            first = await pg.get_attribute(".band", "data-b"); await pg.click(f'.band[data-b="{first}"]'); await pg.click("#full")
            n = sum(1 for k in BY if k.startswith(first))
            for i in range(n):
                q = BY[(await pg.text_content(".card .cond")).strip()]
                for o in await pg.query_selector_all(".opt"):
                    if (int(await o.get_attribute("data-k")) == q["c"]) == (i >= 4): await o.click(); break
                assert await pg.query_selector("#hk") is None, "note button shown on a first run"
                await pg.click("#next")
            await pg.wait_for_selector(".miss"); await pg.screenshot(path=f"{out}/{exam}-debrief.png", full_page=True)
            await pg.click("#again")
            for i in range(n):
                q = BY[(await pg.text_content(".card .cond")).strip()]
                for o in await pg.query_selector_all(".opt"):
                    if int(await o.get_attribute("data-k")) != q["c"]: await o.click(); break
                if i == 0: await pg.click("#hk"); await pg.screenshot(path=f"{out}/{exam}-note.png", full_page=True)
                await pg.click("#next")
            await pg.click("#done"); await pg.click("#back"); await pg.click("#exam")
            for i in range(EX): await pg.click(".opt >> nth=0")
            await pg.wait_for_selector(".big"); await pg.screenshot(path=f"{out}/{exam}-exam.png", full_page=True)
            print("page errors:", errs or "none"); await b.close()
    finally:
        srv.terminate()
asyncio.run(main())
