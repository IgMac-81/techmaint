# TechMaint

**Sistema de Manutenção Predial e de Máquinas** — aplicação web em Python (Flask) que vira
**aplicativo instalável (PWA)** no iPhone e no Android.

Projeto da disciplina *Projeto de aplicação em Python · desenvolvimento em etapas ·
apresentação final* — UniAnchieta, 2026/2.

- 📋 Quadro de tarefas: https://github.com/orgs/TechMind-tech/projects/1
- 🎨 Protótipo no Figma: https://www.figma.com/make/DTnAujFIGHwCQzlDJ7XCMD/Interface-System-Development
- 📚 Documentação técnica: [`docs/`](docs/)

---

## Começando (leia isto primeiro)

Se é seu primeiro dia no projeto, vá direto para **[docs/00-guia-do-calouro.md](docs/00-guia-do-calouro.md)**.
Ele leva você do zero até o sistema rodando na sua máquina.

Resumo, para quem já tem Python instalado:

```bash
git clone https://github.com/TechMind-tech/techmaint.git
cd techmaint
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app run.py seed        # cria o banco com dados de exemplo
python run.py                  # abre em http://127.0.0.1:5000
```

Login de teste: **admin / admin123**

---

## O que o sistema faz

Gerencia o ciclo completo de manutenção: alguém abre um **pedido**, o gestor **aprova**, o
pedido vira uma **ordem de serviço**, o técnico lança **peças** e **horas**, o estoque baixa
sozinho e o painel mostra os **indicadores**.

| Módulo | O que resolve |
|---|---|
| Usuários, perfis e permissões | Quem pode fazer o quê (Administrador, Gestor, Técnico, Cliente) |
| Equipamentos, grupos e departamentos | Cadastro das máquinas e da estrutura predial |
| Peças e estoque | Saldo, mínimo, alerta de reposição e histórico de movimentação |
| Fornecedores e notas fiscais | Entrada de peças com atualização automática do estoque |
| Pedidos e ordens de serviço | O fluxo de manutenção de ponta a ponta |
| Dashboard e relatórios | Tempo médio de atendimento, custo por máquina, exportação em Excel e PDF |

---

## Tecnologias (100% Python, tudo instalável via pip)

| Camada | Biblioteca | Por quê |
|---|---|---|
| Web | **Flask** | Aplicação web robusta, com rotas e templates — cap. 01 do cardápio |
| Banco | **SQLAlchemy + Flask-Migrate** | ORM que sai do SQLite para PostgreSQL sem mudar código — cap. 11 |
| Templates | **Jinja2** | Já vem com o Flask, herança de layout |
| Formulários e segurança | **Flask-WTF, Flask-Login, Werkzeug** | Validação, CSRF, hash de senha — cap. 16 |
| Dados e gráficos | **pandas, Matplotlib** | Indicadores e gráficos gerados no servidor — cap. 04 |
| Relatórios | **openpyxl, ReportLab** | Exportação em Excel e PDF — cap. 10 |
| Testes | **pytest, ruff** | Qualidade a cada Pull Request — cap. 16 |

**Sem Node, sem npm, sem framework de JavaScript.** O front é HTML + CSS + JavaScript puro,
escrito à mão. O PWA é feito com um `manifest.webmanifest` e um service worker de ~60 linhas.

---

## Time

| Nome | R.A. | Papel | GitHub |
|---|---|---|---|
| Igor Godoy Machado | 2601416 | Gestor e engenheiro do projeto (Scrum Master) | `@preencher` |
| Ronaldo Rodrigues Dias Bueno | 2634808 | Líder técnico / arquiteto | `@Buehno` |
| Ana Clara Vitória Roque | 2603355 | Produto e comercial (Product Owner) | `@preencher` |
| Victor Henrique Guido de Azevedo | 2610770 | Desenvolvedor | `@preencher` |
| Samuel dos Santos Silva | 2628078 | Desenvolvedor | `@preencher` |
| Bryan dos Reis Gomes | 2638152 | Desenvolvedor | `@preencher` |
| Matheus Simaroli de Lima | 2630302 | Desenvolvedor | `@preencher` |
| Rafael dos Santos Carvalho | 2622334 | Dados e integração | `@preencher` |

Qualidade e documentação: **todos**.

---

## Cronograma

| Momento | Data | O que é entregue |
|---|---|---|
| Entrega 1 | 14/09/2026 | Grupo, papéis e delimitação do sistema |
| Entrega 2 | 28/09/2026 | Arquitetura e protótipo que já roda |
| Sprint 3 | 12/10/2026 | Módulos do núcleo (checkpoint interno) |
| Entrega 3 | 26/10/2026 | Versão funcional ponta a ponta e plano da apresentação |
| Apresentação | Novembro/2026 | 15 minutos, com todos os integrantes falando |

Detalhamento em [`docs/02-roadmap.md`](docs/02-roadmap.md).

---

## Combinados do time

- **Reunião semanal** de 30 minutos para revisar o quadro (dia e horário: *a definir na Entrega 1*).
- **Toda tarefa vira issue.** Nada de código sem issue.
- Quem começa uma tarefa move o cartão para **Em andamento** antes da primeira linha de código.
- **Pull Request revisado em até 24h.** Ninguém fica travado esperando.
- **Travou 40 minutos?** Pede ajuda. Isso é regra, não vergonha.

### Definição de pronto (DoD)

Uma tarefa só está pronta quando:

1. O código roda na máquina de outra pessoa, não só na sua.
2. `pytest -q` passa e o CI está verde.
3. O Pull Request tem pelo menos 1 aprovação.
4. A issue foi fechada com um print ou GIF mostrando o resultado.

---

## Contribuindo

Leia [CONTRIBUTING.md](CONTRIBUTING.md) — tem o passo a passo de branch, commit e Pull Request,
escrito para quem nunca usou Git em equipe.
