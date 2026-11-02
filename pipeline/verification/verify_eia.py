"""Compare our claimed state price trends against authoritative EIA annual data."""
import openpyxl, os

T = os.path.expandvars(r'%TEMP%')

def load(path, col_val):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    d = {}
    for r in range(5, ws.max_row + 1):
        st = ws.cell(r, 1).value
        v = ws.cell(r, col_val).value
        if st and isinstance(st, str) and isinstance(v, (int, float)):
            d[st.strip()] = v
    return d

p21 = load(T + r'\epa_2021.xlsx', 2)      # Year 2021
p24 = load(T + r'\epa_2025.xlsx', 3)      # Year 2024
p25 = load(T + r'\epa_2025.xlsx', 2)      # Year 2025
y26 = load(T + r'\table_5_06_b.xlsx', 2)  # Aug 2026 YTD

ABBR = {
 'AL':'Alabama','AR':'Arkansas','AZ':'Arizona','GA':'Georgia','IA':'Iowa','ID':'Idaho',
 'IL':'Illinois','IN':'Indiana','KS':'Kansas','MI':'Michigan','MN':'Minnesota',
 'MO':'Missouri','MS':'Mississippi','NC':'North Carolina','ND':'North Dakota',
 'NE':'Nebraska','NJ':'New Jersey','NM':'New Mexico','NV':'Nevada','NY':'New York',
 'OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','TN':'Tennessee',
 'TX':'Texas','UT':'Utah','VA':'Virginia','WA':'Washington','WI':'Wisconsin',
 'WV':'West Virginia','WY':'Wyoming',
}

print(f"{'ST':3}{'2021':>7}{'2024':>7}{'2025':>7}{'26YTD':>7}{'21-25%':>8}{'21-26%':>8}")
for s, full in ABBR.items():
    a, b, c, d = p21.get(full), p24.get(full), p25.get(full), y26.get(full)
    ch25 = (c / a - 1) * 100 if a and c else float('nan')
    ch26 = (d / a - 1) * 100 if a and d else float('nan')
    fmt = lambda x: f"{x:7.2f}" if x else "      -"
    print(f"{s:3}{fmt(a)}{fmt(b)}{fmt(c)}{fmt(d)}{ch25:8.1f}{ch26:8.1f}")

print("\nUS total:")
for name, d in [('2021', p21), ('2024', p24), ('2025', p25), ('2026YTD', y26)]:
    print(' ', name, d.get('U.S. Total'), d.get('US Total'), d.get('United States'))
