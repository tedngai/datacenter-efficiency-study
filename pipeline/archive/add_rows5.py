"""Append US deep-dive rows: agent2 CSV (48 rows, mined Epoch AI) + agent1 uniques (16).
Drops CoreWeave Helios (Afton) - same campus as existing Galaxy Helios (Dickens County).
H100e factors: H100/H200/GH200=1.0, B200/GB200=2.25, GB300/B300=2.5, A100=0.315, L40S=0.19.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
RAW = os.path.join(ROOT, "data", "raw", "data_centers_raw.csv")

COLS = ["name","operator","city","state_province","country","latitude","longitude",
        "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
        "cluster_peak_pflops","h100e_gpu","h100e_third_party","notes","source_url"]

STATE = {"TX":"Texas","OH":"Ohio","NC":"North Carolina","AZ":"Arizona","NE":"Nebraska",
         "IA":"Iowa","MN":"Minnesota","ID":"Idaho","UT":"Utah","WY":"Wyoming",
         "NM":"New Mexico","AL":"Alabama","OR":"Oregon","VA":"Virginia",
         "MS":"Mississippi","PA":"Pennsylvania","ND":"North Dakota","GA":"Georgia"}

def row(name, operator, city, state, country, lat, lon, power=None, it=None,
        gpu=None, types=None, pflops=None, h_gpu=None, h_3p=None, notes="", url=""):
    return {
        "name": name, "operator": operator, "city": city, "state_province": state,
        "country": country, "latitude": lat, "longitude": lon,
        "power_capacity_mw": power, "it_load_mw": it, "announced_gpu_count": gpu,
        "gpu_types": types or "", "cluster_peak_pflops": pflops, "h100e_gpu": h_gpu,
        "h100e_third_party": h_3p, "notes": notes, "source_url": url,
    }

# --- agent 2 rows (from missing_us_ai_datacenters_subagent.csv) ---
file_rows = list(csv.DictReader(open("missing_us_ai_datacenters_subagent.csv", encoding="utf-8")))
DROP = {"CoreWeave Helios (Afton)"}  # dup of existing Galaxy Helios (Dickens County)
rows_from_file = []
for r in file_rows:
    if r["name"] in DROP:
        continue
    # repair shifted-column rows from the subagent CSV
    repairs = {
        "Google Haskell County (Homebound/Thelma)": {},
        "Google Wilbarger County": {},
        "Google Pampa": {},
        "Cipher Apollo": {},
        "MARA Matagorda County": {},
        "Bitdeer Milam County": {},
        "Bitdeer Clarington": {},
        "Crusoe Project Jade": {},
        "Bitfarms Panther Creek": {},
        "Riot Corsicana": {},
        "Cipher Black Pearl": {},
        "Core Scientific Pecos (future colocation)": {},
        "MARA Granbury": {},
    }
    if r["name"] in repairs:
        if r["name"] == "Google Haskell County (Homebound/Thelma)":
            r["notes"] = r["h100e_third_party"]; r["source_url"] = "https://datacenters.google/locations/texas/"
        elif r["name"] == "Google Wilbarger County":
            r["notes"] = r["h100e_gpu"]; r["source_url"] = r["h100e_third_party"]
        elif r["name"] == "Google Pampa":
            r["notes"] = r["h100e_gpu"]; r["source_url"] = r["h100e_third_party"]
        elif r["name"] == "Cipher Apollo":
            _u = r["notes"]; r["notes"] = r["h100e_third_party"]; r["source_url"] = _u
        elif r["name"] == "MARA Matagorda County":
            _u = r["notes"]; r["notes"] = r["h100e_third_party"]; r["source_url"] = _u
        elif r["name"] == "Bitdeer Milam County":
            r["notes"] = r["h100e_gpu"]; r["source_url"] = r["h100e_third_party"]
        elif r["name"] == "Bitdeer Clarington":
            _u = r["notes"]; r["notes"] = r["h100e_third_party"]; r["source_url"] = _u
        elif r["name"] == "Crusoe Project Jade":
            _u = r["notes"]; r["notes"] = r["h100e_third_party"]; r["source_url"] = _u
        elif r["name"] == "Bitfarms Panther Creek":
            _u = r["notes"]; r["notes"] = r["h100e_third_party"]; r["source_url"] = _u
        elif r["name"] == "Riot Corsicana":
            r["gpu_types"] = r["cluster_peak_pflops"]; r["cluster_peak_pflops"] = ""
            r["notes"] = r["source_url"]; r["source_url"] = "https://www.datacenterdynamics.com/en/news/riot-platforms-files-to-add-building-to-cryptomine-and-data-center-campus-in-corsicana-texas/"
        elif r["name"] == "Cipher Black Pearl":
            r["gpu_types"] = r["cluster_peak_pflops"]; r["cluster_peak_pflops"] = ""
            r["notes"] = r["source_url"]; r["source_url"] = "https://baxtel.com/data-center/cipher-digital-black-pearl"
        elif r["name"] == "Core Scientific Pecos (future colocation)":
            r["gpu_types"] = r["cluster_peak_pflops"]; r["cluster_peak_pflops"] = ""
            r["notes"] = r["source_url"]; r["source_url"] = "https://investors.corescientific.com/sec-filings/all-sec-filings/content/0001140361-25-039864/ef20057996_ex99-1.htm"
        elif r["name"] == "MARA Granbury":
            r["gpu_types"] = r["cluster_peak_pflops"]; r["cluster_peak_pflops"] = ""
            r["notes"] = r["source_url"]; r["source_url"] = "https://www.jain.com/analysis/claims/marathon-digital-granbury-texas-facility-capacity-and-ai-integration/"
        r["h100e_gpu"] = ""; r["h100e_third_party"] = "" if r["name"] not in () else r["h100e_third_party"]
    if r["name"] == "AWS Ridgeland":
        r["notes"] += " NOTE: possibly overlapping with our existing 'AWS Madison County (Canton & Ridgeland)' row - kept because Epoch lists it as a distinct campus at 1626 County Line Rd."
    if r["city"] == "san Antonio area":
        r["city"] = "San Antonio area"
    if r["state_province"] in STATE:
        r["state_province"] = STATE[r["state_province"]]
    for k in ("h100e_gpu", "h100e_third_party"):
        if r[k]:
            r[k] = str(int(float(r[k])))
    rows_from_file.append(r)

# --- agent 1 rows not present in the file ---
ROWS = [
row("Google Storey County","Google","Storey County (Tahoe Reno Industrial Center)","Nevada","USA",39.53,-119.55,it=161,types="TPU v4; v5e; v5p; v6e",h_3p=133906,
    notes="Operating Google campus in TRIC; Epoch AI: 161MW IT / ~134k H100e",url="https://datacenters.google/locations/storey-county-nevada/"),
row("Google Cedar Rapids (Big Cedar)","Google","Cedar Rapids","Iowa","USA",41.94,-91.68,power=600,
    notes="New Google campus in Big Cedar Industrial Center; MISO new-load filing shows 600MW for Google; multiple buildings",url="https://epoch.ai/data/ai-data-centers/directory"),
row("Google Fort Wayne","Google","Fort Wayne","Indiana","USA",41.12,-84.90,
    notes="Under construction; multi-building campus, capacity undisclosed; part of Google $10B Indiana investment",url="https://www.thelocalfw.com/what-to-know-about-googles-plans-for-wetlands-in-fort-wayne/"),
row("Meta Bowling Green","Meta","Bowling Green","Ohio","USA",41.36,-83.66,types="NVIDIA B300; Vera Rubin",
    notes="New Meta northwest Ohio campus (Middleton Pike) with new Williams Apollo gas generation project; planned/under construction",url="https://epoch.ai/data/ai-data-centers/directory"),
row("Meta El Paso","Meta","El Paso","Texas","USA",31.80,-106.40,power=1000,
    notes="Announced Jul 2026 with Meta-BlackRock venture; $10B+ campus, 1GW of compute, online from 2028 (coords approximate)",url="https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Announces-New-Strategic-Venture-with-BlackRock-to-Develop-Data-Center-in-El-Paso/default.aspx"),
row("Microsoft Pecos","Microsoft","Pecos","Texas","USA",31.42,-103.49,power=2000,
    notes="Announced Jun 2026 as one of Microsoft's largest single capacity additions (~2GW); multibillion-dollar AI/cloud campus over 5-7 years; distinct from Core Scientific's 200MW Pecos bitcoin-site conversion (coords approximate)",url="https://blogs.microsoft.com/blog/2026/06/22/powering-the-next-wave-of-ai-expanding-capacity-with-our-new-datacenter-in-pecos/"),
row("QTS Cedar Rapids (Big Cedar)","QTS (SNA LLC; reported Meta tenant)","Cedar Rapids","Iowa","USA",41.92,-91.72,power=616,types="NVIDIA B300; Vera Rubin",
    notes="MISO new-load filing shows 616MW for shell entity SNA LLC at Big Cedar Industrial Center; SemiAnalysis reports Meta as tenant; NOTE: separate filing from Google's 600MW at the same industrial center - possible overlap, verify",url="https://epoch.ai/data/ai-data-centers/directory"),
row("QTS Eagle Mountain","QTS","Eagle Mountain","Utah","USA",40.32,-112.01,types="NVIDIA B300",
    notes="QTS campus at 652 E Hyperscale Way next to Meta's Utah site; reported Meta tenant (speculative); capacity unpublished",url="https://q.com/data-centers/eagle-mountain/"),
row("AWS Richmond County","Amazon Web Services","Richmond County (Hamlet area)","North Carolina","USA",34.95,-79.66,
    notes="$10B AWS campus announced Jun 2025 to expand AI/cloud infrastructure; power and coordinates unpublished (approximate)",url="https://www.aboutamazon.com/news/aws/aws-investment-north-carolina-ai-cloud-infrastructure"),
row("AWS Georgia (Butts & Douglas Counties)","Amazon Web Services","Jackson / Douglasville","Georgia","USA",33.31,-83.96,
    notes="$11B AWS expansion announced Jan 2025 for AI/cloud across Butts and Douglas county campuses; coordinates approximate (Butts County)",url="https://www.aboutamazon.com/news/aws/aws-investment-georgia-ai-cloud-infrastructure"),
row("AWS Dobbins Campus (Laveen)","Amazon Web Services","Phoenix (Laveen)","Arizona","USA",33.32,-112.17,
    notes="Amazon Data Services bought 220 acres near Loop 202/W Dobbins Rd for $277M (Dec 2024); SRP South Mountain transmission project provides 1,200MW corridor; planned",url="https://baxtel.com/data-center/amazon-dobbins-campus"),
row("Vantage VA4 (Fredericksburg)","Vantage Data Centers","Stafford County (Fredericksburg region)","Virginia","USA",38.42,-77.41,it=192,
    notes="$2B, 192MW IT campus announced Nov 2025; Vantage's 4th Virginia campus (782MW statewide) serving cloud and AI demand (coords approximate)",url="https://vantage-dc.com/news/vantage-data-centers-invests-2b-in-fredericksburg-virginia-region-to-deliver-fourth-campus-in-the-commonwealth/"),
row("Switch Citadel (Tahoe Reno Campus)","Switch","McCarran (Storey County)","Nevada","USA",39.53,-119.43,power=650,
    notes="2,000-acre Citadel Campus designed for up to 650MW / 7.2M sq ft; high-density AI/HPC-capable superscale colocation; tenant mix undisclosed",url="https://www.switch.com/switch-tahoe-reno-data-center-now-open/"),
row("CloudBurst San Marcos Gigacenter","CloudBurst Data Centers","San Marcos","Texas","USA",29.88,-97.94,power=1200,
    notes="Flagship 1.2GW AI/high-density campus with behind-the-meter gas plant and Energy Transfer gas contract (450k MMBtu/day); under development",url="https://cloudburstdc.com/data-centers/"),
row("CloudBurst Oklahoma City Campus","CloudBurst Data Centers","Oklahoma City","Oklahoma","USA",35.46,-97.54,power=200,
    notes="70+ acre AI/HPC campus; 30MW grid ready-for-service Q4 2026 growing to 200MW, four 50MW buildings, 150kW+ racks (coords approximate)",url="https://cloudburstdc.com/data-centers/"),
row("Fermi America HyperGrid (Project Matador)","Fermi America","Amarillo","Texas","USA",35.35,-101.56,power=11000,
    notes="~5,800-acre Advanced Energy and Intelligence Campus adjacent to Pantex with Texas Tech; up to 11GW IT from nuclear/gas/solar, 18M sq ft; largest US private-grid AI campus proposal; planned, phased from ~2026 (coords approximate)",url="https://www.texastech.edu/stories/25-06-ttu-system-and-fermi-america-announce-partnership.php"),
]

# ---- validate + append ----
existing = list(csv.DictReader(open(CANON, encoding="utf-8")))
names = {r["name"] for r in existing}
added = 0
for r in rows_from_file + ROWS:
    if r["name"] in names:
        print(f"SKIP duplicate: {r['name']}")
        continue
    for k, v in r.items():
        if k in {"latitude","longitude","power_capacity_mw","it_load_mw","announced_gpu_count",
                 "cluster_peak_pflops","h100e_gpu","h100e_third_party"} and v is not None:
            r[k] = str(v)
        elif v is None:
            r[k] = ""
    names.add(r["name"])
    for extra in set(r) - set(COLS):
        del r[extra]
    existing.append(r)
    added += 1

with open(CANON, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(existing)

from collections import Counter
c = Counter(r["state_province"] for r in rows_from_file + ROWS)
print(f"Added {added} rows. By state: {dict(sorted(c.items()))}")
print(f"Total rows now: {len(existing)}")
