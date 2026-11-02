// Load HTML sections in document order to preserve the original page layout.
(async function loadSections() {
  for (const slot of document.querySelectorAll('[data-include]')) {
    const path = slot.dataset.include;
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      slot.outerHTML = await response.text();
    } catch (error) {
      console.error(`Could not load ${path}:`, error);
      slot.textContent = `Unable to load ${path}`;
    }
  }
  // Handle direct visits to an anchor after sections have loaded.
  if (location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
})();
