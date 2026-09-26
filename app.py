"""
app.py
------
O coracao da aplicacao: aqui ficam as ROTAS.

Rota = um endereco do navegador ligado a uma funcao Python.
Quando alguem abre http://127.0.0.1:5000/, o Flask executa a funcao
que estiver marcada com @app.route("/").

Fluxo de uma pagina:
    navegador  ->  rota (app.py)  ->  banco (database.py)  ->  HTML (templates/)

Para rodar:
    python app.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash

import database

# Cria a aplicacao. O `__name__` diz ao Flask onde procurar
# as pastas `templates/` e `static/`.
app = Flask(__name__)

# Chave usada para assinar as mensagens flash (os avisos verdes do topo).
# Em um projeto real, isso vem de uma variavel de ambiente, nunca do codigo.
app.secret_key = "troque-esta-chave-em-producao"

def _ler_dados_formulario():
    """Le e valida os campos do formulario de equipamentos."""
    codigo = request.form.get("Codigo", "").strip().upper()
    descricao = request.form.get("Descricao", "").strip().upper()
    id_departamento_texto = request.form.get("IdDepartamento", "").strip()
    id_grupo_texto = request.form.get("IdGrupo", "").strip()
    id_subgrupo_texto = request.form.get("IdSubGrupo", "").strip()

    if not codigo or not descricao or not id_grupo_texto or not id_subgrupo_texto:
        return None

    try:
        id_departamento = (
            int(id_departamento_texto) if id_departamento_texto else None
        )
        id_grupo = int(id_grupo_texto)
        id_subgrupo = int(id_subgrupo_texto)
    except ValueError:
        return None

    grupo = database.buscar_grupo(id_grupo)
    subgrupo = database.buscar_subgrupo(id_subgrupo)
    departamento = (
        database.buscar_departamento(id_departamento)
        if id_departamento is not None
        else None
    )
    if (
        grupo is None
        or subgrupo is None
        or subgrupo["IdGrupo"] != id_grupo
        or (id_departamento is not None and departamento is None)
    ):
        return None

    return (
        codigo,
        descricao,
        id_departamento,
        departamento["NomeDepartamento"] if departamento else None,
        id_grupo,
        grupo["Grupo"],
        id_subgrupo,
        subgrupo["Subgrupo"],
    )


# ---------------------------------------------------------------------------
# READ - lista todos (pagina inicial)
# ---------------------------------------------------------------------------
@app.route("/")
def listar():
    # `request.args` le o que vem na URL depois do `?`.
    # Exemplo: /?busca=torno  ->  busca == "torno"
    busca = request.args.get("busca", "").strip().upper()
    equipamentos = database.listar_equipamentos(busca)
    # `render_template` procura o arquivo dentro da pasta templates/.
    # Tudo que vem depois do nome do arquivo vira variavel dentro do HTML.
    return render_template("listar.html", equipamentos=equipamentos, busca=busca)


# ---------------------------------------------------------------------------
# GRUPOS - cadastro, edicao e exclusao
# ---------------------------------------------------------------------------
@app.route("/grupos", methods=["GET", "POST"])
def grupos():
    busca = request.args.get("busca", "").strip().upper()
    if request.method == "POST":
        nome_grupo = request.form.get("Grupo", "").strip().upper()
        if not nome_grupo:
            flash("Informe o nome do grupo.", "erro")
        elif database.criar_grupo(nome_grupo):
            flash("Grupo cadastrado.", "sucesso")
        else:
            flash("O grupo já existe.", "erro")
        return redirect(url_for("grupos"))

    return render_template(
        "grupos.html",
        grupos=database.listar_grupos(busca),
        busca=busca,
    )


# ---------------------------------------------------------------------------
# SUBGRUPOS - cadastro, edicao e exclusao
# ---------------------------------------------------------------------------
@app.route("/subgrupos", methods=["GET", "POST"])
def subgrupos():
    grupos_disponiveis = database.listar_grupos()
    busca = request.args.get("busca", "").strip().upper()
    if request.method == "POST":
        nome_subgrupo = request.form.get("Subgrupo", "").strip().upper()
        id_grupo_texto = request.form.get("IdGrupo", "").strip()
        try:
            id_grupo = int(id_grupo_texto)
        except ValueError:
            id_grupo = None

        if not nome_subgrupo or id_grupo is None:
            flash("Informe o subgrupo e selecione um grupo.", "erro")
        elif database.buscar_grupo(id_grupo) is None:
            flash("O grupo selecionado não existe.", "erro")
        elif database.criar_subgrupo(nome_subgrupo, id_grupo):
            flash("Subgrupo cadastrado.", "sucesso")
        else:
            flash("O subgrupo já existe.", "erro")
        return redirect(url_for("subgrupos"))

    return render_template(
        "subgrupos.html",
        subgrupos=database.listar_subgrupos(busca),
        grupos=grupos_disponiveis,
        busca=busca,
    )


# ---------------------------------------------------------------------------
# DEPARTAMENTOS - cadastro, edicao e exclusao
# ---------------------------------------------------------------------------
@app.route("/departamentos", methods=["GET", "POST"])
def departamentos():
    busca = request.args.get("busca", "").strip().upper()
    if request.method == "POST":
        nome = request.form.get("NomeDepartamento", "").strip().upper()
        responsavel = request.form.get("Responsavel", "").strip().upper() or None
        if not nome:
            flash("Informe o nome do departamento.", "erro")
        elif database.criar_departamento(nome, responsavel):
            flash("Departamento cadastrado.", "sucesso")
        else:
            flash("O departamento já existe.", "erro")
        return redirect(url_for("departamentos"))

    return render_template(
        "departamentos.html",
        departamentos=database.listar_departamentos(busca),
        busca=busca,
    )


@app.route("/departamentos/editar/<int:id_departamento>", methods=["GET", "POST"])
def editar_departamento(id_departamento):
    departamento = database.buscar_departamento(id_departamento)
    if departamento is None:
        flash("Departamento não encontrado.", "erro")
        return redirect(url_for("departamentos"))

    if request.method == "POST":
        nome = request.form.get("NomeDepartamento", "").strip().upper()
        responsavel = request.form.get("Responsavel", "").strip().upper() or None
        if not nome:
            flash("Informe o nome do departamento.", "erro")
        elif database.atualizar_departamento(id_departamento, nome, responsavel):
            flash("Departamento atualizado.", "sucesso")
            return redirect(url_for("departamentos"))
        else:
            flash("O departamento já existe.", "erro")
        departamento = database.buscar_departamento(id_departamento)

    return render_template(
        "departamentos.html",
        departamentos=database.listar_departamentos(),
        departamento_edicao=departamento,
    )


@app.route("/departamentos/apagar/<int:id_departamento>", methods=["POST"])
def apagar_departamento(id_departamento):
    try:
        database.apagar_departamento(id_departamento)
    except ValueError as erro:
        flash(str(erro), "erro")
    else:
        flash("Departamento excluído.", "sucesso")
    return redirect(url_for("departamentos"))


@app.route("/subgrupos/editar/<int:id_subgrupo>", methods=["GET", "POST"])
def editar_subgrupo(id_subgrupo):
    subgrupo = database.buscar_subgrupo(id_subgrupo)
    grupos_disponiveis = database.listar_grupos()
    if subgrupo is None:
        flash("Subgrupo não encontrado.", "erro")
        return redirect(url_for("subgrupos"))

    if request.method == "POST":
        nome_subgrupo = request.form.get("Subgrupo", "").strip().upper()
        id_grupo_texto = request.form.get("IdGrupo", "").strip()
        try:
            id_grupo = int(id_grupo_texto)
        except ValueError:
            id_grupo = None

        if not nome_subgrupo or id_grupo is None:
            flash("Informe o subgrupo e selecione um grupo.", "erro")
        elif database.buscar_grupo(id_grupo) is None:
            flash("O grupo selecionado não existe.", "erro")
        elif database.atualizar_subgrupo(id_subgrupo, nome_subgrupo, id_grupo):
            flash("Subgrupo atualizado.", "sucesso")
            return redirect(url_for("subgrupos"))
        else:
            flash("O subgrupo já existe.", "erro")
        subgrupo = database.buscar_subgrupo(id_subgrupo)

    return render_template(
        "subgrupos.html",
        subgrupos=database.listar_subgrupos(),
        grupos=grupos_disponiveis,
        subgrupo_edicao=subgrupo,
    )


@app.route("/subgrupos/apagar/<int:id_subgrupo>", methods=["POST"])
def apagar_subgrupo(id_subgrupo):
    try:
        database.apagar_subgrupo(id_subgrupo)
    except ValueError as erro:
        flash(str(erro), "erro")
    else:
        flash("Subgrupo excluído.", "sucesso")
    return redirect(url_for("subgrupos"))


@app.route("/grupos/editar/<int:id_grupo>", methods=["GET", "POST"])
def editar_grupo(id_grupo):
    grupo = database.buscar_grupo(id_grupo)
    if grupo is None:
        flash("Grupo não encontrado.", "erro")
        return redirect(url_for("grupos"))

    if request.method == "POST":
        nome_grupo = request.form.get("Grupo", "").strip().upper()
        if not nome_grupo:
            flash("Informe o nome do grupo.", "erro")
        elif database.atualizar_grupo(id_grupo, nome_grupo):
            flash("Grupo atualizado.", "sucesso")
            return redirect(url_for("grupos"))
        else:
            flash("O grupo já existe.", "erro")
        grupo = database.buscar_grupo(id_grupo)

    return render_template(
        "grupos.html",
        grupos=database.listar_grupos(),
        grupo_edicao=grupo,
    )


@app.route("/grupos/apagar/<int:id_grupo>", methods=["POST"])
def apagar_grupo(id_grupo):
    try:
        database.apagar_grupo(id_grupo)
    except ValueError as erro:
        flash(str(erro), "erro")
    else:
        flash("Grupo excluído.", "sucesso")
    return redirect(url_for("grupos"))


# ---------------------------------------------------------------------------
# CREATE - formulario vazio (GET) e gravacao (POST)
# ---------------------------------------------------------------------------
@app.route("/novo", methods=["GET", "POST"])
def novo():
    """Uma rota, dois comportamentos:

    GET  = o navegador so quer VER o formulario.
    POST = o usuario clicou em Salvar e esta ENVIANDO os dados.
    """
    grupos = database.listar_grupos()
    subgrupos = database.listar_subgrupos()
    departamentos = database.listar_departamentos()
    if request.method == "POST":
        # `request.form` le os campos do formulario.
        # A chave e o `name=` do input no HTML.
        dados = _ler_dados_formulario()

        # Validacao simples: campo obrigatorio nao pode vir vazio.
        if dados is None:
            flash("Preencha todos os campos.", "erro")
            # Devolve o formulario com o que o usuario ja tinha digitado.
            return render_template(
                "form.html",
                titulo="Novo equipamento",
                equipamento=request.form,
                grupos=grupos,
                subgrupos=subgrupos,
                departamentos=departamentos,
            )

        database.criar_equipamento(*dados)
        flash("Equipamento criado.", "sucesso")
        # Depois de gravar, SEMPRE redirecione. Isso evita que o usuario
        # reenvie o formulario ao apertar F5. (Padrao Post/Redirect/Get.)
        return redirect(url_for("listar"))

    # Caso GET: formulario em branco.
    return render_template(
        "form.html",
        titulo="Novo equipamento",
        equipamento=None,
        grupos=grupos,
        subgrupos=subgrupos,
        departamentos=departamentos,
    )


# ---------------------------------------------------------------------------
# UPDATE - formulario preenchido (GET) e gravacao (POST)
# ---------------------------------------------------------------------------
# O `<int:id_do_equipamento>` captura um pedaco da URL e entrega
# como argumento da funcao. /editar/7 -> id_do_equipamento == 7
@app.route("/editar/<int:id_do_equipamento>", methods=["GET", "POST"])
def editar(id_do_equipamento):
    equipamento = database.buscar_equipamento(id_do_equipamento)
    grupos = database.listar_grupos()
    subgrupos = database.listar_subgrupos()
    departamentos = database.listar_departamentos()

    # Id que nao existe: avisa e volta para a lista.
    if equipamento is None:
        flash("Equipamento nao encontrado.", "erro")
        return redirect(url_for("listar"))

    if request.method == "POST":
        dados = _ler_dados_formulario()

        if dados is None:
            flash("Preencha todos os campos.", "erro")
            return render_template(
                "form.html",
                titulo="Editar equipamento",
                equipamento=request.form,
                grupos=grupos,
                subgrupos=subgrupos,
                departamentos=departamentos,
                id_do_equipamento=id_do_equipamento,
            )

        database.atualizar_equipamento(id_do_equipamento, *dados)
        flash("Equipamento atualizado.", "sucesso")
        return redirect(url_for("listar"))

    # Caso GET: formulario preenchido com os dados atuais.
    return render_template(
        "form.html",
        titulo="Editar equipamento",
        equipamento=equipamento,
        grupos=grupos,
        subgrupos=subgrupos,
        departamentos=departamentos,
        id_do_equipamento=id_do_equipamento,
    )


# ---------------------------------------------------------------------------
# DELETE - so aceita POST
# ---------------------------------------------------------------------------
# Por que so POST? Porque link (GET) pode ser aberto por engano, pelo
# navegador ou por um robo. Acao que apaga dado sempre vai em formulario.
@app.route("/apagar/<int:id_do_equipamento>", methods=["POST"])
def apagar(id_do_equipamento):
    database.apagar_equipamento(id_do_equipamento)
    flash("Equipamento apagado.", "sucesso")
    return redirect(url_for("listar"))


if __name__ == "__main__":
    # Garante que a tabela existe antes de atender a primeira visita.
    database.criar_tabelas()
    # debug=True recarrega o servidor a cada alteracao de arquivo e
    # mostra o erro completo na tela. Use so no seu computador.
    app.run(debug=True)
