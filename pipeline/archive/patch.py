"""Apply manual corrections to data/canonical/data_centers.csv (salvage artifacts)."""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
RAW = os.path.join(ROOT, "data", "raw", "data_centers_raw.csv")

# name -> {column: value} ; only listed keys are changed
FIX = {
    "AWS Project Rainier (New Carlisle)":        {"h100e_gpu": 170000, "h100e_third_party": ""},
    "Meta Prometheus (New Albany)":              {"h100e_gpu": 2250000, "h100e_third_party": ""},
    "Stargate Abilene (Lancium Clean Campus)":   {"h100e_gpu": 1012500, "h100e_third_party": ""},
    "Stargate Port Washington (Lighthouse)":     {"h100e_third_party": 2600000},
    "Stargate Saline Township (The Barn)":       {"h100e_third_party": 2900000},
    "Stargate Lordstown":                        {"h100e_third_party": 546000},
    "Stargate UAE":                              {"h100e_third_party": 2021000},
    "xAI Colossus 1":                            {"h100e_gpu": 247500, "h100e_third_party": ""},
    "xAI Colossus 2":                            {"h100e_gpu": 1100000, "h100e_third_party": ""},
    "xAI QTS Atlanta":                           {"announced_gpu_count": "", "gpu_types": "H100; A100 (11,000 H100 + 1,448 A100)", "cluster_peak_pflops": "", "h100e_gpu": 11456, "h100e_third_party": ""},
    "Nebius Mantsala":                           {"h100e_gpu": "", "h100e_third_party": 49000},
    "Deutsche Telekom Industrial AI Cloud":      {"it_load_mw": "", "announced_gpu_count": 10000, "cluster_peak_pflops": 500, "h100e_gpu": 22500},
    "HUMAIN Riyadh":                             {"it_load_mw": "", "announced_gpu_count": 18000, "h100e_gpu": 45000},
    "China Mobile Hohhot Intelligent Computing Center": {"it_load_mw": "", "announced_gpu_count": 10000, "cluster_peak_pflops": "", "h100e_gpu": 10000},
    "SoftBank DGX SuperPOD Tokyo":               {"it_load_mw": "", "announced_gpu_count": 4000, "h100e_gpu": 9000},
    "SK-AWS Ulsan AI Data Center":               {"it_load_mw": "", "announced_gpu_count": 60000, "h100e_gpu": 60000},
    "Foxconn Kaohsiung AI Factory":              {"it_load_mw": "", "announced_gpu_count": 10000, "h100e_gpu": 22500},
    "Yotta NM1 Navi Mumbai":                     {"it_load_mw": "", "announced_gpu_count": 20400, "h100e_gpu": 20400},
    "Cassava AI Factory Johannesburg":           {"it_load_mw": "", "announced_gpu_count": 3000, "h100e_gpu": 3000},
    "Nebius Vineland (DataOne campus)":          {"h100e_gpu": 375000, "h100e_third_party": ""},
    "Tesla Cortex (Giga Texas)":                 {"h100e_gpu": 230000, "h100e_third_party": ""},
    "Mistral Compute - Essonne (MDA)":           {"h100e_gpu": 40500, "h100e_third_party": ""},
    "Nscale Loughton AI Campus":                 {"h100e_gpu": 57600, "h100e_third_party": ""},
    "Stargate Norway - Kvandal":                 {"h100e_gpu": 225000, "h100e_third_party": ""},
    "Schwarz Group / Deutsche Telekom AI Gigafactory": {"latitude": 53.63, "longitude": 12.69, "power_capacity_mw": 240, "notes": "Announced 2025-2026; EUR5.6bn investment in 240MW data centre by 2033; coordinates are state-level centroid (site TBD)"},
}

rows = list(csv.DictReader(open(CANON, encoding="utf-8")))
n = 0
for r in rows:
    if r["name"] in FIX:
        for k, v in FIX[r["name"]].items():
            r[k] = str(v)
        n += 1

cols = ["name","operator","city","state_province","country","latitude","longitude",
        "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
        "cluster_peak_pflops","h100e_gpu","h100e_third_party","notes","source_url"]
with open(CANON, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print(f"Applied {n} corrections")
