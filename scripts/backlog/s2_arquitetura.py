"""Sprint 2 — 15/09 a 28/09/2026. Entrega 2: arquitetura e protótipo que já roda."""

from scripts.backlog.modelo import (
    AVANCADO,
    BLOQUEIA,
    DESAFIO,
    EQUIPE,
    INICIANTE,
    INTERMEDIARIO,
    M2,
    RONALDO,
    Tarefa,
)

TAREFAS = [
    Tarefa(
        titulo="[S2] Definir a arquitetura em camadas e escrever docs/01-arquitetura.md",
        milestone=M2,
        labels=[RONALDO, AVANCADO, "tipo: doc", BLOQUEIA],
        estimativa="3h",
        objetivo=(
            "Documento de arquitetura explicando as camadas (rotas → regras de negócio → modelos "
            "→ banco), o padrão de blueprints, como o PWA se encaixa, e um diagrama do fluxo "
            "'pedido de manutenção vira ordem de serviço'."
        ),
        porque=(
            "É metade da nota da Entrega 2 e é o contrato que impede sete pessoas de escreverem "
            "sete estilos de código diferentes."
        ),
        passos=[
            "Desenhar o diagrama de camadas e o fluxo principal (Mermaid dentro do markdown).",
            "Definir e escrever a regra: rota nunca fala com o banco direto quando a operação tem mais de um passo — isso vai para uma função de serviço.",
            "Documentar a convenção de nomes (português nos modelos e rotas, snake_case).",
            "Documentar a estratégia de PWA (service worker na raiz, cache por versão).",
            "Documentar a decisão de banco: SQLite no desenvolvimento, com caminho para PostgreSQL sem mudar código (SQLAlchemy).",
        ],
        aceite=[
            "Diagrama de camadas e diagrama do fluxo pedido→OS renderizando no GitHub",
            "Convenções de nome e de commit escritas",
            "Justificativa de cada biblioteca escolhida, ligada ao cardápio da disciplina",
        ],
        arquivos=["docs/01-arquitetura.md"],
    ),
    Tarefa(
        titulo="[S2] Modelar o banco completo em SQLAlchemy e gerar a primeira migração",
        milestone=M2,
        labels=[RONALDO, AVANCADO, "tipo: banco", BLOQUEIA],
        estimativa="5h",
        objetivo=(
            "As 20 tabelas do documento de arquitetura viradas em modelos SQLAlchemy, com as "
            "cardinalidades corretas (N:N de usuários/perfis, 1:1 de pedido/OS), e a migração "
            "inicial gerada pelo Alembic."
        ),
        porque=(
            "Toda tarefa de cadastro dos outros integrantes depende destes modelos. Se a "
            "modelagem estiver errada, o grupo inteiro refaz trabalho em outubro."
        ),
        passos=[
            "Transcrever as tabelas da seção 6 da documentação para `app/models/`.",
            "Conferir cada cardinalidade da seção 7 contra o relacionamento escrito no código.",
            "Rodar `flask db init`, `flask db migrate -m \"estrutura inicial\"`, `flask db upgrade`.",
            "Escrever o seed com dados de exemplo suficientes para demonstrar o sistema.",
            "Documentar o modelo em `docs/04-modelo-de-dados.md` com o diagrama entidade-relacionamento.",
        ],
        aceite=[
            "As 20 tabelas criadas no SQLite após `flask db upgrade`",
            "`PedidoManutencao 1:1 OrdemServico` garantido por constraint `unique` na FK",
            "`flask seed` popula o banco sem erro e roda duas vezes seguidas sem duplicar dados",
            "Diagrama ER no docs/04 batendo com o código",
        ],
        arquivos=["app/models/*.py", "seeds/carregar.py", "docs/04-modelo-de-dados.md"],
    ),
    Tarefa(
        titulo="[S2] Implementar autenticação: login, logout e senha com hash",
        milestone=M2,
        labels=[RONALDO, AVANCADO, "tipo: backend", BLOQUEIA],
        estimativa="4h",
        objetivo=(
            "Login funcionando com Flask-Login, senha guardada como hash (nunca em texto puro), "
            "proteção CSRF nos formulários e redirecionamento para a página que a pessoa tentou "
            "acessar antes do login."
        ),
        porque=(
            "É requisito não-funcional explícito de segurança do projeto, e é o tipo de coisa que "
            "se for feita errada por alguém sem experiência vira uma falha grave na apresentação."
        ),
        passos=[
            "Configurar `LoginManager`, `user_loader` e `login_view`.",
            "Usar `generate_password_hash` / `check_password_hash` do Werkzeug.",
            "Ativar `CSRFProtect` e usar `form.hidden_tag()` em todos os formulários.",
            "Tratar o parâmetro `next` com validação para não virar vetor de redirecionamento aberto.",
            "Escrever os testes: senha errada não entra, senha certa entra, hash != senha.",
        ],
        aceite=[
            "Nenhuma senha em texto puro no banco (confira abrindo o .db)",
            "Página protegida redireciona para /login com o `next` correto",
            "Formulário sem token CSRF é recusado",
            "Testes de autenticação passando no CI",
        ],
        arquivos=["app/blueprints/auth/routes.py", "app/models/usuario.py", "tests/"],
    ),
    Tarefa(
        titulo="[S2] Implementar perfis e permissões (Administrador, Gestor, Técnico, Cliente)",
        milestone=M2,
        labels=[RONALDO, AVANCADO, "tipo: backend"],
        estimativa="3h",
        objetivo=(
            "Decorador `@requer_perfil(...)` funcionando e os 4 perfis do diagrama de casos de uso "
            "com suas permissões carregadas pelo seed."
        ),
        porque=(
            "O diagrama de casos de uso define quem pode o quê. Sem isso, qualquer usuário aprova "
            "o próprio pedido — e o professor vai perguntar exatamente isso na apresentação."
        ),
        passos=[
            "Implementar `requer_perfil` como decorador que devolve 403 quando o perfil não bate.",
            "Popular perfis e permissões no seed conforme a matriz da documentação.",
            "Esconder no menu (template) os links que o perfil não pode acessar — mas sempre validando também no servidor.",
            "Escrever teste: técnico recebe 403 ao tentar aprovar pedido.",
        ],
        aceite=[
            "Os 4 perfis existem com permissões distintas",
            "Rota protegida devolve 403 para perfil errado (validado no servidor, não só no menu)",
            "Página 403 amigável, sem stack trace",
        ],
        arquivos=["app/blueprints/auth/routes.py", "seeds/carregar.py"],
        exemplo=(
            "```python\n"
            "@bp.route('/pedidos/<int:id_pedido>/aprovar', methods=['POST'])\n"
            "@requer_perfil('GESTOR', 'ADMINISTRADOR')\n"
            "def aprovar(id_pedido):\n"
            "    ...\n"
            "```"
        ),
    ),
    Tarefa(
        titulo="[S2] Extrair as cores, fontes e espaçamentos do Figma para o CSS",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: frontend", BLOQUEIA],
        estimativa="2h",
        objetivo=(
            "As variáveis de cor, tamanho de fonte, espaçamento e raio de borda do protótipo do "
            "Figma escritas como variáveis CSS no topo de `app/static/css/app.css`."
        ),
        porque=(
            "Se cada pessoa escolher a própria cor de botão, o sistema fica com cara de sete "
            "sistemas. Uma variável, um valor, o site inteiro muda junto."
        ),
        passos=[
            "Abra o protótipo do Figma (link fixado no README).",
            "Anote: cor primária, cor de fundo, cor de texto, cor de sucesso, cor de erro, cor de borda.",
            "Anote os espaçamentos usados (geralmente múltiplos de 4 ou 8 pixels) e o raio de canto dos cartões.",
            "Preencha o bloco `:root { ... }` do `app.css` com esses valores.",
            "Confira se as cores de texto sobre fundo têm contraste suficiente (mínimo 4.5:1) usando https://webaim.org/resources/contrastchecker/.",
            "Nunca mais escreva uma cor solta no CSS: sempre `var(--cor-primaria)`.",
        ],
        exemplo=(
            "```css\n"
            ":root {\n"
            "  --cor-primaria: #0F766E;   /* botões e topo */\n"
            "  --cor-fundo: #F8FAFC;      /* fundo das páginas */\n"
            "  --cor-texto: #0F172A;\n"
            "  --espaco: 16px;            /* respiro padrão */\n"
            "  --raio: 12px;              /* canto arredondado dos cartões */\n"
            "}\n\n"
            "/* certo */   .botao { background: var(--cor-primaria); }\n"
            "/* errado */  .botao { background: #0F766E; }\n"
            "```"
        ),
        aceite=[
            "Pelo menos 8 variáveis definidas em `:root`",
            "Nenhuma cor escrita em hexadecimal fora do bloco `:root`",
            "Todas as combinações texto/fundo com contraste ≥ 4.5:1, print do verificador na issue",
        ],
        arquivos=["app/static/css/app.css", "docs/05-pwa.md"],
        estudar=[
            "Variáveis CSS em 10 min: https://developer.mozilla.org/pt-BR/docs/Web/CSS/Using_CSS_custom_properties",
        ],
    ),
    Tarefa(
        titulo="[S2] Construir o layout base responsivo (topo, menu e barra inferior)",
        milestone=M2,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: frontend", BLOQUEIA],
        estimativa="4h em dupla",
        objetivo=(
            "O `base.html` com topo fixo, menu lateral no computador, barra de navegação inferior "
            "no celular, e área de avisos (mensagens de sucesso/erro). Todas as telas do sistema "
            "vão herdar deste arquivo."
        ),
        porque=(
            "Herança de template é o que evita copiar e colar o cabeçalho em 30 páginas. Mude "
            "aqui, muda em todas."
        ),
        passos=[
            "Entenda o `{% extends %}` e `{% block %}` do Jinja2 — são as duas palavras que fazem tudo funcionar.",
            "Escreva o layout **primeiro para celular** (uma coluna, barra embaixo).",
            "Só depois adicione `@media (min-width: 768px)` para o menu lateral aparecer e a barra inferior sumir.",
            "Garanta que todo botão e link tenha no mínimo **44x44 pixels** de área de toque (regra da Apple para dedo).",
            "Use `env(safe-area-inset-bottom)` no rodapé para não ficar embaixo da barrinha do iPhone.",
            "Teste no navegador com F12 → ícone de celular, nos tamanhos 390px (iPhone), 768px (tablet) e 1280px (notebook).",
        ],
        exemplo=(
            "```html\n"
            "<!-- filha.html -->\n"
            "{% extends \"base.html\" %}\n"
            "{% block titulo %}Equipamentos{% endblock %}\n"
            "{% block conteudo %}\n"
            "  <h1>Equipamentos</h1>\n"
            "{% endblock %}\n"
            "```\n\n"
            "```css\n"
            "/* mobile-first: escreva o celular primeiro, SEM media query */\n"
            ".cartoes { display: grid; grid-template-columns: repeat(2, 1fr); }\n\n"
            "/* depois, a tela grande */\n"
            "@media (min-width: 768px) {\n"
            "  .cartoes { grid-template-columns: repeat(4, 1fr); }\n"
            "}\n"
            "```"
        ),
        aceite=[
            "Prints nos 3 tamanhos (390px, 768px, 1280px) anexados na issue",
            "Nenhuma barra de rolagem horizontal em 390px",
            "Áreas de toque com no mínimo 44x44px",
            "Mensagens flash aparecem com cor certa (verde sucesso, vermelho erro)",
        ],
        arquivos=["app/templates/base.html", "app/static/css/app.css"],
        estudar=[
            "Jinja2 — herança de templates: https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance",
            "Mobile-first em 8 min: https://developer.mozilla.org/pt-BR/docs/Learn/CSS/CSS_layout/Responsive_Design",
        ],
    ),
    Tarefa(
        titulo="[S2] Montar a tela de login seguindo o protótipo do Figma",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: frontend"],
        estimativa="2h",
        objetivo=(
            "A tela de login bonita e igual ao Figma, com mensagem de erro clara quando a senha "
            "está errada e sem zoom automático ao tocar no campo no iPhone."
        ),
        porque=(
            "É a primeira tela que o professor vai ver na apresentação. Primeira impressão conta — "
            "e é uma tela simples, ótima para a primeira contribuição de quem nunca abriu um PR."
        ),
        passos=[
            "Abra `app/templates/auth/login.html` — o formulário já funciona, você vai cuidar do visual.",
            "Compare lado a lado com a tela do Figma e ajuste espaçamentos, tamanho de fonte e posição do logo.",
            "Garanta `font-size: 16px` nos `<input>` — abaixo disso o Safari do iPhone dá zoom sozinho e fica feio.",
            "Adicione `autocomplete=\"username\"` e `autocomplete=\"current-password\"` para o celular sugerir a senha salva.",
            "Teste errando a senha de propósito: a mensagem precisa aparecer em vermelho e legível.",
        ],
        aceite=[
            "Print lado a lado (Figma × sistema) na issue",
            "Sem zoom automático ao tocar nos campos no iPhone/Safari",
            "Mensagem de erro visível e em português",
            "Funciona com teclado: Tab navega, Enter envia",
        ],
        arquivos=["app/templates/auth/login.html"],
    ),
    Tarefa(
        titulo="[S2] Montar o painel (dashboard) com os 4 cartões de indicadores",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: frontend"],
        estimativa="3h",
        objetivo=(
            "Painel inicial com 4 cartões: pedidos abertos, OS em execução, OS concluídas e peças "
            "em alerta de estoque. Dois por linha no celular, quatro por linha no computador."
        ),
        porque=(
            "É a tela que resume o sistema inteiro em 5 segundos — é dela que você vai falar na "
            "apresentação."
        ),
        passos=[
            "Os números já vêm prontos da rota em `app/blueprints/dashboard/routes.py` (variável `indicadores`).",
            "Monte os cartões com CSS Grid — comece com 2 colunas e mude para 4 dentro do `@media`.",
            "Cada cartão: número grande em cima, rótulo pequeno embaixo.",
            "Deixe cada cartão clicável, levando para a lista correspondente.",
            "Se o número for zero, mostre o cartão mesmo assim (zero também é informação).",
        ],
        aceite=[
            "2 colunas no celular, 4 no computador",
            "Cartões clicáveis levando para a listagem certa",
            "Números batem com o que está no banco (confira rodando o seed)",
        ],
        arquivos=["app/templates/dashboard/index.html"],
        estudar=[
            "CSS Grid em 10 min: https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout",
        ],
    ),
    Tarefa(
        titulo="[S2] CRUD de Departamentos — seu primeiro módulo completo",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: backend", DESAFIO],
        estimativa="4h (é a tarefa que mais ensina do projeto)",
        objetivo=(
            "Cadastro de departamentos funcionando de ponta a ponta: listar, criar, editar e "
            "excluir. É o módulo mais simples do sistema (a tabela tem só 3 colunas) e por isso é "
            "o melhor lugar para aprender o padrão que todos os outros módulos seguem."
        ),
        porque=(
            "CRUD é 80% de qualquer sistema de gestão. Quando você entender este, os outros dez "
            "módulos viram repetição — e você vai conseguir revisar o código dos colegas."
        ),
        passos=[
            "Abra `app/blueprints/equipamentos/routes.py` — é o **módulo de referência**. Leia inteiro antes de escrever qualquer linha.",
            "Crie `app/blueprints/departamentos/routes.py` copiando a ESTRUTURA (não copie e cole cegamente: entenda cada rota).",
            "Crie o formulário `DepartamentoForm` com os campos `nome_departamento` (obrigatório) e `responsavel` (opcional).",
            "Crie as rotas: `listar` (GET), `novo` (GET+POST), `editar` (GET+POST), `excluir` (POST).",
            "Crie os templates `listar.html` e `form.html` em `app/templates/departamentos/`.",
            "Registre o blueprint em `app/__init__.py` (tem uma linha comentada esperando por você).",
            "Adicione o link no menu do `base.html`.",
            "CUIDADO: a rota de excluir precisa ser **POST**, nunca GET. Se for GET, o navegador pode apagar o registro sozinho ao pré-carregar o link.",
        ],
        exemplo=(
            "```python\n"
            "# o esqueleto que TODO módulo de cadastro segue\n"
            "@bp.route('/')\n"
            "@login_required\n"
            "def listar():\n"
            "    itens = db.session.scalars(db.select(Departamento)).all()\n"
            "    return render_template('departamentos/listar.html', itens=itens)\n"
            "\n"
            "@bp.route('/novo', methods=['GET', 'POST'])\n"
            "@login_required\n"
            "def novo():\n"
            "    form = DepartamentoForm()\n"
            "    if form.validate_on_submit():        # só é True no POST com dados válidos\n"
            "        item = Departamento()\n"
            "        form.populate_obj(item)          # copia os campos do form para o objeto\n"
            "        db.session.add(item)\n"
            "        db.session.commit()              # sem o commit, NADA é salvo\n"
            "        flash('Departamento cadastrado.', 'sucesso')\n"
            "        return redirect(url_for('departamentos.listar'))\n"
            "    return render_template('departamentos/form.html', form=form)\n"
            "```"
        ),
        aceite=[
            "Consigo criar, ver na lista, editar e excluir um departamento pelo navegador",
            "Formulário sem nome preenchido mostra erro e NÃO salva",
            "Excluir usa POST e pede confirmação",
            "Aparece mensagem verde de sucesso depois de cada ação",
            "Link do módulo no menu",
        ],
        testar=[
            "Cadastre 'Produção' e confira se aparece na lista",
            "Tente salvar com o nome vazio — tem que dar erro na tela, não erro 500",
            "Edite o responsável e confira se mudou na lista",
            "Exclua e confirme que sumiu",
        ],
        arquivos=[
            "app/blueprints/departamentos/routes.py",
            "app/templates/departamentos/",
            "app/__init__.py",
        ],
        extra=(
            "Adicione uma caixa de busca na listagem que filtra pelo nome do departamento. "
            "Dica: `.ilike(f'%{busca}%')` no `db.select`."
        ),
        estudar=[
            "Flask-WTF formulários: https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/",
            "O que é CRUD: https://pt.wikipedia.org/wiki/CRUD",
        ],
    ),
    Tarefa(
        titulo="[S2] CRUD de Grupos e Subgrupos (cadastro com campo dependente)",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Cadastro de Grupos e de Subgrupos, onde o subgrupo precisa escolher a qual grupo "
            "pertence através de uma lista suspensa."
        ),
        porque=(
            "É o primeiro cadastro com **chave estrangeira** — o momento em que você entende na "
            "prática o que significa 'Grupos 1:N SubGrupos' do diagrama."
        ),
        passos=[
            "Faça primeiro o CRUD de Grupos (é igual ao de Departamentos).",
            "No CRUD de Subgrupos, use `SelectField` do WTForms para o campo `id_grupo`.",
            "Atenção: as opções do `SelectField` precisam ser carregadas ANTES do `validate_on_submit()`, senão a validação falha sempre. Veja o método `carregar_opcoes()` no módulo de referência.",
            "Na listagem de subgrupos, mostre o nome do grupo (não o número do id) — use o relacionamento: `subgrupo.grupo_rel.grupo`.",
            "Impeça excluir um grupo que ainda tem subgrupos: mostre uma mensagem explicando, em vez de deixar dar erro.",
        ],
        aceite=[
            "Lista suspensa de grupos preenchida com os grupos do banco",
            "Listagem mostra o NOME do grupo, não o id",
            "Excluir grupo com subgrupos mostra aviso e não quebra o sistema",
        ],
        arquivos=["app/blueprints/catalogo/", "app/templates/catalogo/"],
    ),
    Tarefa(
        titulo="[S2] Melhorar o CRUD de Equipamentos: busca, filtro por grupo e paginação",
        milestone=M2,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend", DESAFIO],
        estimativa="5h",
        objetivo=(
            "A listagem de equipamentos com campo de busca por descrição, filtro por grupo e "
            "paginação de 20 em 20 — porque uma fábrica tem centenas de máquinas e a página não "
            "pode carregar todas de uma vez."
        ),
        porque=(
            "Performance é requisito não-funcional da documentação. E listagem sem paginação é o "
            "erro número 1 de sistema de faculdade: funciona com 5 registros, trava com 5 mil."
        ),
        passos=[
            "O CRUD básico já existe em `app/blueprints/equipamentos/routes.py` — você vai melhorá-lo.",
            "Adicione o filtro por grupo com um `<select>` que envia por GET (para o filtro ficar salvo na URL e poder ser compartilhado).",
            "Troque o `.all()` por `db.paginate(consulta, page=pagina, per_page=20)`.",
            "Monte os botões 'Anterior / Próxima' mantendo a busca e o filtro na URL.",
            "Mostre 'Nenhum resultado para X' quando a busca não achar nada — nunca uma tabela vazia sem explicação.",
        ],
        exemplo=(
            "```python\n"
            "pagina = request.args.get('pagina', 1, type=int)\n"
            "consulta = db.select(Equipamento).order_by(Equipamento.codigo)\n"
            "if busca:\n"
            "    consulta = consulta.filter(Equipamento.descricao.ilike(f'%{busca}%'))\n"
            "resultado = db.paginate(consulta, page=pagina, per_page=20, error_out=False)\n"
            "# no template: resultado.items, resultado.has_next, resultado.page, resultado.pages\n"
            "```"
        ),
        aceite=[
            "Busca, filtro e paginação funcionam JUNTOS (buscar na página 2 mantém o filtro)",
            "Mensagem amigável quando não há resultado",
            "Máximo de 20 registros por página",
        ],
        arquivos=["app/blueprints/equipamentos/routes.py"],
        extra="Faça a busca funcionar também pelo código do equipamento, não só pela descrição.",
    ),
    Tarefa(
        titulo="[S2] Configurar o CI no GitHub Actions (testes + lint a cada Pull Request)",
        milestone=M2,
        labels=[RONALDO, AVANCADO, "tipo: teste"],
        estimativa="2h",
        objetivo=(
            "Toda vez que alguém abre um Pull Request, o GitHub roda `pytest` e `ruff` "
            "automaticamente e mostra ✅ ou ❌ antes de qualquer um revisar."
        ),
        porque=(
            "Com sete pessoas iniciantes, o CI é o revisor que nunca dorme. Ele pega o erro de "
            "sintaxe antes que ele chegue na main e trave o grupo inteiro."
        ),
        passos=[
            "Criar `.github/workflows/ci.yml` com Python 3.11.",
            "Rodar `ruff check .` e `pytest -q`.",
            "Marcar o check como obrigatório na regra de proteção da branch `main`.",
            "Deixar a mensagem de falha legível para quem nunca viu um CI.",
        ],
        aceite=[
            "PR com teste quebrado fica com ❌ e não pode ser mesclado",
            "Tempo total do CI abaixo de 3 minutos",
        ],
        arquivos=[".github/workflows/ci.yml"],
    ),
    Tarefa(
        titulo="[S2] Escrever seus primeiros testes automatizados com pytest",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: teste", DESAFIO],
        estimativa="3h",
        objetivo=(
            "Pelo menos 6 testes cobrindo o CRUD que você construiu: criar salva no banco, "
            "formulário vazio dá erro, listagem mostra o que foi criado, excluir remove."
        ),
        porque=(
            "Teste automatizado é o que permite mexer no código em outubro sem medo de quebrar o "
            "que já funcionava. E é o diferencial que o professor nota na Entrega 3."
        ),
        passos=[
            "Leia `tests/test_smoke.py` — os testes que já existem são o seu modelo.",
            "Entenda a `fixture`: é a função que prepara o cenário (cria a app e o banco de teste) antes de cada teste.",
            "Escreva um teste por comportamento, com nome em português dizendo o que ele verifica: `def test_criar_departamento_salva_no_banco():`.",
            "Use `cliente.post('/departamentos/novo', data={...}, follow_redirects=True)` para simular o preenchimento do formulário.",
            "Rode `pytest -q` e só abra o PR quando estiver tudo verde.",
        ],
        exemplo=(
            "```python\n"
            "def test_criar_departamento_salva_no_banco(cliente, app):\n"
            "    resposta = cliente.post(\n"
            "        '/departamentos/novo',\n"
            "        data={'nome_departamento': 'Produção', 'responsavel': 'Ana'},\n"
            "        follow_redirects=True,\n"
            "    )\n"
            "    assert resposta.status_code == 200\n"
            "    with app.app_context():\n"
            "        assert db.session.scalar(\n"
            "            db.select(Departamento).filter_by(nome_departamento='Produção')\n"
            "        ) is not None\n"
            "```"
        ),
        aceite=[
            "Mínimo de 6 testes novos, todos passando",
            "Cada teste tem nome em português que explica o que ele verifica",
            "Existe pelo menos 1 teste de caminho ruim (formulário inválido)",
        ],
        arquivos=["tests/"],
        estudar=["pytest em 20 min: https://docs.pytest.org/en/stable/getting-started.html"],
    ),
    Tarefa(
        titulo="[S2] Montar o documento da Entrega 2 (arquitetura + prints do protótipo)",
        milestone=M2,
        labels=[EQUIPE, INICIANTE, "tipo: doc"],
        estimativa="3h",
        objetivo=(
            "PDF da Entrega 2 com: arquitetura resumida, diagrama do banco, prints das telas que "
            "já rodam e o link do repositório e do quadro do projeto."
        ),
        porque="É a entrega avaliada no dia 28/09.",
        passos=[
            "Reúna o conteúdo de `docs/01-arquitetura.md` e `docs/04-modelo-de-dados.md`.",
            "Tire prints do login, do painel e de dois cadastros funcionando — no celular E no computador.",
            "Monte o documento no mesmo padrão visual dos anteriores (cabeçalho TechMaint, rev., data).",
            "Inclua o link do repositório e do Project.",
            "Combine quem apresenta cada parte se o professor pedir.",
        ],
        aceite=[
            "PDF entregue até 28/09",
            "Prints mostrando o sistema rodando de verdade (não é mockup do Figma)",
            "Links do repositório e do quadro funcionando",
        ],
        arquivos=["docs/entregas/entrega-2.md"],
    ),
]
