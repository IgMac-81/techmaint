"""Dados de exemplo para desenvolver e demonstrar o sistema.

Rode com:  flask seed
Isso cria perfis, um usuário admin, departamentos, grupos, equipamentos e peças.
Login de teste: admin / admin123  (troque antes de qualquer demonstração pública)
"""

from decimal import Decimal

from app.extensions import db
from app.models.catalogo import Departamento, Equipamento, Grupo, Peca, SubGrupo
from app.models.estoque import EstoquePeca
from app.models.usuario import Perfil, Permissao, Usuario

PERFIS = [
    ("ADMINISTRADOR", "Acesso total ao sistema"),
    ("GESTOR", "Aprova pedidos e consulta relatórios"),
    ("TECNICO", "Executa ordens de serviço"),
    ("CLIENTE", "Solicita manutenção e acompanha status"),
]

PERMISSOES = [
    ("USUARIO_GERENCIAR", "Criar, editar e desativar usuários"),
    ("PEDIDO_CRIAR", "Abrir pedido de manutenção"),
    ("PEDIDO_APROVAR", "Aprovar ou rejeitar pedidos"),
    ("OS_EXECUTAR", "Executar e encerrar ordens de serviço"),
    ("ESTOQUE_MOVIMENTAR", "Registrar entrada e saída de peças"),
    ("RELATORIO_VER", "Consultar relatórios e dashboards"),
]

MAPA_PERFIL_PERMISSOES = {
    "ADMINISTRADOR": [p[0] for p in PERMISSOES],
    "GESTOR": ["PEDIDO_APROVAR", "RELATORIO_VER", "PEDIDO_CRIAR"],
    "TECNICO": ["OS_EXECUTAR", "ESTOQUE_MOVIMENTAR", "PEDIDO_CRIAR"],
    "CLIENTE": ["PEDIDO_CRIAR"],
}


def carregar_dados_exemplo() -> None:
    db.create_all()

    permissoes = {}
    for nome, descricao in PERMISSOES:
        perm = db.session.scalar(db.select(Permissao).filter_by(nome_permissao=nome))
        if not perm:
            perm = Permissao(nome_permissao=nome, descricao=descricao)
            db.session.add(perm)
        permissoes[nome] = perm

    perfis = {}
    for nome, descricao in PERFIS:
        perfil = db.session.scalar(db.select(Perfil).filter_by(nome_perfil=nome))
        if not perfil:
            perfil = Perfil(nome_perfil=nome, descricao=descricao)
            db.session.add(perfil)
        perfil.permissoes = [permissoes[p] for p in MAPA_PERFIL_PERMISSOES[nome]]
        perfis[nome] = perfil

    if not db.session.scalar(db.select(Usuario).filter_by(login="admin")):
        admin = Usuario(nome="Administrador", login="admin", email="admin@techmaint.local")
        admin.definir_senha("admin123")
        admin.perfis = [perfis["ADMINISTRADOR"]]
        db.session.add(admin)

    if not db.session.scalar(db.select(Departamento)):
        db.session.add_all(
            [
                Departamento(nome_departamento="Produção", responsavel="Igor Machado"),
                Departamento(nome_departamento="Predial", responsavel="Ana Clara"),
                Departamento(nome_departamento="TI", responsavel="Ronaldo Bueno"),
            ]
        )

    if not db.session.scalar(db.select(Grupo)):
        mecanica = Grupo(grupo="Mecânica")
        eletrica = Grupo(grupo="Elétrica")
        db.session.add_all([mecanica, eletrica])
        db.session.flush()

        compressores = SubGrupo(subgrupo="Compressores", id_grupo=mecanica.id_grupo)
        quadros = SubGrupo(subgrupo="Quadros elétricos", id_grupo=eletrica.id_grupo)
        db.session.add_all([compressores, quadros])
        db.session.flush()

        eq1 = Equipamento(
            codigo="CMP-001",
            descricao="Compressor de ar 10HP",
            id_grupo=mecanica.id_grupo,
            id_subgrupo=compressores.id_subgrupo,
            patrimoniado=True,
            vida_util_meses=120,
        )
        eq2 = Equipamento(
            codigo="QDE-001",
            descricao="Quadro de distribuição principal",
            id_grupo=eletrica.id_grupo,
            id_subgrupo=quadros.id_subgrupo,
            patrimoniado=True,
            vida_util_meses=180,
        )
        db.session.add_all([eq1, eq2])
        db.session.flush()

        peca1 = Peca(
            id_equipamento=eq1.id_equipamento,
            nome="Filtro de ar",
            valor_unitario=Decimal("89.90"),
            qtde_estoque=Decimal("4"),
        )
        peca2 = Peca(
            id_equipamento=eq2.id_equipamento,
            nome="Disjuntor 63A",
            valor_unitario=Decimal("142.00"),
            qtde_estoque=Decimal("12"),
        )
        db.session.add_all([peca1, peca2])
        db.session.flush()

        db.session.add_all(
            [
                EstoquePeca(
                    id_peca=peca1.id_peca,
                    qtde_atual=Decimal("4"),
                    estoque_minimo=Decimal("5"),
                    local="Almoxarifado A",
                ),
                EstoquePeca(
                    id_peca=peca2.id_peca,
                    qtde_atual=Decimal("12"),
                    estoque_minimo=Decimal("3"),
                    local="Almoxarifado A",
                ),
            ]
        )

    db.session.commit()
