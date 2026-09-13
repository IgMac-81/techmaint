"""Painel inicial com os indicadores do sistema."""

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models.estoque import EstoquePeca
from app.models.manutencao import OrdemServico, PedidoManutencao

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    indicadores = {
        "pedidos_abertos": db.session.scalar(
            db.select(func.count(PedidoManutencao.id_pedido)).filter_by(status="ABERTO")
        )
        or 0,
        "os_em_execucao": db.session.scalar(
            db.select(func.count(OrdemServico.id_os)).filter_by(status="EM_EXECUCAO")
        )
        or 0,
        "os_concluidas": db.session.scalar(
            db.select(func.count(OrdemServico.id_os)).filter_by(status="CONCLUIDA")
        )
        or 0,
        "pecas_em_alerta": len(
            [e for e in db.session.scalars(db.select(EstoquePeca)).all() if e.abaixo_do_minimo]
        ),
    }
    return render_template("dashboard/index.html", indicadores=indicadores)
