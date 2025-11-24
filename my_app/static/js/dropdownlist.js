
/* ====== Config ======
   Countries API (public)
   - GET countries+states: https://countriesnow.space/api/v0.1/countries/states
   - POST states->cities: https://countriesnow.space/api/v0.1/countries/state/cities
   NOTE: these endpoints are public; no API key required.
   ====== */

const endpoints = {
  countriesStates: "https://countriesnow.space/api/v0.1/countries/states",
  citiesByState: "https://countriesnow.space/api/v0.1/countries/state/cities"
};

// DOM
const countryEl = document.getElementById('country');
const stateEl   = document.getElementById('state');
const cityEl    = document.getElementById('city');

// Simple cache (in-memory + localStorage)
const CACHE_KEY = "loc_cache_v1";
let cache = JSON.parse(localStorage.getItem(CACHE_KEY) || "{}");

/* Utility: save cache to localStorage */
function saveCache() {
  try { localStorage.setItem(CACHE_KEY, JSON.stringify(cache)); } catch(e) { /* ignore */ }
}

/* Load countries + states list (single request) */
async function loadCountriesAndStates() {
  // If in cache, use it
  if (cache.countriesStates) {
    populateCountries(cache.countriesStates);
    return;
  }

  // show loading placeholder
  countryEl.innerHTML = '<option value="">Loading countries…</option>';

  try {
    const resp = await fetch(endpoints.countriesStates);
    if (!resp.ok) throw new Error("Countries fetch failed");

    const json = await resp.json();
    // API returns {error: false, msg: "OK", data: [...]} typically
    const data = json.data || json || [];
    // store minimal mapping: country -> [states]
    const map = {};
    data.forEach(item => {
      const cname = item.country || item.name || item;
      const states = item.states || item.states || [];
      // normalize states to array of strings
      map[cname] = states.map(s => (typeof s === 'string') ? s : (s.name || s.state || ""));
    });

    cache.countriesStates = map;
    saveCache();
    populateCountries(map);

  } catch (err) {
    console.error("Error loading countries/states:", err);
    countryEl.innerHTML = '<option value="">Could not load countries</option>';
    // Keep selects disabled so user knows.
  }
}

/* Populate country select */
function populateCountries(map) {
  countryEl.innerHTML = '<option value="">Select country</option>';
  Object.keys(map).sort().forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    countryEl.appendChild(opt);
  });
  countryEl.disabled = false;
}

/* When country changes -> populate states from cache (we loaded countriesStates earlier) */
countryEl.addEventListener('change', function() {
  const country = this.value;
  cityEl.innerHTML = '<option value="">Select state first</option>';
  cityEl.disabled = true;

  if (!country) {
    stateEl.innerHTML = '<option value="">Select country first</option>';
    stateEl.disabled = true;
    return;
  }

  const map = cache.countriesStates || {};
  const states = map[country] || [];

  // Populate states
  stateEl.innerHTML = '<option value="">Select state</option>';
  states.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s;
    opt.textContent = s;
    stateEl.appendChild(opt);
  });
  stateEl.disabled = false;
});

/* When state changes -> fetch cities via POST to API (or from cache) */
stateEl.addEventListener('change', async function() {
  const country = countryEl.value;
  const state = this.value;

  cityEl.innerHTML = '<option value="">Loading cities…</option>';
  cityEl.disabled = true;

  if (!country || !state) {
    cityEl.innerHTML = '<option value="">Select state first</option>';
    cityEl.disabled = true;
    return;
  }

  // Check cache: cache.cities?.[country]?.[state]
  if (cache.cities && cache.cities[country] && cache.cities[country][state]) {
    populateCities(cache.cities[country][state]);
    return;
  }

  try {
    const resp = await fetch(endpoints.citiesByState, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ country: country, state: state })
    });
    if (!resp.ok) throw new Error('Cities fetch failed');

    const json = await resp.json();
    const cities = json.data || json || [];

    // normalize to array of strings if necessary
    const cityNames = Array.isArray(cities) ? cities : (cities.map ? cities.map(c => c) : []);

    // store in cache
    cache.cities = cache.cities || {};
    cache.cities[country] = cache.cities[country] || {};
    cache.cities[country][state] = cityNames;
    saveCache();

    populateCities(cityNames);
  } catch (err) {
    console.error('Error loading cities:', err);
    cityEl.innerHTML = '<option value="">Could not load cities</option>';
    cityEl.disabled = true;
  }
});

function populateCities(list) {
  cityEl.innerHTML = '<option value="">Select city</option>';
  list.forEach(ct => {
    const opt = document.createElement('option');
    opt.value = ct;
    opt.textContent = ct;
    cityEl.appendChild(opt);
  });
  cityEl.disabled = false;
}

/* Avatar preview */
const avatarInput = document.getElementById('avatar');
const avatarPreview = document.getElementById('avatarPreview');
if (avatarInput && avatarPreview) {
  avatarInput.addEventListener('change', function(e) {
    const f = avatarInput.files && avatarInput.files[0];
    if (!f) { avatarPreview.style.display = 'none'; return; }
    avatarPreview.src = URL.createObjectURL(f);
    avatarPreview.style.display = 'block';
  });
}

/* Kick off loading on page load */
document.addEventListener('DOMContentLoaded', loadCountriesAndStates);