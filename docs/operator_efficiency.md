# Operator efficiency: Google vs Meta vs Microsoft vs AWS vs xAI vs the neoclouds

Companion to `data/canonical/data_centers.csv` and `data/operator_efficiency.csv`.
Built Nov 2026 from each company's own environmental disclosure where one exists.

**Short version:** Meta is the most efficient of the big four on *both* axes
(PUE 1.08, WUE 0.19 L/kWh). AWS uses the least water per kWh (0.12). Google has
the best PUE of the largest fleet. But it is **5–8× more water-intensive per kWh**
than Meta or AWS, because it still evaporatively cools its biggest campuses.
Microsoft sits in the middle. The neoclouds that disclose (Nebius, Crusoe) post
better water numbers than any hyperscaler. Those numbers come from cold-climate,
liquid-cooled designs, not fleet-wide operations. xAI, CoreWeave, Applied
Digital, Lambda and Galaxy publish nothing usable.

---

## 1. What we have on Meta

22 Meta sites in the main dataset (US, Ireland, Denmark, Sweden, Canada), plus
fleet-level disclosure:

| Meta, data centers only | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|
| Electricity (TWh) | 6.97 | 9.12 | 11.17 | 14.98 | **18.06** |
| PUE | 1.10 | 1.09 | 1.08 | 1.08 | **1.08** |
| WUE (L/kWh, withdrawal) | 0.30 | 0.26 | 0.20 | 0.18 | **0.19** |
| Water withdrawn (ML) | — | — | — | — | **4,145** |
| Water consumed (ML) | — | — | — | — | **2,974** |

That is ~1.10B gal withdrawn and **~786M gal consumed** across Meta's entire
global fleet in 2024. It is less than **one** Google site: Council Bluffs
consumed 1.35B gal in 2025. Meta's electricity is 100% renewable-matched. EY
provides limited assurance on select metrics.

Meta's latest disclosure is **FY2024**. The other three have 2025 or FY25 data,
so the comparison below is close but not same-year.

---

## 2. Fleet efficiency, side by side

| Operator | Year | PUE | WUE (L/kWh) | Water per MW-year (gal) | Renewable / low-carbon | Disclosure |
|---|---|---:|---:|---:|---|---|
| **Meta** | 2024 | **1.08** | **0.19** (withdrawal) | 440,000 | 100% matched | A |
| **Google** | 2025 | **1.09** | **1.02** (consumption, derived) | 2,360,000 | 100% matched | A |
| **AWS** | 2025 | 1.14 | **0.12** | 278,000 | 100% matched | A |
| **Microsoft** | FY25 | 1.17 | 0.27 | 625,000 | <100% (2030 goal) | A |
| **xAI** | 2025-26 | ND | ~1.0 (estimate) | ~2,310,000 | none disclosed | D |
| **Nebius** | 2025 | 1.25 portfolio / 1.15 own site | **0.018** (Finland-1) | 42,000 | 62% renewable | B |
| **Crusoe** | 2025 | 1.2–1.4 design | **~0.002** | 4,600 | site-specific | B |
| **IREN** | 2025 | 1.1 air / ~1.2 liquid (guidance) | ND | ND | BC hydro | C |
| **TeraWulf** | 2025 | 1.15 (secondary) | ND | ND | ~60% | C |
| **CoreWeave** | 2025 | ND ("collecting PUE data") | ND | ND | ND | D |
| **Applied Digital** | 2025 | ND (claims only) | ND | ND | claims | D |
| **Lambda** | 2026 | ND (relative claim) | ND | ND | ND | D |
| **Galaxy** | 2025 | ND | ND | ND | ND | D |

Water per MW-year = WUE × 8,760 h × 1,000 kW ÷ 3.785 L/gal. That is the water a
1 MW IT load would use if it ran flat out for a year. It is a normaliser, not a
prediction.

---

## 3. The finding: energy and water trade off

Ranking by PUE and by WUE gives almost opposite orders:

- **PUE (lower better):** Meta 1.08 → Google 1.09 → AWS 1.14 → Microsoft 1.17.
- **WUE (lower better):** AWS 0.12 → Meta 0.19 → Microsoft 0.27 → Google 1.02.

That is not a contradiction. Evaporative cooling is *thermodynamically cheap*.
It cuts compressor load and therefore PUE, but it consumes water. Air-cooled and
closed-loop designs do the reverse. Google runs evaporative cooling at its
largest campuses (Council Bluffs, Mayes County, Berkeley County, The Dalles,
New Albany). That is why its PUE is excellent and its water intensity is the
worst of the four. Meta and AWS moved earlier to closed-loop and dry designs.
That costs a little energy and saves a lot of water.

So "who is most efficient" depends on which resource you price:

- In **water-stressed** places, the Meta and AWS design wins.
- In **hot, humid** places with cheap water, the Google design wins on energy.
- The honest metric is total resource cost, and no operator publishes it.

A second-order point: Microsoft measures its 1.17 only on data centers it
"fully owns and controls and that were operational for 12 months". That excludes
leased capacity and new builds, and both drag PUE up. So 1.17 is a favourable
boundary compared with Google's or Meta's fleet-wide numbers.

---

## 4. The neoclouds: design vs disclosure

The two that publish real numbers look dramatically better than the
hyperscalers:

- **Nebius:** portfolio PUE 1.25 (vs global average 1.54). At its Finland-1 site
  it reports **0.018 L/kWh**, which is 10× better than AWS and 55× better than
  Google. But that is one cold-climate, liquid-cooled, fully owned facility. The
  portfolio number is 1.25.
- **Crusoe:** Crusoe built Abilene to a **design PUE of 1.2–1.4**, tightening to
  1.1–1.25 for projects from 2026. It uses closed-loop cooling at **~910,000
  gal/yr for 200 MW** (~0.002 L/kWh). These are design targets, not audited
  operating data.

The rest are a transparency vacuum. CoreWeave's annual report says it is
"collecting the necessary PUE data". Applied Digital's white paper asserts that
liquid and free cooling lower PUE and WUE, but gives no figure. Lambda claims
direct-to-chip improves PUE "by over 15%" with no baseline. Galaxy publishes
nothing. IREN and TeraWulf give partial numbers (1.1–1.2 PUE) with no water.

**xAI is the extreme case.** It publishes no PUE, no WUE, no energy or emissions
data. It runs on-site gas turbines and takes water from the Memphis Sand
Aquifer. A bottom-up estimate from MLGW's own documents uses 812,502 gpd and
150 MW now (300 MW requested). That puts xAI near **1.0 L/kWh**, which is
Google-class water intensity. Treat it as a ±25% estimate, not a measurement.

---

## 5. Does our dataset reconcile with the disclosures?

Yes, roughly, and the gaps are informative:

| Operator | Average draw implied by disclosure | IT capacity in our dataset | Reading |
|---|---:|---:|---|
| Meta | 18.06 TWh ÷ 8,760 h = **2.06 GW** | ~3.97 GW nameplate IT | ~52% utilisation. Plausible for a fleet still ramping AI capacity. We track nearly all of Meta's fleet. |
| Google | 42.4 TWh ÷ 8,760 h ÷ 1.09 = **4.44 GW IT** | ~2.76 GW nameplate IT | ~62% coverage. We track the big campuses, not the long tail. |

Meta's nameplate is ~2× its average draw. You would expect that from capacity
built ahead of load. Google's coverage gap is what you would expect from a
"major campuses only" scope.

---

## 6. Why this is not yet a true efficiency comparison

1. **Different years.** Meta 2024. Google and AWS 2025. Microsoft FY25
   (to Jun 2025).
2. **Different boundaries.** Microsoft excludes leased sites and sites younger
   than 12 months. Google and Meta report fleet-wide. AWS reports global totals
   but not absolute volumes. Nobody uses the same definition of "data center".
3. **Different WUE definitions.** Meta and AWS divide *withdrawal* by IT kWh.
   Microsoft divides cooling and humidification water by IT kWh. Google publishes
   neither, so we derive the figure here from consumption. Consumption is always
   ≤ withdrawal. So Google's number is the most favourable version available, and
   it is still 5× Meta's.
4. **PUE is not compute efficiency.** It says nothing about useful work per
   joule. A 1.08 facility full of idle GPUs is worse than a 1.25 facility
   running flat out. A real comparison needs tokens/joule or FLOPS/W at the
   workload level, and no operator publishes that comparably.
5. **Renewable "matching" is annual and global**, not hourly and local. 100%
   matched does not mean the electrons serving a given campus are renewable.

A defensible comparison would fix the year, the boundary and the utilisation,
then add a workload benchmark (e.g. MLPerf power) on top. Until then, the table
above is the best available. The disclosure column is as important as the PUE
column.

---

## Sources

- Google, *2026 Environmental Report* (electricity p.93, water p.96–97)
- Meta, *2025 Environmental Data Index* (FY2024)
- Microsoft, datacenter efficiency page (FY24/FY25 PUE and WUE table)
- Amazon, *2025 AWS Summary* (PUE 1.14, WUE 0.12)
- Nebius, *2025 Sustainability Report*
- Crusoe, *2025 Impact Report*
- IREN Q4 FY25 earnings call
- TeraWulf via datacentersearch.org
- CoreWeave 2025 annual report
- Applied Digital white-paper release
- Lambda infrastructure page
- S&P on Galaxy Helios
- MLGW, *xAI Update* (5 May 2025) for the 150/300 MW sequence

Full machine-readable table: `data/operator_efficiency.csv`.
