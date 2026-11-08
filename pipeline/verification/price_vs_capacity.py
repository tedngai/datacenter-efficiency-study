"""Compare the 2021->2026 YTD residential price rise with tracked AI capacity.

Inputs: pipeline/verification/eia_table.txt (EIA state series, UTF-16) and
data/published/data_centers.csv. Output: one line per state, the PJM-core vs
other mean, and a Spearman rank correlation. docs/community_brief.md section 2
quotes this output.

Capacity = gross power where published, else IT load, for operational and
partially operational sites (the convention of the country table).
This is a descriptive check, not a causal test: no controls for fuel, storm
or other costs, and the inventory covers large AI campuses only.
"""
import csv, os, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABBR = {"Alabama": "AL", "Arkansas": "AR", "Arizona": "AZ", "Georgia": "GA", "Iowa": "IA",
        "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Kansas": "KS", "Louisiana": "LA",
        "Michigan": "MI", "Minnesota": "MN", "Missouri": "MO", "Mississippi": "MS",
        "North Carolina": "NC", "North Dakota": "ND", "Nebraska": "NE", "New Jersey": "NJ",
        "New Mexico": "NM", "Nevada": "NV", "New York": "NY", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Virginia": "VA", "Washington": "WA", "Wisconsin": "WI", "West Virginia": "WV",
        "Wyoming": "WY",
        # xAI Colossus 2 straddles Memphis TN / Southaven MS; credit TN (Memphis load).
        "Tennessee / Mississippi": "TN"}
PJM_CORE = {"PA", "NJ", "OH", "IL", "VA", "WV"}  # states mostly inside PJM

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

eia = {}
for line in open(os.path.join(ROOT, "pipeline", "verification", "eia_table.txt"), encoding="utf-16").read().splitlines()[1:]:
    p = line.split()
    if len(p) == 7 and len(p[0]) == 2:
        eia[p[0]] = float(p[6])  # 2021 -> 2026 YTD %

cap = defaultdict(float)
for r in csv.DictReader(open(os.path.join(ROOT, "data", "published", "data_centers.csv"), encoding="utf-8")):
    if r["country"] != "United States" or r["status"] not in ("operational", "partially_operational"):
        continue
    st = ABBR.get(r["state_province"].strip())
    if st is None:
        raise SystemExit(f"unknown state {r['state_province']!r} ({r['name']})")
    cap[st] += num(r["power_capacity_mw"]) or num(r["it_load_mw"]) or 0

pts = sorted(((s, cap.get(s, 0.0), eia[s]) for s in eia), key=lambda p: -p[2])
for s, mw, pct in pts:
    print(f"{s}  operating MW {mw:7.0f}  price 2021->2026 YTD {pct:+5.1f}%")

def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i]); out = [0.0] * len(v); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]: j += 1
        for k in range(i, j + 1): out[order[k]] = (i + j) / 2  # average rank for ties
        i = j + 1
    return out

x, y = ranks([p[1] for p in pts]), ranks([p[2] for p in pts])
mx, my = sum(x) / len(x), sum(y) / len(y)
rho = sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5
core = [p[2] for p in pts if p[0] in PJM_CORE]; rest = [p[2] for p in pts if p[0] not in PJM_CORE]
print(f"\nstates {len(pts)}  PJM-core mean {sum(core)/len(core):+.1f}% (n={len(core)})  others {sum(rest)/len(rest):+.1f}% (n={len(rest)})")
print(f"Spearman rank correlation, operating MW vs price rise: {rho:.2f}")
