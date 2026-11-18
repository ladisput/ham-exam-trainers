#!/usr/bin/env python3
"""Headless check of the public web app (web/, built by tools/web.py) for each trainer in WEB_EXAMS:
the hub links to it, the manifest and icons are valid, the service worker installs and takes over,
fonts come from the site (no Google Fonts), and with the network cut the trainer still opens, answers,
shows a family page, and keeps progress across a reload.
Usage: python3 tools/test_web.py    Screenshots go to shots/web-*.png
Needs: playwright for Python and Chromium (set CHROME=/path if not /usr/bin/google-chrome)."""
import asyncio, importlib.util, json, os, subprocess, sys, time
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("web", os.path.join(ROOT, "tools", "web.py")); web = importlib.util.module_from_spec(spec); spec.loader.exec_module(web)
WEB = os.path.join(ROOT, "web"); out = os.path.join(ROOT, "shots"); os.makedirs(out, exist_ok=True)
PORT = 8791; BASE = f"http://localhost:{PORT}"
fails = []
def ok(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=WEB, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
            for exam in web.WEB_EXAMS:
                cfg = json.load(open(os.path.join(ROOT, "exams", exam, "exam.json")))
                ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
                pg = await ctx.new_page(); errs, outside = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("request", lambda r: outside.append(r.url) if not r.url.startswith(BASE) else None)
                # hub
                await pg.goto(BASE + "/"); await pg.screenshot(path=f"{out}/web-hub.png", full_page=True)
                await pg.click(f'a[href="{exam}/"]'); await pg.wait_for_selector(".band")
                ok(pg.url == f"{BASE}/{exam}/", f"{exam}: hub card opens /{exam}/")
                # manifest and icons
                man = await (await pg.request.get(f"{BASE}/{exam}/manifest.webmanifest")).json()
                ok(man["short_name"] == cfg["short"] and man["display"] == "standalone" and man["start_url"] == "./", f"{exam}: manifest fields")
                for ic in man["icons"]:
                    r = await pg.request.get(f"{BASE}/{exam}/{ic['src']}"); ok(r.ok, f"{exam}: icon {ic['src']} {ic['purpose']}")
                ok(await pg.get_attribute('link[rel="manifest"]', "href") == "manifest.webmanifest", f"{exam}: page links the manifest")
                # service worker takes over
                ready = await pg.evaluate("Promise.race([navigator.serviceWorker.ready.then(()=>true),new Promise(r=>setTimeout(()=>r(false),10000))])")
                ok(ready, f"{exam}: service worker installs")
                if not ready:
                    await ctx.close(); continue
                await pg.reload(); await pg.wait_for_selector(".band")
                ok(await pg.evaluate("!!navigator.serviceWorker.controller"), f"{exam}: service worker controls the page")
                ok(await pg.evaluate("document.fonts.ready.then(()=>document.fonts.check('600 20px \"Barlow Condensed\"')&&document.fonts.check('400 16px Barlow'))"), f"{exam}: fonts load from the site")
                tip = await pg.inner_text("#app")
                ok("Put it on your home screen" in tip, f"{exam}: install card shows in the browser")
                await pg.screenshot(path=f"{out}/web-{exam}-home.png", full_page=True)
                # offline: reload, answer a question, open a family page, reload again and keep the progress
                await ctx.set_offline(True)
                await pg.reload(); await pg.wait_for_selector(".band")
                ok(True, f"{exam}: opens with no network")
                first = await pg.get_attribute(".band", "data-b"); await pg.click(f'.band[data-b="{first}"]'); await pg.click("#full")
                qid = (await pg.text_content(".card .cond")).strip(); await pg.click(".opt")
                await pg.wait_for_timeout(300)
                saved = await pg.evaluate(f"JSON.parse(localStorage.getItem({json.dumps(cfg['ls'])})||'{{}}')")
                ok(qid in saved.get("h", {}), f"{exam}: answer saved on the device under {cfg['ls']}")
                fams = json.load(open(os.path.join(WEB, exam, "families", "_index.json")))["families"]
                await pg.goto(f"{BASE}/{exam}/"); await pg.wait_for_selector(".band")
                if fams:  # prefer a family with a pool figure, to check images too
                    POOLQ = {q["id"]: q for q in json.load(open(os.path.join(WEB, exam, "pool.json")))["qs"]}
                    fam = next((f for f in fams if any(POOLQ[q].get("f") for q in f["questions"])), fams[0])
                    await pg.click(f'.band[data-fam="{fam["id"]}"]'); await pg.wait_for_selector("#fdrill")
                    ok("didn't load" not in await pg.text_content("#fam"), f"{exam}: family page opens offline")
                    await pg.evaluate("Promise.all([...document.querySelectorAll('#fam img')].map(i=>i.decode().catch(()=>0)))")
                    imgs = await pg.evaluate("[...document.querySelectorAll('#fam img')].every(i=>i.complete&&i.naturalWidth>0)")
                    ok(imgs, f"{exam}: family page images load offline")
                await pg.goto(f"{BASE}/{exam}/index.html"); await pg.wait_for_selector(".band")
                saved = await pg.evaluate(f"JSON.parse(localStorage.getItem({json.dumps(cfg['ls'])})||'{{}}')")
                ok(qid in saved.get("h", {}), f"{exam}: progress still there after an offline reload")
                await ctx.set_offline(False)
                # dismissing the install card sticks
                await pg.click("#instx"); await pg.reload(); await pg.wait_for_selector(".band")
                ok("Put it on your home screen" not in await pg.inner_text("#app"), f"{exam}: install card stays dismissed")
                ok(not errs, f"{exam}: no page errors {errs[:3]}")
                ok(not outside, f"{exam}: no requests leave the site {outside[:3]}")
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
    print("All web checks passed." if not fails else f"{len(fails)} web check(s) failed.")
    sys.exit(1 if fails else 0)

asyncio.run(main())
