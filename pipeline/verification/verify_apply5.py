"""Fifth pass (Nov 2026 review): make H100e conversions follow the stated rules.

Each edit names the row, the column, the value we expect to find, and the new
value. The script refuses an edit if the current value differs (MISS), so a
re-run or a stale expectation cannot overwrite data silently.

Rule applied (clarifies D-003):
  * One accelerator model, or several models that share one factor
    -> count x factor.
  * Several models with a published per-model breakdown
    -> sum of (count x factor) per model.
  * Several models with different factors and no breakdown
    -> h100e_gpu blank; h100e_best falls back to the next method.
  * A third-party H100e estimate (Epoch AI etc.) goes in h100e_third_party,
    never in h100e_gpu, even when the third party derived it from GPU counts.
"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
rows = list(csv.DictReader(open(PATH, encoding="utf-8", newline="")))
by_name = {r["name"]: r for r in rows}

# (name, column, expected current value, new value)
SET = [
    # --- mixed generations without a breakdown -> blank h100e_gpu ---
    ("Meta Prometheus (New Albany)", "h100e_gpu", "2250000", ""),
    ("Stargate Norway - Kvandal", "h100e_gpu", "225000", ""),
    ("KISTI National Supercomputing Center (HANGANG No.6)", "h100e_gpu", "8000", ""),
    ("Data Vault Pakistan AI Data Center", "h100e_gpu", "100", ""),
    ("China Telecom Zhongwei Computing Hub Data Center", "h100e_gpu", "10500", ""),
    ("China Mobile Hohhot Intelligent Computing Center", "h100e_gpu", "7000", ""),
    # --- xAI Colossus 1: breakdown is an Epoch estimate -> third party;
    #     old value 247,500 did not match any breakdown ---
    ("xAI Colossus 1", "h100e_gpu", "247500", ""),
    ("xAI Colossus 1", "h100e_third_party", "", "267500"),
    # --- wrong factor: GB300 is 2.5, not 2.25 ---
    ("Foxconn Kaohsiung AI Factory", "h100e_gpu", "22500", "25000"),
    # --- GPU count recorded but never converted ---
    ("Fairwater Atlanta", "h100e_gpu", "", "337500"),
    ("Firmus Southgate Melbourne", "h100e_gpu", "", "46000"),
    ("Vultr Springfield AI Supercluster", "h100e_gpu", "", "60000"),
    # --- breakdown known but count column blank ---
    ("xAI QTS Atlanta", "announced_gpu_count", "", "12448"),
    # --- Epoch AI estimates mis-filed as GPU-count conversions ---
    ("DayOne Nusajaya", "h100e_gpu", "584000", ""),
    ("DayOne Nusajaya", "h100e_third_party", "", "584000"),
    ("DayOne Kempas", "h100e_gpu", "481000", ""),
    ("DayOne Kempas", "h100e_third_party", "", "481000"),
    ("Huawei Wuhu", "h100e_gpu", "97000", ""),
    ("Huawei Wuhu", "h100e_third_party", "", "97000"),
    ("Huawei Horinger", "h100e_gpu", "89000", ""),
    ("Huawei Horinger", "h100e_third_party", "", "89000"),
    ("Alibaba Zhangbei", "h100e_gpu", "32000", ""),
    ("Alibaba Zhangbei", "h100e_third_party", "", "32000"),
    # --- power fields ---
    # Note gives 340 MW IT + 300+ MW IT; 640 is IT load, not gross power.
    ("Fairwater Atlanta", "power_capacity_mw", "640", ""),
    ("Fairwater Atlanta", "it_load_mw", "", "640"),
    # Gross 300 MW < IT 315 MW is impossible; 300 has no source in the note.
    ("Nebius Vineland (DataOne campus)", "power_capacity_mw", "300", ""),
    # 1,289 MW IT is an aggregator figure (dcmap.us) with no primary source;
    # per-building trackers show ~48 MW per building. Keep it in notes only.
    ("Meta Prineville", "it_load_mw", "1289", ""),
]

# (name, text appended to notes)
NOTE = [
    ("Meta Prometheus (New Albany)", "H100e: GB200/GB300 mix with no per-model split, so no GPU-count conversion; best estimate uses 695 MW IT"),
    ("Stargate Norway - Kvandal", "H100e: GB300/Rubin mix with no per-model split, so no GPU-count conversion"),
    ("KISTI National Supercomputing Center (HANGANG No.6)", "H100e: H200/B200 mix with no per-model split, so no GPU-count conversion"),
    ("Data Vault Pakistan AI Data Center", "H100e: four GPU models with no per-model split, so no GPU-count conversion"),
    ("China Telecom Zhongwei Computing Hub Data Center", "H100e: heterogeneous cards with no per-model split, so no GPU-count conversion (was 0.35 Ascend assumption)"),
    ("China Mobile Hohhot Intelligent Computing Center", "H100e: card mix not published, so no GPU-count conversion (was 0.35 Ascend assumption)"),
    ("xAI Colossus 1", "H100e third-party = 150k x 1.0 + 50k x 1.0 + 30k B200 x 2.25 from the Epoch breakdown"),
    ("Foxconn Kaohsiung AI Factory", "H100e uses the GB300 factor 2.5 per gpu_types"),
    ("Fairwater Atlanta", "H100e = 150,000 GB200 x 2.25 (DC-10 only, so a floor for the campus); 640 MW is IT load (340 + 300)"),
    ("Firmus Southgate Melbourne", "H100e = 18,400 GB300 x 2.5"),
    ("Vultr Springfield AI Supercluster", "H100e = 24,000 x 2.5 (MI355X dense OCP-FP8 5.0 PF per AMD spec / 1.979 = 2.54, rounded like B300)"),
    ("xAI QTS Atlanta", "H100e = 11,000 x 1.0 + 1,448 A100 x 0.315"),
    ("Nebius Vineland (DataOne campus)", "Gross power not published (earlier 300 MW was below the 315 MW IT figure)"),
    ("Meta Prineville", "1,289 MW IT figure is from dcmap.us (aggregator), unverified and in conflict with per-building trackers (~48 MW per building); no H100e estimate until a primary source exists; 'AI training site' is a press description"),
    ("SK Broadband Gasan AI Data Center", "H100e counts the 1,032 B200 only (H100 count not published), so it is a floor"),
    ("NHN Cloud Gwangju National AI Data Center", "H100e counts the 1,000 H100 only (other accelerators not counted), so it is a floor"),
    ("LG AI Research AEX cluster (LG Science Park)", "H100e counts the 512 H100 only (A100 count not published), so it is a floor"),
    ("Start Campus SINES Data Campus", "H100e counts the 12,600 GB300 only; Vera Rubin GPUs from 2027 not included"),
]

# Country names: common English short form, no abbreviations (AGENTS.md §5).
COUNTRY = {"USA": "United States", "UK": "United Kingdom"}

miss = 0
for name, col, old, new in SET:
    r = by_name.get(name)
    if r is None:
        print("MISS", name, "(no such row)"); miss += 1; continue
    if r[col] != old:
        print(f"MISS {name} :: {col} expected {old!r} found {r[col]!r}"); miss += 1; continue
    r[col] = new
    print(f"OK   {name} :: {col} {old!r} -> {new!r}")

for name, text in NOTE:
    r = by_name.get(name)
    if r is None:
        print("MISS", name, "(no such row)"); miss += 1; continue
    if text in r["notes"]:
        print("SKIP", name, ":: note already present"); continue
    r["notes"] = (r["notes"].rstrip("; ") + "; " + text) if r["notes"] else text
    print(f"OK   {name} :: notes +")

n_country = 0
for r in rows:
    if r["country"] in COUNTRY:
        r["country"] = COUNTRY[r["country"]]; n_country += 1
print(f"OK   country renamed on {n_country} rows")

if miss:
    raise SystemExit(f"{miss} MISS - nothing written")

with open(PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("rows", len(rows))
