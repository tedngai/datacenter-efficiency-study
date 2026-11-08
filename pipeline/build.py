"""
Build final dataset (data/published/data_centers.csv + .json + index.html)
from data/canonical/data_centers.csv.

H100e methodology (documented in README.md):
- h100e_gpu:     converted from announced GPU counts using dense-FP8 compute ratios vs H100
- h100e_third_party: third-party estimates (e.g. Epoch AI) recorded during research
- h100e_flops:   announced cluster peak PFLOPS (dense FP8-equivalent) / 1.979 PFLOPS per H100
- h100e_power:   power-based estimate: 60% of IT load assumed to power H100-class
                 accelerator systems at ~1.2 kW per GPU  =>  500 H100e per MW of IT load
- h100e_best:    most confident available estimate (gpu > third_party > flops > power)
"""
import csv, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
PUBLISHED = os.path.join(ROOT, "data", "published")
OUT_CSV = os.path.join(PUBLISHED, "data_centers.csv")
OUT_JSON = os.path.join(PUBLISHED, "data_centers.json")
OUT_HTML = os.path.join(ROOT, "index.html")
os.makedirs(PUBLISHED, exist_ok=True)

COLS = ["name","operator","city","state_province","country","latitude","longitude",
        "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
        "cluster_peak_pflops","h100e_gpu","h100e_third_party","status","notes","source_url"]
STATUSES = {"operational", "partially_operational", "under_construction", "planned"}
NUMERIC = {"latitude","longitude","power_capacity_mw","it_load_mw","announced_gpu_count",
           "cluster_peak_pflops","h100e_gpu","h100e_third_party"}

def num(s):
    s = (s or "").strip()
    if not s:
        return None
    return float(s)

rows = list(csv.DictReader(open(RAW, encoding="utf-8")))
print(f"Parsed {len(rows)} rows from raw CSV")

# ---- validation ----
for i, r in enumerate(rows):
    if set(r.keys()) != set(COLS):
        raise SystemExit(f"Row {i+2} ({r.get('name','?')}) has bad columns: {list(r.keys())}")
    for c in NUMERIC:
        v = (r[c] or "").strip()
        if v:
            try:
                float(v)
            except ValueError:
                raise SystemExit(f"Row {i+2} ({r['name']}): non-numeric {c}={v!r}")
    if not r["source_url"].startswith("http"):
        raise SystemExit(f"Row {i+2} ({r['name']}): source_url missing -> column misalignment? got {r['source_url']!r}")
    if r["status"] not in STATUSES:
        raise SystemExit(f"Row {i+2} ({r['name']}): status must be one of {sorted(STATUSES)}, got {r['status']!r}")
    if not r["name"]:
        raise SystemExit(f"Row {i+2}: missing name")
    if (r["latitude"] == "" or r["longitude"] == "") and r["name"]:
        print(f"  WARN: no coordinates: {r['name']}")

# ---- derived H100e columns ----
out = []
for r in rows:
    power = num(r["power_capacity_mw"])
    it = num(r["it_load_mw"])
    gpu_count = num(r["announced_gpu_count"])
    pflops = num(r["cluster_peak_pflops"])
    h_gpu = num(r["h100e_gpu"])
    h_3p = num(r["h100e_third_party"])

    # effective IT load: measured if available, else assume PUE 1.2 from gross capacity
    it_effective = it if it is not None else (power / 1.2 if power else None)
    h_power = round(it_effective * 500) if it_effective else None
    h_flops = round(pflops / 1.979) if pflops else None

    candidates = [("gpu_count", h_gpu), ("third_party", h_3p), ("flops", h_flops), ("power", h_power)]
    h_best, h_method = next(((v, m) for m, v in candidates if v), (None, ""))

    status = r["status"]
    out.append({
        "name": r["name"], "operator": r["operator"], "city": r["city"],
        "state_province": r["state_province"], "country": r["country"],
        "latitude": num(r["latitude"]), "longitude": num(r["longitude"]),
        "power_capacity_mw": power, "it_load_mw": it,
        "announced_gpu_count": gpu_count, "gpu_types": r["gpu_types"],
        "cluster_peak_pflops": pflops,
        "h100e_gpu": h_gpu, "h100e_third_party": h_3p,
        "h100e_flops": h_flops, "h100e_power": h_power,
        "h100e_best": h_best, "h100e_method": h_method,
        "status": status, "status_note": r["notes"], "source_url": r["source_url"],
    })

out.sort(key=lambda x: x["h100e_best"] or 0, reverse=True)

# ---- shared map points ----
# Many rows carry a city-centre point instead of the campus location (seven
# Riyadh sites share one point). Count the other sites within ~1 km (2 dp), so
# the dashboard and readers can see that the point is approximate.
point_count = {}
for o in out:
    if o["latitude"] is not None and o["longitude"] is not None:
        key = (round(o["latitude"], 2), round(o["longitude"], 2))
        point_count[key] = point_count.get(key, 0) + 1
for o in out:
    if o["latitude"] is None or o["longitude"] is None:
        o["location_shared_with"] = None
    else:
        o["location_shared_with"] = point_count[(round(o["latitude"], 2), round(o["longitude"], 2))] - 1

final_cols = ["name","operator","city","state_province","country","latitude","longitude",
              "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
              "cluster_peak_pflops","h100e_gpu","h100e_third_party","h100e_flops",
              "h100e_power","h100e_best","h100e_method","status","status_note","source_url",
              "location_shared_with"]

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=final_cols)
    w.writeheader()
    w.writerows(out)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

# ---- index.html (self-contained interactive dashboard) ----
# Bundling lives in dashboard.py so build_gpu_cooling.py can refresh the page
# after it regenerates the cooling dataset.
import dashboard  # noqa: E402  (same directory, after the data is written)

dashboard.render()

status_counts = {}
for o in out:
    status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1
print("Status breakdown:", dict(sorted(status_counts.items())))

# ---- summary ----
with_data = [o for o in out if o["h100e_best"]]
print(f"\nWrote {OUT_CSV}, {OUT_JSON}, {OUT_HTML}")
print(f"Sites: {len(out)} | with H100e estimate: {len(with_data)} | total H100e: {sum((o['h100e_best'] or 0) for o in out):,.0f}")
print("\nTop 15 by best H100e estimate:")
for o in out[:15]:
    print(f"  {o['h100e_best']:>10,.0f}  {o['name']} ({o['h100e_method']})")
