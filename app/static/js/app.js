/* JavaScript da aplicação — sem frameworks, sem npm. */

// 1) Registra o Service Worker (é o que permite instalar o app no celular).
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then(() => console.log('[TechMaint] service worker registrado'))
      .catch((e) => console.error('[TechMaint] falha ao registrar', e));
  });
}

// 2) Botão "instalar app" no Android/Chrome.
let eventoInstalacao = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  eventoInstalacao = e;
  const botao = document.getElementById('instalar-app');
  if (botao) {
    botao.hidden = false;
    botao.addEventListener('click', async () => {
      botao.hidden = true;
      eventoInstalacao.prompt();
      await eventoInstalacao.userChoice;
      eventoInstalacao = null;
    });
  }
});

// 3) Abre/fecha o menu lateral no tablet.
const botaoMenu = document.getElementById('abrir-menu');
if (botaoMenu) {
  botaoMenu.addEventListener('click', () => {
    document.getElementById('menu-lateral')?.classList.toggle('aberto');
  });
}
