# Como contribuir com o TechMaint

Escrito para quem nunca trabalhou em equipe com Git. Siga na ordem, sem pular.

---

## O ciclo completo, do começo ao fim

```bash
# 1. Sempre comece atualizando a main
git checkout main
git pull

# 2. Crie um branch para a SUA tarefa (nunca trabalhe direto na main)
git checkout -b feat/cadastro-departamentos

# 3. Trabalhe. Salve pedaços pequenos com mensagens claras:
git add .
git commit -m "feat(departamentos): cria formulário e rota de cadastro"

# 4. Antes de abrir o PR, confira se não quebrou nada:
pytest -q
ruff check .

# 5. Envie o branch
git push -u origin feat/cadastro-departamentos

# 6. Abra o Pull Request no GitHub e peça revisão
```

---

## Nome do branch

`tipo/descricao-curta-com-hifens`

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat/` | Funcionalidade nova | `feat/cadastro-fornecedores` |
| `fix/` | Correção de bug | `fix/estoque-negativo` |
| `docs/` | Só documentação | `docs/manual-usuario` |
| `test/` | Só testes | `test/fluxo-ordem-servico` |
| `chore/` | Configuração, dependências | `chore/atualiza-flask` |

---

## Mensagem de commit

Formato: `tipo(modulo): o que mudou, no presente`

✅ Bom:
- `feat(estoque): bloqueia saída maior que o saldo`
- `fix(login): corrige redirecionamento após entrar`

❌ Ruim:
- `alterações` · `update` · `agora vai` · `commit final v2 FINAL`

**Por quê?** Daqui a um mês, quando algo quebrar, o `git log` é o único lugar onde está escrito
por que aquela linha existe.

---

## Pull Request

Um PR = uma issue = um assunto. PR com 40 arquivos de 5 assuntos diferentes é impossível de
revisar e vai ser devolvido.

No corpo do PR, escreva:

```markdown
Fecha #23

## O que mudou
Cadastro de departamentos: listar, criar, editar e excluir.

## Como testar
1. `flask --app run.py seed` e `python run.py`
2. Acesse /departamentos
3. Cadastre "Produção" e confira se aparece na lista

## Print
(cole aqui o print da tela funcionando)
```

O `Fecha #23` faz o GitHub fechar a issue automaticamente quando o PR for aceito.

---

## Revisando o código de um colega

Revisar é a melhor forma de aprender. Ao revisar:

- Rode o código na sua máquina, não aprove só lendo.
- Comente com pergunta, não com acusação: *"o que acontece se o estoque for zero aqui?"* em vez
  de *"isso está errado"*.
- Aprovou? Diga também o que achou bom. Elogio específico ensina tanto quanto correção.

---

## Regras que não se quebram

1. **Nunca faça push direto na `main`.** O GitHub vai recusar de qualquer jeito.
2. **Nunca suba senha, chave ou arquivo `.env`.** Use `.env.example` como modelo.
3. **Nunca suba o arquivo do banco** (`*.db`). Ele já está no `.gitignore`.
4. **Nunca instale biblioteca sem avisar.** Se precisar de uma nova, comente na issue e adicione
   no `requirements.txt` com a versão travada.
5. **Nunca use `float` para dinheiro.** Sempre `Decimal` / `Numeric`.
6. **Nunca confie em validação feita no navegador.** Valide sempre também no servidor.

---

## Padrão de código

- Nomes de variáveis, funções, tabelas e rotas em **português**, `snake_case`.
- Classes em `PascalCase`: `OrdemServico`, `PedidoManutencao`.
- Toda função que faz mais de uma coisa no banco vai para `app/servicos/`, não fica na rota.
- Linha com no máximo 100 caracteres (o `ruff` avisa).
- Comentário explica **por quê**, não **o quê**. O código já diz o quê.

---

## Deu erro e você não entende

1. Leia a **última linha** da mensagem de erro — geralmente é ela que importa.
2. Copie a mensagem inteira e pesquise.
3. Não resolveu em 40 minutos? Peça ajuda na issue, colando: o que você tentou, a mensagem
   completa e o link do seu branch. Marque **@Buehno**.

Pedir ajuda cedo é eficiência, não fraqueza. O combinado do time é esse.
