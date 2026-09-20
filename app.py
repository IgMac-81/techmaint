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

# Opcoes do campo status. Ficam numa lista para nao repetir no HTML
# e para ser facil adicionar uma opcao nova depois.
STATUS_POSSIVEIS = ["Operando", "Em manutencao", "Parado"]


# ---------------------------------------------------------------------------
# READ - lista todos (pagina inicial)
# ---------------------------------------------------------------------------
@app.route("/")
def listar():
    # `request.args` le o que vem na URL depois do `?`.
    # Exemplo: /?busca=torno  ->  busca == "torno"
    busca = request.args.get("busca", "")
    equipamentos = database.listar_equipamentos(busca)
    # `render_template` procura o arquivo dentro da pasta templates/.
    # Tudo que vem depois do nome do arquivo vira variavel dentro do HTML.
    return render_template("listar.html", equipamentos=equipamentos, busca=busca)


# ---------------------------------------------------------------------------
# CREATE - formulario vazio (GET) e gravacao (POST)
# ---------------------------------------------------------------------------
@app.route("/novo", methods=["GET", "POST"])
def novo():
    """Uma rota, dois comportamentos:

    GET  = o navegador so quer VER o formulario.
    POST = o usuario clicou em Salvar e esta ENVIANDO os dados.
    """
    if request.method == "POST":
        # `request.form` le os campos do formulario.
        # A chave e o `name=` do input no HTML.
        nome = request.form["nome"].strip()
        setor = request.form["setor"].strip()
        status = request.form["status"]

        # Validacao simples: campo obrigatorio nao pode vir vazio.
        if not nome or not setor:
            flash("Preencha nome e setor.", "erro")
            # Devolve o formulario com o que o usuario ja tinha digitado.
            return render_template(
                "form.html",
                titulo="Novo equipamento",
                equipamento=request.form,
                status_possiveis=STATUS_POSSIVEIS,
            )

        database.criar_equipamento(nome, setor, status)
        flash("Equipamento criado.", "sucesso")
        # Depois de gravar, SEMPRE redirecione. Isso evita que o usuario
        # reenvie o formulario ao apertar F5. (Padrao Post/Redirect/Get.)
        return redirect(url_for("listar"))

    # Caso GET: formulario em branco.
    return render_template(
        "form.html",
        titulo="Novo equipamento",
        equipamento=None,
        status_possiveis=STATUS_POSSIVEIS,
    )


# ---------------------------------------------------------------------------
# UPDATE - formulario preenchido (GET) e gravacao (POST)
# ---------------------------------------------------------------------------
# O `<int:id_do_equipamento>` captura um pedaco da URL e entrega
# como argumento da funcao. /editar/7 -> id_do_equipamento == 7
@app.route("/editar/<int:id_do_equipamento>", methods=["GET", "POST"])
def editar(id_do_equipamento):
    equipamento = database.buscar_equipamento(id_do_equipamento)

    # Id que nao existe: avisa e volta para a lista.
    if equipamento is None:
        flash("Equipamento nao encontrado.", "erro")
        return redirect(url_for("listar"))

    if request.method == "POST":
        nome = request.form["nome"].strip()
        setor = request.form["setor"].strip()
        status = request.form["status"]

        if not nome or not setor:
            flash("Preencha nome e setor.", "erro")
            return render_template(
                "form.html",
                titulo="Editar equipamento",
                equipamento=request.form,
                status_possiveis=STATUS_POSSIVEIS,
            )

        database.atualizar_equipamento(id_do_equipamento, nome, setor, status)
        flash("Equipamento atualizado.", "sucesso")
        return redirect(url_for("listar"))

    # Caso GET: formulario preenchido com os dados atuais.
    return render_template(
        "form.html",
        titulo="Editar equipamento",
        equipamento=equipamento,
        status_possiveis=STATUS_POSSIVEIS,
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
