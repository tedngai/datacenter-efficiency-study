# Global AI Data Centers — H100-Equivalent Compute Dataset

A dataset of **442 major AI / hyperscale data center campuses worldwide** with their power
capacity, announced GPU counts, announced FLOPS, and estimated compute in
**H100-equivalents (H100e)**.

## Files

| File | Description |
|---|---|
| `data/published/data_centers.csv` | Final dataset, one row per campus, sorted by best H100e estimate |
| `data/published/data_centers.json` | Same data as JSON (typed numbers) |
| `index.html` | Self-contained Compute Atlas dashboard: filterable map, site leaderboard, PUE/WUE explorer, and energy–water scenario lab. Open directly in a browser. |
| `data/canonical/data_centers.csv` | Canonical source of truth (edit this, then rebuild) |
| `data/raw/data_centers_raw.csv` | Original research capture (kept for provenance) |
| `pipeline/build.py` | Computes H100e columns and regenerates outputs: `python pipeline/build.py` |
| `pipeline/frontend/` | Maintainable HTML template, CSS, and JavaScript embedded into `index.html` by the build |
| `pipeline/country_table.py` | Regenerates the country-level summary table |
| `data/us_utility_impacts.csv` | 55 US utility territories: prices, rate cases, water, complaint groups |
| `docs/us_water_energy.md` | US local energy/water impacts report |
| `docs/us_impacts_verification.md` | Verification log for the US impacts study |
| `data/operator_efficiency.csv` | PUE / WUE / water-per-MW-year for 13 operators |
| `docs/operator_efficiency.md` | Operator efficiency analysis and comparability caveats |
| `DATA_DICTIONARY.md` | Column definitions for all three published CSVs |
| `AGENTS.md` | Operating brief for AI agents: role, conventions, git and credential policy |
| `PROGRESS.xml` | Append-only log of decisions, incidents, verifications and changes |

Companion studies: `data/us_utility_impacts.csv` + `docs/us_water_energy.md` (US local
energy/water impacts, with `docs/us_impacts_verification.md`) and
`data/operator_efficiency.csv` + `docs/operator_efficiency.md` (PUE/WUE comparison
across Google, Meta, Microsoft, AWS, xAI and the neoclouds).

## Interactive dashboard

`index.html` combines both published datasets in a responsive, dependency-light
interface:

- **Global atlas:** search and filter 442 campuses, switch between H100e and power
  marker sizing, inspect site notes and sources, and export the filtered rows.
- **Efficiency explorer:** compare PUE and WUE on a log-scale chart, then inspect
  each operator's reporting year, boundary, water basis, and disclosure grade.
- **Scenario lab:** compare annual facility electricity, non-IT overhead, and water
  for two operator profiles at a chosen IT load. Results are unit conversions at
  full utilization, not campus forecasts.

Edit the sources in `pipeline/frontend/`, then run `python pipeline/build.py` to
regenerate the self-contained page. Site and operator values are embedded at build
time; the map tiles, Leaflet, and web fonts require an internet connection.

## H100e methodology

An **H100e** = the compute of one NVIDIA H100 SXM. Since operators don't publish H100e,
every value here is an estimate. Four estimates are computed; `h100e_best` uses the most
direct available signal:

1. **`h100e_gpu` — from announced GPU counts** (most direct). Conversion factors
   (dense FP8 compute ratio vs H100's 1,979 TFLOPS):
   - H100 / H200 / H800 / unspecified "GPUs" = **1.0**
   - B200 / GB200 = **2.25**; GB300/B300 = **2.5**
   - A100 = **0.315**; Trainium2 = **0.34**; Ascend 910B ≈ **0.35**
2. **`h100e_third_party`** — estimates from Epoch AI's data center directory, recorded
   during research (used for several Stargate sites, China sites, DayOne, etc.).
3. **`h100e_flops`** — announced cluster peak PFLOPS (dense FP8-equivalent) ÷ 1.979.
4. **`h100e_power`** — power-based estimate: assume 60% of IT load powers H100-class
   accelerator systems at ~1.2 kW per GPU → **500 H100e per MW of IT load**. If only gross
   facility power is known, IT load = MW ÷ 1.2 (PUE 1.2) → **≈417 H100e per MW**.

`h100e_method` says which estimate `h100e_best` came from: `gpu_count` > `third_party` >
`flops` > `power`.

## Columns

`name, operator, city, state_province, country, latitude, longitude, power_capacity_mw,
it_load_mw, announced_gpu_count, gpu_types, cluster_peak_pflops, h100e_gpu,
h100e_third_party, h100e_flops, h100e_power, h100e_best, h100e_method, status,
status_note, source_url`

- `power_capacity_mw` = gross facility/utility power; `it_load_mw` = IT load where reported.
- Blank = not published / not found. **No values were invented** — where a figure is a
  rumor or analyst estimate, that is noted in `status_note`.
- `cluster_peak_pflops` kept only where officially announced (mostly blank — few operators
  publish it; the Deutsche Telekom 0.5 EFLOPS claim is inconsistent with its GPU count and
  kept as-announced, see note).

## Status classification

Each site has a `status` column (also color-coded on the map):

| Status | Meaning | Count |
|---|---|---|
| `operational` | Fully operating; campus may still have announced expansions | 199 |
| `partially_operational` | First phase(s) live, but the campus is still ramping to its target capacity | 35 |
| `under_construction` | Construction underway; no live AI capacity yet (or first energization imminent) | 117 |
| `planned` | Announced/leased, construction not yet started (incl. some with uncertain status) | 91 |

So **only 199 of 442 sites (45%) are fully operational** — the field is dominated by
gigawatt-scale projects still being built. Judged by H100e, the split is starker still:
roughly two-thirds of the total tracked compute sits in sites that are not yet fully
operational (the biggest single estimates — Stargate Saline, Port Washington, Hyperion,
Prometheus, Stargate UAE — are all still ramping or under construction).

**Regional coverage note**: the first research pass was thin on Asia and empty on Latin
America; later deep-dives expanded China (24 sites — the "Eastern Data, Western Computing"
intelligent computing centers), Malaysia (22 sites — Johor is one of the fastest-growing
AI DC markets), Japan (15), South Korea (12), Europe (+26, incl. EuroHPC AI factories and
gigafactory candidates), the Middle East (+19), and Latin America (+15 — mostly an
announced pipeline; no operating 50MW+ AI-dedicated campus or 10k+ GPU cluster exists in
the region yet, the largest GPU deployment being Mexico's planned 14,480-GPU Coatlicue
supercomputer). A final North America pass added Canada (+14 — including Meta's first
Canadian DC, the 1GW Sturgeon campus, Canada's sovereign AI factories from TELUS/Bell/
Calcul Québec, and the speculative 7.5GW Wonder Valley proposal), deeper Mexico (+17 —
the Querétaro corridor: AWS/Google/Oracle/Alibaba regions, ODATA QR01/02/04, Ascenty,
Bleeding Edge's LatAm-first Blackwell B300 neocloud), and the first Central America/
Caribbean entries (+4 — all small or speculative; the region has no AI-scale campus yet).
Three final passes added Africa (+15 — Teraco Johannesburg/Cape Town, Nigeria's Kasi
and Rack Centre, Egypt's sovereign AI DC, Morocco's Nexus; no published GPU counts
anywhere on the continent), Eastern Europe/Caucasus/Central Asia (+18 — EuroHPC AI
factories in Czechia/Romania/Bulgaria/Lithuania/Slovenia/Hungary, Kazakhstan's Alem
H200 supercomputer and 100k-GPU Data Center Valley, Armenia's Firebird), and
India/South Asia (+21 — the IndiaAI national GPU pool, Yotta's Blackwell Ultra buildout,
L&T Vyoma's 10k-B300 factory for Together AI, Google/Adani Vizag and other gigawatt
campuses; Pakistan/Bangladesh get their first entries). A US re-sweep (+63) then filled
the biggest remaining hole: Google's TPU-campus fleet (Columbus/New Albany/Lancaster OH,
Bristow VA, Omaha/Lincoln/Papillion NE, Mesa AZ, Midlothian TX, Kansas City, Storey
County NV — several with 100k-330k H100e Epoch estimates), Meta's remaining sites
(Rosemount, Kuna, Cheyenne, Eagle Mountain, Los Lunas, Montgomery, Temple, Bowling
Green, El Paso 1GW), Microsoft (Pecos 2GW, Goodyear, Project Osmium), AWS (Berwick PA
Rainier leg, Richmond County NC, Georgia, Arizona), QTS Richmond (~562MW), plus the
crypto-to-AI conversion wave (Hut 8 Beacon Point 1GW for Nvidia, Riot, Cipher/AWS,
Bitdeer, MARA, Core Scientific, Bitfarms, Applied Digital PF3) and neoclouds (Nscale
Ward County, Vultr's 24k-MI355X Springfield supercluster, CloudBurst, and Fermi
America's proposed 11GW Amarillo HyperGrid — now the single largest power figure in
the dataset, still speculative). A final country-by-country sweep (+63) closed the
remaining regional gaps: Australia went from 1 to 9 sites (AirTrunk SYD2/SYD3/MEL1/MEL2,
CDC Marsden Park at 720MW — the Southern Hemisphere's largest — NEXTDC M3, Firmus's
18,400-GPU GB300 cluster, AWS Sydney), Singapore from 0 to 2 (Nxera Tuas, AirTrunk),
Indonesia 0 to 2 (Oracle and PDG in Batam), Thailand 0 to 2, the Philippines 0 to 1
(VITRO), New Zealand 0 to 1 (Datagrid's 1GW Invercargill project), Denmark 0 to 3
(Meta Odense ~475MW, Google Fredericia, CA Skive), Belgium 0 to 1 (Google
Saint-Ghislain), Ireland 1 to 3 (Meta Clonee, AWS Cruiserath), Netherlands 1 to 3
(Google Eemshaven, Microsoft Middenmeer), Spain +Microsoft Aragon, France +SoftBank
Bouchain/Eclairion, Italy +Trino/Milan, Sweden +atNorth Sollefteå; plus Canada's
Saskatchewan/New Brunswick wave, Brazil's RT-One/Ada/Tecto buildout, Chile's Cerrillos
and Ascenty SCL04/05, Peru's first entry, Saudi Microsoft region, Oman/Jordan 400MW
proposals, Israel's Ofek, Kenya's iXAfrica, and India's STT Palava/PDG MU1/AdaniConneX
Noida/CtrlS Future City additions.
Chinese sites mostly use Ascend/heterogeneous chips; their announced
"X万P" figures are FP16/mixed-precision and recorded in notes, not converted inflated
into `cluster_peak_pflops`.

## Caveats

- **Scope**: major AI/hyperscale campuses only (roughly 100 MW+ or named 10k+ GPU
  clusters). Ordinary colo/enterprise data centers and national-lab supercomputers
  (Frontier, El Capitan, JUPITER…) are excluded.
- **Estimates span very different confidence levels**: an Epoch AI projection for a 2028
  build-out and a measured IT load are not equally reliable. Read `status_note` before
  quoting any number.
- Power-based H100e is an upper-bound-style estimate — it credits the whole campus to
  H100-class accelerators, which overstates sites that host general cloud workloads.
- Data compiled via web research from operator press releases, regulator filings, Epoch AI,
  DataCenterDynamics, and press coverage (sources in `source_url`), current as of
  **November 2026**. The field moves fast — many "under construction" figures are targets.
- GPU conversion factors are dense-FP8 compute ratios and ignore memory bandwidth, FP4,
  and interconnect differences that matter a lot in practice.

## Headline numbers (as of compilation)

- **442 campuses**, 353 with a quantifiable H100e estimate
- **~64.0M H100e** total across tracked sites (heavily skewed by gigawatt-scale builds
  still under construction — see status classification above; the two largest figures,
  Fermi America's ~4.6M and Wonder Valley's ~3.1M H100e power-based estimates, are
  speculative proposals without confirmed tenants)
- Largest tracked sites: Stargate Saline Township MI (~2.9M), Stargate Port Washington WI
  (~2.6M), Meta Prometheus OH (~2.25M), Meta Hyperion LA (~2.1M power-est), Stargate UAE
  (~2.0M), xAI Colossus 2 (~1.1M), Stargate Abilene TX (~1.0M)

## US local impacts (water & energy prices)

Companion research on the 121 US sites: **`data/us_utility_impacts.csv`** (55 rows, one
per utility territory: serving utility & type, 5-year energy price trend, rate
events, named community groups complaining about bills, documented water
consumption, water complaints, sources, and a verification grade) and
**`docs/us_water_energy.md`** (summary, headline findings, and the water big-drinker
table). All price series were re-based on EIA annual data (Table 2.10) and the
Jan–Aug 2026 monthly table, and the load-bearing water/rate claims were checked
against primary sources — see **`docs/us_impacts_verification.md`** for the correction
table and residual caveats.

Key takeaways: PJM capacity costs drove the sharpest 2021→2026 bill increases
(PA +53.6%, NJ +47.3%, OH +47.3%, IL +45.9%, VA +41.7%; US average +33.2%);
2025-26 brought a wave of data-center rate classes (Dominion GS-5, AEP Ohio DCT,
Duke, PGE Oregon +29.7% on DCs); water-disclosure secrecy is the most common
trigger for complaints (The Dalles, Chesterfield "Peanut", Eagle Mountain
confidentiality clause, Racine lawsuit); three dataset errors were found and
fixed via this research (Cipher Barber Lake → Colorado City TX; Nscale → town of
Madison, Rockingham County NC; Boydton → co-op territory, not AEP).

## Operator efficiency (PUE / WUE)

Companion comparison of Google, Meta, Microsoft, AWS, xAI and the neoclouds:
**`data/operator_efficiency.csv`** (PUE, WUE, water per MW-year, low-carbon share,
disclosure grade, sources) and **`docs/operator_efficiency.md`** (analysis). Headline:
Meta is best on both axes among the big four (PUE 1.08, WUE 0.19 L/kWh); AWS uses
least water (0.12); Google has the best PUE of the largest fleet (1.09) but is
5–8× more water-intensive per kWh (1.02, derived); Microsoft sits between
(1.17 / 0.27). Energy and water trade off — evaporative cooling cuts PUE and
raises water. Nebius and Crusoe post the best water numbers on cold-climate
liquid-cooled designs; CoreWeave, Applied Digital, Lambda, Galaxy and xAI publish
no usable PUE/WUE.

## Country-level summary

| Country | Sites | MW (known) | H100e (known) |
|---|---:|---:|---:|
| USA | 121 | 69,422 | 38,316,893 |
| China | 29 | 1,926 | 853,920 |
| Malaysia | 25 | 4,481 | 2,624,634 |
| India | 25 | 7,560 | 3,002,471 |
| Mexico | 23 | 1,828 | 838,280 |
| Canada | 20 | 10,404 | 4,341,931 |
| Japan | 16 | 2,094 | 880,405 |
| South Korea | 13 | 913 | 449,789 |
| Saudi Arabia | 12 | 2,616 | 1,152,050 |
| South Africa | 11 | 887 | 374,834 |
| Brazil | 10 | 3,282 | 1,297,416 |
| Australia | 9 | 2,550 | 1,174,155 |
| UK | 9 | 990 | 519,734 |
| United Arab Emirates | 8 | 1,360 | 2,171,001 |
| Germany | 7 | 260 | 148,435 |
| France | 6 | 2,430 | 1,073,833 |
| Italy | 5 | 707 | 318,208 |
| Sweden | 5 | 820 | 335,067 |
| Poland | 5 | 43 | 33,650 |
| Israel | 4 | 196 | 89,382 |
| Finland | 3 | 985 | 428,167 |
| Denmark | 3 | 810 | 357,500 |
| Norway | 3 | 272 | 275,773 |
| Spain | 3 | 400 | 160,000 |
| Ireland | 3 | 675 | 301,250 |
| Netherlands | 3 | 350 | 151,800 |
| Turkey | 3 | 300 | 125,003 |
| Chile | 3 | 270 | 125,000 |
| Nigeria | 3 | 177 | 88,500 |
| Kazakhstan | 2 | 300 | 126,011 |
| Taiwan | 2 | 400 | 147,500 |
| Indonesia | 2 | 190 | 132,386 |
| Bangladesh | 2 | 200 | 83,333 |
| Singapore | 2 | 206 | 103,000 |
| Vietnam | 2 | 144 | 61,333 |
| Thailand | 2 | 147 | 65,167 |
| Kenya | 2 | 30 | 11,250 |
| Pakistan | 2 | 10 | 3,642 |
| Uruguay | 2 | - | - |
| Argentina | 1 | 500 | 208,333 |
| Trinidad and Tobago | 1 | 450 | 187,500 |
| Oman | 1 | 400 | 166,667 |
| Jordan | 1 | 400 | 166,667 |
| Belgium | 1 | 300 | 130,000 |
| New Zealand | 1 | 280 | 116,667 |
| Costa Rica | 1 | 200 | 83,333 |
| Paraguay | 1 | 106 | 44,167 |
| Armenia | 1 | 100 | 41,667 |
| Portugal | 1 | 1,200 | 31,500 |
| Philippines | 1 | 50 | 25,000 |
| Guatemala | 1 | 50 | 20,833 |
| Egypt | 1 | 20 | 10,000 |
| Morocco | 1 | 16 | 8,000 |
| Iceland | 1 | 5 | 5,821 |
| Slovenia | 1 | - | 5,053 |
| Uzbekistan | 1 | 12 | 5,000 |
| Romania | 1 | - | 2,527 |
| Czechia | 1 | - | 430 |
| Serbia | 1 | - | 58 |
| Greece | 1 | - | - |
| Switzerland | 1 | - | - |
| Qatar | 1 | - | - |
| Bahrain | 1 | - | - |
| El Salvador | 1 | - | - |
| Ethiopia | 1 | - | - |
| Bulgaria | 1 | - | - |
| Lithuania | 1 | - | - |
| Hungary | 1 | - | - |
| Ukraine | 1 | - | - |
| Azerbaijan | 1 | - | - |
| Peru | 1 | - | - |

MW = sum of known gross power (falls back to IT load where gross is unpublished); it
mixes announced, operating and speculative capacity, so treat it as a scale indicator,
not a current draw. H100e totals are the sum of per-site best estimates.

## Regenerating

```bash
python pipeline/build.py   # data/canonical/data_centers.csv -> data/published/*.csv|json + index.html
```
