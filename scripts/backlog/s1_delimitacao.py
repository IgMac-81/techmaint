"""Sprint 1 — até 14/09/2026. Entrega 1: grupo, papéis e delimitação."""

from scripts.backlog.modelo import (
    BLOQUEIA,
    EQUIPE,
    INICIANTE,
    M1,
    RONALDO,
    Tarefa,
)

TAREFAS = [
    Tarefa(
        titulo="[S1] Criar repositório, estrutura de pastas e proteger a branch main",
        milestone=M1,
        labels=[RONALDO, "nível: avançado", "tipo: setup", BLOQUEIA],
        estimativa="2h",
        objetivo=(
            "Repositório `TechMind-tech/techmaint` no ar, com a estrutura de pastas do projeto, "
            "`requirements.txt`, `.gitignore`, README, CONTRIBUTING e a branch `main` protegida "
            "(ninguém faz push direto; tudo entra por Pull Request com 1 aprovação)."
        ),
        porque=(
            "Sete pessoas sem experiência mexendo no mesmo código sem proteção = main quebrada "
            "na véspera da entrega. A proteção de branch garante que o que está na main sempre roda."
        ),
        passos=[
            "Criar o repositório na organização TechMind-tech.",
            "Subir a estrutura base: `app/`, `docs/`, `tests/`, `seeds/`, `scripts/`.",
            "Settings → Branches → regra para `main`: exigir Pull Request com 1 aprovação e CI verde.",
            "Criar as labels e os 5 milestones do cronograma.",
            "Convidar os 8 integrantes com permissão `write`.",
        ],
        aceite=[
            "`git clone` + `pip install -r requirements.txt` + `python run.py` funciona em máquina limpa",
            "Push direto na `main` é recusado pelo GitHub",
            "As 5 milestones existem com as datas do cronograma",
            "Todos os integrantes aceitaram o convite da organização",
        ],
        arquivos=["README.md", "CONTRIBUTING.md", ".gitignore", "requirements.txt"],
    ),
    Tarefa(
        titulo="[S1] Configurar seu ambiente e rodar o TechMaint pela primeira vez",
        milestone=M1,
        labels=[EQUIPE, INICIANTE, "tipo: setup", BLOQUEIA],
        estimativa="1h30 (faça hoje, não deixe para a véspera)",
        objetivo=(
            "Seu computador rodando o projeto: Python instalado, ambiente virtual criado, "
            "dependências instaladas e o navegador abrindo a tela de login em "
            "http://127.0.0.1:5000. No fim, comente nesta issue com um print da tela."
        ),
        porque=(
            "Enquanto seu ambiente não roda, você não consegue pegar NENHUMA outra tarefa. "
            "Esta é literalmente a porta de entrada do projeto — e é normal dar erro na primeira "
            "vez: metade do trabalho de programador é fazer o ambiente funcionar."
        ),
        passos=[
            "Instale o **Python 3.11 ou superior** em python.org. No Windows, marque a caixinha **'Add Python to PATH'** na primeira tela do instalador (se esquecer, desinstale e faça de novo).",
            "Instale o **VS Code** e, dentro dele, a extensão **Python** da Microsoft.",
            "Instale o **Git** (git-scm.com) e configure seu nome: `git config --global user.name \"Seu Nome\"` e `git config --global user.email \"seu@email\"`.",
            "Clone o projeto: `git clone https://github.com/TechMind-tech/techmaint.git` e entre na pasta com `cd techmaint`.",
            "Crie o ambiente virtual: `python -m venv .venv`. Ative — Windows: `.venv\\Scripts\\activate` | Mac/Linux: `source .venv/bin/activate`. Deu certo se aparecer `(.venv)` no começo da linha do terminal.",
            "Instale as bibliotecas: `pip install -r requirements.txt`.",
            "Popule o banco de exemplo: `flask --app run.py seed`.",
            "Rode: `python run.py` e abra http://127.0.0.1:5000 no navegador.",
            "Entre com **admin / admin123** e tire um print do painel.",
            "Comente nesta issue com o print e feche-a.",
        ],
        exemplo=(
            "```bash\n"
            "# sequência completa, do zero ao sistema rodando\n"
            "git clone https://github.com/TechMind-tech/techmaint.git\n"
            "cd techmaint\n"
            "python -m venv .venv\n"
            "source .venv/bin/activate      # Windows: .venv\\Scripts\\activate\n"
            "pip install -r requirements.txt\n"
            "flask --app run.py seed\n"
            "python run.py\n"
            "```\n\n"
            "**Erros comuns e o que fazer:**\n\n"
            "| Mensagem | O que aconteceu | Solução |\n"
            "|---|---|---|\n"
            "| `'python' não é reconhecido` | Python fora do PATH | Reinstale marcando 'Add Python to PATH' |\n"
            "| `No module named flask` | Esqueceu de ativar o `.venv` | Ative o venv e rode o `pip install` de novo |\n"
            "| `Address already in use` | Já tem um `python run.py` rodando | Feche o outro terminal ou use `python run.py --port 5001` |\n"
            "| `no such table: usuarios` | Banco vazio | Rode `flask --app run.py seed` |"
        ),
        aceite=[
            "Print da tela de login e do painel comentado na issue",
            "`pytest -q` roda e mostra os testes passando",
            "Você consegue parar (Ctrl+C) e subir o servidor de novo sozinho",
        ],
        estudar=[
            "O que é um ambiente virtual (venv) — 5 min: https://docs.python.org/pt-br/3/tutorial/venv.html",
            "Git em 15 minutos (interativo): https://learngitbranching.js.org/?locale=pt_BR",
        ],
    ),
    Tarefa(
        titulo="[S1] Escrever a delimitação do sistema: o que está dentro e o que está fora",
        milestone=M1,
        labels=[EQUIPE, INICIANTE, "tipo: doc"],
        estimativa="2h em dupla",
        objetivo=(
            "O arquivo `docs/02-roadmap.md` com uma seção de **escopo**: uma lista do que o "
            "TechMaint VAI fazer e — mais importante — uma lista do que ele NÃO vai fazer."
        ),
        porque=(
            "Projeto de faculdade morre por excesso de ambição. Escrever 'não vamos fazer "
            "aplicativo nativo, não vamos integrar com ERP real, não vamos ter chat' agora é o "
            "que salva o grupo em outubro. Escopo definido é entrega garantida."
        ),
        passos=[
            "Releia a seção 4 (Escopo do Sistema) da documentação anexa do projeto.",
            "Liste em `docs/02-roadmap.md`, na seção **Dentro do escopo**, os módulos que vamos entregar: usuários e perfis, equipamentos, peças, fornecedores, notas fiscais, estoque, pedidos de manutenção, ordens de serviço, dashboard e relatórios.",
            "Liste na seção **Fora do escopo (v1)** pelo menos 6 coisas. Sugestões: app nativo na loja, integração real com ERP, emissão fiscal de NF-e de verdade, multiempresa, chat interno, notificações por push.",
            "Para cada item fora do escopo, escreva **uma linha** dizendo por que ficou de fora (tempo, complexidade, não é o foco da matéria).",
            "Abra Pull Request e peça revisão do Igor (gestor) e do Ronaldo (líder técnico).",
        ],
        aceite=[
            "Seção 'Dentro do escopo' com todos os módulos listados",
            "Seção 'Fora do escopo' com no mínimo 6 itens, cada um justificado em uma linha",
            "Texto em português correto, sem 'a gente vai tentar' — use frases afirmativas",
        ],
        arquivos=["docs/02-roadmap.md"],
    ),
    Tarefa(
        titulo="[S1] Registrar o grupo, os papéis e os combinados de comunicação no README",
        milestone=M1,
        labels=[EQUIPE, INICIANTE, "tipo: doc"],
        estimativa="1h",
        objetivo=(
            "Tabela no `README.md` com os 8 integrantes, RA, papel no projeto e usuário do GitHub, "
            "mais os combinados do time (quando é a reunião semanal, onde a gente conversa, "
            "qual o prazo de revisão de Pull Request)."
        ),
        porque=(
            "A Entrega 1 exige exatamente isso. E o papel escrito evita o clássico "
            "'achei que você ia fazer'."
        ),
        passos=[
            "Preencha a tabela de integrantes com nome, RA, papel e @usuário do GitHub.",
            "Papéis já definidos na documentação: Igor Machado (gestor e engenheiro do projeto), Ronaldo Bueno (líder técnico/arquiteto), Victor Henrique, Samuel dos Santos, Bryan dos Reis e Matheus Simaroli (desenvolvedores), Ana Clara (produto e comercial), Rafael dos Santos (dados e integração), qualidade e documentação com todos.",
            "Escreva a seção **Combinados do time**: dia e horário da reunião semanal, canal de conversa, e a regra de que todo Pull Request é revisado em até 24h.",
            "Escreva a **definição de pronto (DoD)**: código roda, testes passam, tem pelo menos 1 aprovação no PR, e a issue foi fechada com um print ou um GIF.",
        ],
        aceite=[
            "Os 8 integrantes na tabela com RA e @usuário do GitHub",
            "Seção 'Combinados do time' com dia/horário da reunião",
            "Definição de pronto escrita e combinada com todo mundo",
        ],
        arquivos=["README.md"],
    ),
    Tarefa(
        titulo="[S1] Montar o quadro do projeto no GitHub Projects e mover as tarefas",
        milestone=M1,
        labels=[EQUIPE, INICIANTE, "tipo: setup"],
        estimativa="45 min",
        objetivo=(
            "Todas as issues visíveis no quadro https://github.com/orgs/TechMind-tech/projects/1 "
            "com as colunas **Backlog → A fazer → Em andamento → Em revisão → Concluído**, do jeito "
            "que a documentação do projeto definiu."
        ),
        porque=(
            "O professor vai olhar o quadro para ver se o grupo está trabalhando de verdade ao "
            "longo do semestre — e não tudo na véspera. O quadro é a nossa prova de processo."
        ),
        passos=[
            "Abra o Project 1 da organização e renomeie as colunas para Backlog, A fazer, Em andamento, Em revisão, Concluído.",
            "Confira se todas as issues criadas apareceram no quadro (elas são adicionadas automaticamente pelo script `scripts/criar_issues.py`).",
            "Mova para **A fazer** só as issues da milestone da Entrega 1 e da Entrega 2. O resto fica no Backlog.",
            "Crie um campo `Sprint` (tipo: seleção) com as opções Sprint 1 a Sprint 5 e classifique as issues.",
            "Regra do time: quem começa uma tarefa move o cartão para **Em andamento** ANTES de escrever a primeira linha de código.",
        ],
        aceite=[
            "Colunas renomeadas conforme a documentação",
            "Todas as issues no quadro, nenhuma solta",
            "Campo Sprint preenchido nas issues das Entregas 1 e 2",
        ],
        estudar=[
            "GitHub Projects em 10 min: https://docs.github.com/pt/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects",
        ],
    ),
]
