# PWA — transformar o site em aplicativo de celular

## O que é um PWA, em uma frase

Um site que o celular instala na tela inicial, abre sem a barra do navegador e continua
funcionando (para leitura) mesmo sem internet.

Três peças fazem isso acontecer:

| Peça | Arquivo | O que faz |
|---|---|---|
| Manifest | `app/static/manifest.webmanifest` | Diz ao celular o nome, os ícones e as cores do app |
| Service worker | `app/static/js/sw.js`, servido em `/sw.js` | Guarda arquivos em cache e responde quando não há internet |
| HTTPS | deploy | **Obrigatório.** Service worker só funciona em HTTPS ou em `localhost` |

---

## As três armadilhas

### 1. O service worker precisa ser servido na RAIZ

Um service worker só controla a pasta onde ele está. Se ele for servido em
`/static/js/sw.js`, ele só controla `/static/` — e o app não funciona offline.

Por isso existe esta rota em `app/__init__.py`:

```python
@app.route("/sw.js")
def service_worker():
    resposta = make_response(send_from_directory(app.static_folder, "js/sw.js"))
    resposta.headers["Service-Worker-Allowed"] = "/"
    resposta.headers["Cache-Control"] = "no-cache"
    return resposta
```

E o registro no `app.js` aponta para a raiz:

```javascript
navigator.serviceWorker.register('/sw.js', { scope: '/' });
```

### 2. Cache sem versão = usuário preso na versão antiga

O sintoma é clássico: você publica uma correção, abre no celular e continua vendo o bug.
O cache velho está sendo servido.

A solução é versionar o nome do cache e apagar os antigos:

```javascript
const VERSAO = 'techmaint-v1';   // ← ao mudar qualquer arquivo do cache, mude para v2

self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys().then((nomes) =>
      Promise.all(nomes.filter((n) => !n.startsWith(VERSAO)).map((n) => caches.delete(n)))
    )
  );
});
```

> **Regra do time:** mexeu no `app.css`, no `app.js` ou na lista de arquivos do cache?
> Suba a versão no `sw.js` no mesmo commit.

### 3. Cache-first em páginas mostra dados velhos

Estoque e ordens de serviço mudam o tempo todo. Se a página vier do cache, o técnico vê saldo
errado. Por isso a estratégia é dividida:

| O quê | Estratégia | Por quê |
|---|---|---|
| CSS, JS, ícones | **cache-first** | Não mudam entre publicações; carregam instantaneamente |
| Páginas HTML | **network-first**, cache como reserva | Dado sempre atual; offline mostra a última versão vista |
| POST (formulários) | não intercepta | Nunca guarde escrita em cache |

---

## Checklist do manifest

- [x] `name` e `short_name` (o curto é o que aparece embaixo do ícone — máximo ~12 caracteres)
- [x] `start_url: "/"` e `scope: "/"`
- [x] `display: "standalone"` (sem barra de navegador)
- [x] `theme_color` igual à cor do topo (o Android pinta a barra de status com ela)
- [x] `background_color` para a tela de abertura
- [x] Ícones 192px e 512px
- [x] Um ícone **maskable** com 20% de margem — o Android corta as bordas em círculo e, sem
      margem, come o logo
- [x] `lang: "pt-BR"`

---

## Como instalar

**Android (Chrome):** abra o site → menu ⋮ → *Instalar aplicativo*. Se o manifest estiver
correto, o próprio Chrome oferece um banner.

**iPhone (Safari):** abra o site → botão Compartilhar → *Adicionar à Tela de Início*.

> O iOS **não** mostra banner automático e **não** dispara o evento `beforeinstallprompt`.
> No iPhone é sempre manual — por isso o manual do usuário precisa ter os prints desse caminho.

---

## Como testar

1. **Lighthouse:** F12 → aba Lighthouse → marque *Progressive Web App* → Analisar.
   Corrija tudo o que aparecer em vermelho.
2. **Offline:** F12 → aba Network → marque *Offline* → recarregue. Uma página já visitada
   precisa abrir; uma nunca visitada precisa cair na página `/offline`.
3. **Atualização:** publique uma mudança visível, suba a versão do cache, recarregue duas
   vezes no celular. A mudança tem que aparecer **sem desinstalar o app**.
4. **Celular real:** instale em um iPhone e em um Android de verdade. Emulador não vale.

---

## Tokens de design (do Figma)

Preencha com os valores do protótipo. Estes são os valores atuais do `app.css`:

| Token | Valor | Onde é usado |
|---|---|---|
| `--cor-primaria` | `#0F766E` | Topo, botões, números do painel |
| `--cor-primaria-escura` | `#115E59` | Botão pressionado |
| `--cor-fundo` | `#F8FAFC` | Fundo das páginas |
| `--cor-superficie` | `#FFFFFF` | Cartões, tabelas, menu |
| `--cor-texto` | `#0F172A` | Texto principal |
| `--cor-texto-suave` | `#64748B` | Rótulos e legendas |
| `--cor-borda` | `#E2E8F0` | Bordas e separadores |
| `--cor-sucesso` | `#16A34A` | Mensagem de sucesso |
| `--cor-erro` | `#DC2626` | Erro, estoque em alerta |
| `--espaco` | `16px` | Respiro padrão |
| `--raio` | `12px` | Canto dos cartões e botões |

**Regra:** nenhuma cor escrita em hexadecimal fora do bloco `:root`. Sempre `var(--cor-x)`.

---

## Regras de responsividade

Escrevemos **mobile-first**: o CSS base é o do celular, e `@media (min-width: 768px)` ajusta
para telas maiores.

| Regra | Por quê |
|---|---|
| `font-size: 16px` nos `<input>` | Abaixo disso, o Safari do iPhone dá zoom sozinho ao tocar |
| Área de toque mínima de 44×44px | Dedo não é ponteiro de mouse |
| Nenhuma rolagem horizontal | Tabela larga vai dentro de `.tabela-rolagem` |
| `env(safe-area-inset-bottom)` no rodapé | Para não ficar embaixo da barrinha do iPhone |
| Contraste mínimo 4.5:1 | Legibilidade sob luz de chão de fábrica |
| Nunca só a cor para indicar estado | Quem é daltônico precisa do texto ou do ícone também |

Tamanhos de teste obrigatórios: **390px** (iPhone), **768px** (tablet), **1280px** (notebook).
