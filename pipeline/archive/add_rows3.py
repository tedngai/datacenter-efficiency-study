"""Append Canada + Mexico additions + Central America/Caribbean rows to data/canonical/data_centers.csv.
H100e factors: H100/H200/GH200=1.0, B200/GB200=2.25, GB300/B300=2.5, A100=0.315,
Trainium2=0.34, Ascend 910B=0.35, L40S=0.19, unspecified=1.0.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
RAW = os.path.join(ROOT, "data", "raw", "data_centers_raw.csv")

COLS = ["name","operator","city","state_province","country","latitude","longitude",
        "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
        "cluster_peak_pflops","h100e_gpu","h100e_third_party","notes","source_url"]

def row(name, operator, city, state, country, lat, lon, power=None, it=None,
        gpu=None, types=None, pflops=None, h_gpu=None, h_3p=None, notes="", url=""):
    return {
        "name": name, "operator": operator, "city": city, "state_province": state,
        "country": country, "latitude": lat, "longitude": lon,
        "power_capacity_mw": power, "it_load_mw": it, "announced_gpu_count": gpu,
        "gpu_types": types or "", "cluster_peak_pflops": pflops, "h100e_gpu": h_gpu,
        "h100e_third_party": h_3p, "notes": notes, "source_url": url,
    }

ROWS = [
# ---------------- CANADA ----------------
row("CoreWeave Cambridge AI Data Centre","CoreWeave (developer: Related Digital/Ascent; Cohere anchor tenant)","Cambridge","Ontario","Canada",43.390,-80.320,power=54,
    notes="Fully operational Aug 2025 (initial capacity Jun 2025); former BlackBerry DC converted, ~64MW project total, ~52MW pre-leased; Cohere anchor under Canada's AI Compute Challenge ($240M federal via $725M project); OVHcloud also tenant; GPU count undisclosed",url="https://www.theglobeandmail.com/business/article-coreweave-ai-data-centre-cambridge-ontario-cohere/"),
row("eStruxture CAL-3","eStruxture Data Centers","Rocky View County (Calgary area)","Alberta","Canada",51.21042,-113.91468,power=90,it=70,
    notes="Under construction, commercial operation H2 2026; C$750M flagship; 125kW+ racks, air + direct-to-chip liquid cooling; CoreWeave signed as Phase 1 anchor tenant (May 2026); largest DC under construction in Alberta",url="https://www.estruxture.com/press-releases/estruxture-announces-coreweave-as-anchor-tenant-for-cal-3-its-landmark-ai-ready-facility-in-alberta"),
row("Meta Sturgeon Data Centre","Meta","Sturgeon County (Alberta Industrial Heartland)","Alberta","Canada",53.830,-113.100,power=1000,
    notes="Announced Jul 2026, site prep underway; Meta's first Canadian DC and largest outside the US; >C$13B ($9.1B); 1GW in two phases on ~970MW firm grid + future on-site gas; closed-loop liquid cooling, no operational water use; open date not set",url="https://www.reuters.com/world/americas/meta-build-c13-billion-alberta-data-center-its-first-canada-2026-07-08/"),
row("TELUS Sovereign AI Factory Rimouski","TELUS","Rimouski","Quebec","Canada",48.230,-68.410,types="NVIDIA H200 SXM5 141GB",
    notes="Operating since Sep 2025; Canada's first fully sovereign AI factory; HPE Cray XD670; TOP500 Nov 2025 #78 (Rpeak 27.44 PF FP64); GPU count undisclosed (est ~700-800 H200); 99% hydro; sold out by May 2026",url="https://www.telus.com/en/about/news-and-events/media-releases/telus-opens-canadas-first-fully-sovereign-ai-factory"),
row("TELUS Kamloops AI Factory","TELUS (with Westbank)","Kamloops","British Columbia","Canada",50.674,-120.327,types="NVIDIA Grace Blackwell & Vera Rubin (planned)",
    notes="Under construction, online late 2026; part of TELUS/Westbank BC sovereign AI cluster - 85MW initial BC Hydro allocation across three sites, scaling to >150MW and >60,000 GPUs by 2032; heat-recovery district heating",url="https://www.telus.com/en/about/news-and-events/media-releases/TELUS-and-Government-of-Canada-advance-work-to-scale-Canadas-sovereign-AI-infrastructure"),
row("TELUS Vancouver M3 AI Factory","TELUS (with Westbank)","Vancouver (Mount Pleasant)","British Columbia","Canada",49.264,-123.099,types="NVIDIA Grace Blackwell & Vera Rubin (planned)",
    notes="Under construction; opening end 2026; one of three TELUS BC sovereign AI sites (cluster >150MW / >60,000 GPUs by 2032); per-site MW not yet split",url="https://www.telus.com/en/about/news-and-events/media-releases/TELUS-and-Government-of-Canada-advance-work-to-scale-Canadas-sovereign-AI-infrastructure"),
row("TELUS Vancouver 150 West Georgia AI Factory","TELUS (with Westbank)","Vancouver (downtown)","British Columbia","Canada",49.282,-123.116,types="NVIDIA Vera Rubin / Grace Blackwell (planned)",
    notes="Planned, online 2029; third site of TELUS BC sovereign AI cluster",url="https://www.telus.com/en/about/news-and-events/media-releases/TELUS-and-Government-of-Canada-advance-work-to-scale-Canadas-sovereign-AI-infrastructure"),
row("Bell AI Fabric Merritt (BUZZ HPC)","Bell Canada (GPU operator: BUZZ HPC, subsidiary of HIVE Digital)","Merritt","British Columbia","Canada",50.113,-120.789,power=6.5,it=5,gpu=2304,types="NVIDIA GB200 (NVL72)",h_gpu=5184,
    notes="Phase 1 live 2026 (6.5MW gross / 5MW critical IT); 2,304 GB200 GPUs going live late 2026-early 2027 under BUZZ HPC's $220M 3-yr sovereign GPU cloud contract serving Cohere; second 6.5MW phase planned",url="https://www.hivedigitaltechnologies.com/news/hives-buzz-hpc-closes-usd-220-million-sovereign-ai-gpu-contract-with-bell-ai-fabric-for-cohere-inc/"),
row("Rorqual (Calcul Quebec national DC)","Calcul Quebec / Digital Research Alliance of Canada (at ETS for McGill)","Montreal","Quebec","Canada",45.4945,-73.5627,gpu=324,types="NVIDIA H100 SXM 80GB",h_gpu=324,
    notes="Operational Jun 2025; academic sovereign supercomputer (C$38.7M) replacing Beluga; 137,000 CPU cores + 324 H100; Top500 #192; serves 20,000+ researchers",url="https://www.alliancecan.ca/en/services/compute/rorqual"),
row("TamIA (PAICE)","Mila + Calcul Quebec (at Universite Laval)","Quebec City","Quebec","Canada",46.7764,-71.2713,gpu=308,types="NVIDIA H100 (212); H200 (96)",h_gpu=308,
    notes="Operational Mar-Apr 2025; PAICE AI-dedicated cluster: 212 H100 + 96 H200; C$21.6M; one of three PAICE systems (with Killarney, Vulcan)",url="https://www.calculquebec.ca/en/nouvelle/press-release-ai-computer-cluster-dedicated-to-academic-research-in-canada/"),
row("Killarney (PAICE)","Vector Institute + SciNet (at University of Toronto)","Toronto","Ontario","Canada",43.6603,-79.3968,gpu=752,types="NVIDIA L40S (672); H100 SXM (80)",h_gpu=208,
    notes="Operational 2025; PAICE cluster: 672 L40S + 80 H100; H100e uses L40S factor 0.19",url="https://www.alliancecan.ca/en/services/compute/killarney"),
row("Vulcan (PAICE)","Amii + University of Alberta","Edmonton","Alberta","Canada",53.5232,-113.5263,gpu=820,types="NVIDIA L40S",h_gpu=156,
    notes="Operational 2025; PAICE cluster: 820 L40S (factor 0.19); priority for Amii/CIFAR AI Chair researchers",url="https://www.alliancecan.ca/en/services/compute/vulcan"),
row("Vantage Quebec City Campus (QC24)","Vantage Data Centers","Quebec City","Quebec","Canada",46.790,-71.300,it=86,
    notes="Partially operating, expanding; QC24 (+32MW IT, C$500M) operational early 2027 brings campus to 86MW critical IT; Hydro-Quebec ~100% renewable; Vantage Canada total 178MW",url="https://vantage-dc.com/news/vantage-data-centers-invests-500-million-cad-to-drive-economic-growth-sustainability-and-innovation-in-quebec/"),
row("Wonder Valley AI Data Centre Park","O'Leary Digital (O'Leary Ventures)","Greenview Industrial Gateway (near Grande Prairie)","Alberta","Canada",54.810,-118.800,power=7500,
    notes="Proposed (announced Dec 2024, permitting 2026, phased from ~2029); up to 7.5GW (raised to ~9GW on-site gas) across 4 phases, ~C$70B; Phase 1 1.4GW; NO anchor tenants confirmed - treat as speculative",url="https://www.cbc.ca/news/canada/edmonton/wonder-valley-newsletter-open-house-9.7217459"),
# ---------------- MEXICO additions ----------------
row("AWS Mexico (Central) Region","Amazon Web Services","Queretaro","Queretaro","Mexico",20.5888,-100.3899,types="Trainium/Inferentia/Graviton (custom accelerators)",
    notes="Operational Jan 2025; AWS's first Mexico region (mx-central-1), 3 AZs; $5B over 15 years; MW not disclosed (~345MW third-party tracker estimate, unverified); AI/ML-capable",url="https://aws.amazon.com/blogs/aws/now-open-aws-mexico-central-region/"),
row("Google Cloud Mexico Region","Google","Queretaro","Queretaro","Mexico",20.59,-100.39,
    notes="Operational Dec 2024; Google's 41st cloud region and first in Mexico; exact site and MW confidential",url="https://cloud.google.com/blog/products/infrastructure/google-cloud-announces-41st-cloud-region-in-mexico"),
row("Oracle Cloud Mexico Central","Oracle","Queretaro","Queretaro","Mexico",20.59,-100.39,
    notes="Operational cloud region since 2022 (first Oracle region in Mexico); no MW published",url="https://www.datacenterdynamics.com/en/news/oracle-to-develop-cloud-region-in-nuevo-leon-mexico/"),
row("Oracle Cloud Mexico Northeast","Oracle","Monterrey","Nuevo Leon","Mexico",25.67,-100.31,
    notes="Operational cloud region since Sep 2023, hosted with Telmex/Triara; no MW published",url="https://www.datacenterdynamics.com/en/news/oracle-to-develop-cloud-region-in-nuevo-leon-mexico/"),
row("Alibaba Cloud Mexico Region","Alibaba Cloud","Queretaro","Queretaro","Mexico",20.59,-100.39,
    notes="Operational Feb 2025; Alibaba's first Latin America cloud region, 1 AZ; hosting DC details not disclosed",url="https://www.datacenterdynamics.com/en/news/alibaba-cloud-launches-mexico-cloud-region/"),
row("Ascenty Queretaro Campus (QRO1-QRO3)","Ascenty","Colon","Queretaro","Mexico",20.63,-100.28,power=81,
    notes="QRO1 25MW (2022), QRO2 31MW (2022), QRO3 25MW (under construction); 81MW combined; colocation, not AI-scale",url="https://ascenty.com/en/data-centers-en/location/mexico/queretaro/"),
row("ODATA (Aligned) QR01","ODATA (Aligned Data Centers)","Queretaro (El Marques)","Queretaro","Mexico",20.60,-100.25,power=32,
    notes="Operational since 2022 (8.4MW phase 1), 32MW at full build-out; sibling of QR03",url="https://www.bnamericas.com/en/news/odata-announces-new-campuses-datacenter-expansions-in-mexico"),
row("ODATA (Aligned) QR02","ODATA (Aligned Data Centers)","Apaseo el Grande","Guanajuato","Mexico",20.46,-100.68,power=30,
    notes="Live Jul 2024; ~15MW first phase, 30MW at full build-out; delivered to hyperscale customer",url="https://www.datacenterdynamics.com/en/news/odatas-qr02-facility-goes-live-in-guanajuato-mexico/"),
row("ODATA (Aligned) QR04","ODATA (Aligned Data Centers)","San Miguel de Allende","Guanajuato","Mexico",20.85,-100.80,power=24,it=12,
    notes="Opened Aug 2025; 24MW design, first 12MW phase operational; Aligned Delta3 cooling up to 50kW/rack, liquid-cooling-ready for AI/ML/HPC",url="https://www.odatadc.com/en/press/Odata-expands-digital-infrastructure-with-fourth-hyperscale-data-center-in-Mexico./"),
row("ODATA (Aligned) MEX01 (Mexico City)","ODATA (Aligned Data Centers)","Mexico City (Tlalnepantla)","State of Mexico","Mexico",19.54,-99.21,power=30,
    notes="Operational ~30MW hyperscale facility in Mexico City metro",url="https://mlq.ai/data-centers/mexico/"),
row("Layer 9 GTO-01 (Project Falcon)","Layer 9 Data Centers","Apaseo el Grande","Guanajuato","Mexico",20.44,-100.64,power=96,
    notes="Hyperscale shell campus; groundbreaking Oct 2022, planned 3-4 buildings of 32MW; construction delayed; shells built but not yet leased",url="https://layer9dc.com/layer-9-data-centers-breaks-ground-on-96mw-campus-in-guanajuato-mexico"),
row("Bleeding Edge QRO1 (AI Factory)","Bleeding Edge","El Marques","Queretaro","Mexico",20.561,-100.317,it=3,types="NVIDIA Blackwell B300",
    notes="Operational Jun-Jul 2026; claims first NVIDIA Blackwell-based AI Factory/neocloud in Mexico & LatAm; ~3MW critical IT, direct-to-chip liquid cooling; GPU count not published; initial capacity fully contracted",url="https://www.datacenterdynamics.com/en/news/bleeding-edge-launches-ai-factory-claims-to-be-first-nvidia-blackwell-based-neocloud-in-mexico-and-latin-america/"),
row("Digital Realty Queretaro Campus (MEX01-MEX03)","Digital Realty","Colon & Santiago de Queretaro","Queretaro","Mexico",20.59,-100.39,power=81,
    notes="Three colocation buildings: MEX01 25MW, MEX02 31MW, MEX03 25MW (utility power); operational",url="https://datacentersintel.com/market/queretaro/"),
row("Scala Tepotzotlan Campus","Scala Data Centers","Tepotzotlan","State of Mexico","Mexico",19.79,-99.22,power=7.9,it=5.1,
    notes="SMEXTP01 operational (~$80M, 7.9MW design / 5.1MW IT live); SMEXTP02 2MW under construction",url="https://scaladatacenters.com/en/scala-data-centers-invests-us-80-million-in-the-first-hyperscale-data-center-in-tepotzotlan-mexico"),
row("KIO Queretaro Campus (QRO1/QRO2 + new DC)","KIO Networks","El Marques","Queretaro","Mexico",20.56,-100.30,power=19,
    notes="~19MW installed in Queretaro state after opening an additional DC Oct 2025; Tier IV KIO/Q5 also in Santiago de Queretaro; distinct from KIO QRO3",url="https://datacentersintel.com/market/queretaro/"),
row("KIO Monterrey Campus (MTY)","KIO Networks","Monterrey (Apodaca)","Nuevo Leon","Mexico",25.67,-100.31,power=24,
    notes="Operational ~24MW; largest KIO site outside Queretaro/CDMX; no AI-scale GPU cluster announced",url="https://mlq.ai/data-centers/mexico/"),
row("Huawei Cloud Mexico-1","Huawei Cloud","Mexico City","State of Mexico","Mexico",19.43,-99.13,
    notes="Operational Huawei Cloud region in Mexico City area; no MW published",url="https://mlq.ai/data-centers/mexico/"),
# ---------------- CENTRAL AMERICA & CARIBBEAN ----------------
row("Latam Data Centers Next AI (Aurum AI Data Center)","Aurum Equity Partners + Bold Capital Group","Guatemala City","Guatemala","Guatemala",14.63,-90.51,power=50,
    notes="Announced Jun 2025: $300M AI-ready data center, 50MW initial capacity, expandable; target operations mid-2026; details scarce - treat as planned",url="https://www.bnamericas.com/en/news/guatemala-attracts-ai-data-centers-as-digital-hub-ambitions-grow"),
row("Quantum AI Free Zone Campus (Quantum FZ)","Quantum FZ","Limon","Limon","Costa Rica",9.99,-83.03,power=200,
    notes="Proposed/early-stage: up to 200MW across 7 AI DC buildings on 42ha free-zone site, Phase 1 50MW; website/land-platform stage - no construction, tenants, or financing confirmed",url="https://quantumfz.com/"),
row("El Salvador National AI Lab (Sovereign AI)","Hydra Host (for Gobierno de El Salvador)","San Salvador","San Salvador","El Salvador",13.69,-89.22,types="NVIDIA B300",
    notes="Operating; world's first sovereign purchase of NVIDIA B300 chips (Jun 2025), housed at National AI Lab; GPU count and MW not published; small-scale sovereign AI",url="https://www.datacenterdynamics.com/en/news/el-salvador-becomes-first-country-to-receive-sovereign-quota-of-nvidia-b300-chips/"),
row("Trinidad & Tobago AI Data Centers (EY 300MW / Hummingbird 150MW MoUs)","Ernst & Young & Hummingbird AI Holdings (MoUs with Government)","Port of Spain area (site TBD)","Trinidad and Tobago","Trinidad and Tobago",10.65,-61.51,power=450,
    notes="2026: Government MoUs for two Tier 4 DCs - 300MW (EY) and 150MW (Hummingbird AI); MoU stage only, no designs or clearance; treat as speculative",url="https://www.guardian.co.tt/news/budget-reveals-15m-data-centre-spend-6.2.2694774.08c3b090fa"),
]

# ---- validate + append ----
existing = list(csv.DictReader(open(CANON, encoding="utf-8")))
names = {r["name"] for r in existing}
added = 0
for r in ROWS:
    if r["name"] in names:
        print(f"SKIP duplicate: {r['name']}")
        continue
    for k, v in r.items():
        if k in {"latitude","longitude","power_capacity_mw","it_load_mw","announced_gpu_count",
                 "cluster_peak_pflops","h100e_gpu","h100e_third_party"} and v is not None:
            r[k] = str(v)
        elif v is None:
            r[k] = ""
    names.add(r["name"])
    existing.append(r)
    added += 1

with open(CANON, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(existing)

by_country = {}
for r in ROWS:
    by_country[r["country"]] = by_country.get(r["country"], 0) + 1
print(f"Added {added} rows. By country: {by_country}")
print(f"Total rows now: {len(existing)}")
