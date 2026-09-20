"""
database.py
-----------
Tudo que fala com o banco de dados (SQLite) mora aqui.

Por que separar em um arquivo só?
- app.py cuida das telas (rotas)
- database.py cuida dos dados (SQL)
Assim, quando você criar uma nova entidade, copia este arquivo e troca o SQL.

SQLite é um banco de dados que vive em um arquivo unico (techmaint.db).
Nao precisa instalar servidor nenhum: ja vem junto com o Python.
"""

import sqlite3

# Nome do arquivo do banco. Ele e criado sozinho na primeira execucao.
NOME_DO_BANCO = "techmaint.db"


def conectar():
    """Abre uma conexao com o banco e devolve ela.

    O `row_factory = sqlite3.Row` faz cada linha do resultado virar algo
    parecido com um dicionario. Sem ele, voce acessaria por posicao
    (`linha[0]`, `linha[1]`). Com ele, acessa por nome (`linha["nome"]`),
    que e muito mais facil de ler no HTML.
    """
    conexao = sqlite3.connect(NOME_DO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    """Cria a tabela caso ela ainda nao exista.

    Roda toda vez que o app sobe. O `IF NOT EXISTS` garante que nada
    seja apagado se a tabela ja estiver la.
    """
    conexao = conectar()
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS equipamentos (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nome   TEXT NOT NULL,
            setor  TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conexao.commit()
    conexao.close()


# ---------------------------------------------------------------------------
# As quatro operacoes do CRUD
#
#   C = Create  (criar)   -> criar_equipamento()
#   R = Read    (ler)     -> listar_equipamentos() e buscar_equipamento()
#   U = Update  (alterar) -> atualizar_equipamento()
#   D = Delete  (apagar)  -> apagar_equipamento()
#
# Repare que TODA consulta usa `?` no lugar dos valores. Isso se chama
# "query parametrizada" e protege contra SQL Injection. Nunca monte SQL
# com f-string ou com `+`.
# ---------------------------------------------------------------------------


def listar_equipamentos(busca=""):
    """READ: devolve a lista de equipamentos, com filtro opcional por nome."""
    conexao = conectar()
    if busca:
        # O `%` do LIKE significa "qualquer coisa antes ou depois".
        linhas = conexao.execute(
            "SELECT * FROM equipamentos WHERE nome LIKE ? ORDER BY id DESC",
            (f"%{busca}%",),
        ).fetchall()
    else:
        linhas = conexao.execute(
            "SELECT * FROM equipamentos ORDER BY id DESC"
        ).fetchall()
    conexao.close()
    return linhas


def buscar_equipamento(id_do_equipamento):
    """READ: devolve UM equipamento pelo id (ou None se nao existir).

    Usado na tela de edicao, para preencher o formulario.
    """
    conexao = conectar()
    linha = conexao.execute(
        "SELECT * FROM equipamentos WHERE id = ?", (id_do_equipamento,)
    ).fetchone()
    conexao.close()
    return linha


def criar_equipamento(nome, setor, status):
    """CREATE: insere um novo equipamento."""
    conexao = conectar()
    conexao.execute(
        "INSERT INTO equipamentos (nome, setor, status) VALUES (?, ?, ?)",
        (nome, setor, status),
    )
    # `commit` = confirma a gravacao. Sem ele, nada e salvo de verdade.
    conexao.commit()
    conexao.close()


def atualizar_equipamento(id_do_equipamento, nome, setor, status):
    """UPDATE: altera um equipamento existente.

    Cuidado: UPDATE sem WHERE altera a tabela inteira. O WHERE e obrigatorio.
    """
    conexao = conectar()
    conexao.execute(
        "UPDATE equipamentos SET nome = ?, setor = ?, status = ? WHERE id = ?",
        (nome, setor, status, id_do_equipamento),
    )
    conexao.commit()
    conexao.close()


def apagar_equipamento(id_do_equipamento):
    """DELETE: remove um equipamento pelo id."""
    conexao = conectar()
    conexao.execute(
        "DELETE FROM equipamentos WHERE id = ?", (id_do_equipamento,)
    )
    conexao.commit()
    conexao.close()
