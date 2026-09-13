# Guia do calouro — do zero ao sistema rodando

Se você nunca programou em equipe, este é o único arquivo que você precisa ler hoje.
Leva cerca de 1h30. Faça com calma, na ordem.

---

## Parte 1 — Instalar as três ferramentas

### Python 3.11 ou superior
Baixe em [python.org/downloads](https://www.python.org/downloads/).

> **No Windows, marque a caixinha "Add Python to PATH" na primeira tela do instalador.**
> Se esquecer, o terminal vai dizer que não conhece o comando `python` e você vai ter que
> desinstalar e instalar de novo. Todo mundo esquece na primeira vez.

Confira no terminal: `python --version` → deve mostrar `Python 3.11.x` ou maior.

### VS Code
Baixe em [code.visualstudio.com](https://code.visualstudio.com/) e instale a extensão
**Python** (da Microsoft) dentro dele.

### Git
Baixe em [git-scm.com](https://git-scm.com/). Depois, no terminal:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## Parte 2 — Baixar e rodar o projeto

```bash
git clone https://github.com/TechMind-tech/techmaint.git
cd techmaint
```

### O ambiente virtual (venv)

```bash
python -m venv .venv
```

Ative:
- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

Deu certo se aparecer `(.venv)` no começo da linha do terminal.

> **O que é isso?** É uma caixinha isolada onde as bibliotecas deste projeto ficam guardadas,
> sem se misturar com as de outros projetos. Toda vez que abrir um terminal novo para mexer
> no TechMaint, ative o venv de novo. **Esquecer de ativar é a causa de 80% dos erros
> "No module named flask".**

### Instalar as bibliotecas e rodar

```bash
pip install -r requirements.txt
flask --app run.py seed      # cria o banco com dados de exemplo
python run.py
```

Abra http://127.0.0.1:5000 e entre com **admin / admin123**.

Para parar o servidor: `Ctrl + C` no terminal.

---

## Parte 3 — Testar no seu celular

1. Descubra o IP do seu computador: `ipconfig` (Windows) ou `ifconfig` (Mac/Linux) — procure
   algo como `192.168.0.15`.
2. Com o celular no **mesmo Wi-Fi**, abra `http://192.168.0.15:5000`.
3. Se não abrir, o firewall do Windows está bloqueando: permita o Python na rede privada.

> O botão "instalar aplicativo" só aparece em **HTTPS**. Por isso o PWA só vai instalar de
> verdade depois do deploy (issue do Sprint 4). No celular pelo IP você consegue testar o
> **visual responsivo**, que já é o suficiente por enquanto.

---

## Parte 4 — Entendendo a estrutura do projeto

```
techmaint/
├── run.py                    ← você roda este arquivo
├── requirements.txt          ← lista de bibliotecas
├── app/
│   ├── __init__.py           ← a "fábrica" que monta a aplicação
│   ├── config.py             ← configurações (senha do banco, chave secreta)
│   ├── extensions.py         ← db, login, csrf
│   ├── models/               ← as TABELAS do banco, em Python
│   ├── blueprints/           ← um "mini-app" por módulo: as ROTAS
│   ├── templates/            ← as PÁGINAS (HTML)
│   └── static/               ← CSS, JavaScript, ícones, manifest do PWA
├── seeds/                    ← dados de exemplo
├── tests/                    ← testes automatizados
└── docs/                     ← esta documentação
```

### O caminho de uma tela, do clique ao banco

```
Você digita /equipamentos no navegador
        ↓
app/blueprints/equipamentos/routes.py   ← a FUNÇÃO que responde essa URL
        ↓
app/models/catalogo.py                  ← consulta a tabela no banco
        ↓
app/templates/equipamentos/listar.html  ← monta o HTML com os dados
        ↓
volta pronto para o navegador
```

Toda tela do sistema é sempre esse mesmo caminho. Quando você entender uma, entendeu todas.

---

## Parte 5 — Palavras que você vai ver o tempo todo

| Palavra | O que é, em português claro |
|---|---|
| **rota** | Uma URL do site ligada a uma função Python |
| **blueprint** | Um conjunto de rotas de um mesmo assunto (um "mini-app") |
| **template** | Arquivo HTML com espaços para dados (`{{ nome }}`) |
| **model** | Uma classe Python que representa uma tabela do banco |
| **ORM** | A ferramenta que traduz Python ↔ SQL, para você não escrever SQL na mão |
| **migração** | Um arquivo que registra uma mudança na estrutura do banco |
| **commit** | Um "salvamento" do código, com uma mensagem explicando o que mudou |
| **branch** | Uma linha de trabalho paralela, para você não atrapalhar os outros |
| **Pull Request (PR)** | O pedido para juntar o seu branch na `main`, passando por revisão |
| **CRUD** | Create, Read, Update, Delete — criar, listar, editar e excluir |
| **CSRF** | Proteção que impede outro site de enviar formulário no seu nome |
| **hash de senha** | A senha embaralhada de forma irreversível; guardamos isso, nunca a senha |
| **PWA** | Site que o celular instala como se fosse aplicativo |
| **service worker** | O JavaScript que roda em segundo plano e faz o PWA funcionar offline |
| **seed** | Script que enche o banco com dados de exemplo |
| **fixture** | Função que prepara o cenário antes de um teste |

---

## Parte 6 — Erros que todo mundo comete

| Mensagem | O que aconteceu | Solução |
|---|---|---|
| `'python' não é reconhecido` | Python fora do PATH | Reinstale marcando "Add Python to PATH" |
| `No module named flask` | Venv não ativado | Ative o `.venv` e rode `pip install -r requirements.txt` |
| `Address already in use` | Já tem um servidor rodando | Feche o outro terminal |
| `no such table: usuarios` | Banco vazio | Rode `flask --app run.py seed` |
| `TemplateNotFound` | Caminho do template errado | Confira a pasta em `app/templates/` |
| Salvou mas não apareceu nada | Faltou `db.session.commit()` | Sem commit, o banco não grava |
| `BuildError: Could not build url` | Nome de rota errado no `url_for` | É `blueprint.funcao`, ex.: `equipamentos.listar` |
| Página sem estilo | Caminho do CSS errado | Use `{{ url_for('static', filename='css/app.css') }}` |

---

## Parte 7 — Pegando sua primeira tarefa

1. Abra o [quadro do projeto](https://github.com/orgs/TechMind-tech/projects/1).
2. Filtre pela label **`nível: iniciante`**.
3. Escolha uma que ninguém pegou, comente *"vou pegar esta"* e mova para **Em andamento**.
4. Leia a issue **inteira** antes de escrever código — ela tem passo a passo, exemplo e os
   critérios que o revisor vai conferir.
5. Siga o [CONTRIBUTING.md](../CONTRIBUTING.md) para criar o branch e abrir o PR.

**Sugestão:** comece por uma issue com a label `desafio ⭐`. São as mais divertidas.

Travou 40 minutos? Peça ajuda. Esse é o combinado.
