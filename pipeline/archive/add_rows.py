"""Append new rows (China deep-dive, Malaysia deep-dive, Japan, South Korea)
to data/canonical/data_centers.csv. h100e_gpu values computed with the documented factor table:
H100/H200=1.0, B200=2.25, GB300=2.5, A100=0.315, Trainium2=0.34, Ascend 910B-class=0.35.
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
# ---------------- CHINA ----------------
row("VNET Bayin Ulanqab Computing Center","VNET Group (ByteDance tenant, reported)","Ulanqab","Inner Mongolia","China",41.03,113.15,it=221,types="Ascend 910C",h_3p=122789,
    notes="Epoch AI: 221 MW IT / 122,789 H100e as of 2026; part of VNET 1.2GW Ulanqab campus (operational since Oct 2024, expanding); major tenant ByteDance (500MW VNET deal); Eastern Data Western Computing corridor",url=E),
row("Envision Galaxy Campus Ulanqab","Envision Group","Ulanqab","Inner Mongolia","China",41.03,113.13,it=118,types="Ascend 950PR/950DT",h_3p=47931,
    notes="Epoch AI: 118 MW IT / 47,931 H100e; first 120MW phase commissioned Aug 2026; full buildout planned 2GW with up to 1M accelerators (claim); Envision Mission Gobi flagship; green-power direct supply",url=E),
row("Alibaba Ulanqab Data Center","Alibaba Cloud","Ulanqab","Inner Mongolia","China",40.98283,113.24075,
    notes="Operational hyperscale campus (5 buildings, 2020-2022); power not published; 2026 prefabricated AI expansion; Alibaba shifting to leased CICC/VNET Ulanqab capacity",url="https://baxtel.com/campus/alibaba-ulanqab-campus"),
row("Alibaba Heyuan (Yuancheng) Data Center","Alibaba Cloud","Heyuan","Guangdong","China",23.7431,114.6979,
    notes="Operational since 2020; ~15B CNY across 3 Heyuan campuses; designed for 300,000 servers; full completion 2028",url="https://www.datacenterdynamics.com/en/news/fire-breaks-out-at-alibaba-cloud-data-center-construction-site"),
row("Volcano Engine Horinger Computing Center (Phase 1)","ByteDance / Volcano Engine","Hohhot (Horinger New Area)","Inner Mongolia","China",40.548,111.69,power=100,
    notes="Under construction; first phase delivering from Dec 2025; two phases ~12B CNY; gigawatt-class campus signed Aug 2026; Horinger cluster total smart compute ~28,000P",url="http://hlgena.huhhot.gov.cn/zxzx/xqdt/202411/t20241105_1805127.html"),
row("Kuaishou Smart Cloud Data Center Ulanqab","Kuaishou","Ulanqab (Jining)","Inner Mongolia","China",41.011,113.19,
    notes="Operational self-built campus; ~10B CNY, designed ~300,000 servers; Building 4 delivered 2026 (~20MW); separate Kuaishou Horinger compute center signed Aug 2026",url="https://baxtel.com/data-center/alibaba-ulanqab-a"),
row("CICC Data Ulanqab Zero-Carbon Computing Base","China Financial Data Group (CICC Data)","Ulanqab (Chahar)","Inner Mongolia","China",41.031,113.145,power=360,
    notes="360MW IT capacity invested Aug 2024; 300MW wind/solar direct connection live Jul 2025; built for lease to Alibaba, ByteDance, Tencent, OPPO; wider CICC cluster planned >2.7GW",url="http://vr.ce.cn/vr2017/news/202610/t20261022_3267701.shtml"),
row("Tencent Tianjin Data Center","Tencent","Tianjin","Tianjin","China",39.3434,117.3616,
    notes="China's first 100k-server campus (2010); new High-Tech Cloud DC (2022) 300,000 servers; 300MW third-party estimate unconfirmed",url="https://www.idcnova.com/news/China-Data-Center-Tour-Tencent-Tianjin-Database-757"),
row("Tencent Qingyuan Cloud Computing Data Center","Tencent","Qingyuan (Qingxin)","Guangdong","China",23.652,112.97,
    notes="Operational since Jul 2020; 300,000 servers across 8 buildings; cluster planned for >1M servers",url="https://www.odcc.org.cn/auth/v-1482993351423057921.html"),
row("Tencent Gui'an Qixing Data Center","Tencent","Gui'an New Area","Guizhou","China",26.446,106.247,
    notes="China's first cave/tunnel data center (2020); tunnel phase 50,000 servers, campus total ~300,000",url="https://english.guiyang.gov.cn/dsjw/2023-12/26/c_952500.htm"),
row("Baidu Cloud Computing (Yangquan) Center","Baidu","Yangquan","Shanxi","China",37.862,113.59,
    notes="Baidu's first self-built hyperscale DC; 160,000+ servers; announced 40 EFLOPS computing power (precision unspecified)",url="https://baike.baidu.com/item/%E7%99%BE%E5%BA%A6%E4%BA%91%E8%AE%A1%E7%AE%97%EF%BC%88%E9%98%B3%E6%B3%89%EF%BC%89%E4%B8%AD%E5%BF%83/76139"),
row("China Telecom Lingang Intelligent Computing Valley","China Telecom Shanghai","Shanghai (Lingang)","Shanghai","China",30.89,121.925,gpu=15000,types="Ascend 910B",h_gpu=5250,
    notes="Operational; largest operator AIDC in China at launch; first single-pool 10,000-card liquid-cooled Ascend cluster (Mar 2024); 15,000 cards total; full buildout planned 300,000-card cluster",url="https://www.chinatelecom.com.cn/ct/news/yunjisuanjisuanli/154868.html"),
row("SenseTime Shanghai Lingang AIDC","SenseTime","Shanghai (Lingang)","Shanghai","China",30.883,121.908,
    notes="Operational; SenseCore network ~54,000 GPUs incl. A100/H800-class; Lingang delivers 14,000 PFLOPS (mixed precision) of 20,000P network-wide",url="https://kjc.shlingang.com/kjc/xwzxs/yqxw/202410/t20241012_32536.shtml"),
row("China Mobile Intelligent Computing Center (Harbin)","China Mobile Heilongjiang","Harbin","Heilongjiang","China",45.598,126.615,gpu=18000,types="Ascend 910B (Atlas 800T A2)",h_gpu=6300,
    notes="Largest single-cluster operator AI DC globally at launch (Aug 2024): 18,000 Ascend cards, 6.9 EFLOPS FP16 announced; PUE 1.2; 18,000-rack campus",url="https://www.hlj.gov.cn/hlj/c107856/202408/c00_31764518.shtml"),
row("China Telecom Qingyang Intelligent Computing Center","China Telecom Gansu","Qingyang","Gansu","China",35.73,107.64,power=250,
    notes="Under construction/expanding; 8 intelligent-computing buildings; >100,000 racks (~250MW IT); first 100kW liquid-cooled racks; Qingyang cluster total 306,000P FP16 (Oct 2026)",url="https://local.cctv.com/2026/09/18/ARTIyjwEDeaq7N2VZI9stVk260918.shtml"),
row("China Mobile (Gansu Qingyang) Data Center","China Mobile","Qingyang","Gansu","China",35.726,107.652,power=300,
    notes="Operational; 4 buildings; 92,000P (FP16) compute carried; hosts Alibaba, Kingsoft Cloud, 70+ enterprises; expanding toward GW-scale",url="https://www.stdaily.com/web/gdxw/2026-06/23/content_536052.html"),
row("Huawei Cloud Gui'an Data Center (Qixing Lake)","Huawei","Gui'an New Area","Guizhou","China",26.437,106.243,gpu=4000,types="Ascend 910B; CloudMatrix 384",h_gpu=1400,
    notes="Huawei's largest global campus; 4,000+ Ascend 910B online with CloudMatrix384 service (Jul 2025); PUE 1.12; used for DeepSeek V3/R1 deployment and Pangu training",url="https://www.huawei.com/cn/sustainability/the-latest/stories/green-data-centers-optimal-pue"),
row("China Telecom Cloud Computing Guizhou Information Park","China Telecom","Gui'an New Area","Guizhou","China",26.415,106.25,
    notes="Operational since 2016; 120,000 servers live (server count, not GPUs); hosts Gui'an Supercomputing Center (~300P class); southern China's largest single-operator cloud DC",url="https://www.chinatelecom.com.cn/ct/news/yunjisuanjisuanli/154887.html"),
row("CCCC Zhongjiao Zhishugu (Zhongwei) Industrial Park","China Communications Construction Company (CCCC)","Zhongwei","Ningxia","China",37.502,105.158,power=140,
    notes="Opened 2026; CCCC's first green data center; >140MW IT, designed for >60,000P; part of Zhongwei Western Cloud Base (88k GPU cards end-2024)",url="https://www.news.cn/politics/20260317/7b4eb07c9754dada8ad61b69a1aeee7/c.html"),
row("China Telecom Zhongwei Computing Hub Data Center","China Telecom Ningxia","Zhongwei","Ningxia","China",37.498,105.152,gpu=30000,types="Domestic heterogeneous (Ascend + others)",h_gpu=10500,
    notes="Operational; 30,000-card multi-heterogeneous intelligent-computing cluster; H100e assumes Ascend-class 0.35 factor; first large-scale green direct-supply project (Datang 2GW wind/solar)",url="https://www.news.cn/politics/20260317/7b4eb07c9754dada8ad61b69a1aeee7/c.html"),
row("Chengdu Intelligent Computing Center","Chengdu Hi-tech Zone with Huawei","Chengdu (Pidu)","Sichuan","China",30.78,103.905,
    notes="Operational May 2022; Phase 1: 300 PFLOPS FP16 (Ascend Atlas 900), southwest China's largest at opening; total planned 1000P",url="https://www.sc.chinanews.com.cn/bwbd/2022-05-12/167035.html"),
row("Wuhan Artificial Intelligence Computing Center","Hubei S&T Investment Group + Huawei","Wuhan (Optics Valley)","Hubei","China",30.475,114.55,
    notes="Operational since May 2021; China's first public-service AI compute infrastructure; 400P FP16 AI + HPC expansion; Huawei Ascend",url="https://www.wuhan.gov.cn/sy/whyw/202510/t20251028_2666958.html"),
row("China Unicom Hohhot Intelligent Computing Center","China Unicom","Hohhot (Horinger)","Inner Mongolia","China",40.61,111.7,gpu=10000,types="Domestic (Ascend ecosystem)",h_gpu=3500,
    notes="One of China Unicom's two 10,000-card-class intelligent-computing clusters (with Shanghai), announced Apr 2025",url="http://www.sasac.gov.cn/n2588025/n2588119/c33310006/content.html"),
row("ByteDance AI Data Center (Guangling County, Datong)","ByteDance / Volcano Engine","Datong (Guangling County)","Shanxi","China",39.76,114.28,
    notes="Reported 2026: $614M AI data center under construction; SemiAnalysis estimates ByteDance China footprint ~5.3GW by end-2026 (mostly leased)",url="https://www.datacenterdynamics.com/en/news/bytedance-takes-up-one-fifth-of-chinas-data-center-capacity"),
# ---------------- MALAYSIA ----------------
row("Bridge Data Centres MY06","Bridge Data Centres (Chindata)","Kulai (Sedenak Tech Park)","Johor","Malaysia",1.6954,103.4214,it=243,types="A100; H100; B200",h_3p=221052,
    notes="Operating; Phase 1 opened Oct 2022, expanded with MY06-2/3/4 buildings; anchor tenant ByteDance; Epoch AI: 243MW power / 221,052 H100e (A100/H100/B200)",url="https://www.mida.gov.my/media-release/bridge-data-centres-and-bytedance-celebrate-grand-opening-of-the-first-phase-hyperscale-data-centre-my06-in-johor-malaysia/"),
row("Bridge Data Centres MY07","Bridge Data Centres (Chindata)","Ulu Tiram (Desa Cemerlang)","Johor","Malaysia",1.55,103.72,power=200,
    notes="Under construction; 200MW+ IT across phases; first Malaysian DC with on-site effluent-water reclamation for AI cooling; target 2027",url="https://www.bridgedatacentres.com/bridge-data-centres-malaysias-first-data-centre-to-apply-effluent-water-and-cooling-technologies-at-johors-first-water-reclamation-plant/"),
row("Bridge Data Centres Cyberjaya (MY01 & MY02)","Bridge Data Centres (Chindata)","Cyberjaya","Selangor","Malaysia",2.9935,101.653,power=98,
    notes="Operating; ~20MW critical IT from 2018 plus 87MW MY02 expansion announced 2024; Bridge lists 98MW total IT for Cyberjaya campuses",url="https://www.datacenterdynamics.com/en/news/bridge-dc-expands-in-malaysia-with-data-center-in-cyberjaya/"),
row("Bridge Data Centres MY03","Bridge Data Centres (Chindata)","Kuala Lumpur","Kuala Lumpur","Malaysia",3.10,101.71,power=48,
    notes="Operating/expanding; 48MW expansion announced 2023; 150 acres earmarked at Southville City for up to 500MW",url="https://www.datacenterdynamics.com/en/news/bridge-dc-announces-48mw-expansion-to-kuala-lumpur-campus-in-malaysia/"),
row("Microsoft Malaysia West","Microsoft","Greater Kuala Lumpur","Kuala Lumpur","Malaysia",3.1478,101.6953,
    notes="Operating (GA 2025); first Azure region in Malaysia, three datacenters in Greater KL; part of $2.2B investment; GPU deployments not disclosed",url="https://news.microsoft.com/source/asia/features/microsoft-announces-its-first-cloud-region-in-malaysia-empowering-more-malaysian-organizations-to-accelerate-ai-innovation/"),
row("AWS Asia Pacific (Malaysia) Region","Amazon Web Services","Kuala Lumpur","Selangor","Malaysia",3.1408,101.693,
    notes="Operating; launched Aug 2024 with three AZs; planned $6.2B investment through 2038; capacity/GPUs not disclosed",url="https://aws.amazon.com/blogs/aws/now-open-aws-asia-pacific-malaysia-region/"),
row("Google Data Center & Cloud Region (Elmina Business Park)","Google","Shah Alam (Elmina)","Selangor","Malaysia",3.19,101.54,
    notes="Under construction; $2B investment announced May 2024; groundbroke Oct 2024; power capacity not disclosed",url="https://www.googlecloudpresscorner.com/2024-05-30-Advancing-Malaysia-Together-Google-Announces-US-2-Billion-Investment-in-Malaysia,-Including-First-Google-Data-Center-and-Google-Cloud-Region"),
row("Oracle Malaysia West 2 (ap-kulai-2)","Oracle","Kulai","Johor","Malaysia",1.65,103.60,
    notes="Operating; OCI public cloud region in Kulai, Johor; follows >$6.5B AI/cloud investment announcement (Oct 2024); GPU deployments not disclosed",url="https://docs.oracle.com/iaas/releasenotes/oci/new-region-malaya-2.htm"),
row("Princeton Digital Group JH1","Princeton Digital Group","Kulai (Sedenak Tech Park)","Johor","Malaysia",1.67,103.44,power=200,
    notes="Phase 1 (52MW) delivered Jul 2024, build-out ongoing; 4-building AI-ready campus upsized to 200MW",url="https://www.datacenterdynamics.com/en/news/princeton-digital-group-tops-out-third-building-of-200mw-campus-in-johor-malaysia/"),
row("AirTrunk JHB1","AirTrunk (Blackstone)","Johor Bahru","Johor","Malaysia",1.5548,103.6808,power=150,
    notes="Operating since Jul 2024; initial 50MW scalable to 150+MW; AI-ready",url="https://airtrunk.com/airtrunk-opens-ai-ready-data-centre-in-malaysia-accelerating-innovation-and-the-energy-transition/"),
row("AirTrunk JHB2","AirTrunk (Blackstone)","Iskandar Puteri","Johor","Malaysia",1.46,103.61,power=270,
    notes="Under development; second Malaysia hyperscale DC scalable to 270MW+; JHB1+JHB2 combined 420+MW",url="https://airtrunk.com/airtrunk-scales-up-in-malaysia-with-announcement-of-second-malaysia-hyperscale-data-centre-jhb2/"),
row("Vantage KUL1 (Cyberjaya I)","Vantage Data Centers","Cyberjaya","Selangor","Malaysia",2.996,101.648,power=31,
    notes="Operating; 31MW critical IT across four buildings; final 16MW facility launched Dec 2025",url="https://vantage-dc.com/news/vantage-data-centers-launches-fully-leased-16mw-facility-in-kuala-lumpur/"),
row("Vantage KUL2 (Cyberjaya II)","Vantage Data Centers","Cyberjaya","Selangor","Malaysia",3.003,101.641,power=256,
    notes="Under construction; 256MW campus, 10 buildings, own 500MVA substation",url="https://www.datacenterdynamics.com/en/news/vantage-breaks-ground-on-256mw-data-center-campus-in-cyberjaya-malaysia/"),
row("Vantage JHB1 (ex-Yondr)","Vantage Data Centers","Kulai (Sedenak Tech Park)","Johor","Malaysia",1.68,103.45,power=300,
    notes="Under development; acquired Yondr's 300MW+ hyperscale AI-ready campus (Sept 2025)",url="https://vantage-dc.com/news/vantage-data-centers-completes-1-6b-investment-in-apac-platform-from-gic-and-adia-closes-acquisition-of-yondrs-300mw-hyperscale-campus-in-johor-malaysia/"),
row("STT Johor 1","ST Telemedia Global Data Centres","Iskandar Puteri (Nusa Cemerlang)","Johor","Malaysia",1.50,103.62,power=120,
    notes="Under construction; up to 166MW development capacity; liquid-cooling capable; $1.37B green financing secured (2026)",url="https://www.datacenterdynamics.com/en/news/stt-gdc-plans-120mw-data-center-campus-in-johor-malaysia/"),
row("STACK JHB01","STACK Infrastructure","Iskandar Puteri (Nusajaya Tech Park)","Johor","Malaysia",1.445,103.594,power=216,
    notes="Under construction; 216-220MW campus targeting cloud and AI; ~120MW phase progressing 2026",url="https://www.stackinfra.com/about/news-press/press-releases/stack-infrastructure-announces-220mw-campus-in-malaysia/"),
row("ZDATA GP3","ZDATA Technologies","Gelang Patah","Johor","Malaysia",1.46,103.60,
    notes="Under construction; groundbroke Feb 2025; reports cite up to 500MW capacity (unconfirmed) and a stop-work order (Aug 2025); power left blank pending confirmation",url="https://w.media/zdata-seeks-us-500-million-loan-for-johor-data-center-reports/"),
row("NTT JHB10","NTT Global Data Centers","Gelang Patah","Johor","Malaysia",1.459,103.614,power=290,
    notes="Planned/under construction; six buildings totaling 290MW on 27.7ha",url="https://www.datacenterdynamics.com/en/news/ntt-plans-290mw-data-center-campus-in-johor-malaysia/"),
row("K2 Strategic JHR01-03","K2 Strategic (Kuok Group)","Kulai (Sedenak Tech Park)","Johor","Malaysia",1.66,103.47,power=60,
    notes="Operating; 60MW campus opened Oct 2024; Johor's third-largest operator (126MW); separate 24MW JHR04 campus also in Kulai",url="https://www.forbes.com/sites/jonathanburgos/2025/02/26/grandson-of-malaysian-billionaire-robert-kuok-builds-data-centers-as-demand-soars-amid-ai-boom/"),
row("Basis Bay Cyberjaya DC2","Basis Bay (JV with STT GDC)","Cyberjaya","Selangor","Malaysia",2.99,101.65,
    notes="Operating (launched Nov 2025); Tier-4-designed; power capacity not disclosed",url="https://basisbay.com/data-centres/"),
row("Digital Cosmos Cyberjaya","Digital Cosmos (S) Pte Ltd","Cyberjaya","Selangor","Malaysia",2.99,101.65,power=182,
    notes="Planned (early stage); 36-acre parcel sold Aug 2026 for campus of up to 182MW",url="https://www.datacenterdynamics.com/en/news/malaysian-property-giant-sells-36-acre-land-parcel-in-cyberjaya-for-data-center/"),
row("FutureData Data Center Park Kuching","FutureData","Kuching","Sarawak","Malaysia",1.55,110.35,power=500,
    notes="Planned; 500MW purpose-built AI data center park; first off-taker announced 2026",url="https://www.datacenterdynamics.com/en/news/futuredata-announces-first-off-taker-at-500mw-malaysian-data-center-park-in-sarawak/"),
# ---------------- JAPAN ----------------
row("SoftBank Hokkaido Tomakomai AI Data Center","SoftBank Corp / IDC Frontier","Tomakomai","Hokkaido","Japan",42.66,141.59,power=300,
    notes="Under construction (groundbroke Apr 2025); first 50MW phase FY2026, expandable to 300MW+ (land for up to 1GW); candidate host for SB OpenAI Japan sovereign compute",url="https://www.softbank.jp/en/sbnews/entry/20250501_01"),
row("SoftBank Osaka Sakai AI Data Center","SoftBank Corp","Sakai","Osaka","Japan",34.555,135.493,power=150,
    notes="Under construction on former Sharp LCD plant; ~150MW at 2026 launch, expandable to 250-400MW+; intended SB OpenAI Japan AI factory; press reports suggest up to ~100,000 GPUs (unconfirmed)",url="https://www.softbank.jp/en/corp/news/press/sbkk/2024/20240607_01"),
row("KDDI TELEHOUSE Osaka Sakai","KDDI Corporation","Sakai","Osaka","Japan",34.556,135.494,power=48,
    notes="Operational Jan 2026; NVIDIA GB200 NVL72 racks with direct liquid cooling; ~48MW per DC Pulse (unverified estimate)",url="https://www.datacentermap.com/japan/osaka/telehouse-osaka-sakai/"),
row("AIST ABCI 3.0","AIST (National Institute of Advanced Industrial Science and Technology)","Kashiwa","Chiba","Japan",35.68882,139.692526,gpu=6128,types="NVIDIA H200 SXM",h_gpu=6128,
    notes="Operating since Jan 2025; 6,128 NVIDIA H200 on Univ. of Tokyo Kashiwa campus; Japan's flagship public AI cloud (~36B yen)",url="https://epoch.ai/data/gpu_clusters.csv"),
row("AIST ABCI-Q (G-QuAT)","AIST","Tsukuba","Ibaraki","Japan",36.065,140.123,gpu=2000,types="NVIDIA H100 SXM",h_gpu=2000,
    notes="Operating 2025; ~2,000 H100 as AI portion of the ABCI-Q quantum-AI center",url="https://flopper.io/datacenters/country/Japan"),
row("Sakura Internet Ishikari Data Center (High-Power GPU Cloud)","Sakura Internet","Ishikari","Hokkaido","Japan",43.19,141.35,gpu=3400,types="NVIDIA H100; H200; B200",h_gpu=3900,
    notes="Operating and expanding; ~2,000 H100 + ~1,000 H200 (Jun 2025) + ~400 B200 of ~1,500 planned (2025); targeting 18.9 EFLOPS (mixed precision) by Mar 2028",url="https://www.sakura.ad.jp/corporate/en/information/2025/08/14/1968220602/"),
row("Ishikari Renewable Energy Data Center No.1","Tokyu Land / Flower Communications (ISRD LLC)","Ishikari","Hokkaido","Japan",43.16,141.33,power=15,
    notes="Completed Mar 2026, service from Aug 2026; 6 data halls incl. Hokkaido's first 2.4MW liquid-cooled GPU-dedicated hall; tenants include GMO GPU Cloud",url="https://www.tokyu-dc.com/en/dc_ishikari.html"),
row("AirTrunk TOK1 (Tokyo East)","AirTrunk (Blackstone)","Inzai","Chiba","Japan",35.83,140.10,power=300,
    notes="Operating since 2021 and expanding; Japan's largest hyperscale campus at 300MW+; 40MW+ phase groundbreaking Jun 2025",url="https://airtrunk.com/airtrunk-breaks-ground-on-40mw-phase-of-tok1-japans-largest-hyperscale-data-centre-campus/"),
row("AirTrunk TOK2 (Tokyo West)","AirTrunk (Blackstone)","Ome","Tokyo","Japan",35.79,139.28,power=110,
    notes="Under construction; 110MW+ across 3 buildings",url="https://airtrunk.com/location/japan/"),
row("AirTrunk OSK2 (Osaka East)","AirTrunk (Blackstone)","East Osaka","Osaka","Japan",34.63,135.60,power=100,
    notes="Announced Dec 2025; up to 100MW serving AI workloads; complements existing 20MW OSK1",url="https://airtrunk.com/airtrunk-to-build-second-osaka-hyperscale-data-centre-to-support-ai-growth/"),
row("Google Inzai Data Center","Google","Inzai","Chiba","Japan",35.83,140.09,
    notes="Operating since Mar 2023; Google's first owned Japan DC; part of ~$730M Japan investment; additional Hiroshima/Wakayama land acquired",url="https://www.datacenterdynamics.com/en/news/google-signs-15mw-virtual-ppa-with-jera-for-data-center-in-inzai-japan/"),
row("Goodman Tsukuba Campus","Goodman Group","Tsukuba","Ibaraki","Japan",36.03,140.07,power=1000,it=800,
    notes="Under construction; 10-building AI-ready campus up to 1GW gross (~800MW IT), full buildout ~2034; DC1 60MW Q1 2028",url="https://dcpulse.com/projects/asia-pacific/japan"),
row("MC Digital Realty NRT14 (Inzai Campus)","MC Digital Realty (Mitsubishi/Digital Realty JV)","Inzai","Chiba","Japan",35.86,140.10,it=31,
    notes="Live/operational from 2026; 31MW with up to 70kW/rack AI-ready halls; sibling NRT10 is NVIDIA DGX-ready",url="https://dcpulse.com/projects/asia-pacific/japan"),
row("TSUBAME4.0","Tokyo Institute of Technology (GSIC)","Yokohama","Kanagawa","Japan",35.523,139.538,gpu=960,types="NVIDIA H100 SXM",h_gpu=960,
    notes="Operating from 2024-2025; ~960 H100; leading Japanese academic AI/HPC cluster",url="https://epoch.ai/data/gpu_clusters.csv"),
row("ai& Tokyo AI Data Center","ai& (AI infrastructure company)","Tokyo","Tokyo","Japan",35.68,139.77,power=40,
    notes="Planned; first Tokyo site deploying Sep 2026 with Rebellions inference racks; ~40MW by end-2027; Japan sovereign-AI inference buildout",url="https://www.hpcwire.com/off-the-wire/rebellions-and-ai-partner-to-bring-energy-efficient-ai-inference-infrastructure-to-japan/"),
# ---------------- SOUTH KOREA ----------------
row("SK Broadband Gasan AI Data Center","SK Broadband / SK Telecom","Seoul","Seoul","South Korea",37.4784,126.8825,gpu=1032,types="NVIDIA B200; H100",h_gpu=2322,
    notes="Operating; hosts SKT GPUaaS Haein cluster of 1,032 B200 (production Aug 2025) plus H100 GPUaaS with Lambda; up to 44kW/rack",url="https://www.penguinsolutions.com/en-us/industries/sovereign-ai"),
row("Naver Data Center GAK Chuncheon","Naver","Chuncheon","Gangwon","South Korea",37.845,127.215,power=40,
    notes="Operating since 2013; Naver's first self-built hyperscale DC; hosts NVIDIA DGX SuperPOD for Hyperclova X training; GPU counts not published",url="https://www.wbgkggtf.org/node/4122"),
row("Naver Data Center GAK Sejong","Naver","Sejong","Sejong","South Korea",36.49,127.24,power=270,
    notes="Operating since Nov 2023; up to 270MW design capacity over six phases; ~1/6 in operation Oct 2025; backbone for Hyperclova X / Ncloud; Naver Cloud plans 60,000+ GPUs",url="https://www.ai-dc.co.kr/international/en/centers/naver-gak-sejong"),
row("National AI Computing Center (Koark)","Koark SPC (Samsung SDS largest shareholder)","Haenam","South Jeolla","South Korea",34.63,126.57,power=40,gpu=15000,h_gpu=15000,
    notes="Under construction; groundbreaking Aug 2026, completion 2028; 40MW and ~15,000 AI chips planned; public-private SPC",url="https://research.bit-planet.kr/en/d/ai-data-center-map-korea-20260917"),
row("Samsung SDS Gumi AI Data Center","Samsung SDS","Gumi","North Gyeongsang","South Korea",36.126,128.334,power=60,
    notes="Planned; KRW 427.3B for 60MW AI DC; target operation Mar 2029",url="https://research.bit-planet.kr/en/d/ai-data-center-map-korea-20260917"),
row("NHN Cloud Gwangju National AI Data Center","NHN Cloud (with MSIT and Gwangju city)","Gwangju","Gwangju","South Korea",35.219,126.756,gpu=1000,types="NVIDIA H100 (plus A100/V100/Graphcore/Sapeon)",h_gpu=1000,
    notes="Operating since Oct 2023; Korea's first AI-specialized DC; 88.5 PF announced (mixed); 1,000+ H100s; government secured 416 H100 for public use",url="https://www.koreajoongangdaily.com/business/nhn-aims-high-with-ai-data-center-powered-by-nvidias-h100-gpus/10647571"),
row("Kakao Data Center Ansan","Kakao","Ansan","Gyeonggi","South Korea",37.3021,126.8323,gpu=2424,types="NVIDIA B200",h_gpu=5454,
    notes="Operating since Jan 2024; selected Aug 2025 as national GPU project operator: 2,424 B200 consigned 5 years, 2,040 installed by Dec 2025",url="https://www.kakaocorp.com/page/detail/11917"),
row("LG Uplus Paju AIDC","LG Uplus","Paju","Gyeonggi","South Korea",37.73,126.76,power=200,gpu=120000,h_gpu=120000,
    notes="Under construction; 200MW confirmed - largest in Seoul metro; building 1 (40-50MW) Jun 2027, fully pre-leased; designed to host up to 120,000 GPUs (MWC 2026, planned)",url="https://www.alphabiz.co.kr/news/articleView.html?idxno=144853"),
row("GS AI Infrastructure Donghae AI Data Center Campus","GS AI Infrastructure (GS Group)","Donghae","Gangwon","South Korea",37.242,129.199,power=100,
    notes="Planned; first 100MW building permitted Oct 2026, completion 2H 2028; Phase 1 1.2GW, long-term campus 2.4GW with on-site GS power (1.19GW)",url="https://en.fnnews.com/news/202610060934305665"),
row("LG AI Research AEX cluster (LG Science Park)","LG AI Research","Seoul","Seoul","South Korea",37.5378,126.829,gpu=512,types="NVIDIA H100; A100",h_gpu=512,
    notes="Operating research compute campus; 512 H100 as of Feb 2025; EXAONE models trained here",url="https://www.businesskorea.co.kr/news/articleView.html?idxno=234996"),
row("AWS Incheon AI Data Center","Amazon Web Services","Incheon","Incheon","South Korea",37.456,126.706,power=100,
    notes="Under construction/announced; AI-dedicated DC up to 100MW; part of KRW 7.85T Korea investment through 2027; separate from SK-AWS Ulsan",url="https://biz.chosun.com/en/en-it/2025/06/20/3XEYELUTIZFZTKKPA6DVY3SYHU/"),
row("KISTI National Supercomputing Center (HANGANG No.6)","KISTI (Ministry of Science and ICT)","Daejeon","Daejeon","South Korea",36.351,127.3655,gpu=8000,types="NVIDIA H200/B200-class (planned)",h_gpu=8000,
    notes="Operating national supercomputing site; 6th-gen HANGANG planned with ~8,000 GPUs by 1H 2026; part of plan for 18,000 advanced GPUs",url="https://www.korea.kr/news/policyNewsView.do?newsId=148939678"),
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
