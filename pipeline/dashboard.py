"""
Render index.html from the published site dataset, the operator efficiency
table and the per-site cooling dataset.

Called by build.py (after the published CSV/JSON are written) and by
build_gpu_cooling.py (after gpu_cooling.csv is regenerated), so the dashboard
always embeds the current data regardless of which script ran last.
"""
import csv
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FRONTEND = os.path.join(ROOT, "pipeline", "frontend")
SITES_JSON = os.path.join(ROOT, "data", "published", "data_centers.json")
OPERATORS_CSV = os.path.join(ROOT, "data", "operator_efficiency.csv")
COOLING_CSV = os.path.join(ROOT, "data", "gpu_cooling.csv")
UTILITIES_CSV = os.path.join(ROOT, "data", "us_utility_impacts.csv")
PRICE_SCRIPT = os.path.join(ROOT, "pipeline", "verification", "price_vs_capacity.py")
OUT_HTML = os.path.join(ROOT, "index.html")

COOLING_NUMERIC = {
    "platform_count", "accelerator_count", "tdp_w", "tdp_w_low", "tdp_w_high",
    "accelerator_heat_mw", "accelerator_heat_mw_low", "accelerator_heat_mw_high",
    "accelerator_heat_share_pct", "it_load_mw", "cooling_thermal_load_mw",
    "pue_used", "cooling_electric_mw", "water_l_per_year", "water_mgal_per_year",
}


def inline_json(value):
    """Serialize for an inline <script>, without letting data close the tag."""
    return (json.dumps(value, ensure_ascii=False)
            .replace("</", "<\\/")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def load_sites():
    with open(SITES_JSON, encoding="utf-8") as handle:
        return json.load(handle)


def load_operators():
    with open(OPERATORS_CSV, encoding="utf-8") as handle:
        operators = list(csv.DictReader(handle))
    # Numeric chart fields are derived at build time; the original disclosure
    # strings remain intact so ranges, estimates and reporting boundaries stay
    # visible.
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
    return operators


def h100e_by_name():
    """Best H100e estimate per site, joined from the published dataset."""
    with open(SITES_JSON, encoding="utf-8") as handle:
        return {row["name"]: row.get("h100e_best") for row in json.load(handle)}


def load_cooling():
    if not os.path.exists(COOLING_CSV):
        return []
    H100E_BY_NAME = h100e_by_name()
    with open(COOLING_CSV, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if key in COOLING_NUMERIC:
                text = (value or "").strip()
                try:
                    item[key] = float(text) if text else None
                except ValueError:
                    item[key] = None
            else:
                item[key] = value
        it = item.get("it_load_mw")
        pue = item.get("pue_used")
        water = item.get("water_l_per_year")
        item["cooling_overhead_pct"] = (
            (pue - 1) * 100 if pue is not None else None)
        # 315 of 442 rows carry the industry default (1.2) rather than an
        # operator disclosure. That is an assumption, not evidence, so the
        # dashboard has to be able to tell the two apart.
        item["pue_disclosed"] = (
            pue is not None
            and not (item.get("pue_basis") or "").startswith("industry default"))
        item["water_l_per_mw_year"] = (
            water / it if water is not None and it else None)
        item["water_ml_per_mw_year"] = (
            item["water_l_per_mw_year"] / 1e6
            if item["water_l_per_mw_year"] is not None else None)
        h100e = H100E_BY_NAME.get(item.get("name"))
        item["h100e_best"] = h100e
        item["h100e_per_mw"] = (h100e / it) if h100e and it else None
        out.append(item)
    return out


def load_utilities():
    """The 55 US utility-territory rows, as published (text fields only)."""
    with open(UTILITIES_CSV, encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_states():
    """EIA state price rise and tracked operating MW, from the same code that
    docs/community_brief.md quotes, so the page and the brief cannot drift."""
    spec = importlib.util.spec_from_file_location("price_vs_capacity", PRICE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.state_rows()


def render():
    sites = load_sites()
    operators = load_operators()
    cooling = load_cooling()
    utilities = load_utilities()
    states = load_states()

    with open(os.path.join(FRONTEND, "index.template.html"), encoding="utf-8") as handle:
        html = handle.read()
    with open(os.path.join(FRONTEND, "dashboard.css"), encoding="utf-8") as handle:
        css = handle.read()
    with open(os.path.join(FRONTEND, "dashboard.js"), encoding="utf-8") as handle:
        js = handle.read()

    html = (html
            .replace("/*__DASHBOARD_CSS__*/", css)
            .replace("__DATA__", inline_json(sites))
            .replace("__OPERATORS__", inline_json(operators))
            .replace("__COOLING__", inline_json(cooling))
            .replace("__UTILITIES__", inline_json(utilities))
            .replace("__STATES__", inline_json(states))
            .replace("/*__DASHBOARD_JS__*/", js))
    with open(OUT_HTML, "w", encoding="utf-8") as handle:
        handle.write(html)
    return {"sites": len(sites), "operators": len(operators), "cooling": len(cooling),
            "utilities": len(utilities), "states": len(states)}
