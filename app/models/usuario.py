"""Usuários, perfis e permissões.

Relacionamentos (do documento de arquitetura):
    Usuarios  N:N  Perfis      (tabela de junção usuarios_perfis)
    Perfis    N:N  Permissoes  (tabela de junção perfis_permissoes)
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

usuarios_perfis = db.Table(
    "usuarios_perfis",
    db.Column("id_usuario", db.Integer, db.ForeignKey("usuarios.id_usuario"), primary_key=True),
    db.Column("id_perfil", db.Integer, db.ForeignKey("perfis.id_perfil"), primary_key=True),
)

perfis_permissoes = db.Table(
    "perfis_permissoes",
    db.Column("id_perfil", db.Integer, db.ForeignKey("perfis.id_perfil"), primary_key=True),
    db.Column(
        "id_permissao", db.Integer, db.ForeignKey("permissoes.id_permissao"), primary_key=True
    ),
)


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    perfis = db.relationship("Perfil", secondary=usuarios_perfis, back_populates="usuarios")

    # Flask-Login usa `get_id`; nossa PK não se chama `id`, então sobrescrevemos.
    def get_id(self) -> str:
        return str(self.id_usuario)

    @property
    def is_active(self) -> bool:
        return self.ativo

    def definir_senha(self, senha: str) -> None:
        """NUNCA guarde a senha em texto puro. Guardamos só o hash."""
        self.senha_hash = generate_password_hash(senha)

    def conferir_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def tem_perfil(self, nome_perfil: str) -> bool:
        return any(p.nome_perfil == nome_perfil for p in self.perfis)

    def tem_permissao(self, nome_permissao: str) -> bool:
        return any(
            perm.nome_permissao == nome_permissao for p in self.perfis for perm in p.permissoes
        )

    def __repr__(self) -> str:
        return f"<Usuario {self.login}>"


class Perfil(db.Model):
    __tablename__ = "perfis"

    id_perfil = db.Column(db.Integer, primary_key=True)
    nome_perfil = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))

    usuarios = db.relationship("Usuario", secondary=usuarios_perfis, back_populates="perfis")
    permissoes = db.relationship(
        "Permissao", secondary=perfis_permissoes, back_populates="perfis"
    )

    def __repr__(self) -> str:
        return f"<Perfil {self.nome_perfil}>"


class Permissao(db.Model):
    __tablename__ = "permissoes"

    id_permissao = db.Column(db.Integer, primary_key=True)
    nome_permissao = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(200))

    perfis = db.relationship("Perfil", secondary=perfis_permissoes, back_populates="permissoes")

    def __repr__(self) -> str:
        return f"<Permissao {self.nome_permissao}>"
