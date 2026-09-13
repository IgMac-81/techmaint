"""Configuração da aplicação.

Tudo que muda entre o computador de cada pessoa (senha do banco, chave secreta)
fica aqui, lido de variáveis de ambiente. Nunca coloque senha dentro do código.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave-em-producao")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'techmaint.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Sessão / cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7 dias

    # Regras de negócio
    ITENS_POR_PAGINA = 20
    PERCENTUAL_ALERTA_ESTOQUE = 1.0  # alerta quando qtde <= estoque mínimo


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


CONFIGS = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}


def get_config(nome: str | None = None):
    return CONFIGS.get(nome or os.getenv("FLASK_ENV", "dev"), DevConfig)
