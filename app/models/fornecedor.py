"""Fornecedores, prestadores de serviço, notas fiscais e itens de nota."""

from app.extensions import db


class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id_fornecedor = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    fantasia = db.Column(db.String(100))
    cnpj = db.Column(db.String(14), unique=True, nullable=False, index=True)
    inscricao_estadual = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    ativo = db.Column(db.Boolean, default=True)

    notas = db.relationship("NotaFiscal", back_populates="fornecedor")

    def __repr__(self) -> str:
        return f"<Fornecedor {self.razao_social}>"


class PrestadorServico(db.Model):
    __tablename__ = "prestadores_servico"

    id_prestador = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    fantasia = db.Column(db.String(100))
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    inscricao_estadual = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    cep = db.Column(db.String(8))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    servicos = db.relationship("ServicoOS", back_populates="prestador")


class NotaFiscal(db.Model):
    __tablename__ = "notas_fiscais"

    id_nota_fiscal = db.Column(db.Integer, primary_key=True)
    id_fornecedor = db.Column(
        db.Integer, db.ForeignKey("fornecedores.id_fornecedor"), nullable=False
    )
    numero_nf = db.Column(db.Integer, nullable=False)
    chave_acesso_nfe = db.Column(db.String(44))
    serie_nf = db.Column(db.String(10))
    data_emissao = db.Column(db.Date)
    data_entrada = db.Column(db.Date)
    cfop = db.Column(db.String(4))
    valor_total_nf = db.Column(db.Numeric(18, 2))
    valor_frete = db.Column(db.Numeric(18, 2))
    valor_ipi = db.Column(db.Numeric(18, 2))
    valor_icms = db.Column(db.Numeric(18, 2))
    observacao = db.Column(db.String(500))

    fornecedor = db.relationship("Fornecedor", back_populates="notas")
    itens = db.relationship("ItemNotaFiscal", back_populates="nota", cascade="all, delete-orphan")


class ItemNotaFiscal(db.Model):
    __tablename__ = "itens_nota_fiscal"

    id_item_nf = db.Column(db.Integer, primary_key=True)
    id_nota_fiscal = db.Column(
        db.Integer, db.ForeignKey("notas_fiscais.id_nota_fiscal"), nullable=False
    )
    id_peca = db.Column(db.Integer, db.ForeignKey("pecas.id_peca"), nullable=False)
    descricao_item = db.Column(db.String(200))
    ncm = db.Column(db.String(8))
    cfop = db.Column(db.String(4))
    qtde = db.Column(db.Numeric(18, 3), nullable=False)
    valor_unitario = db.Column(db.Numeric(18, 2), nullable=False)
    valor_total = db.Column(db.Numeric(18, 2), nullable=False)

    nota = db.relationship("NotaFiscal", back_populates="itens")
    peca = db.relationship("Peca")
