"""
Build final dataset (data/published/data_centers.csv + .json + index.html)
from data/canonical/data_centers.csv.

H100e methodology (documented in README.md):
- h100e_gpu:     converted from announced GPU counts using dense-FP8 compute ratios vs H100
- h100e_third_party: third-party estimates (e.g. Epoch AI) recorded during research
- h100e_flops:   announced cluster peak PFLOPS (dense FP8-equivalent) / 1.979 PFLOPS per H100
- h100e_power:   power-based estimate: 60% of IT load assumed to power H100-class
                 accelerator systems at ~1.2 kW per GPU  =>  500 H100e per MW of IT load
- h100e_best:    most confident available estimate (gpu > third_party > flops > power)
"""
import csv, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
PUBLISHED = os.path.join(ROOT, "data", "published")
OUT_CSV = os.path.join(PUBLISHED, "data_centers.csv")
OUT_JSON = os.path.join(PUBLISHED, "data_centers.json")
OUT_HTML = os.path.join(ROOT, "index.html")
os.makedirs(PUBLISHED, exist_ok=True)

COLS = ["name","operator","city","state_province","country","latitude","longitude",
        "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
        "cluster_peak_pflops","h100e_gpu","h100e_third_party","notes","source_url"]
NUMERIC = {"latitude","longitude","power_capacity_mw","it_load_mw","announced_gpu_count",
           "cluster_peak_pflops","h100e_gpu","h100e_third_party"}

def num(s):
    s = (s or "").strip()
    if not s:
        return None
    return float(s)

def clean_cell(col, s):
    s = (s or "").strip()
    if col in NUMERIC and s:
        try:
            f = float(s)
        except ValueError:
            raise SystemExit(f"Non-numeric value in {col!r}: {s!r} in row for {rows[i]['name'] if rows else '?'}")
    return s

rows = list(csv.DictReader(open(RAW, encoding="utf-8")))
print(f"Parsed {len(rows)} rows from raw CSV")

# ---- build status (based on research notes) ----
STATUS = {
    # --- fully operational ---
    "Fairwater Atlanta": "operational",
    "Microsoft Boydton (Azure East US)": "operational",
    "Microsoft West Des Moines": "operational",
    "Microsoft Quincy": "operational",
    "Microsoft San Antonio": "operational",
    "Microsoft Chicago metro": "operational",
    "Microsoft Dublin (Grange Castle)": "operational",
    "Google The Dalles": "operational",
    "Google Council Bluffs": "operational",
    "Google Pryor (Mayes County)": "operational",
    "Google Loudoun County (Ashburn)": "operational",
    "Google Lenoir": "operational",
    "AWS US East (N. Virginia)": "operational",
    "AWS New Albany": "operational",
    "Meta Prineville": "operational",
    "Meta Altoona": "operational",
    "Meta Fort Worth": "operational",
    "Meta Huntsville": "operational",
    "xAI Colossus 1": "operational",
    "xAI QTS Atlanta": "operational",
    "CoreWeave Denton (Core Scientific)": "operational",
    "CoreWeave Plano": "operational",
    "CoreWeave Chicago (ORD1)": "operational",
    "CoreWeave Las Vegas": "operational",
    "CoreWeave Austin (Core Scientific)": "operational",
    "Nebius Kansas City": "operational",
    "IREN Childress": "operational",
    "Tesla Cortex (Giga Texas)": "operational",
    "QScale Q01 Campus": "operational",
    "Mistral Compute - Essonne (MDA)": "operational",
    "Nebius Mantsala": "operational",
    "Deutsche Telekom Industrial AI Cloud": "operational",
    "AWS Aragon AI Campus": "operational",
    "Alibaba Zhangbei": "operational",
    "Huawei Wuhu": "operational",
    "Huawei Horinger": "operational",
    "China Mobile Hohhot Intelligent Computing Center": "operational",
    "iFlytek Feixing Intelligent Computing Platform": "operational",
    "SoftBank DGX SuperPOD Tokyo": "operational",
    "Foxconn Kaohsiung AI Factory": "operational",
    "Yotta NM1 Navi Mumbai": "operational",
    "DayOne Nusajaya": "operational",
    "DayOne Kempas": "operational",
    "YTL Green Data Center Park Kulai": "operational",
    "AirTrunk SYD1 Sydney West": "operational",
    "Cassava AI Factory Johannesburg": "operational",
    # --- partially operational (first phase(s) live, campus still ramping) ---
    "Fairwater AI Datacenter (Mount Pleasant)": "partially_operational",
    "AWS Project Rainier (New Carlisle)": "partially_operational",
    "AWS Boardman (Columbia Basin)": "partially_operational",
    "AWS Madison County (Canton & Ridgeland)": "partially_operational",
    "Meta Prometheus (New Albany)": "partially_operational",
    "Stargate Abilene (Lancium Clean Campus)": "partially_operational",
    "xAI Colossus 2": "partially_operational",
    "Galaxy Helios (CoreWeave West Texas)": "partially_operational",
    "Nebius Vineland (DataOne campus)": "partially_operational",
    "TeraWulf Lake Mariner": "partially_operational",
    "Cipher Barber Lake (Barbour County)": "partially_operational",
    "Applied Digital Polaris Forge 1": "partially_operational",
    # --- under construction ---
    "AWS Falls Township (Keystone)": "under_construction",
    "Meta Hyperion (Richland Parish)": "under_construction",
    "Meta Jeffersonville": "under_construction",
    "Stargate Port Washington (Lighthouse)": "under_construction",
    "Stargate Shackelford County": "under_construction",
    "Stargate Milam County": "under_construction",
    "Stargate Saline Township (The Barn)": "under_construction",
    "Stargate Lordstown": "under_construction",
    "Project Jupiter (Stargate Dona Ana County)": "under_construction",
    "CoreWeave Lancaster": "under_construction",
    "TeraWulf Abernathy": "under_construction",
    "Applied Digital Polaris Forge 2": "under_construction",
    "IREN Sweetwater Hub (Sweetwater 1 & 2)": "under_construction",
    "Nscale Loughton AI Campus": "under_construction",
    "Stargate Norway - Kvandal": "under_construction",
    "IPAI Heilbronn": "under_construction",
    "Nebius Lappeenranta AI Factory": "under_construction",
    "Stargate UAE": "under_construction",
    "HUMAIN Riyadh": "under_construction",
    "HUMAIN Dammam": "under_construction",
    "DataVolt Oxagon AI Campus": "under_construction",
    "SK-AWS Ulsan AI Data Center": "under_construction",
    "Reliance Jamnagar AI Data Center": "under_construction",
    "Viettel Tan Phu Trung Data Center": "under_construction",
    # --- planned / announced (not yet started construction) ---
    "Google West Memphis": "under_construction",
    "AWS Salem Township (Susquehanna)": "planned",
    "Crusoe Abilene II (Microsoft campus)": "planned",
    "TeraWulf Lake Hawkeye (Cayuga site)": "planned",
    "Hut 8 River Bend": "planned",
    "Lambda DFW-04 (Aligned)": "planned",
    "Campus AI (Mistral Paris AI Campus)": "planned",
    "Stargate UK - Cobalt Park": "planned",
    "Schwarz Group / Deutsche Telekom AI Gigafactory": "planned",
    "Schwarz Digits AI Data Centre Lubbenau": "planned",
    "Nebius Lille AI Factory": "planned",
    "Sesterce AI Campus Jamsa": "planned",
    # --- CHINA deep-dive additions ---
    "VNET Bayin Ulanqab Computing Center": "partially_operational",
    "Envision Galaxy Campus Ulanqab": "partially_operational",
    "Alibaba Ulanqab Data Center": "operational",
    "Alibaba Heyuan (Yuancheng) Data Center": "operational",
    "Volcano Engine Horinger Computing Center (Phase 1)": "under_construction",
    "Kuaishou Smart Cloud Data Center Ulanqab": "operational",
    "CICC Data Ulanqab Zero-Carbon Computing Base": "operational",
    "Tencent Tianjin Data Center": "operational",
    "Tencent Qingyuan Cloud Computing Data Center": "operational",
    "Tencent Gui'an Qixing Data Center": "operational",
    "Baidu Cloud Computing (Yangquan) Center": "operational",
    "China Telecom Lingang Intelligent Computing Valley": "operational",
    "SenseTime Shanghai Lingang AIDC": "operational",
    "China Mobile Intelligent Computing Center (Harbin)": "operational",
    "China Telecom Qingyang Intelligent Computing Center": "under_construction",
    "China Mobile (Gansu Qingyang) Data Center": "operational",
    "Huawei Cloud Gui'an Data Center (Qixing Lake)": "operational",
    "China Telecom Cloud Computing Guizhou Information Park": "operational",
    "CCCC Zhongjiao Zhishugu (Zhongwei) Industrial Park": "operational",
    "China Telecom Zhongwei Computing Hub Data Center": "operational",
    "Chengdu Intelligent Computing Center": "operational",
    "Wuhan Artificial Intelligence Computing Center": "operational",
    "China Unicom Hohhot Intelligent Computing Center": "operational",
    "ByteDance AI Data Center (Guangling County, Datong)": "under_construction",
    # --- MALAYSIA deep-dive additions ---
    "Bridge Data Centres MY06": "partially_operational",
    "Bridge Data Centres MY07": "under_construction",
    "Bridge Data Centres Cyberjaya (MY01 & MY02)": "operational",
    "Bridge Data Centres MY03": "operational",
    "Microsoft Malaysia West": "operational",
    "AWS Asia Pacific (Malaysia) Region": "operational",
    "Google Data Center & Cloud Region (Elmina Business Park)": "under_construction",
    "Oracle Malaysia West 2 (ap-kulai-2)": "operational",
    "Princeton Digital Group JH1": "partially_operational",
    "AirTrunk JHB1": "operational",
    "AirTrunk JHB2": "under_construction",
    "Vantage KUL1 (Cyberjaya I)": "operational",
    "Vantage KUL2 (Cyberjaya II)": "under_construction",
    "Vantage JHB1 (ex-Yondr)": "under_construction",
    "STT Johor 1": "under_construction",
    "STACK JHB01": "under_construction",
    "ZDATA GP3": "under_construction",
    "NTT JHB10": "under_construction",
    "K2 Strategic JHR01-03": "operational",
    "Basis Bay Cyberjaya DC2": "operational",
    "Digital Cosmos Cyberjaya": "planned",
    "FutureData Data Center Park Kuching": "planned",
    # --- JAPAN additions ---
    "SoftBank Hokkaido Tomakomai AI Data Center": "under_construction",
    "SoftBank Osaka Sakai AI Data Center": "under_construction",
    "KDDI TELEHOUSE Osaka Sakai": "operational",
    "AIST ABCI 3.0": "operational",
    "AIST ABCI-Q (G-QuAT)": "operational",
    "Sakura Internet Ishikari Data Center (High-Power GPU Cloud)": "operational",
    "Ishikari Renewable Energy Data Center No.1": "operational",
    "AirTrunk TOK1 (Tokyo East)": "operational",
    "AirTrunk TOK2 (Tokyo West)": "under_construction",
    "AirTrunk OSK2 (Osaka East)": "planned",
    "Google Inzai Data Center": "operational",
    "Goodman Tsukuba Campus": "under_construction",
    "MC Digital Realty NRT14 (Inzai Campus)": "operational",
    "TSUBAME4.0": "operational",
    "ai& Tokyo AI Data Center": "planned",
    # --- SOUTH KOREA additions ---
    "SK Broadband Gasan AI Data Center": "operational",
    "Naver Data Center GAK Chuncheon": "operational",
    "Naver Data Center GAK Sejong": "partially_operational",
    "National AI Computing Center (Koark)": "under_construction",
    "Samsung SDS Gumi AI Data Center": "planned",
    "NHN Cloud Gwangju National AI Data Center": "operational",
    "Kakao Data Center Ansan": "operational",
    "LG Uplus Paju AIDC": "under_construction",
    "GS AI Infrastructure Donghae AI Data Center Campus": "planned",
    "LG AI Research AEX cluster (LG Science Park)": "operational",
    "AWS Incheon AI Data Center": "under_construction",
    "KISTI National Supercomputing Center (HANGANG No.6)": "operational",
    # --- EUROPE deep-dive additions ---
    "Google Waltham Cross (UK AI compute)": "operational",
    "CoreWeave Crawley (Digital Realty LGW15/16)": "operational",
    "CoreWeave London Docklands (Global Switch)": "operational",
    "CoreWeave Scotland (DataVita Fortis)": "operational",
    "Vantage CWL1 Newport (South Wales AI Growth Zone)": "operational",
    "Vantage Bridgend Campus": "planned",
    "Microsoft Acton (UK South expansion)": "under_construction",
    "JUPITER / JAIF (Exascale AI Factory)": "operational",
    "HammerHAI (HLRS AI Factory)": "operational",
    "Blue Swan Bavaria AI Gigafactory (candidate)": "planned",
    "Alice Recoque (AI2F / TGCC)": "under_construction",
    "EcoDataCenter 2 (Kvarnsveden)": "under_construction",
    "CoreWeave Norway (Ovrebo)": "operational",
    "Microsoft Narvik (Norway AI expansion)": "planned",
    "Nscale Keflavik": "operational",
    "MIMER (Sweden AI Factory)": "under_construction",
    "NLAIF (Dutch AI Factory)": "planned",
    "Start Campus SINES Data Campus": "partially_operational",
    "BSC AI Factory Barcelona (MareNostrum)": "operational",
    "Fastweb NeXXt AI Factory": "operational",
    "Domyn Colosseum (iGenius AI Factory)": "operational",
    "Leonardo / IT4LIA AI Factory (CINECA)": "operational",
    "Gaia AI Factory": "under_construction",
    "PIAST AI Factory": "under_construction",
    "Pharos / DAEDALUS AI Factory": "operational",
    "Swiss AI Platform": "operational",
    # --- MIDDLE EAST deep-dive additions ---
    "Khazna QAJ1 Ajman AI Data Center": "under_construction",
    "Khazna AUH8 Masdar City": "under_construction",
    "Khazna AUH4 Mafraq": "under_construction",
    "Microsoft-G42 200MW UAE Expansion (via Khazna)": "under_construction",
    "Moro Hub Green Data Centre (MBR Solar Park)": "operational",
    "Moro Hub Warsan Green Data Centre": "under_construction",
    "Core42 Abu Dhabi Sovereign AI Cluster (DGX SuperPOD)": "operational",
    "HUMAIN-AWS AI Zone Riyadh": "planned",
    "HUMAIN-xAI Compute Campus Riyadh": "under_construction",
    "SDAIA Sovereign AI Factory": "under_construction",
    "SDAIA Hexagon Data Center": "under_construction",
    "Shaheen III Supercomputer (KAUST)": "operational",
    "DataVolt Riyadh AI Data Center (MODON)": "planned",
    "Alibaba Cloud Riyadh Region (SCCC)": "operational",
    "Ooredoo Sovereign AI Cloud Qatar": "operational",
    "Nebius AI Cloud Modi'in (Mega Or)": "operational",
    "Nebius-Mega Or AI Data Center Beit Shemesh": "under_construction",
    "NVIDIA Israel-1 AI Supercomputer": "operational",
    "AWS Middle East (Bahrain) Region": "operational",
    # --- LATIN AMERICA additions ---
    "Scala AI City": "planned",
    "Scala Tambore Campus": "operational",
    "Ascenty Vinhedo AI Campus": "partially_operational",
    "TikTok/ByteDance Pecem Data Center": "under_construction",
    "Elea Rio AI City": "planned",
    "Tecto DC QR03 (former ODATA)": "partially_operational",
    "CloudHQ Queretaro Campus": "under_construction",
    "KIO QRO3": "under_construction",
    "Microsoft Mexico Central (Queretaro region)": "operational",
    "Coatlicue Supercomputer": "planned",
    "Google Quilicura Data Center": "operational",
    "Google Canelones Data Center (Project Teros)": "under_construction",
    "Antel AI Data Center": "planned",
    "Stargate Argentina (OpenAI x Sur Energy)": "planned",
    "Crusoe-Araico Itaipu AI Data Center": "planned",
    # --- CANADA deep-dive additions ---
    "CoreWeave Cambridge AI Data Centre": "operational",
    "eStruxture CAL-3": "under_construction",
    "Meta Sturgeon Data Centre": "under_construction",
    "TELUS Sovereign AI Factory Rimouski": "operational",
    "TELUS Kamloops AI Factory": "under_construction",
    "TELUS Vancouver M3 AI Factory": "under_construction",
    "TELUS Vancouver 150 West Georgia AI Factory": "planned",
    "Bell AI Fabric Merritt (BUZZ HPC)": "partially_operational",
    "Rorqual (Calcul Quebec national DC)": "operational",
    "TamIA (PAICE)": "operational",
    "Killarney (PAICE)": "operational",
    "Vulcan (PAICE)": "operational",
    "Vantage Quebec City Campus (QC24)": "partially_operational",
    "Wonder Valley AI Data Centre Park": "planned",
    # --- MEXICO additions + CENTRAL AMERICA / CARIBBEAN ---
    "AWS Mexico (Central) Region": "operational",
    "Google Cloud Mexico Region": "operational",
    "Oracle Cloud Mexico Central": "operational",
    "Oracle Cloud Mexico Northeast": "operational",
    "Alibaba Cloud Mexico Region": "operational",
    "Ascenty Queretaro Campus (QRO1-QRO3)": "partially_operational",
    "ODATA (Aligned) QR01": "operational",
    "ODATA (Aligned) QR02": "operational",
    "ODATA (Aligned) QR04": "partially_operational",
    "ODATA (Aligned) MEX01 (Mexico City)": "operational",
    "Layer 9 GTO-01 (Project Falcon)": "under_construction",
    "Bleeding Edge QRO1 (AI Factory)": "operational",
    "Digital Realty Queretaro Campus (MEX01-MEX03)": "operational",
    "Scala Tepotzotlan Campus": "operational",
    "KIO Queretaro Campus (QRO1/QRO2 + new DC)": "operational",
    "KIO Monterrey Campus (MTY)": "operational",
    "Huawei Cloud Mexico-1": "operational",
    "Latam Data Centers Next AI (Aurum AI Data Center)": "planned",
    "Quantum AI Free Zone Campus (Quantum FZ)": "planned",
    "El Salvador National AI Lab (Sovereign AI)": "operational",
    "Trinidad & Tobago AI Data Centers (EY 300MW / Hummingbird 150MW MoUs)": "planned",
    # --- AFRICA deep-dive additions ---
    "Teraco Isando Campus (JB1/JB3/JB5)": "operational",
    "Teraco JB4 Bredell": "operational",
    "Vantage Data Centers Waterfall City": "planned",
    "Equinix Cape Town Airport Data Centre 1 & 2": "planned",
    "Cosmas Data City Cape Town Campus": "planned",
    "Microsoft Azure South Africa Regions (Johannesburg & Cape Town)": "operational",
    "Oracle Cloud Johannesburg Region": "operational",
    "AWS Africa (Cape Town) Region": "operational",
    "G42 / Microsoft East Africa Cloud Region (Olkaria)": "planned",
    "Rack Centre LGS2": "operational",
    "Kasi Cloud LOS1 (Lekki Campus)": "partially_operational",
    "AFRIDATA Nigeria (Lagos + Delta)": "planned",
    "ADC Egypt / Egypt Sovereign AI Data Centre": "planned",
    "Nexus AI Factory": "planned",
    "Wingu Africa Addis Ababa Data Centre (EAII AI partnership)": "operational",
    # --- EASTERN EUROPE / CAUCASUS / CENTRAL ASIA additions ---
    "Baltic AI GigaFactory (bid)": "planned",
    "Atman Data Center Warsaw-3 (WAW-3)": "partially_operational",
    "Microsoft Cloud Region Poland (Mazovia expansion)": "operational",
    "KarolAIna Supercomputer (Czech AI Factory CZAI)": "planned",
    "RO AI Factory Supercomputer": "planned",
    "BRAIN++ / Discoverer++ AI Supercomputer": "planned",
    "LitAI Factory Supercomputer": "planned",
    "SLAIF Next-Gen AI Supercomputer (Vega successor)": "planned",
    "LEVENTE Supercomputer": "planned",
    "Serbian National AI Platform (SAIFA host)": "operational",
    "Ukraine State AI Factory": "planned",
    "Google Cloud & Turkcell Hyperscale Region (Turkiye)": "under_construction",
    "ARF / ARF-ACC (TRUBA National Supercomputing)": "operational",
    "Firebird AI Data Center Hrazdan": "under_construction",
    "AzInTelecom Supercomputer Center": "operational",
    "Alem.cloud National AI Supercomputer (Alem.AI)": "operational",
    "Data Center Valley Ekibastuz": "planned",
    "DataVolt TAS-1 (Tashkent IT Park DC)": "under_construction",
    # --- INDIA & SOUTH ASIA additions ---
    "IndiaAI Compute Platform (National GPU Pool)": "operational",
    "Yotta D2 Greater Noida": "under_construction",
    "Yotta D1 Greater Noida": "operational",
    "Yotta NM2 Navi Mumbai": "under_construction",
    "L&T Vyoma SPD1 (Sriperumbudur AI Campus)": "partially_operational",
    "E2E Networks TIR AI DC Chennai (at L&T Vyoma)": "operational",
    "NxtGen AI Factory Bengaluru": "operational",
    "STT Noida 2 (Neysa AI Deployment)": "under_construction",
    "NTT DATA-Neysa Hyderabad AI DC Cluster": "planned",
    "Google-AdaniConneX Visakhapatnam AI Hub": "under_construction",
    "Digital Connexion Visakhapatnam AI-Native Campus": "planned",
    "HyperVault AI Data Center Hyderabad": "planned",
    "Microsoft India South Central Region (Hyderabad)": "operational",
    "AWS Asia Pacific (Hyderabad) Expansion": "operational",
    "Sify Noida 02 AI-Ready Hyperscale Campus": "operational",
    "Sify Rabale (Mumbai 03) Hyperscale AI Campus": "partially_operational",
    "CtrlS Chandan Valley AI Campus": "planned",
    "Anant Raj Manesar AI Cloud DC": "partially_operational",
    "Data Vault Pakistan AI Data Center": "operational",
    "Sky47 Karakorum-01": "operational",
    "Summit Group Data Centre (Planned)": "planned",
    # --- US deep-dive additions (hyperscaler TPU fleets, neoclouds, crypto-to-AI) ---
    "Nscale Ward County (Barstow)": "operational",
    "Hut 8 Beacon Point": "under_construction",
    "Riot Rockdale": "partially_operational",
    "Riot Corsicana": "under_construction",
    "Crusoe Goodnight (Project Llano)": "under_construction",
    "Google Haskell County (Homebound/Thelma)": "planned",
    "Google Wilbarger County": "under_construction",
    "Google Pampa": "planned",
    "Cipher Black Pearl": "under_construction",
    "Cipher Apollo": "planned",
    "Core Scientific Pecos (future colocation)": "planned",
    "MARA Granbury": "partially_operational",
    "MARA Matagorda County": "planned",
    "Bitdeer Milam County": "planned",
    "Google Midlothian": "operational",
    "Google Columbus": "operational",
    "Google New Albany": "operational",
    "Google Lancaster": "operational",
    "Vultr Springfield AI Supercluster": "under_construction",
    "Bitdeer Clarington": "under_construction",
    "Google Mesa": "operational",
    "Microsoft Goodyear": "operational",
    "Google Omaha": "operational",
    "Google Lincoln": "operational",
    "Google Papillion": "operational",
    "Google Kansas City East": "operational",
    "Microsoft Project Osmium": "under_construction",
    "Meta Rosemount": "under_construction",
    "Meta Kuna": "under_construction",
    "Meta Eagle Mountain": "operational",
    "Meta Cheyenne": "under_construction",
    "Crusoe Project Jade": "planned",
    "Meta Los Lunas": "operational",
    "Meta Montgomery": "under_construction",
    "Meta Temple": "under_construction",
    "Meta-QTS Hillsboro 2": "operational",
    "Google Bristow": "operational",
    "QTS Richmond (Sandston)": "partially_operational",
    "CoreWeave Chester": "under_construction",
    "AWS Ridgeland": "operational",
    "AWS Berwick": "under_construction",
    "Bitfarms Panther Creek": "under_construction",
    "Nscale Madison County": "under_construction",
    "Core Scientific Marble": "under_construction",
    "Core Scientific Dalton": "under_construction",
    "Core Scientific Muskogee": "under_construction",
    "Applied Digital Polaris Forge 3": "planned",
    "Google Storey County": "operational",
    "Google Cedar Rapids (Big Cedar)": "under_construction",
    "Google Fort Wayne": "under_construction",
    "Meta Bowling Green": "planned",
    "Meta El Paso": "planned",
    "Microsoft Pecos": "planned",
    "QTS Cedar Rapids (Big Cedar)": "under_construction",
    "QTS Eagle Mountain": "planned",
    "AWS Richmond County": "planned",
    "AWS Georgia (Butts & Douglas Counties)": "under_construction",
    "AWS Dobbins Campus (Laveen)": "planned",
    "Vantage VA4 (Fredericksburg)": "under_construction",
    "Switch Citadel (Tahoe Reno Campus)": "operational",
    "CloudBurst San Marcos Gigacenter": "under_construction",
    "CloudBurst Oklahoma City Campus": "planned",
    "Fermi America HyperGrid (Project Matador)": "planned",
    # --- country-by-country sweep: APAC ---
    "AirTrunk SYD3 Sydney West": "operational",
    "AirTrunk SYD2 Sydney North": "operational",
    "AirTrunk MEL1 Melbourne": "operational",
    "AirTrunk MEL2 Melbourne": "under_construction",
    "NEXTDC M3 Melbourne": "operational",
    "CDC Marsden Park Data Centre": "under_construction",
    "Firmus Southgate Melbourne": "operational",
    "AWS Asia Pacific (Sydney) Region": "operational",
    "Datagrid New Zealand AI Factory": "under_construction",
    "AirTrunk Singapore SGP1/SGP2": "partially_operational",
    "Nxera DC Tuas": "operational",
    "Oracle Indonesia North (Batam)": "operational",
    "Princeton Digital Group BT1 Batam": "under_construction",
    "STT Bangkok Campus (BKK1/BKK2)": "under_construction",
    "Google Chonburi Data Center": "under_construction",
    "VITRO Santa Rosa Data Center": "operational",
    "FPT AI Factory": "operational",
    "Google Changhua Data Center": "operational",
    # --- country-by-country sweep: Western Europe / Nordics ---
    "Meta Clonee": "operational",
    "AWS Dublin Cruiserath Campus": "operational",
    "Google Eemshaven": "operational",
    "Microsoft Middenmeer": "operational",
    "Google Saint-Ghislain": "operational",
    "Meta Odense": "operational",
    "Google Fredericia": "operational",
    "CA DataCenter Skive": "under_construction",
    "Meta Lulea": "operational",
    "Microsoft Sweden (Sandviken/Gavle)": "operational",
    "atNorth Solleftea (SWE04)": "planned",
    "Eclairion Loire-sur-Rhone": "planned",
    "SoftBank Bouchain AI Campus": "planned",
    "Microsoft Aragon (Zaragoza)": "under_construction",
    "Cavour Hyperscale Campus Trino": "planned",
    "K2 Strategic Milan (MIL 1)": "planned",
    # --- country-by-country sweep: Americas ---
    "Bell AI Fabric Sherwood Campus": "under_construction",
    "FTL Miramichi Data Centre Campus": "planned",
    "Spruce Lake Data Centre Hub": "planned",
    "Microsoft Vaughan YTO11": "under_construction",
    "Beacon Foothills AI Data Center Hub": "planned",
    "RT-One Uberlandia AI Campus": "under_construction",
    "RT-One Maringa AI Campus": "planned",
    "Ada Infrastructure GRU10": "under_construction",
    "Tecto TGRU1": "under_construction",
    "Elea BEL1 Belem": "planned",
    "AI-GDC Nuevo Leon AI/HPC Center": "planned",
    "Google Cerrillos Data Center": "planned",
    "Ascenty Santiago SCL04/SCL05": "under_construction",
    "DOMARA Lima AI Data Center": "planned",
    # --- country-by-country sweep: Middle East / Africa / South Asia ---
    "Microsoft Azure Saudi Arabia East": "operational",
    "ZeroPoint DC (NEOM)": "operational",
    "Khazna Ankara AI Data Center": "planned",
    "Ofek Data Center (Ashdod)": "planned",
    "Mubbadrah Salalah AI Data Centre": "planned",
    "Mindstream Jordan Al-Risha Campus": "planned",
    "Prieska Off-Grid AI Campus": "planned",
    "Teraco CT2 Cape Town": "operational",
    "iXAfrica NBOX1 Nairobi": "partially_operational",
    "STT GDC Palava Campus": "under_construction",
    "Princeton Digital Group MU1": "operational",
    "CtrlS Future City Campus": "planned",
    "AdaniConneX Noida Campus": "partially_operational",
    "Digital Connexion MAA10 Chennai": "under_construction",
    "ADIC Kaliakair Frontier AI Campus": "planned",
}

# ---- validation ----
for i, r in enumerate(rows):
    if set(r.keys()) != set(COLS):
        raise SystemExit(f"Row {i+2} ({r.get('name','?')}) has bad columns: {list(r.keys())}")
    for c in NUMERIC:
        v = (r[c] or "").strip()
        if v:
            try:
                float(v)
            except ValueError:
                raise SystemExit(f"Row {i+2} ({r['name']}): non-numeric {c}={v!r}")
    if not r["source_url"].startswith("http"):
        raise SystemExit(f"Row {i+2} ({r['name']}): source_url missing -> column misalignment? got {r['source_url']!r}")
    if not r["name"]:
        raise SystemExit(f"Row {i+2}: missing name")
    if (r["latitude"] == "" or r["longitude"] == "") and r["name"]:
        print(f"  WARN: no coordinates: {r['name']}")

# ---- derived H100e columns ----
out = []
for r in rows:
    power = num(r["power_capacity_mw"])
    it = num(r["it_load_mw"])
    gpu_count = num(r["announced_gpu_count"])
    pflops = num(r["cluster_peak_pflops"])
    h_gpu = num(r["h100e_gpu"])
    h_3p = num(r["h100e_third_party"])

    # effective IT load: measured if available, else assume PUE 1.2 from gross capacity
    it_effective = it if it is not None else (power / 1.2 if power else None)
    h_power = round(it_effective * 500) if it_effective else None
    h_flops = round(pflops / 1.979) if pflops else None

    candidates = [("gpu_count", h_gpu), ("third_party", h_3p), ("flops", h_flops), ("power", h_power)]
    h_best, h_method = next(((v, m) for m, v in candidates if v), (None, ""))

    status = STATUS.get(r["name"], "unknown")
    out.append({
        "name": r["name"], "operator": r["operator"], "city": r["city"],
        "state_province": r["state_province"], "country": r["country"],
        "latitude": num(r["latitude"]), "longitude": num(r["longitude"]),
        "power_capacity_mw": power, "it_load_mw": it,
        "announced_gpu_count": gpu_count, "gpu_types": r["gpu_types"],
        "cluster_peak_pflops": pflops,
        "h100e_gpu": h_gpu, "h100e_third_party": h_3p,
        "h100e_flops": h_flops, "h100e_power": h_power,
        "h100e_best": h_best, "h100e_method": h_method,
        "status": status, "status_note": r["notes"], "source_url": r["source_url"],
    })

out.sort(key=lambda x: x["h100e_best"] or 0, reverse=True)

final_cols = ["name","operator","city","state_province","country","latitude","longitude",
              "power_capacity_mw","it_load_mw","announced_gpu_count","gpu_types",
              "cluster_peak_pflops","h100e_gpu","h100e_third_party","h100e_flops",
              "h100e_power","h100e_best","h100e_method","status","status_note","source_url"]

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=final_cols)
    w.writeheader()
    w.writerows(out)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

# ---- index.html (self-contained interactive dashboard) ----
FRONTEND = os.path.join(ROOT, "pipeline", "frontend")
with open(os.path.join(ROOT, "data", "operator_efficiency.csv"), encoding="utf-8") as f:
    operators = list(csv.DictReader(f))

# Numeric chart fields are derived at build time; the original disclosure strings
# remain intact so ranges, estimates and reporting boundaries stay visible.
for operator in operators:
    pue_numbers = [float(v) for v in re.findall(r"\d+(?:\.\d+)?", operator["pue"])]
    pue_kind = "design" if "design" in operator["pue"].lower() else "reported"
    operator["pue_kind"] = pue_kind
    if not pue_numbers:
        operator["pue_value"] = None
    elif pue_kind == "design" and len(pue_numbers) >= 2:
        operator["pue_value"] = (pue_numbers[0] + pue_numbers[1]) / 2
    else:
        operator["pue_value"] = pue_numbers[0]
    wue = operator["wue_l_per_kwh"].strip()
    water = operator["water_gal_per_mw_year"].replace(",", "").strip()
    operator["wue_value"] = float(wue) if re.fullmatch(r"\d+(?:\.\d+)?", wue) else None
    operator["water_value"] = float(water) if re.fullmatch(r"\d+(?:\.\d+)?", water) else None

with open(os.path.join(FRONTEND, "index.template.html"), encoding="utf-8") as f:
    html = f.read()
with open(os.path.join(FRONTEND, "dashboard.css"), encoding="utf-8") as f:
    css = f.read()
with open(os.path.join(FRONTEND, "dashboard.js"), encoding="utf-8") as f:
    js = f.read()

# Prevent data strings from closing the inline script element.
def inline_json(value):
    return (json.dumps(value, ensure_ascii=False)
            .replace("</", "<\\/")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))

html = (html
        .replace("/*__DASHBOARD_CSS__*/", css)
        .replace("__DATA__", inline_json(out))
        .replace("__OPERATORS__", inline_json(operators))
        .replace("/*__DASHBOARD_JS__*/", js))
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

missing_status = [o["name"] for o in out if o["status"] == "unknown"]
if missing_status:
    print("  WARN: rows without status:", missing_status)
status_counts = {}
for o in out:
    status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1
print("Status breakdown:", dict(sorted(status_counts.items())))

# ---- summary ----
with_data = [o for o in out if o["h100e_best"]]
print(f"\nWrote {OUT_CSV}, {OUT_JSON}, {OUT_HTML}")
print(f"Sites: {len(out)} | with H100e estimate: {len(with_data)} | total H100e: {sum((o['h100e_best'] or 0) for o in out):,.0f}")
print("\nTop 15 by best H100e estimate:")
for o in out[:15]:
    print(f"  {o['h100e_best']:>10,.0f}  {o['name']} ({o['h100e_method']})")
