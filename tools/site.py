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
    return bad


def build(exam):
    cfg = load(os.path.join(ROOT, "exams", exam, "exam.json"))
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        sys.exit(f"exam.json is missing: {', '.join(missing)}")
    html = open(os.path.join(ROOT, "app", "template.html"), encoding="utf-8").read()
    for k in ["title", "callSize", "callWidth"]:
        html = html.replace("{{" + k + "}}", str(cfg[k]))
    html = html.replace("{{config}}", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    if "{{" in html:
        sys.exit("template has an unfilled {{placeholder}}")
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
