const C = "fitness-v2";
const U = ["/","/static/css/style.css","/static/js/app.js","/static/manifest.json"];
self.addEventListener("install", e => { e.waitUntil(caches.open(C).then(c => c.addAll(U))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== C).map(x => caches.delete(x))))); self.clients.claim(); });
self.addEventListener("fetch", e => { if (e.request.method === "GET") e.respondWith(caches.match(e.request).then(c => c || fetch(e.request))); });
