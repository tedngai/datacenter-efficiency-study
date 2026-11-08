"""
Build data/gpu_cooling.csv (and .json) from the canonical site inventory and
the accelerator reference table.

Method (documented in docs/gpu_cooling.md):

  accelerator_heat_mw        = accelerator_count x tdp_w / 1e6
  cooling_thermal_load_mw    ~= it_load_mw          (all IT energy becomes heat)
  cooling_electric_mw        = it_load_mw x (PUE - 1)
  water_l_per_year           = it_load_mw x 8,760 h x 1,000 kWh/MWh x WUE

The last line is an operator-fleet scaling, not a site measurement. It is only
emitted where the operator publishes (or we derive) a WUE, and is labelled as
such. A liquid-cooled rack does not imply zero water: the facility still has to
reject the heat, and that is where evaporation happens.

Run after pipeline/build.py:
    python pipeline/build.py
    python pipeline/build_gpu_cooling.py
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANONICAL = os.path.join(ROOT, "data", "canonical", "data_centers.csv")
PUBLISHED = os.path.join(ROOT, "data", "published", "data_centers.csv")
PLATFORMS = os.path.join(ROOT, "data", "gpu_platforms.csv")
OUT_CSV = os.path.join(ROOT, "data", "gpu_cooling.csv")
OUT_JSON = os.path.join(ROOT, "data", "gpu_cooling.json")

# Operator-level disclosures. PUE and WUE are fleet/portfolio figures, not
# site measurements. Longest key wins, so "Amazon Web Services" beats "Amazon".
PROFILES = {
    "Google": dict(pue=1.09, pue_label="2025 fleet", wue=1.02,
                   wue_label="2025 fleet, derived from consumption", heat="evaporative"),
    "Meta": dict(pue=1.08, pue_label="FY2024 fleet", wue=0.19,
                 wue_label="FY2024 fleet, withdrawal basis", heat="hybrid"),
    "Microsoft": dict(pue=1.17, pue_label="FY25 fleet", wue=0.27,
                      wue_label="FY25 fleet", heat="hybrid"),
    "Amazon Web Services": dict(pue=1.14, pue_label="2025 fleet", wue=0.12,
                                wue_label="2025 fleet", heat="hybrid"),
    "Amazon": dict(pue=1.14, pue_label="2025 fleet", wue=0.12,
                   wue_label="2025 fleet", heat="hybrid"),
    "AWS": dict(pue=1.14, pue_label="2025 fleet", wue=0.12,
                wue_label="2025 fleet", heat="hybrid"),
    "xAI": dict(pue=None, pue_label="no disclosure", wue=1.0,
                wue_label="2025 estimate, Memphis aquifer", heat="evaporative"),
    "Crusoe": dict(pue=1.3, pue_label="design midpoint 1.2-1.4", wue=0.002,
                   wue_label="design, closed-loop non-evaporative", heat="dry_closed_loop"),
    "Nebius": dict(pue=1.25, pue_label="2025 portfolio", wue=0.018,
                   wue_label="2025 Finland-1, liquid-cooled", heat="dry_closed_loop"),
    "IREN": dict(pue=1.15, pue_label="guidance midpoint 1.1-1.2", wue=None,
                 wue_label="not disclosed", heat=None),
    "TeraWulf": dict(pue=1.15, pue_label="single campus, secondary source", wue=None,
                     wue_label="not disclosed", heat=None),
    "Applied Digital": dict(pue=None, pue_label="no disclosure", wue=None,
                            wue_label="waterless claim, no figure", heat="dry_closed_loop"),
}
DEFAULT_PUE = 1.2
DEFAULT_PUE_LABEL = "industry default, not operator-disclosed"

VENDOR_TOKENS = {
    "NVIDIA": r"\bNVIDIA\b|\bGB200\b|\bGB300\b|\bB200\b|\bB300\b|\bH100\b|\bH200\b|\bA100\b|\bGH200\b|\bL40S\b|\bL4\b|\bH20\b|\bL20\b",
    "Google": r"\bTPU\b|\bGoogle\b",
    "AWS": r"\bTrainium|\bInferentia|\bGraviton\b",
    "AMD": r"\bAMD\b|\bMI300|\bMI325|\bMI355|\bMI430",
    "Huawei": r"\bAscend\b|\bHuawei\b",
    "Meta": r"\bMTIA\b",
    "Intel": r"\bGaudi\b",
}

# Notes that mention hardware but not the site's own deployed fleet.
NOTE_HARDWARE_EXCLUDE = {
    "Microsoft Acton (UK South expansion)",
    # The note describes a national procurement, not this campus's fit-out.
    "DataVolt TAS-1 (Tashkent IT Park DC)",
}

COLS = [
    "name", "operator", "country", "status",
    "gpu_types_raw", "gpu_evidence",
    "platform_ids", "platform_models", "platform_count", "platform_confidence",
    "accelerator_count", "accelerator_count_basis",
    "tdp_w", "tdp_w_low", "tdp_w_high", "tdp_basis",
    "accelerator_heat_mw", "accelerator_heat_mw_low", "accelerator_heat_mw_high",
    "accelerator_heat_share_pct",
    "it_load_mw", "it_load_basis",
    "cooling_thermal_load_mw",
    "pue_used", "pue_basis", "cooling_electric_mw",
    "rack_cooling", "rack_cooling_basis",
    "heat_rejection", "heat_rejection_basis",
    "water_dependency",
    "water_l_per_year", "water_mgal_per_year", "water_estimate_basis",
    "confidence", "consistency", "basis",
    "source_url", "platform_source_url",
]


def as_float(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def as_int(value):
    number = as_float(value)
    return int(round(number)) if number is not None else None


def fmt(value, digits=2):
    if value is None:
        return ""
    text = f"{value:.{digits}f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def profile_for(operator):
    for key in sorted(PROFILES, key=len, reverse=True):
        if key.lower() in (operator or "").lower():
            return key, PROFILES[key]
    return None, None


def load_platforms():
    with open(PLATFORMS, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["_regex"] = re.compile(row["match_regex"], re.I)
        row["_specific"] = row["specific"].strip() == "1"
    return rows


def match_platforms(text, platforms):
    """Return matched platform rows, specific first, with generic fallbacks."""
    specific = [p for p in platforms if p["_specific"]]
    generic = [p for p in platforms if not p["_specific"]]

    matched = [p for p in specific if p["_regex"].search(text)]
    if matched:
        # Add a vendor-level placeholder only when the vendor is named but no
        # specific model of that vendor was identified.
        for vendor, token in VENDOR_TOKENS.items():
            if not re.search(token, text, re.I):
                continue
            if any(p["vendor"] == vendor for p in matched):
                continue
            fallback = next((p for p in generic if p["vendor"] == vendor), None)
            if fallback:
                matched.append(fallback)
        # A site that names both a specific part and its wider family (e.g.
        # "Blackwell and Vera Rubin") should keep both. Only add the family row
        # when no matched platform already belongs to that family.
        blackwell = next((p for p in generic if p["platform_id"] == "nvidia_blackwell_generic"), None)
        if (blackwell and blackwell["_regex"].search(text)
                and not any("Blackwell" in p["family"] for p in matched)):
            matched.append(blackwell)
        return matched

    fallback_matches = [p for p in generic if p["_regex"].search(text)]
    if len(fallback_matches) > 1:
        vendor_matches = [p for p in fallback_matches if p["vendor"] != "Various"]
        if vendor_matches:
            # A named family (e.g. Blackwell) is more informative than a bare
            # vendor placeholder, so drop the vendor-wide row when both match.
            if any(p["platform_id"] != "nvidia_generic" and p["vendor"] == "NVIDIA"
                   for p in vendor_matches):
                vendor_matches = [p for p in vendor_matches if p["platform_id"] != "nvidia_generic"]
            fallback_matches = vendor_matches
    return fallback_matches


def aggregate_tdp(platforms):
    """Return (point, low, high, basis). Point is blank for mixed generations."""
    if not platforms:
        return None, None, None, "no accelerator platform identified"
    values = []
    for platform in platforms:
        tdp = as_float(platform["tdp_w"])
        if tdp is None:
            return None, None, None, f"{platform['model']} has no published TDP"
        values.append(tdp)
    low, high = min(values), max(values)
    if low == high:
        return low, low, high, f"all matched platforms share {fmt(low, 0)} W"
    return None, low, high, "mixed platform TDPs (" + ", ".join(
        f"{p['model']} {fmt(as_float(p['tdp_w']), 0)} W" for p in platforms) + ")"


def rack_cooling_for(platforms, notes):
    note = notes or ""
    if re.search(r"\bimmersion\b", note, re.I):
        return "immersion", "site note"
    if re.search(r"air\s*\+\s*direct[- ]to[- ]chip|hybrid[^.]{0,40}(liquid|air)", note, re.I):
        return "hybrid", "site note"
    if re.search(r"direct[- ]to[- ]chip|direct[- ]liquid|direct liquid", note, re.I):
        return "dlc", "site note"
    if re.search(r"liquid[- ]cool", note, re.I):
        if re.search(r"capable|ready|prepared", note, re.I):
            return "dlc_capable", "site note (capability, not confirmed deployment)"
        return "dlc", "site note"

    values = {p["rack_cooling"] for p in platforms}
    if not values:
        return "unknown", "no hardware evidence"
    if values == {"air"}:
        return "air", "platform-implied"
    if values == {"dlc"}:
        return "dlc", "platform-implied"
    if values <= {"air", "dlc"}:
        return "hybrid", "platform-implied"
    if "air_or_dlc" in values or "dlc_or_air" in values:
        return "air_or_dlc", "platform-implied"
    if "immersion" in values:
        return "immersion", "platform-implied"
    return "unknown", "platform cooling not resolved"


def heat_rejection_for(notes, profile, profile_key):
    note = notes or ""
    if re.search(r"no operational water use|waterless|non[- ]evaporative", note, re.I):
        return "dry_closed_loop", "site note"
    if re.search(r"evaporative|cooling tower", note, re.I):
        return "evaporative", "site note"
    if profile and profile.get("heat"):
        if profile.get("wue") is not None:
            basis = (f"operator fleet profile: {profile['heat']} heat rejection, "
                     f"WUE {fmt(profile['wue'], 3)} L/kWh ({profile['wue_label']}); not site-specific")
        else:
            basis = f"operator fleet profile: {profile['heat']} heat rejection; not site-specific"
        return profile["heat"], basis
    return "unknown", "no site or operator evidence"


def water_dependency_for(wue):
    if wue is None:
        return "unknown"
    if wue >= 0.5:
        return "high"
    if wue >= 0.2:
        return "moderate"
    if wue >= 0.05:
        return "low"
    return "negligible"


def confidence_for(platforms, count_known, tdp_known, site_cooling):
    """Grade the hardware/heat estimate, capped by the weakest TDP source.

    A site cannot be graded A if the TDP it rests on is itself a secondary
    estimate, so the completeness grade is capped at the worst platform grade.
    """
    all_specific = bool(platforms) and all(p["_specific"] for p in platforms)
    if all_specific and count_known and tdp_known and site_cooling:
        grade = "A"
    elif all_specific and count_known and tdp_known:
        grade = "B"
    elif all_specific or count_known:
        grade = "C"
    else:
        grade = "D"
    if platforms:
        worst = max("ABCD".index(p["confidence"]) for p in platforms)
        grade = "ABCD"[max("ABCD".index(grade), worst)]
    return grade


def main():
    if not os.path.exists(PUBLISHED):
        sys.exit("Run pipeline/build.py first: data/published/data_centers.csv is missing.")
    with open(PUBLISHED, encoding="utf-8") as handle:
        sites = list(csv.DictReader(handle))
    platforms = load_platforms()

    out = []
    warnings = []
    for site in sites:
        name = site["name"].strip()
        operator = site["operator"].strip()
        notes = site.get("notes", "") or site.get("status_note", "")
        gpu_types = (site.get("gpu_types") or "").strip()

        evidence = "gpu_types" if gpu_types else "none"
        text = gpu_types
        if not gpu_types and name not in NOTE_HARDWARE_EXCLUDE and notes:
            text = notes
            evidence = "notes"

        matched = match_platforms(text, platforms) if text else []
        if not matched:
            # Notes are scanned for hardware, but a site with no match has no
            # accelerator evidence regardless of how much prose it carries.
            evidence = "none"
        platform_ids = ";".join(p["platform_id"] for p in matched)
        platform_models = "; ".join(p["model"] for p in matched)
        platform_source = matched[0]["source_url"] if matched else ""

        tdp_w, tdp_low, tdp_high, tdp_basis = aggregate_tdp(matched)
        count = as_int(site.get("announced_gpu_count"))
        count_known = count is not None and count > 0

        heat_mw = None
        heat_low = None
        heat_high = None
        heat_share = None
        if count_known and tdp_low is not None:
            heat_low = count * tdp_low / 1e6
            heat_high = count * tdp_high / 1e6
            if tdp_w is not None:
                heat_mw = count * tdp_w / 1e6

        profile_key, profile = profile_for(operator)
        pue = profile["pue"] if profile else None
        pue_label = profile["pue_label"] if profile else None
        if pue is None:
            pue = DEFAULT_PUE
            pue_label = DEFAULT_PUE_LABEL
        wue = profile["wue"] if profile else None
        wue_label = profile["wue_label"] if profile else None

        it_load = as_float(site.get("it_load_mw"))
        power = as_float(site.get("power_capacity_mw"))
        if it_load is not None and it_load > 0:
            it_basis = "published IT load"
        elif power is not None and power > 0:
            it_load = power / pue
            it_basis = f"derived: gross power / PUE {fmt(pue, 2)}"
        else:
            it_load = None
            it_basis = "no power or IT-load figure"

        if heat_mw is not None and it_load:
            heat_share = heat_mw / it_load * 100

        cooling_thermal = it_load
        cooling_electric = it_load * (pue - 1) if it_load else None

        rack, rack_basis = rack_cooling_for(matched, notes)
        heat, heat_basis = heat_rejection_for(notes, profile, profile_key)
        water_dep = water_dependency_for(wue)

        water_l = it_load * 8760 * 1000 * wue if (it_load and wue is not None) else None
        water_mgal = water_l / 3.78541e6 if water_l is not None else None
        water_basis = (
            f"operator fleet WUE {fmt(wue, 3)} L/kWh x site IT load; not site-measured ({wue_label})"
            if water_l is not None else "no operator WUE and no site measurement"
        )
        # A site that explicitly states it uses no operational water should not
        # inherit its operator's fleet WUE. That would contradict the evidence.
        if re.search(r"no operational water use|waterless|non[- ]evaporative", notes or "", re.I):
            water_l = 0.0
            water_mgal = 0.0
            water_dep = "negligible"
            water_basis = "site note states no operational water use; operator fleet WUE not applied"

        # Confidence grades the hardware/heat estimate. Water has its own
        # evidence column (heat_rejection_basis) and dependency grade.
        site_cooling = rack_basis.startswith("site note") or heat_basis == "site note"
        confidence = confidence_for(matched, count_known, tdp_low is not None, site_cooling)

        if heat_low is not None and it_load:
            if heat_low > it_load * 1.02:
                consistency = "accelerator heat exceeds reported IT load; check count or IT basis"
                warnings.append(f"{name}: accelerator heat {heat_low:.1f}-{heat_high:.1f} MW exceeds IT load {it_load:.1f} MW")
            elif heat_high > it_load * 1.02:
                consistency = "upper accelerator-heat bound exceeds reported IT load"
            else:
                consistency = "ok"
        elif heat_low is None:
            consistency = "no accelerator heat estimate"
        else:
            consistency = "no IT load to compare"

        if tdp_w is not None:
            tdp_text = f"{fmt(tdp_w, 0)} W TDP"
        elif tdp_low is not None:
            tdp_text = f"{fmt(tdp_low, 0)}-{fmt(tdp_high, 0)} W TDP range"
        else:
            tdp_text = "TDP unresolved"

        basis_parts = [
            platform_models or "no accelerator model",
            f"{count:,} accelerators" if count_known else "count unpublished",
            tdp_text,
            f"rack {rack}",
            f"heat rejection {heat}",
            f"water {water_dep}",
        ]

        out.append({
            "name": name,
            "operator": operator,
            "country": site.get("country", ""),
            "status": site.get("status", ""),
            "gpu_types_raw": gpu_types,
            "gpu_evidence": evidence,
            "platform_ids": platform_ids,
            "platform_models": platform_models,
            "platform_count": len(matched),
            "platform_confidence": max((p["confidence"] for p in matched),
                                       key=lambda grade: "ABCD".index(grade), default="D"),
            "accelerator_count": count if count_known else "",
            "accelerator_count_basis": "announced" if count_known else "unknown",
            "tdp_w": fmt(tdp_w, 0),
            "tdp_w_low": fmt(tdp_low, 0),
            "tdp_w_high": fmt(tdp_high, 0),
            "tdp_basis": tdp_basis,
            "accelerator_heat_mw": fmt(heat_mw, 2),
            "accelerator_heat_mw_low": fmt(heat_low, 2),
            "accelerator_heat_mw_high": fmt(heat_high, 2),
            "accelerator_heat_share_pct": fmt(heat_share, 1),
            "it_load_mw": fmt(it_load, 1),
            "it_load_basis": it_basis,
            "cooling_thermal_load_mw": fmt(cooling_thermal, 1),
            "pue_used": fmt(pue, 2),
            "pue_basis": pue_label,
            "cooling_electric_mw": fmt(cooling_electric, 2),
            "rack_cooling": rack,
            "rack_cooling_basis": rack_basis,
            "heat_rejection": heat,
            "heat_rejection_basis": heat_basis,
            "water_dependency": water_dep,
            "water_l_per_year": fmt(water_l, 0),
            "water_mgal_per_year": fmt(water_mgal, 1),
            "water_estimate_basis": water_basis,
            "confidence": confidence,
            "consistency": consistency,
            "basis": "; ".join(basis_parts),
            "source_url": site.get("source_url", ""),
            "platform_source_url": platform_source,
        })

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLS)
        writer.writeheader()
        writer.writerows(out)

    numeric_fields = {
        "platform_count", "accelerator_count", "tdp_w", "tdp_w_low", "tdp_w_high",
        "accelerator_heat_mw", "accelerator_heat_mw_low", "accelerator_heat_mw_high",
        "accelerator_heat_share_pct", "it_load_mw", "cooling_thermal_load_mw",
        "pue_used", "cooling_electric_mw", "water_l_per_year", "water_mgal_per_year",
    }
    json_rows = []
    for row in out:
        item = {}
        for key, value in row.items():
            if key in numeric_fields:
                item[key] = as_float(value)
            else:
                item[key] = value
        json_rows.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as handle:
        json.dump(json_rows, handle, ensure_ascii=False, indent=1)

    # ---- validation ----
    if len(out) != len(sites):
        sys.exit(f"Row count mismatch: {len(out)} output vs {len(sites)} input")
    names = [row["name"] for row in out]
    if len(names) != len(set(names)):
        sys.exit("Duplicate site names in output")

    print(f"Wrote {OUT_CSV} and {OUT_JSON}")
    print(f"Sites: {len(out)}")
    print(f"  with named accelerator platform: {sum(1 for r in out if r['platform_ids'])}")
    print(f"  with announced accelerator count: {sum(1 for r in out if r['accelerator_count'] != '')}")
    print(f"  with accelerator heat estimate:   {sum(1 for r in out if r['accelerator_heat_mw_low'] != '')}"
          f" ({sum(1 for r in out if r['accelerator_heat_mw'] != '')} single-TDP,"
          f" {sum(1 for r in out if r['accelerator_heat_mw'] == '' and r['accelerator_heat_mw_low'] != '')} ranged)")
    print(f"  with IT load / thermal load:      {sum(1 for r in out if r['it_load_mw'] != '')}")
    print(f"  with cooling electricity:         {sum(1 for r in out if r['cooling_electric_mw'] != '')}")
    print(f"  with fleet-scaled water estimate: {sum(1 for r in out if r['water_l_per_year'] != '')}")
    print("Confidence:", {grade: sum(1 for r in out if r['confidence'] == grade) for grade in "ABCD"})
    print("Rack cooling:", {value: sum(1 for r in out if r['rack_cooling'] == value)
                           for value in sorted({r['rack_cooling'] for r in out})})
    print("Heat rejection:", {value: sum(1 for r in out if r['heat_rejection'] == value)
                              for value in sorted({r['heat_rejection'] for r in out})})
    if warnings:
        print("WARNINGS:")
        for warning in warnings[:20]:
            print("  ", warning)
    else:
        print("No accelerator-heat > IT-load inconsistencies.")

    # Refresh the dashboard so index.html embeds the dataset just written.
    import dashboard
    dashboard.render()


if __name__ == "__main__":
    main()
