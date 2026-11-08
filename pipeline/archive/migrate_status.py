"""One-off migration (Nov 2026): move site status from the STATUS dict in
build.py into a `status` column in the canonical CSV.

Status was keyed by site name in code, so a renamed row silently became
`unknown`. The values come from data/published/data_centers.csv, which the
last build wrote from that dict, so the migration changes no status.
The column goes in just before `notes`.
"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
PUB = os.path.join(ROOT, "data", "published", "data_centers.csv")
VALID = {"operational", "partially_operational", "under_construction", "planned"}

rows = list(csv.DictReader(open(CANON, encoding="utf-8", newline="")))
cols = list(rows[0].keys())
if "status" in cols:
    raise SystemExit("canonical CSV already has a status column; nothing to do")

published = {r["name"]: r["status"] for r in csv.DictReader(open(PUB, encoding="utf-8", newline=""))}
bad = [r["name"] for r in rows if published.get(r["name"]) not in VALID]
if bad:
    raise SystemExit(f"{len(bad)} rows have no valid published status: {bad}")

for r in rows:
    r["status"] = published[r["name"]]

cols.insert(cols.index("notes"), "status")
with open(CANON, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("migrated", len(rows), "rows:", dict(sorted(counts.items())))
