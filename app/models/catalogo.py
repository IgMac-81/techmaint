"""Departamentos, grupos, subgrupos, equipamentos e peças."""

from app.extensions import db


class Departamento(db.Model):
    __tablename__ = "departamentos"

    id_departamento = db.Column(db.Integer, primary_key=True)
    nome_departamento = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f"<Departamento {self.nome_departamento}>"


class Grupo(db.Model):
    __tablename__ = "grupos"

    id_grupo = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(100), nullable=False)

    subgrupos = db.relationship("SubGrupo", back_populates="grupo_rel")


class SubGrupo(db.Model):
    __tablename__ = "subgrupos"

    id_subgrupo = db.Column(db.Integer, primary_key=True)
    subgrupo = db.Column(db.String(200), nullable=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey("grupos.id_grupo"), nullable=False)

    grupo_rel = db.relationship("Grupo", back_populates="subgrupos")
    equipamentos = db.relationship("Equipamento", back_populates="subgrupo_rel")


class Equipamento(db.Model):
    __tablename__ = "equipamentos"

    id_equipamento = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False, unique=True, index=True)
    descricao = db.Column(db.String(200), nullable=False)
    ncm = db.Column(db.String(8))
    id_grupo = db.Column(db.Integer, db.ForeignKey("grupos.id_grupo"), nullable=False)
    id_subgrupo = db.Column(db.Integer, db.ForeignKey("subgrupos.id_subgrupo"), nullable=False)
    controla_depreciacao = db.Column(db.Boolean, default=False)
    patrimoniado = db.Column(db.Boolean, default=False)
    vida_util_meses = db.Column(db.SmallInteger)
    valor_residual_padrao = db.Column(db.Numeric(18, 2))

    subgrupo_rel = db.relationship("SubGrupo", back_populates="equipamentos")
    pecas = db.relationship("Peca", back_populates="equipamento")
    pedidos = db.relationship("PedidoManutencao", back_populates="equipamento")

    def __repr__(self) -> str:
        return f"<Equipamento {self.codigo}>"


class Peca(db.Model):
    __tablename__ = "pecas"

    id_peca = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(
        db.Integer, db.ForeignKey("equipamentos.id_equipamento"), nullable=False
    )
    nome = db.Column(db.String(200), nullable=False)
    ncm = db.Column(db.String(8))
    valor_unitario = db.Column(db.Numeric(18, 2), nullable=False, default=0)
    qtde_estoque = db.Column(db.Numeric(18, 3), nullable=False, default=0)

    equipamento = db.relationship("Equipamento", back_populates="pecas")
    estoques = db.relationship("EstoquePeca", back_populates="peca")

    def __repr__(self) -> str:
        return f"<Peca {self.nome}>"
