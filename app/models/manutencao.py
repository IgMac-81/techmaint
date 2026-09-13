"""Pedidos de manutenção, ordens de serviço e seus filhos.

Fluxo do negócio:
    PedidoManutencao (alguém pede)  ->  OrdemServico (o técnico executa)
    A OS tem: itens (peças usadas), serviços (o que foi feito) e
    apontamentos (horas trabalhadas).
"""

from datetime import datetime

from app.extensions import db

STATUS_PEDIDO = ("ABERTO", "APROVADO", "REJEITADO", "CONVERTIDO")
STATUS_OS = ("ABERTA", "EM_EXECUCAO", "AGUARDANDO_PECA", "CONCLUIDA", "CANCELADA")
PRIORIDADES = ("BAIXA", "MEDIA", "ALTA", "CRITICA")


class PedidoManutencao(db.Model):
    __tablename__ = "pedidos_manutencao"

    id_pedido = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(
        db.Integer, db.ForeignKey("equipamentos.id_equipamento"), nullable=False
    )
    id_departamento = db.Column(
        db.Integer, db.ForeignKey("departamentos.id_departamento"), nullable=False
    )
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    solicitante = db.Column(db.String(100), nullable=False)
    descricao_problema = db.Column(db.String(500))
    prioridade = db.Column(db.String(20), default="MEDIA")
    status = db.Column(db.String(20), nullable=False, default="ABERTO")

    equipamento = db.relationship("Equipamento", back_populates="pedidos")
    departamento = db.relationship("Departamento")
    ordem_servico = db.relationship("OrdemServico", back_populates="pedido", uselist=False)

    def __repr__(self) -> str:
        return f"<Pedido {self.id_pedido} {self.status}>"


class OrdemServico(db.Model):
    __tablename__ = "ordens_servico"

    id_os = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(
        db.Integer, db.ForeignKey("pedidos_manutencao.id_pedido"), nullable=False, unique=True
    )
    data_abertura = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime)
    responsavel = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default="ABERTA")
    observacao = db.Column(db.String(500))

    pedido = db.relationship("PedidoManutencao", back_populates="ordem_servico")
    itens = db.relationship("ItemOS", back_populates="os", cascade="all, delete-orphan")
    servicos = db.relationship("ServicoOS", back_populates="os", cascade="all, delete-orphan")
    apontamentos = db.relationship(
        "ApontamentoOS", back_populates="os", cascade="all, delete-orphan"
    )

    @property
    def custo_total(self):
        pecas = sum((i.valor_total or 0) for i in self.itens)
        servicos = sum((s.valor_servico or 0) for s in self.servicos)
        return pecas + servicos

    @property
    def horas_totais(self):
        return sum((a.horas_trabalhadas or 0) for a in self.apontamentos)


class ItemOS(db.Model):
    __tablename__ = "itens_os"

    id_item_os = db.Column(db.Integer, primary_key=True)
    id_os = db.Column(db.Integer, db.ForeignKey("ordens_servico.id_os"), nullable=False)
    id_peca = db.Column(db.Integer, db.ForeignKey("pecas.id_peca"), nullable=False)
    quantidade = db.Column(db.Numeric(18, 3), nullable=False)
    valor_unitario = db.Column(db.Numeric(18, 2))
    valor_total = db.Column(db.Numeric(18, 2))

    os = db.relationship("OrdemServico", back_populates="itens")
    peca = db.relationship("Peca")


class ServicoOS(db.Model):
    __tablename__ = "servicos_os"

    id_servico_os = db.Column(db.Integer, primary_key=True)
    id_os = db.Column(db.Integer, db.ForeignKey("ordens_servico.id_os"), nullable=False)
    id_prestador = db.Column(db.Integer, db.ForeignKey("prestadores_servico.id_prestador"))
    descricao_servico = db.Column(db.String(200), nullable=False)
    valor_servico = db.Column(db.Numeric(18, 2))

    os = db.relationship("OrdemServico", back_populates="servicos")
    prestador = db.relationship("PrestadorServico", back_populates="servicos")


class ApontamentoOS(db.Model):
    __tablename__ = "apontamentos_os"

    id_apontamento = db.Column(db.Integer, primary_key=True)
    id_os = db.Column(db.Integer, db.ForeignKey("ordens_servico.id_os"), nullable=False)
    data_apontamento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tecnico = db.Column(db.String(100), nullable=False)
    horas_trabalhadas = db.Column(db.Numeric(5, 2))
    observacao = db.Column(db.String(500))

    os = db.relationship("OrdemServico", back_populates="apontamentos")
