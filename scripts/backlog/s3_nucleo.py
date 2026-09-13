"""Sprint 3 — 29/09 a 12/10/2026. Módulos do núcleo: cadastros, estoque e fluxo de manutenção."""

from scripts.backlog.modelo import (
    AVANCADO,
    DESAFIO,
    EQUIPE,
    INICIANTE,
    INTERMEDIARIO,
    M3,
    RONALDO,
    Tarefa,
)

TAREFAS = [
    Tarefa(
        titulo="[S3] CRUD de Peças vinculadas ao equipamento",
        milestone=M3,
        labels=[EQUIPE, INICIANTE, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Cadastro de peças com nome, NCM, valor unitário e o equipamento a que pertencem. "
            "Na tela do equipamento, uma aba mostrando as peças dele."
        ),
        porque="'Equipamentos 1:N Peças' é a base do controle de estoque e do custo por máquina.",
        passos=[
            "Crie o CRUD seguindo o padrão do módulo de referência.",
            "Campo `valor_unitario`: use `DecimalField` com `places=2`. **Nunca use `float` para dinheiro** — 0.1 + 0.2 em float dá 0.30000000000000004.",
            "Na listagem, formate o valor como R$ 1.234,56 (crie um filtro Jinja `moeda`).",
            "Adicione na tela de detalhe do equipamento a lista das peças dele.",
            "Impeça valor unitário negativo com um validador `NumberRange(min=0)`.",
        ],
        exemplo=(
            "```python\n"
            "# app/filtros.py — registre com app.jinja_env.filters['moeda'] = moeda\n"
            "def moeda(valor):\n"
            "    if valor is None:\n"
            "        return 'R$ 0,00'\n"
            "    texto = f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')\n"
            "    return f'R$ {texto}'\n"
            "```\n"
            "No template: `{{ peca.valor_unitario | moeda }}`"
        ),
        aceite=[
            "Peça sempre vinculada a um equipamento existente",
            "Valores aparecem no formato brasileiro R$ 1.234,56",
            "Valor negativo é recusado com mensagem na tela",
        ],
        arquivos=["app/blueprints/pecas/", "app/templates/pecas/"],
    ),
    Tarefa(
        titulo="[S3] CRUD de Fornecedores com validação de CNPJ",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend", DESAFIO],
        estimativa="5h",
        objetivo=(
            "Cadastro completo de fornecedores (razão social, CNPJ, endereço, contato) com "
            "validação de verdade do CNPJ — o cálculo dos dois dígitos verificadores."
        ),
        porque=(
            "É a tarefa mais divertida do sprint: você implementa um algoritmo real, usado por "
            "todo sistema brasileiro. E impede o clássico CNPJ '11111111111111' no banco."
        ),
        passos=[
            "Crie o CRUD seguindo o padrão.",
            "Escreva a função `cnpj_valido(cnpj)` em `app/validadores.py` — recebe a string, tira pontuação e confere os dois dígitos verificadores.",
            "Guarde o CNPJ **só com números** no banco (14 caracteres), e formate na exibição.",
            "Crie um validador WTForms customizado que usa essa função.",
            "Impeça CNPJ duplicado (a coluna já é `unique`, mas trate o erro para mostrar mensagem amigável em vez de erro 500).",
            "Escreva testes: um CNPJ válido de verdade passa, um inválido não passa, um com máscara também passa.",
        ],
        exemplo=(
            "```python\n"
            "def cnpj_valido(cnpj: str) -> bool:\n"
            "    numeros = ''.join(c for c in cnpj if c.isdigit())\n"
            "    if len(numeros) != 14 or numeros == numeros[0] * 14:\n"
            "        return False\n"
            "\n"
            "    def digito(base: str, pesos: list[int]) -> str:\n"
            "        soma = sum(int(d) * p for d, p in zip(base, pesos))\n"
            "        resto = soma % 11\n"
            "        return '0' if resto < 2 else str(11 - resto)\n"
            "\n"
            "    p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]\n"
            "    p2 = [6] + p1\n"
            "    d1 = digito(numeros[:12], p1)\n"
            "    d2 = digito(numeros[:12] + d1, p2)\n"
            "    return numeros[12:] == d1 + d2\n"
            "```"
        ),
        aceite=[
            "CNPJ inválido é recusado com mensagem clara no formulário",
            "CNPJ salvo sem pontuação, exibido com máscara 00.000.000/0000-00",
            "CNPJ duplicado mostra aviso amigável, não erro 500",
            "Pelo menos 4 testes da função de validação",
        ],
        arquivos=["app/blueprints/fornecedores/", "app/validadores.py", "tests/test_validadores.py"],
        extra=(
            "Faça o mesmo para CPF e crie uma máscara automática no campo com JavaScript puro "
            "(sem biblioteca), formatando enquanto a pessoa digita."
        ),
    ),
    Tarefa(
        titulo="[S3] CRUD de Prestadores de Serviço",
        milestone=M3,
        labels=[EQUIPE, INICIANTE, "tipo: backend"],
        estimativa="3h",
        objetivo="Cadastro de empresas que executam serviços nas ordens de serviço.",
        porque=(
            "A tabela é quase idêntica à de fornecedores — é a tarefa perfeita para você provar "
            "que entendeu o padrão e conseguir fazer sozinho, sem consultar o exemplo o tempo todo."
        ),
        passos=[
            "Reaproveite a função `cnpj_valido` já criada (importe, não copie e cole).",
            "Crie o CRUD completo.",
            "Adicione o campo `ativo` e, na listagem, mostre por padrão só os ativos, com uma caixinha 'mostrar inativos'.",
            "Em vez de excluir de verdade, marque `ativo = False` (isso se chama exclusão lógica — a gente nunca perde o histórico).",
        ],
        aceite=[
            "Exclusão é lógica (marca inativo), não apaga do banco",
            "Listagem mostra só ativos por padrão",
            "A validação de CNPJ é importada, não duplicada",
        ],
        arquivos=["app/blueprints/prestadores/"],
    ),
    Tarefa(
        titulo="[S3] Cadastro de Nota Fiscal com itens (formulário mestre-detalhe)",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend"],
        estimativa="6h em dupla",
        objetivo=(
            "Tela onde se cadastra a nota (fornecedor, número, data, impostos) e, na mesma "
            "página, vários itens (peça, quantidade, valor unitário), com o total calculado "
            "automaticamente."
        ),
        porque=(
            "É o primeiro formulário com N filhos — o padrão mais comum em sistema de gestão e o "
            "que mais dá trabalho de acertar. Quem fizer esta tarefa vai saber fazer qualquer "
            "formulário depois."
        ),
        passos=[
            "Use `FieldList(FormField(ItemNotaForm))` do WTForms para a lista de itens.",
            "Adicione um botão '+ Adicionar item' em JavaScript puro que clona a última linha do formulário e renumera os campos.",
            "Calcule `valor_total` de cada item (quantidade × valor unitário) no servidor — **nunca confie na conta feita no navegador**, o usuário pode alterar.",
            "Some os itens e compare com o `valor_total_nf` digitado; se a diferença for maior que R$ 0,01, avise (mas deixe salvar, porque frete e impostos podem explicar).",
            "Salve a nota e os itens dentro da MESMA transação: se um item falhar, nada é salvo.",
        ],
        exemplo=(
            "```python\n"
            "try:\n"
            "    nota = NotaFiscal(...)\n"
            "    db.session.add(nota)\n"
            "    db.session.flush()          # gera o id da nota sem fechar a transação\n"
            "    for dados in form.itens.data:\n"
            "        item = ItemNotaFiscal(id_nota_fiscal=nota.id_nota_fiscal, **dados)\n"
            "        item.valor_total = item.qtde * item.valor_unitario\n"
            "        db.session.add(item)\n"
            "    db.session.commit()         # só agora tudo vira definitivo\n"
            "except Exception:\n"
            "    db.session.rollback()       # deu errado? desfaz TUDO\n"
            "    raise\n"
            "```"
        ),
        aceite=[
            "Consigo cadastrar uma nota com 3 itens em uma única tela",
            "Total de cada item calculado no servidor",
            "Erro em um item não deixa a nota salva pela metade",
            "Aviso quando a soma dos itens não bate com o total da nota",
        ],
        arquivos=["app/blueprints/notas/", "app/templates/notas/"],
        estudar=[
            "FieldList do WTForms: https://wtforms.readthedocs.io/en/3.1.x/fields/#field-enclosures",
        ],
    ),
    Tarefa(
        titulo="[S3] Regra de negócio: entrada de nota fiscal atualiza o estoque",
        milestone=M3,
        labels=[RONALDO, AVANCADO, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Ao confirmar a entrada de uma nota fiscal, cada item soma no `EstoquePeca` e gera um "
            "registro em `MovimentacaoEstoquePeca`, tudo em uma transação única e sem risco de "
            "duplicar se a pessoa clicar duas vezes."
        ),
        porque=(
            "É a primeira regra de negócio com efeito colateral em outra tabela. Feita errada, o "
            "estoque fica com número errado e o dashboard inteiro mente."
        ),
        passos=[
            "Criar `app/servicos/estoque.py` com `dar_entrada_por_nota(id_nota)`.",
            "Marcar a nota com um status para impedir processar duas vezes (idempotência).",
            "Registrar a movimentação com `documento_origem = f'NF-{numero}'` para rastreabilidade.",
            "Tratar o caso de peça sem registro de estoque ainda (criar o `EstoquePeca` na hora).",
            "Escrever o teste: processar a mesma nota duas vezes não dobra o estoque.",
        ],
        aceite=[
            "Estoque sobe exatamente a quantidade da nota",
            "Processar a mesma nota duas vezes não altera o estoque na segunda vez",
            "Falha no meio do processo não deixa estoque inconsistente (rollback)",
            "Teste automatizado cobrindo os três casos acima",
        ],
        arquivos=["app/servicos/estoque.py", "tests/test_estoque.py"],
    ),
    Tarefa(
        titulo="[S3] Tela de estoque de peças com alerta de estoque baixo",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: frontend"],
        estimativa="4h",
        objetivo=(
            "Listagem do estoque com quantidade atual, mínimo, local — e as linhas abaixo do "
            "mínimo destacadas em vermelho, com um filtro 'mostrar só os em alerta'."
        ),
        porque=(
            "'Alertas de baixo estoque' é requisito funcional explícito. E é o indicador que "
            "aparece no painel — a tela precisa bater com o cartão."
        ),
        passos=[
            "A propriedade `abaixo_do_minimo` já existe no modelo `EstoquePeca` — use ela no template.",
            "Destaque a linha com uma classe CSS, não com cor escrita direto no HTML.",
            "Não use SÓ a cor para indicar o alerta: adicione também um ícone ou a palavra 'Repor' (tem gente daltônica).",
            "Adicione o filtro `?alerta=1` na URL.",
            "Ordene por padrão: os mais críticos primeiro.",
        ],
        aceite=[
            "Linhas em alerta destacadas com cor E texto",
            "Filtro 'só em alerta' funcionando pela URL",
            "O número de peças em alerta bate com o cartão do painel",
        ],
        arquivos=["app/blueprints/estoque/", "app/templates/estoque/"],
    ),
    Tarefa(
        titulo="[S3] Movimentação manual de estoque (entrada e saída avulsa)",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Tela para registrar entrada ou saída de peça fora da nota fiscal (ajuste de "
            "inventário, devolução), sempre com motivo obrigatório e gravando o histórico."
        ),
        porque=(
            "'Histórico de consumo e movimentação de peças' é requisito da documentação. E é o "
            "que permite auditar por que o número mudou."
        ),
        passos=[
            "Formulário com peça, tipo (ENTRADA/SAÍDA), quantidade e observação obrigatória.",
            "**Bloqueie saída maior que o saldo** — mostre 'Saldo insuficiente: disponível X'.",
            "Reaproveite o serviço `app/servicos/estoque.py` (não reescreva a regra).",
            "Mostre o histórico das últimas 20 movimentações da peça na mesma tela.",
        ],
        aceite=[
            "Saída maior que o saldo é recusada com mensagem clara",
            "Toda movimentação fica no histórico com data, tipo, quantidade e motivo",
            "A quantidade em `EstoquePeca` sempre bate com a soma das movimentações",
        ],
        arquivos=["app/blueprints/estoque/"],
        extra="Crie uma tela de 'extrato da peça', igual a um extrato bancário, com saldo acumulado linha a linha.",
    ),
    Tarefa(
        titulo="[S3] Abrir pedido de manutenção (o fluxo começa aqui)",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend"],
        estimativa="5h",
        objetivo=(
            "Tela onde técnico ou cliente abre um pedido: escolhe a máquina, o departamento, "
            "descreve o problema e define a prioridade. O pedido nasce com status ABERTO."
        ),
        porque=(
            "É o caso de uso número 1 do diagrama e o começo da demonstração da apresentação. "
            "Se essa tela for confusa, a apresentação inteira fica confusa."
        ),
        passos=[
            "Formulário com equipamento (lista suspensa com busca), departamento, descrição do problema (mínimo 20 caracteres) e prioridade.",
            "Preencha o campo `solicitante` automaticamente com `current_user.nome` — não peça para a pessoa digitar o próprio nome.",
            "Status inicial sempre ABERTO, definido no servidor (nunca aceite o status vindo do formulário).",
            "Depois de salvar, leve para a tela de detalhe do pedido mostrando o número gerado.",
            "Faça a tela funcionar bem no celular: é lá que o técnico vai abrir o pedido, no meio do chão de fábrica.",
        ],
        aceite=[
            "Pedido criado com status ABERTO e solicitante preenchido automaticamente",
            "Descrição com menos de 20 caracteres é recusada",
            "Tela usável com uma mão só no celular (campos grandes, botão no alcance do polegar)",
            "Número do pedido visível depois de salvar",
        ],
        arquivos=["app/blueprints/manutencao/"],
    ),
    Tarefa(
        titulo="[S3] Aprovar ou rejeitar pedido (só o gestor pode)",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Fila de pedidos aguardando decisão, com botões Aprovar e Rejeitar. Rejeitar exige "
            "escrever o motivo. Só perfil GESTOR ou ADMINISTRADOR enxerga os botões — e só eles "
            "conseguem executar a ação, mesmo chamando a URL direto."
        ),
        porque=(
            "'Aprovar Pedidos' é caso de uso exclusivo do Gestor no diagrama. Esta é a tarefa que "
            "prova que o controle de acesso funciona de verdade."
        ),
        passos=[
            "Use o decorador `@requer_perfil('GESTOR', 'ADMINISTRADOR')` nas rotas de aprovar e rejeitar.",
            "Esconda os botões no template para quem não pode — mas **mantenha a validação no servidor**: esconder botão não é segurança.",
            "Rejeitar abre um campo de motivo obrigatório, salvo na observação.",
            "Registre quem aprovou e quando.",
            "Escreva o teste: técnico chamando a URL de aprovar recebe 403.",
        ],
        aceite=[
            "Técnico chamando POST /aprovar direto recebe 403",
            "Rejeição sem motivo é recusada",
            "Fica registrado quem aprovou/rejeitou e quando",
            "Teste automatizado do 403",
        ],
        arquivos=["app/blueprints/manutencao/"],
    ),
    Tarefa(
        titulo="[S3] Converter pedido aprovado em Ordem de Serviço (regra 1:1)",
        milestone=M3,
        labels=[RONALDO, AVANCADO, "tipo: backend"],
        estimativa="4h",
        objetivo=(
            "Serviço que transforma um pedido APROVADO em uma OS, respeitando a cardinalidade "
            "1:1 — um pedido gera no máximo uma ordem de serviço, mesmo com dois cliques "
            "simultâneos."
        ),
        porque=(
            "É o coração do sistema e o ponto mais sujeito a bug de concorrência. A constraint "
            "`unique` no banco é a rede de proteção; a regra na aplicação é a primeira linha."
        ),
        passos=[
            "Criar `app/servicos/manutencao.py` com `converter_pedido_em_os(id_pedido, responsavel)`.",
            "Validar: pedido existe, status é APROVADO, e ainda não tem OS.",
            "Criar a OS com status ABERTA e mudar o pedido para CONVERTIDO na mesma transação.",
            "Tratar `IntegrityError` da constraint unique devolvendo mensagem de negócio, não erro 500.",
            "Testar: chamar duas vezes cria só uma OS.",
        ],
        aceite=[
            "Pedido não aprovado não gera OS",
            "Duas chamadas seguidas geram uma única OS",
            "Pedido vira CONVERTIDO junto com a criação da OS (mesma transação)",
            "Testes cobrindo os três casos",
        ],
        arquivos=["app/servicos/manutencao.py", "tests/test_manutencao.py"],
    ),
    Tarefa(
        titulo="[S3] Ordem de Serviço: lançar peças utilizadas e baixar do estoque",
        milestone=M3,
        labels=[EQUIPE, AVANCADO, "tipo: backend"],
        estimativa="6h em dupla, com revisão do líder técnico",
        objetivo=(
            "Na tela da OS, adicionar as peças usadas no conserto. Cada peça lançada dá baixa no "
            "estoque e registra a movimentação. Remover a peça devolve ao estoque."
        ),
        porque=(
            "É onde manutenção e estoque se encontram — o ponto que faz o sistema ser um "
            "ecossistema e não duas telas soltas. Também é onde mora o maior risco de bug do "
            "projeto, por isso é revisada pelo líder técnico antes de entrar."
        ),
        passos=[
            "Use o serviço de estoque já pronto: `registrar_saida(...)` com `documento_origem = f'OS-{id_os}'`.",
            "Grave `valor_unitario` copiado da peça **no momento do lançamento** — se o preço mudar depois, o custo histórico da OS não pode mudar junto.",
            "Bloqueie lançar peça sem saldo; sugira o status AGUARDANDO_PECA para a OS.",
            "Ao remover um item da OS, estorne a movimentação (nova movimentação de entrada, nunca apague a antiga).",
            "Mostre o custo total da OS atualizado a cada lançamento (a propriedade `custo_total` já existe no modelo).",
        ],
        aceite=[
            "Lançar peça baixa o estoque na quantidade certa",
            "Remover item devolve ao estoque por estorno (histórico preservado)",
            "Peça sem saldo é bloqueada com mensagem clara",
            "Custo total da OS bate com a soma dos itens + serviços",
            "Teste automatizado do ciclo lançar → remover → saldo volta ao original",
        ],
        arquivos=["app/blueprints/manutencao/", "app/servicos/estoque.py"],
    ),
    Tarefa(
        titulo="[S3] Ordem de Serviço: apontamento de horas do técnico",
        milestone=M3,
        labels=[EQUIPE, INICIANTE, "tipo: backend"],
        estimativa="3h",
        objetivo=(
            "Na tela da OS, o técnico registra data, nome e horas trabalhadas. A tela mostra o "
            "total de horas da OS."
        ),
        porque=(
            "É o dado que alimenta o indicador de 'tempo médio de atendimento' do painel. Tarefa "
            "simples e de efeito visível — ótima segunda contribuição."
        ),
        passos=[
            "Formulário pequeno na própria tela da OS (data, técnico, horas, observação).",
            "Preencha técnico e data automaticamente com o usuário logado e a data de hoje, deixando editável.",
            "Aceite horas com casa decimal (1,5 hora) usando `DecimalField(places=2)`.",
            "Recuse horas ≤ 0 ou > 24.",
            "Mostre a soma das horas no topo da OS (a propriedade `horas_totais` já existe).",
        ],
        aceite=[
            "Apontamentos listados em ordem de data",
            "Total de horas correto na tela",
            "Horas inválidas recusadas com mensagem",
        ],
        arquivos=["app/blueprints/manutencao/"],
    ),
    Tarefa(
        titulo="[S3] Ordem de Serviço: serviços executados e prestador responsável",
        milestone=M3,
        labels=[EQUIPE, INICIANTE, "tipo: backend"],
        estimativa="3h",
        objetivo=(
            "Lançar os serviços feitos na OS (descrição e valor), podendo vincular a um prestador "
            "externo cadastrado."
        ),
        porque="Completa o custo da OS: peças + mão de obra externa = custo real da manutenção.",
        passos=[
            "Formulário com descrição, valor e lista suspensa de prestadores (opcional — pode ser serviço interno).",
            "Some os serviços no custo total da OS.",
            "Na listagem de prestadores, mostre quantas OS cada um atendeu.",
        ],
        aceite=[
            "Serviço com ou sem prestador funciona",
            "Custo total da OS soma peças + serviços",
        ],
        arquivos=["app/blueprints/manutencao/"],
    ),
    Tarefa(
        titulo="[S3] Encerrar Ordem de Serviço com as validações do fluxo",
        milestone=M3,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: backend"],
        estimativa="3h",
        objetivo=(
            "Botão de concluir OS que grava a data de fechamento, muda o status para CONCLUIDA e "
            "impede alterações depois disso."
        ),
        porque=(
            "Sem trava, alguém edita uma OS de setembro em novembro e todo relatório histórico "
            "muda. Dado fechado é dado confiável."
        ),
        passos=[
            "Exija pelo menos um apontamento de horas OU um serviço antes de concluir.",
            "Grave `data_fechamento` com a data e hora do momento.",
            "Bloqueie adicionar peças, serviços e apontamentos em OS concluída (no servidor).",
            "Mostre um selo visual 'CONCLUÍDA' na tela.",
            "Permita reabrir apenas para perfil ADMINISTRADOR, registrando o motivo.",
        ],
        aceite=[
            "OS vazia não pode ser concluída",
            "OS concluída recusa alterações mesmo chamando a URL direto",
            "Só administrador reabre, com motivo registrado",
        ],
        arquivos=["app/blueprints/manutencao/"],
    ),
]
