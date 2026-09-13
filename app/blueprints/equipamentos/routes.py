"""CRUD de equipamentos — MÓDULO DE REFERÊNCIA.

Copie a ESTRUTURA deste arquivo ao criar os outros módulos (peças, fornecedores,
pedidos...). As cinco rotas abaixo (listar, novo, editar, excluir) são o mesmo
esqueleto que todo módulo de cadastro tem.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Optional

from app.extensions import db
from app.models.catalogo import Equipamento, Grupo, SubGrupo

bp = Blueprint("equipamentos", __name__)


class EquipamentoForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired(), Length(max=50)])
    descricao = StringField("Descrição", validators=[DataRequired(), Length(max=200)])
    ncm = StringField("NCM", validators=[Optional(), Length(max=8)])
    id_grupo = SelectField("Grupo", coerce=int, validators=[DataRequired()])
    id_subgrupo = SelectField("Subgrupo", coerce=int, validators=[DataRequired()])
    patrimoniado = BooleanField("Patrimoniado")
    vida_util_meses = IntegerField("Vida útil (meses)", validators=[Optional()])

    def carregar_opcoes(self):
        """SelectField precisa saber as opções ANTES de validar."""
        self.id_grupo.choices = [
            (g.id_grupo, g.grupo) for g in db.session.scalars(db.select(Grupo)).all()
        ]
        self.id_subgrupo.choices = [
            (s.id_subgrupo, s.subgrupo) for s in db.session.scalars(db.select(SubGrupo)).all()
        ]


@bp.route("/")
@login_required
def listar():
    busca = request.args.get("busca", "").strip()
    consulta = db.select(Equipamento).order_by(Equipamento.codigo)
    if busca:
        consulta = consulta.filter(Equipamento.descricao.ilike(f"%{busca}%"))
    equipamentos = db.session.scalars(consulta).all()
    return render_template(
        "equipamentos/listar.html", equipamentos=equipamentos, busca=busca
    )


@bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = EquipamentoForm()
    form.carregar_opcoes()
    if form.validate_on_submit():
        equipamento = Equipamento()
        form.populate_obj(equipamento)
        db.session.add(equipamento)
        db.session.commit()
        flash("Equipamento cadastrado com sucesso.", "sucesso")
        return redirect(url_for("equipamentos.listar"))
    return render_template("equipamentos/form.html", form=form, titulo="Novo equipamento")


@bp.route("/<int:id_equipamento>/editar", methods=["GET", "POST"])
@login_required
def editar(id_equipamento: int):
    equipamento = db.get_or_404(Equipamento, id_equipamento)
    form = EquipamentoForm(obj=equipamento)
    form.carregar_opcoes()
    if form.validate_on_submit():
        form.populate_obj(equipamento)
        db.session.commit()
        flash("Equipamento atualizado.", "sucesso")
        return redirect(url_for("equipamentos.listar"))
    return render_template("equipamentos/form.html", form=form, titulo="Editar equipamento")


@bp.route("/<int:id_equipamento>/excluir", methods=["POST"])
@login_required
def excluir(id_equipamento: int):
    equipamento = db.get_or_404(Equipamento, id_equipamento)
    db.session.delete(equipamento)
    db.session.commit()
    flash("Equipamento excluído.", "sucesso")
    return redirect(url_for("equipamentos.listar"))
