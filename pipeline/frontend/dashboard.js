(() => {
  "use strict";

  const STATUS = {
    operational: { label: "Operational", long: "Fully operational", color: "#45d483" },
    partially_operational: { label: "Partial", long: "Partially operational", color: "#e8c653" },
    under_construction: { label: "Construction", long: "Under construction", color: "#68a8f8" },
    planned: { label: "Planned", long: "Planned / announced", color: "#b58af2" },
    unknown: { label: "Unknown", long: "Unknown status", color: "#9ca3af" }
  };
  const METHODS = {
    gpu_count: "GPU count",
    third_party: "Third-party",
    flops: "Peak FLOPS",
    power: "Power estimate"
  };
  const OPERATOR_COLORS = {
    Google: "#e7a84d",
    Meta: "#69a9ef",
    Microsoft: "#57c5b6",
    AWS: "#e4cc58",
    Nebius: "#b58af2",
    Crusoe: "#ed8d78"
  };

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const esc = (value) => String(value ?? "").replace(/[&<>'"]/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[char]);
  const safeUrl = (value) => /^https?:\/\//i.test(value || "") ? esc(value) : "#";
  const num = (value, digits = 0) => value == null || Number.isNaN(Number(value))
    ? "—"
    : Number(value).toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits });
  // Explicit solid tints avoid the fill-opacity compositing artefact that
  // renders a solid core inside a translucent circle in Chrome.
  const hexToRgb = hex => {
    const value = hex.replace("#", "");
    return [0, 2, 4].map(i => parseInt(value.slice(i, i + 2), 16));
  };
  const tint = (hex, white = 0.6) => {
    const [r, g, b] = hexToRgb(hex);
    const mix = c => Math.round(c + (255 - c) * white);
    return `rgb(${mix(r)},${mix(g)},${mix(b)})`;
  };
  const compact = (value, digits = 1) => {
    if (value == null || !Number.isFinite(Number(value))) return "—";
    const n = Number(value);
    if (Math.abs(n) >= 1e6) return `${(n / 1e6).toFixed(digits)}M`;
    if (Math.abs(n) >= 1e3) return `${(n / 1e3).toFixed(n >= 1e5 ? 0 : digits)}k`;
    return n.toLocaleString("en-US", { maximumFractionDigits: digits });
  };
  const powerOf = d => d.power_capacity_mw ?? d.it_load_mw ?? null;
  const locationOf = d => [d.city, d.state_province, d.country].filter(Boolean).join(", ");
  const statusOf = d => STATUS[d.status] || STATUS.unknown;
  const operatorColor = name => OPERATOR_COLORS[name] || "#82dfb5";

  /* ---------- Dataset summary ---------- */
  const totalPower = DATA.reduce((sum, d) => sum + (powerOf(d) || 0), 0);
  const countries = [...new Set(DATA.map(d => d.country).filter(Boolean))].sort();
  const statusCounts = Object.keys(STATUS).reduce((acc, key) => {
    acc[key] = DATA.filter(d => (d.status || "unknown") === key).length;
    return acc;
  }, {});

  // Capacity (MW) by status: the headline for a community reader. Same
  // convention as the country table: gross power where published, else IT load.
  const powerByStatus = (rows) => Object.keys(STATUS).reduce((acc, key) => {
    acc[key] = rows.filter(d => (d.status || "unknown") === key).reduce((sum, d) => sum + (powerOf(d) || 0), 0);
    return acc;
  }, {});
  const pct = (part, whole) => whole ? Math.round(part / whole * 100) : 0;
  const worldMW = powerByStatus(DATA);
  const usMW = powerByStatus(DATA.filter(d => d.country === "United States"));
  const pipelineShare = (mw, total) => pct(mw.planned + mw.under_construction, total);
  const totalUS = Object.values(usMW).reduce((a, b) => a + b, 0);
  const worldPipeline = `${pipelineShare(worldMW, totalPower)}%`;

  $("#hero-total").textContent = num(totalPower / 1000, 1);
  $("#hero-sites").textContent = num(DATA.length);
  $("#hero-pipeline-text").textContent = worldPipeline;
  $("#thesis-pipeline").textContent = worldPipeline;
  $("#hero-share").textContent = `${worldPipeline} planned or under construction`;
  $("#stat-us").textContent = `${num(totalUS / 1000, 1)} GW`;
  $("#stat-us-pipeline").textContent = `${pipelineShare(usMW, totalUS)}%`;
  $("#stat-countries").textContent = num(countries.length);
  $("#stat-operational").textContent = `${pct(worldMW.operational, totalPower)}%`;

  const activeStatusKeys = Object.keys(STATUS).filter(key => statusCounts[key]);
  $("#hero-status-stack").innerHTML = activeStatusKeys.map(key =>
    `<span style="width:${worldMW[key] / totalPower * 100}%;background:${STATUS[key].color}" title="${STATUS[key].long}: ${num(worldMW[key] / 1000, 1)} GW, ${statusCounts[key]} sites"></span>`
  ).join("");
  $("#hero-status-key").innerHTML = activeStatusKeys.map(key =>
    `<div><i style="background:${STATUS[key].color}"></i><span>${STATUS[key].label}</span><b>${num(worldMW[key] / 1000, 1)} GW</b></div>`
  ).join("");

  /* ---------- Reveal motion ---------- */
  const revealItems = $$(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06, rootMargin: "0px 0px -30px" });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add("visible"));
  }

  /* ---------- Atlas filters and map ---------- */
  const activeStatuses = new Set(activeStatusKeys);
  let selectedSite = null;
  let filteredSites = [...DATA];
  let visibleCount = 10;
  let map = null;
  let markerLayer = null;
  const markerBySite = new Map();

  $("#country-filter").insertAdjacentHTML("beforeend", countries.map(country =>
    `<option value="${esc(country)}">${esc(country)}</option>`
  ).join(""));

  function renderStatusFilters() {
    $("#status-filters").innerHTML = activeStatusKeys.map(key => `
      <button class="status-filter ${activeStatuses.has(key) ? "active" : ""}" type="button"
        data-status="${key}" aria-pressed="${activeStatuses.has(key)}">
        <i style="background:${STATUS[key].color}"></i>${STATUS[key].long}<b>${statusCounts[key]}</b>
      </button>`).join("");
  }

  function getFilteredSites() {
    const query = $("#site-search").value.trim().toLowerCase();
    const country = $("#country-filter").value;
    return DATA.filter(d => {
      const matchesQuery = !query || [d.name, d.operator, d.city, d.state_province, d.country]
        .filter(Boolean).join(" ").toLowerCase().includes(query);
      return matchesQuery && (!country || d.country === country) && activeStatuses.has(d.status || "unknown");
    });
  }

  if (window.L) {
    const canvasRenderer = L.canvas({ padding: 0.4 });
    map = L.map("map", { renderer: canvasRenderer, zoomControl: false, worldCopyJump: true, minZoom: 2 })
      .setView([27, 8], 2.35);
    L.control.zoom({ position: "bottomright" }).addTo(map);
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
      attribution: "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ",
      maxZoom: 16
    }).addTo(map);
    markerLayer = L.layerGroup().addTo(map);
  } else {
    $("#map").innerHTML = '<div style="padding:40px;color:#b7c4b9">The map library could not load. The leaderboard and all site details remain available below.</div>';
  }

  function markerValue(d) {
    return $("#size-metric").value === "h100e_best" ? d.h100e_best : powerOf(d);
  }

  // Sites that share one (often city-centre) point would stack into a single
  // clickable marker. Spread each such group on a small ring (~4 km) so every
  // site can be selected once the map is zoomed in. The order comes from the
  // full dataset, so a marker does not jump when the filters change. The
  // panel tells the reader the point is approximate.
  const pointKey = d => `${d.latitude.toFixed(2)}|${d.longitude.toFixed(2)}`;
  const displayPoint = new Map();
  {
    const groups = new Map();
    DATA.filter(d => d.latitude != null && d.longitude != null).forEach(d => {
      const key = pointKey(d);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(d);
    });
    groups.forEach(sites => {
      sites.sort((a, b) => a.name.localeCompare(b.name));
      sites.forEach((d, i) => {
        if (sites.length === 1) { displayPoint.set(d.name, [d.latitude, d.longitude]); return; }
        const angle = 2 * Math.PI * i / sites.length;
        const r = 0.04;
        const lngScale = Math.max(Math.cos(d.latitude * Math.PI / 180), 0.2);
        displayPoint.set(d.name, [d.latitude + r * Math.sin(angle), d.longitude + r * Math.cos(angle) / lngScale]);
      });
    });
  }

  function updateMarkers() {
    markerBySite.clear();
    if (!map || !markerLayer) return;
    markerLayer.clearLayers();
    const metric = $("#size-metric").value;
    const maxValue = Math.max(...DATA.map(d => markerValue(d) || 0), 1);
    filteredSites.forEach(d => {
      if (d.latitude == null || d.longitude == null) return;
      const value = markerValue(d);
      const radius = value ? 4 + 12 * Math.sqrt(value / maxValue) : 3.5;
      const selected = selectedSite && selectedSite.name === d.name;
      const status = statusOf(d);
      const marker = L.circleMarker(displayPoint.get(d.name), {
        radius: selected ? radius + 2 : radius,
        color: selected ? "#ffffff" : status.color,
        weight: selected ? 2.5 : 1,
        fillColor: status.color,
        fillOpacity: selected ? 0.95 : 0.65
      });
      const valueLabel = metric === "power"
        ? `${value ? num(value) : "Unknown"} MW`
        : `${value ? compact(value) : "Unknown"} H100e`;
      marker.bindTooltip(`<strong>${esc(d.name)}</strong><span>${esc(valueLabel)}</span>`, {
        direction: "top", offset: [0, -5], className: "site-tooltip", opacity: 1
      });
      marker.on("click", () => selectSite(d, false));
      marker.addTo(markerLayer);
      markerBySite.set(d.name, marker);
    });
  }

  function panelList(sites) {
    const top = [...sites].sort((a, b) => (powerOf(b) || 0) - (powerOf(a) || 0)).slice(0, 6);
    if (!top.length) {
      return '<div class="panel-kicker"><span>NO MATCHES</span></div><h3 class="panel-title">Nothing fits those filters.</h3><p class="panel-list-intro">Try another country, status, or search term.</p>';
    }
    return `
      <div class="panel-kicker"><span>AT A GLANCE</span><span>TOP ${top.length}</span></div>
      <h3 class="panel-title">${sites.length === DATA.length ? "The largest requests for power" : "Your selection"}</h3>
      <p class="panel-list-intro">The largest sites in the current filter, by stated power. Select a campus to see its status, its note and its source.</p>
      <div class="panel-site-list">${top.map((d, index) => `
        <button class="panel-site-item" type="button" data-site="${esc(d.name)}">
          <span class="rank">${String(index + 1).padStart(2, "0")}</span>
          <span><strong>${esc(d.name)}</strong><small>${esc(d.country)}</small></span>
          <b>${powerOf(d) != null ? `${num(powerOf(d))} MW` : "—"}</b>
        </button>`).join("")}</div>`;
  }

  function panelDetail(d) {
    const status = statusOf(d);
    const note = d.status_note || "This row has no additional site note.";
    const longNote = note.length > 270;
    return `
      <div class="panel-kicker"><span>SITE PROFILE</span><button type="button" data-close-site aria-label="Close site profile">×</button></div>
      <h3 class="panel-title">${esc(d.name)}</h3>
      <p class="panel-location">${esc(d.operator)}<br>${esc(locationOf(d))}</p>
      ${d.location_shared_with > 0 ? `<p class="panel-approx">Approximate location. ${d.location_shared_with === 1 ? "One other site uses" : `${d.location_shared_with} other sites use`} this map point, so the coordinates are probably a city centre, not the campus.</p>` : ""}
      <span class="panel-status"><i style="background:${status.color}"></i>${status.long}</span>
      <div class="panel-hero-metric">
        <strong>${powerOf(d) != null ? num(powerOf(d)) : "—"}</strong><small>MW</small>
        <p>${powerOf(d) == null ? "No power figure published" : d.power_capacity_mw != null ? `Stated gross power · ${d.status === "operational" ? "capacity, not average draw" : "a request, not a load yet"}` : "IT load only · gross power not published"}</p>
      </div>
      <div class="panel-metrics">
        <div><span>IT LOAD</span><b>${d.it_load_mw != null ? `${num(d.it_load_mw)} MW` : "Not published"}</b></div>
        <div><span>COMPUTE (H100e)</span><b>${d.h100e_best ? `${num(d.h100e_best)} · ${METHODS[d.h100e_method] || esc(d.h100e_method)}` : "No estimate"}</b></div>
        <div><span>ANNOUNCED GPUs</span><b>${d.announced_gpu_count != null ? num(d.announced_gpu_count) : "Not published"}</b></div>
        <div><span>ACCELERATORS</span><b>${esc(d.gpu_types || "Not published")}</b></div>
      </div>
      <div class="panel-note" id="panel-note"><span>RESEARCH NOTE</span><p>${esc(note)}</p>${longNote ? '<button type="button" data-expand-note>Read the full note ↓</button>' : ""}</div>
      <a class="source-button" href="${safeUrl(d.source_url)}" target="_blank" rel="noopener noreferrer"><span>Open the primary source</span><span>↗</span></a>`;
  }

  function selectSite(d, moveMap = true) {
    selectedSite = d;
    $("#site-panel").innerHTML = panelDetail(d);
    updateMarkers();
    if (map && moveMap && d.latitude != null && d.longitude != null) {
      map.flyTo(displayPoint.get(d.name), Math.max(map.getZoom(), 5), { duration: 0.65 });
      const marker = markerBySite.get(d.name);
      if (marker) marker.openTooltip();
    }
  }

  function renderRanking() {
    const sorted = [...filteredSites].sort((a, b) => (powerOf(b) || 0) - (powerOf(a) || 0));
    const max = Math.max(...sorted.map(d => powerOf(d) || 0), 1);
    const shown = sorted.slice(0, visibleCount);
    $("#site-ranking").innerHTML = shown.length ? shown.map((d, index) => {
      const status = statusOf(d);
      return `<tr>
        <td><button class="site-name-button" type="button" data-site="${esc(d.name)}"><span class="rank-num">${String(index + 1).padStart(2, "0")}</span>${esc(d.name)}<small>${esc(d.country)} · ${esc(d.operator)}</small></button></td>
        <td><span class="table-status"><i style="background:${status.color}"></i>${status.label}</span></td>
        <td>${d.it_load_mw != null ? `${num(d.it_load_mw)} MW` : "—"}</td>
        <td class="estimate-cell">${powerOf(d) != null ? `${num(powerOf(d))} MW` : "—"}<div class="estimate-bar" style="width:${(powerOf(d) || 0) / max * 100}%"></div></td>
        <td class="method-cell">${d.h100e_best ? `${compact(d.h100e_best)} · ${METHODS[d.h100e_method] || "—"}` : "—"}</td>
      </tr>`;
    }).join("") : '<tr><td colspan="5" class="empty-row">No sites match the current filters.</td></tr>';
    const more = $("#show-more-sites");
    more.hidden = sorted.length <= 10;
    more.innerHTML = visibleCount >= sorted.length
      ? `Show the first 10 sites <span aria-hidden="true">↑</span>`
      : `Show more sites <span aria-hidden="true">↓</span> <span style="color:#60776a">${Math.min(visibleCount, sorted.length)} / ${sorted.length}</span>`;
  }

  function updateAtlas() {
    filteredSites = getFilteredSites();
    if (selectedSite && !filteredSites.some(d => d.name === selectedSite.name)) selectedSite = null;
    $("#map-count").textContent = `${filteredSites.length} site${filteredSites.length === 1 ? "" : "s"}`;
    $("#filter-summary").textContent = filteredSites.length === DATA.length
      ? `Showing all ${DATA.length} sites in ${countries.length} countries.`
      : `Showing ${filteredSites.length} of ${DATA.length} sites. The selection holds ${num(filteredSites.reduce((sum, d) => sum + (powerOf(d) || 0), 0) / 1000, 1)} GW of stated power.`;
    if (!selectedSite) $("#site-panel").innerHTML = panelList(filteredSites);
    updateMarkers();
    renderRanking();
  }

  renderStatusFilters();
  updateAtlas();

  $("#status-filters").addEventListener("click", event => {
    const button = event.target.closest("[data-status]");
    if (!button) return;
    const key = button.dataset.status;
    if (activeStatuses.has(key)) activeStatuses.delete(key); else activeStatuses.add(key);
    visibleCount = 10;
    renderStatusFilters();
    updateAtlas();
  });
  ["site-search", "country-filter", "size-metric"].forEach(id => {
    $(`#${id}`).addEventListener(id === "site-search" ? "input" : "change", () => {
      visibleCount = 10;
      updateAtlas();
    });
  });
  $("#reset-filters").addEventListener("click", () => {
    $("#site-search").value = "";
    $("#country-filter").value = "";
    $("#size-metric").value = "power";
    activeStatusKeys.forEach(key => activeStatuses.add(key));
    selectedSite = null;
    visibleCount = 10;
    renderStatusFilters();
    updateAtlas();
    if (map) map.setView([27, 8], 2.35);
  });
  $("#site-panel").addEventListener("click", event => {
    const siteButton = event.target.closest("[data-site]");
    const closeButton = event.target.closest("[data-close-site]");
    const expandButton = event.target.closest("[data-expand-note]");
    if (siteButton) {
      const d = DATA.find(site => site.name === siteButton.dataset.site);
      if (d) selectSite(d, true);
    }
    if (closeButton) {
      selectedSite = null;
      $("#site-panel").innerHTML = panelList(filteredSites);
      updateMarkers();
    }
    if (expandButton) {
      const note = $("#panel-note");
      note.classList.toggle("expanded");
      expandButton.textContent = note.classList.contains("expanded") ? "Collapse the note ↑" : "Read the full note ↓";
    }
  });
  $("#site-ranking").addEventListener("click", event => {
    const button = event.target.closest("[data-site]");
    if (!button) return;
    const d = DATA.find(site => site.name === button.dataset.site);
    if (d) {
      selectSite(d, true);
      $(".atlas-grid").scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
  $("#show-more-sites").addEventListener("click", () => {
    visibleCount = visibleCount >= filteredSites.length ? 10 : visibleCount + 10;
    renderRanking();
  });
  $("#export-filtered").addEventListener("click", () => {
    if (!filteredSites.length) return;
    const columns = Object.keys(DATA[0]);
    const quote = value => `"${String(value ?? "").replace(/"/g, '""')}"`;
    const csv = [columns.join(","), ...filteredSites.map(d => columns.map(col => quote(d[col])).join(","))].join("\n");
    const url = URL.createObjectURL(new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "compute-atlas-selection.csv";
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  /* ---------- Operator efficiency chart ---------- */
  const plottableOperators = OPERATORS.filter(d => d.pue_value != null && d.wue_value != null);
  let operatorFilter = "all";
  let selectedOperator = "Meta";

  function filteredOperators() {
    return plottableOperators.filter(d => {
      if (operatorFilter === "hyperscaler") return d.category === "hyperscaler";
      if (operatorFilter === "reported") return d.pue_kind !== "design";
      return true;
    });
  }

  function renderFindings() {
    const hyperscalers = OPERATORS.filter(d => d.category === "hyperscaler" && d.disclosure_grade === "A");
    const pueWinner = [...hyperscalers].filter(d => d.pue_value != null).sort((a, b) => a.pue_value - b.pue_value)[0];
    const wueWinner = [...hyperscalers].filter(d => d.wue_value != null).sort((a, b) => a.wue_value - b.wue_value)[0];
    if (pueWinner) {
      $("#finding-pue").textContent = num(pueWinner.pue_value, 2);
      $("#finding-pue-label").textContent = `${pueWinner.operator} · ${pueWinner.metric_year}`;
    }
    if (wueWinner) {
      $("#finding-wue").textContent = `${num(wueWinner.wue_value, 2)} L`;
      $("#finding-wue-label").textContent = `${wueWinner.operator} · per IT kWh, ${wueWinner.metric_year}`;
    }
  }

  function renderOperatorDetail(name) {
    const d = OPERATORS.find(operator => operator.operator === name) || plottableOperators[0];
    if (!d) return;
    selectedOperator = d.operator;
    const overhead = d.pue_value != null ? Math.round((d.pue_value - 1) * 100) : null;
    $("#operator-detail").innerHTML = `
      <div class="operator-top"><p class="mini-label">SELECTED PROFILE</p><span class="grade-badge" title="Disclosure grade ${esc(d.disclosure_grade)}">${esc(d.disclosure_grade)}</span></div>
      <div class="operator-name-row"><i class="operator-swatch" style="background:${operatorColor(d.operator)}"></i><h3 class="operator-name">${esc(d.operator)}</h3></div>
      <p class="operator-year">${esc(d.metric_year)} · ${esc(d.category)}</p>
      <div class="operator-metrics">
        <div class="operator-metric"><span>PUE</span><strong>${d.pue_value != null ? num(d.pue_value, 2) : "ND"}</strong><small>facility / IT energy</small></div>
        <div class="operator-metric"><span>WUE</span><strong>${d.wue_value != null ? num(d.wue_value, 3) : "ND"}</strong><small>litres / IT kWh</small></div>
      </div>
      <p class="operator-overhead">${overhead != null ? `<strong>${overhead} units</strong> of non-IT facility overhead for every 100 units of IT energy.` : "The operator does not disclose PUE, so we cannot calculate facility overhead."}<br>Water normalizer: <strong>${d.water_value != null ? compact(d.water_value) : "—"} gal</strong> per MW-year.</p>
      <div class="operator-scope"><span>PUE BOUNDARY</span><p>${esc(d.pue_scope)}</p></div>
      <div class="operator-scope"><span>WUE BASIS</span><p>${esc(d.wue_basis)}</p></div>
      <div class="operator-scope"><span>REPORTING CAVEAT</span><p class="operator-note">${esc(d.notes)}</p></div>
      <a class="operator-source" href="${safeUrl(d.source_url)}" target="_blank" rel="noopener noreferrer"><span>View the company disclosure</span><span>↗</span></a>`;
  }

  function renderEfficiencyChart() {
    const svg = $("#efficiency-chart");
    const data = filteredOperators();
    const W = 760, H = 470;
    const margin = { top: 38, right: 42, bottom: 70, left: 72 };
    const innerW = W - margin.left - margin.right;
    const innerH = H - margin.top - margin.bottom;
    const xMin = 1, xMax = 1.45, yMin = 0.001, yMax = 2;
    const x = value => margin.left + (value - xMin) / (xMax - xMin) * innerW;
    const y = value => margin.top + (Math.log10(yMax) - Math.log10(value)) / (Math.log10(yMax) - Math.log10(yMin)) * innerH;
    const xTicks = [1, 1.1, 1.2, 1.3, 1.4];
    const yTicks = [0.001, 0.01, 0.1, 1, 2];
    const labelOffsets = {
      Google: [13, -10], Meta: [13, -10], AWS: [13, 20], Microsoft: [13, -10],
      Nebius: [13, -11], Crusoe: [13, 20]
    };

    let content = `
      <rect x="${margin.left}" y="${margin.top}" width="${innerW}" height="${innerH}" fill="#f6f8f2" rx="8"/>
      ${yTicks.map(tick => `<line class="chart-grid" x1="${margin.left}" x2="${W - margin.right}" y1="${y(tick)}" y2="${y(tick)}"/><text class="chart-axis-label" x="${margin.left - 13}" y="${y(tick) + 3}" text-anchor="end">${tick}</text>`).join("")}
      ${xTicks.map(tick => `<line class="chart-grid" y1="${margin.top}" y2="${H - margin.bottom}" x1="${x(tick)}" x2="${x(tick)}"/><text class="chart-axis-label" x="${x(tick)}" y="${H - margin.bottom + 23}" text-anchor="middle">${tick.toFixed(1)}</text>`).join("")}
      <text class="chart-axis-title" x="${margin.left + innerW / 2}" y="${H - 16}" text-anchor="middle">PUE · LOWER ENERGY OVERHEAD ←</text>
      <text class="chart-axis-title" transform="translate(18 ${margin.top + innerH / 2}) rotate(-90)" text-anchor="middle">WUE (L/kWh) · LOG SCALE</text>
      <text class="chart-sub-label" x="${margin.left + 12}" y="${margin.top + 19}">MORE WATER INTENSITY ↑</text>
      <text class="chart-sub-label" x="${W - margin.right - 12}" y="${H - margin.bottom - 12}" text-anchor="end">BETTER ON BOTH ↙</text>`;

    content += data.map(d => {
      const px = x(d.pue_value), py = y(d.wue_value);
      const [dx, dy] = labelOffsets[d.operator] || [12, -10];
      const design = d.pue_kind === "design";
      const color = operatorColor(d.operator);
      return `<g>
        <circle class="chart-point" data-operator="${esc(d.operator)}" tabindex="0" role="button"
          aria-label="${esc(d.operator)}: PUE ${esc(d.pue)}, WUE ${esc(d.wue_l_per_kwh)} litres per kilowatt-hour"
          cx="${px}" cy="${py}" r="${d.operator === selectedOperator ? 9 : 7}" fill="${color}" fill-opacity=".9"
          stroke="${d.operator === selectedOperator ? "#17221c" : "#fbfcf8"}" stroke-width="${d.operator === selectedOperator ? 3 : 2}"
          stroke-dasharray="${design ? "3 2" : "none"}"/>
        <text class="chart-label" x="${px + dx}" y="${py + dy}">${esc(d.operator)}</text>
        <text class="chart-sub-label" x="${px + dx}" y="${py + dy + 12}">${num(d.pue_value, 2)} / ${num(d.wue_value, 3)}</text>
      </g>`;
    }).join("");
    svg.innerHTML = `<title id="chart-title">Operator PUE and WUE comparison</title><desc id="chart-desc">Scatter plot of operators with both power and water usage effectiveness values. Lower values are better. Select a point to read its scope and reporting caveats.</desc>${content}`;
    $("#chart-coverage").textContent = `${data.length} shown. ${OPERATORS.length - plottableOperators.length} operators lack a complete pair.`;

    $$(".chart-point", svg).forEach(point => {
      const showTooltip = event => {
        const d = OPERATORS.find(operator => operator.operator === point.dataset.operator);
        const wrap = $("#efficiency-chart-wrap").getBoundingClientRect();
        const rect = point.getBoundingClientRect();
        const clientX = event.clientX || rect.left + rect.width / 2;
        const clientY = event.clientY || rect.top;
        const tooltip = $("#chart-tooltip");
        tooltip.innerHTML = `<strong>${esc(d.operator)}</strong><span>PUE ${esc(d.pue)}</span><span>WUE ${esc(d.wue_l_per_kwh)} L/kWh</span>`;
        tooltip.style.left = `${clientX - wrap.left}px`;
        tooltip.style.top = `${clientY - wrap.top - 8}px`;
        tooltip.classList.add("visible");
      };
      point.addEventListener("mouseenter", showTooltip);
      point.addEventListener("mousemove", showTooltip);
      point.addEventListener("focus", showTooltip);
      point.addEventListener("mouseleave", () => $("#chart-tooltip").classList.remove("visible"));
      point.addEventListener("blur", () => $("#chart-tooltip").classList.remove("visible"));
      point.addEventListener("click", () => {
        renderOperatorDetail(point.dataset.operator);
        renderEfficiencyChart();
      });
      point.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          renderOperatorDetail(point.dataset.operator);
          renderEfficiencyChart();
        }
      });
    });
  }

  function renderOperatorTable() {
    $("#operator-table").innerHTML = OPERATORS.map(d => `<tr>
      <td>${esc(d.operator)}</td><td>${esc(d.metric_year)}</td><td>${esc(d.pue)}</td><td>${esc(d.wue_l_per_kwh)}</td>
      <td><span class="table-grade" title="Disclosure grade ${esc(d.disclosure_grade)}">${esc(d.disclosure_grade)}</span></td>
      <td>${esc(d.pue_scope)}</td></tr>`).join("");
  }

  $("#operator-filter").addEventListener("click", event => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    operatorFilter = button.dataset.filter;
    $$("button", $("#operator-filter")).forEach(item => item.classList.toggle("active", item === button));
    renderEfficiencyChart();
  });

  renderFindings();
  renderOperatorDetail(selectedOperator);
  renderEfficiencyChart();
  renderOperatorTable();

  /* ---------- Site-level efficiency ---------- */
  const REJECTION_COLORS = {
    evaporative: "#e7a84d",
    hybrid: "#69a9ef",
    dry_closed_loop: "#57c5b6",
    unknown: "#9ca3af"
  };
  const REJECTION_LABELS = {
    evaporative: "Evaporative",
    hybrid: "Hybrid",
    dry_closed_loop: "Dry / closed loop",
    unknown: "Unknown"
  };
  const RACK_LABELS = {
    air: "Air",
    air_or_dlc: "Air or DLC",
    dlc: "Direct-to-chip",
    dlc_capable: "DLC-capable",
    hybrid: "Hybrid",
    immersion: "Immersion",
    unknown: "Unknown"
  };

  // A PUE of 1.2 is the industry default we apply when nothing is disclosed.
  // It is an assumption, so it never counts as site evidence here.
  const hasPue = c => c.pue_disclosed === true;
  const hasWater = c => c.water_ml_per_mw_year != null;
  // xAI publishes no WUE: its water figure multiplies a stated 1.0 L/kWh
  // estimate. That is a weaker claim than an operator disclosure, so it is
  // marked in the ledger rather than shown as if it were measured.
  const assumedWue = c => /estimate/i.test(c.water_estimate_basis || "");
  const drySites = COOLING.filter(c => hasWater(c) && c.water_ml_per_mw_year === 0);
  const scoredBoth = COOLING.filter(c => hasPue(c) && hasWater(c) && c.water_ml_per_mw_year > 0);

  function renderCoverage() {
    const total = COOLING.length || DATA.length;
    const cards = [
      { n: total, label: "sites tracked" },
      { n: COOLING.filter(c => c.it_load_mw != null).length, label: "with a power denominator" },
      { n: COOLING.filter(hasPue).length, label: "with operator-disclosed PUE" },
      { n: COOLING.filter(hasWater).length, label: "with a water intensity" },
      { n: COOLING.filter(c => c.accelerator_heat_mw_low != null).length, label: "with an accelerator heat estimate" },
      { n: COOLING.filter(c => c.it_load_mw == null).length, label: "no power denominator", cls: "muted" }
    ];
    $("#coverage-strip").innerHTML = cards.map(card => `
      <div class="coverage-card ${card.cls || ""}">
        <div class="coverage-value"><strong>${num(card.n)}</strong><span>${Math.round(card.n / total * 100)}%</span></div>
        <div class="coverage-track"><i style="width:${card.n / total * 100}%"></i></div>
        <p>${card.label}</p>
      </div>`).join("");
  }

  let siteWaterFilter = "all";

  function filteredSitePoints() {
    return scoredBoth.filter(c => siteWaterFilter === "all" || c.heat_rejection === siteWaterFilter);
  }

  // The scorable campuses sit on only a handful of distinct (PUE, water)
  // positions, because both numbers are operator-level. Grouping identical
  // positions and sizing by site count makes that clustering visible instead
  // of hiding it under overlapping dots. Two campuses only share a position if
  // the chart cannot tell them apart. The key is therefore the rounded pixel
  // position, not the raw value: operator water intensities differ in the
  // fourth decimal (8.9345 vs 8.9394) because each site divides its own water
  // total by its own IT load, and value equality would stack two bubbles on
  // one pixel.
  function groupedSitePoints(data, project) {
    const groups = new Map();
    data.forEach(c => {
      const { px, py } = project(c);
      const key = `${Math.round(px)}|${Math.round(py)}|${c.heat_rejection}`;
      if (!groups.has(key)) {
        groups.set(key, {
          pue: c.pue_used,
          water: c.water_ml_per_mw_year,
          rejection: c.heat_rejection,
          sites: []
        });
      }
      groups.get(key).sites.push(c);
    });
    return [...groups.values()].map(g => ({
      ...g,
      pue: g.sites.reduce((sum, c) => sum + c.pue_used, 0) / g.sites.length,
      water: g.sites.reduce((sum, c) => sum + c.water_ml_per_mw_year, 0) / g.sites.length
    })).sort((a, b) => b.sites.length - a.sites.length);
  }

  function renderSiteChart() {
    const svg = $("#site-efficiency-chart");
    if (!svg) return;
    const data = filteredSitePoints();
    const W = 760, H = 470;
    const margin = { top: 38, right: 46, bottom: 74, left: 78 };
    const innerW = W - margin.left - margin.right;
    const innerH = H - margin.top - margin.bottom;
    const xMin = 1.05, xMax = 1.32;
    const yMin = 0.01, yMax = 20;
    const x = v => margin.left + (v - xMin) / (xMax - xMin) * innerW;
    const y = v => margin.top + (Math.log10(yMax) - Math.log10(v)) / (Math.log10(yMax) - Math.log10(yMin)) * innerH;
    const groups = groupedSitePoints(data, c => ({
      px: x(Math.min(Math.max(c.pue_used, xMin), xMax)),
      py: y(Math.min(Math.max(c.water_ml_per_mw_year, yMin), yMax))
    }));
    const xTicks = [1.05, 1.10, 1.15, 1.20, 1.25, 1.30];
    const yTicks = [0.01, 0.1, 1, 10];
    const maxSites = Math.max(...groups.map(g => g.sites.length), 1);
    const radius = n => 8 + 22 * Math.sqrt(n / maxSites);

    let content = `
      <rect x="${margin.left}" y="${margin.top}" width="${innerW}" height="${innerH}" fill="#f6f8f2" rx="8"/>
      ${yTicks.map(t => `<line class="chart-grid" x1="${margin.left}" x2="${W - margin.right}" y1="${y(t)}" y2="${y(t)}"/><text class="chart-axis-label" x="${margin.left - 13}" y="${y(t) + 3}" text-anchor="end">${t}</text>`).join("")}
      ${xTicks.map(t => `<line class="chart-grid" y1="${margin.top}" y2="${H - margin.bottom}" x1="${x(t)}" x2="${x(t)}"/><text class="chart-axis-label" x="${x(t)}" y="${H - margin.bottom + 23}" text-anchor="middle">${t.toFixed(2)}</text>`).join("")}
      <text class="chart-axis-title" x="${margin.left + innerW / 2}" y="${H - 18}" text-anchor="middle">POWER USAGE EFFECTIVENESS · LOWER ←</text>
      <text class="chart-axis-title" transform="translate(20 ${margin.top + innerH / 2}) rotate(-90)" text-anchor="middle">WATER · ML PER MW IT-YEAR (LOG)</text>
      <text class="chart-sub-label" x="${margin.left + 12}" y="${margin.top + 19}">MORE WATER ↑</text>
      <text class="chart-sub-label" x="${margin.left + 12}" y="${H - margin.bottom - 12}">BETTER ↙</text>`;

    const bubbles = groups.map((g, i) => {
      const cx = x(Math.min(Math.max(g.pue, xMin), xMax));
      const cy = y(Math.min(Math.max(g.water, yMin), yMax));
      const r = radius(g.sites.length);
      const color = REJECTION_COLORS[g.rejection] || REJECTION_COLORS.unknown;
      const operators = [...new Set(g.sites.map(s => s.operator))].slice(0, 2).join(", ");
      return `<g class="site-group" data-index="${i}" tabindex="0" role="button"
        aria-label="${g.sites.length} sites at PUE ${num(g.pue, 2)} and ${num(g.water, 2)} megalitres per MW-year: ${esc(operators)}">
        <circle class="chart-point site-point" cx="${cx}" cy="${cy}" r="${r}" fill="${tint(color, 0.62)}" stroke="${color}" stroke-width="1.6"/>
        ${g.sites.length > 1 ? `<text class="site-count" x="${cx}" y="${cy + 4}" text-anchor="middle">${g.sites.length}</text>` : ""}
      </g>`;
    }).join("");
    // The static frame goes in first, then the bubbles are appended, so the
    // tooltip wiring below always attaches to freshly parsed nodes.
    svg.innerHTML = `<title id="site-chart-title">Site PUE and water intensity</title><desc id="site-chart-desc">Each bubble is a distinct combination of operator-disclosed PUE and water intensity. Bubble area is the number of campuses at that position.</desc>${content}`;
    svg.insertAdjacentHTML("beforeend", bubbles);
    $("#site-chart-coverage").textContent = `${data.length} sites in ${groups.length} distinct positions. Size shows the number of sites.`;
    $("#site-chart-legend").innerHTML = ["evaporative", "hybrid", "dry_closed_loop", "unknown"].map(key => {
      const n = data.filter(c => (c.heat_rejection || "unknown") === key).length;
      if (!n) return "";
      return `<span><i style="background:${REJECTION_COLORS[key]}"></i>${esc(REJECTION_LABELS[key])} <b>${n}</b></span>`;
    }).join("");

    $$(".site-group", svg).forEach(node => {
      const g = groups[Number(node.dataset.index)];
      if (!g) return;
      const show = event => {
        const wrap = $("#site-chart-wrap").getBoundingClientRect();
        const rect = node.getBoundingClientRect();
        const clientX = event.clientX || rect.left + rect.width / 2;
        const clientY = event.clientY || rect.top;
        const tip = $("#site-chart-tooltip");
        const names = g.sites.slice(0, 3).map(s => esc(s.name)).join(" · ");
        const more = g.sites.length > 3 ? ` +${g.sites.length - 3} more` : "";
        const totalIt = g.sites.reduce((sum, s) => sum + (s.it_load_mw || 0), 0);
        tip.innerHTML = `<strong>${g.sites.length} campus${g.sites.length === 1 ? "" : "es"} · ${num(totalIt, 0)} MW IT</strong>
          <span>PUE ${num(g.pue, 2)} · water ${num(g.water, 2)} ML/MW-yr</span>
          <span>${esc(REJECTION_LABELS[g.rejection] || g.rejection)} heat rejection · fleet WUE, not metered</span>
          <span>${names}${more}</span>`;
        tip.style.left = `${clientX - wrap.left}px`;
        tip.style.top = `${clientY - wrap.top - 8}px`;
        tip.classList.add("visible");
      };
      const hide = () => $("#site-chart-tooltip").classList.remove("visible");
      node.addEventListener("mouseenter", show);
      node.addEventListener("mousemove", show);
      node.addEventListener("focus", show);
      node.addEventListener("mouseleave", hide);
      node.addEventListener("blur", hide);
      const open = () => {
        const biggest = g.sites.slice().sort((a, b) => (b.it_load_mw || 0) - (a.it_load_mw || 0))[0];
        const site = biggest && DATA.find(d => d.name === biggest.name);
        if (!site) return;
        selectSite(site, true);
        $("#infrastructure").scrollIntoView({ behavior: "smooth", block: "start" });
      };
      node.addEventListener("click", open);
      node.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") { event.preventDefault(); open(); }
      });
    });
  }

  function renderMatrix() {
    const rows = ["dlc", "air_or_dlc", "air", "hybrid", "immersion", "dlc_capable", "unknown"];
    const cols = ["evaporative", "hybrid", "dry_closed_loop", "unknown"];
    const present = rows.filter(r => COOLING.some(c => c.rack_cooling === r));
    const counts = {};
    COOLING.forEach(c => {
      const key = `${c.rack_cooling}|${c.heat_rejection}`;
      counts[key] = (counts[key] || 0) + 1;
    });
    const max = Math.max(...Object.values(counts), 1);
    // Cells sit on a light panel, so a single dark ink works at every shade.
    const shade = n => n
      ? `rgba(186,232,116,${0.14 + 0.72 * n / max})`
      : "rgba(18,37,30,.05)";
    const weight = n => n / max > 0.5 ? 600 : 400;
    const table = `
      <table class="matrix-table">
        <thead><tr><th></th>${cols.map(col => `<th>${esc(REJECTION_LABELS[col])}</th>`).join("")}</tr></thead>
        <tbody>
          ${present.map(row => `<tr>
            <th>${esc(RACK_LABELS[row] || row)}</th>
            ${cols.map(col => {
              const n = counts[`${row}|${col}`] || 0;
              return `<td style="background:${shade(n)};font-weight:${weight(n)}">${n || "·"}</td>`;
            }).join("")}
          </tr>`).join("")}
        </tbody>
      </table>`;
    $("#cooling-matrix").innerHTML = `
      <p class="mini-label">RACK COOLING × HEAT REJECTION</p>
      <h3>Two decisions, not one</h3>
      <p class="matrix-intro">A liquid-cooled rack can still evaporate water at the plant. These counts cover the ${COOLING.length} sites across the two independent layers.</p>
      <div class="matrix-panel"><div class="matrix-scroll">${table}</div></div>
      <p class="matrix-foot">The right-hand column sets water use, not the left.</p>`;
  }

  let ledgerSort = { key: "it_load_mw", dir: -1 };
  let ledgerVisible = 25;
  let ledgerQuery = "";
  let ledgerFilter = "all";

  function ledgerRows() {
    const q = ledgerQuery.toLowerCase();
    return COOLING.filter(c => {
      if (q && !`${c.name} ${c.operator} ${c.country}`.toLowerCase().includes(q)) return false;
      const pue = hasPue(c), water = hasWater(c);
      if (ledgerFilter === "both") return pue && water;
      if (ledgerFilter === "pue") return pue && !water;
      if (ledgerFilter === "water") return water && !pue;
      if (ledgerFilter === "none") return !pue && !water;
      return true;
    }).sort((a, b) => {
      const av = a[ledgerSort.key], bv = b[ledgerSort.key];
      const aNull = av == null || av === "" || av === "unknown";
      const bNull = bv == null || bv === "" || bv === "unknown";
      if (aNull && bNull) return a.name.localeCompare(b.name);
      if (aNull) return 1;
      if (bNull) return -1;
      if (typeof av === "number" && typeof bv === "number") return (av - bv) * ledgerSort.dir;
      return String(av).localeCompare(String(bv)) * ledgerSort.dir;
    });
  }

  function renderLedger() {
    const rows = ledgerRows();
    const shown = rows.slice(0, ledgerVisible);
    $("#ledger-body").innerHTML = shown.length ? shown.map(c => {
      const conf = c.confidence || "D";
      const pue = hasPue(c);
      return `<tr data-site="${esc(c.name)}">
        <td><strong>${esc(c.name)}</strong><small>${esc(c.country || "")}</small></td>
        <td>${esc(c.operator || "")}</td>
        <td>${c.it_load_mw != null ? num(c.it_load_mw, 0) : "—"}</td>
        <td>${c.h100e_per_mw != null ? num(c.h100e_per_mw, 0) : "—"}</td>
        <td class="${pue ? "" : "ledger-assumed"}">${c.pue_used != null ? num(c.pue_used, 2) + (pue ? "" : "*") : "—"}</td>
        <td>${hasWater(c) ? (assumedWue(c) ? `<span class="ledger-assumed" title="WUE is a stated estimate, not a disclosure">≈${num(c.water_ml_per_mw_year, 2)}</span>` : num(c.water_ml_per_mw_year, 2)) : "—"}</td>
        <td><span class="ledger-chip" data-rack="${esc(c.rack_cooling)}">${esc(RACK_LABELS[c.rack_cooling] || c.rack_cooling)}</span></td>
        <td>${esc(REJECTION_LABELS[c.heat_rejection] || c.heat_rejection)}</td>
        <td><span class="conf-badge conf-${conf}">${conf}</span></td>
      </tr>`;
    }).join("") : '<tr><td colspan="9" class="empty-row">No sites match those filters.</td></tr>';
    $("#ledger-count").textContent = `${shown.length} of ${rows.length} sites shown. The dataset holds ${COOLING.length}.`;
    const more = $("#ledger-more");
    more.hidden = rows.length <= 25;
    more.innerHTML = ledgerVisible >= rows.length
      ? `Show the first 25 sites <span aria-hidden="true">↑</span>`
      : `Show more sites <span aria-hidden="true">↓</span> <span style="color:#60776a">${Math.min(ledgerVisible, rows.length)} / ${rows.length}</span>`;
  }

  $("#site-water-filter").addEventListener("click", event => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    siteWaterFilter = button.dataset.filter;
    $$("button", $("#site-water-filter")).forEach(item => item.classList.toggle("active", item === button));
    renderSiteChart();
  });
  $("#ledger-search").addEventListener("input", event => {
    ledgerQuery = event.target.value.trim();
    ledgerVisible = 25;
    renderLedger();
  });
  $("#ledger-filter").addEventListener("change", event => {
    ledgerFilter = event.target.value;
    ledgerVisible = 25;
    renderLedger();
  });
  $$(".ledger-table [data-sort]").forEach(button => {
    button.addEventListener("click", () => {
      const key = button.dataset.sort;
      ledgerSort = ledgerSort.key === key ? { key, dir: -ledgerSort.dir } : { key, dir: 1 };
      renderLedger();
    });
  });
  $("#ledger-body").addEventListener("click", event => {
    const row = event.target.closest("tr[data-site]");
    if (!row) return;
    const site = DATA.find(d => d.name === row.dataset.site);
    if (!site) return;
    selectSite(site, true);
    $("#infrastructure").scrollIntoView({ behavior: "smooth", block: "start" });
  });
  $("#ledger-more").addEventListener("click", () => {
    const rows = ledgerRows();
    ledgerVisible = ledgerVisible >= rows.length ? 25 : ledgerVisible + 25;
    renderLedger();
  });

  renderCoverage();
  renderSiteChart();
  renderMatrix();
  renderLedger();

  /* ---------- Scenario lab ---------- */
  const scenarioOperators = plottableOperators;
  const scenarioA = $("#operator-a");
  const scenarioB = $("#operator-b");
  const options = scenarioOperators.map(d => `<option value="${esc(d.operator)}">${esc(d.operator)}</option>`).join("");
  scenarioA.innerHTML = options;
  scenarioB.innerHTML = options;
  scenarioA.value = "Meta";
  scenarioB.value = "Google";

  function scenarioResult(d, load, maxElectricity) {
    const itGWh = load * 8.76;
    const facilityGWh = itGWh * d.pue_value;
    const overheadGWh = facilityGWh - itGWh;
    const waterMGal = load * d.water_value / 1e6;
    return { d, itGWh, facilityGWh, overheadGWh, waterMGal, maxElectricity };
  }

  function scenarioCard(result, label) {
    const { d, facilityGWh, overheadGWh, waterMGal, maxElectricity } = result;
    return `<article class="scenario-card">
      <div class="scenario-card-head"><h3>${esc(d.operator)}</h3><span>PROFILE ${label} · ${esc(d.metric_year)}</span></div>
      <div class="scenario-big"><strong>${num(facilityGWh, 1)}</strong><span>GWh / year</span></div>
      <p class="scenario-card-label">Total facility electricity at PUE ${num(d.pue_value, 2)}${d.pue_kind === "design" ? " (design midpoint)" : ""}</p>
      <div class="scenario-bar"><i style="width:${facilityGWh / maxElectricity * 100}%"></i></div>
      <div class="scenario-submetrics">
        <div><span>FACILITY OVERHEAD</span><strong>${num(overheadGWh, 1)} <small>GWh</small></strong></div>
        <div><span>WATER NORMALIZER</span><strong>${num(waterMGal, waterMGal < 10 ? 2 : 1)} <small>Mgal</small></strong></div>
      </div>
    </article>`;
  }

  function updateScenario() {
    const load = Number($("#load-slider").value);
    $("#load-output").textContent = `${num(load)} MW`;
    $("#load-slider").style.setProperty("--range-progress", `${(load - 10) / 990 * 100}%`);
    const a = scenarioOperators.find(d => d.operator === scenarioA.value);
    const b = scenarioOperators.find(d => d.operator === scenarioB.value);
    if (!a || !b) return;
    const maxElectricity = Math.max(a.pue_value, b.pue_value) * load * 8.76;
    const resultA = scenarioResult(a, load, maxElectricity);
    const resultB = scenarioResult(b, load, maxElectricity);
    $("#scenario-results").innerHTML = scenarioCard(resultA, "A") + scenarioCard(resultB, "B");
    if (a.operator === b.operator) {
      $("#scenario-delta").innerHTML = `<span>Select a different Profile B to compare the energy and water trade-off at <strong>${num(load)} MW IT load</strong>.</span>`;
      return;
    }
    const waterDifference = Math.abs(resultA.waterMGal - resultB.waterMGal);
    const waterSaver = resultA.waterMGal < resultB.waterMGal ? a : b;
    const energySaver = resultA.facilityGWh < resultB.facilityGWh ? a : b;
    const energyDifference = Math.abs(resultA.facilityGWh - resultB.facilityGWh);
    $("#scenario-delta").innerHTML = `<span>At this load, <strong>${esc(waterSaver.operator)}</strong> uses <strong>${num(waterDifference, waterDifference < 10 ? 2 : 1)} million fewer gallons</strong> per year. <strong>${esc(energySaver.operator)}</strong> uses <strong>${num(energyDifference, 1)} GWh less facility electricity</strong>.</span>`;
  }

  /* ---------- Who pays: state prices ---------- */
  const US_AVG_RISE = 33.2; // EIA, US residential average 13.66 -> 18.19 c/kWh, 2021 -> 2026 YTD
  const mean = values => values.reduce((a, b) => a + b, 0) / (values.length || 1);
  const rankOf = values => {
    const order = values.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
    const out = new Array(values.length);
    for (let i = 0; i < order.length;) {
      let j = i;
      while (j + 1 < order.length && order[j + 1][0] === order[i][0]) j += 1;
      for (let k = i; k <= j; k += 1) out[order[k][1]] = (i + j) / 2;
      i = j + 1;
    }
    return out;
  };
  const spearman = (xs, ys) => {
    const rx = rankOf(xs), ry = rankOf(ys), mx = mean(rx), my = mean(ry);
    let num_ = 0, dx = 0, dy = 0;
    rx.forEach((x, i) => { num_ += (x - mx) * (ry[i] - my); dx += (x - mx) ** 2; dy += (ry[i] - my) ** 2; });
    return num_ / Math.sqrt(dx * dy);
  };
  {
    const core = STATES.filter(d => d.pjm_core), rest = STATES.filter(d => !d.pjm_core);
    $("#who-pjm").textContent = `+${mean(core.map(d => d.rise_pct)).toFixed(0)}%`;
    $("#who-pjm-label").textContent = `Average residential price rise in the ${core.length} tracked states mostly inside PJM (${core.map(d => d.state).join(", ")}).`;
    $("#who-other").textContent = `+${mean(rest.map(d => d.rise_pct)).toFixed(0)}%`;
    $("#who-other-label").textContent = `Average in the other ${rest.length} tracked states. The US average rose ${US_AVG_RISE}%.`;
    $("#who-rho").textContent = spearman(STATES.map(d => d.operating_mw), STATES.map(d => d.rise_pct)).toFixed(2);
    $("#state-chart-heading").textContent = `${STATES.length} states with a tracked site`;
  }

  let stateSort = "rise";
  function renderStateChart() {
    const svg = $("#state-chart");
    const rows = [...STATES].sort((a, b) => stateSort === "mw"
      ? b.operating_mw - a.operating_mw || b.rise_pct - a.rise_pct
      : b.rise_pct - a.rise_pct);
    // Draw at the real pixel width so the labels stay legible on a phone.
    const W = Math.max(320, Math.round(svg.getBoundingClientRect().width) || 760), top = 26, rowH = 18.5, left = 36, right = W < 520 ? 70 : 96;
    const H = top + rows.length * rowH + 30;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const maxPct = Math.ceil(Math.max(...rows.map(d => d.rise_pct)) / 10) * 10;
    const x = v => left + (W - left - right) * v / maxPct;
    const ticks = [];
    for (let t = 0; t <= maxPct; t += 10) ticks.push(t);
    const bars = rows.map((d, i) => {
      const y = top + i * rowH;
      const fill = d.pjm_core ? "var(--orange)" : "#9bb59a";
      return `<g class="state-row" tabindex="0" data-state="${esc(d.state)}">
        <rect x="0" y="${y}" width="${W}" height="${rowH}" fill="transparent"/>
        <text class="chart-label" x="${left - 10}" y="${y + rowH / 2 + 3.5}" text-anchor="end">${esc(d.state)}</text>
        <rect x="${left}" y="${y + 3}" width="${Math.max(x(d.rise_pct) - left, 1)}" height="${rowH - 6}" rx="2" fill="${fill}"/>
        <text class="chart-sub-label" x="${x(d.rise_pct) + 6}" y="${y + rowH / 2 + 3}">+${d.rise_pct.toFixed(1)}%</text>
        <text class="chart-sub-label state-mw" x="${W - 4}" y="${y + rowH / 2 + 3}" text-anchor="end">${d.operating_mw ? `${num(d.operating_mw)} MW` : "0 MW"}</text>
      </g>`;
    }).join("");
    svg.innerHTML = `<title>Residential electricity price rise by state</title>
      ${ticks.map(t => `<line class="chart-grid" x1="${x(t)}" x2="${x(t)}" y1="${top - 6}" y2="${H - 26}"/><text class="chart-axis-label" x="${x(t)}" y="${H - 10}" text-anchor="middle">${t}%</text>`).join("")}
      <line x1="${x(US_AVG_RISE)}" x2="${x(US_AVG_RISE)}" y1="${top - 12}" y2="${H - 26}" stroke="var(--ink)" stroke-width="1.2" stroke-dasharray="4 3"/>
      <text class="chart-sub-label" x="${x(US_AVG_RISE) + 5}" y="${top - 12}">US avg +${US_AVG_RISE}%</text>
      <text class="chart-sub-label" x="${W - 4}" y="${top - 12}" text-anchor="end">AI MW</text>
      ${bars}`;
  }
  renderStateChart();
  {
    let resizeTimer = null;
    window.addEventListener("resize", () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(renderStateChart, 150); });
  }
  $("#state-sort").addEventListener("click", event => {
    const button = event.target.closest("[data-sort]");
    if (!button) return;
    stateSort = button.dataset.sort;
    $$("#state-sort button").forEach(b => b.classList.toggle("active", b === button));
    renderStateChart();
  });
  {
    const tip = $("#state-tooltip");
    const show = row => {
      const d = STATES.find(s => s.state === row.dataset.state);
      if (!d) return;
      const box = row.getBoundingClientRect(), wrap = $("#state-chart").parentElement.getBoundingClientRect();
      tip.innerHTML = `<strong>${esc(d.state)}${d.pjm_core ? " · mostly PJM" : ""}</strong><span>${d.price_2021.toFixed(2)}¢ → ${d.price_2026_ytd.toFixed(2)}¢ per kWh</span><span>+${d.rise_pct.toFixed(1)}% · ${num(d.operating_mw)} MW tracked AI operating</span>`;
      tip.style.left = `${box.left - wrap.left + box.width / 2}px`;
      tip.style.top = `${box.top - wrap.top}px`;
      tip.classList.add("visible");
    };
    const svg = $("#state-chart");
    svg.addEventListener("mouseover", e => { const r = e.target.closest(".state-row"); if (r) show(r); });
    svg.addEventListener("focusin", e => { const r = e.target.closest(".state-row"); if (r) show(r); });
    svg.addEventListener("mouseleave", () => tip.classList.remove("visible"));
    svg.addEventListener("focusout", () => tip.classList.remove("visible"));
  }

  /* ---------- Who pays: utility finder ---------- */
  let selectedUtility = UTILITIES[0] ? UTILITIES[0].region : null;
  const utilityText = u => [u.region, u.utility, u.utility_type, u.our_sites_covered].join(" ").toLowerCase();
  const gradeOf = u => (u.verification || "").trim().charAt(0).toUpperCase();
  const field = (label, value) => value && value.trim()
    ? `<div class="utility-field"><span>${label}</span><p>${esc(value)}</p></div>` : "";
  function renderUtilityDetail(u) {
    if (!u) { $("#utility-detail").innerHTML = '<p class="utility-empty">No territory matches that search.</p>'; return; }
    const sources = (u.sources || "").split(";").map(x => x.trim()).filter(Boolean);
    $("#utility-detail").innerHTML = `
      <div class="utility-head"><div><p class="mini-label">${esc(u.utility_type)}</p><h3>${esc(u.region)}</h3><p class="utility-name">${esc(u.utility)}</p></div><span class="grade-badge" title="${esc(u.verification)}">${esc(gradeOf(u) || "?")}</span></div>
      ${field("TRACKED SITES", u.our_sites_covered)}
      ${field("RESIDENTIAL PRICE, 2021 → 2026", u.energy_price_trend_2021_2026)}
      ${field("RATE CASES AND TARIFFS", u.energy_rate_events)}
      ${field("NAMED GROUPS ON BILLS", u.bill_complaint_groups)}
      ${field("WATER USE", u.water_consumption)}
      ${field("WATER DISPUTES", u.water_complaints)}
      ${field("VERIFICATION", u.verification)}
      ${sources.length ? `<div class="utility-field"><span>SOURCES (${sources.length})</span><ul class="utility-sources">${sources.map(src => /^https?:\/\//i.test(src)
        ? `<li><a href="${safeUrl(src)}" target="_blank" rel="noopener noreferrer">${esc(src.replace(/^https?:\/\/(www\.)?/i, "").slice(0, 70))} ↗</a></li>`
        : `<li>${esc(src)}</li>`).join("")}</ul></div>` : ""}`;
  }
  function renderUtilities() {
    const q = ($("#utility-search").value || "").trim().toLowerCase();
    const rows = UTILITIES.filter(u => !q || utilityText(u).includes(q));
    if (!rows.some(u => u.region === selectedUtility)) selectedUtility = rows[0] ? rows[0].region : null;
    $("#utility-count").textContent = q ? `${rows.length} of ${UTILITIES.length} territories` : `${UTILITIES.length} territories`;
    $("#utility-list").innerHTML = rows.map(u => `
      <button type="button" role="listitem" class="utility-item${u.region === selectedUtility ? " active" : ""}" data-region="${esc(u.region)}">
        <strong>${esc(u.region)}</strong><small>${esc(u.utility)}</small><b>${esc(gradeOf(u))}</b>
      </button>`).join("") || '<p class="utility-empty">No match. Try a state name or an operator.</p>';
    renderUtilityDetail(UTILITIES.find(u => u.region === selectedUtility));
  }
  renderUtilities();
  $("#utility-search").addEventListener("input", renderUtilities);
  $("#utility-list").addEventListener("click", event => {
    const button = event.target.closest("[data-region]");
    if (!button) return;
    selectedUtility = button.dataset.region;
    renderUtilities();
  });

  ["load-slider", "operator-a", "operator-b"].forEach(id => {
    $(`#${id}`).addEventListener(id === "load-slider" ? "input" : "change", updateScenario);
  });
  updateScenario();
})();
