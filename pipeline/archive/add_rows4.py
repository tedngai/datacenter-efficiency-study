"""Append Africa + Eastern Europe/Central Asia + India/South Asia deep-dive rows.
H100e factors: H100/H200/GH200=1.0, B200/GB200=2.25, GB300/B300=2.5, A100=0.315, L40S=0.19.
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
# ---------------- AFRICA ----------------
row("Teraco Isando Campus (JB1/JB3/JB5)","Teraco (Digital Realty)","Isando (Johannesburg)","Gauteng","South Africa",-26.1380,28.1987,power=80,it=40,types="NVIDIA (DGX-Ready colocation; Altron AI Factory via ASUS/HPE)",
    notes="Operational; 40MW live IT of 80MVA total; hosts NAPAfrica and cloud on-ramps; JB5 (2024) is a 30MW AI-ready hall hosting Altron AI Factory (South Africa's first operational AI factory, live Oct 2025, customers incl. Lelapa AI)",url="https://africacomputetracker.org/facilities/teraco-isando-campus/"),
row("Teraco JB4 Bredell","Teraco (Digital Realty)","Bredell (Kempton Park)","Gauteng","South Africa",-26.0964,28.2401,it=50,types="NVIDIA AI-ready colocation",
    notes="Operational; 30MW expansion completed 2025 made JB4 Africa's largest standalone DC at 50MW critical IT; further JB7 expansion (~R8bn, +40MW AI-ready) announced 2025-2026",url="https://datacentremagazine.com/news/teraco-expands-jb4-into-africas-largest-data-centre"),
row("Vantage Data Centers Waterfall City","Vantage Data Centers","Midrand","Gauteng","South Africa",-26.0174,28.1041,it=87,
    notes="Announced Feb 2026; Vantage's South Africa entry; 87MW IT secured via SolarAfrica renewable PPA; no AI-specific capacity disclosed",url="https://africacomputetracker.org/facilities/vantage-waterfall-city/"),
row("Equinix Cape Town Airport Data Centre 1 & 2","Equinix","Cape Town","Western Cape","South Africa",-33.9706,18.5978,power=160,
    notes="Announced 2026; two new-build facilities (~80MW gross each per Africa Compute Tracker) at Cape Town Airport site; no IT-load or AI capacity disclosed yet",url="https://africacomputetracker.org/facilities/equinix-cape-town-airport-dc1/"),
row("Cosmas Data City Cape Town Campus","Cavaleros Group","Cape Town","Western Cape","South Africa",-33.9249,18.4241,power=360,
    notes="Announced/under development, expected from 2027; 360MW total plan - among Africa's largest announced campuses; no AI-specific disclosures yet",url="https://africacomputetracker.org/facilities/cavaleros-cdc-cape-town-campus/"),
row("Microsoft Azure South Africa Regions (Johannesburg & Cape Town)","Microsoft","Johannesburg & Cape Town","Gauteng / Western Cape","South Africa",-26.2041,28.0473,
    notes="Operating; Microsoft's first African cloud regions; ~$1.1B invested since 2019 plus R5.4bn (~$300M) announced Mar 2025 to expand cloud & AI capacity by 2027; no campus MW or GPU counts published",url="https://www.reuters.com/technology/artificial-intelligence/microsoft-invest-additional-54-billion-rand-south-africa-ai-infrastructure-2025-03-06/"),
row("Oracle Cloud Johannesburg Region","Oracle","Johannesburg","Gauteng","South Africa",-26.2041,28.0473,
    notes="Operating since Jan 2022 - Oracle's first African cloud region (af-johannesburg-1); offers OCI AI services; capacity not disclosed",url="https://www.oracle.com/news/announcement/oracle-cloud-johannesburg-region-2022-01-19/"),
row("AWS Africa (Cape Town) Region","Amazon Web Services","Cape Town","Western Cape","South Africa",-33.9249,18.4241,
    notes="Operating since Apr 2020 (af-south-1), AWS's first African region, 3 AZs; no capacity or GPU counts published",url="https://aws.amazon.com/blogs/aws/now-open-aws-africa-cape-town-region/"),
row("G42 / Microsoft East Africa Cloud Region (Olkaria)","G42 / Microsoft (with Kenya government partners)","Olkaria","Nakuru County","Kenya",-0.8833,36.3000,
    notes="Paused. Announced May 2024 as part of $1B Microsoft-G42 Kenya initiative (geothermal-powered Azure East Africa campus); by mid-2026 stalled: 100MW concept scaled to 1GW (~1/3 of Kenya's grid), talks broke down over offtake guarantees; not formally cancelled",url="https://africacomputetracker.org/facilities/g42-microsoft-kenya-dc1/"),
row("Rack Centre LGS2","Rack Centre (Jagal Group)","Lagos (Ikeja/Oregun)","Lagos State","Nigeria",6.6018,3.3515,it=12,types="AI-ready racks up to 70kW",
    notes="Operational, commissioned Apr 2025; West Africa's first hyperscale/AI-ready campus building: 12MW IT across six 2MW halls, N+2 cooling for 70kW racks; no GPU counts published",url="https://www.datacenterdynamics.com/en/news/rack-centre-launches-12mw-data-center-in-lagos-nigeria/"),
row("Kasi Cloud LOS1 (Lekki Campus)","Kasi Cloud Datacenters (NSIA / DH Capital-backed)","Lagos (Maiyegun, Lekki)","Lagos State","Nigeria",6.4386,3.5476,it=100,types="GPU racks 10-100kW design",
    notes="First phase operational (May 2026: 5.5MW data hall + 7.5MW ecosystem floor); ~100MW critical IT at full build; $250M initial capex; adjacent to Equiano & 2Africa subsea landings",url="https://nsia.com.ng/kasi-cloud-datacenters-commissions-west-africas-first-hyperscaleready-ai-capable-data-centre-campus-in-lagos/"),
row("AFRIDATA Nigeria (Lagos + Delta)","INFRAGORA Global Capital","Lagos & Delta State","Lagos State / Delta State","Nigeria",6.5244,3.3792,it=65,types="480 x 50kW GPU racks planned",
    notes="Announced Oct 2026, construction from Q2 2027; two AI-native Tier IV DCs, 60-70MW combined expanding to 100MW; $650M-$1B estimate; USTDA feasibility grant; financing not secured yet",url="https://ustda.gov/ustda-backs-ai-ready-data-center-development-in-nigeria/"),
row("ADC Egypt / Egypt Sovereign AI Data Centre","ADC Egypt JV (Vodafone Business + Elsewedy Electric + Cassava)","Cairo (site TBD)","Cairo Governorate","Egypt",30.0444,31.2357,it=20,types="NVIDIA (planned, via Cassava NVIDIA Cloud Partnership)",
    notes="Announced Sep 2026; Egypt's largest DC and first sovereign AI DC; 20MW initial within ~3 years on path to 200MW; ~$200M phase-1 FDI, up to $1B total; NVIDIA GPU-as-a-Service via Cassava (NVIDIA's first African cloud partner)",url="https://www.vodacom.com/news-article.php?articleID=16998"),
row("Nexus AI Factory","Nexus Core Systems (with Naver Cloud; Morocco Ministry of Digital Transition)","Nouaceur (Casablanca)","Casablanca-Settat","Morocco",33.4300,-7.6000,it=16,types="NVIDIA Blackwell (planned)",
    notes="Announced Apr 2026 at GITEX Africa; $1.2B initial; phase 1 16MW, phase 2 to 36MW by end-2027; 500MW long-term target on TAQA Morocco renewables",url="https://gitexafrica.com/articles/nexus-factory-launch-at-gitex-africa-positions-morocco-as-a-future-ai-gateway"),
row("Wingu Africa Addis Ababa Data Centre (EAII AI partnership)","Wingu Group (with Ethiopian AI Institute)","Addis Ababa","","Ethiopia",9.0100,38.7600,types="NVIDIA DGX H200 (EAII tender Dec 2025)",
    notes="Operating; Tier III carrier-neutral facility; May 2025 partnership with Ethiopian AI Institute to host AI compute; EAII tendered NVIDIA DGX H200 purchases Dec 2025; capacity figures not published",url="https://africacomputetracker.org/facilities/"),
# ---------------- EASTERN EUROPE / CAUCASUS / CENTRAL ASIA ----------------
row("Baltic AI GigaFactory (bid)","Poland-led consortium (with Lithuania, Czechia; EuroHPC tender)","TBD (shortlist: Krakow, Wroclaw, Poznan, Skawina, Warsaw)","Poland","Poland",51.1079,17.0385,gpu=25000,types="H100e-class accelerators (EuroHPC Lot 1 medium: 25k-75k H100e)",h_gpu=25000,
    notes="Bid/planned; EUR 3bn Baltic AI GigaFactory EoI approved by EC Jul 2025; EUR 100M Polish state commitment approved Jul 2026; contracts expected early 2027, launch ~2028; one of 76 EU gigafactory bids (Poland centroid coords)",url="https://nowosci.ai/en/article/five-polish-cities-race-eu-ai-gigafactory"),
row("Atman Data Center Warsaw-3 (WAW-3)","Atman (Polcom)","Duchnice (Ozarowska 66B)","Mazowieckie","Poland",52.199,20.860,power=43.2,it=14.4,types="NVIDIA L4/L40S/H200 offered (Power line)",
    notes="First building 14.4MW IT live, expanding to 3 buildings/43.2MW IT by ~2028; Poland's largest AI-ready colocation campus; 140kW/rack, liquid cooling",url="https://atman.pl/en/atman-data-center/warsaw-3/"),
row("Microsoft Cloud Region Poland (Mazovia expansion)","Microsoft (SPV)","Warsaw area (3 DCs)","Mazowieckie","Poland",52.230,21.010,types="Azure (GPU-backed cloud region)",
    notes="Operating (region live Apr 2023, $1bn phase 1) + $700M phase 2 through mid-2026 for AI & cloud (announced Feb 2025); hosts Bielik/PLLuM Polish LLMs; power not disclosed",url="https://www.gov.pl/web/primeminister/microsoft-invests-pln-3-billion-in-a-new-data-center-in-poland"),
row("KarolAIna Supercomputer (Czech AI Factory CZAI)","IT4Innovations (VSB-TUO consortium)","Ostrava","Moravian-Silesian","Czechia",49.826,18.162,gpu=340,types="AI-optimized chips (unspecified)",pflops=850,
    notes="Planned (CZAI project 2026-2029, ~CZK 1bn, 50% EuroHPC); successor to Karolina; 850 PF AI peak; Czech AI Factory won Oct 2025 EuroHPC call",url="https://www.it4i.cz/en/about/infoservice/news/the-czech-republic-has-its-own-ai-factory-including-a-new-ai-supercomputer"),
row("RO AI Factory Supercomputer","ICI Bucharest + POLITEHNICA Bucharest consortium","Bucharest","Bucharest-Ilfov","Romania",44.473,26.089,types="AI-optimized supercomputer (vendor TBD)",pflops=5000,
    notes="Planned/procurement; started Sep 2026, fully operational by end-2027; EUR 50M; >5 EFLOPS AI peak; Romania won EuroHPC AI Factory Oct 2025",url="https://datacenter-forum.ro/en/interview-with-victor-vevera-ici-bucharest-what-resources-and-services-will-ro-ai-factory-provide-and-when-will-it-become-operational/"),
row("BRAIN++ / Discoverer++ AI Supercomputer","Sofia Tech Park + INSAIT","Sofia","Sofia-Grad","Bulgaria",42.660,23.376,
    notes="Planned/procurement; EUR 90M EuroHPC AI Factory (selected Mar 2025); Discoverer++ tender (EUR 54.2M) closed Oct 2026, install by end-2026; existing Discoverer+ upgraded Apr 2025 with GPU partition for AI",url="https://www.eurohpc-ju.europa.eu/ai-factories/bulgaria_en"),
row("LitAI Factory Supercomputer","Vilnius University consortium (LRTC host)","Vilnius","Vilnius","Lithuania",54.700,25.250,
    notes="Planned (won EuroHPC Oct 2025); EUR 130M project (EUR 65M EU co-funding), largest AI factory in the Baltics; hosted at LRTC Third State Data Centre; GPU types TBD",url="https://eimin.lrv.lt/en/structure-and-contacts/news-1/eimin-lithuania-wins-65-million-eu-tender-for-the-countrys-first-artificial-intelligence-centre-hVuh/"),
row("SLAIF Next-Gen AI Supercomputer (Vega successor)","IZUM with ARNES & Jozef Stefan Institute","Maribor (ARNES DC at Mariborski otok HE hydropower campus)","Podravska","Slovenia",46.545,15.640,types="AI-optimized EuroHPC system (TBD)",pflops=10000,
    notes="Planned, production expected late 2027 at new hydro-powered ARNES DC; 10 EFLOPS mixed-precision AI + 100 PF FP64; Slovenian AI Factory (EuroHPC, selected Mar 2025)",url="https://www.sling.si/en/slaif/"),
row("LEVENTE Supercomputer","DKF (Digital Government Development Co.)","Budapest","Budapest","Hungary",47.497,19.040,types="AI-capable mid-range system (TBD)",
    notes="Planned; hosting agreement Jul 2025, procurement underway, online ~2027; EUR 42M (35% EuroHPC); at least 23 PF FP64 (kept out of FP8 column); Hungary also holds HunAIFA antenna + Komondor (5 PF, 200+ GPUs, Debrecen)",url="https://www.eurohpc-ju.europa.eu/way-open-building-eurohpc-world-class-supercomputer-hungary-2025-07-09_en"),
row("Serbian National AI Platform (SAIFA host)","Office for IT and eGovernment (Government of Serbia)","Kragujevac","Sumadija","Serbia",44.013,20.911,gpu=80,types="NVIDIA DGX A100 (32 GPUs) + DGX H200 (48 GPUs)",pflops=37,h_gpu=58,
    notes="Operating + upgrading; gov DC Kragujevac: 4x DGX A100 (5 PF AI) free for academia; 6x DGX H200 (32 PF AI) available 2025; H100e = 32 A100 x0.315 + 48 H200; SAIFA AI Factory Antenna won (linked to Pharos Greece & IT4LIA Italy)",url="https://www.ite.gov.rs/tekst/en/35/national-platform-for-artificial-intelligence-ai.php"),
row("Ukraine State AI Factory","Ministry of Digital Transformation of Ukraine","Kyiv (national; sites not disclosed)","Kyiv","Ukraine",50.450,30.523,types="GPU clusters (TBD)",
    notes="Announced Aug 2025, planned; first state AI infrastructure: GPU compute clusters + water-cooled server rooms; first users Diia AI assistant & Dream AI tutor; no MW/GPU counts published (wartime)",url="https://fact-news.com.ua/en/ukraine-to-create-state-infrastructure-for-ai-development/"),
row("Google Cloud & Turkcell Hyperscale Region (Turkiye)","Turkcell (infra partner) + Google Cloud","Ankara","Ankara","Turkey",39.933,32.859,power=200,types="Google Cloud accelerators (unpublished)",
    notes="Announced; construction from Q1 2026, full capacity by 2028; first hyperscale DC in Turkiye: 3 synchronized DCs (Sovereign Cloud); Google $2bn/10yr + Turkcell $1bn; 200MW is a third-party estimate, not officially stated",url="https://datacenterindex.ai/projects/google-turkcell-turkey-hyperscale-ai-campus"),
row("ARF / ARF-ACC (TRUBA National Supercomputing)","TUBITAK ULAKBIM (TRUBA)","Ankara","Ankara","Turkey",39.891,32.783,gpu=504,types="Mix incl. NVIDIA A100 (72), H100 (24), P100/V100; 80k+ CPU cores",pflops=5,
    notes="Operating, growing; Turkiye's most powerful national HPC/AI system; 504 GPUs per ministry (Oct 2025); mixed generations so no single H100e factor applied",url="https://ulakbim.tubitak.gov.tr/en/tbmm-artificial-intelligence-research-commission-visits-tubitak-ulakbimi-turkeys-supercomputer-infrastructure-under-scrutiny/"),
row("Firebird AI Data Center Hrazdan","Firebird (AI cloud) with Government of Armenia, NVIDIA, Team Group","Hrazdan","Kotayk","Armenia",40.536,44.767,power=100,types="NVIDIA Blackwell (thousands, count unpublished)",
    notes="Under construction; $500M initial investment; first phase operational Q2 2026 (US export approval received); scalable to >100MW; first regional AI factory in the Caucasus",url="https://armenpress.am/en/article/1236360"),
row("AzInTelecom Supercomputer Center","AzInTelecom LLC (AZCON Holding)","Baku","Baku","Azerbaijan",40.409,49.867,types="NVIDIA H200",
    notes="Operating (introduced Dec 2025) + expanding; first supercomputer center in Azerbaijan under AI Strategy 2025-2028; within two Tier III DCs (Baku, Yevlakh) with two more under construction",url="https://www.trend.az/azerbaijan/society/4129979.html"),
row("Alem.cloud National AI Supercomputer (Alem.AI)","NITEC / Ministry of AI & Digital Development (built with Presight/G42)","Astana","Astana","Kazakhstan",51.128,71.430,types="NVIDIA H200",pflops=2000,
    notes="Operating (launched Jul 2025); ~2 EFLOPS FP8 peak, most powerful in Central Asia; at ministry Tier III DC in Alem.AI hub; access via QazCompute (free for startups/universities); GPU count unpublished",url="https://astanatimes.com/2025/09/kazakhstans-first-supercomputer-how-it-works-why-it-matters/"),
row("Data Center Valley Ekibastuz","Firebird + JSC Kazakhtelecom (with NVIDIA)","Ekibastuz","Pavlodar","Kazakhstan",51.686,75.320,power=300,gpu=100000,types="NVIDIA GB300 and Vera Rubin",
    notes="Announced Jun 2026 ($10bn agreements); 300MW power available now, phased expansion designed to 1GW; 100k state-of-the-art GPUs planned; mixed GB300 + unreleased Rubin so no single H100e factor applied (>=225k if all GB300-class)",url="https://primeminister.kz/en/news/data-center-valley-kazakhstan-government-firebird-and-nvidia-sign-10-billion-package-of-agreements-in-artificial-intelligence-31516"),
row("DataVolt TAS-1 (Tashkent IT Park DC)","DataVolt (Saudi Arabia) at Tashkent IT Park","Tashkent","Tashkent","Uzbekistan",41.311,69.290,power=12,
    notes="Under construction; phase 1 ready-for-service end-2026; Central Asia's largest AI-ready green DC (>95% green power); DataVolt plans $6.5bn/20 DCs/520MW in Uzbekistan by 2030; govt procuring Blackwell B200 clusters nationally",url="https://data-volt.com/media/breaking-news/150m-non-recourse-financing-for-central-asias-largest-ai-ready-data-center/"),
# ---------------- INDIA & SOUTH ASIA ----------------
row("IndiaAI Compute Platform (National GPU Pool)","MeitY/IndiaAI (empanelled CSPs: Yotta, Netmagic/SIFY, E2E, Jio, NxtGen, CtrlS, Tata Comm, Locuz, Vensysco)","Distributed nationwide","(nationwide)","India",22.35,78.66,gpu=34333,types="NVIDIA H100/H200/A100/L40S/L4, AMD MI300X/MI325X, Intel Gaudi 2, AWS Inferentia2/Trainium",
    notes="National distributed AI compute pool, not a single campus; 18,000+ GPUs announced Feb 2025, scaled to 34,333 in 2nd round (late 2025); tenants incl. Sarvam AI (4,096 H100 SXM at Yotta); mixed chip types so no single H100e factor applied (most H100/H200-class, ~30k H100e order of magnitude); India centroid coords",url="https://www.fortuneindia.com/technology/indiaai-mission-scales-up-with-34000-gpus-backs-indian-ai-models-for-the-future/123599"),
row("Yotta D2 Greater Noida","Yotta Data Services (Hiranandani)","Greater Noida","Uttar Pradesh","India",28.4744,77.5040,power=60,it=60,gpu=20736,types="NVIDIA HGX B300 (Blackwell Ultra)",h_gpu=51840,
    notes="Under construction; $2B+ investment; India's first Blackwell Ultra deployment; go-live targeted Aug 2026; 10,000+ GPUs committed to IndiaAI Mission; will host one of APAC's largest NVIDIA DGX Cloud clusters; campus scalable to 250MW",url="https://mlq.ai/news/yotta-data-services-announces-2-billion-investment-for-nvidia-blackwell-ai-supercluster-in-india"),
row("Yotta D1 Greater Noida","Yotta Data Services (Hiranandani)","Greater Noida","Uttar Pradesh","India",28.4744,77.5040,power=50,it=30,types="NVIDIA (Yotta Shakti Cloud GPU-ready)",
    notes="Operating since 2021; 300,000 sq ft Tier III+ hyperscale, 30MW IT expandable to 50MW; D4 building on same campus planned at 120MW with reported ~95,000 GPUs (50k Vera Rubin + 45k GB300, ~$7.5B, reported 2026 - rumor/pipeline)",url="https://yotta.com/data-center-in-india"),
row("Yotta NM2 Navi Mumbai","Yotta Data Services (Hiranandani)","Navi Mumbai","Maharashtra","India",18.9960,73.1170,power=80,types="NVIDIA GB300 / Vera Rubin (planned)",
    notes="Under construction/fit-out within NM1 campus park (scalable to 1-2GW); reported 75-80MW designed to support ~36,000-40,000 GB300-class GPUs (estimate); part of Yotta's plan to exceed 80,000 GPUs by FY27-28",url="https://www.blackridgeresearch.com/blog/list-of-top-ten-largest-data-center-companies-in-india"),
row("L&T Vyoma SPD1 (Sriperumbudur AI Campus)","L&T-Cloudfiniti / Vyoma.AI (LTN Compute)","Chennai (Sriperumbudur)","Tamil Nadu","India",12.9675,79.9430,power=250,it=30,gpu=10000,types="NVIDIA B300",h_gpu=25000,
    notes="30MW facility live; campus Phase 1 designed for 250MW (billed gigawatt-scale); will host India's largest NVIDIA B300 AI Factory (10,000 GPUs) for Together AI (~$1-1.75B deal, Aug 2026); 52MW expansion groundbreaking Oct 2026",url="https://www.larsentoubro.com/pressreleases/2026/2026-08-13-larsen-toubro-secures-mega-order-as-part-of-a-strategic-partnership-with-together-ai-to-build-indias-largest-nvidia-b300-ai-factory"),
row("E2E Networks TIR AI DC Chennai (at L&T Vyoma)","E2E Networks","Chennai (Sriperumbudur)","Tamil Nadu","India",12.9675,79.9430,gpu=1024,types="NVIDIA B200 (1,024), plus H200/H100 clusters",h_gpu=2304,
    notes="IndiaAI L1 empanelled provider; 1,024-GPU B200 cluster procured for Chennai DC at L&T Vyoma (H100e for the B200s only); E2E also operates 2,048 H200 + ~1,000 H100 across Delhi NCR and Chennai",url="https://www.datacenterdynamics.com/en/news/e2e-networks-acquires-1024-nvidia-b200-gpu-cluster-for-chennai-data-center"),
row("NxtGen AI Factory Bengaluru","NxtGen AI (NxtGen Cloud Technologies)","Bengaluru","Karnataka","India",12.8452,77.6600,gpu=4096,types="NVIDIA Blackwell (B200-class)",h_gpu=9216,
    notes="Announced Jan 2026; Rs 3,600 crore sovereign AI factory built with Dell AI Factory with NVIDIA; described as India's first dedicated AI factory; IndiaAI empanelled provider",url="https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~1~dell-technologies-enables-nxtgen-to-build-indias-largest-ai-factory.htm"),
row("STT Noida 2 (Neysa AI Deployment)","STT GDC India (tenant: Neysa Networks)","Noida (Greater Noida)","Uttar Pradesh","India",28.6000,77.3800,gpu=9000,types="GPU (type unspecified)",h_gpu=9000,
    notes="Neysa to deploy GPU infrastructure supporting up to 9,000 GPUs in first phase; go-live Q1 2027; high-density AI training/inference; Neysa (Blackstone-backed, $1B+) plans 20,000+ GPUs in India",url="https://www.datacenterdynamics.com/en/news/sttgdc-to-host-neysa-gpus-at-data-center-in-noida-india"),
row("NTT DATA-Neysa Hyderabad AI DC Cluster","NTT DATA + Neysa Networks (Telangana govt MoU)","Hyderabad","Telangana","India",17.3850,78.4867,power=400,gpu=25000,types="GPU (type unspecified)",h_gpu=25000,
    notes="Planned; Rs 10,500 crore (~$1.2B) tripartite MoU Apr 2025; 400MW AI DC cluster with up to 25,000 GPUs, billed as India's most powerful AI supercomputing infrastructure; 500MW total power via grid + renewables",url="https://www.datacenterdynamics.com/en/news/ntt-plans-data-center-in-hyderabad-india"),
row("Google-AdaniConneX Visakhapatnam AI Hub","Google (owner) / AdaniConneX + Nxtra by Airtel (developers)","Visakhapatnam","Andhra Pradesh","India",17.7521,83.3246,power=1000,
    notes="Announced Oct 2025; ~$15B 2026-2030; gigawatt-scale AI campus across three sites plus green energy (Adani Khavda) and subsea cable gateway; first 400MW phase awarded to AdaniConneX; groundbreaking 2026; billed as India's largest AI DC campus",url="https://www.adani.com/newsroom/media-releases/adani-and-google-partner-to-build-indias-largest-data-centre-campus-in-visakhapatnam"),
row("Digital Connexion Visakhapatnam AI-Native Campus","Digital Connexion (Reliance + Brookfield + Digital Realty JV)","Visakhapatnam","Andhra Pradesh","India",17.7200,83.2900,power=1000,types="AI-native GPU (planned)",
    notes="MoU Nov 2025; $11B by 2030 for 1GW AI-native capacity across 400 acres; purpose-built 40-100kW racks; JV also operates Chennai MAA10 (20MW live, 100-120MW campus)",url="https://www.datacenterdynamics.com/en/news/digital-connexion-signs-mou-to-build-1gw-campus-in-andhra-pradesh-india"),
row("HyperVault AI Data Center Hyderabad","HyperVault (TCS subsidiary; TPG strategic partner)","Hyderabad","Telangana","India",17.3850,78.4867,power=1000,
    notes="Announced Sep 2026; 264 acres secured for up to 1GW AI-ready campus; TPG committed $1B (TCS+TPG up to Rs 18,000 crore); liquid-cooled direct-to-chip; first of >1GW planned across India",url="https://www.tcs.com/who-we-are/newsroom/press-release/tcs-hypervault-establish-large-scale-ai-data-center-campus-telangana"),
row("Microsoft India South Central Region (Hyderabad)","Microsoft","Hyderabad","Telangana","India",17.4200,78.3400,types="AI-ready Azure (GPU fleet unspecified)",
    notes="Microsoft's largest India hyperscale region, 3 AZs, AI-ready, went live 2026 (strategic Asia/Global South hub); part of $17.5B India investment 2026-2030 (on top of $3B announced Jan 2025); also expanding Chennai, Hyderabad, Pune",url="https://news.microsoft.com/source/asia/2026/09/21/ai-ambition-into-action-microsoft-brings-ai-ready-capabilities-across-its-india-cloud-infrastructure-establishes-india-south-central-region-as-a-strategic-hub-for-asia-and-global-south"),
row("AWS Asia Pacific (Hyderabad) Expansion","Amazon Web Services","Hyderabad","Telangana","India",17.4400,78.3700,types="AWS AI chips (Trainium/Inferentia)",
    notes="Region operating since Nov 2022; $7B Hyderabad expansion agreement with Telangana (groundbreaking Aug 2026); additional $13B announced 2026 for Mumbai+Hyderabad AI/cloud (part of $21B 2026-2030 India plan)",url="https://www.datacenterdynamics.com/en/news/aws-to-invest-7bn-in-data-centers-in-hyderabad-india"),
row("Sify Noida 02 AI-Ready Hyperscale Campus","Sify Infinit Spaces (Sify Technologies)","Noida (Delhi NCR)","Uttar Pradesh","India",28.5355,77.3910,power=43,it=25.92,types="GPU colocation (NVIDIA DGX-Ready certified)",
    notes="Sify's largest AI-ready hyperscale campus in North India; NVIDIA DGX-Ready certified up to 130kW/rack with D2C and rear-door cooling; Sify portfolio 129MW operational (Mar 2026) + 103MW AI-ready additions (IFC-backed)",url="https://www.sifytechnologies.com/data-center"),
row("Sify Rabale (Mumbai 03) Hyperscale AI Campus","Sify Infinit Spaces (Sify Technologies)","Navi Mumbai (Rabale)","Maharashtra","India",19.1157,73.0155,power=377,types="GPU colocation (NVIDIA DGX-Ready certified)",
    notes="T5 campus designed for 12 towers (5 operational), scalable to 377+MW IT; NVIDIA DGX-Ready certified (2024, among India's first); 200+ kW/rack capable",url="https://sifyinfinitspaces.com"),
row("CtrlS Chandan Valley AI Campus","CtrlS Datacenters","Hyderabad (Chandanvelly)","Telangana","India",17.1449,78.1334,power=700,types="Liquid-cooled AI racks (GPU-ready)",
    notes="Planned/developing; 40 acres, >700MW scalable to 1.4GW, 700 MVA sanctioned; AI-ready liquid cooling; sister Future City campus planned at 750MW (100% green); CtrlS targets 4.4GW by 2030",url="https://www.ctrls.com/datacenter-hyderabad"),
row("Anant Raj Manesar AI Cloud DC","Anant Raj Ltd","Manesar (Gurugram)","Haryana","India",28.3580,76.9390,power=50,it=21,types="Immersion-cooled AI/GPU (Submer partnership)",
    notes="21MW phase live at ARL Tech Park, campus designed for 50MW; Submer immersion-cooled AI/GPU partnership; ~28MW operational across Manesar/Rai/Panchkula with 300MW potential",url="https://anantrajcloud.com"),
row("Data Vault Pakistan AI Data Center","Data Vault Pakistan (with Telenor Pakistan)","Karachi (Korangi)","Sindh","Pakistan",24.8330,67.1400,it=3,gpu=3000,types="NVIDIA H100/H200 (claimed)",h_gpu=3000,
    notes="Launched Nov 2025; Pakistan's first AI-ready sovereign DC & GPU-as-a-Service (Telenor partnership); >3,000 H100/H200 GPUs reported via US export licenses (unverified claim); ~3MW AI IT load is DCMI estimate",url="https://datavault.com.pk"),
row("Sky47 Karakorum-01","Sky47","Rawalpindi","Punjab","Pakistan",33.6000,73.0500,power=8.5,
    notes="Opened Jul 2026 with 8.5MW; offers GPU capacity from Rawalpindi; Pakistan's AI IT load estimated ~2MW end-2025 growing to ~68MW by 2030 (DCMI estimate)",url="https://www.dcmarketinsights.com/report/pakistan-data-center-market"),
row("Summit Group Data Centre (Planned)","Summit Group / Summit Communications","near Dhaka","Dhaka","Bangladesh",23.7810,90.4150,
    notes="Planned; announced Jan 2026 as Summit's first data center near Dhaka leveraging its power generation, fiber, and land; talks with global tech partners; Bangladesh govt separately plans sovereign AI infrastructure; capacity/GPUs not disclosed",url="https://www.linkedin.com/posts/summitcommltd_summit-group-plans-first-data-centre-in-bangladesh-activity-7414613905286766592-ByZ6"),
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
