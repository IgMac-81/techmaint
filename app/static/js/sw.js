/* Service Worker do TechMaint.
   É o arquivo que faz o site virar APP instalável e funcionar offline.
   Estratégia:
     - arquivos estáticos (css/js/ícones): cache primeiro (rápido)
     - páginas HTML: rede primeiro, cache como reserva (dado sempre atual)
   ATENÇÃO: ao mudar qualquer arquivo do CACHE_ESTATICO, mude a VERSAO abaixo,
   senão o celular continua servindo a versão antiga. */

const VERSAO = 'techmaint-v1';
const CACHE_ESTATICO = `${VERSAO}-estatico`;
const CACHE_PAGINAS = `${VERSAO}-paginas`;

const ARQUIVOS_BASE = [
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/manifest.webmanifest',
  '/static/icons/icon-192.png',
  '/offline'
];

self.addEventListener('install', (evento) => {
  evento.waitUntil(
    caches.open(CACHE_ESTATICO)
      .then((cache) => cache.addAll(ARQUIVOS_BASE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(
        nomes.filter((n) => !n.startsWith(VERSAO)).map((n) => caches.delete(n))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (evento) => {
  const requisicao = evento.request;
  if (requisicao.method !== 'GET') return;

  const url = new URL(requisicao.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.startsWith('/static/')) {
    evento.respondWith(
      caches.match(requisicao).then((resposta) => resposta || buscarEGuardar(requisicao, CACHE_ESTATICO))
    );
    return;
  }

  evento.respondWith(
    buscarEGuardar(requisicao, CACHE_PAGINAS).catch(() =>
      caches.match(requisicao).then((r) => r || caches.match('/offline'))
    )
  );
});

function buscarEGuardar(requisicao, nomeCache) {
  return fetch(requisicao).then((resposta) => {
    const copia = resposta.clone();
    caches.open(nomeCache).then((cache) => cache.put(requisicao, copia));
    return resposta;
  });
}
