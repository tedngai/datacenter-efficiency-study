"""Third pass: add EIA price anchors to the two New York rows and re-grade them."""
import csv, sys, os
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "us_utility_impacts.csv")
rows = list(csv.DictReader(open(PATH, encoding='utf-8')))

NY = ('NY 19.48¢ (2021) → 26.39¢ (2025) → 29.26¢ (2026 YTD) per EIA statewide '
      '(upstate industrial zones run well below the state average, which is pulled up by NYC). ')

fixes = 0
for r in rows:
    if r['region'].startswith('New York'):
        if not r['energy_price_trend_2021_2026'].startswith('NY '):
            r['energy_price_trend_2021_2026'] = NY + r['energy_price_trend_2021_2026']
            fixes += 1
        r['verification'] = 'B - price (EIA) verified; water figure secondary or not published'

print('NY rows patched:', fixes)

cols = list(rows[0].keys())
with open(PATH, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)

print('Grades:', Counter(r['verification'][0] for r in rows))
print('Rows:', len(rows))
