"""Apply verification corrections to us_utility_impacts.csv and add a verification grade.

Prices re-based on EIA annual data:
  - 2021 and 2024 from EIA Electric Power Annual Table 2.10 (2021, 2025 editions)
  - 2025 from EPA 2025 (Table 2.10)
  - 2026 YTD from EEM Table 5.6.B (Jan-Aug 2026)
Water/rate claims checked against primary sources (Google 2026 Environmental
Report p.97, SCC orders, PJM BRA, utility filings, local reporting).
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "us_utility_impacts.csv")
rows = list(csv.DictReader(open(PATH, encoding="utf-8")))

# (region substring, field, old, new)
FIXES = [
    ("Virginia — NoVA", "energy_price_trend_2021_2026",
     "~11.0¢/kWh 2021 → 15.2¢ 2025 (EIA-861) → ~17.6¢ mid-2026 (~+30-60%). Jan 2026 order:",
     "11.96¢/kWh 2021 → 15.28¢ 2025 → 16.95¢ 2026 YTD (EIA annual; +41.7% 2021→2026). Jan 2026 order:"),
    ("Georgia — Atlanta", "energy_price_trend_2021_2026",
     "~11.7¢ (2021) → 15.48¢ (2024) → 17.55¢ (PSC 500-kWh survey); typical customer ~$43/mo more than 2022.",
     "12.51¢ (2021) → 14.74¢ (2025) → 15.48¢ (2026 YTD) per EIA; Georgia PSC 500-kWh survey = $87.75 (17.55¢) for Georgia Power; typical customer ~$43/mo more than 2022."),
    ("Tennessee — Memphis", "energy_price_trend_2021_2026",
     "~10.5-11¢ (2021) → ~13¢ (2026)",
     "TN 11.07¢ (2021) → 13.22¢ (2025) → 13.80¢ (2026 YTD) per EIA; MLGW ~13¢ (2026)"),
    ("Mississippi — Jackson", "energy_price_trend_2021_2026",
     "~11¢ (2021) → 13.21¢ (2024-25) → ~16.5¢ (Feb 2026; ~$165/mo typical bill, +$14.22 incl. DC-related rider).",
     "11.56¢ (2021) → 14.03¢ (2025) → 15.06¢ (2026 YTD) per EIA; Entergy's Feb 2026 monthly figure ~16.5¢ (~$165/mo typical, +$14.22 incl. DC rider)."),
    ("Alabama — Montgomery", "energy_price_trend_2021_2026",
     "~13.09¢ (2021) → 16.77¢ (2024) — above 16.48¢ US avg; highest avg residential bills of the 100 largest US utilities (2024).",
     "12.96¢ (2021) → 16.09¢ (2025) per EIA — still below the 17.23¢ US average, but high household usage gives among the highest total bills (highest of the 100 largest utilities in 2024, per ICN)."),
    ("Arkansas — West Memphis", "energy_price_trend_2021_2026",
     "~9.9¢ (2021) → ~14.37¢ (Aug 2026).",
     "11.27¢ (2021) → 12.87¢ (2025) → 13.74¢ (2026 YTD) per EIA; Entergy cites 14.37¢ for Aug 2026."),
    ("Arizona — West Valley", "energy_price_trend_2021_2026",
     "AZ ~11.7¢ (2021) → ~13.5-14¢ (2025-26).",
     "AZ 12.54¢ (2021) → 15.26¢ (2025) → 15.36¢ (2026 YTD) per EIA."),
    ("Nevada — Las Vegas", "energy_price_trend_2021_2026",
     "NV ~11.4¢ (2021) → ~13-14¢ (2025).",
     "NV 11.49¢ (2021) → 13.26¢ (2025) → 13.36¢ (2026 YTD) per EIA."),
    ("Pennsylvania — Berwick", "energy_price_trend_2021_2026",
     "PA ~13¢ (2021) → ~17-18¢ (2025).",
     "PA 13.76¢ (2021) → 19.29¢ (2025) → 21.13¢ (2026 YTD) per EIA."),
    ("Wyoming — Cheyenne", "energy_price_trend_2021_2026",
     "WY residential 9.14¢ (2024), +27% since 2012, still ~24% below national avg.",
     "WY 11.17¢ (2021) → 13.37¢ (2025) → 14.01¢ (2026 YTD) per EIA (still below the US average). The widely cited '9.14¢ in 2024' figure could not be reconciled with EIA and was dropped."),
    ("Utah — Eagle Mountain", "energy_price_trend_2021_2026",
     "UT residential ~10-11¢/kWh (2021) rising to ~12¢/kWh (2025) per EIA (approximate).",
     "UT 10.43¢/kWh (2021) → 13.02¢ (2025) → 13.19¢ (2026 YTD) per EIA."),
    ("Idaho — Kuna", "energy_price_trend_2021_2026",
     "ID residential ~9-10¢/kWh (2021) to ~11-12¢/kWh (2026) per EIA/IDACORP chart (approximate; IDACORP says prices 20-30% below national average).",
     "ID 10.16¢/kWh (2021) → 11.83¢ (2025) → 13.02¢ (2026 YTD) per EIA (IDACORP says prices 20-30% below national average)."),
    ("New Mexico — Los Lunas", "energy_price_trend_2021_2026",
     "NM residential ~13-14¢/kWh 2025 (approximate).",
     "NM 13.52¢/kWh (2021) → 14.85¢ (2025) → 15.34¢ (2026 YTD) per EIA."),
    ("Oregon — The Dalles", "energy_price_trend_2021_2026",
     "PNW residential ~11¢/kWh (2021) → ~14-15¢ (2025) regional.",
     "OR 11.37¢/kWh (2021) → 15.46¢ (2025) → 15.46¢ (2026 YTD) per EIA."),
    ("Iowa — Des Moines", "energy_price_trend_2021_2026",
     "residential 11.2¢/kWh in 2025 vs Iowa state avg 13.6¢ (electricrates.org)",
     "residential 11.2¢/kWh in 2025 (utility-specific) vs Iowa state avg 13.62¢ (EIA 2025)"),
    ("Texas — Oncor", "energy_price_trend_2021_2026",
     "Texas residential avg (EIA): 12.11c/kWh 2021, 13.76c 2022, 14.46c 2023, 14.94c 2024, 15.47c 2025, ~16.99c/kWh Apr 2026",
     "Texas residential avg (EIA): 12.11c/kWh 2021, 14.94c 2024, 15.40c 2025, 16.03c 2026 YTD (16.99c was an April 2026 monthly peak)"),
    ("Wisconsin — Mount Pleasant", "energy_price_trend_2021_2026",
     "April 2026: new request for 2027-28 of +$347.1M electric (+9.3%; residential +16.3%; typical bill $144→~$166 by 2028).",
     "April 2026: request for 2027-28 (+$347.1M; residential +10.28% in 2027 and +5.52% in 2028, ~+16.4% cumulative; typical bill ~$144→$166)."),
    ("Texas — Panhandle", "water_consumption",
     "max 2.5M gpd from city at ~$8.72/1,000 gal (double the standard rate)",
     "max 2.5M gpd from city at $8.72/1,000 gal — the highest industrial rate Amarillo has ever charged"),
    ("Arizona — West Valley", "water_consumption",
     "Microsoft Goodyear: 2023 council amendment allows 1.2M gal/day at full build-out (agreement wording allows up to 3M gal/day delivered);",
     "Microsoft Goodyear: 2023 council amendment gives 1.2M gpd of wastewater capacity at full build-out (Microsoft paid $36M toward the $90M 157th Ave plant); original water-cooling plan was up to 5M gpd, and buildings 4-5 switched to air cooling;"),
    ("Arizona — West Valley", "water_consumption",
     "Business Insider (Jun 2025) cited city docs planning 1M gal/day per building x5 buildings = 1.83B gal/yr; actual use withheld as 'proprietary'",
     "BI (2025) reported the original plan as 1M gpd per building (5M gpd / 1.83B gal-yr at full build-out), now superseded by air cooling for later buildings; actual use withheld as 'proprietary'"),
    ("Iowa — Des Moines", "water_consumption",
     "Google Council Bluffs: ~1.4 billion gallons withdrawn in 2024 (National Wildlife Federation / company reporting)",
     "Google Council Bluffs: 1,746.4M gal withdrawn / 1,346.0M consumed in 2025 (Google 2026 Environmental Report p.97)"),
    ("Ohio — Columbus", "water_consumption",
     "Google New Albany ~127M gal/yr; city exploring recycled-water supply.",
     "Google New Albany 1,008.1M gal withdrawn / 835.7M consumed in 2025 (Lancaster 307.1/135.8; Lockbourne 460.8/359.5); city exploring recycled-water supply."),
    ("Mississippi — Jackson", "water_consumption",
     "annual average ~93 million gallons/year (0.25 MGD) but contracted hottest-day peak of 3.67 MGD cooling discharge - ~14x the annual average and ~82% of the 4.5 MGD peak-day capacity of the city system serving it",
     "annual average ~93 million gallons/year (0.25 MGD); peak-day demand reported at ~3.7 MGD (~82% of the 4.5 MGD city system peak) - this specific figure was NOT found in the service-agreement text, so treat it as unverified"),
    ("Tennessee — Memphis", "water_consumption",
     "MLGW contract for 1.3 million gallons/day of drinking water; permitted up to 1.28 MGD",
     "contract demand reported at 1.3 MGD (paywalled Commercial Appeal; unverified); permitted up to 1.28 MGD"),
    ("Virginia — NoVA", "water_consumption",
     "2023 DC potable use ~899M-1.0B gal (+250% vs 2019; FWW claims 1.6B incl. all uses — contested). Reclaimed system: 736M gal 2024.",
     "2023 DC potable use 899M gal PLUS 815M gal reclaimed (>1B total; +250% vs 2019 per Grist; FWW claims 1.6B incl. all uses — contested). Reclaimed system delivered 750M+ gal to ~40 customers in 2025."),
]

for region_sub, field, old, new in FIXES:
    hits = [r for r in rows if region_sub in r["region"]]
    if not hits:
        print("MISS REGION:", region_sub); continue
    done = False
    for r in hits:
        if old in r[field]:
            r[field] = r[field].replace(old, new)
            done = True
    print(("OK  " if done else "MISS ") + region_sub + " :: " + field)

# Verification grades
A = {  # price + water/rate both checked against primary sources
    "Dominion Energy Virginia", "Georgia Power (Southern Co.)", "Memphis Light Gas & Water (MLGW) / TVA",
    "Alabama Power (Southern Co.)", "Entergy Arkansas", "Oncor Electric Delivery",
    "Xcel Energy / Southwestern Public Service (SPS)", "Portland General Electric (PGE)",
    "We Energies (WEC)", "Umatilla Electric Cooperative (+ Columbia Basin EC, Pacific Power)",
    "Northern Wasco County PUD (electric) / City of The Dalles (water)",
    "Grant County PUD", "Arizona Public Service (APS)", "Salt River Project (SRP)",
    "NV Energy (Nevada Power / Sierra Pacific)", "Rocky Mountain Power (PacifiCorp)",
    "Cheyenne Light, Fuel & Power (Black Hills Energy); water: Cheyenne BPU",
    "Idaho Power (IDACORP)", "Public Service Co. of New Mexico (PNM / TXNM Energy)",
    "Entergy Mississippi", "Public Service Co. of New Mexico (PNM)", "AEP Ohio (Ohio Power Co.)",
    "Duke Energy Carolinas (DEC)", "Duke Energy Progress (DEP)", "PPL Electric Utilities",
}
B = {  # price verified; water secondary/unverified
    "Alliant Energy (IPL)", "Omaha Public Power District (OPPD)", "Lincoln Electric System (LES)",
    "Evergy", "Xcel Energy (NSP-Minnesota)", "FirstEnergy Ohio (Ohio Edison/Toledo Edison)",
    "Indiana Michigan Power (I&M, AEP)", "Duke Energy Indiana", "Montana-Dakota Utilities (MDU) + area co-ops",
    "DTE Energy", "Commonwealth Edison (ComEd)", "Pacific Power (PacifiCorp)",
    "PECO Energy (Exelon)", "Mon Power / Potomac Edison (FirstEnergy)", "Vineland Municipal Electric Utility + Atlantic City Electric (Exelon)",
    "City of Lancaster municipal utilities", "CPS Energy", "Austin Energy",
    "El Paso Electric", "El Paso Electric (NM side)", "Mecklenburg Electric Cooperative / Southside Electric Cooperative (+ some Dominion)",
    "Oklahoma Gas & Electric (OG&E) + municipal water (OKC, Muskogee)",
    "San Marcos municipal utilities / area co-ops",
}
C = {  # water verified, price not independently checked
    "NYPA hydropower / National Grid / NYSEG", "NYSEG (Avangrid); water: Bolton Point (Southern Cayuga Lake Intermunicipal WC)",
}
for r in rows:
    u = r["utility"]
    if u in A:
        r["verification"] = "A - price (EIA) and water/rate claims checked against primary sources"
    elif u in B:
        r["verification"] = "B - price (EIA) verified; water figure secondary or not published"
    elif u in C:
        r["verification"] = "C - water/rate verified; price trend not independently checked"
    else:
        r["verification"] = "D - not independently re-verified"

cols = list(rows[0].keys())
with open(PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

from collections import Counter
print("\nGrades:", Counter(r["verification"][0] for r in rows))
print("Rows:", len(rows), "Cols:", len(cols))
