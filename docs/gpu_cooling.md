# Accelerators, cooling and water: what the hardware does and does not tell you

Companion to `data/canonical/data_centers.csv`. Built Nov 2026 from vendor
documentation, operator engineering disclosures and the site notes in the
inventory.

**Short version:** the GPU vendor does not determine a data centre's water use.
Cooling is two separate decisions — how heat leaves the **rack**, and how the
**facility** rejects it to the sky. A rack full of liquid-cooled GPUs can sit in
a campus that evaporates billions of litres a year, and an air-cooled hall can
run on dry coolers with almost no water. Of the 442 sites, 177 name an
accelerator platform (specific model or family placeholder), but only **51** have
enough evidence (model, count, TDP) to estimate accelerator heat, and only **94**
have a water figure — every one of which is an operator-fleet scaling, not a site
measurement.

---

## 1. The claim this dataset corrects

A common shorthand says "NVIDIA uses water, TPUs do not" or "liquid cooling is
water-free". Both are wrong, and for the same reason: they conflate the rack
loop with the facility loop.

- Google's TPU v3/v4/v5p/Ironwood racks are **liquid-cooled**, but Google's own
  OCP material describes the liquid loop transferring heat to facility water and
  then to **cooling towers**. Liquid at the rack does not mean no evaporation at
  the plant.
- NVIDIA's GB200/GB300 NVL72 reference racks are direct-to-chip liquid, with
  roughly **90% of rack heat to liquid and 10% to air**. NVIDIA also documents a
  45 °C liquid design that can reject heat through **outdoor dry coolers**,
  eliminating water — but that is a facility choice the operator may not take.
- AWS says its Trainium2 and GB200 halls use **hybrid air plus direct-to-chip
  liquid**, and that its closed-loop liquid design does not increase water use.
  Project Rainier sites use outside air for months at a time. That is an
  operator claim about a design, not a metered site figure.

So the dataset records two independent fields — `rack_cooling` and
`heat_rejection` — and refuses to derive one from the other. Water is only
estimated where the operator publishes a fleet WUE, and is labelled as such.

---

## 2. Files

| File | Rows | What it is |
|---|---:|---|
| `data/gpu_platforms.csv` | 41 | Accelerator reference table: TDP, rack system, rack cooling, heat-to-liquid share, source, match rule |
| `data/gpu_cooling.csv` | 442 | One row per site: matched platform(s), heat estimate, cooling electricity, rack cooling, heat rejection, water estimate, confidence |
| `data/gpu_cooling.json` | 442 | Same, typed JSON |
| `pipeline/build_gpu_cooling.py` | — | Generator; run after `pipeline/build.py` |

Rebuild:

```powershell
python pipeline/build.py
python pipeline/build_gpu_cooling.py
```

The build validates row count, name uniqueness, and that every site carries a
confidence grade. It prints warnings where accelerator heat exceeds reported IT
load.

---

## 3. Method

For each site the build:

1. reads `gpu_types`; if blank, scans `notes` for a named accelerator (19 sites
   are identified this way, e.g. KDDI Osaka Sakai = GB200 NVL72 from the note);
2. matches those tokens against the 41-row platform table;
3. aggregates TDP only when every matched platform has one;
4. computes heat, cooling electricity and (where a WUE exists) water.

### 3.1 Formulas

| Quantity | Formula | Notes |
|---|---|---|
| Accelerator heat | `count × TDP / 1e6` MW | TDP in watts; the die/board heat, not the whole facility |
| Cooling thermal load | `≈ IT load` MW | All IT energy becomes heat; this is the load the plant must reject |
| Cooling electricity | `IT load × (PUE − 1)` MW | The non-IT share of facility power |
| Water | `IT MW × 8,760 h × 1,000 kWh/MWh × WUE` L/yr | Fleet WUE applied to site IT load |

Two consequences worth stating plainly:

- **`cooling_thermal_load_mw` is not `accelerator_heat_mw`.** The former is the
  whole IT load (CPUs, memory, networking, power conversion); the latter is only
  the accelerators. Accelerator heat is typically 50–80% of IT load at an AI
  campus, but the dataset does not assume a ratio — it reports both and lets the
  reader compare where both exist.
- **Water is an upper-bound scaling, not a measurement.** A site using an
  operator's fleet WUE inherits every other site in that fleet. It is useful for
  ranking and for order-of-magnitude, not for a permit application.

### 3.2 Mixed generations

Mixed accelerator generations get **no single TDP**. The build emits
`tdp_w_low` / `tdp_w_high` and `accelerator_heat_mw_low` / `_high`, leaves the
point columns blank, and explains the mix in `tdp_basis`. Example: Google Storey
County runs `TPU v4; v5e; v5p; v6e`, so the range is 200–450 W per chip.

### 3.3 Waterless overrides

Four sites state no operational water use, so the operator WUE is **not**
applied and water is set to 0 with `water_dependency = negligible`:

- CloudHQ Queretaro (waterless cooling)
- Meta Sturgeon (closed-loop liquid, "no operational water use")
- Elea BEL1 Belem (waterless cooling)
- Google Canelones / Project Teros (waterless cooling)

These are design claims from the cited sources. A 0 here means "no evaporative
water in the stated design", not "metered zero".

---

## 4. Coverage

| Measure | Sites | Share |
|---|---:|---:|
| Any accelerator platform (model or family) | 177 | 40% |
| — from `gpu_types` | 158 | |
| — from site notes | 19 | |
| Announced accelerator count | 74 | 17% |
| Accelerator heat estimate | 51 | 12% |
| — single TDP | 36 | |
| — TDP range | 15 | |
| IT load / thermal load | 307 | 69% |
| Cooling electricity | 307 | 69% |
| Water estimate (fleet-scaled) | 94 | 21% |

Confidence in the **hardware/heat** estimate: **A 0, B 38, C 66, D 338**. There
is no A because no site combines an officially published TDP, a published count
and a site-specific cooling disclosure. That is a finding, not a defect.

### 4.1 Rack cooling

| `rack_cooling` | Sites |
|---|---:|
| `unknown` | 303 |
| `air_or_dlc` (platform supports both) | 70 |
| `dlc` (direct-to-chip liquid) | 54 |
| `dlc_capable` (declared readiness, not confirmed) | 6 |
| `air` | 4 |
| `hybrid` (air + liquid in the same hall) | 3 |
| `immersion` | 2 |

`air_or_dlc` is deliberately not resolved to one answer. H100/H200/B200 SXM can
be air- or liquid-cooled; the platform does not tell you which the operator
installed.

### 4.2 Facility heat rejection

| `heat_rejection` | Sites |
|---|---:|
| `unknown` | 310 |
| `hybrid` | 74 |
| `evaporative` | 42 |
| `dry_closed_loop` | 16 |

Where a site note is silent, the operator's fleet profile is used and the basis
string says so. Google is mapped to evaporative, Meta/Microsoft/AWS to hybrid,
Crusoe/Nebius/Applied Digital to dry closed loop. This is a fleet-level
assumption: an individual Google campus may be dry, and a Meta campus may
evaporate.

### 4.3 Water dependency

| `water_dependency` | Sites |
|---|---:|
| `unknown` | 313 |
| `low` | 45 |
| `high` | 42 |
| `moderate` | 29 |
| `negligible` | 13 |

Thresholds on WUE (L/kWh): ≥0.5 high, ≥0.2 moderate, ≥0.05 low, below that
negligible.

---

## 5. Platform notes

The reference table covers NVIDIA (18 rows), Google TPU (7), AMD (5), AWS (4),
Huawei (4), Meta MTIA, Intel Gaudi and a generic fallback. Highlights and
caveats:

- **NVIDIA H100/H200 SXM** — 700 W, air or direct-to-chip. H100 PCIe is 350 W
  and air-only; the match rule excludes it from SXM rows.
- **NVIDIA B200** — 1000 W in HGX; the same die runs at 1200 W per GPU in
  GB200 NVL72. **B300/GB300** are ~1400 W per GPU, a secondary estimate because
  NVIDIA has not published a single-GPU number.
- **NVIDIA H800** — China-market H100 variant, 700 W, treated as a secondary
  estimate. It appears at SenseTime Lingang alongside A100s.
- **NVIDIA Vera Rubin** — announced, no production TDP. Any site mapped to it
  gets `tdp_w` blank and `confidence` capped at D for heat purposes.
- **Google TPU** — v3 300 W, v4 400 W, v5e 200 W, v5p 450 W, v6e 200 W, v7
  Ironwood 600 W, all **estimates**: Google does not publish per-chip TDP.
  Liquid: v3, v4, v5p, v7. Air: v5e, v6e. A bare "TPU" therefore cannot be
  resolved to a cooling type, which is why `google_tpu_generic` exists.
- **AWS Trainium2** — ~500 W working estimate (SemiAnalysis); other estimates
  reach 700 W. AWS does not publish. Rack cooling is hybrid air + DLC.
- **AMD MI300X** 750 W, **MI355X** 1400 W with a direct-liquid option.
- **Huawei Ascend 910B** ~400 W, **910C** ~600 W. CloudMatrix 384 is 384 chips
  in a hybrid row-air plus liquid system. Ascend 950 is announced, no TDP.

---

## 6. Worked examples

**Stargate Abilene (Crusoe/Oracle for OpenAI), B.** 450,000 GB200 at 1200 W =
**540 MW** of accelerator heat, 58.5% of a 923 MW IT load derived from gross
power ÷ design PUE 1.3. Rack cooling `dlc` (platform-implied); heat rejection
`dry_closed_loop` from Crusoe's design profile. Water 16.2 ML/yr (4.3 Mgal) at
WUE 0.002 — an upper bound on a design claim, not a meter reading.

**Meta Prometheus (New Albany), C, flagged.** 1,000,000 GB200/GB300 at
1200–1400 W implies **1200–1400 MW** of accelerator heat against a reported
**695 MW** IT load. The note explains it: hundreds of thousands of GPUs today,
scaling to ~1 million. The count is a target, the IT load is current, and the
two do not belong in the same arithmetic. The row keeps the range and carries
`consistency = accelerator heat exceeds reported IT load`.

**Google Storey County, C.** Four TPU generations in one campus produce a
200–450 W range and `rack_cooling = hybrid` (v5e/v6e air, v4/v5p liquid). No
count is published, so no heat total is emitted. Water is fleet-scaled at
1.02 L/kWh → 1.44 GL/yr (380 Mgal) on 161 MW IT.

**xAI Colossus 1, B.** 230,000 mixed H100/H200/B200 → 161–230 MW accelerator
heat. No IT load is published, so no water figure is emitted even though xAI's
estimated WUE is ~1.0. The row shows the heat range and stops.

**China Telecom Lingang, C.** 15,000 Ascend 910B at 400 W = 6 MW. Site note
confirms liquid cooling; no IT load and no heat-rejection evidence, so water is
`unknown`. This is the shape most Chinese rows take.

---

## 7. Consistency flags

Three rows carry `consistency` warnings. None is silently corrected:

| Site | Accelerator heat | Reported IT load | Likely cause |
|---|---:|---:|---|
| Meta Prometheus | 1200–1400 MW | 695 MW | count is a future target, IT load is current |
| JUPITER / JAIF | 24 MW | 16.7 MW | IT load derived from gross ÷ default PUE understates system power |
| Domyn Colosseum | 6.9 MW | 5.8 MW | same derivation issue, small site |

The warning is the deliverable. A reader who sees 1.2 GW of GPUs against 695 MW
of IT should distrust one of the two numbers, and the dataset says which.

---

## 8. What is still unknown

- **Counts.** 368 of 442 sites publish no accelerator count. Without a count
  there is no heat total, only a per-chip TDP.
- **Models.** 265 sites name no accelerator at all. Notes often say "AI-ready"
  or "GPU-capable", which is a marketing description, not hardware.
- **Rack cooling.** 303 sites have no rack-level evidence. The platform default
  is not the installation.
- **Heat rejection.** 310 sites have no facility-level evidence. Operator fleet
  profiles are a proxy, not a site record.
- **Site water.** Zero sites publish a metered IT-water figure in this dataset.
  Every water number is a WUE scaling. Municipal and utility records are the
  next step, not vendor documentation.

---

### How this reads on the dashboard

The `index.html` site-efficiency view applies the rule above literally: a campus
is plotted only when it has an **operator-disclosed** PUE and a water intensity.
The industry default of 1.20 that fills 315 rows is an assumption, so it is
excluded even though it makes the axis look better populated. That leaves 88
campuses, and they land on six distinct positions — Google 26, Meta 20,
Microsoft 19, AWS 14, Nebius 5, Crusoe 4.

That result is the point. Once PUE is a fleet figure and water is a fleet WUE,
site-level efficiency *is* operator-level efficiency, and the scatter says so
instead of pretending otherwise. The rack-cooling × heat-rejection matrix is the
one panel that stays genuinely per-site: 34 of 442 sites name both layers, 36 are
evaporative with no rack evidence, and 39 are direct-to-chip with unknown
rejection.

---

## 9. Sources

Vendor and operator engineering:

- NVIDIA, *GB200 NVL72* and *GB300 NVL72* reference architectures; H100, H200,
  B200, GH200, A100, L40S, L4 product pages
- NVIDIA, "Liquid cooling for AI factories" (45 °C facility water, dry coolers):
  `https://blogs.nvidia.com/blog/liquid-cooling-ai-factories`
- Google Cloud, "Enabling 1 MW IT racks and liquid cooling at OCP EMEA Summit"
  (TPU v3 onward; liquid loop to facility water and cooling towers)
- Google, TPU v5e / v6e / Ironwood documentation and launch posts
- AWS, "AWS liquid cooling data centers" (hybrid air + direct-to-chip;
  closed-loop water claim)
- AWS, Project Rainier (outside-air months, Trainium2)
- AMD, MI300X product page and MI355X platform brochure
- Huawei, CloudMatrix 384 paper: `https://arxiv.org/abs/2506.12708`

Fleet PUE/WUE and comparability caveats: `docs/operator_efficiency.md` and
`data/operator_efficiency.csv`.

**Do not quote a water figure from this dataset as a site measurement.** It is
an operator-fleet WUE multiplied by a site IT load, and the basis column says so
on every row.
