"""Sprint 5 — 27/10 a novembro/2026. Ensaio, congelamento e apresentação final."""

from scripts.backlog.modelo import (
    AVANCADO,
    EQUIPE,
    INICIANTE,
    M5,
    RONALDO,
    Tarefa,
)

TAREFAS = [
    Tarefa(
        titulo="[S5] Congelar o código (code freeze) e fechar a versão 1.0",
        milestone=M5,
        labels=[RONALDO, AVANCADO, "tipo: setup"],
        estimativa="2h",
        objetivo=(
            "Tag `v1.0` criada, a partir de uma main testada, e a regra combinada: da data do "
            "congelamento até a apresentação, só entra correção de bug crítico."
        ),
        porque=(
            "A funcionalidade nova de última hora é o que quebra a demonstração. Congelar é o que "
            "transforma um projeto que funciona em um projeto que funciona **no dia**."
        ),
        passos=[
            "Rodar a suíte de testes completa e o fluxo de ponta a ponta na mão.",
            "Publicar a versão final no ambiente de demonstração.",
            "Criar a tag `v1.0` e a release no GitHub com o resumo do que foi entregue.",
            "Fechar ou mover para 'Backlog futuro' toda issue que não vai entrar.",
            "Comunicar o congelamento ao grupo: da data X em diante, só bug crítico.",
        ],
        aceite=[
            "Tag v1.0 e release publicadas",
            "Ambiente de demonstração rodando a v1.0",
            "Quadro do projeto sem issues em aberto sem destino definido",
        ],
    ),
    Tarefa(
        titulo="[S5] Ensaio cronometrado da apresentação (mínimo 2 rodadas)",
        milestone=M5,
        labels=[EQUIPE, INICIANTE, "tipo: apresentação"],
        estimativa="2h por ensaio, com o grupo todo",
        objetivo=(
            "Dois ensaios completos, cronometrados, com todo mundo falando a própria parte e a "
            "demonstração rodando no ambiente publicado — do celular, como vai ser no dia."
        ),
        porque=(
            "Ninguém acerta o tempo na primeira tentativa. O primeiro ensaio sempre passa de 20 "
            "minutos; é ele que mostra o que cortar."
        ),
        passos=[
            "Ensaio 1: cronometre cada bloco e anote o tempo real de cada pessoa.",
            "Corte o que passou: prefira cortar explicação técnica a cortar demonstração.",
            "Ensaio 2: rode com o setup real (mesmo notebook, mesmo cabo, mesmo celular).",
            "Teste a demonstração com a internet do celular, não só no Wi-Fi.",
            "Confira o plano B: o vídeo abre e tem áudio?",
            "Anote na issue o tempo final de cada bloco.",
        ],
        aceite=[
            "Dois ensaios registrados com os tempos anotados",
            "Tempo total entre 13 e 15 minutos",
            "Os 8 integrantes falaram nos dois ensaios",
            "Plano B testado",
        ],
        arquivos=["docs/08-apresentacao.md"],
    ),
    Tarefa(
        titulo="[S5] Montar os slides da apresentação final",
        milestone=M5,
        labels=[EQUIPE, INICIANTE, "tipo: apresentação"],
        estimativa="4h em dupla",
        objetivo=(
            "Slides enxutos seguindo o roteiro: problema, escopo, arquitetura, banco, "
            "demonstração (só o título, a tela é o sistema), indicadores, aprendizados."
        ),
        porque=(
            "Slide cheio de texto faz a plateia ler em vez de ouvir. O sistema rodando é o "
            "protagonista; o slide é só a placa de rua."
        ),
        passos=[
            "Máximo de 6 linhas por slide. Sem parágrafo.",
            "Use as cores e a marca do Figma para o slide combinar com o sistema.",
            "Um slide de arquitetura com o diagrama, um de banco com o ER — ambos já prontos nos docs.",
            "Um slide de indicadores com o print dos gráficos reais do sistema.",
            "Slide final com os aprendizados: o que deu errado e o que o grupo faria diferente (o professor valora honestidade).",
        ],
        aceite=[
            "Máximo de 12 slides",
            "Nenhum slide com mais de 6 linhas de texto",
            "Prints reais do sistema, nenhum mockup",
            "Arquivo no Drive do grupo e uma cópia em PDF no repositório",
        ],
        arquivos=["docs/apresentacao/"],
    ),
    Tarefa(
        titulo="[S5] Checklist do dia da apresentação",
        milestone=M5,
        labels=[EQUIPE, INICIANTE, "tipo: apresentação"],
        estimativa="1h",
        objetivo=(
            "Lista de verificação impressa e conferida no dia: equipamentos, acessos, plano B e "
            "ordem de fala."
        ),
        porque="É o que impede o 'esqueci o adaptador HDMI' virar a lembrança da apresentação.",
        passos=[
            "Liste: notebook carregado, adaptador de vídeo, celular com o PWA já instalado, internet móvel como reserva.",
            "Confira os acessos: login de demonstração funcionando, ambiente publicado no ar, vídeo do plano B no celular E no notebook.",
            "Confirme a ordem de fala e onde cada pessoa fica em pé.",
            "Combine o horário de chegada com 30 minutos de folga.",
            "Rode o fluxo de demonstração uma última vez, 1 hora antes.",
        ],
        aceite=[
            "Checklist escrito e conferido pelo grupo no dia anterior",
            "Ambiente de demonstração testado na manhã da apresentação",
        ],
        arquivos=["docs/08-apresentacao.md"],
    ),
    Tarefa(
        titulo="[S5] Retrospectiva final do projeto",
        milestone=M5,
        labels=[EQUIPE, INICIANTE, "tipo: doc"],
        estimativa="1h30 com o grupo todo",
        objetivo=(
            "Documento curto e honesto com: o que funcionou, o que não funcionou, o que cada "
            "pessoa aprendeu e o que o grupo faria diferente."
        ),
        porque=(
            "O Scrum prevê retrospectiva ao fim de cada sprint, e a documentação do projeto "
            "assumiu esse compromisso. Além disso, é a parte que vira resposta de entrevista de "
            "estágio: 'me conta de um projeto em equipe'."
        ),
        passos=[
            "Cada pessoa escreve, antes da reunião: 1 coisa que funcionou, 1 que não, 1 que aprendeu.",
            "Na reunião, leiam tudo sem interromper e agrupem os temas parecidos.",
            "Escolham as 3 mudanças mais importantes que fariam se começassem de novo.",
            "Foque em processo, não em pessoa: 'as revisões demoravam 3 dias', não 'fulano demora'.",
        ],
        aceite=[
            "Contribuição escrita dos 8 integrantes",
            "3 mudanças priorizadas",
            "Documento no repositório",
        ],
        arquivos=["docs/09-retrospectiva.md"],
    ),
]
