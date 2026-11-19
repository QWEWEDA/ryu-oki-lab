/* RYU / OKI LAB — offline cache. Update CACHE_VERSION when files change. */
const CACHE_VERSION = 'ryu-oki-lab-2026-11-pwa-v1';
const APP_FILES = [
  './', './index.html', './style.css', './app.js',
  './data/routes.js', './data/routes.json', './data/patch-status.json',
  './manifest.webmanifest', './icons/ryu-192.png', './icons/ryu-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_VERSION);
    // If the core files cannot be downloaded, don't activate a broken offline app.
    await cache.addAll(['./', './index.html', './style.css', './app.js', './data/routes.js']);
    // A missing optional asset shouldn't prevent offline support from installing.
    await Promise.all(APP_FILES.slice(5).map(url => cache.add(url).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith('ryu-oki-lab-') && key !== CACHE_VERSION) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  const scope = new URL(self.registration.scope);
  if (url.origin !== scope.origin || !url.pathname.startsWith(scope.pathname)) return;

  // Treat cache-busting query strings (e.g. patch-status.json?now=...) as one file.
  const canonical = url.origin + url.pathname;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_VERSION);
    try {
      const response = await fetch(request);
      if (response.ok && response.type === 'basic') {
        await cache.put(canonical, response.clone());
      }
      return response;
    } catch (_) {
      const saved = await cache.match(canonical);
      if (saved) return saved;
      if (request.mode === 'navigate') {
        const home = await cache.match(new URL('./index.html', scope).href);
        if (home) return home;
      }
      return Response.error();
    }
  })());
});
