"""Fábrica da aplicação (application factory).

Em vez de criar `app = Flask(__name__)` solto no topo do arquivo, criamos uma
FUNÇÃO que devolve a aplicação. Isso permite criar uma app de teste com outra
configuração sem duplicar código — é o padrão recomendado pela documentação
oficial do Flask.
"""

from pathlib import Path

from flask import Flask, render_template

from app.config import get_config
from app.extensions import csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    _registrar_extensoes(app)
    _registrar_blueprints(app)
    _registrar_pwa(app)
    _registrar_erros(app)
    _registrar_comandos(app)

    return app


def _registrar_extensoes(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def carregar_usuario(user_id: str):
        return db.session.get(Usuario, int(user_id))


def _registrar_blueprints(app: Flask) -> None:
    """Cada módulo do sistema é um blueprint — um 'mini-app' com suas rotas.

    Conforme cada dupla terminar seu módulo, descomente a linha correspondente.
    """
    from app.blueprints.auth.routes import bp as auth_bp
    from app.blueprints.dashboard.routes import bp as dashboard_bp
    from app.blueprints.equipamentos.routes import bp as equipamentos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(equipamentos_bp, url_prefix="/equipamentos")

    # from app.blueprints.pecas.routes import bp as pecas_bp
    # app.register_blueprint(pecas_bp, url_prefix="/pecas")
    # from app.blueprints.estoque.routes import bp as estoque_bp
    # app.register_blueprint(estoque_bp, url_prefix="/estoque")
    # from app.blueprints.fornecedores.routes import bp as fornecedores_bp
    # app.register_blueprint(fornecedores_bp, url_prefix="/fornecedores")
    # from app.blueprints.manutencao.routes import bp as manutencao_bp
    # app.register_blueprint(manutencao_bp, url_prefix="/manutencao")
    # from app.blueprints.relatorios.routes import bp as relatorios_bp
    # app.register_blueprint(relatorios_bp, url_prefix="/relatorios")


def _registrar_pwa(app: Flask) -> None:
    """O service worker precisa ser servido na RAIZ do site.

    Se ele for servido em /static/js/sw.js, o navegador só deixa ele controlar
    a pasta /static — e o app não funciona offline. Por isso este atalho.
    """
    from flask import make_response, send_from_directory

    @app.route("/sw.js")
    def service_worker():
        resposta = make_response(
            send_from_directory(app.static_folder, "js/sw.js")
        )
        resposta.headers["Content-Type"] = "application/javascript"
        resposta.headers["Service-Worker-Allowed"] = "/"
        resposta.headers["Cache-Control"] = "no-cache"
        return resposta

    @app.route("/offline")
    def offline():
        return render_template("offline.html")


def _registrar_erros(app: Flask) -> None:
    @app.errorhandler(403)
    def erro_403(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def erro_404(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def erro_500(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500


def _registrar_comandos(app: Flask) -> None:
    import click

    @app.cli.command("seed")
    def seed():
        """Popula o banco com dados de exemplo: flask seed"""
        from seeds.carregar import carregar_dados_exemplo

        carregar_dados_exemplo()
        click.echo("Dados de exemplo carregados.")
