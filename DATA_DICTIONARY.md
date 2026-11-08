# Data dictionary

Column definitions for the five published CSVs. Units are metric unless noted.

---

## 1. `data/published/data_centers.csv` (and `.json`)

One row per site. `pipeline/build.py` generates this file from
`data/canonical/data_centers.csv`. Edit the canonical file, then rebuild.

| Column | Type | Description |
|---|---|---|
| `name` | text | Site or campus name as commonly reported |
| `operator` | text | Owner or operator. Includes anchor tenants where relevant. |
| `city` | text | Nearest city or locality |
| `state_province` | text | First-level administrative unit |
| `country` | text | Common English short name (`United Arab Emirates`, not `UAE`) |
| `latitude` | float | WGS84 decimal degrees |
| `longitude` | float | WGS84 decimal degrees |
| `power_capacity_mw` | float | Gross facility power capacity, MW (blank if unknown) |
| `it_load_mw` | float | IT load in MW. Sometimes derived as gross ÷ PUE. |
| `announced_gpu_count` | integer | Announced accelerator count, all types |
| `gpu_types` | text | Accelerator mix, e.g. `H100, GB200` |
| `cluster_peak_pflops` | float | Announced peak FP16/BF16-class throughput, PFLOPS |
| `h100e_gpu` | float | H100e from GPU count conversion |
| `h100e_third_party` | float | H100e from analyst or third-party estimates |
| `h100e_flops` | float | H100e from peak FLOPS conversion |
| `h100e_power` | float | H100e from power: 500 per MW IT (417 per MW gross at PUE 1.2) |
| `h100e_best` | float | Published estimate. Uses the strongest available method. |
| `h100e_method` | text | Which method produced `h100e_best` |
| `status` | enum | `operational` / `partially_operational` / `under_construction` / `planned` |
| `status_note` | text | Qualification, date or source for the status |
| `source_url` | text | Primary source for the row |

**H100e factors:** H100/H200/H800/GH200 = 1.0. B200/GB200 = 2.25.
GB300/B300 = 2.5. A100 = 0.315. Trainium2 = 0.34. Ascend 910B = 0.35.
L40S = 0.19. Unspecified = 1.0. Leave mixed generations blank with a note.

---

## 2. `data/us_utility_impacts.csv`

One row per **utility territory** (55 rows), not per site. Many US sites share
a utility.

| Column | Description |
|---|---|
| `region` | Human-readable territory label |
| `utility` | Serving utility, or utilities where co-op and IOU edges overlap |
| `utility_type` | Investor-owned / municipal / cooperative / federal |
| `our_sites_covered` | Sites from the main dataset in this territory |
| `energy_price_trend_2021_2026` | Residential trend. EIA state averages with docket detail. |
| `energy_rate_events` | Rate cases, riders and tariffs, with dates |
| `bill_complaint_groups` | Named, sourced groups that complain about bills |
| `water_consumption` | Documented water use. Withdrawal versus consumption, as stated. |
| `water_complaints` | Named disputes, lawsuits and disclosure fights |
| `sources` | URLs separated by semicolons |
| `verification` | `A` / `B` / `C` / `D` grade with a one-line definition |

**Grades.** A = price (EIA) and water or rate claims checked against primary
sources. B = price verified, water secondary or unpublished. C = water verified,
price unchecked. D = not re-verified.

---

## 3. `data/operator_efficiency.csv`

One row per operator (13). Fleet-level metrics from company disclosure where it
exists.

| Column | Description |
|---|---|
| `operator` | Company |
| `category` | `hyperscaler` / `AI-native` / `neocloud` |
| `metric_year` | Reporting year. It varies by company, so read the caveats. |
| `pue` | Power Usage Effectiveness as reported, or `ND` |
| `pue_scope` | Boundary of the PUE figure: fleet-wide, owned-only, design or single site |
| `wue_l_per_kwh` | Water Usage Effectiveness, litres per IT kWh, or `ND` |
| `wue_basis` | Withdrawal or consumption, and whether reported or derived |
| `water_gal_per_mw_year` | WUE × 8,760 h × 1,000 kW ÷ 3.785 L/gal (normaliser) |
| `low_carbon_or_renewable` | Renewable matching or low-carbon share as claimed |
| `disclosure_grade` | A = assured annual disclosure. B = company-reported but limited. C = secondary or guidance. D = none. |
| `notes` | Boundary, year and methodology caveats |
| `source_url` | Primary source |

**Do not compare across rows without reading `pue_scope` and `wue_basis`.**
Withdrawal-based WUE and consumption-based WUE are not the same metric. A
single-site figure is not a fleet figure.

---

## 4. `data/gpu_platforms.csv`

One row per accelerator platform or family (41 rows). `pipeline/build_gpu_cooling.py`
uses this reference data. Edit here, never in the generated per-site output.

| Column | Description |
|---|---|
| `platform_id` | Stable key, e.g. `nvidia_gb200`, `google_tpu_v5p` |
| `vendor` | NVIDIA / Google / AWS / AMD / Huawei / Meta / Intel / Various |
| `family` | Product family (Hopper, Blackwell, TPU, Trainium, Ascend…) |
| `model` | Human-readable model |
| `generation` | Generation token used for grouping |
| `architecture` | Die or architecture name where known |
| `launch_year` | First production year (blank if unlaunched) |
| `tdp_w` | Per-accelerator TDP in watts (blank if unpublished) |
| `tdp_basis` | `official`, `secondary estimate`, or `not launched` |
| `rack_system` | Reference rack (HGX H100, GB200 NVL72, TPU pod…) |
| `rack_accelerators` | Accelerators per reference rack |
| `rack_power_kw` | Reference rack power, kW |
| `rack_cooling` | `air`, `dlc`, `air_or_dlc`, `hybrid`, `immersion`, `unknown` |
| `heat_to_liquid_pct` | Share of rack heat captured by liquid, where stated |
| `coolant_supply_max_c` | Maximum design coolant supply temperature, °C |
| `cooling_notes` | What the vendor actually says, with caveats |
| `confidence` | A = official spec. B = company-reported. C = secondary estimate. D = unpublished. |
| `source_url` | Primary vendor document |
| `match_regex` | Case-insensitive regex used to match site text |
| `specific` | `1` = named model. `0` = family or vendor fallback. |

**Mixed generations.** A site that matches more than one platform with different
TDPs gets no single value. The build emits a low/high range instead.

---

## 5. `data/gpu_cooling.csv` (and `.json`)

One row per site (442). `pipeline/build_gpu_cooling.py` generates this file from
`data/published/data_centers.csv` plus `data/gpu_platforms.csv`.

| Column | Description |
|---|---|
| `name`, `operator`, `country`, `status` | Site identity, copied from the inventory |
| `gpu_types_raw` | Raw `gpu_types` string from the inventory |
| `gpu_evidence` | `gpu_types`, `notes`, or `none` — the field that identified the hardware |
| `platform_ids` | Matched `platform_id` values, separated by semicolons |
| `platform_models` | Human-readable matched models |
| `platform_count` | Number of matched platforms |
| `platform_confidence` | Weakest confidence grade among matched platforms |
| `accelerator_count` | Announced count (blank if unpublished) |
| `accelerator_count_basis` | `announced` or `unknown` |
| `tdp_w` | Single per-chip TDP, only when all matched platforms agree |
| `tdp_w_low`, `tdp_w_high` | TDP range for mixed generations |
| `tdp_basis` | Why the TDP is a point, a range, or blank |
| `accelerator_heat_mw` | `count × tdp_w / 1e6` (point estimate) |
| `accelerator_heat_mw_low`, `_high` | Heat range for mixed generations |
| `accelerator_heat_share_pct` | Accelerator heat ÷ IT load, % |
| `it_load_mw` | Site IT load, published or derived (gross ÷ PUE) |
| `it_load_basis` | `published IT load` or the derivation |
| `cooling_thermal_load_mw` | Heat the plant must reject, ≈ IT load |
| `pue_used` | PUE applied to the site |
| `pue_basis` | Operator fleet, design, or the industry default of 1.2 |
| `cooling_electric_mw` | `IT load × (PUE − 1)` |
| `rack_cooling` | `air`, `dlc`, `air_or_dlc`, `hybrid`, `immersion`, `dlc_capable`, `unknown` |
| `rack_cooling_basis` | `site note`, `platform-implied`, or `no hardware evidence` |
| `heat_rejection` | `evaporative`, `dry_closed_loop`, `hybrid`, `unknown` |
| `heat_rejection_basis` | Site note or operator fleet profile, labelled as such |
| `water_dependency` | `high` / `moderate` / `low` / `negligible` / `unknown` from WUE |
| `water_l_per_year` | `IT MW × 8,760 × 1,000 × WUE` — **fleet-scaled, not measured** |
| `water_mgal_per_year` | Same in million US gallons |
| `water_estimate_basis` | States the WUE, its year and basis, and that it is not site-measured |
| `confidence` | A–D for the hardware and heat estimate (water has its own basis) |
| `consistency` | `ok`, a heat-vs-IT-load flag, or `no accelerator heat estimate` |
| `basis` | One-line human summary of the row |
| `source_url` | Site source |
| `platform_source_url` | Vendor source for the matched platform |

**Confidence grades (hardware and heat):** A = official TDP + published count +
site-specific cooling evidence. B = specific platform + count + TDP, with cooling
that is not site-specific. C = partial (specific platform or count, but not both).
D = no usable hardware evidence. The weakest matched platform caps the grade, so
a site that rests on a secondary TDP estimate cannot score A.

**Water.** Never read `water_l_per_year` as a site measurement. It is an
operator-fleet WUE applied to a site IT load. Four sites with an explicit
waterless design carry 0 and `negligible`.

### 5a. Fields the dashboard derives (not in the CSV)

`pipeline/dashboard.py` adds these fields to the embedded JSON only. The page
uses them to separate evidence from assumption:

| Field | Description |
|---|---|
| `pue_disclosed` | `true` only when `pue_basis` is not `industry default…`. 315 of 442 rows are `false`. The site-efficiency chart refuses to plot them. |
| `h100e_best`, `h100e_per_mw` | Best H100e estimate joined from `data_centers.json`, and that estimate ÷ `it_load_mw`. Power-based estimates sit at 500 by construction. |
| `cooling_overhead_pct` | `(pue_used − 1) × 100` — the non-IT share implied by the PUE in use |
| `water_l_per_mw_year`, `water_ml_per_mw_year` | `water_l_per_year ÷ it_load_mw`, and the same in megalitres |

The ledger marks a water figure with `≈` when `water_estimate_basis` contains
"estimate". Currently that is the two xAI rows, which multiply a stated
1.0 L/kWh by site IT load rather than use a published WUE. The chart cannot show
them anyway, because xAI's PUE is the industry default.

The site-efficiency scatter groups campuses by **rounded pixel position**, not by
raw value. Operator water intensities differ in the fourth decimal (8.9345 vs
8.9394 ML/MW-yr), because each site divides its own water total by its own IT
load. Value equality would stack two bubbles on one pixel and read as a rendering
artifact.
