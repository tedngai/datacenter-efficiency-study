"""Append Europe / Middle East / Latin America deep-dive rows to data/canonical/data_centers.csv.
Same conventions as add_rows.py. H100e factors: H100/H200/GH200=1.0, B200/GB200=2.25,
GB300/B300=2.5, A100=0.315, Trainium2=0.34, Ascend 910B=0.35, unspecified=1.0.
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

E = "https://epoch.ai/data/ai-data-centers"

ROWS = [
# ---------------- EUROPE ----------------
row("Google Waltham Cross (UK AI compute)","Google","Cheshunt","Hertfordshire","UK",51.700,-0.035,it=88,types="TPU v6e",h_3p=123800,
    notes="Operational (2025-2026); Google's ~1bn GBP UK AI compute site; Epoch AI: 88 MW IT / ~123.8k H100e, TPU v6e; DeepMind speculative user",url=E),
row("CoreWeave Crawley (Digital Realty LGW15/16)","CoreWeave","Crawley","England","UK",51.116,-0.165,power=24,types="NVIDIA H200",
    notes="Operational Oct 2024; Europe's first large NVIDIA H200 AI deployment; part of CoreWeave's 2.5bn GBP UK investment",url="https://investors.coreweave.com/news/news-details/2025/CoreWeave-Announces-Two-Initial-Data-Centers-Hosting-NVIDIA-Hopper-GPUs-Now-Operational-in-the-United-Kingdom-Accelerating-AI-Infrastructure/default.aspx"),
row("CoreWeave London Docklands (Global Switch)","CoreWeave","London","England","UK",51.508,0.014,types="NVIDIA H100; H200",
    notes="Operational Dec 2024; at Global Switch Docklands campus (224 MVA secured power); major H100/H200 deployment",url="https://investors.coreweave.com/news/news-details/2025/CoreWeave-Announces-Two-Initial-Data-Centers-Hosting-NVIDIA-Hopper-GPUs-Now-Operational-in-the-United-Kingdom-Accelerating-AI-Infrastructure/default.aspx"),
row("CoreWeave Scotland (DataVita Fortis)","CoreWeave / DataVita","Newhouse","North Lanarkshire","UK",55.827,-3.912,power=40,types="NVIDIA GB300",
    notes="Fortis DV1 operational (24MW running, ~40MW design); CoreWeave GB300 deployment Sep 2025; North Lanarkshire AI Growth Zone targets 500MW+",url="https://www.datacenterdynamics.com/en/news/coreweave-plans-15bn-uk-ai-data-center-investment-will-deploy-nvidia-gpus-at-scotlands-datavita-data-center/"),
row("Vantage CWL1 Newport (South Wales AI Growth Zone)","Vantage Data Centers","Newport","Wales","UK",51.544,-2.946,power=148,
    notes="Operating since 2010 (ex-Next Generation Data); 148MW campus; Nebius signed Aug 2026 for first high-density AI capacity; Microsoft major customer; >1GW AI-ready planned across South Wales",url="https://vantage-dc.com/news/vantage-data-centers-and-nebius-expand-uk-ai-infrastructure-with-first-deployment-in-south-wales-ai-growth-zone/"),
row("Vantage Bridgend Campus","Vantage Data Centers","Bridgend","Wales","UK",51.520,-3.580,power=600,
    notes="Planned; former Ford engine plant bought 2024; 10 buildings over 10-15 years; ~600MW (estimate); anchor of 10bn GBP South Wales AI Growth Zone",url="https://www.datacenterdynamics.com/en/news/uk-announces-fourth-ai-growth-zone-in-south-wales/"),
row("Microsoft Acton (UK South expansion)","Microsoft","London (Acton)","England","UK",51.517,-0.274,
    notes="Under construction, nearing completion May 2026; part of Microsoft $30bn 2025-2028 UK investment; its planned 23,040 GB300 Loughton supercomputer was cancelled Oct 2026 over grid delays",url="https://ukstories.microsoft.com/features/building-the-foundations-of-the-uks-intelligence-economy/"),
row("JUPITER / JAIF (Exascale AI Factory)","Forschungszentrum Julich (EuroHPC)","Julich","North Rhine-Westphalia","Germany",50.906,6.405,power=20,gpu=24000,types="NVIDIA GH200",h_gpu=24000,
    notes="Operational (inaugurated Sep 2025); Europe's first exascale supercomputer: ~24,000 GH200; ~40 EF FP8-class AI; core of JAIF AI Factory; German gigafactory bids would build on it",url="https://www.fz-juelich.de/en/jupiter"),
row("HammerHAI (HLRS AI Factory)","EuroHPC JU / HLRS","Stuttgart","Baden-Wurttemberg","Germany",48.782,9.178,gpu=860,types="NVIDIA B200 (GB200 NVL4)",h_gpu=1935,
    notes="In service H2 2026; 215x GB200 NVL4 nodes = 860 B200; >15 EF peak AI inference; first standalone EuroHPC AI-factory supercomputer",url="https://www.hammerhai.eu/system/"),
row("Blue Swan Bavaria AI Gigafactory (candidate)","Blue Swan consortium (Bayern KI)","Schweinfurt","Bavaria","Germany",50.047,10.229,
    notes="EU AI Gigafactory candidate (bids due Nov 2026, selection 2027); Bavarian state-backed; competing German bids include Telekom/Schwarz/IONOS (50k-100k GPUs proposed) and Silicon Saxony",url="https://beckmann.ai/en/ai-economy/2026-07/eu-tender-seven-ai-gigafactories"),
row("Alice Recoque (AI2F / TGCC)","CEA (EuroHPC)","Bruyeres-le-Chatel","Ile-de-France","France",48.609,2.158,types="AMD Instinct MI430X",
    notes="Deployment expected 2026-2027; 2nd EuroHPC exascale supercomputer, AI-ready; cornerstone of AI Factory France (AI2F); GPU count and power not published",url="https://www-hpc.cea.fr/en/AliceRecoque.html"),
row("EcoDataCenter 2 (Kvarnsveden)","EcoDataCenter","Borlange","Dalarna","Sweden",60.490,15.520,power=250,types="NVIDIA Vera Rubin",
    notes="Under construction (ground broken Sep 2025); 250MW at launch, up to 600MW potential; Mistral AI 1.2bn EUR partnership deploying Vera Rubin from 2027; sister Falun site hosts DeepL GB200 SuperPod",url="https://ecodatacenter.tech/press/mistral-ai-and-ecodatacenter-partner-to-build-ai-focused-data-center-in-sweden-3431886"),
row("CoreWeave Norway (Ovrebo)","CoreWeave","Ovrebo","Agder","Norway",58.766,7.965,it=42,types="NVIDIA B200",h_3p=50773,
    notes="Operational (2025-2026); Epoch AI: 42 MW IT / ~50.8k H100e, B200; hydro-powered; OpenAI speculative user; distinct from Stargate Norway at Kvandal",url=E),
row("Microsoft Narvik (Norway AI expansion)","Microsoft","Narvik","Nordland","Norway",68.438,17.427,types="NVIDIA Vera Rubin",
    notes="Planned; Epoch lists as likely Microsoft with Rubin GPUs; ~30,000 Rubin GPUs contracted in Norway (Apr 2026) as part of Nscale-Microsoft projects - site-level split unpublished",url=E),
row("Nscale Keflavik","Nscale","Reykjanesbaer (Keflavik)","Southern Peninsula","Iceland",63.985,-22.605,it=5.11,types="NVIDIA B300",h_3p=5821,
    notes="Operational (2025-2026); Epoch AI: 5.1 MW IT / ~5.8k H100e, B300; geothermal/hydro powered",url=E),
row("MIMER (Sweden AI Factory)","EuroHPC JU / Linkoping University","Linkoping","Ostergotland","Sweden",58.397,15.576,gpu=400,types="NVIDIA GB200 (NVL4)",h_gpu=900,
    notes="In delivery, operational 2026; 100 GB200 NVL4 systems; Sweden's EuroHPC AI Factory",url="https://www.eurohpc-ju.europa.eu/ai-factories_en"),
row("NLAIF (Dutch AI Factory)","AIFNL Foundation (SURF-led)","Groningen","Groningen","Netherlands",53.219,6.567,gpu=1800,h_gpu=1800,
    notes="Under procurement (selected Oct 2025); Dutch AI-optimised supercomputer with ~1,800 high-end GPUs; GPU model and power unpublished",url="https://aic4nl.nl/en/nieuws/update-nederlandse-ai-fabriek-vraag-nu-al-europese-rekentijd-aan/"),
row("Start Campus SINES Data Campus","Start Campus","Sines","Setubal","Portugal",37.900,-8.760,power=1200,it=33,gpu=12600,types="NVIDIA GB300; Vera Rubin",h_gpu=31500,h_3p=31834,
    notes="SIN01 (26MW) launched Jan 2025; Nscale deploying 12,600+ GB300 for Microsoft; May 2026 expansion adds 66,000+ Vera Rubin GPUs from 2027 plus 200MW SIN02; fully permitted for 1.2GW; Epoch AI: 33MW IT / ~31.8k H100e; Microsoft $10bn plan reported",url="https://www.nscale.tech/press-releases/nscale-start-campus"),
row("BSC AI Factory Barcelona (MareNostrum)","Barcelona Supercomputing Center (EuroHPC)","Barcelona","Catalonia","Spain",41.389,2.116,
    notes="AI Factory operational, expanding 2026; Spain's gigafactory bid led by Telefonica/BSC targets Barcelona; GPU count unpublished",url="https://digital-strategy.ec.europa.eu/en/policies/ai-factories"),
row("Fastweb NeXXt AI Factory","Fastweb+Vodafone","Ponte San Pietro (Bergamo)","Lombardy","Italy",45.695,9.565,gpu=248,types="NVIDIA H100",h_gpu=248,
    notes="Operational since Jul 2024; 31 DGX H100 nodes hosted in Aruba's Ponte San Pietro DC; ~1 EF FP8 estimated; B300 expansion announced Oct 2026; trains MIIA Italian LLM",url="https://www.datacenterdynamics.com/en/news/fastweb-launches-nvidia-dgx-superpod-supercomputer-in-italy/"),
row("Domyn Colosseum (iGenius AI Factory)","Domyn (iGenius)","Southern Italy (undisclosed)","Southern Italy","Italy",40.300,17.000,power=7,gpu=5760,types="NVIDIA GB200 (NVL72)",h_gpu=12960,
    notes="Deployed 2025-2026; 80x GB200 NVL72; 115 EF FP4/FP8; exact location undisclosed for security; Vertiv modular build, ~$1bn backed by Italian government",url="https://thenextweb.com/news/domyn-raises-1bn-debt-colosseum-italy"),
row("Leonardo / IT4LIA AI Factory (CINECA)","CINECA (EuroHPC)","Bologna","Emilia-Romagna","Italy",44.528,11.384,gpu=14000,types="NVIDIA A100; GB200 (LISA partition)",
    notes="Operational; Leonardo pre-exascale (~14,000 GPUs incl. LISA AI partition); IT4LIA AI Factory selected 2025; mixed GPU generations so no single H100e factor applied",url="https://www.tomshw.it/business/nexxt-ai-factory-il-supercomputer-italiano-guadagna-nuovo-hardware-nvidia"),
row("Gaia AI Factory","ACC Cyfronet AGH (EuroHPC)","Krakow","Lesser Poland","Poland",50.023,19.915,gpu=1000,h_gpu=1000,
    notes="Under deployment (selected 2025-2026); ~70M EUR; over 1,000 GPU accelerators; ~10 EF reported (precision unclear)",url="https://www.cyfronet.pl/en/news/2025/w-ack-cyfronet-agh-powstanie-gaia-ai-factory"),
row("PIAST AI Factory","PSNC (EuroHPC)","Poznan","Greater Poland","Poland",52.402,16.928,gpu=450,h_gpu=450,
    notes="Under deployment (selected Mar 2025); ~450 GPUs initially, expansion to 1,500+ planned",url="https://www.psnc.pl/piast-ai/"),
row("Pharos / DAEDALUS AI Factory","GRNET (EuroHPC)","Athens","Attica","Greece",37.980,23.780,
    notes="Operational 2026; DAEDALUS supercomputer integrated with Pharos, Greece's AI Factory (first-wave selection Dec 2024); GPU count unpublished",url="https://www.hpcwire.com/off-the-wire/eurohpc-ju-signs-procurement-contract-for-daedalus-supercomputer/"),
row("Swiss AI Platform","Swisscom","Zurich","Zurich","Switzerland",47.377,8.535,types="NVIDIA DGX SuperPOD (H100-class)",
    notes="Operational since late 2024; Switzerland's first NVIDIA DGX SuperPOD; sovereign GPU-as-a-service; GPU count unpublished",url="https://www.swisscom.ch/en/about/news/2024/11/28-ai-platform.html"),
# ---------------- MIDDLE EAST ----------------
row("Khazna QAJ1 Ajman AI Data Center","Khazna Data Centers (G42)","Ajman","Ajman","United Arab Emirates",25.4052,55.5136,power=100,
    notes="Under construction; region's first AI-optimized hyperscale DC; ~100,000 sqm, 20x5MW data halls; liquid cooling; first phase due Dec 2026",url="https://khaznadatacenters.com/press-release/khazna-expands-infrastructure-to-accelerate-uaes-leadership-in-artificial-intelligence/"),
row("Khazna AUH8 Masdar City","Khazna Data Centers (G42)","Masdar City","Abu Dhabi","United Arab Emirates",24.4267,54.6150,power=30,
    notes="Under construction; cloud/AI-capable modular DC due Aug 2026; 60MW combined with AUH4",url="https://khaznadatacenters.com/press-release/khazna-expands-infrastructure-to-accelerate-uaes-leadership-in-artificial-intelligence/"),
row("Khazna AUH4 Mafraq","Khazna Data Centers (G42)","Mafraq","Abu Dhabi","United Arab Emirates",24.78,54.83,power=30,
    notes="Under construction; cloud/AI-capable modular DC due Dec 2026; 60MW combined with AUH8",url="https://khaznadatacenters.com/press-release/khazna-expands-infrastructure-to-accelerate-uaes-leadership-in-artificial-intelligence/"),
row("Microsoft-G42 200MW UAE Expansion (via Khazna)","Khazna Data Centers (G42) for Microsoft Azure","(site not disclosed)","United Arab Emirates","United Arab Emirates",24.0,54.0,
    notes="Announced Nov 2025 as part of Microsoft's $15.2B UAE commitment; 200MW expansion through Khazna for Azure sovereign cloud with advanced GPUs; online before end-2026; site(s) not disclosed (UAE centroid coords)",url="https://www.wam.ae/en/article/bmkc5tz-microsoft-g42-accelerate-uaes-digital-future-with"),
row("Moro Hub Green Data Centre (MBR Solar Park)","Moro Hub (Digital DEWA)","Dubai","Dubai","United Arab Emirates",24.95,55.32,power=100,
    notes="Operating since Feb 2023; world's largest solar-powered data centre (Guinness-certified); >100MW across phases; hosts AI/IoT workloads",url="https://www.dewa.gov.ae/en/about-us/media-publications/latest-news/2023/02/hamdan-bin-mohammed-inaugurates"),
row("Moro Hub Warsan Green Data Centre","Moro Hub (Digital DEWA)","Warsan","Dubai","United Arab Emirates",25.21,55.39,power=100,
    notes="Under construction; fourth Moro Hub green DC; >100MW planned; power density provisioned for AI/LLM workloads; phase 1 due H2 2026",url="https://www.dewa.gov.ae/en/about-us/media-publications/latest-news/2026/1/he-saeed-mohammed-al-tayer-reviews-construction-progress"),
row("Core42 Abu Dhabi Sovereign AI Cluster (DGX SuperPOD)","Core42 (G42)","Abu Dhabi","Abu Dhabi","United Arab Emirates",24.45,54.38,types="NVIDIA DGX H100 (SuperPOD)",
    notes="Operating; TOP500-listed NVIDIA DGX H100 SuperPOD (Rpeak 87.27 PFLOPS, Nov 2024); MW and GPU count not published",url="https://www.top500.org/site/51056/"),
row("HUMAIN-AWS AI Zone Riyadh","HUMAIN (PIF) + AWS","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,gpu=150000,types="NVIDIA GB300; AWS Trainium (mixed)",
    notes="Planned/under development; announced Nov 2025; up to 150,000 AI accelerators (mixed GB300 + Trainium, split unpublished so no single H100e factor applied); part of >$5B AWS-HUMAIN investment",url="https://press.aboutamazon.com/2025/11/aws-and-humain-expand-partnership-with-nvidia-ai-infrastructure-and-aws-ai-chip-deal-to-drive-global-ai-innovation"),
row("HUMAIN-xAI Compute Campus Riyadh","HUMAIN (PIF) with xAI","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,power=500,types="NVIDIA Blackwell (GB300)",
    notes="Planned/under construction; 500MW+ dedicated xAI facility (first non-US xAI site), announced Nov 2025, 2026 delivery target",url="https://www.saudicompute.com/topics/humain-xai-jv/"),
row("SDAIA Sovereign AI Factory","SDAIA (with NVIDIA)","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,gpu=5000,types="NVIDIA Blackwell",h_gpu=11250,
    notes="Deploying; announced May 2025: up to 5,000 NVIDIA Blackwell GPUs for sovereign AI factory (ALLAM LLM, smart-city AI)",url="https://nvidianews.nvidia.com/news/saudi-arabia-and-nvidia-to-build-ai-factories-to-power-next-wave-of-intelligence-for-the-age-of-reasoning"),
row("SDAIA Hexagon Data Center","SDAIA","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,power=480,
    notes="Under construction; foundation stone Jan 2026; world's largest government data centre (Tier IV design); GPU counts not published",url="https://www.spa.gov.sa/en/N2480268"),
row("Shaheen III Supercomputer (KAUST)","KAUST (HPE Cray)","Thuwal","Makkah Province","Saudi Arabia",22.31,39.10,gpu=2800,types="NVIDIA GH200",h_gpu=2800,
    notes="Operating; GPU partition accepted Oct 2025; Middle East's fastest supercomputer (TOP500 #18, Nov 2025): 122.8 PFLOPS HPL (FP64, kept out of FP8 column); 2,800 GH200 + CPU partition",url="https://www.kaust.edu.sa/en/news/top-ranked-arab-university-unveils-middle-east-s-most-powerful-supercomputer"),
row("DataVolt Riyadh AI Data Center (MODON)","DataVolt","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,
    notes="Planned; MODON land-lease (Feb 2025) for AI-ready DC on 55,000 sqm; part of DataVolt $5B Saudi investment; capacity not disclosed",url="https://data-volt.com/wp-content/uploads/2025/03/DataVolt-x-MODON-Press-Release.pdf"),
row("Alibaba Cloud Riyadh Region (SCCC)","SCCC (Alibaba Cloud JV with stc)","Riyadh","Riyadh Province","Saudi Arabia",24.71,46.68,types="NVIDIA L20; H20",
    notes="Operating since 2022; partner region me-central-1 with two Riyadh AZs; stc confirms NVIDIA L20/H20 GPU clusters with Qwen LLMs; MW not published",url="https://www.stc.com.sa/en/business/digital-portfolio/cloud/sccc.html"),
row("Ooredoo Sovereign AI Cloud Qatar","Ooredoo (infrastructure by Syntys)","Doha","Doha","Qatar",25.29,51.53,types="NVIDIA Hopper (H100/H200)",
    notes="Operating (launched Jul 2025); NVIDIA Cloud Partner; sovereign AI bare-metal; GPU count/MW not published",url="https://www.ooredoo.qa/web/en/press-release/ooredoo-deploys-nvidia-accelerated-computing-in-qatar-ushers-in-the-countrys-next-wave-of-innovation"),
row("Nebius AI Cloud Modi'in (Mega Or)","Nebius (leased from Mega Or)","Modi'in","Central District","Israel",31.89,35.01,power=8,gpu=4000,types="NVIDIA HGX B200",h_gpu=9000,
    notes="Operating (Oct 2025); one of Israel's first NVIDIA Blackwell deployments; 4,000 B200 at 8MW; 25% offered to Israel Innovation Authority national supercomputer",url="https://nebius.com/newsroom/nebius-brings-nvidia-blackwell-to-israel-with-one-of-the-country-s-first-ai-infrastructure-deployments"),
row("Nebius-Mega Or AI Data Center Beit Shemesh","Nebius (leased from Mega Or)","Beit Shemesh","Jerusalem District","Israel",31.74,34.99,power=80,
    notes="Under construction; 80MW lease signed Jan 2026 (delivery from Q3 2026); expandable to 222MW",url="https://www.datacenterdynamics.com/en/news/nebius-signs-80mw-data-center-lease-with-mega-or-in-israel/"),
row("NVIDIA Israel-1 AI Supercomputer","NVIDIA (built with Dell Technologies)","(Central District)","Central District","Israel",32.0,34.9,gpu=2048,types="NVIDIA H100 (Dell XE9680)",h_gpu=2048,
    notes="Operating; phase 1 available Nov 2023 for NVIDIA R&D and partners; 256 XE9680 servers, 2,048 H100s; exact facility and MW undisclosed (approximate coords)",url="https://aidatacenterindex.com/datacenters/nvidia-israel-1-ai-supercomputer-israel.html"),
row("AWS Middle East (Bahrain) Region","Amazon Web Services","Manama","Capital Governorate","Bahrain",26.07,50.55,
    notes="Operating since 2019 (me-south-1); first AWS region in the Middle East; hosts regional AI/ML workloads; MW not published",url="https://aws.amazon.com/about-aws/global-infrastructure/regions_az/"),
# ---------------- LATIN AMERICA ----------------
row("Scala AI City","Scala Data Centers (DigitalBridge)","Eldorado do Sul","Rio Grande do Sul","Brazil",-30.085,-51.595,it=54,
    notes="Planned/announced Sep 2024; Phase 1 54MW IT, $500M, racks >150kW for AI/ML; Brazil approved 5GW grid connection (largest in country); construction expected 2026; no GPU counts published",url="https://scaladatacenters.com/en/with-an-initial-investment-of-usd-500-million-scala-data-centers-and-rio-grande-do-sul-government-sign-agreement-for-largest-digital-infrastructure-project-in-the-state-of-southern-brazil/"),
row("Scala Tambore Campus","Scala Data Centers (DigitalBridge)","Barueri","Sao Paulo","Brazil",-23.55,-46.63,power=450,
    notes="Operating hyperscale campus, largest in Latin America at full build (17 buildings, 450MW IT); 560MW on-site substation; marketed for AI/ML with 24-100kW racks and liquid cooling; no GPU counts published",url="https://www.datacenterdynamics.com/en/product-news/scala-data-centers-breaks-ground-on-560mw-power-substation-in-sao-paulo"),
row("Ascenty Vinhedo AI Campus","Ascenty (Digital Realty/Brookfield)","Vinhedo","Sao Paulo","Brazil",-23.04,-46.99,power=170,
    notes="Operating campus; May 2026 $1.2B AI expansion: Vinhedo 2 expanded to 80MW + new 90MW Vinhedo 3 fully dedicated to AI (direct-to-chip liquid cooling), delivery 2026-2027; ~170MW total (estimate)",url="https://ascenty.com/en/blog/news-ascenty-en/ascenty-ai-contracts"),
row("TikTok/ByteDance Pecem Data Center","Omnia (Patria) + Casa dos Ventos; tenant ByteDance","Caucaia (Pecem)","Ceara","Brazil",-3.53,-38.83,power=300,it=200,
    notes="Under construction (works began Jan 2026); Phase 1 200MW IT (~300MW draw); five DCs announced, total ~$40bn by 2035, 100% wind-powered; TikTok says services for external markets, not AI training; first hall due Sep 2027",url="https://g1.globo.com/ce/ceara/noticia/2026/01/16/obras-do-mega-data-center-do-tiktok-comecam-no-ceara.ghtml"),
row("Elea Rio AI City","Elea Data Centers (I Squared Capital)","Rio de Janeiro (Barra da Tijuca)","Rio de Janeiro","Brazil",-23.00,-43.40,power=1500,
    notes="Announced May 2025; AI-focused DC district; 1.5GW certified renewable energy capacity (not IT load), potential 3.2GW by 2032; 225MW grid connection by Jan 2029; Oracle MoU (Aug 2025)",url="https://megawhat.uol.com.br/economia-e-politica/elea-recebe-parecer-para-conectar-data-center-no-rio-de-janeiro/"),
row("Tecto DC QR03 (former ODATA)","Tecto (Aligned Data Centers)","El Marques","Queretaro","Mexico",20.75,-100.18,it=300,
    notes="Largest DC campus in Mexico; first 72MW building live May 2025; 200MW energized Feb 2025; five buildings, 300MW IT at full build ($3.3B); Aligned DeltaFlow liquid cooling being installed for AI/ML; no GPU counts published",url="https://odatadc.com/en/press/Odata-announces-the-energization-of-the-largest-data-center-campus-in-Mexico--solving-the-energy-shortage-for-data-center-development-in-Quer%C3%A9taro."),
row("CloudHQ Queretaro Campus","CloudHQ","Queretaro","Queretaro","Mexico",20.62,-100.19,power=1000,it=900,
    notes="Confirmed Sep 2025 with ~$6B; six buildings, up to 900MW critical IT on 52 hectares, waterless cooling; designed for cloud + AI training; ready-for-service ~2027",url="https://mexiconewsdaily.com/business/cloudhq-4b-queretaro-data-centers"),
row("KIO QRO3","KIO Networks (I Squared Capital)","El Marques","Queretaro","Mexico",20.76,-100.11,it=100,
    notes="Announced Aug 2026: $1.3B to 2030, ~100MW planned (KIO's largest); a 12MW building operational early 2026; targeting cloud and AI demand",url="https://www.bnamericas.com/en/news/mexicos-kio-eyes-us13bn-in-data-center-investment-by-2030"),
row("Microsoft Mexico Central (Queretaro region)","Microsoft","Queretaro (Colon)","Queretaro","Mexico",20.73,-100.43,
    notes="Azure Mexico Central live May 2024 (first hyperscale region in Spanish-speaking LatAm); $1.3B cloud+AI investment over 3 years; capacity undisclosed, no specific AI-scale campus published",url="https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/10/08/how-mexico-is-pioneering-ai-innovation-for-a-global-future/"),
row("Coatlicue Supercomputer","Government of Mexico (ATDT/Secihti; UNAM/IPN/Cinvestav)","(site TBD)","Mexico","Mexico",19.43,-99.13,gpu=14480,h_gpu=14480,
    notes="Announced Nov 2025: Latin America's most powerful public supercomputer, 14,480 GPUs, 314 PF stated peak (precision unpublished, kept out of FP8 column), ~$326M, ~20MW; construction H2 2026, completion ~2028 (Mexico centroid coords)",url="https://es.wired.com/articulos/coatlicue-asi-es-la-supercomputadora-que-convertira-a-mexico-en-lider-de-procesamiento-de-datos-en-latam"),
row("Google Quilicura Data Center","Google","Quilicura (Santiago)","Santiago Metropolitan","Chile",-33.36,-70.74,
    notes="Operating since 2015 (Google's first LatAm DC), ~$290M; anchors Santiago cloud region; NOT confirmed AI-scale/GPU-dense; second Chilean DC (Cerrillos) revived 2026 after environmental court stall",url="https://datacenters.google/locations/quilicura-chile"),
row("Google Canelones Data Center (Project Teros)","Google","Canelones (Parque de las Ciencias)","Canelones","Uruguay",-34.81,-56.03,
    notes="Announced Aug 2024 with >$850M; under construction; redesigned to single building ~1/3 original capacity with waterless cooling; Google says it supports regional AI demand; no GPU-dense specs published",url="https://www.datacenterdynamics.com/en/news/google-breaks-ground-on-uruguay-data-center"),
row("Antel AI Data Center","Antel (state telecom)","Canelones (Pando)","Canelones","Uruguay",-34.75,-55.95,
    notes="Announced Aug 2026 by Uruguay's Presidency: $70M AI-specialised DC, construction from Q1 2027, operation 2028-2029; power/GPU counts not published",url="https://econosur.org/insights/uruguay/uruguay-digital-bet"),
row("Stargate Argentina (OpenAI x Sur Energy)","Sur Energy (developer; OpenAI intended offtaker)","Confluencia area","Neuquen","Argentina",-38.95,-68.06,power=500,
    notes="LOI signed Oct 2025 for first Stargate project in Latin America: up to 500MW, up to $25B; still at LOI stage as of Oct 2026 - no definitive contract; not yet a committed project",url="https://www.sur.energy/press-release"),
row("Crusoe-Araico Itaipu AI Data Center","Crusoe (Crusoe Cloud) + Araico","Hernandarias (Itaipu)","Alto Parana","Paraguay",-25.49,-54.62,power=106,
    notes="Announced 22 Oct 2026: Crusoe's first dedicated AI cloud deployment in Latin America, powered by Itaipu hydro; path to 106MW IT, options to ~280MW; initial deployment mid-2027",url="https://capdex.com/news/crusoe-araico-partner-on-106-mw-ai-data-center-near-itaipu"),
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
