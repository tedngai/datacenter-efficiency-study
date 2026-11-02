"""Emit a country-level summary table (sites, known MW, H100e) from the
published dataset, and write it to data/published/country_table.md."""
import csv, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "data", "published", "data_centers.csv")
OUT = os.path.join(ROOT, "data", "published", "country_table.md")

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
agg = defaultdict(lambda: {"n": 0, "mw": 0.0, "mw_n": 0, "h": 0.0, "h_n": 0})
for r in rows:
    a = agg[r["country"]]
    a["n"] += 1
    try:
        if r["h100e_best"]:
            a["h"] += float(r["h100e_best"]); a["h_n"] += 1
    except (KeyError, ValueError):
        pass
    try:
        if r["power_capacity_mw"]:
            a["mw"] += float(r["power_capacity_mw"]); a["mw_n"] += 1
        elif r["it_load_mw"]:
            a["mw"] += float(r["it_load_mw"]); a["mw_n"] += 1
    except (KeyError, ValueError):
        pass

lines = ["| Country | Sites | MW (known) | H100e (known) |", "|---|---:|---:|---:|"]
for c, a in sorted(agg.items(), key=lambda kv: -kv[1]["n"]):
    mw = f"{a['mw']:,.0f}" if a["mw_n"] else "-"
    h = f"{a['h']:,.0f}" if a["h_n"] else "-"
    lines.append(f"| {c} | {a['n']} | {mw} | {h} |")
table = "\n".join(lines)

print(table)
open(OUT, "w", encoding="utf-8").write(table + "\n")
