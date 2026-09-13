"""Testes de fumaça: provam que o sistema sobe e responde.

Rode com:  pytest -q
Se algum destes falhar, NÃO abra Pull Request — está quebrado.
"""

import pytest

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario


@pytest.fixture
def app():
    aplicacao = create_app("test")
    with aplicacao.app_context():
        db.create_all()
        usuario = Usuario(nome="Teste", login="teste", email="teste@techmaint.local")
        usuario.definir_senha("senha123")
        db.session.add(usuario)
        db.session.commit()
        yield aplicacao
        db.session.remove()
        db.drop_all()


@pytest.fixture
def cliente(app):
    return app.test_client()


def test_pagina_de_login_abre(cliente):
    resposta = cliente.get("/login")
    assert resposta.status_code == 200
    assert "TechMaint" in resposta.get_data(as_text=True)


def test_painel_exige_login(cliente):
    resposta = cliente.get("/", follow_redirects=False)
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_login_com_senha_certa_entra(cliente):
    resposta = cliente.post(
        "/login", data={"login": "teste", "senha": "senha123"}, follow_redirects=True
    )
    assert resposta.status_code == 200
    assert "Painel" in resposta.get_data(as_text=True)


def test_login_com_senha_errada_falha(cliente):
    resposta = cliente.post(
        "/login", data={"login": "teste", "senha": "errada"}, follow_redirects=True
    )
    assert "inválidos" in resposta.get_data(as_text=True)


def test_senha_nunca_e_salva_em_texto_puro(app):
    with app.app_context():
        usuario = db.session.scalar(db.select(Usuario).filter_by(login="teste"))
        assert usuario.senha_hash != "senha123"
        assert usuario.conferir_senha("senha123")


def test_service_worker_e_servido_na_raiz(cliente):
    resposta = cliente.get("/sw.js")
    assert resposta.status_code == 200
    assert resposta.headers["Service-Worker-Allowed"] == "/"


def test_manifest_existe(cliente):
    resposta = cliente.get("/static/manifest.webmanifest")
    assert resposta.status_code == 200
