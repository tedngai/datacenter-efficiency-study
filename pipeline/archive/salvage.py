"""Salvage mis-formatted rows in data/raw/data_centers_raw.csv -> data/canonical/data_centers.csv
Heuristics per data row (fields after country):
  lat, lon = first two numeric fields
  tail: last field = source_url (starts with http); longest remaining field = notes;
        remaining 'E' should be [power, it_load, gpu_count, gpu_types, pflops, h100e_gpu, h100e_3p]
        gpu_types = only non-numeric non-empty field; numeric slots filled positionally,
        extra trailing empties dropped / missing padded.
Prints full report for manual verification.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
RAW = os.path.join(ROOT, "data", "raw", "data_centers_raw.csv")

def is_num(s):
    try:
        float(s); return True
    except (ValueError, TypeError):
        return False

rows = list(csv.reader(open(RAW, encoding="utf-8")))
header, data = rows[0], rows[1:]
assert header[0] == "name"

fixed, problems = [], []
for f in data:
    if not f or not f[0]:
        continue
    name, operator, city, state, country = f[0], f[1], f[2], f[3], f[4]
    rest = f[5:]
    # first two numerics = lat, lon
    idx = [i for i, v in enumerate(rest) if is_num(v.strip())]
    if len(idx) < 2:
        problems.append((name, "no lat/lon")); continue
    lat, lon = rest[idx[0]], rest[idx[1]]
    tail = rest[idx[1]+1:]
    url = tail[-1].strip()
    if not url.startswith("http"):
        problems.append((name, f"url not last: {url[:60]}")); url = ""
    body = tail[:-1] if url else tail
    # longest field = notes
    notes = max(body, key=lambda s: len(s.strip())) if body else ""
    E = [v.strip() for v in body if v is not notes]
    # gpu_types: only non-numeric non-empty
    types = ""
    E2 = []
    for v in E:
        if v and not is_num(v) and v is not notes:
            if not types:
                types = v
            else:
                problems.append((name, f"second non-numeric in E: {v[:40]}"))
        else:
            E2.append(v)
    # trim trailing empties to <=6, pad to 6
    while len(E2) and len(E2) > 6 and E2[-1] == "":
        E2.pop()
    while len(E2) < 6:
        E2.append("")
    if len(E2) > 6:
        problems.append((name, f"E2 has {len(E2)} slots: {E2}"))
    power, it, gpu_count, pflops, h_gpu, h_3p = E2[:6]
    fixed.append([name, operator, city, state, country, lat, lon,
                  power, it, gpu_count, types, pflops, h_gpu, h_3p, notes, url])

with open(CANON, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(header)
    w.writerows(fixed)

print(f"fixed rows: {len(fixed)}  -> data/canonical/data_centers.csv\n")
if problems:
    print("PROBLEMS:")
    for p in problems: print("  ", p)
print("\n--- FULL REPORT (verify each line) ---")
for r in fixed:
    print(f"{r[0][:42]:42} | pwr={r[7]:>6} it={r[8]:>7} gpu={r[9]:>7} ty={r[10][:24]:24} pf={r[11]:>6} hG={r[12]:>8} h3={r[13]:>8} | {r[14][:70]}")
