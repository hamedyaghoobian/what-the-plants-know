"""The numbers for the README and the wall label: per book, the share of plants said of people,
and of the plants that are plants, the share on each rung of the ladder.

  python3 -I tools/stats.py
"""
import json
from collections import Counter, defaultdict

BOOKS = ["kalila", "attar", "shahnameh", "masnavi", "marzban", "parvin", "golestan", "bustan"]
RUNGS = ["rational", "gratuitous", "constructive", "species-typical", "anthropectomy"]
d = json.load(open("site/atlas/data.json"))
R = {"book": 0, "species": 1, "figure": 3, "mode": 4, "spec": 6}

def rung(rows):
    c = Counter(r[R["spec"]] for r in rows if r[R["figure"]] != "figure")
    n = sum(c[k] for k in RUNGS) or 1
    return {k: round(100 * c[k] / n) for k in RUNGS}, n

print(f"{'book':10s} {'plants':>6s} {'fig%':>5s}  " + " ".join(f"{k[:9]:>9s}" for k in RUNGS))
for b, name in enumerate(BOOKS):
    rows = [r for r in d["rows"] if r[0] == b]
    figs = sum(1 for r in rows if r[R["figure"]] == "figure")
    sh, n = rung(rows)
    print(f"{name:10s} {len(rows):6d} {round(100 * figs / max(1, len(rows))):5d}  " + " ".join(f"{sh[k]:9d}" for k in RUNGS))
allrows = d["rows"]
sh, n = rung(allrows)
print("all", len(allrows), sum(1 for r in allrows if r[R["figure"]] == "figure"), sh)

by = defaultdict(list)
for r in allrows: by[r[R["species"]]].append(r)
print("\nspecies: total, % figure, rung shares of the rest")
for s, rs in sorted(by.items(), key=lambda x: -len(x[1]))[:30]:
    sh, n = rung(rs)
    print(f"{s:14s} {len(rs):5d} fig {round(100 * sum(1 for r in rs if r[R['figure']] == 'figure') / len(rs)):3d}%  " + " ".join(f"{k[:5]} {sh[k]}" for k in RUNGS))

print("\nmode: n, rung shares (plants that are plants)")
modes = defaultdict(list)
for r in allrows:
    if r[R["figure"]] != "figure": modes[r[R["mode"]]].append(r)
for m, rs in sorted(modes.items(), key=lambda x: -len(x[1])):
    sh, n = rung(rs)
    print(f"{m:8s} {n:5d}  " + " ".join(f"{k[:5]} {sh[k]}" for k in RUNGS))
print("characters by book:", Counter(BOOKS[r[0]] for r in allrows if r[R["figure"]] == "character"))
