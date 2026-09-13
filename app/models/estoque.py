"""Estoque de peças e de equipamentos, e suas movimentações."""

from datetime import datetime

from app.extensions import db


class EstoquePeca(db.Model):
    __tablename__ = "estoque_pecas"

    id_estoque_peca = db.Column(db.Integer, primary_key=True)
    id_peca = db.Column(db.Integer, db.ForeignKey("pecas.id_peca"), nullable=False)
    qtde_atual = db.Column(db.Numeric(18, 3), nullable=False, default=0)
    localizacao = db.Column(db.String(100))
    estoque_minimo = db.Column(db.Numeric(18, 3), default=0)
    estoque_maximo = db.Column(db.Numeric(18, 3))
    ultima_atualizacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    local = db.Column(db.String(50))

    peca = db.relationship("Peca", back_populates="estoques")

    @property
    def abaixo_do_minimo(self) -> bool:
        """Usado pelo dashboard para o alerta de estoque baixo."""
        if self.estoque_minimo is None:
            return False
        return self.qtde_atual <= self.estoque_minimo


class MovimentacaoEstoquePeca(db.Model):
    __tablename__ = "movimentacao_estoque_pecas"

    id_movimento = db.Column(db.Integer, primary_key=True)
    id_peca = db.Column(db.Integer, db.ForeignKey("pecas.id_peca"), nullable=False)
    tipo_movimento = db.Column(db.String(20), nullable=False)  # ENTRADA / SAIDA
    quantidade = db.Column(db.Numeric(18, 3), nullable=False)
    valor_unitario = db.Column(db.Numeric(18, 2))
    data_movimento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    documento_origem = db.Column(db.String(50))
    observacao = db.Column(db.String(500))

    peca = db.relationship("Peca")


class EstoqueEquipamento(db.Model):
    __tablename__ = "estoque_equipamentos"

    id_estoque_equip = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(
        db.Integer, db.ForeignKey("equipamentos.id_equipamento"), nullable=False
    )
    id_departamento = db.Column(
        db.Integer, db.ForeignKey("departamentos.id_departamento"), nullable=False
    )
    qtde_atual = db.Column(db.Numeric(18, 3), nullable=False, default=0)
    localizacao = db.Column(db.String(100))
    status = db.Column(db.String(20))  # ATIVO / EM_MANUTENCAO / BAIXADO
    ultima_atualizacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    equipamento = db.relationship("Equipamento")
    departamento = db.relationship("Departamento")


class MovimentacaoEquipamento(db.Model):
    __tablename__ = "movimentacao_equipamentos"

    id_movimento_eq = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(
        db.Integer, db.ForeignKey("equipamentos.id_equipamento"), nullable=False
    )
    id_departamento = db.Column(
        db.Integer, db.ForeignKey("departamentos.id_departamento"), nullable=False
    )
    tipo_movimento = db.Column(db.String(20), nullable=False)
    data_movimento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    responsavel = db.Column(db.String(100))
    observacao = db.Column(db.String(500))
