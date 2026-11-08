"""Sixth pass (Nov 2026): source notes for the three heat-vs-IT warnings.

No numeric value changes. The cooling build flags these rows because the
accelerator heat it computes exceeds the IT load. Each note records what the
primary source says, so a reader can see which number to distrust.
"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
rows = list(csv.DictReader(open(PATH, encoding="utf-8", newline="")))
by_name = {r["name"]: r for r in rows}

NOTE = [
    ("Meta Prometheus (New Albany)",
     "Meta engineering post (19 Oct 2026): 'hundreds of thousands of GPUs' today, ~1 million at full scale, "
     "platforms GB200 NVL72 then GB300 NVL72, Vera Rubin NVL72 next; it gives no MW figure. "
     "The 695 MW comes from datacenter.fyi (aggregator) and the 1,000 MW is the 'gigawatt-scale' label. "
     "Meta's own rack figures (~120 kW per 72 GB200, ~135 kW per 72 GB300) put 1M GPUs at ~1.7-1.9 GW IT, "
     "so the full-scale count and the 1 GW figure do not agree"),
    ("JUPITER / JAIF (Exascale AI Factory)",
     "JSC (A. Herten, 2 Dec 2025): 5,884 Booster nodes x 4 GH200, superchip TDP 680 W, 17 MW limit (HPL); "
     "the 20 MW gross figure has no primary source"),
    ("Domyn Colosseum (iGenius AI Factory)",
     "The Next Web: 'drawing about 7MW', basis (gross or IT) not stated; 80 NVL72 racks at Meta's ~120 kW "
     "per 72 GB200 would draw ~9.6 MW IT, so the 7 MW is probably low"),
]

miss = 0
for name, text in NOTE:
    r = by_name.get(name)
    if r is None:
        print("MISS", name, "(no such row)"); miss += 1; continue
    if text in r["notes"]:
        print("SKIP", name, ":: note already present"); continue
    r["notes"] = r["notes"].rstrip("; ") + "; " + text
    print("OK  ", name, ":: notes +")

if miss:
    raise SystemExit(f"{miss} MISS - nothing written")
with open(PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("rows", len(rows))
