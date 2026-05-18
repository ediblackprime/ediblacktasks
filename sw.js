self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  // Permite que la app cargue los recursos normalmente
  event.respondWith(fetch(event.request));
});
