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
  const totalH100e = DATA.reduce((sum, d) => sum + (d.h100e_best || 0), 0);
  const totalPower = DATA.reduce((sum, d) => sum + (powerOf(d) || 0), 0);
  const countries = [...new Set(DATA.map(d => d.country).filter(Boolean))].sort();
  const statusCounts = Object.keys(STATUS).reduce((acc, key) => {
    acc[key] = DATA.filter(d => (d.status || "unknown") === key).length;
    return acc;
  }, {});

  $("#hero-total").textContent = compact(totalH100e, 1);
  $("#stat-sites").textContent = num(DATA.length);
  $("#stat-countries").textContent = num(countries.length);
  $("#stat-power").textContent = `${compact(totalPower, 1)} GW`.replace("k GW", " GW");
  $("#stat-operational").textContent = `${Math.round(statusCounts.operational / DATA.length * 100)}%`;

  const activeStatusKeys = Object.keys(STATUS).filter(key => statusCounts[key]);
  $("#hero-status-stack").innerHTML = activeStatusKeys.map(key =>
    `<span style="width:${statusCounts[key] / DATA.length * 100}%;background:${STATUS[key].color}" title="${STATUS[key].long}: ${statusCounts[key]}"></span>`
  ).join("");
  $("#hero-status-key").innerHTML = activeStatusKeys.map(key =>
    `<div><i style="background:${STATUS[key].color}"></i><span>${STATUS[key].label}</span><b>${statusCounts[key]}</b></div>`
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
    return $("#size-metric").value === "power" ? powerOf(d) : d.h100e_best;
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
      const marker = L.circleMarker([d.latitude, d.longitude], {
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
    const top = [...sites].sort((a, b) => (b.h100e_best || 0) - (a.h100e_best || 0)).slice(0, 6);
    if (!top.length) {
      return '<div class="panel-kicker"><span>NO MATCHES</span></div><h3 class="panel-title">Nothing fits those filters.</h3><p class="panel-list-intro">Try another country, status, or search term.</p>';
    }
    return `
      <div class="panel-kicker"><span>AT A GLANCE</span><span>TOP ${top.length}</span></div>
      <h3 class="panel-title">${sites.length === DATA.length ? "The compute frontier" : "Your selection"}</h3>
      <p class="panel-list-intro">Largest sites in the current filter, by best H100e estimate. Select a campus to inspect its scale and source.</p>
      <div class="panel-site-list">${top.map((d, index) => `
        <button class="panel-site-item" type="button" data-site="${esc(d.name)}">
          <span class="rank">${String(index + 1).padStart(2, "0")}</span>
          <span><strong>${esc(d.name)}</strong><small>${esc(d.country)}</small></span>
          <b>${d.h100e_best ? compact(d.h100e_best) : "—"}</b>
        </button>`).join("")}</div>`;
  }

  function panelDetail(d) {
    const status = statusOf(d);
    const note = d.status_note || "No additional site note is published for this row.";
    const longNote = note.length > 270;
    return `
      <div class="panel-kicker"><span>SITE PROFILE</span><button type="button" data-close-site aria-label="Close site profile">×</button></div>
      <h3 class="panel-title">${esc(d.name)}</h3>
      <p class="panel-location">${esc(d.operator)}<br>${esc(locationOf(d))}</p>
      <span class="panel-status"><i style="background:${status.color}"></i>${status.long}</span>
      <div class="panel-hero-metric">
        <strong>${d.h100e_best ? num(d.h100e_best) : "—"}</strong><small>H100e</small>
        <p>${d.h100e_best ? `Best estimate · ${METHODS[d.h100e_method] || esc(d.h100e_method)}` : "No defensible H100e estimate is available"}</p>
      </div>
      <div class="panel-metrics">
        <div><span>GROSS POWER</span><b>${powerOf(d) != null ? `${num(powerOf(d))} MW` : "Not published"}</b></div>
        <div><span>IT LOAD</span><b>${d.it_load_mw != null ? `${num(d.it_load_mw)} MW` : "Not published"}</b></div>
        <div><span>ANNOUNCED GPUs</span><b>${d.announced_gpu_count != null ? num(d.announced_gpu_count) : "Not published"}</b></div>
        <div><span>ACCELERATORS</span><b>${esc(d.gpu_types || "Not published")}</b></div>
      </div>
      <div class="panel-note" id="panel-note"><span>RESEARCH NOTE</span><p>${esc(note)}</p>${longNote ? '<button type="button" data-expand-note>Read full note ↓</button>' : ""}</div>
      <a class="source-button" href="${safeUrl(d.source_url)}" target="_blank" rel="noopener noreferrer"><span>Open primary source</span><span>↗</span></a>`;
  }

  function selectSite(d, moveMap = true) {
    selectedSite = d;
    $("#site-panel").innerHTML = panelDetail(d);
    updateMarkers();
    if (map && moveMap && d.latitude != null && d.longitude != null) {
      map.flyTo([d.latitude, d.longitude], Math.max(map.getZoom(), 5), { duration: 0.65 });
      const marker = markerBySite.get(d.name);
      if (marker) marker.openTooltip();
    }
  }

  function renderRanking() {
    const sorted = [...filteredSites].sort((a, b) => (b.h100e_best || 0) - (a.h100e_best || 0));
    const max = Math.max(...sorted.map(d => d.h100e_best || 0), 1);
    const shown = sorted.slice(0, visibleCount);
    $("#site-ranking").innerHTML = shown.length ? shown.map((d, index) => {
      const status = statusOf(d);
      return `<tr>
        <td><button class="site-name-button" type="button" data-site="${esc(d.name)}"><span class="rank-num">${String(index + 1).padStart(2, "0")}</span>${esc(d.name)}<small>${esc(d.country)} · ${esc(d.operator)}</small></button></td>
        <td><span class="table-status"><i style="background:${status.color}"></i>${status.label}</span></td>
        <td>${powerOf(d) != null ? `${num(powerOf(d))} MW` : "—"}</td>
        <td class="estimate-cell">${d.h100e_best ? num(d.h100e_best) : "—"}<div class="estimate-bar" style="width:${(d.h100e_best || 0) / max * 100}%"></div></td>
        <td class="method-cell">${METHODS[d.h100e_method] || "—"}</td>
      </tr>`;
    }).join("") : '<tr><td colspan="5" class="empty-row">No sites match the current filters.</td></tr>';
    const more = $("#show-more-sites");
    more.hidden = sorted.length <= 10;
    more.innerHTML = visibleCount >= sorted.length
      ? `Show first 10 sites <span aria-hidden="true">↑</span>`
      : `Show more sites <span aria-hidden="true">↓</span> <span style="color:#60776a">${Math.min(visibleCount, sorted.length)} / ${sorted.length}</span>`;
  }

  function updateAtlas() {
    filteredSites = getFilteredSites();
    if (selectedSite && !filteredSites.some(d => d.name === selectedSite.name)) selectedSite = null;
    $("#map-count").textContent = `${filteredSites.length} site${filteredSites.length === 1 ? "" : "s"}`;
    $("#filter-summary").textContent = filteredSites.length === DATA.length
      ? `Showing all ${DATA.length} sites · ${countries.length} countries.`
      : `Showing ${filteredSites.length} of ${DATA.length} sites · ${compact(filteredSites.reduce((sum, d) => sum + (d.h100e_best || 0), 0))} H100e in selection.`;
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
    $("#size-metric").value = "h100e_best";
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
      expandButton.textContent = note.classList.contains("expanded") ? "Collapse note ↑" : "Read full note ↓";
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
      <p class="operator-overhead">${overhead != null ? `<strong>${overhead} units</strong> of non-IT facility overhead for every 100 units of IT energy.` : "PUE is not disclosed, so facility overhead cannot be calculated."}<br>Water normalizer: <strong>${d.water_value != null ? compact(d.water_value) : "—"} gal</strong> per MW-year.</p>
      <div class="operator-scope"><span>PUE BOUNDARY</span><p>${esc(d.pue_scope)}</p></div>
      <div class="operator-scope"><span>WUE BASIS</span><p>${esc(d.wue_basis)}</p></div>
      <div class="operator-scope"><span>REPORTING CAVEAT</span><p class="operator-note">${esc(d.notes)}</p></div>
      <a class="operator-source" href="${safeUrl(d.source_url)}" target="_blank" rel="noopener noreferrer"><span>View company disclosure</span><span>↗</span></a>`;
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
    svg.innerHTML = `<title id="chart-title">Operator PUE and WUE comparison</title><desc id="chart-desc">Scatter plot of operators with both power and water usage effectiveness values. Lower values are better. Select a point for scope and reporting caveats.</desc>${content}`;
    $("#chart-coverage").textContent = `${data.length} shown · ${OPERATORS.length - plottableOperators.length} operators lack a complete pair`;

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
    $("#scenario-delta").innerHTML = `<span>At this load, <strong>${esc(waterSaver.operator)}</strong> uses <strong>${num(waterDifference, waterDifference < 10 ? 2 : 1)} million fewer gallons</strong> per year; <strong>${esc(energySaver.operator)}</strong> uses <strong>${num(energyDifference, 1)} GWh less facility electricity</strong>.</span>`;
  }

  ["load-slider", "operator-a", "operator-b"].forEach(id => {
    $(`#${id}`).addEventListener(id === "load-slider" ? "input" : "change", updateScenario);
  });
  updateScenario();
})();
