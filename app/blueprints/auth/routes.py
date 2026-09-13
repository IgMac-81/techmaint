"""Login, logout e proteção de rotas."""

from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Length

from app.extensions import db
from app.models.usuario import Usuario

bp = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    login = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=50)])
    senha = PasswordField("Senha", validators=[DataRequired()])
    lembrar = BooleanField("Continuar conectado")


def requer_perfil(*perfis: str):
    """Decorador de autorização.

    Uso:
        @bp.route("/usuarios")
        @requer_perfil("ADMINISTRADOR")
        def listar_usuarios(): ...
    """

    def decorador(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            if not any(current_user.tem_perfil(p) for p in perfis):
                abort(403)
            return view(*args, **kwargs)

        return wrapper

    return decorador


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = db.session.scalar(db.select(Usuario).filter_by(login=form.login.data))
        if usuario and usuario.ativo and usuario.conferir_senha(form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            destino = request.args.get("next") or url_for("dashboard.index")
            return redirect(destino)
        flash("Usuário ou senha inválidos.", "erro")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))
