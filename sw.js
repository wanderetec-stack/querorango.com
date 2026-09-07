const CACHE_NAME = 'querorango-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/receitas/',
  '/css/style.css',
  '/js/main.js',
  '/js/recipe.js',
  '/manifest.json',
  '/offline.html'
];

// Install: cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// Fetch: stale-while-revalidate for HTML; cache-first for assets
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET and cross-origin
  if (request.method !== 'GET' || url.origin !== location.origin) return;

  // Images: cache-first
  if (request.destination === 'image') {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(request).then(cached => {
          if (cached) return cached;
          return fetch(request).then(response => {
            cache.put(request, response.clone());
            return response;
          });
        })
      )
    );
    return;
  }

  // HTML pages: stale-while-revalidate
  if (request.destination === 'document') {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(request).then(cached => {
          const fetchPromise = fetch(request)
            .then(response => {
              cache.put(request, response.clone());
              return response;
            })
            .catch(() => caches.match('/offline.html'));
          return cached || fetchPromise;
        })
      )
    );
    return;
  }

  // CSS/JS: cache-first
  event.respondWith(
    caches.open(CACHE_NAME).then(cache =>
      cache.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          cache.put(request, response.clone());
          return response;
        });
      })
    )
  );
});

// Push notifications
self.addEventListener('push', event => {
  const data = event.data?.json() ?? {};
  event.waitUntil(
    self.registration.showNotification(data.title || 'Quero Rango 🍊', {
      body: data.body || 'Nova receita deliciosa te esperando!',
      icon: '/assets/icons/icon-192.png',
      badge: '/assets/icons/icon-72.png',
      tag: 'querorango-notification',
      data: { url: data.url || '/' }
    })
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
