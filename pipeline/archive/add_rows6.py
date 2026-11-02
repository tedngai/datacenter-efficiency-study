"""Append country-by-country sweep rows (APAC, W.Europe/Nordics, Americas, ME/Africa/S.Asia).
Drops 3 duplicates found across sweeps/existing data.
Also normalizes country name 'UAE' -> 'United Arab Emirates'.
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
# ---------------- ASIA-PACIFIC ----------------
row("AirTrunk SYD3 Sydney West","AirTrunk","Sydney","New South Wales","Australia",-33.797,150.880,power=330,it=330,
    notes="Operating/expanding; 330MW+ (facility page now cites 400+MW masterplan); 42 data halls on 8.3ha; AirTrunk calls it APAC's largest hyperscale campus outside China; part of AirTrunk's >1.2GW Australian platform",
    url="https://airtrunk.com/location/syd3-sydney-west/"),
row("AirTrunk SYD2 Sydney North","AirTrunk","Sydney","New South Wales","Australia",-33.808,151.158,power=158,it=158,
    notes="Operating since 2021; 158MW+; 24 data halls; 132kV diverse feed; PUE 1.15; hyperscale/AI cloud campus",
    url="https://airtrunk.com/location/syd2-sydney-north/"),
row("AirTrunk MEL1 Melbourne","AirTrunk","Melbourne","Victoria","Australia",-37.803,144.735,power=276,it=276,
    notes="Operating; 276MW+; 34 data halls on 8.8ha; part of >630MW AirTrunk Melbourne platform with MEL2",
    url="https://airtrunk.com/location/mel1-melbourne/"),
row("AirTrunk MEL2 Melbourne","AirTrunk","Melbourne","Victoria","Australia",-37.700,144.780,power=354,it=354,
    notes="Planned/under construction; site acquired Dec 2025; 354MW+ campus, A$5B+, up to 32 data halls; lifts AirTrunk Melbourne to >630MW (coords approximate)",
    url="https://airtrunk.com/location/mel2-melbourne/"),
row("NEXTDC M3 Melbourne","NEXTDC","Melbourne","Victoria","Australia",-37.801,144.884,power=225,it=225,
    notes="Operating/expanding; 225MW IT campus at West Footscray, 23,000 racks; Tier IV; 185MW fit-out in progress at Dec 2025; positioned for cloud, AI and high-density compute",
    url="https://www.nextdc.com/data-centres/melbourne-data-centres/m3-melbourne"),
row("CDC Marsden Park Data Centre","CDC Data Centres","Sydney","New South Wales","Australia",-33.685,150.837,power=720,it=504,
    notes="Under construction since Oct 2024; 504MW ICT load with 720MVA dedicated substation; six 4-storey buildings, 24 data halls each, 20.1ha; billed as largest DC campus in the Southern Hemisphere; AI-ready",
    url="https://cdc.com.au/resources/news/cdc-data-centres-breaks-ground-on-new-state-of-the-art-data-centre-development-in-marsden-park-industrial-precinct/"),
row("Firmus Southgate Melbourne","Firmus Technologies","Melbourne","Victoria","Australia",-37.816,144.845,power=57,it=41,gpu=18400,types="NVIDIA GB300",h_3p=46488,
    notes="Operating 2026 at CDC Brooklyn campus; 18,400 GB300 GPUs contracted (Mar 2026), running customer models by Aug 2026; Epoch AI: 41MW IT / 57MW gross / ~46.5k H100e; first stage of 1.6GW Project Southgate with CDC and NVIDIA",
    url="https://firmus.co/newsroom/southgate-expansion"),
row("AWS Asia Pacific (Sydney) Region","Amazon Web Services","Sydney","New South Wales","Australia",-33.860,151.040,power=300,it=300,
    notes="Operating; ap-southeast-2 with 3 AZs; ~300MW campus IT per third-party tracker (AWS does not publish site MW); part of A$20B 2025-2029 Australian expansion; Trainium/Inferentia and GPU AI workloads",
    url="https://datacentersearch.org/sites/aws-sydney"),
row("Datagrid New Zealand AI Factory","Datagrid New Zealand","Invercargill","Southland","New Zealand",-46.350,168.330,power=280,
    notes="Under construction; consent granted Mar 2026, earthworks Jul 2026; phase 1 280MW, full build-out 1GW on 49ha; NZ$5B; dedicated grid exit point; Tasman Ring subsea cable landing",
    url="https://www.datagrid.nz/pr1-rc/resourceconsent"),
row("AirTrunk Singapore SGP1/SGP2","AirTrunk","Singapore","Singapore","Singapore",1.371,103.973,power=148,it=148,
    notes="SGP1 78MW+ operating since 2020; SGP2 70MW+ under development; combined 148MW+ at Loyang near Changi North cable landing; Singapore's largest independent hyperscale platform",
    url="https://airtrunk.com/location/singapore/"),
row("Nxera DC Tuas","Nxera (Singtel)","Singapore","Singapore","Singapore",1.320,103.652,power=58,it=58,
    notes="Operational Feb 2026; 58MW AI-ready, Singapore's highest power-density multi-tenant DC; largest direct-to-chip liquid cooling deployment in Singapore; >90% pre-committed; integrated cable landing station",
    url="https://www.nxera-dc.com/about-us/newsroom/nxera-opens-data-centre"),
row("Oracle Indonesia North (Batam)","Oracle","Batam","Riau Islands","Indonesia",1.186,104.090,power=94,it=72,types="NVIDIA B200/B300",h_3p=84386,
    notes="Operational; OCI ap-batam-1 launched May 2025; three buildings at DayOne Nongsa Digital Park; 34MW committed plus 38MW reserved; Epoch AI: 72MW IT / ~84.4k H100e; anchor AI cloud region for Singapore overflow",
    url="https://epoch.ai/data/ai-data-centers/directory/oracle-batam"),
row("Princeton Digital Group BT1 Batam","Princeton Digital Group","Batam","Riau Islands","Indonesia",1.170,104.080,power=96,it=96,
    notes="Planned/under construction; 96MW campus in Nongsa Digital Park, four buildings up to 24MW each on 15 acres; power fully secured; part of PDG's $1B SG+ strategy",
    url="https://princetondg.com/press-releases/princeton-digital-group-announces-sg-a-comprehensive-strategy-for-the-singapore-region-with-an-initial-investment-plan-of-us1b-expanding-to-batam-and-johor/"),
row("STT Bangkok Campus (BKK1/BKK2)","ST Telemedia Global Data Centres","Bangkok","Bangkok","Thailand",13.735,100.645,power=47,it=47,
    notes="Under development; BKK1 23MW + BKK2 24MW at Hua Mak; NVIDIA DGX-Ready; immersion and direct-to-chip liquid cooling; Thailand's largest carrier-neutral hyperscale campus",
    url="https://www.sttgdc.com/th-en/locations/bangkok"),
row("Google Chonburi Data Center","Google","Chonburi","Chonburi","Thailand",13.150,101.300,power=100,
    notes="Under construction at WHA Nong Yai industrial estate; part of $1B Thailand investment announced Sep 2024; ~half complete Aug 2026; 100MW is a third-party estimate (Google has not published MW)",
    url="https://www.googlecloudpresscorner.com/2024-09-30-Google-Announces-Plans-to-Invest-US-1-Billion-to-Build-Data-Center-and-Cloud-Region-in-Thailand,-Support-Initiatives-to-Expand-AI-Opportunities-for-Thais"),
row("VITRO Santa Rosa Data Center","VITRO (PLDT/ePLDT)","Santa Rosa","Laguna","Philippines",14.284,121.111,power=50,it=50,
    notes="Operational Jul 2024; 50MW, 4,500+ racks; Philippines' first AI-ready hyperscale DC; TIA-942 Rated 3; hosts ePLDT's first NVIDIA GPU servers and GPU-as-a-Service; PLDT targets up to 500MW national capacity",
    url="https://vitrodc.com/vitro-benchmark-data-center-excellence-ai-ready-santa-rosa/"),
row("FPT AI Factory","FPT Corporation","Hanoi","Hanoi","Vietnam",21.013,105.526,power=4.2,gpu=3000,types="NVIDIA H100",pflops=2968,h_gpu=3000,
    notes="Operational Jan 2025 at Hoa Lac Hi-Tech Park; Vietnam's first AI factory, ~$200M; Epoch AI estimates ~3,000 H100 SXM5 and 2.97 EFLOPS FP16 (FPT disclosed 'thousands')",
    url="https://fpt.com/en/news/fpt-news/can-canh-sieu-chip-nvidia-tai-nha-may-ai-cua-fpt-tai-viet-nam"),
row("Google Changhua Data Center","Google","Changhua","Changhua County","Taiwan",24.080,120.430,power=300,
    notes="Operational since 2013, repeatedly expanded; Google's largest DC in Asia and a key AI/TPU hub; 300MW is a third-party estimate (Google does not publish site MW)",
    url="https://datacenters.google/locations/taiwan"),
# ---------------- WESTERN EUROPE / NORDICS ----------------
row("Meta Clonee","Meta","Clonee","County Meath","Ireland",53.4117,-6.4432,power=200,it=170,
    notes="Operating; first building 2018, campus expanded; Meta says the site supports AI and cloud workloads; 219MW of new Irish renewables contracted; ~EUR 1.4bn invested; power figures are estimates from campus scale",
    url="https://datacenters.atmeta.com/asset/clonee-data-center-info-sheet/"),
row("AWS Dublin Cruiserath Campus","Amazon Web Services","Dublin (Cruiserath, Mulhuddart)","County Dublin","Ireland",53.4046,-6.3673,power=220,it=220,
    notes="Operating/expanding; 65-acre campus buildings A-G; F and G online 2025-26; full build-out ~220MW (new E/F/G load 73MW); AWS AI/cloud region",
    url="https://www.datacenterdynamics.com/en/news/amazon-gets-ok-for-three-new-data-centers-in-dublin/"),
row("Google Eemshaven","Google","Eemshaven","Groningen","Netherlands",53.4375,6.8281,power=100,it=90,
    notes="Operating since 2016; >100MW; anchor of europe-west4; canal-water cooling; Google cites the site as supporting AI-powered services; IT load estimated",
    url="https://datacenters.google/locations/eemshaven-netherlands-var"),
row("Microsoft Middenmeer","Microsoft","Middenmeer","Noord-Holland","Netherlands",52.8067,4.9931,power=250,it=210,
    notes="Operating/expanding; Agriport A7 campus (~53ha), six new buildings proposed 2025; Microsoft's total Dutch footprint ~548MW; per-site split not published (estimate)",
    url="https://local.microsoft.com/blog/microsoft-bouwt-aan-toekomstbestendige-datacentercampus-in-middenmeer/"),
row("Google Saint-Ghislain","Google","Saint-Ghislain","Hainaut (Wallonia)","Belgium",50.4592,3.8264,power=300,it=260,
    notes="Operating; EUR 5bn AI infrastructure investment announced Oct 2025 for 2026-27 expansion; second campus under construction; grid operator Elia confirmed 200-300MW available",
    url="https://www.googlecloudpresscorner.com/2025-10-07-Google-Announces-New-EUR5-Billion-AI-Infrastructure-Investment-in-Belgium-through-2027"),
row("Meta Odense","Meta","Odense","Region of Southern Denmark","Denmark",55.4368,10.3593,power=540,it=475,
    notes="Operating; three buildings (~900,000 sq ft); ~475MW live capacity (DC Atlas estimate), 540MW grid access; waste heat donated to Odense district heating (up to 25MW)",
    url="https://dcatlas.io/en/explore/facilities/meta-inc-odense-denmark-data-center-odense"),
row("Google Fredericia","Google","Fredericia","Region of Southern Denmark","Denmark",55.5657,9.7025,power=160,it=140,
    notes="Operating; Google's first Danish DC, DKK 4.5bn; 160MW capacity matched by 160MW of Danish solar; supports AI-powered services",
    url="https://www.datacenter-forum.com/datacenter-forum/after-two-years-of-construction-google-opens-data-center-in-fredericia-denmark"),
row("CA DataCenter Skive","CA Group (CA DataCenter)","Skive (GreenLab, Spottrup)","Central Jutland","Denmark",56.59,8.79,power=110,it=100,
    notes="Under construction/planned; up to 100MW IT flexible AI/HPC DC inside GreenLab's sector-coupled energy park; fully operational expected 2027",
    url="https://www.greenlab.dk/knowledge/renowned-swedish-company-invests-billions-in-in-ai-data-center-in-greenlab/"),
row("Meta Lulea","Meta","Lulea","Norrbotten","Sweden",65.6147,22.137,power=120,it=100,
    notes="Operating since 2013; multiple buildings on Lule river hydro power; one of Meta's first European sites, now carrying AI/cloud workloads (power estimated)",
    url="https://datacenters.atmeta.com/asset/lulea-data-center-info-sheet/"),
row("Microsoft Sweden (Sandviken/Gavle)","Microsoft","Sandviken","Gavleborg","Sweden",60.621,16.776,power=150,it=120,gpu=20000,types="NVIDIA GPUs (unspecified)",
    notes="Operating; $3.2bn Swedish cloud/AI investment announced 2024; more than 20,000 GPUs deployed across Sandviken, Gavle and Staffanstorp (aggregate figure, not per site, so no per-site H100e applied); Sweden Central Azure region",
    url="https://www.datacenterdynamics.com/en/news/microsoft-to-deploy-20000-gpus-in-sweden/"),
row("atNorth Solleftea (SWE04)","atNorth","Langssele (Solleftea)","Vasternorrland","Sweden",63.178,17.058,power=300,it=240,
    notes="Planned/under development; 300MW mega site on 50ha at Hamre Industrial Park; operational target H1 2028; E.ON signed 200MW grid connection",
    url="https://www.atnorth.com/nordic-data-centers/sweden-data-centers/solleftea-swe04/"),
row("Eclairion Loire-sur-Rhone","Eclairion (HPC Group)","Loire-sur-Rhone / Givors","Auvergne-Rhone-Alpes","France",45.571,4.777,power=350,it=350,
    notes="Planned; EDF selected Eclairion in Jun 2026 to redevelop the former Loire-sur-Rhone coal plant into a 350MW IT AI data centre; feasibility and permitting underway",
    url="https://www.datacenterdynamics.com/en/news/edf-selects-softbank-and-eclairion-to-deliver-ai-data-center-projects-at-former-power-stations-in-france/"),
row("SoftBank Bouchain AI Campus","SoftBank","Bouchain (Valenciennes)","Hauts-de-France","France",50.29,3.315,power=400,it=350,
    notes="Planned; EDF preferred bidder Jun 2026 for a 400MW AI DC at the Bouchain power station site; part of SoftBank's plan for up to 5GW / $75bn of French AI capacity (IT load estimated)",
    url="https://www.datacenterdynamics.com/en/news/edf-selects-softbank-and-eclairion-to-deliver-ai-data-center-projects-at-former-power-stations-in-france/"),
row("Microsoft Aragon (Zaragoza)","Microsoft","Zaragoza","Aragon","Spain",41.618,-0.908,power=400,it=320,
    notes="Under construction; 874,000 sq m campus near Z-40 and Puerto Venecia; Microsoft's first data centres in Aragon, described as new AI datacenters with closed-loop air and liquid-to-chip cooling (capacity estimate)",
    url="https://local.microsoft.com/blog/understanding-microsoft-datacenters-in-aragon/"),
row("Cavour Hyperscale Campus Trino","Techbau / Cavour Hyperscale","Trino","Piedmont","Italy",45.193,8.296,power=400,it=350,
    notes="Planned; EUR 4bn conversion of the former Enel Galileo Ferraris power plant into a 300-400MW AI/cloud campus; declared of national strategic interest 2026; backers claim it could be Europe's largest DC",
    url="https://www.datacenterdynamics.com/en/news/italy-plans-to-build-europes-largest-data-center-in-former-trino-power-plant/"),
row("K2 Strategic Milan (MIL 1)","K2 Strategic Infrastructure (Kuok Group)","Milan (south)","Lombardy","Italy",45.33,9.2,power=300,it=260,
    notes="Planned; ~EUR 5.3bn, ~300MW hyperscale AI campus south of Milan; national strategic interest status 2026; coordinates approximate (IT load estimated)",
    url="https://www.reuters.com/world/asia-pacific/kuok-group-eyes-53-billion-data-center-investment-italy-2026-06-26/"),
# ---------------- AMERICAS ----------------
row("Bell AI Fabric Sherwood Campus","Bell Canada","Regina (RM of Sherwood)","Saskatchewan","Canada",50.393,-104.567,power=300,
    notes="Under construction; announced Mar 2026, four building shells rising Oct 2026; 65ha site on provincial grid; part of Bell AI Fabric national AI network",
    url="https://www.saskatchewan.ca/government/news-and-media/2026/october/01/bell-ai-fabric"),
row("FTL Miramichi Data Centre Campus","Faster Than Light (FTL)","Miramichi","New Brunswick","Canada",47.0298,-65.4704,power=375,
    notes="Announced Oct 2026; 375MW campus with initial 100MW phase; colocation to multiple tenants; AI/HPC-capable but AI use not confirmed; land zoned heavy industrial",
    url="https://www.cbc.ca/news/canada/new-brunswick/miramichi-data-centre-flt-faster-than-light-council-9.7374686"),
row("Spruce Lake Data Centre Hub","Beacon New Brunswick / VoltaGrid","Saint John","New Brunswick","Canada",45.2187,-66.1767,power=390,
    notes="Proposed; US$6bn investment; under 60ha at Spruce Lake Industrial Park; designed for AI and cloud; in federal impact assessment registry",
    url="https://www.sjdatacentre.ca/"),
row("Microsoft Vaughan YTO11","Microsoft","Vaughan","Ontario","Canada",43.7926,-79.6287,power=60,it=48,
    notes="Commissioning H2 2026; shell completed Jul 2026; Azure Canada Central; inference-focused per Microsoft Canada; capacity not published (48MW IT / 60MW utility is a third-party estimate)",
    url="https://datacentersearch.org/sites/microsoft-vaughan-yto11"),
row("Beacon Foothills AI Data Center Hub","Beacon Data Centres","Foothills County","Alberta","Canada",50.5939,-113.8191,power=400,
    notes="Approved; ~US$4bn campus; 400MW AESO interconnection request (P2926); AI-focused data centre hub; land-use approvals Feb 2025",
    url="https://www.westernwheel.ca/local-news/foothills-county-grants-further-approvals-to-4-billion-data-centre-10298053"),
row("RT-One Uberlandia AI Campus","RT-One","Uberlandia","Minas Gerais","Brazil",-18.9186,-48.2772,power=100,it=100,
    notes="Under construction from Sep 2026, first delivery 2026-27; 100MW initial phase, modular expansion to 400MW+; part of R$15bn Brazil programme; liquid-cooled high-density AI/HPC",
    url="https://www.cnnbrasil.com.br/infra/com-alta-demanda-empresa-investira-r-15-bi-em-data-centers-de-ia/"),
row("RT-One Maringa AI Campus","RT-One","Maringa","Parana","Brazil",-23.4205,-51.9331,power=200,it=200,
    notes="Planned; up to 200MW initial capacity, modular expansion beyond 400MW; part of RT-One's R$15bn Latin America AI platform with Uberlandia; permitting behind Uberlandia",
    url="https://www.hitachienergy.com/news-and-events/press-releases/2026/01/en-rt-one-and-hitachi-energy-announce-collaboration-to-enable-latin-america-s-largest-ai-data-center-platform"),
row("Ada Infrastructure GRU10","Ada Infrastructure (Ares Management)","Franco da Rocha","Sao Paulo","Brazil",-23.3217,-46.7269,power=300,it=100,
    notes="Under construction (groundbreaking Jun 2026; online Dec 2027-Jun 2028); two onsite substations totalling 300MW; up to three buildings, 100MW+ computing; hyperscale cloud/AI/GPU; R$2.7bn Brazil investment",
    url="https://adainfrastructure.com/en-US/insights/news/ada-infrastructure-announces-groundbreaking-of-its-first-data-center-campus-in-brazil"),
row("Tecto TGRU1","Tecto Data Centers (V.tal/BTG)","Santana de Parnaiba","Sao Paulo","Brazil",-23.4439,-46.9178,power=200,
    notes="Under construction; designed for up to 200MW; high-density AI and hyperscale workloads; Greater Sao Paulo; part of US$2bn 2026-2028 Tecto expansion",
    url="https://tecto.com/en/data-centers-platform/under-construction/tgru1-en/"),
row("Elea BEL1 Belem","Elea Data Centers","Belem","Para","Brazil",-1.4558,-48.4902,power=7.5,it=7.5,
    notes="Planned; operations Q2 2027; initial 7.5MW expandable to 100MW; first AI-neutral data centre in the Amazon; 100% renewable PPA with AXIA Energia; waterless cooling",
    url="https://eleadatacenters.com/en/2026/06/26/elea-announces-the-amazon-regions-first-ai-data-center-with-power-infrastructure-from-axia-energia/"),
row("AI-GDC Nuevo Leon AI/HPC Center","AI-GDC / Cipre Holding","San Pedro Garza Garcia","Nuevo Leon","Mexico",25.6573,-100.4026,types="NVIDIA (unspecified)",
    notes="Planned; US$1bn initial investment, phased 2026-2030; Nvidia technology and AI-ready design; billed as Mexico's first HPC/AI centre; capacity not published",
    url="https://www.nl.gob.mx/es/boletines/nl-se-va-convertir-en-el-hub-de-inteligencia-artificial-samuel-garcia-anuncia-inversion"),
row("Google Cerrillos Data Center","Google (Dataluna SpA)","Santiago (Cerrillos)","Region Metropolitana","Chile",-33.5027,-70.7156,power=120,
    notes="Planned/approved; US$200m, 23ha, 32,412 sq m, four phases; 44 backup diesel gensets totalling 120.25MW; air-cooled, no water use; SEA ruled Oct 2026 no full EIA; Google says no final build decision (power is backup-generation-based estimate)",
    url="https://www.bnamericas.com/es/reportajes/google-evita-evaluacion-ambiental-para-data-center-de-us200-millones-en-chile"),
row("Ascenty Santiago SCL04/SCL05","Ascenty (Digital Realty/Brookfield)","Quilicura (Santiago)","Region Metropolitana","Chile",-33.3667,-70.7333,power=150,it=150,
    notes="Under development; SCL04 + SCL05 add 150MW combined, online 2027-2028; adjacent to SCL01-03 Quilicura campus; AI-ready, 100% renewable; part of US$1.2bn Chile capex",
    url="https://www.linkedin.com/posts/ascenty_ascenty-datacenter-chile-activity-7367240323464343554-0_TG"),
row("DOMARA Lima AI Data Center","DMR Inmobiliaria (DOMARA) / undisclosed US operator","Lima (Lurin area)","Lima","Peru",-12.275,-76.87,
    notes="Planned, awaiting Peruvian government approval; US$500m AI data centre on 180ha near Lima; linked to a US government/US private operator; capacity not published",
    url="https://www.bnamericas.com/en/interviews/peruvian-developer-eyes-hyperscaler-boom-preps-eight-sites-for-ai"),
# ---------------- MIDDLE EAST / AFRICA / SOUTH ASIA ----------------
row("Microsoft Azure Saudi Arabia East","Microsoft","Dammam","Eastern Province","Saudi Arabia",26.42,50.088,power=100,
    notes="General availability Nov 2026; 3 availability zones; first Microsoft datacenter region in KSA; 100MW is a third-party tracker estimate, not confirmed by Microsoft",
    url="https://news.microsoft.com/source/emea/2026/08/microsoft-announces-saudi-arabia-east-datacenter-region-will-be-available-in-november-2026/"),
row("ZeroPoint DC (NEOM)","NEOM Tech & Digital / EzdiTek","NEOM","Tabuk","Saudi Arabia",28.05,35.25,power=36,it=36,
    notes="Hyperscale campus of 3 data centers, 36MW with expansion room; ~$0.5bn; positioned for cloud/AI ('cognitive technologies'), carrier-neutral subsea gateway; announced Feb 2022",
    url="https://www.prnewswire.com/news-releases/zeropoint-dc-hyperscale-data-center-to-support-ecosystem-of-cognitive-technologies-301472989.html"),
row("Khazna Ankara AI Data Center","Khazna Data Centers (G42)","Ankara","Ankara","Turkey",39.9500,32.7500,power=100,
    notes="Planned/under development; announced Apr 2025 in Baskent Organized Industrial Zone; AI-capable from outset, modular, capacity up to 100MW",
    url="https://khaznadatacenters.com/press-release/g42s-khazna-data-centers-expands-into-turkiye-to-support-countrys-ai-ambitions/"),
row("Ofek Data Center (Ashdod)","Dalia Energy / Serverfarm / Israel Infrastructure Fund","Ashdod","Southern District","Israel",31.7900,34.6400,power=130,
    notes="Planned; completion H2 2029, ~$1.5bn; Israel's largest planned DC; 130MW initial scaling toward 200MW compute, powered by a dedicated 850MW gas plant; Nvidia GPUs planned",
    url="https://www.datacenterdynamics.com/en/news/dalia-energy-plans-israels-biggest-data-center/"),
row("Mubbadrah Salalah AI Data Centre","Mubbadrah Investment consortium (Sustopia Capital, Vela Tech, O2 Global Energy)","Salalah","Dhofar","Oman",17.0151,54.0924,power=400,
    notes="Announced Oct 2026; $3bn initial investment, up to 400MW, purpose-built for hyperscalers and AI training/inference; 400MW solar+battery co-located; Crusoe named as potential off-taker; planned",
    url="https://www.zawya.com/en/economy/oman-mubbadrah-investment-leads-consortium-to-develop-400mw-ai-data-centre-1850092"),
row("Mindstream Jordan Al-Risha Campus","Mindstream Energy (Mindstream Jordan LLC)","Al-Risha","Zarqa","Jordan",32.3000,36.9500,power=400,
    notes="Announced Jul 2026; 245-acre campus targeting up to 400MW phased sovereign AI/HPC capacity, integrated on-site natural gas generation and modular AI data centers; planned",
    url="https://www.prnewswire.com/news-releases/mindstream-energy-dba-mindstream-jordan-llc-targets-400-mw-sovereign-ai-infrastructure-platform-in-jordan-to-serve-growing-regional-compute-demand-302821924.html"),
row("Prieska Off-Grid AI Campus","Terranum / Prieska Power Reserve","Prieska","Northern Cape","South Africa",-29.6667,22.7333,power=100,
    notes="Planned; announced Mar 2026, 100MW initial phase expandable to 500MW, fully off-grid 100% renewable (co-located wind+solar), targeting hyperscale AI demand from 2029",
    url="https://programminginsider.com/felix-huettenbach-and-terranum-advance-plans-for-africas-largest-off-grid-data-center-campus-in-prieska-south-africa/"),
row("Teraco CT2 Cape Town","Teraco (a Digital Realty company)","Cape Town","Western Cape","South Africa",-33.8750,18.7000,power=50,it=50,
    notes="Operational; CT2 expansion completed Nov 2025 adding 32MW across 8 halls, taking the facility to 50MW critical IT load; marketed for cloud and next-gen AI workloads",
    url="https://www.teraco.co.za/news/teraco-completes-ct2-data-centre-expansion/"),
row("iXAfrica NBOX1 Nairobi","iXAfrica Data Centres","Nairobi","Nairobi County","Kenya",-1.3500,36.8800,power=30,it=22.5,
    notes="East Africa's largest hyperscale/AI-ready campus on Mombasa Road, 4.3 acres, 2 buildings; NBOX1.1 4.5MW IT live Feb 2025; NBOX1.2 18MW IT planned; liquid-cooling capable",
    url="https://ixafrica.co.ke/campus-specs/"),
row("STT GDC Palava Campus","ST Telemedia Global Data Centres India","Mumbai (Palava)","Maharashtra","India",19.1600,73.1000,it=400,
    notes="Under construction; groundbreaking Mar 2026 on 46-acre campus designed to ~400MW IT load, first phase 50MW IT; Rs 5,000 crore investment; Palava City between Thane and Navi Mumbai",
    url="https://www.datacenterdynamics.com/en/news/stt-gdc-breaks-ground-on-third-data-center-campus-in-mumbai-india/"),
row("Princeton Digital Group MU1","Princeton Digital Group","Navi Mumbai (Airoli)","Maharashtra","India",19.172654,72.992812,it=150,
    notes="Operational; 150MW IT campus across 5 buildings on 50 acres, 220kV substation, Tier III, IGBC Platinum, India's first OCP-Ready facility",
    url="https://princetondg.com/wp-content/uploads/2024/07/MU1_Factsheet-Updated_Digital.pdf"),
row("CtrlS Future City Campus","CtrlS Datacenters","Hyderabad (Bharat Future City)","Telangana","India",17.1000,78.3500,power=750,
    notes="Planned; 36-acre campus stated up to 750MW scalable to 1.2GW, 400kV GIS with 700MVA sanctioned power, 100% green; no commissioning schedule published (press reports cite 2GW, conflicting)",
    url="https://www.ctrls.com/datacenter-hyderabad/"),
row("AdaniConneX Noida Campus","AdaniConneX (Adani Enterprises / EdgeConneX)","Noida","Uttar Pradesh","India",28.6270,77.3640,it=150,
    notes="Operational/expanding; Sector 62 campus with 150MW IT potential, Phase 1 live Jan 2025; Google leased 464,460 sq ft on a 10-year term; current operating capacity ~35MW",
    url="https://www.adaniconnex.com/data-centers"),
row("Digital Connexion MAA10 Chennai","Digital Connexion (Digital Realty / Brookfield / MUFG)","Chennai (Ambattur)","Tamil Nadu","India",13.0985,80.1420,power=100,it=20,
    notes="Under development; MAA10 first building on a planned 100MW campus at Ambattur Industrial Estate; building total power 20MW, data halls 2.2-4.4MW, N+2 cooling, IGBC Platinum",
    url="https://digitalconnexion.com/india/maa10"),
row("ADIC Kaliakair Frontier AI Campus","ADIC (UK)","Kaliakair (Gazipur)","Dhaka","Bangladesh",24.0500,90.2200,power=200,
    notes="Proposed Jul 2026; ~$2bn FDI, 'Frontier AI Data Centre and Quantum-Ready Sovereign Compute Campus'; phase 1 30-50MW in 24 months, then 100-200MW; 100MW captive power plant proposed; not yet approved",
    url="https://theclimatewatch.com/uk-firm-proposes-2bn-investment-in-bangladesh-ai-data-centre-plan/"),
]

DROP = {
    "Start Campus Sines",          # existing 'Start Campus SINES Data Campus'
    "Nscale Keflavik",             # existing
    "ODATA DC QR03",               # existing 'Tecto DC QR03 (former ODATA)'
    "Khazna Ajman AI Data Center", # existing 'Khazna QAJ1 Ajman AI Data Center'
}

existing = list(csv.DictReader(open(CANON, encoding="utf-8")))
# normalize country naming
for r in existing:
    if r["country"] == "UAE":
        r["country"] = "United Arab Emirates"

names = {r["name"] for r in existing}
added = 0
for r in ROWS:
    if r["name"] in names or r["name"] in DROP:
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

from collections import Counter
c = Counter(r["country"] for r in ROWS if r["name"] not in DROP)
print(f"Added {added} rows. By country: {dict(sorted(c.items()))}")
print(f"Total rows now: {len(existing)}")
