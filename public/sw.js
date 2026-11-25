const scope = new URL(self.registration.scope);
const shell = scope.href;
const models = new URL('models/', scope).pathname;
const modelManifest = new URL('models/model.json', scope).pathname;
const cacheName = 'cilla-shell-v2:' + scope.pathname;

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(cacheName).then((cache) =>
    cache.addAll(['', 'icon.svg', 'manifest.webmanifest'].map((path) => new URL(path, scope).href))
  ));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== scope.origin ||
      !url.pathname.startsWith(scope.pathname) || (url.pathname.startsWith(models) && url.pathname !== modelManifest)) return;

  event.respondWith((async () => {
    const cache = await caches.open(cacheName);
    try {
      const response = await fetch(request);
      if (response.ok) await cache.put(request, response.clone());
      return response;
    } catch {
      return await cache.match(request) ??
        (request.mode === 'navigate' ? await cache.match(shell) : undefined) ??
        Response.error();
    }
  })());
});
