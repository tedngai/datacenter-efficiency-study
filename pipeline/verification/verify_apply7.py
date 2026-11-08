"""Seventh pass (Nov 2026): spell out two abbreviated state names.

The state comparison in docs/community_brief.md groups sites by
state_province. Two rows used a postal code, so they formed their own group.
No numeric value changes.
"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
rows = list(csv.DictReader(open(PATH, encoding="utf-8", newline="")))
cols = list(rows[0].keys())
by_name = {r["name"]: r for r in rows}

SET = [
    ("Google Kansas City East", "state_province", "MO", "Missouri"),
    ("Core Scientific Muskogee", "state_province", "OK", "Oklahoma"),
]

miss = 0
for name, col, old, new in SET:
    r = by_name.get(name)
    if r is None or r[col] != old:
        print("MISS", name, col, repr(r[col] if r else None)); miss += 1
    else:
        r[col] = new; print("OK  ", name, col, old, "->", new)
if miss:
    raise SystemExit(f"{miss} MISS, nothing written")
with open(PATH, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
