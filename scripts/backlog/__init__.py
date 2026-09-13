"""Backlog do TechMaint como dados Python.

Cada tarefa vira uma issue no GitHub e um item no Project.
Rode `python scripts/criar_issues.py --dry-run` para ver o que seria criado.
"""

from scripts.backlog.s1_delimitacao import TAREFAS as S1
from scripts.backlog.s2_arquitetura import TAREFAS as S2
from scripts.backlog.s3_nucleo import TAREFAS as S3
from scripts.backlog.s4_entrega3 import TAREFAS as S4
from scripts.backlog.s5_apresentacao import TAREFAS as S5

TAREFAS = S1 + S2 + S3 + S4 + S5

MILESTONES = [
    {
        "titulo": "Entrega 1 — Grupo, papéis e delimitação",
        "vence_em": "2026-09-14",
        "descricao": "Definição do grupo, papéis e delimitação do sistema.",
    },
    {
        "titulo": "Entrega 2 — Arquitetura e protótipo que roda",
        "vence_em": "2026-09-28",
        "descricao": "Arquitetura documentada, banco modelado, login funcionando e primeiros cadastros na tela.",
    },
    {
        "titulo": "Sprint 3 — Módulos do núcleo",
        "vence_em": "2026-10-12",
        "descricao": "Cadastros completos, estoque e o fluxo pedido → ordem de serviço.",
    },
    {
        "titulo": "Entrega 3 — Versão funcional ponta a ponta",
        "vence_em": "2026-10-26",
        "descricao": "Relatórios, dashboard com indicadores, PWA instalável e plano da apresentação.",
    },
    {
        "titulo": "Apresentação final",
        "vence_em": "2026-11-09",
        "descricao": "Ensaio, code freeze e apresentação de 15 minutos com todos falando.",
    },
]

LABELS = [
    ("dono: ronaldo", "B60205", "Tarefa crítica/arquitetural — Ronaldo (líder técnico)"),
    ("dono: equipe", "0E8A16", "Aberta para qualquer integrante pegar"),
    ("nível: iniciante", "C2E0C6", "Primeiro semestre consegue fazer seguindo o passo a passo"),
    ("nível: intermediário", "FBCA04", "Exige juntar duas ou três coisas já vistas"),
    ("nível: avançado", "D93F0B", "Regra de negócio delicada ou risco de quebrar o sistema"),
    ("desafio ⭐", "5319E7", "Tarefa divertida, com um extra opcional para quem quiser ir além"),
    ("tipo: setup", "BFDADC", "Ambiente, ferramentas e configuração"),
    ("tipo: banco", "1D76DB", "Modelagem e migrações"),
    ("tipo: backend", "0052CC", "Rotas, regras de negócio, Python"),
    ("tipo: frontend", "006B75", "Templates, CSS, responsividade"),
    ("tipo: pwa", "5319E7", "Manifest, service worker, instalação no celular"),
    ("tipo: relatório", "FEF2C0", "Exportações, gráficos e indicadores"),
    ("tipo: teste", "C5DEF5", "Testes automatizados e qualidade"),
    ("tipo: doc", "D4C5F9", "Documentação e entregas acadêmicas"),
    ("tipo: apresentação", "E99695", "Roteiro, slides e ensaio"),
    ("bloqueia outros", "000000", "Outras tarefas dependem desta — prioridade máxima"),
]

__all__ = ["TAREFAS", "MILESTONES", "LABELS"]
