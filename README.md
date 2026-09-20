# TechMaint — CRUD base em Flask

Projeto base, propositalmente pequeno, para aprender e para copiar em outros
módulos. Uma entidade (**Equipamentos**) com as quatro operações do CRUD:
criar, listar, editar e apagar.

Sem framework de CSS, sem ORM, sem blueprint. Só Flask, SQLite, Jinja e CSS.
Tudo comentado em português.

---

## 1. Como rodar

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual (Windows, PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Instale o Flask:

```bash
pip install -r requirements.txt
```

Rode:

```bash
python app.py
```

Abra <http://127.0.0.1:5000> no navegador. O arquivo `techmaint.db` é criado
sozinho na primeira execução.

> **Ambiente virtual (`venv`)** é uma pasta com um Python só para este projeto.
> Serve para as bibliotecas de um projeto não conflitarem com as de outro.
> Você sabe que está ativo quando aparece `(.venv)` no começo da linha do
> terminal.

---

## 2. Os arquivos

```
techmaint/
├── app.py                 rotas: liga cada endereço a uma função
├── database.py            todo o SQL: as quatro operações do CRUD
├── requirements.txt       bibliotecas necessárias
├── templates/
│   ├── base.html          molde: cabeçalho, rodapé, avisos
│   ├── listar.html        tabela + busca (o R do CRUD)
│   └── form.html          formulário que serve para criar E editar
└── static/
    └── css/style.css      todo o visual
```

A regra de ouro: **`app.py` não escreve SQL** e **`database.py` não conhece
HTML**. Cada arquivo com um trabalho só.

---

## 3. Como os dados percorrem o sistema

```
navegador  →  rota (app.py)  →  função (database.py)  →  banco (SQLite)
                   ↓
             template (templates/)  →  HTML pronto  →  navegador
```

As rotas e o que cada uma faz:

| Endereço | Método | Função | Operação |
|---|---|---|---|
| `/` | GET | `listar` | READ (lista) |
| `/novo` | GET | `novo` | mostra o formulário vazio |
| `/novo` | POST | `novo` | CREATE |
| `/editar/<id>` | GET | `editar` | mostra o formulário preenchido |
| `/editar/<id>` | POST | `editar` | UPDATE |
| `/apagar/<id>` | POST | `apagar` | DELETE |

**GET** = quero ver uma página. **POST** = estou enviando dados.
Apagar só aceita POST, porque link pode ser aberto sem querer.

---

## 4. Quatro ideias que se repetem em qualquer CRUD

**Um formulário serve para criar e editar.** Em `form.html`, a variável
`equipamento` decide: vazia mostra campos em branco, preenchida mostra os
valores atuais.

**Post/Redirect/Get.** Depois de gravar, a rota faz `redirect`. Sem isso, o
usuário apertaria F5 e cadastraria o mesmo registro duas vezes.

**Query parametrizada.** Todo SQL usa `?` no lugar dos valores. Nunca monte
SQL com f-string: é assim que nasce SQL Injection.

**Valide no Python, não só no HTML.** O `required` do navegador ajuda, mas
pode ser burlado. A verificação que vale é a do servidor.

---

## 5. Criar uma entidade nova (ex.: Fornecedores)

1. Em `database.py`: copie o bloco de funções, troque `equipamentos` por
   `fornecedores` e ajuste as colunas no `CREATE TABLE`.
2. Em `app.py`: copie as quatro rotas e troque os nomes.
3. Em `templates/`: copie `listar.html` e `form.html`, ajuste as colunas
   da tabela e os campos do formulário.
4. Em `base.html`: adicione o link no menu.

Quando passar de três ou quatro entidades, vale estudar **Blueprints**, que
é o jeito do Flask de separar o projeto em módulos.

---

## 6. Trabalhando com Git no VS Code

Este projeto está na branch **`crud-base`**. A `main` continua intacta com a
versão anterior.

### Abrir o projeto

`Arquivo → Abrir Pasta` e escolha `techmaint`. O painel do Git é o terceiro
ícone da barra lateral esquerda (três bolinhas ligadas por linhas), atalho
`Ctrl+Shift+G`.

### Ver em qual branch você está

Canto **inferior esquerdo** da janela. Aparece o nome da branch atual.
Clicando nele, o VS Code lista as branches e você troca de uma para outra.

> Trocar de branch com alterações não salvas no Git pode dar conflito.
> Faça commit antes de trocar.

### O ciclo do dia a dia

1. **Edite** os arquivos normalmente.
2. Abra o painel Git. Os arquivos alterados aparecem em *Changes*.
3. Clique no nome de um arquivo para ver o que mudou: vermelho é o que saiu,
   verde é o que entrou.
4. Passe o mouse no arquivo e clique no **`+`** (*Stage Changes*). Isso
   escolhe o que entra no commit. Para tudo de uma vez, use o `+` do
   cabeçalho *Changes*.
5. Escreva a mensagem na caixa de texto do topo. Frase curta, no presente:
   `adiciona busca por setor`.
6. Clique em **Commit**. O commit ficou salvo no seu computador.
7. Clique em **Sync Changes** (ou `...` → *Push*) para enviar ao GitHub.

Faça um commit por assunto. Vários commits pequenos são muito mais fáceis de
entender depois do que um commit gigante.

### Fazer o merge de `crud-base` na `main`

Quando estiver funcionando e comitado:

1. Canto inferior esquerdo → troque para **`main`**.
2. `...` (menu do painel Git) → **Pull** — traz o que houver de novo do
   GitHub.
3. `...` → **Branch** → **Merge...** → escolha **`crud-base`**.
4. **Sync Changes** para enviar a `main` atualizada.

Em resumo: você fica **na branch que vai receber** e manda trazer a outra.

### Se der conflito

O VS Code marca o arquivo e mostra os botões *Accept Current Change*,
*Accept Incoming Change* e *Accept Both Changes*. Escolha, salve o arquivo,
dê *Stage* e faça o commit do merge.

*Current* é a branch em que você está (`main`). *Incoming* é a que está
chegando (`crud-base`).

### Depois do merge

A branch `crud-base` pode ser apagada: painel Git → `...` → *Branch* →
*Delete Branch*. O histórico dos commits continua na `main`.

### Os mesmos comandos pelo terminal

Se quiser entender o que o VS Code faz por baixo:

```bash
git status
git add .
git commit -m "adiciona busca por setor"
git push
git checkout main
git merge crud-base
git push
```
