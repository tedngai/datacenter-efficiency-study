import csv, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "canonical", "data_centers.csv")

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
by = defaultdict(list)
for r in rows:
    by[r["country"]].append(r["name"])
c = Counter(r["country"] for r in rows)
print(f"{len(rows)} rows, {len(by)} countries\n")
for k in sorted(by, key=lambda x: -len(by[x])):
    print(f"== {k} ({len(by[k])})")
    for n in sorted(by[k]):
        print("   ", n)
