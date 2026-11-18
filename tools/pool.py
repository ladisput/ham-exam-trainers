#!/usr/bin/env python3
"""Question-pool tools for the ham exam trainers.

Usage (run from the repo root):
  python3 tools/pool.py build  <exam>   verify raw JSON against the official PDF, write site/pool.json
  python3 tools/pool.py list   <exam> [prefix ...]   print id | question | correct [x: wrong answers]
  python3 tools/pool.py merge  <exam>   merge notes/*.json into site/hooks.json
  python3 tools/pool.py check  <exam>   sanity-check notes against the answer key

<exam> is technician, general, or extra. Exam settings live in EXAMS below.
Needs: pdftotext (poppler-utils).
"""
import glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMS = {
    "technician": {"letter": "T", "raw": "technician-2026-2030.json",
                   "pdf": "2026-2030 Technician Pool and Syllabus Public Release Feb 19 2026.pdf"},
    "general": {"letter": "G", "raw": "general-2023-2027.json",
                "pdf": "General Class Pool and Syllabus 2023-2027 Public Release with 6th Errata Feb 4 2026.pdf"},
    "extra": {"letter": "E", "raw": "extra-2024-2028.json",
              "pdf": "2024-2028 Extra Class Question Pool and Syllabus Public Release with 4th Errata Feb 4 2026.pdf"},
}

def paths(exam):
    d = os.path.join(ROOT, "exams", exam)
    return d, os.path.join(d, "raw", EXAMS[exam]["raw"]), os.path.join(ROOT, "sources", EXAMS[exam]["pdf"])

def pdf_text(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout

fixcase = lambda s: re.sub(r"\brf\b", "RF", s)  # capitalize() lowers acronyms

norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("’", "'"))

def build(exam):
    d, raw, pdf = paths(exam)
    L = EXAMS[exam]["letter"]
    t = pdf_text(pdf).replace("\u2013", "-").replace("\u2014", "-")
    qs_raw = json.load(open(raw))
    # verify every question, answer and key against the PDF
    first = t.find(f"{L}1A01 (")
    if first < 0:
        first = t.find(f"{L}0A01 (")
    blocks = re.split(rf"\n\s*(?={L}\d[A-Z]\d\d\s*\([A-D]\))", t[first:])
    P = {}
    for b in blocks:
        m = re.match(rf"\s*({L}\d[A-Z]\d\d)\s*\(([A-D])\)", b)
        if m:
            P[m.group(1)] = (m.group(2), norm(b.split("~~")[0]))
    bad = []
    for q in qs_raw:
        p = P.get(q["id"])
        if not p:
            bad.append((q["id"], "not in PDF")); continue
        if p[0] != q["correct_letter"]:
            bad.append((q["id"], "answer key differs"))
        if not all(norm(x) in p[1] for x in [q["question"]] + q["answers"]):
            bad.append((q["id"], "text differs"))
    extra_in_pdf = [k for k in P if k not in {q["id"] for q in qs_raw}]
    print(f"PDF questions: {len(P)}  JSON questions: {len(qs_raw)}")
    print("Mismatches:", bad or "none")
    print("In PDF but not JSON (check if withdrawn):", extra_in_pdf or "none")
    # syllabus titles
    # syllabus = the first "SUBELEMENT x1" block that is followed by its group list (skips errata notes)
    s = next(m.start() for m in re.finditer(rf"SUBELEMENT {L}1", t)
             if re.search(rf"\n\s*{L}1A ", t[m.start():m.start() + 400]))
    e = t.find(f"SUBELEMENT {L}1", s + 10)
    subs, groups, cur = {}, {}, None
    for line in t[s:e].split("\n"):
        line = line.strip()
        m = re.search(rf"SUBELEMENT ({L}\d) - (.+?) -? ?\[", line)
        if m:
            subs[m.group(1)] = fixcase(m.group(2).replace("’", "'").strip().capitalize()); cur = None
            line = line[:m.start()].strip()
        if not line:
            continue
        m2 = re.match(rf"({L}\d[A-Z]) (?:- )?(.*)", line)
        if m2:
            cur = m2.group(1); groups[cur] = m2.group(2); continue
        if cur and not re.match(r"(20\d\d|FCC|Effective)", line):
            groups[cur] += ("" if groups[cur].endswith("-") else " ") + line
    # the Safety subelement (x0) is listed last in some syllabi
    for m in re.finditer(rf"SUBELEMENT ({L}0) - (.+?) -? ?\[", t):
        subs.setdefault(m.group(1), fixcase(m.group(2).strip().capitalize()))
    for m in re.finditer(rf"\n\s*({L}0[A-Z]) (.+)", t[:first]):
        groups.setdefault(m.group(1), m.group(2).strip())
    qs = sorted([{"id": q["id"], "q": q["question"], "a": q["answers"], "c": q["correct"],
                  "f": q["figure"], "r": q["refs"]} for q in qs_raw], key=lambda q: q["id"])
    missing = sorted({q["id"][:3] for q in qs} - set(groups))
    print(f"Subelements: {len(subs)}  Groups: {len(groups)}  Groups missing a title: {missing or 'none'}")
    os.makedirs(os.path.join(d, "site"), exist_ok=True)
    json.dump({"subs": subs, "groups": groups, "qs": qs}, open(os.path.join(d, "site", "pool.json"), "w"),
              ensure_ascii=False, separators=(",", ":"))
    print("Wrote", os.path.join("exams", exam, "site", "pool.json"))

def load_pool(exam):
    return json.load(open(os.path.join(ROOT, "exams", exam, "site", "pool.json")))

def lst(exam, prefixes):
    for q in load_pool(exam)["qs"]:
        if not prefixes or any(q["id"].startswith(p) for p in prefixes):
            wrong = " / ".join(a for i, a in enumerate(q["a"]) if i != q["c"])
            fig = f" [figure {q['f']}]" if q["f"] else ""
            print(f"{q['id']}|{q['q']}{fig}|=> {q['a'][q['c']]}  [x: {wrong}]")

def merge(exam):
    h = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "exams", exam, "notes", "*.json"))):
        h.update(json.load(open(f)))
    ids = [q["id"] for q in load_pool(exam)["qs"]]
    print("notes:", len(h), "of", len(ids), " missing:", [i for i in ids if i not in h] or "none",
          " unknown ids:", [k for k in h if k not in ids] or "none")
    json.dump(h, open(os.path.join(ROOT, "exams", exam, "site", "hooks.json"), "w"),
              ensure_ascii=False, separators=(",", ":"))

def check(exam):
    h = json.load(open(os.path.join(ROOT, "exams", exam, "site", "hooks.json")))
    n = lambda s: s.replace(",", "")
    flagged = 0
    for q in load_pool(exam)["qs"]:
        c = q["a"][q["c"]]; note = h.get(q["id"], "")
        nums = re.findall(r"\d+(?:\.\d+)?", n(c))
        if nums and not q["f"] and any(x not in n(note) for x in nums):
            print("NUMBER NOT IN NOTE:", q["id"], "|", c, "|", note[:100]); flagged += 1
        if c.startswith("All these") and "all" not in note.lower():
            print("ALL-OF-THESE NOT SAID:", q["id"]); flagged += 1
        for i, a in enumerate(q["a"]):
            if i != q["c"] and a.startswith("All these") and re.search(r"all (three|of these)", note.lower()):
                print("NOTE SAYS ALL BUT ANSWER ISN'T:", q["id"]); flagged += 1
    print("flagged:", flagged, "(review each by hand; some are fine)")

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in {"build", "list", "merge", "check"} or sys.argv[2] not in EXAMS:
        print(__doc__); sys.exit(1)
    cmd, exam = sys.argv[1], sys.argv[2]
    {"build": lambda: build(exam), "list": lambda: lst(exam, sys.argv[3:]),
     "merge": lambda: merge(exam), "check": lambda: check(exam)}[cmd]()
