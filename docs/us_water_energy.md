# US local impacts: water consumption & energy prices around our 121 tracked sites

Companion to the main dataset (`data/canonical/data_centers.csv`, 442 sites / 121
US). Full per-utility data: **`data/us_utility_impacts.csv`** (55 rows, one per
utility territory). Each row holds sites covered, the 2021→2026 price trend, rate
events, bill-complaint groups, water consumption, water complaints, sources and a
verification grade. We researched it in Nov 2026 from web sources (regulators, EIA
figures, local news, advocacy reports). Every row carries sources.

**We re-based all price series on EIA annual data (Table 2.10) and the Jan–Aug
2026 EIA monthly table. We checked the load-bearing water and rate claims against
primary sources. What changed, and what is still soft, is in
[`us_impacts_verification.md`](us_impacts_verification.md).**

## How to read this

Sites fall into 55 distinct utility territories (municipal, IOU, co-op). For each
territory the row gives the serving utility and a 5-year residential price trend.
It also names who complains about bills, the documented water consumption, and who
complains about water. Price trends are **state averages** (EIA) unless a docket
appears. Where we know a utility sits off the state average, the row says so.

## Headline findings

**1. Bills rose in every tracked state. The clearest data center link is the PJM capacity market, not the campus next door.**
- Sharpest checked residential increases 2021→2026 YTD (EIA state data) in
  tracked-territory states:
  - **PA +53.6%** (13.76¢→21.13¢), **NY +50.2%**, **NJ +47.3%** (16.35¢→24.09¢),
    **OH +47.3%**, **IL +45.9%**, **WA +42.6%**.
  - **VA +41.7%** (11.96¢→16.95¢, with JLARC projecting up to +$37/mo by 2040),
    **OR +36.0%**, **TX +32.4%**, **NC +32.0%**, **WI +31.2%**, **MS +30.3%**.
  - **GA +23.7%** (12.51¢→15.48¢ state average). Georgia Power's 500-kWh survey
    bill is $87.75 / 17.55¢. **Duke NC +16–18%** over 2026–28.
  - US average +33.2% (13.66¢→18.19¢).
  The NJ rise includes a 17–20% step in Jun 2025, driven by PJM capacity
  auctions.
- PJM capacity auctions are the biggest single mechanical driver across
  VA/PA/NJ/IL. The 2025/26 auction cleared ~8x the prior year. PJM's
  Independent Market Monitor estimates that existing and forecast data center
  load (7.9 GW) added **$9.33B** to that auction's $14.69B total. That figure
  is a with-and-without model result, not a bill accounting
  ([IMM Part G, 3 Jun 2025](https://www.monitoringanalytics.com/reports/reports/2025/IMM_Analysis_of_the_20252026_RPM_Base_Residual_Auction_Part_G_20250603_Revised.pdf)).
- The state rise follows market structure more than local AI capacity. The six
  tracked states mostly inside PJM (PA, NJ, OH, IL, VA, WV) rose by 44% on
  average. The other 26 tracked states rose by 26%. Across all 32, the rank
  correlation with tracked operating AI capacity is 0.15, which is weak
  (`pipeline/verification/price_vs_capacity.py`). State averages have no
  controls, so this neither proves nor rules out a local effect.
- Counter-examples where utilities claim data centers LOWER bills:
  - MidAmerican IA (no base electric increase since 2014).
  - **MDU North Dakota** ($45.4M returned to customers from Applied Digital
    contracts).
  - Indiana Michigan Power (promising ~5% cuts).
  - Entergy MS/AR (claims AWS/Google revenue offsets).
  - Grant PUD WA ($0.065/kWh).
  Treat utility claims with care. In MS and AR the supporting contracts are
  **statutory trade secrets** (SB 2001). Elsewhere the utility fought in court:
  Entergy sued to block publication of the Google contract and lost.

**2. The regulatory response of 2025-2026: new data-center rate classes.**
Nearly every large utility territory now has a DC-specific tariff, or is
litigating one. Dominion GS-5 sets ≥25MW, 85% distribution/transmission and 60%
generation minimum take from 2027. AEP Ohio DCT sets ≥85% of contracted capacity
for up to 12 years. Duke NC/DEP has a large-load tariff, and Georgia Power has a
large-load rule. APS XHLF proposes +45%. NV Energy requires ≥25MW agreements. PGE
Oregon has its first-ever DC class **(+29.7% on DCs, −1.3% residential)**. Also
PPL PA, We Energies VLC, Xcel MN "rate stability", SRP E-67, I&M ≥80% minimum
demand, Oncor/SB6. Intervenors contest whether these shield ratepayers (SELC, OCC
Ohio, CUB WI/IL/MN/OR, PA OCA, which filed a formal complaint against PPL backed
by Gov. Shapiro).

**3. Named community groups complaining about energy bills** (per territory,
full list in CSV):
- **Virginia:** Piedmont Environmental Council, Coalition to Protect Prince
  William County, SELC, Sierra Club VA/CCAN ("rebuilding the grid just to serve
  data centers"). Also Data Center Defiance Central Virginia and Henrico NAACP.
- **Georgia:** Georgians for Affordable Energy ("data cost gold rush"). **The
  Nov 2025 PSC elections flipped two seats to Democrats on this issue.**
- **Memphis:** Protect Our Aquifer ("residents pay 68% more for water than Elon
  Musk's xAI"), MCAP. **NAACP/Earthjustice federal lawsuit vs xAI over ~60
  unpermitted turbines (DOJ moved to dismiss for xAI).**
- **Ohio:** Ohio Consumers' Counsel (DCs "contribute few local jobs").
- **Illinois:** CUB ("AI use and data centers are causing ComEd bills to spike").
- **New Jersey:** Division of Rate Counsel. **Energy affordability decided the
  2025 governor's race (Sherrill rate-freeze pledge).**
- **Pennsylvania:** PA OCA formal complaint and Gov. Shapiro intervention.
- **Wisconsin:** CUB ("should not pay a single cent"). The PSC forced DCs to pay
  100% of new generation costs, and Oracle withdrew its lawsuit against the rule.
- **Oklahoma:** OKC passed a first-of-kind moratorium. "YOU CAN'T DRINK DATA".
- **Arizona:** AG Kris Mayes pressing ACC over an alleged $587M cost shift.
- **Michigan:** AG Dana Nessel lost the standing fight on Stargate Saline's
  redacted DTE contracts.

**4. Water: the documented big drinkers in our US fleet.**
| Site | Documented water | Notes |
|---|---|---|
| Google Council Bluffs IA | 1,746.4M gal withdrawn / 1,346.0M consumed (2025) | more than any other Google site worldwide. ~1.3B gal consumed |
| Google Mayes County OK | 1,396.7M gal withdrawn / 1,081.4M consumed (2025) | |
| Google New Albany OH | 1,008.1M gal withdrawn / 835.7M consumed (2025) | Columbus-area DCs overall ~1.2B gal/yr of drinking-quality water (~3% of city supply) |
| Google Berkeley County SC | 988.5M gal withdrawn / 901.7M consumed (2025) | highest consumption ratio of Google's big sites |
| Google The Dalles OR | 654.3M gal withdrawn / 469.0M consumed (2025) | ~40% of the city's total water. The city sued The Oregonian to keep it secret (settled 2022) |
| Google Douglas County GA | 440.6M gal withdrawn / 367.1M consumed (2025) | plus 394.3M gal reclaimed |
| Google Lenoir NC | 378.3M gal withdrawn / 344.3M consumed (2025) | Google's #8 US site by withdrawal |
| Google Nebraska (Omaha/Papillion/Lincoln) | 732.1M gal consumed (2025, up from 134.7M in 2023 and 46.6M in 2022) | ~one week of Omaha MUD customer use |
| Meta Prineville OR | 117.5M gal (2020) | funds ASR aquifer recharge |
| xAI Colossus 1 Memphis | ~812k gpd recorded. Contract demand reported at 1.3M gpd (unverified). Expansions to 5+ MGD projected | Memphis Sand Aquifer. $80M recycling plant stalled. 19¢ vs 32¢ per 100 gal resident rate disparity |
| AWS Ridgeland MS | avg 93M gal/yr. Reported ~3.7 MGD peak-day (not in the service agreement) | would be 82% of that city system's peak capacity |
| Microsoft WDM / Meta Altoona IA | 68.5M / 64M gal (2024) | funded ASR well / city doubling supply |
| Meta Eagle Mountain UT | >35M gal in 2024. **The city contract keeps use confidential and requires the city to alert Meta to records requests** | spurred Utah HB76 disclosure law |
| Microsoft Goodyear AZ | 1.2M gpd of wastewater capacity at full build-out. Original plan up to 5M gpd, later buildings air-cooled. Actual use withheld as "proprietary" | paid $36M toward the $90M wastewater plant |
| Meta Los Lunas NM | ~70M gal/yr (State Engineer data) | "drained the Rio Grande" claim debunked (Snopes) |
| Fermi America Amarillo TX | Amarillo authorized 2.5M gpd at $8.72/1,000 gal, the highest industrial rate the city has ever charged. Company claims up to 18.5M gpd | Ogallala Aquifer concerns (Environment America) |

**5. Water complaints and disclosure fights — the pattern.**
- **Secrecy is the trigger, more than volume.** Examples: Chesterfield VA (Google
  "Peanut" 6 MGD cap undisclosed), Georgia NDAs (WSB "Data Centers & Water
  Secrets"). Also Eagle Mountain UT (confidentiality clause) and The Dalles OR
  (records lawsuit), plus Racine WI (MEA sued the city) and Coweta County GA.
  Google stopped treating site water data as a trade secret in Dec 2022. Most
  others have not.
- **Lawsuits and appeals:** MEA v. Racine (water records), Sandow Lakes Ranch v.
  Post Oak Savannah GCD (Milam County well rules), NM Supreme Court stay on a
  Project Jupiter replacement well, Sierra Club v. BLM (Lake Mead TS2), NAACP v.
  xAI.
- **Moratoria:** OKC (Apr-Dec 2026), San Marcos TX (**first full TX DC ban**,
  Jun 2026), Norman/Edmond OK and Reno NV (to Aug 2027). Also Rosemount MN and
  multiple Nebraska counties.
- **Legislation passed:** Nebraska LB1010 (water/power reporting), Utah HB76
  (disclosure), Idaho HB895/HB911 (no consumptive cooling off municipal water,
  self-funding). Also Alabama SB 270, Texas SB6, the Oregon POWER Act and the
  Georgia large-load rule. Mississippi SB 2001 is the outlier: AWS wrote it, and
  it shrouds contracts in trade-secret status.

**6. Where the water story is positive.** Applied Digital ND runs closed-loop
("about two households" per campus), and Stargate Abilene used ~8M gal fill and
~10M/yr. Hut 8 Beacon Point & Galaxy Helios are self-supplied closed-loop, and
TeraWulf NY runs zero withdrawal, closed loop. Also Nebius Vineland (Bloom fuel
cells, minimal water) and Meta Kuna ID (gave 2.5M gpd of rights to the city +
$100M system). Google Mesa switched to air-cooled because of water risk. We
Energies/Port Washington & Mount Pleasant WI make closed-loop claims, which are
disputed.

## Dataset corrections found during this research (applied)

1. **Cipher Barber Lake is in Colorado City, Texas**, not Barbour County, WV
   (Cipher 8-K, Sep 2025). We fixed the row. The WV Mon Power row in the CSV
   remains only as regional context.
2. **Nscale NC-1 is in the town of Madison, Rockingham County**, not Madison
   County (Duke Energy Carolinas territory). Fixed.
3. **Mecklenburg Electric Cooperative, Southside Electric Coop and Dominion
   serve Microsoft Boydton, not AEP Virginia** (EIA territory data). We added a
   note. AEP's Boydton attribution was wrong.
4. Possible duplicate: **AWS Berwick ≈ AWS Salem Township (Susquehanna)** may be
   a single $20B campus (flagged, both rows kept).

## Checks (Nov 2026)

We re-based every price series on EIA annual data, and we checked every
load-bearing water claim against a primary source. The 2021 baselines we first
supplied were **~1¢/kWh too low in most states**. Examples: Virginia 11.0¢ vs
EIA 11.96¢, Arkansas 9.9¢ vs 11.27¢, Georgia 11.7¢ vs 12.51¢. Several 2025
figures were mid-year quotes or "typical bill ÷ 1,000 kWh" arithmetic. Three
water figures changed materially (Council Bluffs, New Albany, Google Nebraska).
We downgraded two to "reported, unverified" (AWS Ridgeland's 3.67 MGD peak,
xAI's 1.3 MGD contract demand). We overstated one claim: Fermi's $8.72/1,000 gal
is the highest industrial rate Amarillo has ever charged, but "double the
standard rate" was not supported. Full log, correction table and the items still
soft: [`us_impacts_verification.md`](us_impacts_verification.md).

## Caveats

- Price trends are **EIA state averages** (annual Table 2.10 for 2021/2024/2025,
  EEM Table 5.6.B for Jan–Aug 2026 YTD), not utility-specific rates. Rows add
  docket-level detail where we know the utility diverges from the state
  average. 2026 is a partial year.
- "Bill complaint groups" lists named, sourced complaints only. The absence of a
  group does not mean an absence of concern.
- Water figures are a patchwork of utility disclosures, sustainability reports
  and journalism. Methods differ (withdrawal vs consumption, potable vs
  reclaimed, calendar vs fiscal years). Rows say which when known.
- Verification grades in the CSV: **A** = price and water/rate both checked
  against primary sources (25 rows), **B** = price checked, water secondary or
  unpublished (30 rows). See [`us_impacts_verification.md`](us_impacts_verification.md)
  for the correction table and the items still unchecked.
