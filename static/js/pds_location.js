/**
 * PDS Cascading Location Dropdowns
 * Uses the PSGC (Philippine Standard Geographic Code) public API
 * API Docs: https://psgc.gitlab.io/api/
 *
 * Usage:
 *   Include this script after your HTML fields.
 *   Requires Select2 (optional, for searchable dropdowns).
 *   Call: initPDSLocation({ useSelect2: true })
 */

(function () {
  "use strict";

  const PSGC_BASE = "https://psgc.gitlab.io/api";

  // ── Field IDs (customize to match your Django form field names) ──────────
  const FIELD = {
    province:     "id_province",
    municipality: "id_municipality",
    barangay:     "id_barangay",
    zip:          "id_zip_code",
  };

  // ── Helpers ───────────────────────────────────────────────────────────────

  function getEl(id) {
    return document.getElementById(id);
  }

  function setLoading(selectEl, isLoading) {
    selectEl.disabled = isLoading;
    if (isLoading) {
      selectEl.dataset.placeholder = selectEl.options[0]?.text || "";
      selectEl.options[0].text = "Loading…";
    } else {
      if (selectEl.dataset.placeholder) {
        selectEl.options[0].text = selectEl.dataset.placeholder;
      }
    }
  }

  function clearSelect(selectEl, placeholderText) {
    selectEl.innerHTML = `<option value="">${placeholderText}</option>`;
    selectEl.disabled = true;
    if (window.$ && $(selectEl).data("select2")) {
      $(selectEl).val(null).trigger("change");
    }
  }

  function populateSelect(selectEl, items, valueKey, labelKey, enableAfter) {
    const placeholder = selectEl.options[0]?.text || "";
    selectEl.innerHTML = `<option value="">${placeholder}</option>`;
    items
      .sort((a, b) => a[labelKey].localeCompare(b[labelKey]))
      .forEach((item) => {
        const opt = document.createElement("option");
        opt.value = item[valueKey];
        opt.text = item[labelKey];
        // Store zip on municipality options for instant fill
        if (item.zipCode) opt.dataset.zip = item.zipCode;
        selectEl.appendChild(opt);
      });
    selectEl.disabled = !enableAfter;
    if (window.$ && $(selectEl).data("select2")) {
      $(selectEl).val(null).trigger("change");
    }
  }

  async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`PSGC API error: ${res.status} ${url}`);
    return res.json();
  }

  // ── Core fetch functions ──────────────────────────────────────────────────

  async function loadProvinces() {
    const provEl = getEl(FIELD.province);
    setLoading(provEl, true);
    try {
      const data = await fetchJSON(`${PSGC_BASE}/provinces/`);
      populateSelect(provEl, data, "code", "name", true);
    } catch (err) {
      console.error("Failed to load provinces:", err);
      provEl.options[0].text = "Error loading provinces";
    } finally {
      setLoading(provEl, false);
    }
  }

  async function loadMunicipalities(provinceCode) {
    const munEl = getEl(FIELD.municipality);
    clearSelect(munEl, "Select Municipality/City");
    clearSelect(getEl(FIELD.barangay), "Select Barangay");
    getEl(FIELD.zip).value = "";

    setLoading(munEl, true);
    try {
      // PSGC exposes both cities and municipalities per province
      const [municipalities, cities] = await Promise.all([
        fetchJSON(`${PSGC_BASE}/provinces/${provinceCode}/municipalities/`).catch(() => []),
        fetchJSON(`${PSGC_BASE}/provinces/${provinceCode}/cities/`).catch(() => []),
      ]);
      const combined = [...municipalities, ...cities];
      populateSelect(munEl, combined, "code", "name", true);
    } catch (err) {
      console.error("Failed to load municipalities/cities:", err);
      munEl.options[0].text = "Error loading data";
    } finally {
      setLoading(munEl, false);
    }
  }

  async function loadBarangays(munCode) {
    const bgyEl = getEl(FIELD.barangay);
    clearSelect(bgyEl, "Select Barangay");

    setLoading(bgyEl, true);
    try {
      // Try municipality endpoint first, fall back to city
      let data = await fetchJSON(`${PSGC_BASE}/municipalities/${munCode}/barangays/`).catch(() => null);
      if (!data) {
        data = await fetchJSON(`${PSGC_BASE}/cities/${munCode}/barangays/`).catch(() => []);
      }
      populateSelect(bgyEl, data, "code", "name", true);
    } catch (err) {
      console.error("Failed to load barangays:", err);
      bgyEl.options[0].text = "Error loading data";
    } finally {
      setLoading(bgyEl, false);
    }
  }

  async function fillZipCode(munCode) {
    // Try to get zip from the selected option's dataset first (cached)
    const munEl = getEl(FIELD.municipality);
    const selectedOpt = munEl.options[munEl.selectedIndex];
    if (selectedOpt?.dataset.zip) {
      getEl(FIELD.zip).value = selectedOpt.dataset.zip;
      return;
    }
    // Otherwise fetch from PSGC detail endpoint
    try {
      let detail = await fetchJSON(`${PSGC_BASE}/municipalities/${munCode}/`).catch(() => null);
      if (!detail) detail = await fetchJSON(`${PSGC_BASE}/cities/${munCode}/`).catch(() => null);
      if (detail?.zipCode) {
        getEl(FIELD.zip).value = detail.zipCode;
        if (selectedOpt) selectedOpt.dataset.zip = detail.zipCode; // cache it
      }
    } catch (err) {
      console.error("Failed to fetch ZIP code:", err);
    }
  }

  // ── Event wiring ──────────────────────────────────────────────────────────

  function wireEvents(useSelect2) {
    const provEl = getEl(FIELD.province);
    const munEl  = getEl(FIELD.municipality);

    function onProvinceChange() {
      const code = provEl.value;
      clearSelect(munEl, "Select Municipality/City");
      clearSelect(getEl(FIELD.barangay), "Select Barangay");
      getEl(FIELD.zip).value = "";
      if (code) loadMunicipalities(code);
    }

    function onMunicipalityChange() {
      const code = munEl.value;
      clearSelect(getEl(FIELD.barangay), "Select Barangay");
      getEl(FIELD.zip).value = "";
      if (code) {
        loadBarangays(code);
        fillZipCode(code);
      }
    }

    if (useSelect2 && window.$) {
      // Select2 fires a custom "change" event
      $(provEl).on("change", onProvinceChange);
      $(munEl).on("change", onMunicipalityChange);
    } else {
      provEl.addEventListener("change", onProvinceChange);
      munEl.addEventListener("change", onMunicipalityChange);
    }
  }

  // ── Select2 initializer (optional) ───────────────────────────────────────

  function initSelect2() {
    if (!window.$ || !$.fn.select2) return;
    [FIELD.province, FIELD.municipality, FIELD.barangay].forEach((id) => {
      $(`#${id}`).select2({
        placeholder: document.getElementById(id)?.options[0]?.text || "Select…",
        allowClear: true,
        width: "100%",
      });
    });
  }

  // ── Public init ───────────────────────────────────────────────────────────

  /**
   * @param {Object} options
   * @param {boolean} [options.useSelect2=false] - Enable Select2 searchable dropdowns
   */
  window.initPDSLocation = function (options = {}) {
    const { useSelect2 = false } = options;

    // Make ZIP field read-only
    const zipEl = getEl(FIELD.zip);
    if (zipEl) {
      zipEl.readOnly = true;
      zipEl.style.backgroundColor = "var(--color-background-secondary, #f5f5f5)";
      zipEl.title = "Auto-filled based on selected municipality/city";
    }

    // Initial state: disable dependent dropdowns
    clearSelect(getEl(FIELD.municipality), "Select Municipality/City");
    clearSelect(getEl(FIELD.barangay), "Select Barangay");

    if (useSelect2) initSelect2();
    wireEvents(useSelect2);
    loadProvinces();
  };
})();