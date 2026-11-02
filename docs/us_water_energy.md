# US local impacts: water consumption & energy prices around our 121 tracked sites

Companion to the main dataset (`data/canonical/data_centers.csv`, 442 sites / 121 US).
Full per-utility data: **`data/us_utility_impacts.csv`** (55 rows, one per utility
territory: sites covered, 2021→2026 price trend, rate events, bill-complaint
groups, water consumption, water complaints, sources, verification grade).
Researched Nov 2026 via web sources (regulators, EIA figures, local news,
advocacy reports); every row carries sources.

**All price series were re-based on EIA annual data (Table 2.10) and the
Jan–Aug 2026 EIA monthly table, and the load-bearing water/rate claims were
checked against primary sources. What changed, and what is still soft, is in
[`us_impacts_verification.md`](us_impacts_verification.md).**

## How to read this

Sites were grouped into 55 distinct utility territories (municipal, IOU, co-op).
For each: the serving utility, 5-year residential price trend, who is complaining
about bills, documented water consumption, and who is complaining about water.
Price trends are **state averages** (EIA) unless a docket is cited; where a
utility is known to sit off the state average, the row says so.

## Headline findings

**1. Bills are rising everywhere, but data centers are being blamed unevenly.**
- Sharpest verified residential increases 2021→2026 YTD (EIA state data) in
  tracked-territory states: **PA +53.6% (13.76¢→21.13¢)**, **NY +50.2%**,
  **NJ +47.3% (16.35¢→24.09¢, including a 17–20% step in Jun 2025 driven by PJM
  capacity auctions)**, **OH +47.3%**, **IL +45.9%**, **WA +42.6%**,
  **VA +41.7% (11.96¢→16.95¢, with JLARC projecting up to +$37/mo by 2040)**,
  **OR +36.0%**, **TX +32.4%**, **NC +32.0%**, **WI +31.2%**, **MS +30.3%**,
  **GA +23.7% (12.51¢→15.48¢ state average; Georgia Power's 500-kWh survey bill
  is $87.75 / 17.55¢)**, **Duke NC (+16–18% over 2026–28)**. US average +33.2%
  (13.66¢→18.19¢).
- PJM capacity auctions are the biggest single mechanical driver across
  VA/PA/NJ/IL: 2025/26 cleared ~8x the prior year.
- Counter-examples where utilities claim DCs LOWER bills: MidAmerican IA
  (no base electric increase since 2014), **MDU North Dakota ($45.4M returned
  to customers from Applied Digital contracts)**, Indiana Michigan Power
  (promising ~5% cuts), Entergy MS/AR (claims AWS/Google revenue offsets),
  Grant PUD WA ($0.065/kWh). Treat utility claims with care — in MS and AR the
  supporting contracts are **statutory trade secrets** (SB 2001) or were fought
  over in court (Entergy sued to block publication of the Google contract and lost).

**2. The regulatory response of 2025-2026: new data-center rate classes.**
Nearly every large utility territory now has (or is litigating) a DC-specific
tariff — Dominion GS-5 (≥25MW, 85% distribution/transmission and 60% generation
minimum take from 2027), AEP Ohio DCT (≥85% of contracted
capacity for up to 12 years), Duke NC/DEP large-load tariff, Georgia Power
large-load rule, APS XHLF (+45% proposed), NV Energy mandatory ≥25MW agreements,
PGE Oregon's first-ever DC class **(+29.7% on DCs, −1.3% residential)**,
PPL PA, We Energies VLC, Xcel MN "rate stability", SRP E-67, I&M ≥80% minimum
demand, Oncor/SB6. Whether these shield ratepayers is contested by intervenors
(SELC, OCC Ohio, CUB WI/IL/MN/OR, PA OCA — which filed a formal complaint against
PPL backed by Gov. Shapiro).

**3. Named community groups complaining about energy bills** (per territory,
full list in CSV):
- **Virginia:** Piedmont Environmental Council, Coalition to Protect Prince
  William County, SELC, Sierra Club VA/CCAN ("rebuilding the grid just to serve
  data centers"), Data Center Defiance Central Virginia, Henrico NAACP.
- **Georgia:** Georgians for Affordable Energy ("data cost gold rush");
  **the Nov 2025 PSC elections flipped two seats to Democrats on this issue.**
- **Memphis:** Protect Our Aquifer — "residents pay 68% more for water than
  Elon Musk's xAI"; MCAP; **NAACP/Earthjustice federal lawsuit vs xAI over ~60
  unpermitted turbines (DOJ moved to dismiss for xAI)**.
- **Ohio:** Ohio Consumers' Counsel (DCs "contribute few local jobs").
- **Illinois:** CUB ("AI use and data centers are causing ComEd bills to spike").
- **New Jersey:** Division of Rate Counsel; **energy affordability decided the
  2025 governor's race (Sherrill rate-freeze pledge)**.
- **Pennsylvania:** PA OCA formal complaint + Gov. Shapiro intervention.
- **Wisconsin:** CUB ("should not pay a single cent") — PSC forced DCs to pay
  100% of new generation costs; Oracle withdrew its lawsuit against the rule.
- **Oklahoma:** OKC passed a first-of-kind moratorium; "YOU CAN'T DRINK DATA".
- **Arizona:** AG Kris Mayes pressing ACC over an alleged $587M cost shift.
- **Michigan:** AG Dana Nessel lost the standing fight on Stargate Saline's
  redacted DTE contracts.

**4. Water: the documented big drinkers in our US fleet.**
| Site | Documented water | Notes |
|---|---|---|
| Google Council Bluffs IA | 1,746.4M gal withdrawn / 1,346.0M consumed (2025) | more than any other Google site worldwide; ~1.3B gal consumed |
| Google Mayes County OK | 1,396.7M gal withdrawn / 1,081.4M consumed (2025) | |
| Google New Albany OH | 1,008.1M gal withdrawn / 835.7M consumed (2025) | Columbus-area DCs overall ~1.2B gal/yr of drinking-quality water (~3% of city supply) |
| Google Berkeley County SC | 988.5M gal withdrawn / 901.7M consumed (2025) | highest consumption ratio of Google's big sites |
| Google The Dalles OR | 654.3M gal withdrawn / 469.0M consumed (2025) | ~40% of the city's total water; city sued The Oregonian to keep it secret (settled 2022) |
| Google Douglas County GA | 440.6M gal withdrawn / 367.1M consumed (2025) | plus 394.3M gal reclaimed |
| Google Lenoir NC | 378.3M gal withdrawn / 344.3M consumed (2025) | Google's #8 US site by withdrawal |
| Google Nebraska (Omaha/Papillion/Lincoln) | 732.1M gal consumed (2025, up from 134.7M in 2023 and 46.6M in 2022) | ~one week of Omaha MUD customer use |
| Meta Prineville OR | 117.5M gal (2020) | funds ASR aquifer recharge |
| xAI Colossus 1 Memphis | ~812k gpd recorded; contract demand reported at 1.3M gpd (unverified); expansions to 5+ MGD projected | Memphis Sand Aquifer; $80M recycling plant stalled; 19¢ vs 32¢ per 100 gal resident rate disparity |
| AWS Ridgeland MS | avg 93M gal/yr; reported ~3.7 MGD peak-day (not in the service agreement) | would be 82% of that city system's peak capacity |
| Microsoft WDM / Meta Altoona IA | 68.5M / 64M gal (2024) | funded ASR well / city doubling supply |
| Meta Eagle Mountain UT | >35M gal 2024; **city contract keeps use confidential and requires alerting Meta to records requests** | spurred Utah HB76 disclosure law |
| Microsoft Goodyear AZ | 1.2M gpd of wastewater capacity at full build-out; original plan up to 5M gpd, later buildings air-cooled; actual use withheld as "proprietary" | paid $36M toward the $90M wastewater plant |
| Meta Los Lunas NM | ~70M gal/yr (State Engineer data) | "drained the Rio Grande" claim debunked (Snopes) |
| Fermi America Amarillo TX | Amarillo authorized 2.5M gpd at $8.72/1,000 gal — the highest industrial rate the city has ever charged; company claims up to 18.5M gpd | Ogallala Aquifer concerns (Environment America) |

**5. Water complaints and disclosure fights — the pattern.**
- **Secrecy is the trigger, more than volume:** Chesterfield VA (Google "Peanut"
  6 MGD cap undisclosed), Georgia NDAs (WSB "Data Centers & Water Secrets"),
  Eagle Mountain UT (confidentiality clause), The Dalles OR (records lawsuit),
  Racine WI (MEA sued the city), Coweta County GA. Google stopped treating site
  water data as a trade secret in Dec 2022, but most others haven't.
- **Lawsuits/appeals:** MEA v. Racine (water records); Sandow Lakes Ranch v.
  Post Oak Savannah GCD (Milam County well rules); NM Supreme Court stay on a
  Project Jupiter replacement well; Sierra Club v. BLM (Lake Mead TS2); NAACP v. xAI.
- **Moratoria:** OKC (Apr-Dec 2026), San Marcos TX (**first full TX DC ban**,
  Jun 2026), Norman/Edmond OK, Reno NV (to Aug 2027), Rosemount MN pause,
  multiple Nebraska counties.
- **Legislation passed:** Nebraska LB1010 (water/power reporting), Utah HB76
  (disclosure), Idaho HB895/HB911 (no consumptive cooling off municipal water;
  self-funding), Alabama SB 270, Texas SB6, Oregon POWER Act, Georgia large-load
  rule, Mississippi SB 2001 (the outlier: written for AWS, shrouds contracts in
  trade-secret status).

**6. Where the water story is positive.** Applied Digital ND ("about two
households" per campus, closed-loop), Stargate Abilene (~8M gal fill, ~10M/yr),
Hut 8 Beacon Point & Galaxy Helios (self-supplied closed-loop), TeraWulf NY
(zero withdrawal, closed loop), Nebius Vineland (Bloom fuel cells, minimal
water), Meta Kuna ID (gave 2.5M gpd of rights to the city + $100M system),
Google Mesa (switched to air-cooled because of water risk), We Energies/
Port Washington & Mount Pleasant WI (closed-loop claims, disputed).

## Dataset corrections found during this research (applied)

1. **Cipher Barber Lake is in Colorado City, Texas** — not Barbour County, WV
   (Cipher 8-K, Sep 2025). Row corrected; the WV Mon Power row in the CSV is
   kept only as regional context.
2. **Nscale NC-1 is in the town of Madison, Rockingham County** — not Madison
   County (Duke Energy Carolinas territory). Corrected.
3. **Microsoft Boydton is served by Mecklenburg Electric Cooperative /
   Southside Electric Coop / Dominion — not AEP Virginia** (EIA territory
   data). Note added; AEP's Boydton attribution was wrong.
4. Possible duplicate: **AWS Berwick ≈ AWS Salem Township (Susquehanna)** may
   be a single $20B campus (flagged, both rows kept).

## Verification (Nov 2026)

Every price series was re-based on EIA annual data and every load-bearing water
claim was checked against a primary source. The 2021 baselines originally
supplied were **~1¢/kWh too low in most states** (Virginia 11.0¢ vs EIA 11.96¢;
Arkansas 9.9¢ vs 11.27¢; Georgia 11.7¢ vs 12.51¢), and several 2025 figures were
mid-year quotes or "typical bill ÷ 1,000 kWh" arithmetic. Three water figures
changed materially (Council Bluffs, New Albany, Google Nebraska), two were
downgraded to "reported, unverified" (AWS Ridgeland's 3.67 MGD peak; xAI's
1.3 MGD contract demand), and one claim was overstated: Fermi's $8.72/1,000 gal
is the highest industrial rate Amarillo has ever charged, but "double the
standard rate" was not supported. Full log, correction table and the items still
soft: [`us_impacts_verification.md`](us_impacts_verification.md).

## Caveats

- Price trends are **EIA state averages** (annual Table 2.10 for 2021/2024/2025;
  EEM Table 5.6.B for Jan–Aug 2026 YTD), not utility-specific rates. Rows add
  docket-level detail where the utility is known to diverge from the state
  average. 2026 is a partial year.
- "Bill complaint groups" lists named, sourced complaints only; absence of a
  group ≠ absence of concern.
- Water figures are a patchwork of utility disclosures, sustainability reports
  and journalism; methodologies differ (withdrawal vs consumption, potable vs
  reclaimed, calendar vs fiscal years). Rows say which when known.
- Verification grades in the CSV: **A** = price and water/rate both checked
  against primary sources (25 rows), **B** = price verified, water secondary or
  unpublished (30 rows). See [`us_impacts_verification.md`](us_impacts_verification.md)
  for the correction table and the items still unverified.
