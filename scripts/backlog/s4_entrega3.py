"""Sprint 4 — 13/10 a 26/10/2026. Entrega 3: ponta a ponta, relatórios, PWA e plano da apresentação."""

from scripts.backlog.modelo import (
    AVANCADO,
    DESAFIO,
    EQUIPE,
    INICIANTE,
    INTERMEDIARIO,
    M4,
    RONALDO,
    Tarefa,
)

TAREFAS = [
    Tarefa(
        titulo="[S4] Indicadores reais do painel: tempo médio de atendimento e custo por máquina",
        milestone=M4,
        labels=[RONALDO, AVANCADO, "tipo: relatório"],
        estimativa="4h",
        objetivo=(
            "Consultas agregadas entregando os 4 indicadores da documentação: tempo médio de "
            "atendimento, custo por máquina, peças mais usadas e status das ordens."
        ),
        porque=(
            "São exatamente os indicadores que a documentação prometeu. É o slide que fecha a "
            "apresentação."
        ),
        passos=[
            "Tempo médio = média de (data_fechamento − data_abertura) das OS concluídas no período.",
            "Custo por máquina = soma dos itens e serviços das OS agrupada por equipamento.",
            "Peças mais usadas = top 10 por quantidade somada em `ItensOS`.",
            "Escrever as consultas com SQLAlchemy (`func.avg`, `func.sum`, `group_by`) e não puxando tudo para o Python.",
            "Colocar tudo em `app/servicos/indicadores.py` para as telas e os relatórios usarem a mesma fonte.",
        ],
        aceite=[
            "Os 4 indicadores calculados no banco, não em laço Python",
            "Filtro por período funcionando",
            "Conferência manual: os números batem com uma conta feita na mão em cima do seed",
        ],
        arquivos=["app/servicos/indicadores.py"],
    ),
    Tarefa(
        titulo="[S4] Gráficos do painel gerados com Matplotlib (sem biblioteca de JavaScript)",
        milestone=M4,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: relatório", DESAFIO],
        estimativa="5h",
        objetivo=(
            "Dois gráficos no painel — OS por status (barras) e custo por máquina (barras "
            "horizontais) — desenhados no servidor com Matplotlib e devolvidos como imagem PNG."
        ),
        porque=(
            "O projeto é 100% Python: o gráfico é gerado em Python, não em JavaScript. E "
            "funciona offline no PWA, porque é só uma imagem."
        ),
        passos=[
            "Instale e importe o Matplotlib com o backend `Agg` (sem interface gráfica): `matplotlib.use('Agg')` **antes** de importar o pyplot — se esquecer, o servidor trava.",
            "Crie uma rota `/graficos/os-por-status.png` que gera a figura e devolve com `mimetype='image/png'`.",
            "Escreva a imagem num buffer de memória (`io.BytesIO`), nunca num arquivo no disco.",
            "Use as cores do sistema (as variáveis do Figma) para o gráfico combinar com a tela.",
            "Sempre feche a figura com `plt.close(fig)` — se não fechar, o servidor vai comendo memória até cair.",
        ],
        exemplo=(
            "```python\n"
            "import io\n"
            "import matplotlib\n"
            "matplotlib.use('Agg')          # ANTES do pyplot, sempre\n"
            "import matplotlib.pyplot as plt\n"
            "from flask import send_file\n"
            "\n"
            "@bp.route('/graficos/os-por-status.png')\n"
            "@login_required\n"
            "def grafico_os_por_status():\n"
            "    dados = contar_os_por_status()          # {'ABERTA': 3, 'CONCLUIDA': 7}\n"
            "    fig, ax = plt.subplots(figsize=(5, 3), dpi=120)\n"
            "    ax.bar(list(dados.keys()), list(dados.values()), color='#0F766E')\n"
            "    ax.set_title('Ordens de serviço por status')\n"
            "    fig.tight_layout()\n"
            "\n"
            "    buffer = io.BytesIO()\n"
            "    fig.savefig(buffer, format='png')\n"
            "    plt.close(fig)                          # NÃO esqueça\n"
            "    buffer.seek(0)\n"
            "    return send_file(buffer, mimetype='image/png')\n"
            "```\n"
            "No template: `<img src=\"{{ url_for('dashboard.grafico_os_por_status') }}\" alt=\"Ordens por status\">`"
        ),
        aceite=[
            "Os dois gráficos aparecem no painel",
            "Figura fechada após gerar (sem vazamento de memória)",
            "Imagem legível no celular (não pode ficar minúscula)",
            "`alt` descritivo em cada imagem",
        ],
        arquivos=["app/blueprints/dashboard/routes.py", "requirements.txt"],
        extra="Adicione um filtro de período (últimos 30/90 dias) que muda os dois gráficos.",
    ),
    Tarefa(
        titulo="[S4] Relatório de ordens de serviço com filtros",
        milestone=M4,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: relatório"],
        estimativa="4h",
        objetivo=(
            "Tela de relatório com filtros de período, máquina, status e departamento, mostrando "
            "a lista e os totalizadores (quantidade, custo total, horas totais)."
        ),
        porque=(
            "'Emissão de relatórios com filtros' é requisito funcional. É também a tela base das "
            "duas exportações (Excel e PDF)."
        ),
        passos=[
            "Monte os filtros via GET para a URL poder ser salva e compartilhada.",
            "Valide que a data inicial não é maior que a final.",
            "Mostre os totalizadores no topo, sempre respeitando os filtros aplicados.",
            "Mostre o resumo do filtro em texto ('OS de 01/10 a 26/10, máquina CMP-001') — vai direto para o cabeçalho do PDF depois.",
            "Se não houver resultado, explique: 'Nenhuma OS encontrada com estes filtros'.",
        ],
        aceite=[
            "Filtros combinam entre si e sobrevivem ao recarregar a página",
            "Totalizadores respeitam os filtros",
            "Data inicial maior que a final é recusada",
        ],
        arquivos=["app/blueprints/relatorios/"],
    ),
    Tarefa(
        titulo="[S4] Exportar o relatório para Excel com openpyxl",
        milestone=M4,
        labels=[EQUIPE, INICIANTE, "tipo: relatório", DESAFIO],
        estimativa="4h",
        objetivo=(
            "Botão 'Exportar Excel' que baixa um .xlsx com os dados filtrados, cabeçalho em "
            "negrito, colunas com largura ajustada e uma linha de totais."
        ),
        porque=(
            "Gestor vive no Excel. Esse botão é o que faz o sistema parecer profissional na "
            "apresentação — e é uma tarefa bem contida, ótima para quem está começando."
        ),
        passos=[
            "Reaproveite a MESMA consulta do relatório na tela (importe a função, não duplique).",
            "Monte a planilha com `openpyxl` (ou `pandas.DataFrame.to_excel`).",
            "Deixe o cabeçalho em negrito, congele a primeira linha (`freeze_panes='A2'`) e ajuste a largura das colunas.",
            "Formate datas como DD/MM/AAAA e valores como moeda.",
            "Devolva com `send_file(..., as_attachment=True, download_name='relatorio-os.xlsx')`.",
            "Teste abrindo no Excel/LibreOffice de verdade — não confie só no download.",
        ],
        exemplo=(
            "```python\n"
            "import io\n"
            "from openpyxl import Workbook\n"
            "from openpyxl.styles import Font\n"
            "from flask import send_file\n"
            "\n"
            "wb = Workbook()\n"
            "ws = wb.active\n"
            "ws.title = 'Ordens de Serviço'\n"
            "ws.append(['OS', 'Máquina', 'Abertura', 'Status', 'Custo'])\n"
            "for celula in ws[1]:\n"
            "    celula.font = Font(bold=True)\n"
            "ws.freeze_panes = 'A2'\n"
            "\n"
            "for os_ in ordens:\n"
            "    ws.append([os_.id_os, os_.pedido.equipamento.codigo,\n"
            "               os_.data_abertura.strftime('%d/%m/%Y'), os_.status, float(os_.custo_total)])\n"
            "\n"
            "buffer = io.BytesIO()\n"
            "wb.save(buffer)\n"
            "buffer.seek(0)\n"
            "return send_file(buffer, as_attachment=True, download_name='relatorio-os.xlsx',\n"
            "                 mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')\n"
            "```"
        ),
        aceite=[
            "Arquivo abre no Excel sem aviso de corrompido",
            "Cabeçalho em negrito e primeira linha congelada",
            "Datas em DD/MM/AAAA e valores como número (não texto)",
            "Os dados do arquivo batem com os filtros da tela",
        ],
        arquivos=["app/blueprints/relatorios/"],
        extra="Adicione uma segunda aba com o resumo por máquina.",
    ),
    Tarefa(
        titulo="[S4] Exportar a Ordem de Serviço em PDF com ReportLab",
        milestone=M4,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: relatório", DESAFIO],
        estimativa="5h",
        objetivo=(
            "Botão que gera o PDF de uma OS: cabeçalho com logo e número, dados da máquina e do "
            "solicitante, tabela de peças, tabela de serviços, total e linha de assinatura."
        ),
        porque=(
            "É o documento que o técnico leva impresso para o chão de fábrica. Gerar PDF em "
            "Python é uma habilidade que você leva para qualquer emprego."
        ),
        passos=[
            "Use `reportlab.platypus` (SimpleDocTemplate, Paragraph, Table) — é bem mais fácil que desenhar no canvas coordenada por coordenada.",
            "Monte o cabeçalho com o logo do Figma e o número da OS.",
            "Use `Table` com `TableStyle` para as peças e os serviços.",
            "Gere em memória (`io.BytesIO`) e devolva com `as_attachment=True`.",
            "Nome do arquivo: `OS-0001.pdf`, com zeros à esquerda.",
            "Teste com uma OS sem peças e com uma OS com 20 peças (quebra de página).",
        ],
        aceite=[
            "PDF abre corretamente no celular e no computador",
            "OS sem peças gera PDF sem quebrar",
            "OS com 20 peças quebra a página mantendo o cabeçalho da tabela",
            "Total do PDF bate com o total da tela",
        ],
        arquivos=["app/servicos/pdf.py", "app/blueprints/manutencao/"],
        estudar=[
            "ReportLab platypus (o guia do usuário, capítulo 5): https://docs.reportlab.com/reportlab/userguide/ch5_paragraph/",
        ],
    ),
    Tarefa(
        titulo="[S4] Transformar o site em PWA instalável no iPhone e no Android",
        milestone=M4,
        labels=[RONALDO, AVANCADO, "tipo: pwa"],
        estimativa="5h",
        objetivo=(
            "Manifest completo, service worker servido na raiz com estratégia de cache por "
            "versão, página offline e o site passando na auditoria PWA do Lighthouse."
        ),
        porque=(
            "É o diferencial do nosso projeto: 'instala no celular como aplicativo'. Feito errado "
            "(service worker no /static, cache sem versão) ele serve versão velha e ninguém "
            "entende por que o sistema não atualiza."
        ),
        passos=[
            "Servir `sw.js` na raiz com o cabeçalho `Service-Worker-Allowed: /`.",
            "Cache: estáticos com cache-first, páginas com network-first e reserva offline.",
            "Versionar o nome do cache e limpar os antigos no evento `activate`.",
            "Manifest com `display: standalone`, ícones 192/512 e um maskable.",
            "Rodar o Lighthouse (F12 → Lighthouse → Progressive Web App) e corrigir tudo o que apontar.",
            "Documentar em `docs/05-pwa.md` o passo a passo de instalação no iPhone (Safari → Compartilhar → Adicionar à Tela de Início) e no Android (Chrome → Instalar aplicativo).",
        ],
        aceite=[
            "Instala no iPhone e no Android e abre sem a barra do navegador",
            "Com o avião ligado, uma página já visitada ainda abre",
            "Nova versão publicada aparece sem precisar desinstalar o app",
            "Lighthouse sem erro crítico de PWA (print na issue)",
        ],
        arquivos=["app/static/js/sw.js", "app/static/manifest.webmanifest", "docs/05-pwa.md"],
    ),
    Tarefa(
        titulo="[S4] Gerar os ícones e a tela de abertura do app a partir do logo",
        milestone=M4,
        labels=[EQUIPE, INICIANTE, "tipo: pwa", DESAFIO],
        estimativa="3h",
        objetivo=(
            "Ícones 192px, 512px e 512px maskable gerados com Pillow a partir do logo do TechMaint, "
            "mais o ícone de atalho do iOS."
        ),
        porque=(
            "O ícone é a cara do app na tela do celular do professor. E gerar imagem por código, "
            "em vez de no editor, é 100% Python e reprodutível."
        ),
        passos=[
            "Pegue o logo do TechMaint em alta resolução (está no cabeçalho dos documentos).",
            "Escreva `scripts/gerar_icones.py` usando Pillow para redimensionar e centralizar.",
            "Para o ícone **maskable**, deixe 20% de margem em volta — o Android corta as bordas em círculo e comeria o logo.",
            "Salve em `app/static/icons/` e confira se os nomes batem com o `manifest.webmanifest`.",
            "Instale o app no seu celular e tire uma foto da tela inicial para anexar na issue.",
        ],
        exemplo=(
            "```python\n"
            "from PIL import Image\n"
            "\n"
            "logo = Image.open('docs/marca/logo.png').convert('RGBA')\n"
            "for tamanho in (192, 512):\n"
            "    fundo = Image.new('RGBA', (tamanho, tamanho), '#0F766E')\n"
            "    margem = int(tamanho * 0.18)          # 0.28 para o maskable\n"
            "    logo_r = logo.resize((tamanho - margem * 2,) * 2, Image.LANCZOS)\n"
            "    fundo.paste(logo_r, (margem, margem), logo_r)\n"
            "    fundo.save(f'app/static/icons/icon-{tamanho}.png')\n"
            "```"
        ),
        aceite=[
            "Os 3 ícones gerados pelo script (não à mão)",
            "Ícone maskable não corta o logo quando o Android arredonda",
            "Foto da tela inicial do celular com o app instalado anexada na issue",
        ],
        arquivos=["scripts/gerar_icones.py", "app/static/icons/"],
    ),
    Tarefa(
        titulo="[S4] Passar o checklist de responsividade em todas as telas",
        milestone=M4,
        labels=[EQUIPE, INICIANTE, "tipo: frontend"],
        estimativa="4h em dupla",
        objetivo=(
            "Percorrer todas as telas do sistema em 3 tamanhos (390px, 768px, 1280px) e corrigir "
            "o que quebrar, registrando o antes e depois."
        ),
        porque=(
            "A demonstração vai ser no celular. Uma tabela que estoura a tela na hora da "
            "apresentação é o tipo de coisa que a turma inteira percebe."
        ),
        passos=[
            "Abra o F12 → modo dispositivo e passe em cada tela nos 3 tamanhos.",
            "Procure: rolagem horizontal (proibida), texto menor que 14px, botão menor que 44px, tabela estourando, campo colado na borda.",
            "Toda tabela larga vai dentro de `<div class=\"tabela-rolagem\">`.",
            "Formulários viram uma coluna só abaixo de 768px.",
            "Monte a tabela de antes/depois com prints na issue.",
        ],
        aceite=[
            "Nenhuma tela com rolagem horizontal em 390px",
            "Nenhum botão ou link com área de toque menor que 44x44px",
            "Prints de todas as telas nos 3 tamanhos anexados",
        ],
        arquivos=["app/templates/", "app/static/css/app.css"],
    ),
    Tarefa(
        titulo="[S4] Testes automatizados dos fluxos principais de ponta a ponta",
        milestone=M4,
        labels=[EQUIPE, INTERMEDIARIO, "tipo: teste"],
        estimativa="5h",
        objetivo=(
            "Um teste que percorre o fluxo completo: login → abrir pedido → aprovar → virar OS → "
            "lançar peça → apontar horas → concluir → conferir estoque e indicadores."
        ),
        porque=(
            "É a prova automatizada de que o sistema funciona 'de ponta a ponta', que é "
            "literalmente o que a Entrega 3 pede. E te dá segurança para mexer no código depois."
        ),
        passos=[
            "Escreva o teste como uma história, com comentários em cada etapa.",
            "Confira o estado do banco depois de cada passo, não só o código HTTP.",
            "Inclua pelo menos um caminho ruim (tentar concluir OS vazia).",
            "Garanta que o teste roda isolado (banco em memória, sem depender de ordem).",
        ],
        aceite=[
            "Teste de ponta a ponta passando no CI",
            "Estoque conferido no final do fluxo",
            "Pelo menos um teste de caminho ruim",
        ],
        arquivos=["tests/test_fluxo_completo.py"],
    ),
    Tarefa(
        titulo="[S4] Publicar uma versão de demonstração com HTTPS para instalar no celular",
        milestone=M4,
        labels=[RONALDO, AVANCADO, "tipo: setup"],
        estimativa="4h",
        objetivo=(
            "O sistema no ar em uma URL pública com HTTPS, rodando com gunicorn, para o grupo e o "
            "professor instalarem o PWA no próprio celular."
        ),
        porque=(
            "Service worker **só funciona em HTTPS** (ou localhost). Sem deploy, não dá para "
            "demonstrar a instalação — que é o nosso diferencial. E depender do Wi-Fi da "
            "faculdade no dia da apresentação é risco desnecessário."
        ),
        passos=[
            "Escolher a hospedagem e configurar as variáveis de ambiente (SECRET_KEY forte, nunca a do exemplo).",
            "Rodar com gunicorn atrás de HTTPS.",
            "Rodar as migrações e o seed de demonstração na primeira publicação.",
            "Testar a instalação do PWA em um iPhone e em um Android reais.",
            "Documentar o processo em `docs/07-deploy.md` para qualquer um do grupo conseguir republicar.",
        ],
        aceite=[
            "URL pública com HTTPS funcionando",
            "PWA instalável a partir dela em iPhone e Android",
            "SECRET_KEY de produção diferente da do repositório",
            "Passo a passo de publicação documentado",
        ],
        arquivos=["docs/07-deploy.md"],
    ),
    Tarefa(
        titulo="[S4] Escrever o manual do usuário com prints",
        milestone=M4,
        labels=[EQUIPE, INICIANTE, "tipo: doc"],
        estimativa="4h em dupla",
        objetivo=(
            "Manual em PDF ensinando, com print em cada passo, como: entrar, abrir um pedido, "
            "aprovar, executar a OS, consultar estoque, emitir relatório e instalar o app no "
            "celular."
        ),
        porque=(
            "A documentação anexa prevê o 'Manual do Usuário / Guia de Operação' como entregável. "
            "E escrever o manual revela as telas confusas — várias melhorias de usabilidade vão "
            "sair daqui."
        ),
        passos=[
            "Organize por PERFIL (o que o técnico faz, o que o gestor faz), não por tela.",
            "Um print por passo, com a área importante destacada.",
            "Escreva no imperativo e sem jargão: 'Toque em Novo pedido', não 'o usuário deverá acionar a rotina de inclusão'.",
            "Inclua a seção 'Instalar no celular' com prints do iPhone e do Android.",
            "Anote numa lista as telas que você achou confusas enquanto escrevia — vira issue de melhoria.",
        ],
        aceite=[
            "Todos os fluxos principais cobertos com print",
            "Seção de instalação no celular com as duas plataformas",
            "Lista de melhorias de usabilidade sugeridas ao final",
        ],
        arquivos=["docs/06-manual-do-usuario.md"],
    ),
    Tarefa(
        titulo="[S4] Montar o plano da apresentação: roteiro de 15 minutos com todos falando",
        milestone=M4,
        labels=[EQUIPE, INICIANTE, "tipo: apresentação"],
        estimativa="3h com o grupo todo",
        objetivo=(
            "Roteiro minuto a minuto dos 15 minutos, com o nome de quem fala em cada bloco (os 8 "
            "integrantes precisam falar), o que aparece na tela e quem opera o computador."
        ),
        porque=(
            "A regra é explícita: 15 minutos, todos os integrantes falando. Sem roteiro, duas "
            "pessoas falam 6 minutos cada e três ficam mudas."
        ),
        passos=[
            "Divida assim: 2 min problema e contexto (Ana Clara), 2 min escopo e processo (Igor), 3 min arquitetura e banco (Ronaldo), 5 min demonstração ao vivo (os 4 desenvolvedores, um módulo cada), 2 min dados e relatórios (Rafael), 1 min resultados e aprendizados (todos, uma frase cada).",
            "Para a demonstração, defina o roteiro exato de cliques — nada de improviso.",
            "Defina o **plano B**: vídeo gravado da demonstração, caso a internet falhe.",
            "Cronometre cada bloco e ajuste até caber em 15 minutos com folga de 1 minuto.",
            "Liste as 5 perguntas mais prováveis do professor e quem responde cada uma.",
        ],
        aceite=[
            "Roteiro com nome e tempo de cada pessoa, somando no máximo 15 minutos",
            "Roteiro de cliques da demonstração escrito",
            "Vídeo de plano B gravado e guardado no Drive",
            "Perguntas prováveis mapeadas com o responsável pela resposta",
        ],
        arquivos=["docs/08-apresentacao.md"],
    ),
]
