# Verification ledger — full corpus check, November 2026

## Scope and method

This log records a full check of the three published data files:

- `data/published/data_centers.csv` — 442 site rows
- `data/us_utility_impacts.csv` — 55 utility rows
- `data/operator_efficiency.csv` — 13 operator rows

15 parallel research agents checked the rows. Each agent read the cited source
URL for its rows. If the fetch failed, the agent did one separate web search.
Each agent graded the main fields of each row: operator, location, the
headline number (power or GPU count), and status.

Machine scripts checked the derived numbers first. The scripts re-computed the
status totals, the H100e sums, the GPU conversion factors, and the method
priority. The scripts also tested whether all 623 cited URLs respond.

The full per-row record is in `data/verification/verdicts.csv`. Each row of that
file has a claim ID, a verdict, a rationale that names the evidence, and the
source URLs that the agent read.

## Verdict vocabulary

- SUPPORTED — the cited source or a separate primary source confirms the row.
- PARTLY_SUPPORTED — the row is real, but one main field lacks support. The rationale names that field.
- CONTRADICTED — separate evidence shows a main number wrong. The rationale states both numbers.
- UNVERIFIABLE — no accessible evidence. No row got this grade.

## Results

| File | Rows | SUPPORTED | PARTLY_SUPPORTED | CONTRADICTED |
|---|---:|---:|---:|---:|
| `data_centers.csv` | 442 | 350 | 84 | 8 |
| `us_utility_impacts.csv` | 55 | 43 | 11 | 1 |
| `operator_efficiency.csv` | 13 | 9 | 4 | 0 |
| All files | 510 | 402 (79%) | 99 (19%) | 9 (2%) |

The energy price endpoints in all 55 utility rows match the EIA tables. Three
agents pulled the EIA Table 2.10 and Table 5.6.B data files. They compared the
2021, 2025, and 2026 year-to-date state prices digit for digit.

## Corrections applied

The check found 9 contradicted rows, 2 mis-cited sources, and 8 dead links. All
of them got corrections in the canonical data. The published files were rebuilt.

| # | Row | Correction | Evidence |
|---|---|---|---|
| 1 | AWS Madison County | 2,200 MW → 1,000 MW | The cited project page states 1.0 GW. Epoch AI lists 284 MW IT for the Madison Mega Site today. |
| 2 | Google Midlothian | Third-party estimate 331,986 → 143,581 H100e | The Epoch AI data file gives this value. |
| 3 | TeraWulf Cayuga (Justified Data Campus) | Renamed to TeraWulf Lake Hawkeye (Cayuga site) | The Anthropic 401 MW lease is at the sister site Justified Data in Hawesville, Kentucky. This row now describes the Cayuga site in Lansing, New York. |
| 4 | Fairwater Atlanta | Union City, 324 MW → Fayetteville, 640 MW IT, >150,000 GB200 | The old figures belong to the separate EdgeConneX ATL11 project. Microsoft opened Fairwater Atlanta in October 2025. |
| 5 | China Telecom Qingyang | 250 MW → 135 MW | The Qingyang municipal government states 22,500 racks and 135 MW at full build-out. |
| 6 | Bridge Data Centres Cyberjaya | 98 MW → 20 MW | DCD states ~20 MW for the two original sites. The 87 MW third campus is a separate project. |
| 7 | Nebius Beit Shemesh | 80 MW → 58 MW | The 80 MW lease combines the 22 MW Masmiyya site with this 58 MW site. |
| 8 | China Mobile Hohhot | 10,000 → 20,000 accelerator cards | Yicai and China Daily report ~20,000 cards at ~6.7 EFLOPS. |
| 9 | Data Vault Pakistan | 3,000 GPUs → 100 GPUs | The operator site states 100 GPUs installed and 1 MW critical IT (October 2026). The 3,000 figure is a CEO procurement claim. |
| 10 | FirstEnergy Ohio (utility row) | 2025 bill increase: ~7.1% → 11.8% / 13.3% | The FirstEnergy customer notice states 11.8% (Ohio Edison) and 13.3% (Toledo Edison). |
| 11 | Google West Memphis | New source URL. Status planned → under_construction | The old URL pointed to The Dalles, Oregon. Construction began in October 2025 per the Arkansas EDC and the Arkansas Democrat-Gazette. |
| 12 | Bitdeer Milam County | New source URL | The old URL described the Ohio campus. The new URL is the DCD article on the Milam County land purchase. |

The corrections changed the headline totals. The dataset now tracks ~64.0M H100e
(before: ~64.7M). A later pass (`verify_apply5.py`, Nov 2026) applied the
mixed-generation rule and brought the total to ~61.4M. See `PROGRESS.xml` C-014. The status split is 199 operational, 35 partially operational,
117 under construction, 91 planned.

## Dead links

The URL check found 8 dead links in 7 rows. All got replacements, and each
replacement responds with HTTP 200:

- `local.cctv.com` (China Telecom Qingyang) → the China Telecom news page on the Qingyang cluster
- `larsentoubro.com/...indias-largest...` → the same press release at the correct URL
- `news.cn/...Zhongwei...` → the same Xinhua article at the correct URL
- `fpt.com` Vietnamese URL → the FPT page on the first AI Factory in Vietnam
- `cloudburstdc.com/data-centers/` (2 rows) → the DCD article on the CloudBurst Texas construction start
- `africacomputetracker.org/facilities/` (Wingu Addis Ababa) → the Wingu EAII partnership announcement

## Patterns in the partly supported rows

99 rows (19%) are PARTLY_SUPPORTED. The rationale names the unconfirmed field in
each row. Four patterns cover most of them:

- Third-party estimates. The row quotes an Epoch AI or analyst estimate. The cited source does not carry that number.
- Status drift. The row says planned. Newer sources show construction. The reverse also occurs.
- Tracker power figures. A tracker (DC Atlas, usdatamap, Baxtel) is the only source for the MW figure.
- GPU count mix-ups. Some rows mix H100-equivalents with announced GPU counts.

## Residual caveats

- 52 cited URLs return 403 to scripts (bot blocks). We did not open them in a browser. Reuters and Bloomberg links are in this group.
- The PARTLY_SUPPORTED rows stay in the dataset. Read the rationale in `verdicts.csv` before you quote a number from one of them.
- The check confirms the rows as of November 2026. The field moves fast. Re-check the under_construction rows before you quote their capacity.
