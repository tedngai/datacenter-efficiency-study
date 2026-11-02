"""Fourth pass: fix Dominion order date/terms wording."""
import csv, sys, os
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "data", "us_utility_impacts.csv")
rows = list(csv.DictReader(open(PATH, encoding='utf-8')))

FIX = [
    ('Jan 2026 order: +$11.24/mo + $2.36/mo 2027 (1,000 kWh).',
     'Nov 2025 SCC order: +$11.24/mo (2026) + $2.36/mo (2027) for 1,000 kWh.'),
    ('(Jan 2027, 14-yr contracts, 85%/60% minimum demand)',
     '(from Jan 2027; 85% distribution/transmission and 60% generation minimum take)'),
]
for r in rows:
    for old, new in FIX:
        for k, v in r.items():
            if old in v:
                r[k] = v.replace(old, new)
                print('OK  ', r['region'], '::', k)

cols = list(rows[0].keys())
with open(PATH, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(rows)
print('rows', len(rows))
