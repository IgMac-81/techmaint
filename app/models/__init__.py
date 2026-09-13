"""Modelos do TechMaint.

Importar tudo aqui garante que o SQLAlchemy "enxergue" todas as tabelas
quando rodarmos as migrações.
"""

from app.models.catalogo import (  # noqa: F401
    Departamento,
    Equipamento,
    Grupo,
    Peca,
    SubGrupo,
)
from app.models.estoque import (  # noqa: F401
    EstoqueEquipamento,
    EstoquePeca,
    MovimentacaoEquipamento,
    MovimentacaoEstoquePeca,
)
from app.models.fornecedor import (  # noqa: F401
    Fornecedor,
    ItemNotaFiscal,
    NotaFiscal,
    PrestadorServico,
)
from app.models.manutencao import (  # noqa: F401
    ApontamentoOS,
    ItemOS,
    OrdemServico,
    PedidoManutencao,
    ServicoOS,
)
from app.models.usuario import Perfil, Permissao, Usuario  # noqa: F401

__all__ = [
    "Usuario",
    "Perfil",
    "Permissao",
    "Departamento",
    "Grupo",
    "SubGrupo",
    "Equipamento",
    "Peca",
    "Fornecedor",
    "PrestadorServico",
    "NotaFiscal",
    "ItemNotaFiscal",
    "EstoquePeca",
    "MovimentacaoEstoquePeca",
    "EstoqueEquipamento",
    "MovimentacaoEquipamento",
    "PedidoManutencao",
    "OrdemServico",
    "ItemOS",
    "ServicoOS",
    "ApontamentoOS",
]
