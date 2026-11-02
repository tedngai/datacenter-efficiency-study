"""Second correction pass: exact-substring fixes missed by verify_apply.py.

Prices anchored to EIA Electric Power Annual Table 2.10 (2021, 2024, 2025)
and EEM Table 5.6.B (Jan-Aug 2026 YTD).
"""
import csv, sys, os
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "us_utility_impacts.csv")
rows = list(csv.DictReader(open(PATH, encoding='utf-8')))

FIXES = [
    # ---- price anchors ----
    ('Virginia — Southside', 'energy_price_trend_2021_2026',
     'APCo (adjacent) 12.29¢ (Nov 2021) → ~16.4-17.2¢ (2025).',
     'VA statewide 11.96¢ (2021) → 15.28¢ (2025) → 16.95¢ (2026 YTD) per EIA; '
     'APCo (adjacent territory) 12.29¢ (Nov 2021) → ~16.4-17.2¢ (2025).'),
    ('Virginia — Richmond metro', 'energy_price_trend_2021_2026',
     'Same Dominion trend: ~11¢ (2021) → ~17.6¢ (2026); +$11.24/mo Jan 2026.',
     'Same Dominion trend: 11.96¢ (2021) → 15.28¢ (2025) → 16.95¢ (2026 YTD) per EIA; '
     '+$11.24/mo Jan 2026.'),
    ('Virginia — Chesterfield', 'energy_price_trend_2021_2026',
     'Same Dominion trend (+$11.24/mo Jan 2026).',
     'Same Dominion trend: 11.96¢ (2021) → 15.28¢ (2025) → 16.95¢ (2026 YTD) per EIA '
     '(+$11.24/mo Jan 2026).'),
    ('Alabama — Huntsville', 'energy_price_trend_2021_2026',
     'TN ~11.1¢ (2021) → ~12-13¢ (2026).',
     'AL statewide 12.96¢ (2021) → 16.09¢ (2025) → 16.51¢ (2026 YTD) per EIA; '
     'Huntsville Utilities is a TVA distributor (TVA territory rates run below the AL statewide average).'),
    ('Texas — AEP Texas', 'energy_price_trend_2021_2026',
     'vs TX avg 16.39¢',
     'vs TX statewide 16.03¢ (EIA 2026 YTD)'),
    ('Texas — Panhandle', 'energy_price_trend_2021_2026',
     'below TX deregulated avg 16.99¢',
     'below the TX statewide average (16.03¢, EIA 2026 YTD)'),
    ('Iowa — Des Moines', 'energy_price_trend_2021_2026',
     'residential 11.2¢ (2025) vs IA avg 13.6¢.',
     'residential 11.2¢ (2025) vs IA state average 13.62¢ (EIA 2025; IA 12.73¢ in 2021 → 14.55¢ 2026 YTD).'),
    ('Iowa — Cedar Rapids', 'energy_price_trend_2021_2026',
     'IA residential avg 13.6¢ (2025)',
     'IA residential avg 13.62¢ (EIA 2025)'),
    ('Oklahoma — OKC', 'energy_price_trend_2021_2026',
     '~13.19¢ effective, 28% below US avg',
     '~13.19¢ effective (EIA OK 2025: 13.21¢; US 17.23¢ — ~23% below)'),
    ('Washington — Quincy', 'energy_price_trend_2021_2026',
     '(vs WA avg $0.133, US $0.156)',
     '(vs WA 13.17¢ and US 17.23¢, EIA 2025)'),
    ('Illinois — Chicago', 'energy_price_trend_2021_2026',
     'Statewide residential +7.1% in 2025.',
     'Statewide residential rose 15.87¢ (2024) → 17.67¢ (2025) per EIA (+11.3%).'),
    ('Texas — Oncor', 'energy_price_trend_2021_2026',
     'TX residential 12.11¢ (2021) → 15.47¢ (2025) → ~16.99¢ (Apr 2026).',
     'TX residential 12.11¢ (2021) → 15.40¢ (2025) → 16.03¢ (2026 YTD) per EIA '
     '(16.99¢ was an April 2026 monthly peak).'),
    ('Wisconsin — Mount Pleasant', 'energy_price_trend_2021_2026',
     'Apr 2026 request for 2027-28: +$347.1M (+9.3%; residential +16.3%; typical bill $144→~$166 by 2028).',
     'Apr 2026 request for 2027-28: +$347.1M; residential +10.28% in 2027 and +5.52% in 2028 '
     '(~+16.4% cumulative; typical bill ~$144→$166).'),
    ('Utah — Eagle Mountain', 'energy_price_trend_2021_2026',
     '2024 request of 30% (cut to 18%)',
     'UT 10.43¢ (2021) → 13.02¢ (2025) → 13.19¢ (2026 YTD) per EIA. '
     '2024 request of 30% (cut to 18%)'),
    ('Idaho — Kuna', 'energy_price_trend_2021_2026',
     'ID ~9-10¢ (2021) → ~11-12¢ (2026).',
     'ID 10.16¢ (2021) → 11.83¢ (2025) → 13.02¢ (2026 YTD) per EIA.'),
    ('New Mexico — Los Lunas', 'energy_price_trend_2021_2026',
     'PNM residential +$6.23/mo per phase',
     'NM 13.52¢ (2021) → 14.85¢ (2025) → 15.34¢ (2026 YTD) per EIA. '
     'PNM residential +$6.23/mo per phase'),
    ('Oregon — The Dalles', 'energy_price_trend_2021_2026',
     'No major DC-attributed retail rate case found 2021-26; PNW residential ~11¢ (2021) → ~14-15¢ (2025) regional.',
     'No major DC-attributed retail rate case found 2021-26; OR residential 11.37¢ (2021) → '
     '15.46¢ (2025) → 15.46¢ (2026 YTD) per EIA.'),
    # ---- water corrections ----
    ('Texas — Panhandle', 'water_consumption',
     'at ~$8.72/1,000 gal — DOUBLE the standard rate',
     'at $8.72/1,000 gal — the highest industrial water rate Amarillo has ever charged'),
    ('Arizona — West Valley', 'water_consumption',
     'Microsoft Goodyear: 2023 amendment allows 1.2M gpd at full build-out (wording up to 3M gpd); '
     '~56M gal/yr potable estimate (Atlantic 2024); BI (2025): city docs planned 1M gpd x 5 buildings = 1.83B gal/yr; '
     "actual use withheld as 'proprietary'. Microsoft pays $36M toward wastewater expansion;",
     'Microsoft Goodyear: 2023 council amendment gives 1.2M gpd of wastewater capacity at full build-out '
     '(Microsoft paid $36M toward the $90M 157th Ave plant); the original water-cooling plan was up to 5M gpd '
     '(~1M gpd per building × 5 ≈ 1.83B gal/yr, per BI 2025), and buildings 4-5 were switched to air cooling; '
     "actual use withheld as 'proprietary';"),
    ('Iowa — Des Moines', 'water_consumption',
     'Google Council Bluffs: ~1.4 BILLION gallons 2024 — one of the largest single DC water users in the US.',
     'Google Council Bluffs: 1,746.4M gal withdrawn / 1,346.0M consumed in 2025 '
     '(Google 2026 Environmental Report p.97) — more than any other Google data center worldwide.'),
    ('Nebraska — Omaha', 'water_consumption',
     'up from ~135M in 2024',
     'up from 134.7M in 2023 (46.6M in 2022)'),
    ('Mississippi — Jackson', 'water_consumption',
     'AWS Ridgeland: avg ~93M gal/yr but contracted hottest-day peak of 3.67 MGD — '
     '~82% of the 4.5 MGD peak capacity of the city system;',
     'AWS Ridgeland: avg ~93M gal/yr; a peak-day demand of ~3.7 MGD (~82% of the 4.5 MGD city-system peak) '
     'has been reported but does NOT appear in the water-service agreement text (unverified);'),
    ('Tennessee — Memphis', 'water_consumption',
     'recorded ~812,502 gal/day; contract 1.3 MGD;',
     'recorded ~812,502 gal/day; contract demand reported at 1.3 MGD '
     '(paywalled Commercial Appeal; unverified);'),
    ('Ohio — Lancaster', 'water_consumption',
     'No published figure for Lancaster (neighboring Google New Albany ~127M gal/yr).',
     'No published figure for Lancaster (neighboring Google New Albany withdrew 1,008.1M gal / '
     'consumed 835.7M gal in 2025).'),
]

misses = 0
for region_sub, field, old, new in FIXES:
    hits = [r for r in rows if region_sub in r['region']]
    if not hits:
        print('MISS REGION:', region_sub); misses += 1; continue
    done = False
    for r in hits:
        if old in r[field]:
            r[field] = r[field].replace(old, new)
            done = True
    print(('OK   ' if done else 'MISS ') + region_sub + ' :: ' + field)
    if not done:
        misses += 1

# Grade overrides for rows whose utility string bypassed the first mapping.
GRADE = {
    'Virginia — Richmond metro': 'B - price (EIA) verified; water figure secondary or not published',
    'Virginia — Chesterfield': 'B - price (EIA) verified; water figure secondary or not published',
    'Alabama — Huntsville': 'B - price (EIA) verified; water figure secondary or not published',
    'Texas — AEP Texas': 'B - price (EIA) verified; water figure secondary or not published',
    'Texas — West (Permian': 'B - price (EIA) verified; water figure secondary or not published',
    'Iowa — Des Moines': 'A - price (EIA) and water/rate claims checked against primary sources',
}
for r in rows:
    for k, v in GRADE.items():
        if k in r['region']:
            r['verification'] = v

# Drop the empty New Mexico cross-reference stub (content lives in the Los Lunas row).
before = len(rows)
rows = [r for r in rows if 'statewide context' not in r['region']]
print('Dropped stub rows:', before - len(rows))

cols = list(rows[0].keys())
with open(PATH, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

print('\nMISSES:', misses)
print('Grades:', Counter(r['verification'][0] for r in rows))
print('Rows:', len(rows), 'Cols:', len(cols))
