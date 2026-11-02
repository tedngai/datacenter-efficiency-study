# Verification log — US water & energy impacts

Companion to `data/us_utility_impacts.csv` (55 utility-territory rows covering all 121
tracked US sites) and `us_water_energy.md`. This file records what was
independently checked, what was wrong, and what is still soft.

Date of check: November 2026.

---

## 1. Method

Three kinds of claim were checked, each against a different class of source.

**Energy prices → EIA, one source for all rows.**
- 2021: EIA *Electric Power Annual 2021*, Table 2.10 (`/electricity/annual/archive/2021/xls/epa_02_10.xlsx`)
- 2024 and 2025: EIA *Electric Power Annual 2025*, Table 2.10 (`/electricity/annual/xls/epa_02_10.xlsx`)
- 2026: EIA *Electric Power Monthly*, Table 5.6.B, **January–August 2026 YTD**
  (`/electricity/monthly/xls/table_5_06_b.xlsx`)
- National average for context: 13.66¢ (2021) → 16.48¢ (2024) → 17.23¢ (2025)
  → 18.19¢ (2026 YTD), residential, all sectors.

Scripts: `verify_eia.py` (builds the state table), `verify_apply.py`,
`verify_apply2.py`, `verify_apply3.py` (apply corrections; each prints
`OK`/`MISS` per edit so nothing is silently skipped).

**Water volumes → primary disclosures and filings.**
- Google 2026 Environmental Report, p.97 ("Water use by data center location",
  calendar 2025) — the only hyperscaler publishing site-level withdrawal *and*
  consumption.
- Utility/city disclosures (Loudoun Water, Columbus DPU, Hillsboro, Cheyenne BPU,
  Kuna, Las Vegas/SNWA, Albuquerque/Bernalillo, Amarillo), rate-case and service
  agreements (Ridgeland MS water-service agreement; SRBC docket 20260301;
  Cheyenne–Meta agreement), state-engineer filings (New Mexico), and Meta's and
  Microsoft's sustainability reporting.
- Press used only where it quotes a primary number (Nebraska Examiner/Flatwater
  for the 732M-gal figure; Amarillo Globe-News for the water contract).

**Rate events → orders and dockets.**
- Virginia SCC final order in the Dominion biennial review (25 Nov 2025): GS-5
  class for ≥25 MW, effective 1 Jan 2027, 85% distribution / 60% generation
  minimum take.
- PJM 2025/26 Base Residual Auction results (total cost to load $14.7B; the
  $269.92/MW-day clearing price is the widely reported figure, not stated in the
  report text itself).
- Georgia PSC Residential Rate Survey (Georgia Power 500 kWh = $87.75 / 17.55¢).
- Wisconsin PSC docket 5-UR-111 (approved 12.38% residential) and 5-UR-112
  (pending, +10.28% / +5.52%).
- Umatilla Electric Cooperative rate notices (~+$12/mo, Oct 2025).

---

## 2. The systematic error that mattered

The 2021 baselines originally supplied were **~1¢/kWh too low in most states**,
and several 2025 figures were mid-year quotes, forecast "typical bill ÷ 1,000 kWh"
arithmetic, or a monthly peak presented as an annual average.

Examples of the original vs EIA:

| State | Original 2021 claim | EIA 2021 | Original 2025 claim | EIA 2025 |
|---|---|---|---|---|
| Virginia | ~11.0¢ | **11.96¢** | 15.2¢ | **15.28¢** |
| Georgia | ~11.7¢ | **12.51¢** | 17.55¢ (PSC survey) | **14.74¢** |
| Arkansas | ~9.9¢ | **11.27¢** | 14.37¢ (Aug 2026) | **12.87¢** |
| Arizona | ~11.7¢ | **12.54¢** | ~13.5–14¢ | **15.26¢** |
| Pennsylvania | ~13¢ | **13.76¢** | ~17–18¢ | **19.29¢** |
| Wyoming | "9.14¢ (2024)" | **12.47¢** | — | **13.37¢** |
| Texas | 12.11¢ | 12.11¢ ✓ | 15.47¢ | **15.40¢** |

Two consequences:

1. **Direction was usually right, magnitude was not.** Understating the 2021 base
   understates the increase; e.g. Virginia's rise is **+41.7%** to 2026 YTD, not
   the "+30–60%" band originally written.
2. **One row had the sign wrong.** Alabama Montgomery was described as *above* the
   national average (13.09¢ vs 16.48¢). It is **below** it (12.96¢ vs 17.23¢ in
   2025); Alabama's high bills come from consumption per household, not price per
   kWh. Corrected, with the distinction spelled out.

The Wyoming "9.14¢ in 2024" figure could not be reconciled with any EIA series
and was **removed** rather than patched.

### Verified state series now in the CSV (residential, ¢/kWh)

| State | 2021 | 2024 | 2025 | 2026 YTD | 2021→2026 |
|---|---|---|---|---|---|
| AL | 12.96 | 15.18 | 16.09 | 16.51 | +27.4% |
| AR | 11.27 | 12.32 | 12.87 | 13.74 | +21.9% |
| AZ | 12.54 | 14.91 | 15.26 | 15.36 | +22.5% |
| GA | 12.51 | 14.08 | 14.74 | 15.48 | +23.7% |
| IA | 12.73 | 13.40 | 13.62 | 14.55 | +14.3% |
| ID | 10.16 | 11.52 | 11.83 | 13.02 | +28.1% |
| IL | 13.18 | 15.87 | 17.67 | 19.23 | +45.9% |
| IN | 13.37 | 14.77 | 15.96 | 17.04 | +27.4% |
| KS | 12.98 | 14.15 | 14.44 | 15.26 | +17.6% |
| MI | 17.54 | 19.30 | 20.03 | 21.73 | +23.9% |
| MN | 13.50 | 15.45 | 15.83 | 16.44 | +21.8% |
| MO | 11.41 | 12.91 | 13.30 | 14.28 | +25.2% |
| MS | 11.56 | 13.39 | 14.03 | 15.06 | +30.3% |
| NC | 11.32 | 14.13 | 14.00 | 14.94 | +32.0% |
| ND | 10.85 | 11.51 | 11.82 | 12.46 | +14.8% |
| NE | 10.75 | 11.53 | 12.05 | 12.92 | +20.2% |
| NJ | 16.35 | 19.34 | 22.48 | 24.09 | +47.3% |
| NM | 13.52 | 14.20 | 14.85 | 15.34 | +13.5% |
| NV | 11.49 | 15.00 | 13.26 | 13.36 | +16.3% |
| NY | 19.48 | 24.43 | 26.39 | 29.26 | +50.2% |
| OH | 12.77 | 15.99 | 16.90 | 18.81 | +47.3% |
| OK | 11.00 | 12.24 | 13.21 | 13.81 | +25.5% |
| OR | 11.37 | 14.70 | 15.46 | 15.46 | +36.0% |
| PA | 13.76 | 17.77 | 19.29 | 21.13 | +53.6% |
| TN | 11.07 | 12.42 | 13.22 | 13.80 | +24.7% |
| TX | 12.11 | 14.94 | 15.40 | 16.03 | +32.4% |
| UT | 10.43 | 12.22 | 13.02 | 13.19 | +26.5% |
| VA | 11.96 | 14.41 | 15.28 | 16.95 | +41.7% |
| WA | 10.11 | 11.90 | 13.17 | 14.42 | +42.6% |
| WI | 14.52 | 17.18 | 18.08 | 19.05 | +31.2% |
| WV | 12.15 | 15.07 | 15.39 | 15.58 | +28.2% |
| WY | 11.17 | 12.47 | 13.37 | 14.01 | +25.4% |
| **US** | **13.66** | **16.48** | **17.23** | **18.19** | **+33.2%** |

These are **state averages**, not utility-specific rates. Where the utility is
known to sit off the state average, the row says so (Dominion above the Virginia
average; TVA distributors below the Alabama average; MidAmerican below the Iowa
average; Grant County PUD far below the Washington average).

---

## 3. Water corrections

| Claim | Was | Now | Source |
|---|---|---|---|
| Google Council Bluffs | "~1.4B gal (2024)" | **1,746.4M gal withdrawn / 1,346.0M consumed (2025)** | Google 2026 Env. Report p.97 |
| Google New Albany OH | "~127M gal/yr" | **1,008.1M withdrawn / 835.7M consumed (2025)**; Lancaster 307.1/135.8, Lockbourne 460.8/359.5 | same |
| Google Nebraska | "732M gal 2025, up from ~135M in **2024**" | 732.1M in 2025, up from **134.7M in 2023** (46.6M in 2022) | Google reporting via Nebraska Examiner, Jul 2026 |
| Google Lenoir NC | "344M gal consumed, #8 site" | 378.3M withdrawn / 344.3M consumed — still #8 by withdrawal among Google US sites | Google 2026 Env. Report p.97 |
| Loudoun County VA | "899M gal (2023)" | 899M gal **potable** *plus* 815M gal reclaimed (>1B total); 750M+ reclaimed delivered to ~40 customers in 2025 | Loudoun Water / Hanover analysis |
| Microsoft Goodyear AZ | "1.2M gpd allowed (wording up to 3M)" | **1.2M gpd of wastewater capacity** at full build-out ($36M toward the $90M 157th Ave plant); original plan up to 5M gpd (~1.83B gal/yr), buildings 4–5 now air-cooled | AZ Tech Council / council amendment |
| Fermi America Amarillo | "$8.72/1,000 gal — double the standard rate" | $8.72/1,000 gal — **the highest industrial water rate the city has ever charged** ("double" was not supported) | Amarillo Globe-News, 29 Oct 2025 |

### Downgraded to "reported, unverified"

- **AWS Ridgeland MS, 3.67 MGD peak-day** — the figure is *not* in the water-service
  agreement text (checked in full). The agreement does support the ~93M gal/yr
  average and the $53.7M water/sewer split. Row now says so explicitly.
- **xAI Memphis, 1.3 MGD contract demand** — source is a paywalled Commercial
  Appeal piece; the 812,502 gpd actual draw and the 19¢ vs 32¢ per-100-gallon
  disparity are documented elsewhere and stand.

### Re-verified as-is (no change)

- **Loudoun Water:** data centers ≈9% of average-day potable use.
- **xAI Memphis:** 812,502 gpd from the Memphis Sand Aquifer; ~25M gal bought in
  March; 19¢/100 gal vs 32¢ for residents.
- **Meta Eagle Mountain:** >35M gal in 2024; the 2018 agreement keeps monthly use
  confidential and requires the city to alert Meta when records are requested
  (confirmed to the Salt Lake Tribune, Jan 2026).
- **Meta Prineville:** 117.5M gal (445,000 m³) of city water in 2020.
- **Fermi Amarillo:** 2.5 MGD authorization; up to 18.5 MGD claimed by the company.
- **Microsoft Goodyear:** $36M contribution to the wastewater plant.
- **Umatilla Electric:** ~+$12/mo (~$0.43/day) Oct 2025, ~$8M revenue gap.
- **Dominion GS-5:** ≥25 MW, effective 1 Jan 2027, 85%/60% minimums, $565.7M
  (2026) + $209.9M (2027), +$11.24/mo then +$2.36/mo, ROE 9.8%.
- **We Energies:** 5-UR-111 approved at 12.38% residential; 2027–28 request
  +10.28% / +5.52%.
- **Georgia Power:** $87.75 / 17.55¢ for 500 kWh (PSC survey).
- **MidAmerican:** no base electric rate increase since 2014 (city of Norwalk
  statement; consistent with Electric Tariff No. 2 filed Aug 2014).
- **MEC (Boydton VA):** 2021 SCC filing confirms a data-center special rate in
  Mecklenburg Electric Cooperative territory — the dataset's "AEP serves Boydton"
  attribution was wrong.
- **PJM 2025/26 BRA:** total cost to load $14.7B; $269.92/MW-day clearing price
  (widely reported; not in the report text).

---

## 4. Verification grades

Each row carries a `verification` column:

| Grade | Meaning | Rows |
|---|---|---|
| **A** | Price (EIA) **and** the water/rate-case claims checked against primary sources | **25** |
| **B** | Price (EIA) verified; water figure is secondary reporting or not published | **30** |
| **C** | Water/rate verified; price not independently checked | **0** |
| **D** | Not re-verified | **0** |

The `D` grade is now empty. Of the seven rows that started there, six were
re-graded once the utility-name mismatch that bypassed the first grading map was
fixed, and the seventh — an empty New Mexico "statewide context" stub — was
**deleted**; its content duplicates the Los Lunas row, which is graded A.

Upgrades in this pass: MidAmerican (D→A, after the Google report replaced the
"1.4B gal" estimate), Richmond/Henrico, Chesterfield, Huntsville, AEP Texas and
Texas West (D→B, once the utility-name mismatch that bypassed the first grading
map was fixed), and both New York rows (C→B, after EIA price anchors were added).

---

## 5. What is still not verified

- **Utility-specific rates.** Every price trend is a state average except where a
  docket number is cited (Dominion, We Energies, Umatilla, Georgia PSC, PNM, I&M,
  Evergy, OPPD). A utility-level EIA-861 series would be the next step.
- **2026 is Jan–Aug YTD**, not a full year; the last four months can move the
  annual figure by a few tenths of a cent.
- **Water years are not aligned.** Google is calendar 2025; utility fiscal years,
  city pumpage and state-engineer data are all different periods. Withdrawal and
  consumption are mixed across sources — rows say which when known.
- **Company-only claims** (closed-loop, "zero withdrawal", future recycling
  plants) are labelled as company claims, not measurements.
- **Territory attribution** is approximate where co-ops and IOUs overlap
  (Boydton, the Permian, northern Virginia co-op edges). The Mecklenburg fix shows
  how easily this goes wrong.
- **AWS Berwick ≈ AWS Salem Township** may be a single $20B campus, and
  **QTS Cedar Rapids vs Google Cedar Rapids** may be the same MISO load. Both
  remain flagged in the main dataset, not resolved.
