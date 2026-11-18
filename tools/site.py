#!/usr/bin/env python3
"""Build and check an exam site from the shared template.

Usage (run from the repo root):
  python3 tools/site.py build <exam>   write exams/<exam>/site/index.html from app/template.html + exams/<exam>/exam.json,
                                       and copy finished family pages into exams/<exam>/site/families/
  python3 tools/site.py check <exam>   check the exam's family files against its pool (SPEC.md check 3, the parts code can do)

Never hand-edit exams/<exam>/site/index.html: edit app/template.html (shared) or exam.json (per exam), then build.
Never change an exam's "ls" key once it is live, or saved progress is lost.
"""
import glob, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ["title", "heading", "element", "source", "letter", "ex", "pass", "ls", "callSize", "callWidth"]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def family_files(exam):
    """Finished family pages: every families/<exam>/<id>.json except the index."""
    d = os.path.join(ROOT, "families", exam)
    return sorted(p for p in glob.glob(os.path.join(d, "*.json")) if not os.path.basename(p).startswith("_"))


def check(exam):
    """Return a list of problems with the exam's family files (empty = all good)."""
    site = os.path.join(ROOT, "exams", exam, "site")
    BY = {q["id"]: q for q in load(os.path.join(site, "pool.json"))["qs"]}
    idx_p = os.path.join(ROOT, "families", exam, "_index.json")
    index = {f["id"]: f for f in load(idx_p)["families"]} if os.path.exists(idx_p) else {}
    bad = []
    # index: known question ids, at most two families per question
    seen = {}
    for fid, f in index.items():
        for q in f["questions"]:
            if q not in BY:
                bad.append(f"_index {fid}: {q} is not in the pool")
            seen.setdefault(q, []).append(fid)
    bad += [f"_index: {q} is in {len(v)} families ({', '.join(v)}); the limit is 2" for q, v in seen.items() if len(v) > 2]
    for p in family_files(exam):
        fam = load(p)
        fid = os.path.basename(p)[:-5]
        for k in ["id", "exam", "title", "idea", "core", "widget", "traps", "questions"]:
            if k not in fam:
                bad.append(f"{fid}: missing '{k}'")
        if fam.get("id") != fid:
            bad.append(f"{fid}: id '{fam.get('id')}' does not match the file name")
        if fam.get("exam") != exam:
            bad.append(f"{fid}: exam '{fam.get('exam')}' should be '{exam}'")
        if fid not in index:
            bad.append(f"{fid}: not listed in _index.json")
        elif fam.get("questions") != index[fid]["questions"]:
            bad.append(f"{fid}: questions differ from _index.json")
        for q in fam.get("questions", []):
            if q not in BY:
                bad.append(f"{fid}: {q} is not in the pool")
        for t in fam.get("traps", []):
            q = BY.get(t.get("q"))
            if not q:
                bad.append(f"{fid}: trap question {t.get('q')} is not in the pool")
            elif t.get("q") not in fam.get("questions", []):
                bad.append(f"{fid}: trap question {t['q']} is not one of the family's questions")
            elif t.get("wrong") not in [a for i, a in enumerate(q["a"]) if i != q["c"]]:
                bad.append(f"{fid}: trap for {t['q']}: '{t.get('wrong')}' is not a wrong answer of that question")
        # widget presets ("Try a question from the pool"): a family question, pointing at something that exists
        w = fam.get("widget", {}); c = w.get("config", {})
        size = {"match": len(c.get("pairs", [])), "sort-bins": len(c.get("cards", [])), "scenario": len(c.get("situations", []))}
        for pr in c.get("presets", []):
            if pr.get("q") not in fam.get("questions", []):
                bad.append(f"{fid}: preset {pr.get('q')} is not one of the family's questions")
            k = {"match": "i", "sort-bins": "t", "scenario": "s"}.get(w.get("type"))
            if k and not (isinstance(pr.get(k), int) and 0 <= pr[k] < size[w["type"]]):
                bad.append(f"{fid}: preset {pr.get('q')}: '{k}' is out of range")
            t = w.get("type")
            if t == "power-wheel" and not (len(pr.get("vals", {})) == 2 and set(pr["vals"]) <= set("PEIR")):
                bad.append(f"{fid}: preset {pr.get('q')}: vals must give exactly two of P, E, I, R")
            if t == "sine-wave" and pr.get("kind") not in ("pk", "pp", "rms", "w"):
                bad.append(f"{fid}: preset {pr.get('q')}: kind must be pk, pp, rms or w")
            if t == "s-meter" and not all(isinstance(pr.get(k), (int, float)) for k in ("from", "d")):
                bad.append(f"{fid}: preset {pr.get('q')}: needs numbers 'from' and 'd'")
            if t == "combiner" and not (pr.get("kind") in ("R", "L", "C") and pr.get("mode") in ("series", "parallel") and 2 <= len(pr.get("parts", [])) <= 4):
                bad.append(f"{fid}: preset {pr.get('q')}: needs kind R/L/C, mode series/parallel and 2 to 4 parts")
            if t == "transformer" and not (pr.get("np", 0) > 0 and pr.get("ns", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs np and ns above zero")
            if t == "reactance-graph" and not ((pr.get("at") or isinstance(pr.get("f"), (int, float))) and pr.get("mode", "series") in ("series", "parallel")):
                bad.append(f"{fid}: preset {pr.get('q')}: needs f (MHz) or at: true, and mode series/parallel")
            if t == "antenna-ruler" and not (pr.get("f", 0) > 0 and pr.get("kind") in ("dipole", "quarter", "yagi")):
                bad.append(f"{fid}: preset {pr.get('q')}: needs f (MHz) and kind dipole/quarter/yagi")
            if t == "fm-spectrum" and not (pr.get("dev", 0) > 0 and pr.get("af", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs dev and af (kHz) above zero")
            if t == "link-budget" and not set(pr) <= {"q", "w", "tl", "ta", "path", "ra", "rl", "bw", "nf", "g", "focus"}:
                bad.append(f"{fid}: preset {pr.get('q')}: unknown key")
            if t == "mixer" and pr.get("mode") not in ("rx", "mod", "det"):
                bad.append(f"{fid}: preset {pr.get('q')}: mode must be rx, mod or det")
            if t == "two-tone" and not (pr.get("a1", 0) > 0 and pr.get("a2", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs a1 and a2 (Hz)")
            if t == "sun-timeline" and not (pr.get("ev") in ("flare", "cme", "hole", "rot") and pr.get("t", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs ev flare/cme/hole/rot and t (minutes)")
            if t == "sun-indices" and not ("ssn" in pr or pr.get("k") in ("quiet", "storm")):
                bad.append(f"{fid}: preset {pr.get('q')}: needs ssn or k quiet/storm")
            if t == "ionosphere" and not (pr.get("tod", "day") in ("day", "night", "flare") and (pr.get("f") or pr.get("snap") in ("muf", "fc", "ca"))):
                bad.append(f"{fid}: preset {pr.get('q')}: needs f or snap, and tod day/night/flare")
            if t == "skip-zone" and not (pr.get("band", "20") in ("40", "20", "10") and pr.get("d", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs band 40/20/10 and d (miles)")
            if t == "great-circle" and not (pr.get("to") in ("London", "Tokyo", "Sydney", "Cape Town", "Rio", "Mumbai") and pr.get("path", "short") in ("short", "long")):
                bad.append(f"{fid}: preset {pr.get('q')}: needs a known city 'to' and path short/long")
            if t == "band-tuner":
                bands = c.get("bands") or list(USPLAN)
                lo, hi = USPLAN.get(pr.get("b"), (0, 0))
                if pr.get("b") not in bands or not lo <= pr.get("f", 0) <= hi or pr.get("m") not in c.get("modes", ["cw", "voice", "image", "rtty", "ft8"]):
                    bad.append(f"{fid}: preset {pr.get('q')}: needs a listed band b, f (kHz) inside it and a listed mode m")
            if t == "power-limit" and not (pr.get("b") in ("160", "80", "60", "40", "30", "20", "17", "15", "12", "10", "6") and pr.get("w", 0) > 0):
                bad.append(f"{fid}: preset {pr.get('q')}: needs band b and w (watts)")
            if w.get("type") == "band-chart":
                B = c["bands"][pr.get("b", 0)] if pr.get("b", 0) < len(c["bands"]) else None
                if B is None or ("i" in pr and not 0 <= pr["i"] < len(B.get("segs", [])) + len(B.get("marks", []))):
                    bad.append(f"{fid}: preset {pr.get('q')}: band or item out of range")
    return bad


# band edges in kHz for band-tuner presets (the full plan is USPLAN in app/template.html)
USPLAN = {"160": (1800, 2000), "80": (3500, 4000), "40": (7000, 7300), "30": (10100, 10150), "20": (14000, 14350), "17": (18068, 18168),
          "15": (21000, 21450), "12": (24890, 24990), "10": (28000, 29700), "6": (50000, 54000), "2": (144000, 148000)}


def render(exam, extra=None):
    """The page for one exam: app/template.html filled in from exam.json (plus `extra` settings, e.g. {"web": true})."""
    cfg = load(os.path.join(ROOT, "exams", exam, "exam.json"))
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        sys.exit(f"exam.json is missing: {', '.join(missing)}")
    cfg.update(extra or {})
    html = open(os.path.join(ROOT, "app", "template.html"), encoding="utf-8").read()
    for k in ["title", "callSize", "callWidth"]:
        html = html.replace("{{" + k + "}}", str(cfg[k]))
    html = html.replace("{{config}}", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    if "{{" in html:
        sys.exit("template has an unfilled {{placeholder}}")
    return html


def build(exam):
    html = render(exam)
    site = os.path.join(ROOT, "exams", exam, "site")
    with open(os.path.join(site, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    # family pages: only finished ones are published; the site index lists only those
    problems = check(exam)
    if problems:
        print("Family problems (fix before publishing):", *problems, sep="\n  ")
    out = os.path.join(site, "families")
    if os.path.isdir(out):
        shutil.rmtree(out)
    files = family_files(exam)
    os.makedirs(out)
    fams = []
    for p in files:
        fam = load(p)
        shutil.copy(p, os.path.join(out, os.path.basename(p)))
        fams.append({"id": fam["id"], "title": fam["title"], "questions": fam["questions"]})
    with open(os.path.join(out, "_index.json"), "w", encoding="utf-8") as f:
        json.dump({"exam": exam, "families": fams}, f, ensure_ascii=False, indent=1)
    print(f"Built exams/{exam}/site/index.html; {len(fams)} family page(s) published.")
    return not problems


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("build", "check"):
        sys.exit(__doc__)
    cmd, exam = sys.argv[1], sys.argv[2]
    if cmd == "build":
        sys.exit(0 if build(exam) else 1)
    problems = check(exam)
    print("Family problems:", *problems, sep="\n  ") if problems else print("Families: no problems")
    sys.exit(1 if problems else 0)
