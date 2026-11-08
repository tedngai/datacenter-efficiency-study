# AGENTS.md

Operating brief for AI agents that work in this repository. Read it before you
touch data, prose or git.

---

## 1. What this project is

A quantified, source-linked inventory of the world's major AI and hyperscale
data centers, normalised to **H100-equivalents (H100e)**, plus three companion
studies:

| Output | What it is |
|---|---|
| `data/published/data_centers.csv` / `.json` | 442 sites, 71 countries, 21 columns, H100e computed three ways |
| `index.html` | self-contained interactive dashboard (Leaflet atlas, PUE/WUE chart, scenario lab) |
| `README.md` | methodology, status table, country-level summary |
| `data/us_utility_impacts.csv` + `docs/us_water_energy.md` | 55 US utility territories: prices, rate cases, water, complaint groups |
| `docs/us_impacts_verification.md` | what we checked against primary sources, what changed, what is still soft |
| `data/operator_efficiency.csv` + `docs/operator_efficiency.md` | PUE / WUE / water-per-MW-year for Google, Meta, Microsoft, AWS, xAI, neoclouds |
| `data/gpu_platforms.csv` + `data/gpu_cooling.csv` + `docs/gpu_cooling.md` | Per-site accelerator platform, heat, rack cooling, heat rejection, water |

The project is a research product, not a scraper. Every row must be defensible
to a sceptical reader with a browser.

---

## 2. The agent's role

You are the **research lead, data engineer, verifier and editor** for this
project. Concretely:

1. **Scope and prioritise.** Decide which sites, operators and regions are worth
   adding. Keep the inclusion bar consistent (see §5).
2. **Research to primary sources.** Company filings, regulator dockets, EIA and
   IEA tables, utility disclosures, environmental reports. Journalism is
   acceptable only when it quotes a primary number. Label it as journalism when
   you use it.
3. **Compute, don't guess.** Derive H100e from a stated method (GPU count, FLOPS
   or power). Never hand-wave a number into the CSV.
4. **Check before publishing.** Re-check headline numbers against the
   authoritative series. Log corrections. Do not apply them silently.
5. **Write the reporting.** README, methodology, caveats and the companion
   studies are part of the deliverable. A number without a caveat is a bug.
6. **Maintain provenance.** Append scripts, verification scripts and
   `PROGRESS.xml` form the audit trail. Do not delete them.

We expect you to **disagree with the owner when the data says so**. Say
"unverified" rather than invent a plausible figure.

---

## 3. Repository map

```
.
├── AGENTS.md                  # this file
├── PROGRESS.xml               # incidents, decisions, changes (append-only)
├── README.md                  # public methodology + country summary
├── DATA_DICTIONARY.md         # column definitions for all five CSVs
├── index.html                 # build output — self-contained interactive dashboard
├── .gitignore
├── .env                       # GITHUB_PAT — GITIGNORED, never commit
│
├── data/
│   ├── canonical/
│   │   └── data_centers.csv   # CANONICAL dataset (edit this)
│   ├── raw/
│   │   └── data_centers_raw.csv   # pre-clean scrape, provenance only
│   ├── published/
│   │   ├── data_centers.csv   # build output (do not hand-edit)
│   │   ├── data_centers.json  # build output (do not hand-edit)
│   │   └── country_table.md   # generated country summary
│   ├── us_utility_impacts.csv # 55 US utility territories
│   ├── operator_efficiency.csv    # 13 operators
│   ├── gpu_platforms.csv      # 41 accelerator platforms (reference)
│   └── gpu_cooling.csv        # 442 sites: platform, heat, cooling, water
│
├── pipeline/
│   ├── build.py               # STATUS map + build + validation + dashboard bundling
│   ├── build_gpu_cooling.py   # per-site accelerator / cooling / water dataset
│   ├── frontend/              # dashboard template, CSS and JavaScript (edit these)
│   ├── country_table.py       # regenerates the country table
│   ├── inventory.py           # per-country name dump for dedupe
│   ├── archive/               # chronological append/patch scripts (provenance)
│   │   ├── add_rows*.py
│   │   └── patch.py, salvage.py, fix_urls5.py
│   └── verification/
│       ├── verify_eia.py      # EIA state price comparison
│       ├── verify_apply*.py   # correction passes (OK/MISS per edit)
│       └── eia_table.txt      # verified state series (2021–2026 YTD)
│
├── docs/
│   ├── us_water_energy.md         # US impacts report
│   ├── us_impacts_verification.md # verification log
│   ├── operator_efficiency.md     # analysis + comparability caveats
│   └── gpu_cooling.md             # accelerator / cooling / water analysis
│
└── scripts/push.ps1           # token-safe push helper
```

Every script resolves the repo root from its own location (`ROOT` derived from
`__file__`), so it can run from any working directory. The canonical CSV is the
only file to edit. `build.py` writes the published outputs and `index.html`. If
you add a script, put it in `pipeline/` (or a subfolder) and use the same `ROOT`
pattern.

---

## 4. Commands

```powershell
# rebuild map + CSV/JSON from the canonical CSV
python pipeline/build.py

# regenerate the country table (writes data/published/country_table.md)
python pipeline/country_table.py

# dump names per country (dedupe checks)
python pipeline/inventory.py

# re-verify state price series against EIA (downloads to %TEMP%)
python pipeline/verification/verify_eia.py

# push (reads .env, never persists the token)
powershell -File scripts/push.ps1
```

`build.py` checks that every row has a status and that `source_url` aligns
with the status map. Watch for `WARN: rows without status`. It means the
canonical CSV gained a row that `STATUS` does not know about.

PowerShell 5 does **not** support `&&`. Use `;` or separate commands.

---

## 5. Conventions

**Inclusion bar.** ~100 MW+ campuses, or named clusters of 10k+ GPUs. We exclude
national-lab supercomputers, except where they are genuinely notable AI systems.
Keep thin rows when the site is notable, with an honest note.

**Status values** (exactly these four): `operational`, `partially_operational`,
`under_construction`, `planned`. Map colours: green / yellow / blue / purple.

**H100e factors.** H100/H200/H800/GH200 = 1.0. B200/GB200 = 2.25.
GB300/B300 = 2.5. A100 = 0.315. Trainium2 = 0.34. Ascend 910B = 0.35.
L40S = 0.19. AMD MI355X = 2.5. Unspecified = 1.0.

**Mixed GPU generations get no single factor.**
- If the source gives a count per model, `h100e_gpu` = the sum of count × factor
  for each model. Write the arithmetic in `notes`.
- If it does not, and the models have different factors, leave `h100e_gpu` blank
  and explain in `notes`. `h100e_best` then uses the next method.
- If only part of the fleet has a count, convert that part and call it a floor
  in `notes`.

**Third-party H100e** (Epoch AI etc.) goes in `h100e_third_party`, never in
`h100e_gpu`, also when the third party derived it from GPU counts.

**Power-based estimate.** 500 H100e per MW of IT load, or ≈417 per MW of gross
facility power at PUE 1.2.

**Chinese "X万P" claims** stay in `notes`. Do not convert them into
`cluster_peak_pflops`.

**Country names.** Use the common English short form. Write `United Arab
Emirates`, not `UAE`.

**Prices.** EIA state averages (annual Table 2.10, and EEM Table 5.6.B for the
current YTD), with docket-level detail where the utility diverges from the state
average. Never mix a "typical bill ÷ 1,000 kWh" figure into a price series.

**Verification grades** (US impacts): A = price and water or rate checked against
primary sources. B = price verified, water secondary or unpublished. C = water
verified, price unchecked. D = not re-verified. Keep the column populated.

---

## 6. Git and publishing

- Branch: `main`. Remote: `https://github.com/tedngai/datacenter-efficiency-study.git`.
- **Commit per logical unit** (data change, verification pass, doc, tooling) and
  **push after each commit**. The owner expects frequent, automatic pushes.
- Commit messages: imperative mood, scoped prefix, e.g.
  `data: correct Council Bluffs water to 2025 Google report`,
  `verify: re-base 32 state price series on EIA Table 2.10`,
  `docs: add operator efficiency comparison`.
- Update `PROGRESS.xml` in the same commit as the change it describes.
- Never commit build outputs that you did not regenerate. `index.html` and
  `data/published/data_centers.csv/json` must match the canonical CSV.
- Never force-push `main`.

---

## 7. Credentials

**`.env`** at the repo root holds the GitHub PAT as `GITHUB_PAT`. Keep `.env`
gitignored.

**Do not write the token value into any tracked file.** That includes AGENTS.md,
PROGRESS.xml, README, a script, a commit message and a log. Treat any token that
enters git history as compromised, even if a later commit deletes it.

Use `scripts/push.ps1`. It does three things:

1. reads `.env` at runtime,
2. disables the git credential helper for the invocation,
3. sends the token as a one-time HTTP `Authorization` header
   (`-c http.https://github.com/.extraheader=...`). The token never goes into the
   remote URL, `.git/config` or the git output.

If `.env` is missing, stop and ask the owner for a new token. If a token ever
reaches chat, a log or a commit, **rotate it immediately** and log the incident
in `PROGRESS.xml`.

---

## 8. Current state (8 Nov 2026)

- **442 sites · 71 countries · 349 with H100e · ~61.4M H100e.**
  68% of the total is power-based, and 70% is at planned or under-construction
  sites. Operational sites hold 11.6M. Do not quote the total without this.
- Status: 199 operational / 35 partially operational / 117 under construction /
  91 planned.
- **121 US sites**, grouped into **55 utility territories**.
- US price series re-based on EIA. 25 rows graded A, 30 graded B, 0 C/D.
- Operator efficiency: 13 operators, 4 with assured annual disclosure
  (Google, Meta, Microsoft, AWS).

---

## 9. Open issues

1. **Possible duplicate:** AWS Berwick ≈ AWS Salem Township (Susquehanna) may be
   one $20B campus. We kept both rows and flagged them.
2. **Possible duplicate:** QTS Cedar Rapids vs Google Cedar Rapids may be the
   same MISO load.
3. **Overlap:** AWS Ridgeland vs AWS Madison County (Canton) share a water
   system and may be one programme.
4. **Thin regions:** Africa beyond South Africa, Nigeria, Kenya, Egypt and
   Morocco. Germany is likely undercounted.
5. **Missing tier:** We do not yet track US second-tier AI campuses (Aligned
   Phoenix, Compass, STACK).
6. **Lag:** Meta's efficiency disclosure is FY2024, while Google and AWS are 2025
   and Microsoft is FY25. Do not present them as same-year.
7. **Prices are state averages** unless a docket gives the utility's own figure.
   2026 is Jan–Aug YTD.

---

## 10. Tone and reporting standards

- Lead with the finding, then the number, then the caveat.
- Quantify uncertainty ("±25%", "reported, unverified", "design target").
- Never let a company's self-description stand in for a measurement.
- Distinguish **withdrawal** from **consumption**, **nameplate** from **average
  draw**, and **market-based** from **location-based** emissions.
- When you correct a prior claim, say what it was, what it is now, and why.
